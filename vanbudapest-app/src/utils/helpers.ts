import { format, parseISO, isValid } from 'date-fns';
import { hu } from 'date-fns/locale';

// HTML eltávolítása szövegből
export function stripHtml(html: string): string {
  return html.replace(/<[^>]*>/g, '').replace(/&[^;]+;/g, ' ').trim();
}

// Szöveg rövidítése
export function truncate(text: string, maxLength: number): string {
  const stripped = stripHtml(text);
  if (stripped.length <= maxLength) return stripped;
  return stripped.substring(0, maxLength).trim() + '...';
}

// Dátum formázás magyarul
export function formatDate(dateString: string): string {
  try {
    const date = parseISO(dateString);
    if (!isValid(date)) return dateString;
    return format(date, 'yyyy. MMMM d.', { locale: hu });
  } catch {
    return dateString;
  }
}

// Relatív dátum (pl. "2 napja")
export function formatRelativeDate(dateString: string): string {
  try {
    const date = parseISO(dateString);
    if (!isValid(date)) return dateString;

    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Ma';
    if (diffDays === 1) return 'Tegnap';
    if (diffDays < 7) return `${diffDays} napja`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} hete`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} hónapja`;
    return `${Math.floor(diffDays / 365)} éve`;
  } catch {
    return dateString;
  }
}

// Olvasási idő becslése
export function estimateReadingTime(content: string): string {
  const text = stripHtml(content);
  const wordsPerMinute = 180; // Magyar átlag
  const words = text.split(/\s+/).length;
  const minutes = Math.ceil(words / wordsPerMinute);
  return `${minutes} perc olvasás`;
}

// Színek az app-hoz
export const colors = {
  primary: '#2E7D32',       // Zöld
  primaryDark: '#1B5E20',
  primaryLight: '#4CAF50',
  secondary: '#FFA000',     // Sárga/narancs
  background: '#FAFAFA',
  surface: '#FFFFFF',
  text: '#212121',
  textSecondary: '#757575',
  border: '#E0E0E0',
  error: '#D32F2F',
  success: '#388E3C',
};

// Spacing értékek
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};
