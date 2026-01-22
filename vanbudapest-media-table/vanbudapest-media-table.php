<?php
/**
 * Plugin Name: VanBudapest Média Táblázat
 * Plugin URI: https://vanbudapest.hu
 * Description: Táblázatos média könyvtár böngésző - képek hivatkozásainak egyszerű másolása
 * Version: 1.0.0
 * Author: VanBudapest
 * Author URI: https://vanbudapest.hu
 * License: GPL v2 or later
 * Text Domain: vanbudapest-media-table
 */

if (!defined('ABSPATH')) {
    exit;
}

class VanBudapest_Media_Table {

    private static $instance = null;

    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_assets'));
        add_action('wp_ajax_vbmt_get_media', array($this, 'ajax_get_media'));
        add_action('wp_ajax_vbmt_update_category', array($this, 'ajax_update_category'));
    }

    public function add_admin_menu() {
        add_menu_page(
            'Média Táblázat',
            'Média Táblázat',
            'upload_files',
            'vanbudapest-media-table',
            array($this, 'render_admin_page'),
            'dashicons-format-gallery',
            26
        );
    }

    public function enqueue_admin_assets($hook) {
        if ('toplevel_page_vanbudapest-media-table' !== $hook) {
            return;
        }

        wp_enqueue_style(
            'vbmt-admin-style',
            plugin_dir_url(__FILE__) . 'assets/css/admin-style.css',
            array(),
            '1.0.0'
        );

        wp_enqueue_script(
            'vbmt-admin-script',
            plugin_dir_url(__FILE__) . 'assets/js/admin-script.js',
            array('jquery'),
            '1.0.0',
            true
        );

        wp_localize_script('vbmt-admin-script', 'vbmt_ajax', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('vbmt_nonce'),
        ));
    }

    public function ajax_get_media() {
        check_ajax_referer('vbmt_nonce', 'nonce');

        if (!current_user_can('upload_files')) {
            wp_send_json_error('Nincs jogosultságod');
        }

        $page = isset($_POST['page']) ? intval($_POST['page']) : 1;
        $per_page = isset($_POST['per_page']) ? intval($_POST['per_page']) : 50;
        $category = isset($_POST['category']) ? sanitize_text_field($_POST['category']) : '';
        $search = isset($_POST['search']) ? sanitize_text_field($_POST['search']) : '';

        $args = array(
            'post_type' => 'attachment',
            'post_status' => 'inherit',
            'posts_per_page' => $per_page,
            'paged' => $page,
            'orderby' => 'date',
            'order' => 'DESC',
        );

        if (!empty($search)) {
            $args['s'] = $search;
        }

        if (!empty($category) && $category !== 'all') {
            $args['meta_query'] = array(
                array(
                    'key' => '_vbmt_category',
                    'value' => $category,
                    'compare' => '='
                )
            );
        }

        $query = new WP_Query($args);
        $media_items = array();

        foreach ($query->posts as $attachment) {
            $url = wp_get_attachment_url($attachment->ID);
            $thumb_url = '';
            $is_image = wp_attachment_is_image($attachment->ID);

            if ($is_image) {
                $thumb = wp_get_attachment_image_src($attachment->ID, 'thumbnail');
                $thumb_url = $thumb ? $thumb[0] : $url;
            }

            $category = get_post_meta($attachment->ID, '_vbmt_category', true);
            if (empty($category)) {
                $category = $this->auto_detect_category($attachment->post_title, $url);
            }

            $media_items[] = array(
                'id' => $attachment->ID,
                'title' => $attachment->post_title,
                'url' => $url,
                'thumb_url' => $thumb_url,
                'is_image' => $is_image,
                'date' => get_the_date('Y-m-d', $attachment->ID),
                'category' => $category,
                'mime_type' => $attachment->post_mime_type,
            );
        }

        wp_send_json_success(array(
            'items' => $media_items,
            'total' => $query->found_posts,
            'pages' => $query->max_num_pages,
            'current_page' => $page,
        ));
    }

    private function auto_detect_category($title, $url) {
        $text = strtolower($title . ' ' . $url);

        if (strpos($text, 'f1') !== false || strpos($text, 'formula') !== false || strpos($text, 'hungaroring') !== false) {
            return 'f1';
        }
        if (strpos($text, 'airport') !== false || strpos($text, 'repter') !== false || strpos($text, 'reptér') !== false || strpos($text, 'ferihegy') !== false) {
            return 'airport';
        }
        if (strpos($text, 'fleet') !== false || strpos($text, 'flotta') !== false || strpos($text, 'mercedes') !== false || strpos($text, 'vito') !== false) {
            return 'fleet';
        }
        if (strpos($text, 'balaton') !== false || strpos($text, 'siofok') !== false || strpos($text, 'siófok') !== false) {
            return 'balaton';
        }
        if (strpos($text, 'budapest') !== false || strpos($text, 'pest') !== false || strpos($text, 'buda') !== false) {
            return 'budapest';
        }
        if (strpos($text, 'festival') !== false || strpos($text, 'fesztival') !== false || strpos($text, 'fesztivál') !== false || strpos($text, 'sziget') !== false) {
            return 'festival';
        }
        if (strpos($text, 'vip') !== false || strpos($text, 'luxury') !== false || strpos($text, 'prémium') !== false) {
            return 'vip';
        }

        return 'other';
    }

    public function ajax_update_category() {
        check_ajax_referer('vbmt_nonce', 'nonce');

        if (!current_user_can('upload_files')) {
            wp_send_json_error('Nincs jogosultságod');
        }

        $attachment_id = isset($_POST['attachment_id']) ? intval($_POST['attachment_id']) : 0;
        $category = isset($_POST['category']) ? sanitize_text_field($_POST['category']) : '';

        if (!$attachment_id) {
            wp_send_json_error('Érvénytelen média azonosító');
        }

        update_post_meta($attachment_id, '_vbmt_category', $category);

        wp_send_json_success(array('message' => 'Kategória frissítve'));
    }

    public function render_admin_page() {
        ?>
        <div class="vbmt-wrap">
            <div class="vbmt-toolbar">
                <div class="vbmt-toolbar-left">
                    <h1>VanBudapest Média Könyvtár</h1>
                </div>
                <div class="vbmt-toolbar-right">
                    <input type="text" class="vbmt-search" id="vbmt-search" placeholder="Keresés...">
                    <select class="vbmt-category-filter" id="vbmt-category-filter">
                        <option value="all">Összes kategória</option>
                        <option value="f1">F1</option>
                        <option value="airport">Reptér</option>
                        <option value="fleet">Flotta</option>
                        <option value="balaton">Balaton</option>
                        <option value="budapest">Budapest</option>
                        <option value="festival">Fesztivál</option>
                        <option value="vip">VIP</option>
                        <option value="other">Egyéb</option>
                    </select>
                    <span class="vbmt-count"><span id="vbmt-visible-count">0</span> / <span id="vbmt-total-count">0</span> elem</span>
                </div>
            </div>

            <div class="vbmt-excel-container">
                <table class="vbmt-excel" id="vbmt-media-table">
                    <thead>
                        <tr>
                            <th class="vbmt-col-date vbmt-sortable" data-sort="date">Feltöltés dátuma ▼</th>
                            <th class="vbmt-col-preview">Kép</th>
                            <th class="vbmt-col-link">Link</th>
                            <th class="vbmt-col-copy">Másolás</th>
                            <th class="vbmt-col-category vbmt-sortable" data-sort="category">Kategória</th>
                        </tr>
                    </thead>
                    <tbody id="vbmt-table-body">
                        <tr>
                            <td colspan="5" class="vbmt-loading">Betöltés...</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="vbmt-footer">
                <div class="vbmt-pagination">
                    <button class="vbmt-btn" id="vbmt-prev-page" disabled>◀ Előző</button>
                    <span class="vbmt-page-info"><span id="vbmt-current-page">1</span> / <span id="vbmt-total-pages">1</span></span>
                    <button class="vbmt-btn" id="vbmt-next-page">Következő ▶</button>
                </div>
            </div>

            <div class="vbmt-modal" id="vbmt-modal">
                <div class="vbmt-modal-content">
                    <span class="vbmt-modal-close" id="vbmt-modal-close">&times;</span>
                    <img src="" alt="Előnézet" id="vbmt-modal-image">
                    <div class="vbmt-modal-footer">
                        <input type="text" id="vbmt-modal-url" readonly>
                        <button class="vbmt-btn vbmt-btn-primary" id="vbmt-modal-copy">Másolás</button>
                    </div>
                </div>
            </div>

            <div class="vbmt-toast" id="vbmt-toast">Link vágólapra másolva!</div>
        </div>
        <?php
    }
}

// Initialize plugin
VanBudapest_Media_Table::get_instance();
