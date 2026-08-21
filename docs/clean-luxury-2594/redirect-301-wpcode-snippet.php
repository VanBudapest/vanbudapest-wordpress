<?php
/**
 * WPCode snippet - VanBudapest.com
 * Title    : VB 301 - Clean Luxury (2594) regi COVID slug atiranyitas
 * Code Type: PHP Snippet
 * Location : Run Everywhere
 * Status   : Active
 *
 * Miert kell: a 2594-es oldal slugja 2026-08-21-en
 *   covid-hungary-private-bus-airport-transfer  ->  clean-hungary-private-bus-airport-transfer
 * lett. A WordPress beepitett _wp_old_slug atiranyitasa PAGE tipusnal ezen a
 * permalink-strukturan NEM sul el (a rewrite csak `pagename` query-vart allit be,
 * a wp_old_slug_redirect() viszont `name`-et var), ezert kell ez a snippet.
 *
 * A kod alatti resz mehet a WPCode "Code Preview" mezojebe (a nyito <?php nelkul).
 */

add_action( 'template_redirect', function () {
    if ( ! is_404() ) { return; }
    $old = 'covid-hungary-private-bus-airport-transfer';
    $new = 'clean-hungary-private-bus-airport-transfer';
    $uri = isset( $_SERVER['REQUEST_URI'] ) ? $_SERVER['REQUEST_URI'] : '';
    $path = trim( (string) parse_url( $uri, PHP_URL_PATH ), '/' );
    if ( $path === $old ) {
        wp_safe_redirect( home_url( '/' . $new . '/' ), 301 );
        exit;
    }
}, 1 );
