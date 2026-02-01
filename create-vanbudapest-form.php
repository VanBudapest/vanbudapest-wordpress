<?php
/**
 * VanBudapest Booking Form v2 - Forminator Form Creator
 *
 * HASZNÁLAT:
 * 1. Másold ezt a fájlt a WordPress gyökérmappájába (ahol a wp-config.php van)
 * 2. Futtasd egyszer a böngészőből: https://yoursite.com/create-vanbudapest-form.php
 * 3. Töröld a fájlt a sikeres létrehozás után!
 *
 * @version 2.0
 * @date 2026-01-31
 */

// Load WordPress
require_once('wp-load.php');

// Security check - only admins can run this
if (!current_user_can('manage_options')) {
    wp_die('Unauthorized access. Please log in as admin.');
}

// Check if Forminator is active
if (!class_exists('Forminator_API')) {
    wp_die('Forminator plugin is not active. Please install and activate Forminator first.');
}

echo "<h1>VanBudapest Booking Form v2 - Creator</h1>";
echo "<pre>";

// ============================================
// FORM SETTINGS
// ============================================
$settings = array(
    'formName' => 'VanBudapest Booking Form v2',
    'form-type' => 'default',
    'form-style' => 'default',
    'enable-ajax' => 'true',
    'validation-inline' => true,
    'form-padding' => 'custom',
    'form-padding-top' => '0',
    'form-padding-right' => '0',
    'form-padding-bottom' => '0',
    'form-padding-left' => '0',
    'form-border' => 'none',
    'pagination-header' => 'nav',
    'submission-behaviour' => 'behaviour-thankyou',
    'thankyou-message' => 'Thank you for your booking request! We will contact you within 24 hours with a personalized quote.',
    'submitData' => array(
        'button-text' => 'Request a Quote →',
        'button-processing-text' => 'Submitting...'
    ),
    'pagination-labels' => array(
        'prev' => '← Back',
        'next' => 'Next →'
    )
);

// ============================================
// HELPER FUNCTIONS
// ============================================
function generate_wrapper_id() {
    return 'wrapper-' . rand(1000000000, 9999999999) . '-' . rand(1000, 9999);
}

// ============================================
// STEP 1: SERVICE SELECTION
// ============================================
$wrappers = array();

// Page break for step 1
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'page-break-1',
            'type' => 'page-break',
            'field_label' => 'Service Selection'
        )
    )
);

// HTML Title
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-1',
            'type' => 'html',
            'variations' => '<h2 class="vb-form-title">How can we help you today?</h2><p class="vb-form-subtitle">Select the service that best fits your needs</p>'
        )
    )
);

// Service Selection Radio
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'radio-1',
            'type' => 'radio',
            'field_label' => 'Select Service',
            'required' => 'true',
            'options' => array(
                array('label' => 'Transfers (Airport & Long-Distance) — One-way or return, any distance', 'value' => 'airport'),
                array('label' => 'Hourly Ride & Sightseeing — Chauffeur service or guided tours', 'value' => 'hourly'),
                array('label' => 'Multi-day Trips — Private tours & trips', 'value' => 'countryside'),
                array('label' => 'Event Transportation — Conferences & groups', 'value' => 'event'),
                array('label' => 'UEFA CL Final — May 28-31, 2026', 'value' => 'uefa'),
                array('label' => 'F1 Grand Prix — July 23-26, 2026', 'value' => 'f1')
            ),
            'layout' => 'vertical'
        )
    )
);

// ============================================
// STEP 2: VEHICLE & GROUP
// ============================================
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'page-break-2',
            'type' => 'page-break',
            'field_label' => 'Vehicle & Group'
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-2',
            'type' => 'html',
            'variations' => '<h2 class="vb-form-title">Vehicle & Group Details</h2><p class="vb-form-subtitle">Select your preferred vehicle(s) and group size</p>'
        )
    )
);

