<?php
/**
 * Admin page for VanBudapest Media Manager
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class VBMM_Admin {

    public function __construct() {
        add_action( 'admin_menu', array( $this, 'add_menu_page' ) );
        add_action( 'admin_enqueue_scripts', array( $this, 'enqueue_assets' ) );
    }

    /**
     * Add submenu under Media
     */
    public function add_menu_page() {
        add_media_page(
            __( 'VanBudapest Manager', 'vanbudapest-media-manager' ),
            __( 'VanBudapest Manager', 'vanbudapest-media-manager' ),
            'upload_files',
            'vanbudapest-manager',
            array( $this, 'render_page' )
        );
    }

    /**
     * Enqueue admin CSS and JS
     */
    public function enqueue_assets( $hook ) {
        if ( 'media_page_vanbudapest-manager' !== $hook ) {
            return;
        }

        wp_enqueue_media();

        wp_enqueue_style(
            'vbmm-admin',
            VBMM_PLUGIN_URL . 'assets/css/admin.css',
            array(),
            VBMM_VERSION
        );

        wp_enqueue_script(
            'vbmm-admin',
            VBMM_PLUGIN_URL . 'assets/js/admin.js',
            array( 'jquery', 'wp-util' ),
            VBMM_VERSION,
            true
        );

        $shortpixel_active = is_plugin_active( 'shortpixel-image-optimiser/wp-shortpixel.php' )
            || is_plugin_active( 'shortpixel-adaptive-images/short-pixel-ai.php' );

        wp_localize_script( 'vbmm-admin', 'vbmmData', array(
            'ajaxUrl'          => admin_url( 'admin-ajax.php' ),
            'restUrl'          => rest_url( 'vbmm/v1/' ),
            'nonce'            => wp_create_nonce( 'vbmm_nonce' ),
            'restNonce'        => wp_create_nonce( 'wp_rest' ),
            'uploadsUrl'       => wp_get_upload_dir()['baseurl'],
            'shortpixelActive' => $shortpixel_active,
            'i18n'             => array(
                'selectAll'      => __( 'Összes kijelölése', 'vanbudapest-media-manager' ),
                'deselectAll'    => __( 'Kijelölés törlése', 'vanbudapest-media-manager' ),
                'selected'       => __( 'kijelölve', 'vanbudapest-media-manager' ),
                'copyHtml'       => __( 'HTML kód másolása', 'vanbudapest-media-manager' ),
                'copyUrls'       => __( 'URL-ek másolása', 'vanbudapest-media-manager' ),
                'copyMarkdown'   => __( 'Markdown másolása', 'vanbudapest-media-manager' ),
                'copyCss'        => __( 'CSS háttérkép másolása', 'vanbudapest-media-manager' ),
                'copied'         => __( 'Másolva!', 'vanbudapest-media-manager' ),
                'deleteConfirm'  => __( 'Biztosan törlöd a kijelölt fájlokat?', 'vanbudapest-media-manager' ),
                'noResults'      => __( 'Nincs találat', 'vanbudapest-media-manager' ),
                'loading'        => __( 'Betöltés...', 'vanbudapest-media-manager' ),
                'saved'          => __( 'Mentve!', 'vanbudapest-media-manager' ),
                'error'          => __( 'Hiba történt', 'vanbudapest-media-manager' ),
                'optimized'      => __( 'Optimalizálva', 'vanbudapest-media-manager' ),
                'notOptimized'   => __( 'Nincs optimalizálva', 'vanbudapest-media-manager' ),
            ),
        ) );
    }

    /**
     * Render the admin page
     */
    public function render_page() {
        if ( ! current_user_can( 'upload_files' ) ) {
            wp_die( __( 'Nincs jogosultságod ehhez az oldalhoz.', 'vanbudapest-media-manager' ) );
        }
        ?>
        <div class="wrap vbmm-wrap">
            <h1 class="vbmm-title">
                <span class="vbmm-logo">VB</span>
                VanBudapest Media Manager
            </h1>

            <!-- Toolbar -->
            <div class="vbmm-toolbar">
                <div class="vbmm-toolbar-left">
                    <label class="vbmm-checkbox-label">
                        <input type="checkbox" id="vbmm-select-all">
                        <span id="vbmm-select-all-label"><?php esc_html_e( 'Összes kijelölése', 'vanbudapest-media-manager' ); ?></span>
                    </label>
                    <span class="vbmm-selected-count" id="vbmm-selected-count" style="display:none;">
                        <strong id="vbmm-count-number">0</strong> <?php esc_html_e( 'kijelölve', 'vanbudapest-media-manager' ); ?>
                    </span>
                </div>
                <div class="vbmm-toolbar-center">
                    <div class="vbmm-search-box">
                        <input type="text" id="vbmm-search" placeholder="<?php esc_attr_e( 'Keresés: fájlnév, alt text, cím...', 'vanbudapest-media-manager' ); ?>">
                        <span class="vbmm-search-icon dashicons dashicons-search"></span>
                    </div>
                </div>
                <div class="vbmm-toolbar-right">
                    <div class="vbmm-view-toggle">
                        <button type="button" class="vbmm-view-btn active" data-view="grid" title="Rács nézet">
                            <span class="dashicons dashicons-grid-view"></span>
                        </button>
                        <button type="button" class="vbmm-view-btn" data-view="list" title="Lista nézet">
                            <span class="dashicons dashicons-list-view"></span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Filters -->
            <div class="vbmm-filters">
                <select id="vbmm-filter-type">
                    <option value=""><?php esc_html_e( 'Minden típus', 'vanbudapest-media-manager' ); ?></option>
                    <option value="image/jpeg">JPEG</option>
                    <option value="image/png">PNG</option>
                    <option value="image/webp">WebP</option>
                    <option value="image/svg+xml">SVG</option>
                    <option value="image/gif">GIF</option>
                    <option value="application/pdf">PDF</option>
                    <option value="video">Videó</option>
                </select>
                <select id="vbmm-filter-date">
                    <option value=""><?php esc_html_e( 'Minden dátum', 'vanbudapest-media-manager' ); ?></option>
                    <?php echo $this->get_date_options(); ?>
                </select>
                <select id="vbmm-filter-size">
                    <option value=""><?php esc_html_e( 'Minden méret', 'vanbudapest-media-manager' ); ?></option>
                    <option value="small">&lt; 100 KB</option>
                    <option value="medium">100 KB - 500 KB</option>
                    <option value="large">500 KB - 2 MB</option>
                    <option value="xlarge">&gt; 2 MB</option>
                </select>
                <select id="vbmm-filter-attached">
                    <option value=""><?php esc_html_e( 'Összes', 'vanbudapest-media-manager' ); ?></option>
                    <option value="attached"><?php esc_html_e( 'Bejegyzéshez csatolva', 'vanbudapest-media-manager' ); ?></option>
                    <option value="unattached"><?php esc_html_e( 'Nem csatolt', 'vanbudapest-media-manager' ); ?></option>
                </select>
                <select id="vbmm-sort">
                    <option value="date-desc"><?php esc_html_e( 'Dátum (újabb elöl)', 'vanbudapest-media-manager' ); ?></option>
                    <option value="date-asc"><?php esc_html_e( 'Dátum (régebbi elöl)', 'vanbudapest-media-manager' ); ?></option>
                    <option value="title-asc"><?php esc_html_e( 'Cím (A-Z)', 'vanbudapest-media-manager' ); ?></option>
                    <option value="title-desc"><?php esc_html_e( 'Cím (Z-A)', 'vanbudapest-media-manager' ); ?></option>
                    <option value="size-asc"><?php esc_html_e( 'Méret (kisebb elöl)', 'vanbudapest-media-manager' ); ?></option>
                    <option value="size-desc"><?php esc_html_e( 'Méret (nagyobb elöl)', 'vanbudapest-media-manager' ); ?></option>
                </select>
                <button type="button" class="button" id="vbmm-reset-filters">
                    <span class="dashicons dashicons-dismiss"></span>
                    <?php esc_html_e( 'Szűrők törlése', 'vanbudapest-media-manager' ); ?>
                </button>
            </div>

            <!-- Bulk Actions Bar (shown when items selected) -->
            <div class="vbmm-bulk-bar" id="vbmm-bulk-bar" style="display:none;">
                <div class="vbmm-bulk-left">
                    <strong id="vbmm-bulk-count">0</strong> <?php esc_html_e( 'elem kijelölve', 'vanbudapest-media-manager' ); ?>
                </div>
                <div class="vbmm-bulk-actions">
                    <div class="vbmm-export-group">
                        <span class="vbmm-export-label"><?php esc_html_e( 'Exportálás:', 'vanbudapest-media-manager' ); ?></span>
                        <button type="button" class="button vbmm-export-btn" data-format="html" title="HTML img tag-ek">
                            <span class="dashicons dashicons-editor-code"></span> HTML
                        </button>
                        <button type="button" class="button vbmm-export-btn" data-format="urls" title="Sima URL-ek">
                            <span class="dashicons dashicons-admin-links"></span> URL
                        </button>
                        <button type="button" class="button vbmm-export-btn" data-format="markdown" title="Markdown formátum">
                            <span class="dashicons dashicons-editor-paste-text"></span> MD
                        </button>
                        <button type="button" class="button vbmm-export-btn" data-format="css" title="CSS background-image">
                            <span class="dashicons dashicons-art"></span> CSS
                        </button>
                        <button type="button" class="button vbmm-export-btn" data-format="array" title="JavaScript/PHP tömb">
                            <span class="dashicons dashicons-editor-ul"></span> Array
                        </button>
                        <button type="button" class="button vbmm-export-btn" data-format="csv" title="CSV export">
                            <span class="dashicons dashicons-media-spreadsheet"></span> CSV
                        </button>
                    </div>
                    <div class="vbmm-action-group">
                        <button type="button" class="button vbmm-bulk-optimize" id="vbmm-bulk-optimize" title="ShortPixel optimalizálás">
                            <span class="dashicons dashicons-performance"></span>
                            <?php esc_html_e( 'Optimalizálás', 'vanbudapest-media-manager' ); ?>
                        </button>
                        <button type="button" class="button vbmm-bulk-delete" id="vbmm-bulk-delete" title="Kijelöltek törlése">
                            <span class="dashicons dashicons-trash"></span>
                            <?php esc_html_e( 'Törlés', 'vanbudapest-media-manager' ); ?>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Stats Bar -->
            <div class="vbmm-stats-bar" id="vbmm-stats-bar">
                <span class="vbmm-stat">
                    <span class="dashicons dashicons-images-alt2"></span>
                    <span id="vbmm-stat-total">0</span> <?php esc_html_e( 'fájl', 'vanbudapest-media-manager' ); ?>
                </span>
                <span class="vbmm-stat">
                    <span class="dashicons dashicons-database"></span>
                    <span id="vbmm-stat-size">0 MB</span>
                </span>
                <span class="vbmm-stat vbmm-stat-shortpixel" style="display:none;">
                    <span class="dashicons dashicons-performance"></span>
                    <span id="vbmm-stat-optimized">0</span> <?php esc_html_e( 'optimalizálva', 'vanbudapest-media-manager' ); ?>
                </span>
            </div>

            <!-- Media Grid -->
            <div class="vbmm-media-container" id="vbmm-media-container">
                <div class="vbmm-loading" id="vbmm-loading">
                    <span class="spinner is-active"></span>
                    <p><?php esc_html_e( 'Médiatár betöltése...', 'vanbudapest-media-manager' ); ?></p>
                </div>
                <div class="vbmm-media-grid" id="vbmm-media-grid"></div>
                <div class="vbmm-no-results" id="vbmm-no-results" style="display:none;">
                    <span class="dashicons dashicons-format-image"></span>
                    <p><?php esc_html_e( 'Nincs találat a szűrőknek megfelelően.', 'vanbudapest-media-manager' ); ?></p>
                </div>
            </div>

            <!-- Load More -->
            <div class="vbmm-load-more" id="vbmm-load-more" style="display:none;">
                <button type="button" class="button button-primary" id="vbmm-load-more-btn">
                    <?php esc_html_e( 'Továbbiak betöltése', 'vanbudapest-media-manager' ); ?>
                </button>
            </div>

            <!-- Export Modal -->
            <div class="vbmm-modal" id="vbmm-export-modal" style="display:none;">
                <div class="vbmm-modal-overlay"></div>
                <div class="vbmm-modal-content">
                    <div class="vbmm-modal-header">
                        <h2 id="vbmm-modal-title"><?php esc_html_e( 'Exportált kód', 'vanbudapest-media-manager' ); ?></h2>
                        <button type="button" class="vbmm-modal-close" id="vbmm-modal-close">&times;</button>
                    </div>
                    <div class="vbmm-modal-body">
                        <div class="vbmm-export-options" id="vbmm-export-options"></div>
                        <textarea class="vbmm-export-code" id="vbmm-export-code" readonly rows="15"></textarea>
                    </div>
                    <div class="vbmm-modal-footer">
                        <button type="button" class="button button-primary" id="vbmm-copy-export">
                            <span class="dashicons dashicons-clipboard"></span>
                            <?php esc_html_e( 'Vágólapra másolás', 'vanbudapest-media-manager' ); ?>
                        </button>
                        <button type="button" class="button" id="vbmm-download-export">
                            <span class="dashicons dashicons-download"></span>
                            <?php esc_html_e( 'Letöltés', 'vanbudapest-media-manager' ); ?>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Inline Edit Panel -->
            <div class="vbmm-edit-panel" id="vbmm-edit-panel" style="display:none;">
                <div class="vbmm-edit-panel-header">
                    <h3><?php esc_html_e( 'Részletek szerkesztése', 'vanbudapest-media-manager' ); ?></h3>
                    <button type="button" class="vbmm-edit-close" id="vbmm-edit-close">&times;</button>
                </div>
                <div class="vbmm-edit-panel-body">
                    <div class="vbmm-edit-preview">
                        <img id="vbmm-edit-preview-img" src="" alt="">
                    </div>
                    <div class="vbmm-edit-fields">
                        <input type="hidden" id="vbmm-edit-id">
                        <div class="vbmm-field">
                            <label for="vbmm-edit-title"><?php esc_html_e( 'Cím', 'vanbudapest-media-manager' ); ?></label>
                            <input type="text" id="vbmm-edit-title">
                        </div>
                        <div class="vbmm-field">
                            <label for="vbmm-edit-alt"><?php esc_html_e( 'Alt szöveg', 'vanbudapest-media-manager' ); ?></label>
                            <input type="text" id="vbmm-edit-alt">
                        </div>
                        <div class="vbmm-field">
                            <label for="vbmm-edit-caption"><?php esc_html_e( 'Felirat', 'vanbudapest-media-manager' ); ?></label>
                            <textarea id="vbmm-edit-caption" rows="2"></textarea>
                        </div>
                        <div class="vbmm-field">
                            <label for="vbmm-edit-description"><?php esc_html_e( 'Leírás', 'vanbudapest-media-manager' ); ?></label>
                            <textarea id="vbmm-edit-description" rows="3"></textarea>
                        </div>
                        <div class="vbmm-field vbmm-field-readonly">
                            <label><?php esc_html_e( 'Fájl URL', 'vanbudapest-media-manager' ); ?></label>
                            <div class="vbmm-url-field">
                                <input type="text" id="vbmm-edit-url" readonly>
                                <button type="button" class="button vbmm-copy-url" title="URL másolása">
                                    <span class="dashicons dashicons-clipboard"></span>
                                </button>
                            </div>
                        </div>
                        <div class="vbmm-field vbmm-field-readonly">
                            <label><?php esc_html_e( 'Fájl méret', 'vanbudapest-media-manager' ); ?></label>
                            <span id="vbmm-edit-filesize"></span>
                        </div>
                        <div class="vbmm-field vbmm-field-readonly">
                            <label><?php esc_html_e( 'Méret (px)', 'vanbudapest-media-manager' ); ?></label>
                            <span id="vbmm-edit-dimensions"></span>
                        </div>
                        <div class="vbmm-field vbmm-field-readonly">
                            <label><?php esc_html_e( 'Feltöltve', 'vanbudapest-media-manager' ); ?></label>
                            <span id="vbmm-edit-date"></span>
                        </div>
                        <div class="vbmm-edit-sizes" id="vbmm-edit-sizes">
                            <label><?php esc_html_e( 'Elérhető méretek', 'vanbudapest-media-manager' ); ?></label>
                            <div id="vbmm-sizes-list"></div>
                        </div>
                    </div>
                </div>
                <div class="vbmm-edit-panel-footer">
                    <button type="button" class="button button-primary" id="vbmm-edit-save">
                        <span class="dashicons dashicons-saved"></span>
                        <?php esc_html_e( 'Mentés', 'vanbudapest-media-manager' ); ?>
                    </button>
                    <a href="#" class="button" id="vbmm-edit-wp-link" target="_blank">
                        <span class="dashicons dashicons-edit"></span>
                        <?php esc_html_e( 'Szerkesztés WP-ben', 'vanbudapest-media-manager' ); ?>
                    </a>
                </div>
            </div>
        </div>
        <?php
    }

    /**
     * Generate date filter options from existing uploads
     */
    private function get_date_options() {
        global $wpdb;
        $months = $wpdb->get_results(
            "SELECT DISTINCT YEAR(post_date) AS year, MONTH(post_date) AS month
             FROM {$wpdb->posts}
             WHERE post_type = 'attachment'
             ORDER BY post_date DESC"
        );

        $output = '';
        $month_names = array(
            1 => 'Január', 2 => 'Február', 3 => 'Március', 4 => 'Április',
            5 => 'Május', 6 => 'Június', 7 => 'Július', 8 => 'Augusztus',
            9 => 'Szeptember', 10 => 'Október', 11 => 'November', 12 => 'December',
        );

        foreach ( $months as $row ) {
            $value = sprintf( '%04d-%02d', $row->year, $row->month );
            $label = $month_names[ (int) $row->month ] . ' ' . $row->year;
            $output .= sprintf( '<option value="%s">%s</option>', esc_attr( $value ), esc_html( $label ) );
        }

        return $output;
    }
}
