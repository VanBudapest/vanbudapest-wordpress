import React from 'react';
import {
  View,
  FlatList,
  RefreshControl,
  StyleSheet,
  Text,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { usePosts } from '../hooks/useWordPress';
import { PostCard, LoadingSpinner, ErrorMessage } from '../components';
import { RootStackParamList, WPPost } from '../types';
import { colors, spacing } from '../utils/helpers';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export function HomeScreen() {
  const navigation = useNavigation<NavigationProp>();
  const { posts, loading, error, loadMore, refresh, hasMore } = usePosts();

  const handlePostPress = (post: WPPost) => {
    navigation.navigate('PostDetail', {
      postId: post.ID,
      title: post.title,
    });
  };

  const renderPost = ({ item }: { item: WPPost }) => (
    <PostCard post={item} onPress={() => handlePostPress(item)} />
  );

  const renderFooter = () => {
    if (!hasMore) {
      return (
        <Text style={styles.endMessage}>Nincs több bejegyzés</Text>
      );
    }
    if (loading && posts.length > 0) {
      return <LoadingSpinner message="" />;
    }
    return null;
  };

  if (loading && posts.length === 0) {
    return <LoadingSpinner fullScreen message="Bejegyzések betöltése..." />;
  }

  if (error && posts.length === 0) {
    return <ErrorMessage message={error} onRetry={refresh} />;
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={posts}
        renderItem={renderPost}
        keyExtractor={(item) => item.ID.toString()}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl
            refreshing={loading && posts.length > 0}
            onRefresh={refresh}
            colors={[colors.primary]}
            tintColor={colors.primary}
          />
        }
        onEndReached={loadMore}
        onEndReachedThreshold={0.5}
        ListFooterComponent={renderFooter}
        ListHeaderComponent={
          <Text style={styles.header}>Legújabb bejegyzések</Text>
        }
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
    paddingVertical: spacing.sm,
  },
  header: {
    fontSize: 22,
    fontWeight: '700',
    color: colors.text,
    marginHorizontal: spacing.md,
    marginTop: spacing.md,
    marginBottom: spacing.sm,
  },
  endMessage: {
    textAlign: 'center',
    color: colors.textSecondary,
    padding: spacing.lg,
    fontSize: 14,
  },
});