// Vehicle Checkboxes
$vehicles = array(
    array('id' => 'checkbox-1', 'label' => 'Business Car – up to 3 pax – Mercedes E-Class', 'value' => 'business-car'),
    array('id' => 'checkbox-2', 'label' => 'Premium VAN – up to 6-7 pax – Mercedes V-Class', 'value' => 'premium-van'),
    array('id' => 'checkbox-3', 'label' => 'Minibus – up to 14-20 pax – Mercedes Sprinter', 'value' => 'minibus'),
    array('id' => 'checkbox-4', 'label' => 'Coach Bus – up to 49 pax – Mercedes Tourismo', 'value' => 'coach'),
    array('id' => 'checkbox-5', 'label' => 'Luxury Minibus VIP – up to 8 pax – Mercedes Sprinter', 'value' => 'luxury-minibus'),
    array('id' => 'checkbox-6', 'label' => 'Luxury Car VIP – up to 3 pax – Mercedes S-Class', 'value' => 'luxury-car')
);

$number_id = 1;
foreach ($vehicles as $vehicle) {
    $wrappers[] = array(
        'wrapper_id' => generate_wrapper_id(),
        'fields' => array(
            array(
                'element_id' => $vehicle['id'],
                'type' => 'checkbox',
                'field_label' => $vehicle['label'],
                'options' => array(
                    array('label' => $vehicle['label'], 'value' => $vehicle['value'])
                )
            ),
            array(
                'element_id' => 'number-' . $number_id,
                'type' => 'number',
                'field_label' => 'Qty',
                'default_value' => '1',
                'limit_min' => '1',
                'limit_max' => '20',
                'conditions' => array(
                    'action' => 'show',
                    'rule' => 'all',
                    'conditions' => array(
                        array('element_id' => $vehicle['id'], 'rule' => 'is', 'value' => $vehicle['value'])
                    )
                )
            )
        )
    );
    $number_id++;
}

// Group Details
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'number-10',
            'type' => 'number',
            'field_label' => 'Total Number of Guests',
            'required' => 'true',
            'default_value' => '1',
            'limit_min' => '1',
            'limit_max' => '500'
        ),
        array(
            'element_id' => 'number-11',
            'type' => 'number',
            'field_label' => 'Pieces of Luggage',
            'default_value' => '0',
            'limit_min' => '0',
            'limit_max' => '100'
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-1',
            'type' => 'text',
            'field_label' => 'Special Items / Notes',
            'placeholder' => 'e.g., Golf bags, Ski equipment, Wheelchair, Child seats'
        )
    )
);

// ============================================
// STEP 3: SERVICE DETAILS
// ============================================
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'page-break-3',
            'type' => 'page-break',
            'field_label' => 'Service Details'
        )
    )
);

// ============================================
// AIRPORT TRANSFER SECTION
// ============================================
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-3',
            'type' => 'html',
            'variations' => '<h2 class="vb-form-title">Transfer Details</h2><p class="vb-form-subtitle">One-way or return transfers, any distance</p>',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'date-1',
            'type' => 'date',
            'field_label' => 'Pickup Date',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
                )
            )
        ),
        array(
            'element_id' => 'time-1',
            'type' => 'time',
            'field_label' => 'Pickup Time',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-2',
            'type' => 'text',
            'field_label' => 'Pickup Address',
            'required' => 'true',
            'placeholder' => 'e.g., Budapest Airport Terminal 2B, Hotel name, or any address',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-3',
            'type' => 'text',
            'field_label' => 'Drop-off Address',
            'required' => 'true',
            'placeholder' => 'e.g., Hilton Budapest, Airport, or any destination',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
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
        )
    )
);

// Return transfer question
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'radio-2',
            'type' => 'radio',
            'field_label' => 'Do you require a return transfer?',
            'required' => 'true',
            'options' => array(
                array('label' => 'Yes', 'value' => 'yes'),
                array('label' => 'No', 'value' => 'no', 'default' => true)
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
                )
            )
        )
    )
);

