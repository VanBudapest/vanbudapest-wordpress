# VanBudapest Booking Form v2 - TELJES IMPLEMENTÁCIÓS ÚTMUTATÓ

> **Forrás:** HTML Prototípus v55 (2 napig tesztelt TESZT-PILOT űrlap)
> **Cél:** Új Forminator űrlap létrehozása "szó szerint" a prototípus alapján
> **Dátum:** 2026-01-31

---

## 📋 TARTALOM

1. [Űrlap alapbeállítások](#1-űrlap-alapbeállítások)
2. [STEP 1: Service Selection](#2-step-1-service-selection)
3. [STEP 2: Vehicle & Group Details](#3-step-2-vehicle--group-details)
4. [STEP 3: Service Details](#4-step-3-service-details)
   - [3A: Airport & Long-Distance Transfer](#step-3a-airport--long-distance-transfer)
   - [3B: Hourly Ride & Sightseeing](#step-3b-hourly-ride--sightseeing)
   - [3C: Multi-day Trips](#step-3c-multi-day-trips)
   - [3D: F1 Grand Prix](#step-3d-f1-grand-prix)
   - [3E: UEFA Champions League Final](#step-3e-uefa-champions-league-final)
   - [3F: Event Transportation](#step-3f-event-transportation)
5. [STEP 4: Contact & Billing](#5-step-4-contact--billing)
6. [Kondíciók összefoglaló](#6-kondíciók-összefoglaló)
7. [CSS kód](#7-css-kód)
8. [Email sablon](#8-email-sablon)

---

## 1. ŰRLAP ALAPBEÁLLÍTÁSOK

### Új űrlap létrehozása
1. WordPress Admin → Forminator → Forms → Create
2. **Form Name:** `VanBudapest Booking Form v2`
3. **Form Type:** Custom Form

### Pagination beállítások
- **Pagination Type:** Wizard (multi-step)
- **Progress Bar:** Navigation with Steps
- **Total Steps:** 4

### Step Labels (sorrendben):
| Step | Label |
|------|-------|
| 1 | Service Selection |
| 2 | Vehicle & Group |
| 3 | Service Details |
| 4 | Contact & Billing |

### Button Labels:
| Step | Back Button | Next Button |
|------|-------------|-------------|
| 1 | (nincs) | Next: Vehicle & Group → |
| 2 | ← Back | Next: Service Details → |
| 3 | ← Back | Next: Contact Details → |
| 4 | ← Back | Request a Quote → |

---

## 2. STEP 1: SERVICE SELECTION

### Page Break #1
- **Label:** Service Selection

### Section: Service Selection Header
```
ID: section-service-header
Title: (üres - CSS-sel formázott)
```

### HTML Field: Page Title
```html
<h2 class="vb-form-title">How can we help you today?</h2>
<p class="vb-form-subtitle">Select the service that best fits your needs</p>
```

---

### Field: select-service
| Property | Value |
|----------|-------|
| **Field ID** | `select-service` |
| **Type** | Radio |
| **Label** | Select the service that best fits your needs |
| **Required** | ✅ Yes |
| **Layout** | Grid (3 columns) |

**Options (PONTOS SORREND):**
```
✈️ Transfers (Airport & Long-Distance) — One-way or return, any distance;airport
⏰ Hourly Ride & Sightseeing — Chauffeur service or guided tours;hourly
🗺️ Multi-day Trips — Private tours & trips;countryside
🎪 Event Transportation — Conferences & groups;event
⚽ UEFA CL Final — May 28-31, 2026;uefa
🏎️ F1 Grand Prix — July 23-26, 2026;f1
```

> **MEGJEGYZÉS:** A Forminator-ban radio button lesz, CSS-sel card-szerűvé alakítjuk.

---

## 3. STEP 2: VEHICLE & GROUP DETAILS

### Page Break #2
- **Label:** Vehicle & Group

### Section: Vehicle & Group Header
```
ID: section-vehicle-header
```

### HTML Field: Page Title
```html
<h2 class="vb-form-title">Vehicle & Group Details</h2>
<p class="vb-form-subtitle">Select your preferred vehicle(s) and group size</p>
```

---

### Section: Vehicle Selection
```
ID: section-vehicle-selection
Title: Vehicle Selection
```

### HTML Field: Vehicle Help Text
```html
<p class="vb-help-text">Select one or more vehicles. For mixed groups, choose multiple vehicle types.</p>
```

---

### VEHICLE CHECKBOXOK (6 db)

#### Field: vehicle-business-car
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-business-car` |
| **Type** | Checkbox (single) |
| **Label** | 🚗 Business Car – up to 3 pax – Mercedes E-Class |
| **Required** | ❌ No |

#### Field: vehicle-business-car-qty
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-business-car-qty` |
| **Type** | Number |
| **Label** | Qty |
| **Default** | 1 |
| **Min** | 1 |
| **Max** | 20 |
| **Condition** | `vehicle-business-car` is checked |

---

#### Field: vehicle-premium-van
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-premium-van` |
| **Type** | Checkbox (single) |
| **Label** | 🚐 Premium VAN – up to 6-7 pax – Mercedes V-Class |
| **Required** | ❌ No |

#### Field: vehicle-premium-van-qty
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-premium-van-qty` |
| **Type** | Number |
| **Label** | Qty |
| **Default** | 1 |
| **Min** | 1 |
| **Max** | 20 |
| **Condition** | `vehicle-premium-van` is checked |

---

#### Field: vehicle-minibus
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-minibus` |
| **Type** | Checkbox (single) |
| **Label** | 🚌 Minibus – up to 14-20 pax – Mercedes Sprinter |
| **Required** | ❌ No |

#### Field: vehicle-minibus-qty
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-minibus-qty` |
| **Type** | Number |
| **Label** | Qty |
| **Default** | 1 |
| **Min** | 1 |
| **Max** | 20 |
| **Condition** | `vehicle-minibus` is checked |

---

#### Field: vehicle-coach
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-coach` |
| **Type** | Checkbox (single) |
| **Label** | 🚍 Coach Bus – up to 49 pax – Mercedes Tourismo |
| **Required** | ❌ No |

#### Field: vehicle-coach-qty
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-coach-qty` |
| **Type** | Number |
| **Label** | Qty |
| **Default** | 1 |
| **Min** | 1 |
| **Max** | 10 |
| **Condition** | `vehicle-coach` is checked |

---

#### Field: vehicle-luxury-minibus (VIP)
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-luxury-minibus` |
| **Type** | Checkbox (single) |
| **Label** | 🚐 Luxury Minibus VIP – up to 8 pax – Mercedes Sprinter |
| **Required** | ❌ No |
| **CSS Class** | `vip-vehicle` |

#### Field: vehicle-luxury-minibus-qty
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-luxury-minibus-qty` |
| **Type** | Number |
| **Label** | Qty |
| **Default** | 1 |
| **Min** | 1 |
| **Max** | 10 |
| **Condition** | `vehicle-luxury-minibus` is checked |

---

#### Field: vehicle-luxury-car (VIP)
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-luxury-car` |
| **Type** | Checkbox (single) |
| **Label** | 👔 Luxury Car VIP – up to 3 pax – Mercedes S-Class |
| **Required** | ❌ No |
| **CSS Class** | `vip-vehicle` |

#### Field: vehicle-luxury-car-qty
| Property | Value |
|----------|-------|
| **Field ID** | `vehicle-luxury-car-qty` |
| **Type** | Number |
| **Label** | Qty |
| **Default** | 1 |
| **Min** | 1 |
| **Max** | 10 |
| **Condition** | `vehicle-luxury-car` is checked |

---

### Section: Group Details
```
ID: section-group-details
Title: Group Details
```

#### Field: total-guests
| Property | Value |
|----------|-------|
| **Field ID** | `total-guests` |
| **Type** | Number |
| **Label** | Total Number of Guests |
| **Required** | ✅ Yes |
| **Default** | 1 |
| **Min** | 1 |
| **Max** | 500 |

#### Field: total-luggage
| Property | Value |
|----------|-------|
| **Field ID** | `total-luggage` |
| **Type** | Number |
| **Label** | Pieces of Luggage |
| **Required** | ❌ No |
| **Default** | 0 |
| **Min** | 0 |
| **Max** | 100 |

#### Field: special-items
| Property | Value |
|----------|-------|
| **Field ID** | `special-items` |
| **Type** | Text |
| **Label** | Special Items / Notes |
| **Required** | ❌ No |
| **Placeholder** | e.g., Golf bags, Ski equipment, Wheelchair, Child seats |

---

## 4. STEP 3: SERVICE DETAILS

### Page Break #3
- **Label:** Service Details

> **FONTOS:** A Step 3 tartalma KONDICIONÁLIS - minden service type-nak saját mezői vannak!

---

## STEP 3A: AIRPORT & LONG-DISTANCE TRANSFER

**Master Condition:** `select-service` = `airport`

### Section: Airport Header
```
ID: section-airport
Title: (HTML-ből)
Condition: select-service = airport
```

### HTML Field: Airport Title
```html
<h2 class="vb-form-title">Transfer Details</h2>
<p class="vb-form-subtitle">One-way or return transfers, any distance</p>
```
**Condition:** `select-service` = `airport`

---

### Section: Transfer Information
```
ID: section-transfer-info
Title: Transfer Information
Condition: select-service = airport
```

#### Field: airport-pickup-date
| Property | Value |
|----------|-------|
| **Field ID** | `airport-pickup-date` |
| **Type** | Date |
| **Label** | Pickup Date |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `airport` |

#### Field: airport-pickup-time
| Property | Value |
|----------|-------|
| **Field ID** | `airport-pickup-time` |
| **Type** | Time |
| **Label** | Pickup Time |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `airport` |

#### Field: airport-pickup-address
| Property | Value |
|----------|-------|
| **Field ID** | `airport-pickup-address` |
| **Type** | Text |
| **Label** | Pickup Address |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Budapest Airport Terminal 2B, Hotel name, or any address |
| **Condition** | `select-service` = `airport` |

#### Field: airport-dropoff-address
| Property | Value |
|----------|-------|
| **Field ID** | `airport-dropoff-address` |
| **Type** | Text |
| **Label** | Drop-off Address |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Hilton Budapest, Airport, or any destination |
| **Condition** | `select-service` = `airport` |

#### Field: airport-flight-number
| Property | Value |
|----------|-------|
| **Field ID** | `airport-flight-number` |
| **Type** | Text |
| **Label** | Flight Number (if airport transfer) |
| **Required** | ❌ No |
| **Placeholder** | e.g., FR1023 |
| **Description** | Optional – for airport pickups, we monitor your flight for delays |
| **Condition** | `select-service` = `airport` |

---

#### Field: airport-return-transfer
| Property | Value |
|----------|-------|
| **Field ID** | `airport-return-transfer` |
| **Type** | Radio |
| **Label** | Do you require a return transfer? |
| **Required** | ✅ Yes |
| **Default** | no |
| **Condition** | `select-service` = `airport` |

**Options:**
```
Yes;yes
No;no
```

---

### RETURN TRANSFER FIELDS (Conditional)

**Condition:** `airport-return-transfer` = `yes`

#### Field: airport-return-date
| Property | Value |
|----------|-------|
| **Field ID** | `airport-return-date` |
| **Type** | Date |
| **Label** | Return Date |
| **Required** | ✅ Yes (when visible) |
| **Condition** | `airport-return-transfer` = `yes` |

#### Field: airport-return-time
| Property | Value |
|----------|-------|
| **Field ID** | `airport-return-time` |
| **Type** | Time |
| **Label** | Return Time |
| **Required** | ✅ Yes (when visible) |
| **Condition** | `airport-return-transfer` = `yes` |

#### Field: airport-return-pickup
| Property | Value |
|----------|-------|
| **Field ID** | `airport-return-pickup` |
| **Type** | Text |
| **Label** | Return Pickup Address |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | e.g., Hotel address for return journey |
| **Condition** | `airport-return-transfer` = `yes` |

#### Field: airport-return-dropoff
| Property | Value |
|----------|-------|
| **Field ID** | `airport-return-dropoff` |
| **Type** | Text |
| **Label** | Return Drop-off Address |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | e.g., Budapest Airport Terminal 2B |
| **Condition** | `airport-return-transfer` = `yes` |

---

### Section: Airport Special Requirements
```
ID: section-airport-special
Title: Special Requirements (optional)
Condition: select-service = airport
```

#### Field: airport-special-requirements
| Property | Value |
|----------|-------|
| **Field ID** | `airport-special-requirements` |
| **Type** | Checkbox (multiple) |
| **Label** | (hidden - checkboxes speak for themselves) |
| **Required** | ❌ No |
| **Condition** | `select-service` = `airport` |

**Options:**
```
♿ Wheelchair accessible;wheelchair
👶 Child safety seats;child-seats
🎀 Hostess / Additional Staff;hostess
👤 On-site coordinator;coordinator
🗣️ English-speaking driver;english-driver
🔒 Security / Protocol;security
```

#### Field: airport-additional-preferences
| Property | Value |
|----------|-------|
| **Field ID** | `airport-additional-preferences` |
| **Type** | Textarea |
| **Label** | Additional Preferences (optional) |
| **Required** | ❌ No |
| **Placeholder** | Any other requests or preferences... |
| **Rows** | 2 |
| **Condition** | `select-service` = `airport` |

---

## STEP 3B: HOURLY RIDE & SIGHTSEEING

**Master Condition:** `select-service` = `hourly`

### Section: Hourly Header
```
ID: section-hourly
Condition: select-service = hourly
```

### HTML Field: Hourly Title
```html
<h2 class="vb-form-title">Hourly Ride & Sightseeing</h2>
<p class="vb-form-subtitle">Chauffeur service or private guided tour in Budapest</p>
```
**Condition:** `select-service` = `hourly`

---

### Section: Service Type Selection
```
ID: section-hourly-type
Title: What type of service do you need?
Condition: select-service = hourly
```

#### Field: hourly-service-type
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-service-type` |
| **Type** | Radio |
| **Label** | (hidden - included in options) |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `hourly` |

**Options (Rich formatting - use HTML in label):**
```
<strong>Chauffeur Service</strong> <span style="color:#666;">(driver only)</span><p style="margin:4px 0 0; font-size:13px; color:#666;">You direct the route – perfect for business, shopping, or custom itineraries</p>;chauffeur
<strong>Private Sightseeing Tour</strong> <span style="color:#C8B560;">(driver + licensed guide)</span><p style="margin:4px 0 0; font-size:13px; color:#666;">Expert guide plans the tour – history, culture, local insights included</p>;sightseeing
```

---

### SIGHTSEEING FIELDS (Conditional)

**Condition:** `hourly-service-type` = `sightseeing`

### Section: Tour Guide Options
```
ID: section-guide-options
Title: Tour Guide Options
Condition: hourly-service-type = sightseeing
```

#### Field: guide-language
| Property | Value |
|----------|-------|
| **Field ID** | `guide-language` |
| **Type** | Select |
| **Label** | Guide Language |
| **Required** | ✅ Yes (when visible) |
| **Condition** | `hourly-service-type` = `sightseeing` |

**Options:**
```
-- Select language --;
English;english
German (Deutsch);german
Spanish (Español);spanish
French (Français);french
Italian (Italiano);italian
Russian (Русский);russian
Chinese (中文);chinese
Polish (Polski);polish
```

---

#### Field: tour-package
| Property | Value |
|----------|-------|
| **Field ID** | `tour-package` |
| **Type** | Radio |
| **Label** | Tour Package |
| **Required** | ✅ Yes (when visible) |
| **Condition** | `hourly-service-type` = `sightseeing` |

**Options (6 túra - "Budapest Classic" = MOST POPULAR):**
```
<strong>Castle District Focus</strong> <span style="color:#666; font-size:13px;">(3-4 hours)</span><p style="margin:2px 0 0; font-size:13px; color:#666;">Buda Castle, Fisherman's Bastion, Matthias Church, Gellért Hill</p>;castle
<strong>Pest Highlights</strong> <span style="color:#666; font-size:13px;">(3-4 hours)</span><p style="margin:2px 0 0; font-size:13px; color:#666;">Downtown, Basilica, Parliament, Andrássy Avenue, Heroes' Square</p>;pest
<strong>Budapest Classic</strong> <span style="color:#666; font-size:13px;">(4-5 hours)</span> ★ MOST POPULAR<p style="margin:2px 0 0; font-size:13px; color:#666;">Best of both Buda & Pest sides — the complete introduction</p>;classic
<strong>Grand Budapest Tour</strong> <span style="color:#666; font-size:13px;">(6+ hours)</span><p style="margin:2px 0 0; font-size:13px; color:#666;">Full-day comprehensive tour with hidden gems & local favorites</p>;grand
<strong>Jewish Heritage</strong> <span style="color:#666; font-size:13px;">(3-4 hours)</span><p style="margin:2px 0 0; font-size:13px; color:#666;">Jewish Quarter, Great Synagogue, memorials & historic sites</p>;jewish
<strong>Custom Tour</strong><p style="margin:2px 0 0; font-size:13px; color:#666;">I have specific preferences or interests</p>;custom
```

---

#### Field: custom-tour-requests
| Property | Value |
|----------|-------|
| **Field ID** | `custom-tour-requests` |
| **Type** | Textarea |
| **Label** | Special Requests |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | Tell us about your interests, must-see places, or any special requirements... |
| **Condition** | `tour-package` = `custom` |

---

### RIDE DETAILS (Both Chauffeur & Sightseeing)

**Condition:** `select-service` = `hourly`

### Section: Ride Details
```
ID: section-hourly-ride
Title: Ride Details
Condition: select-service = hourly
```

#### Field: hourly-pickup-date
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-pickup-date` |
| **Type** | Date |
| **Label** | Pickup Date |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `hourly` |

#### Field: hourly-pickup-time
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-pickup-time` |
| **Type** | Time |
| **Label** | Pickup Time |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `hourly` |

---

### CHAUFFEUR-ONLY FIELDS

**Condition:** `hourly-service-type` = `chauffeur`

### HTML Field: Duration Help Text
```html
<p class="vb-help-text">Minimum rental duration is 3+1 hours.</p>
```
**Condition:** `hourly-service-type` = `chauffeur`

#### Field: hourly-duration
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-duration` |
| **Type** | Select |
| **Label** | Ride Duration |
| **Required** | ✅ Yes (when visible) |
| **Condition** | `hourly-service-type` = `chauffeur` |

**Options:**
```
-- Select duration --;
3 hours (3+1);3
4 hours (4+1);4
5 hours (5+1);5
6 hours (6+1);6
7 hours (7+1);7
8 hours (8+1);8
9 hours (9+1);9
10 hours (10+1);10
11 hours (11+1);11
12 hours (12+1);12
```

---

#### Field: hourly-pickup-address
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-pickup-address` |
| **Type** | Text |
| **Label** | Pickup Address |
| **Required** | ✅ Yes |
| **Placeholder** | Enter Pickup Address |
| **Condition** | `select-service` = `hourly` |

#### Field: hourly-destination (Chauffeur only)
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-destination` |
| **Type** | Text |
| **Label** | Destination Address |
| **Required** | ❌ No |
| **Condition** | `hourly-service-type` = `chauffeur` |

#### Field: hourly-route-stops (Chauffeur only)
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-route-stops` |
| **Type** | Textarea |
| **Label** | Route & Stops |
| **Required** | ❌ No |
| **Placeholder** | Any optional stops along the route |
| **Condition** | `hourly-service-type` = `chauffeur` |

#### Field: hourly-dropoff-address
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-dropoff-address` |
| **Type** | Text |
| **Label** | Drop-off Address |
| **Required** | ✅ Yes |
| **Placeholder** | Final Destination Address |
| **Condition** | `select-service` = `hourly` |

---

### Section: Hourly Special Requirements
```
ID: section-hourly-special
Title: Special Requirements (optional)
Condition: select-service = hourly
```

#### Field: hourly-special-requirements
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-special-requirements` |
| **Type** | Checkbox (multiple) |
| **Required** | ❌ No |
| **Condition** | `select-service` = `hourly` |

**Options:**
```
♿ Wheelchair accessible;wheelchair
👶 Child safety seats;child-seats
🎀 Hostess / Additional Staff;hostess
👤 On-site coordinator;coordinator
🗣️ English-speaking driver;english-driver
🔒 Security / Protocol;security
```

#### Field: hourly-additional-preferences
| Property | Value |
|----------|-------|
| **Field ID** | `hourly-additional-preferences` |
| **Type** | Textarea |
| **Label** | Additional Preferences (optional) |
| **Required** | ❌ No |
| **Placeholder** | Any other requests or preferences... |
| **Rows** | 2 |
| **Condition** | `select-service` = `hourly` |

---

## STEP 3C: MULTI-DAY TRIPS

**Master Condition:** `select-service` = `countryside`

### Section: Multi-day Header
```
ID: section-countryside
Condition: select-service = countryside
```

### HTML Field: Multi-day Title
```html
<h2 class="vb-form-title">Multi-day Trip Details</h2>
<p class="vb-form-subtitle">Plan your private tour or extended trip</p>
```
**Condition:** `select-service` = `countryside`

---

### Section: Trip Information
```
ID: section-trip-info
Title: Trip Information
Condition: select-service = countryside
```

#### Field: countryside-start-date
| Property | Value |
|----------|-------|
| **Field ID** | `countryside-start-date` |
| **Type** | Date |
| **Label** | Start Date |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `countryside` |

#### Field: countryside-pickup-time
| Property | Value |
|----------|-------|
| **Field ID** | `countryside-pickup-time` |
| **Type** | Time |
| **Label** | Pickup Time |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `countryside` |

#### Field: countryside-total-days
| Property | Value |
|----------|-------|
| **Field ID** | `countryside-total-days` |
| **Type** | Number |
| **Label** | Total Days |
| **Required** | ✅ Yes |
| **Min** | 2 |
| **Max** | 30 |
| **Placeholder** | e.g., 3 |
| **Description** | Minimum 2 days for multi-day trips |
| **Condition** | `select-service` = `countryside` |

#### Field: countryside-pickup-address
| Property | Value |
|----------|-------|
| **Field ID** | `countryside-pickup-address` |
| **Type** | Text |
| **Label** | Pickup Address |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Hotel in Budapest |
| **Condition** | `select-service` = `countryside` |

#### Field: countryside-itinerary
| Property | Value |
|----------|-------|
| **Field ID** | `countryside-itinerary` |
| **Type** | Textarea |
| **Label** | Trip Itinerary / Details |
| **Required** | ✅ Yes |
| **Rows** | 6 |
| **Condition** | `select-service` = `countryside` |

**Placeholder:**
```
Describe your trip, e.g.:

Day 1: Budapest → Eger (wine tasting) → overnight in Eger
Day 2: Eger → Tokaj wine region → return to Budapest
Day 3: Budapest sightseeing → Airport transfer
```

---

### Section: Countryside Special Requirements
```
ID: section-countryside-special
Title: Special Requirements (optional)
Condition: select-service = countryside
```

#### Field: countryside-special-requirements
| Property | Value |
|----------|-------|
| **Field ID** | `countryside-special-requirements` |
| **Type** | Checkbox (multiple) |
| **Required** | ❌ No |
| **Condition** | `select-service` = `countryside` |

**Options:**
```
♿ Wheelchair accessible;wheelchair
👶 Child safety seats;child-seats
🎀 Hostess / Additional Staff;hostess
👤 On-site coordinator;coordinator
🗣️ English-speaking driver;english-driver
🔒 Security / Protocol;security
```

#### Field: countryside-additional-preferences
| Property | Value |
|----------|-------|
| **Field ID** | `countryside-additional-preferences` |
| **Type** | Textarea |
| **Label** | Additional Preferences (optional) |
| **Required** | ❌ No |
| **Placeholder** | Any other requests or preferences... |
| **Rows** | 2 |
| **Condition** | `select-service` = `countryside` |

---

## STEP 3D: F1 GRAND PRIX

**Master Condition:** `select-service` = `f1`

### Section: F1 Header
```
ID: section-f1
Condition: select-service = f1
```

### HTML Field: F1 Title
```html
<h2 class="vb-form-title">F1 Grand Prix Transfers</h2>
<p class="vb-form-subtitle">July 23-26, 2026 • Hungaroring</p>
```
**Condition:** `select-service` = `f1`

---

### Section: F1 Day Selection
```
ID: section-f1-days
Title: Choose Your Day(s)
Condition: select-service = f1
```

#### Field: f1-days
| Property | Value |
|----------|-------|
| **Field ID** | `f1-days` |
| **Type** | Checkbox (multiple) |
| **Label** | Select the days you need transportation |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `f1` |

**Options:**
```
Thursday, July 23, 2026;thu
Friday, July 24, 2026;fri
Saturday, July 25, 2026;sat
Sunday, July 26, 2026;sun
```

### HTML Field: F1 Help Text
```html
<p class="vb-help-text">Maximum 10 hours per day. Service ends upon return to Budapest.</p>
```
**Condition:** `select-service` = `f1`

---

#### Field: f1-pickup-address
| Property | Value |
|----------|-------|
| **Field ID** | `f1-pickup-address` |
| **Type** | Text |
| **Label** | Pickup Address |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Hilton Budapest |
| **Condition** | `select-service` = `f1` |

#### Field: f1-destination
| Property | Value |
|----------|-------|
| **Field ID** | `f1-destination` |
| **Type** | Text |
| **Label** | Event Destination |
| **Required** | ❌ No |
| **Default** | Hungaroring – Formula 1 Hungarian Grand Prix |
| **Read-only** | ✅ Yes (or just display as HTML) |
| **Condition** | `select-service` = `f1` |

#### Field: f1-dropoff-address
| Property | Value |
|----------|-------|
| **Field ID** | `f1-dropoff-address` |
| **Type** | Text |
| **Label** | Final Drop-off Address |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Same as pickup, or Airport |
| **Condition** | `select-service` = `f1` |

---

### Section: F1 Special Requirements
```
ID: section-f1-special
Title: Special Requirements (optional)
Condition: select-service = f1
```

#### Field: f1-special-requirements
| Property | Value |
|----------|-------|
| **Field ID** | `f1-special-requirements` |
| **Type** | Checkbox (multiple) |
| **Required** | ❌ No |
| **Condition** | `select-service` = `f1` |

**Options:**
```
♿ Wheelchair accessible;wheelchair
👶 Child safety seats;child-seats
🎀 Hostess / Additional Staff;hostess
👤 On-site coordinator;coordinator
🗣️ English-speaking driver;english-driver
🔒 Security / Protocol;security
```

#### Field: f1-additional-preferences
| Property | Value |
|----------|-------|
| **Field ID** | `f1-additional-preferences` |
| **Type** | Textarea |
| **Label** | Additional Preferences (optional) |
| **Required** | ❌ No |
| **Placeholder** | Any other requests or preferences... |
| **Rows** | 2 |
| **Condition** | `select-service` = `f1` |

---

## STEP 3E: UEFA CHAMPIONS LEAGUE FINAL

**Master Condition:** `select-service` = `uefa`

### Section: UEFA Header
```
ID: section-uefa
Condition: select-service = uefa
```

### HTML Field: UEFA Title
```html
<h2 class="vb-form-title">UEFA Champions League Final</h2>
<p class="vb-form-subtitle">May 28-31, 2026 • Puskás Aréna, Budapest</p>
```
**Condition:** `select-service` = `uefa`

---

### Section: UEFA Day Selection
```
ID: section-uefa-days
Title: Choose Your Day(s)
Condition: select-service = uefa
```

#### Field: uefa-days
| Property | Value |
|----------|-------|
| **Field ID** | `uefa-days` |
| **Type** | Checkbox (multiple) |
| **Label** | Select the days you need transportation |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `uefa` |

**Options (FONTOS: min hours jelölés!):**
```
Thursday, May 28, 2026 (min. 6 hours);thu
Friday, May 29, 2026 (min. 6 hours);fri
Saturday, May 30, 2026 (MATCH DAY - min. 12 hours);sat
Sunday, May 31, 2026 (min. 6 hours);sun
```

### HTML Field: UEFA Help Text
```html
<p class="vb-help-text">Hourly service only within Budapest during the listed days.</p>
```
**Condition:** `select-service` = `uefa`

---

#### Field: uefa-pickup-address
| Property | Value |
|----------|-------|
| **Field ID** | `uefa-pickup-address` |
| **Type** | Text |
| **Label** | Pickup Address |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Corinthia Hotel Budapest |
| **Condition** | `select-service` = `uefa` |

#### Field: uefa-route-stops
| Property | Value |
|----------|-------|
| **Field ID** | `uefa-route-stops` |
| **Type** | Textarea |
| **Label** | Destination & Route / Stops |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Corinthia Hotel → Puskás Aréna → City Park → Return to hotel |
| **Description** | Enter the planned route with stops (in order) |
| **Condition** | `select-service` = `uefa` |

---

### Section: UEFA Special Requirements
```
ID: section-uefa-special
Title: Special Requirements (optional)
Condition: select-service = uefa
```

#### Field: uefa-special-requirements
| Property | Value |
|----------|-------|
| **Field ID** | `uefa-special-requirements` |
| **Type** | Checkbox (multiple) |
| **Required** | ❌ No |
| **Condition** | `select-service` = `uefa` |

**Options:**
```
♿ Wheelchair accessible;wheelchair
👶 Child safety seats;child-seats
🎀 Hostess / Additional Staff;hostess
👤 On-site coordinator;coordinator
🗣️ English-speaking driver;english-driver
🔒 Security / Protocol;security
```

#### Field: uefa-additional-preferences
| Property | Value |
|----------|-------|
| **Field ID** | `uefa-additional-preferences` |
| **Type** | Textarea |
| **Label** | Additional Preferences (optional) |
| **Required** | ❌ No |
| **Placeholder** | Any other requests or preferences... |
| **Rows** | 2 |
| **Condition** | `select-service` = `uefa` |

---

## STEP 3F: EVENT TRANSPORTATION

**Master Condition:** `select-service` = `event`

### Section: Event Header
```
ID: section-event
Condition: select-service = event
```

### HTML Field: Event Title
```html
<h2 class="vb-form-title">Event Transportation – Request a Proposal</h2>
<p class="vb-form-subtitle">Tell us about your event and transportation needs</p>
```
**Condition:** `select-service` = `event`

---

### HTML Field: Event Sub-navigation
```html
<div class="vb-event-substeps">
  <div class="vb-event-substep active" data-substep="1">
    <div class="vb-event-substep-num">1</div>
    <span>Event Details</span>
  </div>
  <div class="vb-event-substep" data-substep="2">
    <div class="vb-event-substep-num">2</div>
    <span>Transportation Needs</span>
  </div>
</div>
```
**Condition:** `select-service` = `event`

> **MEGJEGYZÉS:** Ez a sub-navigation vizuális elem. A Forminator-ban a mezőket egymás után tesszük, section címekkel elválasztva.

---

### Section: Event Details (Substep 1)
```
ID: section-event-details
Title: Tell us about your event
Condition: select-service = event
```

#### Field: event-name
| Property | Value |
|----------|-------|
| **Field ID** | `event-name` |
| **Type** | Text |
| **Label** | Event Name |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Budapest Tech Summit 2026 |
| **Condition** | `select-service` = `event` |

#### Field: event-organization
| Property | Value |
|----------|-------|
| **Field ID** | `event-organization` |
| **Type** | Text |
| **Label** | Organization Name |
| **Required** | ✅ Yes |
| **Placeholder** | Company or organization name |
| **Condition** | `select-service` = `event` |

#### Field: event-type
| Property | Value |
|----------|-------|
| **Field ID** | `event-type` |
| **Type** | Select |
| **Label** | Event Type |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `event` |

**Options:**
```
-- Select event type --;
Conference / Summit;conference
Corporate Meeting / Incentive;corporate
Wedding / Private Celebration;wedding
Gala / Award Ceremony;gala
Sports Event;sports
Film / TV Production;film
Diplomatic / Government;diplomatic
Other;other
```

#### Field: event-expected-guests
| Property | Value |
|----------|-------|
| **Field ID** | `event-expected-guests` |
| **Type** | Number |
| **Label** | Expected Guests |
| **Required** | ✅ Yes |
| **Placeholder** | Enter number of guests |
| **Condition** | `select-service` = `event` |

#### Field: event-start-date
| Property | Value |
|----------|-------|
| **Field ID** | `event-start-date` |
| **Type** | Date |
| **Label** | Event Start Date |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `event` |

#### Field: event-end-date
| Property | Value |
|----------|-------|
| **Field ID** | `event-end-date` |
| **Type** | Date |
| **Label** | Event End Date |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `event` |

#### Field: event-city
| Property | Value |
|----------|-------|
| **Field ID** | `event-city` |
| **Type** | Text |
| **Label** | Event City |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Budapest |
| **Condition** | `select-service` = `event` |

#### Field: event-venue
| Property | Value |
|----------|-------|
| **Field ID** | `event-venue` |
| **Type** | Text |
| **Label** | Event Venue / Location |
| **Required** | ✅ Yes |
| **Placeholder** | e.g., Hilton Budapest, Buda Castle |
| **Description** | Main event location (hotel, conference center, etc.) |
| **Condition** | `select-service` = `event` |

#### Field: event-venue-2
| Property | Value |
|----------|-------|
| **Field ID** | `event-venue-2` |
| **Type** | Text |
| **Label** | Additional Venue 2 |
| **Required** | ❌ No |
| **Placeholder** | e.g., Gundel Restaurant |
| **Condition** | `select-service` = `event` |

#### Field: event-venue-3
| Property | Value |
|----------|-------|
| **Field ID** | `event-venue-3` |
| **Type** | Text |
| **Label** | Additional Venue 3 |
| **Required** | ❌ No |
| **Placeholder** | e.g., Széchenyi Thermal Bath |
| **Condition** | `select-service` = `event` |

---

### Section: Transportation Needs (Substep 2)
```
ID: section-event-transport
Title: What transportation do you need?
Condition: select-service = event
```

#### Field: event-services-needed
| Property | Value |
|----------|-------|
| **Field ID** | `event-services-needed` |
| **Type** | Checkbox (multiple) |
| **Label** | Services Needed |
| **Required** | ✅ Yes |
| **Condition** | `select-service` = `event` |

**Options:**
```
Airport transfers;airport
Hotel ↔ Venue shuttle;shuttle
Hourly VIP / Chauffeur;hourly-vip
Multi-day program;multi-day
Staff / Crew transport;staff
Other (specify below);other
```

#### Field: event-other-details
| Property | Value |
|----------|-------|
| **Field ID** | `event-other-details` |
| **Type** | Textarea |
| **Label** | Please specify |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | Describe your specific transportation needs... |
| **Condition** | `event-services-needed` contains `other` |

---

#### Field: event-fleet-preferences
| Property | Value |
|----------|-------|
| **Field ID** | `event-fleet-preferences` |
| **Type** | Checkbox (multiple) |
| **Label** | Fleet Preferences (optional) |
| **Required** | ❌ No |
| **Condition** | `select-service` = `event` |

**Options:**
```
🎯 Recommend optimal vehicle mix for my event;recommend-mix
🚐 Prefer uniform fleet (same vehicle type throughout);uniform-fleet
⭐ Prioritize VIP vehicles for executives/speakers;vip-priority
```

### HTML Field: Fleet Help Text
```html
<p class="vb-help-text">You've selected your preferred vehicles in Step 2. Let us know if you have additional preferences for your event.</p>
```
**Condition:** `select-service` = `event`

#### Field: event-fleet-notes
| Property | Value |
|----------|-------|
| **Field ID** | `event-fleet-notes` |
| **Type** | Textarea |
| **Label** | Additional fleet notes (optional) |
| **Required** | ❌ No |
| **Placeholder** | e.g., Need 2 separate vehicles for VIP speakers, rest can be mixed... |
| **Rows** | 2 |
| **Condition** | `select-service` = `event` |

---

### Section: Event Special Requirements
```
ID: section-event-special
Title: Special Requirements (optional)
Condition: select-service = event
```

#### Field: event-special-requirements
| Property | Value |
|----------|-------|
| **Field ID** | `event-special-requirements` |
| **Type** | Checkbox (multiple) |
| **Required** | ❌ No |
| **Condition** | `select-service` = `event` |

**Options:**
```
♿ Wheelchair accessible;wheelchair
👶 Child safety seats;child-seats
🎀 Hostess / Additional Staff;hostess
👤 On-site coordinator;coordinator
🗣️ English-speaking driver;english-driver
🔒 Security / Protocol;security
```

---

#### Field: event-schedule
| Property | Value |
|----------|-------|
| **Field ID** | `event-schedule` |
| **Type** | Textarea |
| **Label** | Schedule / Key Moves (recommended) |
| **Required** | ❌ No |
| **Description** | For accurate pricing, please share at least your top 3 key moves |
| **Condition** | `select-service` = `event` |

**Placeholder:**
```
Example:
• May 15, 10:00 – Airport → Hilton Budapest – 25 guests
• May 15, 18:00 – Hilton → Buda Castle – 25 guests
• May 17, 14:00 – Hilton → Airport – 25 guests
```

#### Field: event-itinerary-upload
| Property | Value |
|----------|-------|
| **Field ID** | `event-itinerary-upload` |
| **Type** | Upload |
| **Label** | Upload Itinerary (optional) |
| **Required** | ❌ No |
| **Allowed types** | PDF, XLSX, DOCX |
| **Max size** | 20MB |
| **Description** | Optional: itinerary, flight list, venue schedule, or RFP brief |
| **Condition** | `select-service` = `event` |

#### Field: event-additional-preferences
| Property | Value |
|----------|-------|
| **Field ID** | `event-additional-preferences` |
| **Type** | Textarea |
| **Label** | Additional Preferences (optional) |
| **Required** | ❌ No |
| **Placeholder** | Any other requests or preferences... |
| **Rows** | 2 |
| **Condition** | `select-service` = `event` |

---

## 5. STEP 4: CONTACT & BILLING

### Page Break #4
- **Label:** Contact & Billing

### Section: Contact & Billing Header
```
ID: section-contact-header
```

### HTML Field: Page Title
```html
<h2 class="vb-form-title">Contact & Billing</h2>
<p class="vb-form-subtitle">Review your services and provide contact details</p>
```

---

### Section: Your Contact Details
```
ID: section-contact
Title: Your Contact Details
```

#### Field: contact-title
| Property | Value |
|----------|-------|
| **Field ID** | `contact-title` |
| **Type** | Select |
| **Label** | Title |
| **Required** | ❌ No |

**Options:**
```
--;
Mr;mr
Mrs;mrs
Ms;ms
Miss;miss
Dr;dr
```

#### Field: contact-first-name
| Property | Value |
|----------|-------|
| **Field ID** | `contact-first-name` |
| **Type** | Text |
| **Label** | First Name |
| **Required** | ✅ Yes |
| **Placeholder** | First name |

#### Field: contact-last-name
| Property | Value |
|----------|-------|
| **Field ID** | `contact-last-name` |
| **Type** | Text |
| **Label** | Last Name |
| **Required** | ✅ Yes |
| **Placeholder** | Last name |

#### Field: contact-email
| Property | Value |
|----------|-------|
| **Field ID** | `contact-email` |
| **Type** | Email |
| **Label** | Email |
| **Required** | ✅ Yes |
| **Placeholder** | email@example.com |

#### Field: contact-phone
| Property | Value |
|----------|-------|
| **Field ID** | `contact-phone` |
| **Type** | Phone |
| **Label** | Phone |
| **Required** | ✅ Yes |
| **Placeholder** | +36 70 XXX XXXX |

---

### Section: Booking For Someone Else
```
ID: section-booking-other
```

#### Field: booking-for-other
| Property | Value |
|----------|-------|
| **Field ID** | `booking-for-other` |
| **Type** | Checkbox (single) |
| **Label** | I'm booking for someone else (e.g., guest, colleague, or client) |
| **Required** | ❌ No |
| **CSS Class** | `vb-toggle-checkbox` |

---

### CLIENT FIELDS (Conditional)

**Condition:** `booking-for-other` is checked

### Section: Passenger / Client Information
```
ID: section-client
Title: Passenger / Client Information
Condition: booking-for-other is checked
```

#### Field: client-title
| Property | Value |
|----------|-------|
| **Field ID** | `client-title` |
| **Type** | Select |
| **Label** | Title |
| **Required** | ❌ No |
| **Condition** | `booking-for-other` is checked |

**Options:**
```
--;
Mr;mr
Mrs;mrs
Ms;ms
Miss;miss
Dr;dr
```

#### Field: client-first-name
| Property | Value |
|----------|-------|
| **Field ID** | `client-first-name` |
| **Type** | Text |
| **Label** | First Name |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | First name |
| **Condition** | `booking-for-other` is checked |

#### Field: client-last-name
| Property | Value |
|----------|-------|
| **Field ID** | `client-last-name` |
| **Type** | Text |
| **Label** | Last Name |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | Last name |
| **Condition** | `booking-for-other` is checked |

#### Field: client-phone
| Property | Value |
|----------|-------|
| **Field ID** | `client-phone` |
| **Type** | Phone |
| **Label** | Mobile |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | +36 70 XXX XXXX |
| **Condition** | `booking-for-other` is checked |

---

### Section: Custom Signage
```
ID: section-signage
```

#### Field: custom-signage
| Property | Value |
|----------|-------|
| **Field ID** | `custom-signage` |
| **Type** | Checkbox (single) |
| **Label** | Use alternative text on the sign (for airport meet & greet service) |
| **Required** | ❌ No |
| **CSS Class** | `vb-toggle-checkbox` |

#### Field: signage-text
| Property | Value |
|----------|-------|
| **Field ID** | `signage-text` |
| **Type** | Text |
| **Label** | Text on sign |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | e.g., Company Name or Group Name |
| **Condition** | `custom-signage` is checked |

---

### Section: Billing Information
```
ID: section-billing
```

#### Field: need-billing
| Property | Value |
|----------|-------|
| **Field ID** | `need-billing` |
| **Type** | Checkbox (single) |
| **Label** | I need an invoice with specific billing details |
| **Required** | ❌ No |
| **CSS Class** | `vb-billing-toggle` |

---

### BILLING FIELDS (Conditional)

**Condition:** `need-billing` is checked

#### Field: billing-name
| Property | Value |
|----------|-------|
| **Field ID** | `billing-name` |
| **Type** | Text |
| **Label** | Name or Company Name |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | e.g., John Doe or ABC Company Ltd. |
| **Condition** | `need-billing` is checked |

#### Field: billing-address
| Property | Value |
|----------|-------|
| **Field ID** | `billing-address` |
| **Type** | Text |
| **Label** | Billing Address |
| **Required** | ✅ Yes (when visible) |
| **Placeholder** | Street, City, Postal Code, Country |
| **Condition** | `need-billing` is checked |

#### Field: billing-vat
| Property | Value |
|----------|-------|
| **Field ID** | `billing-vat` |
| **Type** | Text |
| **Label** | VAT / Tax Number |
| **Required** | ❌ No |
| **Placeholder** | e.g., HU12345678 |
| **Condition** | `need-billing` is checked |

#### Field: billing-notes
| Property | Value |
|----------|-------|
| **Field ID** | `billing-notes` |
| **Type** | Textarea |
| **Label** | Billing Notes |
| **Required** | ❌ No |
| **Placeholder** | Any additional billing instructions or references... |
| **Rows** | 2 |
| **Condition** | `need-billing` is checked |

---

### Section: Additional Information
```
ID: section-additional
Title: Additional Information
```

#### Field: how-heard
| Property | Value |
|----------|-------|
| **Field ID** | `how-heard` |
| **Type** | Select |
| **Label** | How did you hear about us? |
| **Required** | ❌ No |

**Options:**
```
-- Select --;
Google Search;google
Social Media;social
Recommendation;recommendation
Travel Agency / DMC;travel-agency
Returning Customer;returning
Hotel Concierge;hotel
Other;other
```

#### Field: promo-code
| Property | Value |
|----------|-------|
| **Field ID** | `promo-code` |
| **Type** | Text |
| **Label** | Promo Code (optional) |
| **Required** | ❌ No |
| **Placeholder** | Enter promo code if you have one |

---

### Section: Payment Method
```
ID: section-payment
Title: Preferred Payment Method
```

### HTML Field: Payment Help Text
```html
<p class="vb-help-text">For credit card payments, a minimal processing fee applies. Any applicable fees will be included in the quote.</p>
```

#### Field: payment-method
| Property | Value |
|----------|-------|
| **Field ID** | `payment-method` |
| **Type** | Radio |
| **Label** | (hidden) |
| **Required** | ✅ Yes |

**Options:**
```
<strong>Bank Transfer</strong> <span style="color: #2d5016; font-weight: 600;">— No additional fees</span>;bank_transfer
<strong>Credit Card</strong> <span style="color: #8B6914; font-weight: 600;">— +3% processing fee</span>;credit_card
```

---

### Section: Terms & Conditions
```
ID: section-terms
```

#### Field: terms-consent
| Property | Value |
|----------|-------|
| **Field ID** | `terms-consent` |
| **Type** | Consent / GDPR |
| **Label** | I accept the Terms & Conditions and Privacy Policy |
| **Required** | ✅ Yes |
| **Link 1** | Terms & Conditions → /terms |
| **Link 2** | Privacy Policy → /privacy |

---

## 6. KONDÍCIÓK ÖSSZEFOGLALÓ

### Master Conditions (Service Type)

| Mező csoport | Kondíció |
|--------------|----------|
| Airport flow | `select-service` = `airport` |
| Hourly flow | `select-service` = `hourly` |
| Multi-day flow | `select-service` = `countryside` |
| F1 flow | `select-service` = `f1` |
| UEFA flow | `select-service` = `uefa` |
| Event flow | `select-service` = `event` |

### Nested Conditions

| Mező | Parent Condition | Own Condition |
|------|------------------|---------------|
| Return transfer fields | service = airport | `airport-return-transfer` = `yes` |
| Guide fields | service = hourly | `hourly-service-type` = `sightseeing` |
| Duration field | service = hourly | `hourly-service-type` = `chauffeur` |
| Chauffeur route fields | service = hourly | `hourly-service-type` = `chauffeur` |
| Custom tour textarea | service = hourly + type = sightseeing | `tour-package` = `custom` |
| Event other details | service = event | `event-services-needed` contains `other` |

### Toggle Conditions (Step 4)

| Mező csoport | Kondíció |
|--------------|----------|
| Client fields | `booking-for-other` is checked |
| Signage text | `custom-signage` is checked |
| Billing fields | `need-billing` is checked |

### Vehicle Qty Conditions

| Qty Field | Kondíció |
|-----------|----------|
| `vehicle-business-car-qty` | `vehicle-business-car` is checked |
| `vehicle-premium-van-qty` | `vehicle-premium-van` is checked |
| `vehicle-minibus-qty` | `vehicle-minibus` is checked |
| `vehicle-coach-qty` | `vehicle-coach` is checked |
| `vehicle-luxury-minibus-qty` | `vehicle-luxury-minibus` is checked |
| `vehicle-luxury-car-qty` | `vehicle-luxury-car` is checked |

---

## 7. CSS KÓD

A teljes CSS kódot a Forminator → Appearance → Custom CSS mezőbe kell beilleszteni:

```css
/* =====================================================
   VANBUDAPEST BOOKING FORM v2 - CUSTOM CSS
   ===================================================== */

/* CSS Variables */
:root {
  --vb-navy: #0A1F44;
  --vb-gold: #C8B560;
  --vb-gold-dark: #B78D38;
  --vb-gold-light: #D4C470;
  --vb-cream: #F5F0E8;
  --vb-gray-dark: #4a5568;
  --vb-error: #e53e3e;
  --vb-shadow: 0 4px 6px rgba(0,0,0,0.1);
  --vb-shadow-lg: 0 10px 25px rgba(0,0,0,0.15);
  --vb-transition: all 0.3s ease;
}

/* Form Container */
.forminator-custom-form {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  max-width: 800px;
  margin: 0 auto;
}

/* Progress Bar / Steps */
.forminator-pagination-progress {
  background: var(--vb-cream) !important;
  padding: 20px !important;
  border-radius: 12px !important;
  margin-bottom: 24px !important;
}

.forminator-step-number {
  background: var(--vb-gold) !important;
  color: var(--vb-navy) !important;
  font-weight: 700 !important;
}

.forminator-step.forminator-current .forminator-step-number {
  background: var(--vb-navy) !important;
  color: #fff !important;
}

/* Section Titles */
.forminator-section--title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 16px !important;
  font-weight: 600 !important;
  color: var(--vb-navy) !important;
  padding-bottom: 8px !important;
  border-bottom: 2px solid var(--vb-gold) !important;
  display: inline-block !important;
  margin-bottom: 20px !important;
}

/* Form Titles (HTML fields) */
.vb-form-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--vb-navy);
  margin-bottom: 8px;
}

.vb-form-subtitle {
  color: var(--vb-gray-dark);
  margin-bottom: 32px;
}

/* Input Fields */
.forminator-input,
.forminator-select,
.forminator-textarea {
  border: 2px solid #e0e0e0 !important;
  border-radius: 8px !important;
  padding: 14px 16px !important;
  font-size: 15px !important;
  transition: var(--vb-transition) !important;
}

.forminator-input:focus,
.forminator-select:focus,
.forminator-textarea:focus {
  border-color: var(--vb-gold) !important;
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(200, 181, 96, 0.2) !important;
}

/* Radio/Checkbox Items */
.forminator-radio,
.forminator-checkbox {
  border: 2px solid #e0e0e0 !important;
  border-radius: 8px !important;
  padding: 12px 16px !important;
  margin-bottom: 8px !important;
  transition: var(--vb-transition) !important;
}

.forminator-radio:hover,
.forminator-checkbox:hover {
  border-color: var(--vb-gold-light) !important;
}

.forminator-radio.forminator-is_active,
.forminator-checkbox.forminator-is_active {
  border-color: var(--vb-gold) !important;
  background: rgba(200, 181, 96, 0.1) !important;
}

/* VIP Badge for Luxury Vehicles */
.vip-vehicle .forminator-checkbox-label::after {
  content: "VIP";
  display: inline-block;
  background: linear-gradient(135deg, #c9a227 0%, #d4af37 50%, #c9a227 100%);
  color: var(--vb-navy);
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  margin-left: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Most Popular Badge for Tour Packages */
.forminator-radio[data-value="classic"] {
  border: 2px solid var(--vb-gold) !important;
  background: linear-gradient(135deg, rgba(200,181,96,0.08) 0%, rgba(200,181,96,0.02) 100%) !important;
  position: relative !important;
  overflow: visible !important;
}

.forminator-radio[data-value="classic"]::before {
  content: "★ Most Popular";
  position: absolute;
  top: -10px;
  right: 16px;
  background: linear-gradient(135deg, #C8B560 0%, #A89540 100%);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 12px;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(200,181,96,0.4);
  animation: pulse-glow 2s ease-in-out infinite;
  z-index: 10;
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(200,181,96,0.4);
  }
  50% {
    box-shadow: 0 2px 16px rgba(200,181,96,0.7), 0 0 24px rgba(200,181,96,0.3);
  }
}

/* Toggle Checkbox Styling */
.vb-toggle-checkbox {
  background: #f8f9fa !important;
  border-radius: 8px !important;
  padding: 12px 16px !important;
}

.vb-toggle-checkbox .forminator-checkbox-label {
  font-weight: 500 !important;
}

/* Billing Toggle - Gold Styling */
.vb-billing-toggle {
  background: linear-gradient(135deg, #f8f6f0 0%, #f0ede4 100%) !important;
  border: 1px solid #d4c9a8 !important;
  border-radius: 8px !important;
  padding: 14px 18px !important;
}

.vb-billing-toggle .forminator-checkbox-label {
  font-weight: 600 !important;
  color: var(--vb-navy) !important;
}

/* Payment Method Styling */
.forminator-radio[data-value="bank_transfer"] .forminator-radio-label span {
  color: #2d5016 !important;
}

.forminator-radio[data-value="credit_card"] .forminator-radio-label span {
  color: #8B6914 !important;
}

/* Help Text */
.vb-help-text,
.forminator-description {
  font-size: 12px !important;
  color: var(--vb-gray-dark) !important;
  margin-top: 6px !important;
}

/* Buttons */
.forminator-button {
  background: var(--vb-gold) !important;
  color: var(--vb-navy) !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 1.5px !important;
  padding: 16px 32px !important;
  border-radius: 8px !important;
  border: none !important;
  transition: var(--vb-transition) !important;
}

.forminator-button:hover {
  background: var(--vb-gold-dark) !important;
  transform: translateY(-2px) !important;
  box-shadow: var(--vb-shadow-lg) !important;
}

.forminator-button-back {
  background: transparent !important;
  border: 2px solid var(--vb-navy) !important;
  color: var(--vb-navy) !important;
}

.forminator-button-back:hover {
  background: var(--vb-navy) !important;
  color: #fff !important;
}

/* Event Sub-steps Navigation */
.vb-event-substeps {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-bottom: 32px;
}

.vb-event-substep {
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0.5;
}

.vb-event-substep.active {
  opacity: 1;
}

.vb-event-substep-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--vb-gold);
  color: var(--vb-navy);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .vb-form-title {
    font-size: 24px;
  }
  
  .forminator-row {
    flex-direction: column;
  }
  
  .forminator-col {
    width: 100% !important;
  }
}
```

---

## 8. EMAIL SABLON

### Admin Notification Email

**Subject:**
```
🚗 New VanBudapest Booking #{submission_id} | {select-service}
```

**Body (HTML):**
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: 'Inter', Arial, sans-serif; background: #f5f5f5; padding: 20px; }
    .container { max-width: 600px; margin: 0 auto; background: #fff; border-radius: 12px; overflow: hidden; }
    .header { background: #0A1F44; padding: 24px; text-align: center; }
    .header img { height: 40px; }
    .content { padding: 32px; }
    .section { margin-bottom: 24px; }
    .section-title { font-size: 14px; font-weight: 700; color: #C8B560; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; border-bottom: 2px solid #C8B560; padding-bottom: 8px; display: inline-block; }
    .field { margin-bottom: 8px; }
    .field-label { font-weight: 600; color: #0A1F44; }
    .field-value { color: #4a5568; }
    .btn { display: inline-block; background: #C8B560; color: #0A1F44; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; margin-top: 16px; }
    .footer { background: #f8f6f0; padding: 20px; text-align: center; font-size: 12px; color: #666; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="https://vanbudapest.com/wp-content/uploads/vanbudapest-logo-white.png" alt="VanBudapest">
    </div>
    <div class="content">
      <h2 style="color: #0A1F44; margin-bottom: 24px;">New Booking Request #{submission_id}</h2>
      
      <div class="section">
        <div class="section-title">Service Details</div>
        <div class="field"><span class="field-label">Service Type:</span> <span class="field-value">{select-service}</span></div>
        <div class="field"><span class="field-label">Vehicles:</span> <span class="field-value">{vehicle-business-car} {vehicle-premium-van} {vehicle-minibus} {vehicle-coach} {vehicle-luxury-minibus} {vehicle-luxury-car}</span></div>
        <div class="field"><span class="field-label">Total Guests:</span> <span class="field-value">{total-guests}</span></div>
        <div class="field"><span class="field-label">Luggage:</span> <span class="field-value">{total-luggage}</span></div>
      </div>
      
      <div class="section">
        <div class="section-title">Contact Information</div>
        <div class="field"><span class="field-label">Name:</span> <span class="field-value">{contact-title} {contact-first-name} {contact-last-name}</span></div>
        <div class="field"><span class="field-label">Email:</span> <span class="field-value">{contact-email}</span></div>
        <div class="field"><span class="field-label">Phone:</span> <span class="field-value">{contact-phone}</span></div>
      </div>
      
      <div class="section">
        <div class="section-title">Payment & Marketing</div>
        <div class="field"><span class="field-label">Payment Method:</span> <span class="field-value">{payment-method}</span></div>
        <div class="field"><span class="field-label">How heard:</span> <span class="field-value">{how-heard}</span></div>
        <div class="field"><span class="field-label">Promo Code:</span> <span class="field-value">{promo-code}</span></div>
      </div>
      
      <a href="https://vanbudapest.com/wp-admin/admin.php?page=forminator-entries&form_id={form_id}&entry_id={submission_id}" class="btn">View Full Submission →</a>
    </div>
    <div class="footer">
      VanBudapest Booking System | Submission #{submission_id} | {date_mdy}
    </div>
  </div>
</body>
</html>
```

---

## ✅ CHECKLIST - IMPLEMENTÁCIÓ ELLENŐRZÉSE

### Űrlap létrehozás
- [ ] Új form létrehozva: "VanBudapest Booking Form v2"
- [ ] Pagination: 4 step, labels beállítva
- [ ] Button labels beállítva

### Step 1: Service Selection
- [ ] `select-service` radio field (6 opció)
- [ ] HTML title field

### Step 2: Vehicle & Group
- [ ] 6 vehicle checkbox + 6 qty field
- [ ] Qty fields kondíciók beállítva
- [ ] `total-guests` number field
- [ ] `total-luggage` number field
- [ ] `special-items` text field

### Step 3: Service Details
- [ ] **Airport flow** - minden mező + return kondíciók
- [ ] **Hourly flow** - service type + guide + tour packages + duration kondíciók
- [ ] **Multi-day flow** - minden mező
- [ ] **F1 flow** - day checkboxes + addresses
- [ ] **UEFA flow** - day checkboxes + addresses
- [ ] **Event flow** - substep 1 + substep 2 mezők

### Step 4: Contact & Billing
- [ ] Contact fields (title, first, last, email, phone)
- [ ] `booking-for-other` checkbox + client fields kondíció
- [ ] `custom-signage` checkbox + text field kondíció
- [ ] `need-billing` checkbox + billing fields kondíció
- [ ] `how-heard` dropdown
- [ ] `promo-code` text
- [ ] `payment-method` radio
- [ ] `terms-consent` checkbox

### CSS & Email
- [ ] Custom CSS beillesztve
- [ ] Admin email sablon beállítva
- [ ] Tesztelés minden service type-ra

---

**Dokumentum vége**

*Készítette: Claude AI*
*Verzió: 1.0*
*Dátum: 2026-01-31*
