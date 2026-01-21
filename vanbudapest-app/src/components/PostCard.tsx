import React from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import { WPPost } from '../types';
import { truncate, formatRelativeDate, estimateReadingTime, colors, spacing } from '../utils/helpers';

interface PostCardProps {
  post: WPPost;
  onPress: () => void;
}

export function PostCard({ post, onPress }: PostCardProps) {
  const hasImage = !!post.featured_image;

  return (
    <TouchableOpacity style={styles.container} onPress={onPress} activeOpacity={0.7}>
      {hasImage && (
        <Image
          source={{ uri: post.featured_image }}
          style={styles.image}
          resizeMode="cover"
        />
      )}
      <View style={styles.content}>
        <Text style={styles.title} numberOfLines={2}>
          {post.title}
        </Text>
        <Text style={styles.excerpt} numberOfLines={3}>
          {truncate(post.excerpt, 150)}
        </Text>
        <View style={styles.meta}>
          <Text style={styles.date}>{formatRelativeDate(post.date)}</Text>
          <Text style={styles.separator}>•</Text>
          <Text style={styles.readTime}>{estimateReadingTime(post.content)}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    marginHorizontal: spacing.md,
    marginVertical: spacing.sm,
    overflow: 'hidden',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  image: {
    width: '100%',
    height: 180,
  },
  content: {
    padding: spacing.md,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
    marginBottom: spacing.xs,
    lineHeight: 24,
  },
  excerpt: {
    fontSize: 14,
    color: colors.textSecondary,
    lineHeight: 20,
    marginBottom: spacing.sm,
  },
  meta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  date: {
    fontSize: 12,
    color: colors.textSecondary,
  },
  separator: {
    fontSize: 12,
    color: colors.textSecondary,
    marginHorizontal: spacing.xs,
  },
  readTime: {
    fontSize: 12,
    color: colors.primary,
  },
});
