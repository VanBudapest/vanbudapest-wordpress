import React from 'react';
import {
  View,
  ScrollView,
  Text,
  Image,
  StyleSheet,
  useWindowDimensions,
  Share,
  TouchableOpacity,
} from 'react-native';
import { useRoute, RouteProp } from '@react-navigation/native';
import RenderHtml from 'react-native-render-html';
import { Ionicons } from '@expo/vector-icons';
import { usePost } from '../hooks/useWordPress';
import { LoadingSpinner, ErrorMessage } from '../components';
import { RootStackParamList } from '../types';
import { formatDate, estimateReadingTime, colors, spacing } from '../utils/helpers';

type PostDetailRouteProp = RouteProp<RootStackParamList, 'PostDetail'>;

export function PostDetailScreen() {
  const route = useRoute<PostDetailRouteProp>();
  const { postId } = route.params;
  const { post, loading, error } = usePost(postId);
  const { width } = useWindowDimensions();

  const handleShare = async () => {
    if (!post) return;

    try {
      await Share.share({
        title: post.title,
        message: `${post.title}\n\nhttps://vanbudapest.com/${post.slug}`,
        url: `https://vanbudapest.com/${post.slug}`,
      });
    } catch (err) {
      console.error('Share error:', err);
    }
  };

  if (loading) {
    return <LoadingSpinner fullScreen message="Bejegyzés betöltése..." />;
  }

  if (error || !post) {
    return <ErrorMessage message={error || 'Nem található a bejegyzés'} />;
  }

  return (
    <ScrollView style={styles.container}>
      {post.featured_image && (
        <Image
          source={{ uri: post.featured_image }}
          style={styles.featuredImage}
          resizeMode="cover"
        />
      )}

      <View style={styles.content}>
        <Text style={styles.title}>{post.title}</Text>

        <View style={styles.meta}>
          <View style={styles.metaItem}>
            <Ionicons name="calendar-outline" size={16} color={colors.textSecondary} />
            <Text style={styles.metaText}>{formatDate(post.date)}</Text>
          </View>
          <View style={styles.metaItem}>
            <Ionicons name="time-outline" size={16} color={colors.textSecondary} />
            <Text style={styles.metaText}>{estimateReadingTime(post.content)}</Text>
          </View>
          <TouchableOpacity style={styles.shareButton} onPress={handleShare}>
            <Ionicons name="share-outline" size={20} color={colors.primary} />
          </TouchableOpacity>
        </View>

        <View style={styles.authorSection}>
          {post.author?.avatar_URL && (
            <Image
              source={{ uri: post.author.avatar_URL }}
              style={styles.avatar}
            />
          )}
          <Text style={styles.authorName}>{post.author?.name || 'Szerző'}</Text>
        </View>

        <View style={styles.htmlContent}>
          <RenderHtml
            contentWidth={width - spacing.md * 2}
            source={{ html: post.content }}
            tagsStyles={{
              p: { fontSize: 16, lineHeight: 26, color: colors.text, marginBottom: 16 },
              h2: { fontSize: 22, fontWeight: '700', color: colors.text, marginTop: 24, marginBottom: 12 },
              h3: { fontSize: 18, fontWeight: '600', color: colors.text, marginTop: 20, marginBottom: 8 },
              a: { color: colors.primary },
              img: { borderRadius: 8 },
              blockquote: {
                borderLeftWidth: 3,
                borderLeftColor: colors.primary,
                paddingLeft: 16,
                fontStyle: 'italic',
                color: colors.textSecondary,
              },
            }}
          />
        </View>

        {Object.keys(post.categories || {}).length > 0 && (
          <View style={styles.categories}>
            <Text style={styles.categoryLabel}>Kategóriák:</Text>
            <View style={styles.categoryList}>
              {Object.values(post.categories).map((cat) => (
                <View key={cat.ID} style={styles.categoryChip}>
                  <Text style={styles.categoryText}>{cat.name}</Text>
                </View>
              ))}
            </View>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.surface,
  },
  featuredImage: {
    width: '100%',
    height: 250,
  },
  content: {
    padding: spacing.md,
  },
  title: {
    fontSize: 26,
    fontWeight: '700',
    color: colors.text,
    lineHeight: 34,
    marginBottom: spacing.md,
  },
  meta: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  metaText: {
    fontSize: 13,
    color: colors.textSecondary,
    marginLeft: spacing.xs,
  },
  shareButton: {
    marginLeft: 'auto',
    padding: spacing.xs,
  },
  authorSection: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.md,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: colors.border,
    marginBottom: spacing.md,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: spacing.sm,
  },
  authorName: {
    fontSize: 15,
    fontWeight: '500',
    color: colors.text,
  },
  htmlContent: {
    marginBottom: spacing.lg,
  },
  categories: {
    borderTopWidth: 1,
    borderColor: colors.border,
    paddingTop: spacing.md,
  },
  categoryLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.textSecondary,
    marginBottom: spacing.sm,
  },
  categoryList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  categoryChip: {
    backgroundColor: colors.primaryLight + '20',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: 16,
    marginRight: spacing.xs,
    marginBottom: spacing.xs,
  },
  categoryText: {
    fontSize: 13,
    color: colors.primary,
    fontWeight: '500',
  },
});
