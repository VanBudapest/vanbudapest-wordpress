// WordPress API típusok
export interface WPPost {
  ID: number;
  title: string;
  content: string;
  excerpt: string;
  date: string;
  modified: string;
  slug: string;
  author: WPAuthor;
  featured_image?: string;
  categories: Record<string, WPCategory>;
  tags: Record<string, WPTag>;
}

export interface WPAuthor {
  ID: number;
  login: string;
  name: string;
  avatar_URL: string;
}

export interface WPCategory {
  ID: number;
  name: string;
  slug: string;
  post_count: number;
}

export interface WPTag {
  ID: number;
  name: string;
  slug: string;
}

export interface WPPage {
  ID: number;
  title: string;
  content: string;
  slug: string;
  date: string;
  featured_image?: string;
}

// Foglalási típusok
export interface BookingSlot {
  id: string;
  date: string;
  time: string;
  available: boolean;
}

export interface BookingRequest {
  name: string;
  email: string;
  phone: string;
  date: string;
  time: string;
  service: string;
  notes?: string;
}

export interface BookingConfirmation {
  id: string;
  status: 'pending' | 'confirmed' | 'cancelled';
  bookingDetails: BookingRequest;
  createdAt: string;
}

// Navigációs típusok
export type RootStackParamList = {
  MainTabs: undefined;
  PostDetail: { postId: number; title: string };
  PageDetail: { pageId: number; title: string };
  BookingConfirm: { booking: BookingRequest };
};

export type MainTabParamList = {
  Home: undefined;
  Search: undefined;
  Booking: undefined;
  About: undefined;
};
