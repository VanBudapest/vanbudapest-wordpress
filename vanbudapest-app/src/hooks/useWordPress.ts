import { useState, useEffect, useCallback } from 'react';
import { WPPost, WPPage, WPCategory } from '../types';
import * as wordpress from '../services/wordpress';

// Bejegyzések hook
export function usePosts(options?: { category?: string }) {
  const [posts, setPosts] = useState<WPPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [total, setTotal] = useState(0);

  const fetchPosts = useCallback(async (pageNum: number, reset: boolean = false) => {
    try {
      setLoading(true);
      setError(null);

      const result = await wordpress.getPosts({
        page: pageNum,
        perPage: 10,
        category: options?.category,
      });

      setPosts(prev => reset ? result.posts : [...prev, ...result.posts]);
      setTotal(result.total);
      setHasMore(result.posts.length === 10);
    } catch (err) {
      setError('Nem sikerült betölteni a bejegyzéseket');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [options?.category]);

  useEffect(() => {
    fetchPosts(1, true);
  }, [fetchPosts]);

  const loadMore = useCallback(() => {
    if (!loading && hasMore) {
      const nextPage = page + 1;
      setPage(nextPage);
      fetchPosts(nextPage);
    }
  }, [loading, hasMore, page, fetchPosts]);

  const refresh = useCallback(() => {
    setPage(1);
    fetchPosts(1, true);
  }, [fetchPosts]);

  return { posts, loading, error, loadMore, refresh, hasMore, total };
}

// Egyedi bejegyzés hook
export function usePost(postId: number) {
  const [post, setPost] = useState<WPPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchPost() {
      try {
        setLoading(true);
        const data = await wordpress.getPost(postId);
        setPost(data);
      } catch (err) {
        setError('Nem sikerült betölteni a bejegyzést');
      } finally {
        setLoading(false);
      }
    }

    fetchPost();
  }, [postId]);

  return { post, loading, error };
}

// Oldalak hook
export function usePages() {
  const [pages, setPages] = useState<WPPage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchPages() {
      try {
        const data = await wordpress.getPages();
        setPages(data);
      } catch (err) {
        setError('Nem sikerült betölteni az oldalakat');
      } finally {
        setLoading(false);
      }
    }

    fetchPages();
  }, []);

  return { pages, loading, error };
}

// Kategóriák hook
export function useCategories() {
  const [categories, setCategories] = useState<WPCategory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCategories() {
      try {
        const data = await wordpress.getCategories();
        setCategories(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchCategories();
  }, []);

  return { categories, loading };
}

// Keresés hook
export function useSearch() {
  const [results, setResults] = useState<WPPost[]>([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');

  const search = useCallback(async (searchQuery: string) => {
    setQuery(searchQuery);

    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    try {
      setLoading(true);
      const data = await wordpress.searchContent(searchQuery);
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  const clear = useCallback(() => {
    setQuery('');
    setResults([]);
  }, []);

  return { results, loading, query, search, clear };
}