// Return transfer fields (conditional)
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'date-2',
            'type' => 'date',
            'field_label' => 'Return Date',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport'),
                    array('element_id' => 'radio-2', 'rule' => 'is', 'value' => 'yes')
                )
            )
        ),
        array(
            'element_id' => 'time-2',
            'type' => 'time',
            'field_label' => 'Return Time',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport'),
                    array('element_id' => 'radio-2', 'rule' => 'is', 'value' => 'yes')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-5',
            'type' => 'text',
            'field_label' => 'Return Pickup Address',
            'required' => 'true',
            'placeholder' => 'e.g., Hotel address for return journey',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport'),
                    array('element_id' => 'radio-2', 'rule' => 'is', 'value' => 'yes')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-6',
            'type' => 'text',
            'field_label' => 'Return Drop-off Address',
            'required' => 'true',
            'placeholder' => 'e.g., Budapest Airport Terminal 2B',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport'),
                    array('element_id' => 'radio-2', 'rule' => 'is', 'value' => 'yes')
                )
            )
        )
    )
);

// Airport Special Requirements
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-10',
            'type' => 'checkbox',
            'field_label' => 'Special Requirements (optional)',
            'options' => array(
                array('label' => 'Wheelchair accessible', 'value' => 'wheelchair'),
                array('label' => 'Child safety seats', 'value' => 'child-seats'),
                array('label' => 'Hostess / Additional Staff', 'value' => 'hostess'),
                array('label' => 'On-site coordinator', 'value' => 'coordinator'),
                array('label' => 'English-speaking driver', 'value' => 'english-driver'),
                array('label' => 'Security / Protocol', 'value' => 'security')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'textarea-1',
            'type' => 'textarea',
            'field_label' => 'Additional Preferences (optional)',
            'placeholder' => 'Any other requests or preferences...',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'airport')
                )
            )
        )
    )
);

// ============================================
// HOURLY RIDE SECTION
// ============================================
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-4',
            'type' => 'html',
            'variations' => '<h2 class="vb-form-title">Hourly Ride & Sightseeing</h2><p class="vb-form-subtitle">Chauffeur service or private guided tour in Budapest</p>',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'radio-3',
            'type' => 'radio',
            'field_label' => 'What type of service do you need?',
            'required' => 'true',
            'options' => array(
                array('label' => 'Chauffeur Service (driver only) - You direct the route', 'value' => 'chauffeur'),
                array('label' => 'Private Sightseeing Tour (driver + licensed guide) - Expert guide plans the tour', 'value' => 'sightseeing')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
                )
            )
        )
    )
);

// Guide Language (for sightseeing)
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'select-1',
            'type' => 'select',
            'field_label' => 'Guide Language',
            'required' => 'true',
            'options' => array(
                array('label' => '-- Select language --', 'value' => ''),
                array('label' => 'English', 'value' => 'english'),
                array('label' => 'German (Deutsch)', 'value' => 'german'),
                array('label' => 'Spanish (Español)', 'value' => 'spanish'),
                array('label' => 'French (Français)', 'value' => 'french'),
                array('label' => 'Italian (Italiano)', 'value' => 'italian'),
                array('label' => 'Russian', 'value' => 'russian'),
                array('label' => 'Chinese', 'value' => 'chinese'),
                array('label' => 'Polish (Polski)', 'value' => 'polish')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly'),
                    array('element_id' => 'radio-3', 'rule' => 'is', 'value' => 'sightseeing')
                )
            )
        )
    )
);

// Tour Package
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'radio-4',
            'type' => 'radio',
            'field_label' => 'Tour Package',
            'required' => 'true',
            'options' => array(
                array('label' => 'Castle District Focus (3-4 hours) - Buda Castle, Fishermans Bastion, Matthias Church', 'value' => 'castle'),
                array('label' => 'Pest Highlights (3-4 hours) - Downtown, Basilica, Parliament, Heroes Square', 'value' => 'pest'),
                array('label' => 'Budapest Classic (4-5 hours) - MOST POPULAR - Best of Buda and Pest', 'value' => 'classic'),
                array('label' => 'Grand Budapest Tour (6+ hours) - Full-day comprehensive tour', 'value' => 'grand'),
                array('label' => 'Jewish Heritage (3-4 hours) - Jewish Quarter, Great Synagogue', 'value' => 'jewish'),
                array('label' => 'Custom Tour - I have specific preferences', 'value' => 'custom')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly'),
                    array('element_id' => 'radio-3', 'rule' => 'is', 'value' => 'sightseeing')
                )
            )
        )
    )
);

