<?php
/**
 * VanBudapest Booking Form v2 - WPCode Snippet
 *
 * HASZNÁLAT:
 * 1. Menj a WPCode → Add Snippet → Custom Code
 * 2. Válaszd: "PHP Snippet"
 * 3. Illeszd be ezt a teljes kódot
 * 4. Location: "Admin Only"
 * 5. Mentsd és aktiváld
 * 6. Nyisd meg: WP Admin → Forminator → Forms
 * 7. Ha létrejött az űrlap, DEAKTIVÁLD a snippetet!
 *
 * @version 2.0
 */

// Csak egyszer fusson le
if (get_option('vb_booking_form_v2_created')) {
    return;
}

// Csak admin területen
if (!is_admin()) {
    return;
}

// Ellenőrizzük, hogy Forminator aktív-e
if (!class_exists('Forminator_Base_Form_Model')) {
    return;
}

add_action('admin_init', function() {
    // Dupla ellenőrzés
    if (get_option('vb_booking_form_v2_created')) {
        return;
    }

    // Ellenőrizzük, hogy létezik-e már ilyen nevű űrlap
    global $wpdb;
    $existing = $wpdb->get_var("SELECT id FROM {$wpdb->prefix}posts WHERE post_title = 'VanBudapest Booking Form v2' AND post_type = 'forminator_forms' LIMIT 1");

    if ($existing) {
        update_option('vb_booking_form_v2_created', true);
        return;
    }

    // Form wrapper és mező definíciók
    $form_fields = array();

    // ========================================
    // STEP 1 - SERVICE SELECTION
    // ========================================

    // Page Break 1
    $form_fields[] = array(
        'element_id' => 'page-break-1',
        'type' => 'page-break',
        'label' => 'Service Selection'
    );

    // HTML Title
    $form_fields[] = array(
        'element_id' => 'html-1',
        'type' => 'html',
        'variations' => '<h2 style="font-family: Georgia, serif; font-size: 28px; color: #0A1F44; margin-bottom: 8px;">How can we help you today?</h2><p style="color: #666; margin-bottom: 24px;">Select the service that best fits your needs</p>'
    );

    // Service Selection Radio
    $form_fields[] = array(
        'element_id' => 'radio-1',
        'type' => 'radio',
        'field_label' => 'Select Service Type',
        'required' => true,
        'options' => array(
            array('label' => 'Transfers (Airport & Long-Distance) - One-way or return, any distance', 'value' => 'airport', 'key' => 'airport'),
            array('label' => 'Hourly Ride & Sightseeing - Chauffeur service or guided tours', 'value' => 'hourly', 'key' => 'hourly'),
            array('label' => 'Multi-day Trips - Private tours & trips', 'value' => 'countryside', 'key' => 'countryside'),
            array('label' => 'Event Transportation - Conferences & groups', 'value' => 'event', 'key' => 'event'),
            array('label' => 'UEFA CL Final - May 28-31, 2026', 'value' => 'uefa', 'key' => 'uefa'),
            array('label' => 'F1 Grand Prix - July 23-26, 2026', 'value' => 'f1', 'key' => 'f1')
        ),
        'layout' => 'vertical'
    );

    // ========================================
    // STEP 2 - VEHICLE & GROUP
    // ========================================

    $form_fields[] = array(
        'element_id' => 'page-break-2',
        'type' => 'page-break',
        'label' => 'Vehicle & Group'
    );

    $form_fields[] = array(
        'element_id' => 'html-2',
        'type' => 'html',
        'variations' => '<h2 style="font-family: Georgia, serif; font-size: 28px; color: #0A1F44; margin-bottom: 8px;">Vehicle & Group Details</h2><p style="color: #666; margin-bottom: 24px;">Select your preferred vehicle(s) and group size</p>'
    );

    // Vehicle Checkboxes
    $form_fields[] = array(
        'element_id' => 'checkbox-1',
        'type' => 'checkbox',
        'field_label' => 'Select Vehicle(s)',
        'options' => array(
            array('label' => 'Business Car - up to 3 pax - Mercedes E-Class', 'value' => 'business-car', 'key' => 'business-car'),
            array('label' => 'Premium VAN - up to 6-7 pax - Mercedes V-Class', 'value' => 'premium-van', 'key' => 'premium-van'),
            array('label' => 'Minibus - up to 14-20 pax - Mercedes Sprinter', 'value' => 'minibus', 'key' => 'minibus'),
            array('label' => 'Coach Bus - up to 49 pax - Mercedes Tourismo', 'value' => 'coach', 'key' => 'coach'),
            array('label' => 'Luxury Minibus VIP - up to 8 pax - Mercedes Sprinter', 'value' => 'luxury-minibus', 'key' => 'luxury-minibus'),
            array('label' => 'Luxury Car VIP - up to 3 pax - Mercedes S-Class', 'value' => 'luxury-car', 'key' => 'luxury-car')
        )
    );

    // Guest count
    $form_fields[] = array(
        'element_id' => 'number-1',
        'type' => 'number',
        'field_label' => 'Total Number of Guests',
        'required' => true,
        'default_value' => '1',
        'limit_min' => '1',
        'limit_max' => '500'
    );

    // Luggage
    $form_fields[] = array(
        'element_id' => 'number-2',
        'type' => 'number',
        'field_label' => 'Pieces of Luggage',
        'default_value' => '0',
        'limit_min' => '0',
        'limit_max' => '100'
    );

    // Special items
    $form_fields[] = array(
        'element_id' => 'text-1',
        'type' => 'text',
        'field_label' => 'Special Items / Notes',
        'placeholder' => 'e.g., Golf bags, Ski equipment, Wheelchair, Child seats'
    );

    // ========================================
    // STEP 3 - SERVICE DETAILS
    // ========================================

    $form_fields[] = array(
        'element_id' => 'page-break-3',
        'type' => 'page-break',
        'label' => 'Service Details'
    );

    // === AIRPORT SECTION ===
    $form_fields[] = array(
        'element_id' => 'html-3',
        'type' => 'html',
        'variations' => '<h2 style="font-family: Georgia, serif; font-size: 28px; color: #0A1F44;">Transfer Details</h2><p style="color: #666;">One-way or return transfers, any distance</p>',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'date-1',
        'type' => 'date',
        'field_label' => 'Pickup Date',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'time-1',
        'type' => 'time',
        'field_label' => 'Pickup Time',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-2',
        'type' => 'text',
        'field_label' => 'Pickup Address',
        'required' => true,
        'placeholder' => 'e.g., Budapest Airport Terminal 2B, Hotel name, or any address',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-3',
        'type' => 'text',
        'field_label' => 'Drop-off Address',
        'required' => true,
        'placeholder' => 'e.g., Hilton Budapest, Airport, or any destination',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-4',
        'type' => 'text',
        'field_label' => 'Flight Number (optional)',
        'placeholder' => 'e.g., FR1023',
        'description' => 'For airport pickups, we monitor your flight for delays',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
            )
        )
    );

    // Return transfer
    $form_fields[] = array(
        'element_id' => 'radio-2',
        'type' => 'radio',
        'field_label' => 'Do you require a return transfer?',
        'required' => true,
        'options' => array(
            array('label' => 'Yes', 'value' => 'yes', 'key' => 'yes'),
            array('label' => 'No', 'value' => 'no', 'key' => 'no', 'default' => true)
        ),
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
            )
        )
    );

    // Return fields
    $form_fields[] = array(
        'element_id' => 'date-2',
        'type' => 'date',
        'field_label' => 'Return Date',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport'),
                array('element_id' => 'radio-2', 'rule' => 'is', 'value' => 'yes')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'time-2',
        'type' => 'time',
        'field_label' => 'Return Time',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport'),
                array('element_id' => 'radio-2', 'rule' => 'is', 'value' => 'yes')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-5',
        'type' => 'text',
        'field_label' => 'Return Pickup Address',
        'required' => true,
        'placeholder' => 'e.g., Hotel address for return journey',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport'),
                array('element_id' => 'radio-2', 'rule' => 'is', 'value' => 'yes')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-6',
        'type' => 'text',
        'field_label' => 'Return Drop-off Address',
        'required' => true,
        'placeholder' => 'e.g., Budapest Airport Terminal 2B',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport'),
                array('element_id' => 'radio-2', 'rule' => 'is', 'value' => 'yes')
            )
        )
    );

    // === HOURLY SECTION ===
    $form_fields[] = array(
        'element_id' => 'html-4',
        'type' => 'html',
        'variations' => '<h2 style="font-family: Georgia, serif; font-size: 28px; color: #0A1F44;">Hourly Ride & Sightseeing</h2><p style="color: #666;">Chauffeur service or private guided tour</p>',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'radio-3',
        'type' => 'radio',
        'field_label' => 'Service Type',
        'required' => true,
        'options' => array(
            array('label' => 'Chauffeur Service (driver only) - You direct the route', 'value' => 'chauffeur', 'key' => 'chauffeur'),
            array('label' => 'Private Sightseeing Tour (driver + guide) - Expert guide plans the tour', 'value' => 'sightseeing', 'key' => 'sightseeing')
        ),
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'select-1',
        'type' => 'select',
        'field_label' => 'Guide Language',
        'required' => true,
        'options' => array(
            array('label' => '-- Select language --', 'value' => '', 'key' => ''),
            array('label' => 'English', 'value' => 'english', 'key' => 'english'),
            array('label' => 'German', 'value' => 'german', 'key' => 'german'),
            array('label' => 'Spanish', 'value' => 'spanish', 'key' => 'spanish'),
            array('label' => 'French', 'value' => 'french', 'key' => 'french'),
            array('label' => 'Italian', 'value' => 'italian', 'key' => 'italian'),
            array('label' => 'Russian', 'value' => 'russian', 'key' => 'russian'),
            array('label' => 'Chinese', 'value' => 'chinese', 'key' => 'chinese'),
            array('label' => 'Polish', 'value' => 'polish', 'key' => 'polish')
        ),
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly'),
                array('element_id' => 'radio-3', 'rule' => 'is', 'value' => 'sightseeing')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'radio-4',
        'type' => 'radio',
        'field_label' => 'Tour Package',
        'required' => true,
        'options' => array(
            array('label' => 'Castle District Focus (3-4 hours)', 'value' => 'castle', 'key' => 'castle'),
            array('label' => 'Pest Highlights (3-4 hours)', 'value' => 'pest', 'key' => 'pest'),
            array('label' => 'Budapest Classic (4-5 hours) - MOST POPULAR', 'value' => 'classic', 'key' => 'classic'),
            array('label' => 'Grand Budapest Tour (6+ hours)', 'value' => 'grand', 'key' => 'grand'),
            array('label' => 'Jewish Heritage (3-4 hours)', 'value' => 'jewish', 'key' => 'jewish'),
            array('label' => 'Custom Tour', 'value' => 'custom', 'key' => 'custom')
        ),
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly'),
                array('element_id' => 'radio-3', 'rule' => 'is', 'value' => 'sightseeing')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'date-3',
        'type' => 'date',
        'field_label' => 'Pickup Date',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'time-3',
        'type' => 'time',
        'field_label' => 'Pickup Time',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'select-2',
        'type' => 'select',
        'field_label' => 'Ride Duration',
        'required' => true,
        'description' => 'Minimum rental duration is 3+1 hours',
        'options' => array(
            array('label' => '-- Select duration --', 'value' => '', 'key' => ''),
            array('label' => '3 hours (3+1)', 'value' => '3', 'key' => '3'),
            array('label' => '4 hours (4+1)', 'value' => '4', 'key' => '4'),
            array('label' => '5 hours (5+1)', 'value' => '5', 'key' => '5'),
            array('label' => '6 hours (6+1)', 'value' => '6', 'key' => '6'),
            array('label' => '8 hours (8+1)', 'value' => '8', 'key' => '8'),
            array('label' => '10 hours (10+1)', 'value' => '10', 'key' => '10'),
            array('label' => '12 hours (12+1)', 'value' => '12', 'key' => '12')
        ),
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly'),
                array('element_id' => 'radio-3', 'rule' => 'is', 'value' => 'chauffeur')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-7',
        'type' => 'text',
        'field_label' => 'Pickup Address',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-8',
        'type' => 'text',
        'field_label' => 'Drop-off Address',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
            )
        )
    );

    // === MULTI-DAY SECTION ===
    $form_fields[] = array(
        'element_id' => 'html-5',
        'type' => 'html',
        'variations' => '<h2 style="font-family: Georgia, serif; font-size: 28px; color: #0A1F44;">Multi-day Trip Details</h2><p style="color: #666;">Plan your private tour or extended trip</p>',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'date-4',
        'type' => 'date',
        'field_label' => 'Start Date',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'number-3',
        'type' => 'number',
        'field_label' => 'Total Days',
        'required' => true,
        'limit_min' => '2',
        'limit_max' => '30',
        'description' => 'Minimum 2 days',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-9',
        'type' => 'text',
        'field_label' => 'Pickup Address',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'textarea-1',
        'type' => 'textarea',
        'field_label' => 'Trip Itinerary / Details',
        'required' => true,
        'placeholder' => 'Day 1: Budapest - Eger (wine tasting)\nDay 2: Eger - Tokaj - return to Budapest',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
            )
        )
    );

    // === F1 SECTION ===
    $form_fields[] = array(
        'element_id' => 'html-6',
        'type' => 'html',
        'variations' => '<h2 style="font-family: Georgia, serif; font-size: 28px; color: #0A1F44;">F1 Grand Prix Transfers</h2><p style="color: #666;">July 23-26, 2026 - Hungaroring</p>',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'f1')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'checkbox-2',
        'type' => 'checkbox',
        'field_label' => 'Select the days you need transportation',
        'required' => true,
        'options' => array(
            array('label' => 'Thursday, July 23, 2026', 'value' => 'thu', 'key' => 'thu'),
            array('label' => 'Friday, July 24, 2026', 'value' => 'fri', 'key' => 'fri'),
            array('label' => 'Saturday, July 25, 2026', 'value' => 'sat', 'key' => 'sat'),
            array('label' => 'Sunday, July 26, 2026', 'value' => 'sun', 'key' => 'sun')
        ),
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'f1')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-10',
        'type' => 'text',
        'field_label' => 'Pickup Address',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'f1')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-11',
        'type' => 'text',
        'field_label' => 'Drop-off Address',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'f1')
            )
        )
    );

    // === UEFA SECTION ===
    $form_fields[] = array(
        'element_id' => 'html-7',
        'type' => 'html',
        'variations' => '<h2 style="font-family: Georgia, serif; font-size: 28px; color: #0A1F44;">UEFA Champions League Final</h2><p style="color: #666;">May 28-31, 2026 - Puskas Arena</p>',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'uefa')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'checkbox-3',
        'type' => 'checkbox',
        'field_label' => 'Select the days you need transportation',
        'required' => true,
        'options' => array(
            array('label' => 'Thursday, May 28, 2026 (min. 6 hours)', 'value' => 'thu', 'key' => 'thu'),
            array('label' => 'Friday, May 29, 2026 (min. 6 hours)', 'value' => 'fri', 'key' => 'fri'),
            array('label' => 'Saturday, May 30, 2026 (MATCH DAY - min. 12 hours)', 'value' => 'sat', 'key' => 'sat'),
            array('label' => 'Sunday, May 31, 2026 (min. 6 hours)', 'value' => 'sun', 'key' => 'sun')
        ),
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'uefa')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-12',
        'type' => 'text',
        'field_label' => 'Pickup Address',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'uefa')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'textarea-2',
        'type' => 'textarea',
        'field_label' => 'Route & Stops',
        'required' => true,
        'placeholder' => 'e.g., Hotel - Puskas Arena - City Park - Return to hotel',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'uefa')
            )
        )
    );

    // === EVENT SECTION ===
    $form_fields[] = array(
        'element_id' => 'html-8',
        'type' => 'html',
        'variations' => '<h2 style="font-family: Georgia, serif; font-size: 28px; color: #0A1F44;">Event Transportation</h2><p style="color: #666;">Tell us about your event and transportation needs</p>',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-13',
        'type' => 'text',
        'field_label' => 'Event Name',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-14',
        'type' => 'text',
        'field_label' => 'Organization Name',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'select-3',
        'type' => 'select',
        'field_label' => 'Event Type',
        'required' => true,
        'options' => array(
            array('label' => '-- Select --', 'value' => '', 'key' => ''),
            array('label' => 'Conference / Summit', 'value' => 'conference', 'key' => 'conference'),
            array('label' => 'Corporate Meeting', 'value' => 'corporate', 'key' => 'corporate'),
            array('label' => 'Wedding', 'value' => 'wedding', 'key' => 'wedding'),
            array('label' => 'Gala / Award Ceremony', 'value' => 'gala', 'key' => 'gala'),
            array('label' => 'Sports Event', 'value' => 'sports', 'key' => 'sports'),
            array('label' => 'Film / TV Production', 'value' => 'film', 'key' => 'film'),
            array('label' => 'Other', 'value' => 'other', 'key' => 'other')
        ),
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'number-4',
        'type' => 'number',
        'field_label' => 'Expected Guests',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'date-5',
        'type' => 'date',
        'field_label' => 'Event Start Date',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'date-6',
        'type' => 'date',
        'field_label' => 'Event End Date',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'text-15',
        'type' => 'text',
        'field_label' => 'Event Venue / Location',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
            )
        )
    );

    $form_fields[] = array(
        'element_id' => 'textarea-3',
        'type' => 'textarea',
        'field_label' => 'Schedule / Key Moves',
        'placeholder' => 'e.g., May 15, 10:00 - Airport to Hilton - 25 guests',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
            )
        )
    );

    // Special Requirements (all services)
    $form_fields[] = array(
        'element_id' => 'checkbox-4',
        'type' => 'checkbox',
        'field_label' => 'Special Requirements (optional)',
        'options' => array(
            array('label' => 'Wheelchair accessible', 'value' => 'wheelchair', 'key' => 'wheelchair'),
            array('label' => 'Child safety seats', 'value' => 'child-seats', 'key' => 'child-seats'),
            array('label' => 'Hostess / Additional Staff', 'value' => 'hostess', 'key' => 'hostess'),
            array('label' => 'On-site coordinator', 'value' => 'coordinator', 'key' => 'coordinator'),
            array('label' => 'English-speaking driver', 'value' => 'english-driver', 'key' => 'english-driver'),
            array('label' => 'Security / Protocol', 'value' => 'security', 'key' => 'security')
        )
    );

    $form_fields[] = array(
        'element_id' => 'textarea-4',
        'type' => 'textarea',
        'field_label' => 'Additional Preferences (optional)',
        'placeholder' => 'Any other requests or preferences...'
    );

    // ========================================
    // STEP 4 - CONTACT & BILLING
    // ========================================

    $form_fields[] = array(
        'element_id' => 'page-break-4',
        'type' => 'page-break',
        'label' => 'Contact & Billing'
    );

    $form_fields[] = array(
        'element_id' => 'html-9',
        'type' => 'html',
        'variations' => '<h2 style="font-family: Georgia, serif; font-size: 28px; color: #0A1F44;">Contact & Billing</h2><p style="color: #666;">Provide your contact details</p>'
    );

    // Name
    $form_fields[] = array(
        'element_id' => 'name-1',
        'type' => 'name',
        'field_label' => 'Your Name',
        'required' => true,
        'fname' => true,
        'lname' => true,
        'prefix' => false
    );

    // Email
    $form_fields[] = array(
        'element_id' => 'email-1',
        'type' => 'email',
        'field_label' => 'Email',
        'required' => true,
        'placeholder' => 'email@example.com'
    );

    // Phone
    $form_fields[] = array(
        'element_id' => 'phone-1',
        'type' => 'phone',
        'field_label' => 'Phone',
        'required' => true,
        'placeholder' => '+36 70 XXX XXXX'
    );

    // Booking for other
    $form_fields[] = array(
        'element_id' => 'checkbox-5',
        'type' => 'checkbox',
        'field_label' => '',
        'options' => array(
            array('label' => 'I am booking for someone else', 'value' => 'yes', 'key' => 'yes')
        )
    );

    // Passenger name (conditional)
    $form_fields[] = array(
        'element_id' => 'name-2',
        'type' => 'name',
        'field_label' => 'Passenger Name',
        'required' => true,
        'fname' => true,
        'lname' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'checkbox-5', 'rule' => 'is', 'value' => 'yes')
            )
        )
    );

    // Passenger phone (conditional)
    $form_fields[] = array(
        'element_id' => 'phone-2',
        'type' => 'phone',
        'field_label' => 'Passenger Mobile',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'checkbox-5', 'rule' => 'is', 'value' => 'yes')
            )
        )
    );

    // Billing toggle
    $form_fields[] = array(
        'element_id' => 'checkbox-6',
        'type' => 'checkbox',
        'field_label' => '',
        'options' => array(
            array('label' => 'I need an invoice with specific billing details', 'value' => 'yes', 'key' => 'yes')
        )
    );

    // Billing name (conditional)
    $form_fields[] = array(
        'element_id' => 'text-16',
        'type' => 'text',
        'field_label' => 'Name or Company Name',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'checkbox-6', 'rule' => 'is', 'value' => 'yes')
            )
        )
    );

    // Billing address (conditional)
    $form_fields[] = array(
        'element_id' => 'text-17',
        'type' => 'text',
        'field_label' => 'Billing Address',
        'required' => true,
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'checkbox-6', 'rule' => 'is', 'value' => 'yes')
            )
        )
    );

    // VAT (conditional)
    $form_fields[] = array(
        'element_id' => 'text-18',
        'type' => 'text',
        'field_label' => 'VAT / Tax Number',
        'placeholder' => 'e.g., HU12345678',
        'conditions' => array(
            'action' => 'show',
            'rule' => 'all',
            'conditions' => array(
                array('element_id' => 'checkbox-6', 'rule' => 'is', 'value' => 'yes')
            )
        )
    );

    // How heard
    $form_fields[] = array(
        'element_id' => 'select-4',
        'type' => 'select',
        'field_label' => 'How did you hear about us?',
        'options' => array(
            array('label' => '-- Select --', 'value' => '', 'key' => ''),
            array('label' => 'Google Search', 'value' => 'google', 'key' => 'google'),
            array('label' => 'Social Media', 'value' => 'social', 'key' => 'social'),
            array('label' => 'Recommendation', 'value' => 'recommendation', 'key' => 'recommendation'),
            array('label' => 'Travel Agency / DMC', 'value' => 'travel-agency', 'key' => 'travel-agency'),
            array('label' => 'Returning Customer', 'value' => 'returning', 'key' => 'returning'),
            array('label' => 'Hotel Concierge', 'value' => 'hotel', 'key' => 'hotel'),
            array('label' => 'Other', 'value' => 'other', 'key' => 'other')
        )
    );

    // Promo code
    $form_fields[] = array(
        'element_id' => 'text-19',
        'type' => 'text',
        'field_label' => 'Promo Code (optional)',
        'placeholder' => 'Enter promo code if you have one'
    );

    // Payment method
    $form_fields[] = array(
        'element_id' => 'radio-5',
        'type' => 'radio',
        'field_label' => 'Preferred Payment Method',
        'required' => true,
        'options' => array(
            array('label' => 'Bank Transfer - No additional fees', 'value' => 'bank_transfer', 'key' => 'bank_transfer', 'default' => true),
            array('label' => 'Credit Card - +3% processing fee', 'value' => 'credit_card', 'key' => 'credit_card')
        )
    );

    // Terms
    $form_fields[] = array(
        'element_id' => 'consent-1',
        'type' => 'consent',
        'field_label' => 'I accept the Terms & Conditions and Privacy Policy',
        'required' => true,
        'consent_description' => 'I accept the <a href="/terms" target="_blank">Terms & Conditions</a> and <a href="/privacy" target="_blank">Privacy Policy</a>'
    );

    // ========================================
    // CREATE THE FORM
    // ========================================

    // Build wrappers from fields
    $wrappers = array();
    $wrapper_id = 1000000000;

    foreach ($form_fields as $field) {
        $wrapper_id++;
        $wrappers[] = array(
            'wrapper_id' => 'wrapper-' . $wrapper_id . '-' . rand(1000, 9999),
            'fields' => array($field)
        );
    }

    // Form settings
    $settings = array(
        'formName' => 'VanBudapest Booking Form v2',
        'form-type' => 'default',
        'form-style' => 'default',
        'enable-ajax' => 'true',
        'validation-inline' => true,
        'pagination-header' => 'nav',
        'submission-behaviour' => 'behaviour-thankyou',
        'thankyou-message' => 'Thank you for your booking request! We will contact you within 24 hours with a personalized quote.',
        'submitData' => array(
            'button-text' => 'Request a Quote',
            'button-processing-text' => 'Submitting...'
        )
    );

    // Create form post
    $post_data = array(
        'post_title' => 'VanBudapest Booking Form v2',
        'post_type' => 'forminator_forms',
        'post_status' => 'publish'
    );

    $form_id = wp_insert_post($post_data);

    if (!is_wp_error($form_id)) {
        // Save form meta
        update_post_meta($form_id, 'forminator_form_meta', $wrappers);
        update_post_meta($form_id, 'forminator_settings', $settings);

        // Mark as created
        update_option('vb_booking_form_v2_created', true);

        // Admin notice
        add_action('admin_notices', function() use ($form_id) {
            echo '<div class="notice notice-success is-dismissible">';
            echo '<p><strong>VanBudapest Booking Form v2</strong> successfully created! Form ID: ' . $form_id . '</p>';
            echo '<p>Shortcode: <code>[forminator_form id="' . $form_id . '"]</code></p>';
            echo '<p><strong>IMPORTANT:</strong> Deactivate this WPCode snippet now!</p>';
            echo '</div>';
        });
    }
});
