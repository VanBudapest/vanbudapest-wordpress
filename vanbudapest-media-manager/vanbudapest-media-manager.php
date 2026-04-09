<?php
/**
 * Plugin Name: VanBudapest Media Manager
 * Plugin URI: https://vanbudapest.com
 * Description: Advanced media manager with multi-select, inline editing, bulk operations, ShortPixel integration, and HTML code export for frontend development.
 * Version: 1.0.0
 * Author: VanBudapest
 * Author URI: https://vanbudapest.com
 * License: GPL v2 or later
 * Text Domain: vanbudapest-media-manager
 * Domain Path: /languages
 * Requires at least: 5.8
 * Requires PHP: 7.4
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'VBMM_VERSION', '1.0.0' );
define( 'VBMM_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
define( 'VBMM_PLUGIN_URL', plugin_dir_url( __FILE__ ) );
define( 'VBMM_PLUGIN_BASENAME', plugin_basename( __FILE__ ) );

// Autoload classes
require_once VBMM_PLUGIN_DIR . 'includes/class-admin.php';
require_once VBMM_PLUGIN_DIR . 'includes/class-media-api.php';
require_once VBMM_PLUGIN_DIR . 'includes/class-shortpixel.php';

/**
 * Main plugin class
 */
final class VanBudapest_Media_Manager {

    private static $instance = null;

    public static function instance() {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        add_action( 'plugins_loaded', array( $this, 'init' ) );
        register_activation_hook( __FILE__, array( $this, 'activate' ) );
    }

    public function init() {
        new VBMM_Admin();
        new VBMM_Media_API();
        new VBMM_ShortPixel();
    }

    public function activate() {
        if ( ! current_user_can( 'activate_plugins' ) ) {
            return;
        }
        update_option( 'vbmm_version', VBMM_VERSION );
        flush_rewrite_rules();
    }
}

VanBudapest_Media_Manager::instance();