// Custom tour requests
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'textarea-2',
            'type' => 'textarea',
            'field_label' => 'Tell us about your interests',
            'required' => 'true',
            'placeholder' => 'Tell us about your interests, must-see places, or any special requirements...',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly'),
                    array('element_id' => 'radio-3', 'rule' => 'is', 'value' => 'sightseeing'),
                    array('element_id' => 'radio-4', 'rule' => 'is', 'value' => 'custom')
                )
            )
        )
    )
);

// Hourly pickup date/time
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'date-3',
            'type' => 'date',
            'field_label' => 'Pickup Date',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
                )
            )
        ),
        array(
            'element_id' => 'time-3',
            'type' => 'time',
            'field_label' => 'Pickup Time',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
                )
            )
        )
    )
);

// Duration (chauffeur only)
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'select-2',
            'type' => 'select',
            'field_label' => 'Ride Duration',
            'required' => 'true',
            'description' => 'Minimum rental duration is 3+1 hours',
            'options' => array(
                array('label' => '-- Select duration --', 'value' => ''),
                array('label' => '3 hours (3+1)', 'value' => '3'),
                array('label' => '4 hours (4+1)', 'value' => '4'),
                array('label' => '5 hours (5+1)', 'value' => '5'),
                array('label' => '6 hours (6+1)', 'value' => '6'),
                array('label' => '7 hours (7+1)', 'value' => '7'),
                array('label' => '8 hours (8+1)', 'value' => '8'),
                array('label' => '9 hours (9+1)', 'value' => '9'),
                array('label' => '10 hours (10+1)', 'value' => '10'),
                array('label' => '11 hours (11+1)', 'value' => '11'),
                array('label' => '12 hours (12+1)', 'value' => '12')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly'),
                    array('element_id' => 'radio-3', 'rule' => 'is', 'value' => 'chauffeur')
                )
            )
        )
    )
);

// Hourly addresses
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-7',
            'type' => 'text',
            'field_label' => 'Pickup Address',
            'required' => 'true',
            'placeholder' => 'Enter Pickup Address',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-8',
            'type' => 'text',
            'field_label' => 'Drop-off Address',
            'required' => 'true',
            'placeholder' => 'Final Destination Address',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
                )
            )
        )
    )
);

// Hourly Special Requirements
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-11',
            'type' => 'checkbox',
            'field_label' => 'Special Requirements (optional)',
            'options' => array(
                array('label' => 'Wheelchair accessible', 'value' => 'wheelchair'),
                array('label' => 'Child safety seats', 'value' => 'child-seats'),
                array('label' => 'Hostess / Additional Staff', 'value' => 'hostess'),
                array('label' => 'On-site coordinator', 'value' => 'coordinator'),
                array('label' => 'English-speaking driver', 'value' => 'english-driver'),
                array('label' => 'Security / Protocol', 'value' => 'security')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'hourly')
                )
            )
        )
    )
);

// ============================================
// MULTI-DAY TRIPS SECTION
// ============================================
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-5',
            'type' => 'html',
            'variations' => '<h2 class="vb-form-title">Multi-day Trip Details</h2><p class="vb-form-subtitle">Plan your private tour or extended trip</p>',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'date-4',
            'type' => 'date',
            'field_label' => 'Start Date',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
                )
            )
        ),
        array(
            'element_id' => 'time-4',
            'type' => 'time',
            'field_label' => 'Pickup Time',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
                )
            )
        ),
        array(
            'element_id' => 'number-12',
            'type' => 'number',
            'field_label' => 'Total Days',
            'required' => 'true',
            'limit_min' => '2',
            'limit_max' => '30',
            'description' => 'Minimum 2 days for multi-day trips',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-9',
            'type' => 'text',
            'field_label' => 'Pickup Address',
            'required' => 'true',
            'placeholder' => 'e.g., Hotel in Budapest',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'textarea-3',
            'type' => 'textarea',
            'field_label' => 'Trip Itinerary / Details',
            'required' => 'true',
            'placeholder' => 'Describe your trip, e.g.:

Day 1: Budapest - Eger (wine tasting) - overnight in Eger
Day 2: Eger - Tokaj wine region - return to Budapest
Day 3: Budapest sightseeing - Airport transfer',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
                )
            )
        )
    )
);

