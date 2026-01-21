import React, { useEffect, useState } from 'react';
import {
  View,
  ScrollView,
  Text,
  Image,
  TouchableOpacity,
  Linking,
  StyleSheet,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { getSiteInfo } from '../services/wordpress';
import { colors, spacing } from '../utils/helpers';

export function AboutScreen() {
  const [siteInfo, setSiteInfo] = useState<{
    name: string;
    description: string;
    URL: string;
    icon?: { img: string };
  } | null>(null);

  useEffect(() => {
    getSiteInfo().then(setSiteInfo).catch(console.error);
  }, []);

  const openUrl = (url: string) => {
    Linking.openURL(url).catch(console.error);
  };

  const contactItems = [
    {
      icon: 'globe-outline' as const,
      label: 'Weboldal',
      value: 'vanbudapest.com',
      action: () => openUrl('https://vanbudapest.com'),
    },
    {
      icon: 'mail-outline' as const,
      label: 'E-mail',
      value: 'info@vanbudapest.com',
      action: () => openUrl('mailto:info@vanbudapest.com'),
    },
    {
      icon: 'call-outline' as const,
      label: 'Telefon',
      value: '+36 1 234 5678',
      action: () => openUrl('tel:+3612345678'),
    },
    {
      icon: 'location-outline' as const,
      label: 'Cím',
      value: 'Budapest, Magyarország',
      action: () => openUrl('https://maps.google.com/?q=Budapest'),
    },
  ];

  const socialItems = [
    {
      icon: 'logo-facebook' as const,
      label: 'Facebook',
      url: 'https://facebook.com/vanbudapest',
    },
    {
      icon: 'logo-instagram' as const,
      label: 'Instagram',
      url: 'https://instagram.com/vanbudapest',
    },
  ];

  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        {siteInfo?.icon?.img ? (
          <Image source={{ uri: siteInfo.icon.img }} style={styles.logo} />
        ) : (
          <View style={[styles.logo, styles.logoPlaceholder]}>
            <Ionicons name="business" size={48} color={colors.surface} />
          </View>
        )}
        <Text style={styles.siteName}>{siteInfo?.name || 'VanBudapest'}</Text>
        <Text style={styles.siteDescription}>
          {siteInfo?.description || 'Üdvözöljük Budapesten!'}
        </Text>
      </View>

      {/* About section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Rólunk</Text>
        <Text style={styles.aboutText}>
          A VanBudapest célja, hogy bemutassa Budapest szépségeit és segítsen
          felfedezni a város rejtett kincseit. Szolgáltatásainkkal szeretnénk
          hozzájárulni ahhoz, hogy minden látogató emlékezetes élményekkel
          gazdagodjon.
        </Text>
      </View>

      {/* Contact section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Kapcsolat</Text>
        {contactItems.map((item, index) => (
          <TouchableOpacity
            key={index}
            style={styles.contactItem}
            onPress={item.action}
          >
            <View style={styles.contactIcon}>
              <Ionicons name={item.icon} size={22} color={colors.primary} />
            </View>
            <View style={styles.contactInfo}>
              <Text style={styles.contactLabel}>{item.label}</Text>
              <Text style={styles.contactValue}>{item.value}</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.border} />
          </TouchableOpacity>
        ))}
      </View>

      {/* Social section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Kövess minket</Text>
        <View style={styles.socialRow}>
          {socialItems.map((item, index) => (
            <TouchableOpacity
              key={index}
              style={styles.socialButton}
              onPress={() => openUrl(item.url)}
            >
              <Ionicons name={item.icon} size={28} color={colors.surface} />
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* App info */}
      <View style={styles.appInfo}>
        <Text style={styles.appVersion}>VanBudapest App v1.0.0</Text>
        <Text style={styles.copyright}>
          2024 VanBudapest. Minden jog fenntartva.
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    alignItems: 'center',
    paddingVertical: spacing.xl,
    paddingHorizontal: spacing.md,
    backgroundColor: colors.primary,
  },
  logo: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginBottom: spacing.md,
  },
  logoPlaceholder: {
    backgroundColor: colors.primaryDark,
    alignItems: 'center',
    justifyContent: 'center',
  },
  siteName: {
    fontSize: 28,
    fontWeight: '700',
    color: colors.surface,
    marginBottom: spacing.xs,
  },
  siteDescription: {
    fontSize: 16,
    color: colors.surface + 'CC',
    textAlign: 'center',
  },
  section: {
    padding: spacing.md,
    marginTop: spacing.md,
    backgroundColor: colors.surface,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: colors.text,
    marginBottom: spacing.md,
  },
  aboutText: {
    fontSize: 15,
    color: colors.textSecondary,
    lineHeight: 24,
  },
  contactItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  contactIcon: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.primaryLight + '20',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
  },
  contactInfo: {
    flex: 1,
  },
  contactLabel: {
    fontSize: 12,
    color: colors.textSecondary,
    marginBottom: 2,
  },
  contactValue: {
    fontSize: 15,
    color: colors.text,
    fontWeight: '500',
  },
  socialRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: spacing.md,
  },
  socialButton: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  appInfo: {
    alignItems: 'center',
    paddingVertical: spacing.xl,
    paddingHorizontal: spacing.md,
  },
  appVersion: {
    fontSize: 13,
    color: colors.textSecondary,
  },
  copyright: {
    fontSize: 12,
    color: colors.textSecondary,
    marginTop: spacing.xs,
  },
});
