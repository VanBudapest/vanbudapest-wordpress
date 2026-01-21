import axios from 'axios';
import { WPPost, WPPage, WPCategory } from '../types';

const API_BASE = 'https://public-api.wordpress.com/rest/v1.1/sites/vanbudapest.com';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
});

// Bejegyzések lekérdezése
export async function getPosts(options: {
  page?: number;
  perPage?: number;
  search?: string;
  category?: string;
} = {}): Promise<{ posts: WPPost[]; total: number }> {
  const { page = 1, perPage = 10, search, category } = options;

  const params: Record<string, string | number> = {
    number: perPage,
    page,
  };

  if (search) {
    params.search = search;
  }

  if (category) {
    params.category = category;
  }

  const response = await api.get('/posts', { params });

  return {
    posts: response.data.posts,
    total: response.data.found,
  };
}

// Egyedi bejegyzés lekérdezése
export async function getPost(postId: number): Promise<WPPost> {
  const response = await api.get(`/posts/${postId}`);
  return response.data;
}

// Oldalak lekérdezése
export async function getPages(): Promise<WPPage[]> {
  const response = await api.get('/pages');
  return response.data.pages || [];
}

// Egyedi oldal lekérdezése
export async function getPage(pageId: number): Promise<WPPage> {
  const response = await api.get(`/pages/${pageId}`);
  return response.data;
}

// Kategóriák lekérdezése
export async function getCategories(): Promise<WPCategory[]> {
  const response = await api.get('/categories');
  return Object.values(response.data.categories || {});
}

// Keresés
export async function searchContent(query: string): Promise<WPPost[]> {
  const response = await api.get('/posts', {
    params: {
      search: query,
      number: 20,
    },
  });
  return response.data.posts;
}

// Site info
export async function getSiteInfo(): Promise<{
  name: string;
  description: string;
  URL: string;
  icon?: { img: string };
}> {
  const response = await api.get('');
  return response.data;
}
