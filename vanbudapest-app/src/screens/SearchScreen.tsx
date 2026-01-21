import React, { useCallback, useEffect, useState } from 'react';
import {
  View,
  FlatList,
  Text,
  StyleSheet,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useSearch } from '../hooks/useWordPress';
import { PostCard, LoadingSpinner, SearchBar } from '../components';
import { RootStackParamList, WPPost } from '../types';
import { colors, spacing } from '../utils/helpers';
import { Ionicons } from '@expo/vector-icons';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

// Debounce helper
function useDebounce(value: string, delay: number): string {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export function SearchScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { results, loading, search, clear } = useSearch();
  const [searchText, setSearchText] = useState('');
  const debouncedSearch = useDebounce(searchText, 500);

  useEffect(() => {
    if (debouncedSearch) {
      search(debouncedSearch);
    }
  }, [debouncedSearch, search]);

  const handlePostPress = (post: WPPost) => {
    navigation.navigate('PostDetail', {
      postId: post.ID,
      title: post.title,
    });
  };

  const handleClear = useCallback(() => {
    setSearchText('');
    clear();
  }, [clear]);

  const renderPost = ({ item }: { item: WPPost }) => (
    <PostCard post={item} onPress={() => handlePostPress(item)} />
  );

  const renderEmpty = () => {
    if (loading) {
      return <LoadingSpinner message="Keresés..." />;
    }

    if (searchText.length === 0) {
      return (
        <View style={styles.emptyState}>
          <Ionicons name="search" size={64} color={colors.border} />
          <Text style={styles.emptyTitle}>Keresés a tartalomban</Text>
          <Text style={styles.emptyText}>
            Írj be egy keresőszót a bejegyzések közötti kereséshez
          </Text>
        </View>
      );
    }

    if (results.length === 0 && searchText.length > 0) {
      return (
        <View style={styles.emptyState}>
          <Ionicons name="document-text-outline" size={64} color={colors.border} />
          <Text style={styles.emptyTitle}>Nincs találat</Text>
          <Text style={styles.emptyText}>
            Próbálj más keresőszót használni
          </Text>
        </View>
      );
    }

    return null;
  };

  return (
    <View style={styles.container}>
      <SearchBar
        value={searchText}
        onChangeText={setSearchText}
        onClear={handleClear}
        placeholder="Keresés bejegyzésekben..."
      />

      {results.length > 0 && (
        <Text style={styles.resultCount}>
          {results.length} találat "{searchText}" keresésre
        </Text>
      )}

      <FlatList
        data={results}
        renderItem={renderPost}
        keyExtractor={(item) => item.ID.toString()}
        contentContainerStyle={styles.list}
        ListEmptyComponent={renderEmpty}
        keyboardShouldPersistTaps="handled"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  list: {
    flexGrow: 1,
    paddingBottom: spacing.md,
  },
  resultCount: {
    fontSize: 13,
    color: colors.textSecondary,
    marginHorizontal: spacing.md,
    marginBottom: spacing.sm,
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: spacing.xl,
    paddingTop: 100,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
    marginTop: spacing.md,
    marginBottom: spacing.xs,
  },
  emptyText: {
    fontSize: 14,
    color: colors.textSecondary,
    textAlign: 'center',
    lineHeight: 20,
  },
});
