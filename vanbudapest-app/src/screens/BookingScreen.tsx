import React, { useState, useMemo } from 'react';
import {
  View,
  ScrollView,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import { format, addDays } from 'date-fns';
import { hu } from 'date-fns/locale';
import { RootStackParamList, BookingRequest } from '../types';
import { SERVICES, getAvailableSlots, validateEmail, validatePhone, submitBooking } from '../services/booking';
import { LoadingSpinner } from '../components';
import { colors, spacing } from '../utils/helpers';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export function BookingScreen() {
  const navigation = useNavigation<NavigationProp>();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  // Form state
  const [selectedService, setSelectedService] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [selectedTime, setSelectedTime] = useState<string | null>(null);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [notes, setNotes] = useState('');

  // Generált dátumok (következő 14 nap)
  const availableDates = useMemo(() => {
    const dates = [];
    const today = new Date();
    for (let i = 1; i <= 14; i++) {
      const date = addDays(today, i);
      // Hétvégék kizárása
      if (date.getDay() !== 0 && date.getDay() !== 6) {
        dates.push({
          value: format(date, 'yyyy-MM-dd'),
          label: format(date, 'MMMM d. (EEEE)', { locale: hu }),
        });
      }
    }
    return dates;
  }, []);

  // Elérhető időpontok
  const timeSlots = useMemo(() => {
    if (!selectedDate) return [];
    return getAvailableSlots(selectedDate);
  }, [selectedDate]);

  const selectedServiceDetails = SERVICES.find(s => s.id === selectedService);

  const canProceed = () => {
    switch (step) {
      case 1:
        return selectedService !== null;
      case 2:
        return selectedDate !== null && selectedTime !== null;
      case 3:
        return name.trim() && validateEmail(email) && validatePhone(phone);
      default:
        return false;
    }
  };

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      handleSubmit();
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async () => {
    if (!selectedService || !selectedDate || !selectedTime) return;

    const booking: BookingRequest = {
      name: name.trim(),
      email: email.trim(),
      phone: phone.trim(),
      date: selectedDate,
      time: selectedTime,
      service: selectedServiceDetails?.name || selectedService,
      notes: notes.trim(),
    };

    setLoading(true);
    try {
      const confirmation = await submitBooking(booking);
      Alert.alert(
        'Foglalás elküldve!',
        `Köszönjük a foglalást, ${name}!\n\nFoglalás azonosító: ${confirmation.id}\n\nHamarosan felvesszük Önnel a kapcsolatot a megadott elérhetőségeken.`,
        [
          {
            text: 'Rendben',
            onPress: () => {
              // Reset form
              setStep(1);
              setSelectedService(null);
              setSelectedDate(null);
              setSelectedTime(null);
              setName('');
              setEmail('');
              setPhone('');
              setNotes('');
            },
          },
        ]
      );
    } catch (err) {
      Alert.alert('Hiba', 'Nem sikerült elküldeni a foglalást. Kérjük próbálja újra.');
    } finally {
      setLoading(false);
    }
  };

  const renderStep1 = () => (
    <View style={styles.stepContent}>
      <Text style={styles.stepTitle}>Válasszon szolgáltatást</Text>
      <Text style={styles.stepSubtitle}>Melyik szolgáltatásunkat szeretné igénybe venni?</Text>

      {SERVICES.map((service) => (
        <TouchableOpacity
          key={service.id}
          style={[
            styles.serviceCard,
            selectedService === service.id && styles.serviceCardSelected,
          ]}
          onPress={() => setSelectedService(service.id)}
        >
          <View style={styles.serviceInfo}>
            <Text style={styles.serviceName}>{service.name}</Text>
            <Text style={styles.serviceDuration}>{service.duration} perc</Text>
          </View>
          <Text style={styles.servicePrice}>{service.price}</Text>
          {selectedService === service.id && (
            <Ionicons name="checkmark-circle" size={24} color={colors.primary} />
          )}
        </TouchableOpacity>
      ))}
    </View>
  );

  const renderStep2 = () => (
    <View style={styles.stepContent}>
      <Text style={styles.stepTitle}>Válasszon időpontot</Text>
      <Text style={styles.stepSubtitle}>
        {selectedServiceDetails?.name} - {selectedServiceDetails?.duration} perc
      </Text>

      <Text style={styles.sectionLabel}>Dátum</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.dateScroll}>
        {availableDates.map((date) => (
          <TouchableOpacity
            key={date.value}
            style={[
              styles.dateChip,
              selectedDate === date.value && styles.dateChipSelected,
            ]}
            onPress={() => {
              setSelectedDate(date.value);
              setSelectedTime(null);
            }}
          >
            <Text
              style={[
                styles.dateChipText,
                selectedDate === date.value && styles.dateChipTextSelected,
              ]}
            >
              {date.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {selectedDate && (
        <>
          <Text style={styles.sectionLabel}>Időpont</Text>
          <View style={styles.timeGrid}>
            {timeSlots.map((slot) => (
              <TouchableOpacity
                key={slot.id}
                style={[
                  styles.timeSlot,
                  !slot.available && styles.timeSlotUnavailable,
                  selectedTime === slot.time && styles.timeSlotSelected,
                ]}
                onPress={() => slot.available && setSelectedTime(slot.time)}
                disabled={!slot.available}
              >
                <Text
                  style={[
                    styles.timeSlotText,
                    !slot.available && styles.timeSlotTextUnavailable,
                    selectedTime === slot.time && styles.timeSlotTextSelected,
                  ]}
                >
                  {slot.time}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </>
      )}
    </View>
  );

  const renderStep3 = () => (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      style={styles.stepContent}
    >
      <Text style={styles.stepTitle}>Kapcsolati adatok</Text>
      <Text style={styles.stepSubtitle}>Kérjük adja meg elérhetőségeit</Text>

      <View style={styles.summaryBox}>
        <Text style={styles.summaryTitle}>{selectedServiceDetails?.name}</Text>
        <Text style={styles.summaryDetail}>
          {availableDates.find(d => d.value === selectedDate)?.label} - {selectedTime}
        </Text>
        <Text style={styles.summaryPrice}>{selectedServiceDetails?.price}</Text>
      </View>

      <Text style={styles.inputLabel}>Név *</Text>
      <TextInput
        style={styles.input}
        value={name}
        onChangeText={setName}
        placeholder="Teljes név"
        autoCapitalize="words"
      />

      <Text style={styles.inputLabel}>E-mail cím *</Text>
      <TextInput
        style={[styles.input, email && !validateEmail(email) && styles.inputError]}
        value={email}
        onChangeText={setEmail}
        placeholder="pelda@email.com"
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <Text style={styles.inputLabel}>Telefonszám *</Text>
      <TextInput
        style={[styles.input, phone && !validatePhone(phone) && styles.inputError]}
        value={phone}
        onChangeText={setPhone}
        placeholder="+36 30 123 4567"
        keyboardType="phone-pad"
      />

      <Text style={styles.inputLabel}>Megjegyzés (opcionális)</Text>
      <TextInput
        style={[styles.input, styles.inputMultiline]}
        value={notes}
        onChangeText={setNotes}
        placeholder="Egyéb kérés vagy megjegyzés..."
        multiline
        numberOfLines={3}
      />
    </KeyboardAvoidingView>
  );

  if (loading) {
    return <LoadingSpinner fullScreen message="Foglalás küldése..." />;
  }

  return (
    <View style={styles.container}>
      {/* Progress indicator */}
      <View style={styles.progress}>
        {[1, 2, 3].map((s) => (
          <View
            key={s}
            style={[
              styles.progressDot,
              s <= step && styles.progressDotActive,
              s === step && styles.progressDotCurrent,
            ]}
          />
        ))}
      </View>

      <ScrollView style={styles.scrollView} keyboardShouldPersistTaps="handled">
        {step === 1 && renderStep1()}
        {step === 2 && renderStep2()}
        {step === 3 && renderStep3()}
      </ScrollView>

      {/* Bottom navigation */}
      <View style={styles.bottomNav}>
        {step > 1 && (
          <TouchableOpacity style={styles.backButton} onPress={handleBack}>
            <Ionicons name="arrow-back" size={20} color={colors.primary} />
            <Text style={styles.backButtonText}>Vissza</Text>
          </TouchableOpacity>
        )}
        <TouchableOpacity
          style={[styles.nextButton, !canProceed() && styles.nextButtonDisabled]}
          onPress={handleNext}
          disabled={!canProceed()}
        >
          <Text style={styles.nextButtonText}>
            {step === 3 ? 'Foglalás elküldése' : 'Tovább'}
          </Text>
          <Ionicons name="arrow-forward" size={20} color={colors.surface} />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  progress: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: spacing.md,
    backgroundColor: colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  progressDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: colors.border,
    marginHorizontal: spacing.sm,
  },
  progressDotActive: {
    backgroundColor: colors.primaryLight,
  },
  progressDotCurrent: {
    backgroundColor: colors.primary,
    width: 14,
    height: 14,
    borderRadius: 7,
  },
  scrollView: {
    flex: 1,
  },
  stepContent: {
    padding: spacing.md,
  },
  stepTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: colors.text,
    marginBottom: spacing.xs,
  },
  stepSubtitle: {
    fontSize: 14,
    color: colors.textSecondary,
    marginBottom: spacing.lg,
  },
  serviceCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    padding: spacing.md,
    borderRadius: 12,
    marginBottom: spacing.sm,
    borderWidth: 2,
    borderColor: colors.border,
  },
  serviceCardSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primaryLight + '10',
  },
  serviceInfo: {
    flex: 1,
  },
  serviceName: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
  },
  serviceDuration: {
    fontSize: 13,
    color: colors.textSecondary,
    marginTop: 2,
  },
  servicePrice: {
    fontSize: 16,
    fontWeight: '700',
    color: colors.primary,
    marginRight: spacing.sm,
  },
  sectionLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.text,
    marginBottom: spacing.sm,
    marginTop: spacing.md,
  },
  dateScroll: {
    marginHorizontal: -spacing.md,
    paddingHorizontal: spacing.md,
  },
  dateChip: {
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: 8,
    marginRight: spacing.sm,
    borderWidth: 1,
    borderColor: colors.border,
  },
  dateChipSelected: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  dateChipText: {
    fontSize: 13,
    color: colors.text,
  },
  dateChipTextSelected: {
    color: colors.surface,
    fontWeight: '600',
  },
  timeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -spacing.xs,
  },
  timeSlot: {
    width: '30%',
    backgroundColor: colors.surface,
    paddingVertical: spacing.sm,
    borderRadius: 8,
    margin: spacing.xs,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: colors.border,
  },
  timeSlotUnavailable: {
    backgroundColor: colors.border + '50',
    borderColor: colors.border,
  },
  timeSlotSelected: {
    backgroundColor: colors.primary,
    borderColor: colors.primary,
  },
  timeSlotText: {
    fontSize: 15,
    fontWeight: '500',
    color: colors.text,
  },
  timeSlotTextUnavailable: {
    color: colors.textSecondary,
    textDecorationLine: 'line-through',
  },
  timeSlotTextSelected: {
    color: colors.surface,
  },
  summaryBox: {
    backgroundColor: colors.primaryLight + '20',
    padding: spacing.md,
    borderRadius: 12,
    marginBottom: spacing.lg,
  },
  summaryTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: colors.primary,
  },
  summaryDetail: {
    fontSize: 14,
    color: colors.text,
    marginTop: spacing.xs,
  },
  summaryPrice: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.primaryDark,
    marginTop: spacing.xs,
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: '500',
    color: colors.text,
    marginBottom: spacing.xs,
    marginTop: spacing.sm,
  },
  input: {
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 8,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    fontSize: 16,
    color: colors.text,
  },
  inputError: {
    borderColor: colors.error,
  },
  inputMultiline: {
    height: 80,
    textAlignVertical: 'top',
  },
  bottomNav: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: spacing.md,
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    marginRight: 'auto',
  },
  backButtonText: {
    fontSize: 15,
    color: colors.primary,
    marginLeft: spacing.xs,
  },
  nextButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    borderRadius: 8,
  },
  nextButtonDisabled: {
    backgroundColor: colors.border,
  },
  nextButtonText: {
    fontSize: 15,
    fontWeight: '600',
    color: colors.surface,
    marginRight: spacing.xs,
  },
});