// Multi-day Special Requirements
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-12',
            'type' => 'checkbox',
            'field_label' => 'Special Requirements (optional)',
            'options' => array(
                array('label' => 'Wheelchair accessible', 'value' => 'wheelchair'),
                array('label' => 'Child safety seats', 'value' => 'child-seats'),
                array('label' => 'Hostess / Additional Staff', 'value' => 'hostess'),
                array('label' => 'On-site coordinator', 'value' => 'coordinator'),
                array('label' => 'English-speaking driver', 'value' => 'english-driver'),
                array('label' => 'Security / Protocol', 'value' => 'security')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'countryside')
                )
            )
        )
    )
);

// ============================================
// F1 GRAND PRIX SECTION
// ============================================
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-6',
            'type' => 'html',
            'variations' => '<h2 class="vb-form-title">F1 Grand Prix Transfers</h2><p class="vb-form-subtitle">July 23-26, 2026 - Hungaroring</p>',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'f1')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-13',
            'type' => 'checkbox',
            'field_label' => 'Select the days you need transportation',
            'required' => 'true',
            'options' => array(
                array('label' => 'Thursday, July 23, 2026', 'value' => 'thu'),
                array('label' => 'Friday, July 24, 2026', 'value' => 'fri'),
                array('label' => 'Saturday, July 25, 2026', 'value' => 'sat'),
                array('label' => 'Sunday, July 26, 2026', 'value' => 'sun')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'f1')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-10',
            'type' => 'text',
            'field_label' => 'Pickup Address',
            'required' => 'true',
            'placeholder' => 'e.g., Hilton Budapest',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'f1')
                )
            )
        ),
        array(
            'element_id' => 'text-11',
            'type' => 'text',
            'field_label' => 'Final Drop-off Address',
            'required' => 'true',
            'placeholder' => 'e.g., Same as pickup, or Airport',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'f1')
                )
            )
        )
    )
);

// F1 Special Requirements
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-14',
            'type' => 'checkbox',
            'field_label' => 'Special Requirements (optional)',
            'options' => array(
                array('label' => 'Wheelchair accessible', 'value' => 'wheelchair'),
                array('label' => 'Child safety seats', 'value' => 'child-seats'),
                array('label' => 'Hostess / Additional Staff', 'value' => 'hostess'),
                array('label' => 'On-site coordinator', 'value' => 'coordinator'),
                array('label' => 'English-speaking driver', 'value' => 'english-driver'),
                array('label' => 'Security / Protocol', 'value' => 'security')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'f1')
                )
            )
        )
    )
);

// ============================================
// UEFA SECTION
// ============================================
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-7',
            'type' => 'html',
            'variations' => '<h2 class="vb-form-title">UEFA Champions League Final</h2><p class="vb-form-subtitle">May 28-31, 2026 - Puskas Arena, Budapest</p>',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'uefa')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-15',
            'type' => 'checkbox',
            'field_label' => 'Select the days you need transportation',
            'required' => 'true',
            'options' => array(
                array('label' => 'Thursday, May 28, 2026 (min. 6 hours)', 'value' => 'thu'),
                array('label' => 'Friday, May 29, 2026 (min. 6 hours)', 'value' => 'fri'),
                array('label' => 'Saturday, May 30, 2026 (MATCH DAY - min. 12 hours)', 'value' => 'sat'),
                array('label' => 'Sunday, May 31, 2026 (min. 6 hours)', 'value' => 'sun')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'uefa')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-12',
            'type' => 'text',
            'field_label' => 'Pickup Address',
            'required' => 'true',
            'placeholder' => 'e.g., Corinthia Hotel Budapest',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'uefa')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'textarea-4',
            'type' => 'textarea',
            'field_label' => 'Destination & Route / Stops',
            'required' => 'true',
            'placeholder' => 'e.g., Corinthia Hotel - Puskas Arena - City Park - Return to hotel',
            'description' => 'Enter the planned route with stops (in order)',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'uefa')
                )
            )
        )
    )
);

