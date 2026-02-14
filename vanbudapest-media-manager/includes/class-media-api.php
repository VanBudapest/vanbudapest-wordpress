<?php
/**
 * REST API endpoints for VanBudapest Media Manager
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class VBMM_Media_API {

    public function __construct() {
        add_action( 'rest_api_init', array( $this, 'register_routes' ) );
    }

    /**
     * Register REST API routes
     */
    public function register_routes() {
        register_rest_route( 'vbmm/v1', '/media', array(
            'methods'             => 'GET',
            'callback'            => array( $this, 'get_media' ),
            'permission_callback' => array( $this, 'check_permissions' ),
            'args'                => array(
                'page'     => array( 'default' => 1, 'sanitize_callback' => 'absint' ),
                'per_page' => array( 'default' => 40, 'sanitize_callback' => 'absint' ),
                'search'   => array( 'default' => '', 'sanitize_callback' => 'sanitize_text_field' ),
                'type'     => array( 'default' => '', 'sanitize_callback' => 'sanitize_text_field' ),
                'date'     => array( 'default' => '', 'sanitize_callback' => 'sanitize_text_field' ),
                'size'     => array( 'default' => '', 'sanitize_callback' => 'sanitize_text_field' ),
                'attached' => array( 'default' => '', 'sanitize_callback' => 'sanitize_text_field' ),
                'orderby'  => array( 'default' => 'date', 'sanitize_callback' => 'sanitize_text_field' ),
                'order'    => array( 'default' => 'DESC', 'sanitize_callback' => 'sanitize_text_field' ),
            ),
        ) );

        register_rest_route( 'vbmm/v1', '/media/(?P<id>\d+)', array(
            array(
                'methods'             => 'GET',
                'callback'            => array( $this, 'get_single_media' ),
                'permission_callback' => array( $this, 'check_permissions' ),
            ),
            array(
                'methods'             => 'POST',
                'callback'            => array( $this, 'update_media' ),
                'permission_callback' => array( $this, 'check_edit_permissions' ),
            ),
        ) );

        register_rest_route( 'vbmm/v1', '/media/bulk-delete', array(
            'methods'             => 'POST',
            'callback'            => array( $this, 'bulk_delete' ),
            'permission_callback' => array( $this, 'check_delete_permissions' ),
        ) );

        register_rest_route( 'vbmm/v1', '/stats', array(
            'methods'             => 'GET',
            'callback'            => array( $this, 'get_stats' ),
            'permission_callback' => array( $this, 'check_permissions' ),
        ) );
    }

    /**
     * Check basic read permissions
     */
    public function check_permissions() {
        return current_user_can( 'upload_files' );
    }

    /**
     * Check edit permissions
     */
    public function check_edit_permissions() {
        return current_user_can( 'edit_posts' );
    }

    /**
     * Check delete permissions
     */
    public function check_delete_permissions() {
        return current_user_can( 'delete_posts' );
    }

    /**
     * Get media items with filtering
     */
    public function get_media( $request ) {
        $page     = $request->get_param( 'page' );
        $per_page = min( $request->get_param( 'per_page' ), 100 );
        $search   = $request->get_param( 'search' );
        $type     = $request->get_param( 'type' );
        $date     = $request->get_param( 'date' );
        $size     = $request->get_param( 'size' );
        $attached = $request->get_param( 'attached' );
        $orderby  = $request->get_param( 'orderby' );
        $order    = $request->get_param( 'order' );

        $args = array(
            'post_type'      => 'attachment',
            'post_status'    => 'inherit',
            'posts_per_page' => $per_page,
            'paged'          => $page,
            'orderby'        => $orderby,
            'order'          => strtoupper( $order ) === 'ASC' ? 'ASC' : 'DESC',
        );

        // Search
        if ( ! empty( $search ) ) {
            $args['s'] = $search;
            // Also search in alt text meta
            $args['meta_query'] = array(
                'relation' => 'OR',
                array(
                    'key'     => '_wp_attachment_image_alt',
                    'value'   => $search,
                    'compare' => 'LIKE',
                ),
            );
        }

        // MIME type filter
        if ( ! empty( $type ) ) {
            if ( $type === 'video' ) {
                $args['post_mime_type'] = array( 'video/mp4', 'video/webm', 'video/ogg', 'video/avi' );
            } else {
                $args['post_mime_type'] = $type;
            }
        } else {
            // Default: show images and common media types
            $args['post_mime_type'] = array(
                'image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml',
                'application/pdf',
                'video/mp4', 'video/webm',
            );
        }

        // Date filter
        if ( ! empty( $date ) && preg_match( '/^\d{4}-\d{2}$/', $date ) ) {
            $parts = explode( '-', $date );
            $args['date_query'] = array(
                array(
                    'year'  => (int) $parts[0],
                    'month' => (int) $parts[1],
                ),
            );
        }

        // Attached filter
        if ( $attached === 'attached' ) {
            $args['post_parent__not_in'] = array( 0 );
        } elseif ( $attached === 'unattached' ) {
            $args['post_parent'] = 0;
        }

        // Orderby mapping
        if ( $orderby === 'size' ) {
            $args['meta_key'] = '_vbmm_filesize';
            $args['orderby']  = 'meta_value_num';
        }

        $query = new WP_Query( $args );
        $items = array();

        foreach ( $query->posts as $post ) {
            $item = $this->format_media_item( $post );

            // Client-side size filtering for accuracy
            if ( ! empty( $size ) ) {
                $filesize = $item['filesize_raw'];
                $include  = true;
                switch ( $size ) {
                    case 'small':
                        $include = $filesize < 102400;
                        break;
                    case 'medium':
                        $include = $filesize >= 102400 && $filesize < 512000;
                        break;
                    case 'large':
                        $include = $filesize >= 512000 && $filesize < 2097152;
                        break;
                    case 'xlarge':
                        $include = $filesize >= 2097152;
                        break;
                }
                if ( ! $include ) {
                    continue;
                }
            }

            $items[] = $item;
        }

        return new WP_REST_Response( array(
            'items'       => $items,
            'total'       => (int) $query->found_posts,
            'total_pages' => (int) $query->max_num_pages,
            'page'        => $page,
        ), 200 );
    }

    /**
     * Get single media item with all sizes
     */
    public function get_single_media( $request ) {
        $id   = (int) $request->get_param( 'id' );
        $post = get_post( $id );

        if ( ! $post || $post->post_type !== 'attachment' ) {
            return new WP_Error( 'not_found', 'Media not found', array( 'status' => 404 ) );
        }

        $item = $this->format_media_item( $post, true );
        return new WP_REST_Response( $item, 200 );
    }

    /**
     * Update media item metadata
     */
    public function update_media( $request ) {
        $id = (int) $request->get_param( 'id' );
        $post = get_post( $id );

        if ( ! $post || $post->post_type !== 'attachment' ) {
            return new WP_Error( 'not_found', 'Media not found', array( 'status' => 404 ) );
        }

        $params = $request->get_json_params();
        $update = array( 'ID' => $id );

        if ( isset( $params['title'] ) ) {
            $update['post_title'] = sanitize_text_field( $params['title'] );
        }
        if ( isset( $params['caption'] ) ) {
            $update['post_excerpt'] = sanitize_textarea_field( $params['caption'] );
        }
        if ( isset( $params['description'] ) ) {
            $update['post_content'] = sanitize_textarea_field( $params['description'] );
        }

        wp_update_post( $update );

        if ( isset( $params['alt'] ) ) {
            update_post_meta( $id, '_wp_attachment_image_alt', sanitize_text_field( $params['alt'] ) );
        }

        $updated_post = get_post( $id );
        return new WP_REST_Response( $this->format_media_item( $updated_post, true ), 200 );
    }

    /**
     * Bulk delete media items
     */
    public function bulk_delete( $request ) {
        $params = $request->get_json_params();
        $ids    = isset( $params['ids'] ) ? array_map( 'absint', $params['ids'] ) : array();

        if ( empty( $ids ) ) {
            return new WP_Error( 'no_ids', 'No IDs provided', array( 'status' => 400 ) );
        }

        $deleted = array();
        $failed  = array();

        foreach ( $ids as $id ) {
            $result = wp_delete_attachment( $id, true );
            if ( $result ) {
                $deleted[] = $id;
            } else {
                $failed[] = $id;
            }
        }

        return new WP_REST_Response( array(
            'deleted' => $deleted,
            'failed'  => $failed,
        ), 200 );
    }

    /**
     * Get media library stats
     */
    public function get_stats() {
        global $wpdb;

        $total = (int) $wpdb->get_var(
            "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'attachment' AND post_status = 'inherit'"
        );

        // Get total filesize from metadata
        $total_size = 0;
        $attachments = $wpdb->get_col(
            "SELECT ID FROM {$wpdb->posts} WHERE post_type = 'attachment' AND post_status = 'inherit'"
        );

        // Sample-based estimation for large libraries
        $sample = array_slice( $attachments, 0, 500 );
        $sample_size = 0;
        foreach ( $sample as $att_id ) {
            $file = get_attached_file( $att_id );
            if ( $file && file_exists( $file ) ) {
                $sample_size += filesize( $file );
            }
        }

        if ( count( $sample ) > 0 ) {
            $avg_size   = $sample_size / count( $sample );
            $total_size = $avg_size * $total;
        }

        // Count by mime type
        $types = $wpdb->get_results(
            "SELECT post_mime_type, COUNT(*) as count
             FROM {$wpdb->posts}
             WHERE post_type = 'attachment' AND post_status = 'inherit'
             GROUP BY post_mime_type
             ORDER BY count DESC"
        );

        // ShortPixel optimization count
        $optimized = 0;
        if ( is_plugin_active( 'shortpixel-image-optimiser/wp-shortpixel.php' ) ) {
            $optimized = (int) $wpdb->get_var(
                "SELECT COUNT(*) FROM {$wpdb->postmeta}
                 WHERE meta_key = '_shortpixel_status' AND meta_value = '2'"
            );
        }

        return new WP_REST_Response( array(
            'total'          => $total,
            'total_size'     => $total_size,
            'total_size_hr'  => size_format( $total_size ),
            'types'          => $types,
            'optimized'      => $optimized,
        ), 200 );
    }

    /**
     * Format a single media item for API response
     */
    private function format_media_item( $post, $include_sizes = false ) {
        $id       = $post->ID;
        $url      = wp_get_attachment_url( $id );
        $file     = get_attached_file( $id );
        $filesize = $file && file_exists( $file ) ? filesize( $file ) : 0;
        $meta     = wp_get_attachment_metadata( $id );
        $alt      = get_post_meta( $id, '_wp_attachment_image_alt', true );

        // Cache filesize for sorting
        update_post_meta( $id, '_vbmm_filesize', $filesize );

        $item = array(
            'id'            => $id,
            'title'         => $post->post_title,
            'alt'           => $alt ?: '',
            'caption'       => $post->post_excerpt,
            'description'   => $post->post_content,
            'url'           => $url,
            'mime_type'     => $post->post_mime_type,
            'date'          => $post->post_date,
            'modified'      => $post->post_modified,
            'filesize'      => size_format( $filesize ),
            'filesize_raw'  => $filesize,
            'parent'        => $post->post_parent,
            'parent_title'  => $post->post_parent ? get_the_title( $post->post_parent ) : '',
            'edit_link'     => get_edit_post_link( $id, 'raw' ),
        );

        // Image dimensions
        if ( ! empty( $meta['width'] ) && ! empty( $meta['height'] ) ) {
            $item['width']  = (int) $meta['width'];
            $item['height'] = (int) $meta['height'];
        }

        // Thumbnail
        $thumb = wp_get_attachment_image_src( $id, 'thumbnail' );
        $item['thumbnail'] = $thumb ? $thumb[0] : '';

        $medium = wp_get_attachment_image_src( $id, 'medium' );
        $item['medium'] = $medium ? $medium[0] : '';

        // ShortPixel status
        $sp_status = get_post_meta( $id, '_shortpixel_status', true );
        $item['shortpixel_status'] = $sp_status ? (int) $sp_status : 0;

        // All available sizes (for detail view)
        if ( $include_sizes && ! empty( $meta['sizes'] ) ) {
            $sizes = array();
            $upload_dir = wp_get_upload_dir();
            $base_dir   = dirname( get_attached_file( $id ) );
            $base_url   = dirname( $url );

            foreach ( $meta['sizes'] as $size_name => $size_data ) {
                $sizes[ $size_name ] = array(
                    'width'  => $size_data['width'],
                    'height' => $size_data['height'],
                    'url'    => $base_url . '/' . $size_data['file'],
                    'file'   => $size_data['file'],
                );
            }
            $item['sizes'] = $sizes;

            // Add full size
            $item['sizes']['full'] = array(
                'width'  => isset( $meta['width'] ) ? $meta['width'] : 0,
                'height' => isset( $meta['height'] ) ? $meta['height'] : 0,
                'url'    => $url,
                'file'   => basename( $url ),
            );
        }

        return $item;
    }
}
