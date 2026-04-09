<?php
/**
 * ShortPixel integration for VanBudapest Media Manager
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class VBMM_ShortPixel {

    public function __construct() {
        add_action( 'rest_api_init', array( $this, 'register_routes' ) );
    }

    /**
     * Register ShortPixel-related REST routes
     */
    public function register_routes() {
        register_rest_route( 'vbmm/v1', '/shortpixel/status', array(
            'methods'             => 'GET',
            'callback'            => array( $this, 'get_status' ),
            'permission_callback' => function () {
                return current_user_can( 'upload_files' );
            },
        ) );

        register_rest_route( 'vbmm/v1', '/shortpixel/optimize', array(
            'methods'             => 'POST',
            'callback'            => array( $this, 'trigger_optimize' ),
            'permission_callback' => function () {
                return current_user_can( 'edit_posts' );
            },
        ) );
    }

    /**
     * Check if ShortPixel is active and get stats
     */
    public function get_status() {
        $active = is_plugin_active( 'shortpixel-image-optimiser/wp-shortpixel.php' )
            || is_plugin_active( 'shortpixel-adaptive-images/short-pixel-ai.php' );

        if ( ! $active ) {
            return new WP_REST_Response( array(
                'active'    => false,
                'message'   => 'ShortPixel plugin is not active.',
            ), 200 );
        }

        global $wpdb;

        // Count optimized vs total images
        $total_images = (int) $wpdb->get_var(
            "SELECT COUNT(*) FROM {$wpdb->posts}
             WHERE post_type = 'attachment'
             AND post_status = 'inherit'
             AND post_mime_type LIKE 'image/%'"
        );

        $optimized = (int) $wpdb->get_var(
            "SELECT COUNT(*) FROM {$wpdb->postmeta}
             WHERE meta_key = '_shortpixel_status' AND meta_value = '2'"
        );

        // Get total savings if available
        $savings = $wpdb->get_var(
            "SELECT SUM(meta_value) FROM {$wpdb->postmeta}
             WHERE meta_key = '_shortpixel_savings'"
        );

        return new WP_REST_Response( array(
            'active'       => true,
            'total_images' => $total_images,
            'optimized'    => $optimized,
            'pending'      => $total_images - $optimized,
            'savings'      => $savings ? size_format( (float) $savings ) : '0 B',
        ), 200 );
    }

    /**
     * Trigger ShortPixel optimization for given IDs
     */
    public function trigger_optimize( $request ) {
        $params = $request->get_json_params();
        $ids    = isset( $params['ids'] ) ? array_map( 'absint', $params['ids'] ) : array();

        if ( empty( $ids ) ) {
            return new WP_Error( 'no_ids', 'No image IDs provided.', array( 'status' => 400 ) );
        }

        // Check if ShortPixel is available
        if ( ! class_exists( 'WPShortPixel' ) && ! function_exists( 'shortPixelOptimiseNow' ) ) {
            return new WP_Error(
                'shortpixel_unavailable',
                'ShortPixel plugin is not available.',
                array( 'status' => 400 )
            );
        }

        $queued  = array();
        $failed  = array();

        foreach ( $ids as $id ) {
            $post = get_post( $id );
            if ( ! $post || $post->post_type !== 'attachment' ) {
                $failed[] = $id;
                continue;
            }

            // Add to ShortPixel queue via their standard hook
            do_action( 'shortpixel_optimize_now', $id );
            $queued[] = $id;
        }

        return new WP_REST_Response( array(
            'queued'  => $queued,
            'failed'  => $failed,
            'message' => sprintf( '%d image(s) queued for optimization.', count( $queued ) ),
        ), 200 );
    }
}