// UEFA Special Requirements
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-16',
            'type' => 'checkbox',
            'field_label' => 'Special Requirements (optional)',
            'options' => array(
                array('label' => 'Wheelchair accessible', 'value' => 'wheelchair'),
                array('label' => 'Child safety seats', 'value' => 'child-seats'),
                array('label' => 'Hostess / Additional Staff', 'value' => 'hostess'),
                array('label' => 'On-site coordinator', 'value' => 'coordinator'),
                array('label' => 'English-speaking driver', 'value' => 'english-driver'),
                array('label' => 'Security / Protocol', 'value' => 'security')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'uefa')
                )
            )
        )
    )
);

// ============================================
// EVENT TRANSPORTATION SECTION
// ============================================
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-8',
            'type' => 'html',
            'variations' => '<h2 class="vb-form-title">Event Transportation - Request a Proposal</h2><p class="vb-form-subtitle">Tell us about your event and transportation needs</p>',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-13',
            'type' => 'text',
            'field_label' => 'Event Name',
            'required' => 'true',
            'placeholder' => 'e.g., Budapest Tech Summit 2026',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        ),
        array(
            'element_id' => 'text-14',
            'type' => 'text',
            'field_label' => 'Organization Name',
            'required' => 'true',
            'placeholder' => 'Company or organization name',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'select-3',
            'type' => 'select',
            'field_label' => 'Event Type',
            'required' => 'true',
            'options' => array(
                array('label' => '-- Select event type --', 'value' => ''),
                array('label' => 'Conference / Summit', 'value' => 'conference'),
                array('label' => 'Corporate Meeting / Incentive', 'value' => 'corporate'),
                array('label' => 'Wedding / Private Celebration', 'value' => 'wedding'),
                array('label' => 'Gala / Award Ceremony', 'value' => 'gala'),
                array('label' => 'Sports Event', 'value' => 'sports'),
                array('label' => 'Film / TV Production', 'value' => 'film'),
                array('label' => 'Diplomatic / Government', 'value' => 'diplomatic'),
                array('label' => 'Other', 'value' => 'other')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        ),
        array(
            'element_id' => 'number-13',
            'type' => 'number',
            'field_label' => 'Expected Guests',
            'required' => 'true',
            'placeholder' => 'Enter number of guests',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'date-5',
            'type' => 'date',
            'field_label' => 'Event Start Date',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        ),
        array(
            'element_id' => 'date-6',
            'type' => 'date',
            'field_label' => 'Event End Date',
            'required' => 'true',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-15',
            'type' => 'text',
            'field_label' => 'Event City',
            'required' => 'true',
            'placeholder' => 'e.g., Budapest',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        ),
        array(
            'element_id' => 'text-16',
            'type' => 'text',
            'field_label' => 'Event Venue / Location',
            'required' => 'true',
            'placeholder' => 'e.g., Hilton Budapest, Buda Castle',
            'description' => 'Main event location (hotel, conference center, etc.)',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-17',
            'type' => 'checkbox',
            'field_label' => 'Services Needed',
            'required' => 'true',
            'options' => array(
                array('label' => 'Airport transfers', 'value' => 'airport'),
                array('label' => 'Hotel - Venue shuttle', 'value' => 'shuttle'),
                array('label' => 'Hourly VIP / Chauffeur', 'value' => 'hourly-vip'),
                array('label' => 'Multi-day program', 'value' => 'multi-day'),
                array('label' => 'Staff / Crew transport', 'value' => 'staff'),
                array('label' => 'Other (specify below)', 'value' => 'other')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'textarea-5',
            'type' => 'textarea',
            'field_label' => 'Schedule / Key Moves (recommended)',
            'placeholder' => 'Example:
- May 15, 10:00 - Airport to Hilton Budapest - 25 guests
- May 15, 18:00 - Hilton to Buda Castle - 25 guests
- May 17, 14:00 - Hilton to Airport - 25 guests',
            'description' => 'For accurate pricing, please share at least your top 3 key moves',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        )
    )
);

