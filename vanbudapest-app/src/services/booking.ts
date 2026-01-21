import { BookingRequest, BookingConfirmation, BookingSlot } from '../types';

// Elérhető szolgáltatások
export const SERVICES = [
  { id: 'massage', name: 'Masszázs', duration: 60, price: '15.000 Ft' },
  { id: 'consultation', name: 'Konzultáció', duration: 30, price: '10.000 Ft' },
  { id: 'therapy', name: 'Terápia', duration: 90, price: '25.000 Ft' },
  { id: 'workshop', name: 'Workshop', duration: 120, price: '20.000 Ft' },
];

// Elérhető időpontok generálása (szimulált)
export function getAvailableSlots(date: string): BookingSlot[] {
  const times = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'];

  // Szimulált elérhetőség - valós implementációnál API hívás lenne
  return times.map((time, index) => ({
    id: `${date}-${time}`,
    date,
    time,
    // Véletlenszerűen néhány időpont foglalt
    available: Math.random() > 0.3,
  }));
}

// Foglalás elküldése
export async function submitBooking(booking: BookingRequest): Promise<BookingConfirmation> {
  // Szimulált API hívás - valós implementációnál WordPress form/API lenne
  await new Promise(resolve => setTimeout(resolve, 1500));

  // Siker szimulálása
  const confirmation: BookingConfirmation = {
    id: `BK-${Date.now()}`,
    status: 'pending',
    bookingDetails: booking,
    createdAt: new Date().toISOString(),
  };

  return confirmation;
}

// Email validáció
export function validateEmail(email: string): boolean {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

// Telefonszám validáció (magyar formátum)
export function validatePhone(phone: string): boolean {
  const re = /^(\+36|06)?[ -]?(20|30|31|50|70)[ -]?\d{3}[ -]?\d{4}$/;
  return re.test(phone.replace(/\s/g, ''));
}