// Event Special Requirements
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-18',
            'type' => 'checkbox',
            'field_label' => 'Special Requirements (optional)',
            'options' => array(
                array('label' => 'Wheelchair accessible', 'value' => 'wheelchair'),
                array('label' => 'Child safety seats', 'value' => 'child-seats'),
                array('label' => 'Hostess / Additional Staff', 'value' => 'hostess'),
                array('label' => 'On-site coordinator', 'value' => 'coordinator'),
                array('label' => 'English-speaking driver', 'value' => 'english-driver'),
                array('label' => 'Security / Protocol', 'value' => 'security')
            ),
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'radio-1', 'rule' => 'is', 'value' => 'event')
                )
            )
        )
    )
);

// ============================================
// STEP 4: CONTACT & BILLING
// ============================================
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'page-break-4',
            'type' => 'page-break',
            'field_label' => 'Contact & Billing'
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-9',
            'type' => 'html',
            'variations' => '<h2 class="vb-form-title">Contact & Billing</h2><p class="vb-form-subtitle">Review your services and provide contact details</p>'
        )
    )
);

// Contact Details
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'select-4',
            'type' => 'select',
            'field_label' => 'Title',
            'options' => array(
                array('label' => '--', 'value' => ''),
                array('label' => 'Mr', 'value' => 'mr'),
                array('label' => 'Mrs', 'value' => 'mrs'),
                array('label' => 'Ms', 'value' => 'ms'),
                array('label' => 'Miss', 'value' => 'miss'),
                array('label' => 'Dr', 'value' => 'dr')
            )
        ),
        array(
            'element_id' => 'name-1',
            'type' => 'name',
            'field_label' => 'Your Name',
            'required' => 'true',
            'fname' => true,
            'fname_label' => 'First Name',
            'lname' => true,
            'lname_label' => 'Last Name'
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'email-1',
            'type' => 'email',
            'field_label' => 'Email',
            'required' => 'true',
            'placeholder' => 'email@example.com'
        ),
        array(
            'element_id' => 'phone-1',
            'type' => 'phone',
            'field_label' => 'Phone',
            'required' => 'true',
            'placeholder' => '+36 70 XXX XXXX'
        )
    )
);

// Booking for someone else
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-20',
            'type' => 'checkbox',
            'field_label' => '',
            'options' => array(
                array('label' => 'I am booking for someone else (e.g., guest, colleague, or client)', 'value' => 'yes')
            )
        )
    )
);

// Client details (conditional)
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'name-2',
            'type' => 'name',
            'field_label' => 'Passenger Name',
            'required' => 'true',
            'fname' => true,
            'fname_label' => 'First Name',
            'lname' => true,
            'lname_label' => 'Last Name',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'checkbox-20', 'rule' => 'is', 'value' => 'yes')
                )
            )
        ),
        array(
            'element_id' => 'phone-2',
            'type' => 'phone',
            'field_label' => 'Passenger Mobile',
            'required' => 'true',
            'placeholder' => '+36 70 XXX XXXX',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'checkbox-20', 'rule' => 'is', 'value' => 'yes')
                )
            )
        )
    )
);

// Custom signage
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-21',
            'type' => 'checkbox',
            'field_label' => '',
            'options' => array(
                array('label' => 'Use alternative text on the sign (for airport meet and greet service)', 'value' => 'yes')
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-20',
            'type' => 'text',
            'field_label' => 'Text on sign',
            'required' => 'true',
            'placeholder' => 'e.g., Company Name or Group Name',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'checkbox-21', 'rule' => 'is', 'value' => 'yes')
                )
            )
        )
    )
);

// Billing toggle
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'checkbox-22',
            'type' => 'checkbox',
            'field_label' => '',
            'options' => array(
                array('label' => 'I need an invoice with specific billing details', 'value' => 'yes')
            )
        )
    )
);

// Billing details (conditional)
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-21',
            'type' => 'text',
            'field_label' => 'Name or Company Name',
            'required' => 'true',
            'placeholder' => 'e.g., John Doe or ABC Company Ltd.',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'checkbox-22', 'rule' => 'is', 'value' => 'yes')
                )
            )
        ),
        array(
            'element_id' => 'text-22',
            'type' => 'text',
            'field_label' => 'Billing Address',
            'required' => 'true',
            'placeholder' => 'Street, City, Postal Code, Country',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'checkbox-22', 'rule' => 'is', 'value' => 'yes')
                )
            )
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'text-23',
            'type' => 'text',
            'field_label' => 'VAT / Tax Number',
            'placeholder' => 'e.g., HU12345678',
            'conditions' => array(
                'action' => 'show',
                'rule' => 'all',
                'conditions' => array(
                    array('element_id' => 'checkbox-22', 'rule' => 'is', 'value' => 'yes')
                )
            )
        )
    )
);

// How did you hear about us
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'select-5',
            'type' => 'select',
            'field_label' => 'How did you hear about us?',
            'options' => array(
                array('label' => '-- Select --', 'value' => ''),
                array('label' => 'Google Search', 'value' => 'google'),
                array('label' => 'Social Media', 'value' => 'social'),
                array('label' => 'Recommendation', 'value' => 'recommendation'),
                array('label' => 'Travel Agency / DMC', 'value' => 'travel-agency'),
                array('label' => 'Returning Customer', 'value' => 'returning'),
                array('label' => 'Hotel Concierge', 'value' => 'hotel'),
                array('label' => 'Other', 'value' => 'other')
            )
        ),
        array(
            'element_id' => 'text-24',
            'type' => 'text',
            'field_label' => 'Promo Code (optional)',
            'placeholder' => 'Enter promo code if you have one'
        )
    )
);

// Payment method
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'html-10',
            'type' => 'html',
            'variations' => '<p class="vb-help-text">For credit card payments, a minimal processing fee applies. Any applicable fees will be included in the quote.</p>'
        )
    )
);

$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'radio-10',
            'type' => 'radio',
            'field_label' => 'Preferred Payment Method',
            'required' => 'true',
            'options' => array(
                array('label' => 'Bank Transfer — No additional fees', 'value' => 'bank_transfer', 'default' => true),
                array('label' => 'Credit Card — +3% processing fee', 'value' => 'credit_card')
            )
        )
    )
);

// Terms & Conditions
$wrappers[] = array(
    'wrapper_id' => generate_wrapper_id(),
    'fields' => array(
        array(
            'element_id' => 'consent-1',
            'type' => 'consent',
            'field_label' => 'Terms & Conditions',
            'required' => 'true',
            'consent_description' => 'I accept the <a href="/terms" target="_blank">Terms & Conditions</a> and <a href="/privacy" target="_blank">Privacy Policy</a>',
            'required_message' => 'You must accept the Terms & Conditions to proceed.'
        )
    )
);

// ============================================
// CREATE THE FORM
// ============================================
try {
    $form_id = Forminator_API::add_form('VanBudapest Booking Form v2', $wrappers, $settings);

    if (is_wp_error($form_id)) {
        echo "ERROR: " . $form_id->get_error_message();
    } else {
        echo "SUCCESS! Form created with ID: " . $form_id . "\n\n";
        echo "You can now find your form in Forminator -> Forms\n";
        echo "Shortcode: [forminator_form id=\"" . $form_id . "\"]\n\n";
        echo "IMPORTANT: Delete this file now for security!\n";
    }
} catch (Exception $e) {
    echo "ERROR: " . $e->getMessage();
}

echo "</pre>";
?>
