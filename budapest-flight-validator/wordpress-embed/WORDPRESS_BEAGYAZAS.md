# WordPress Beágyazási Útmutató

## 📋 BUD Flight Validator beágyazása WordPress oldalba

### 1. módszer: Iframe beágyazás (Egyszerű)

#### A. Ha külön szerveren fut az alkalmazás

```html
<iframe
    src="http://your-domain.com:3000"
    width="100%"
    height="1200px"
    frameborder="0"
    style="border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
</iframe>
```

**WordPress oldalon:**
1. Új oldal / bejegyzés létrehozása
2. Block Editor → Custom HTML block hozzáadása
3. Beillesztés az iframe kód
4. Közzététel

---

### 2. módszer: Beágyazott HTML kód (Teljes integráció)

#### A. HTML kód beillesztése

1. **WordPress Admin → Pages → Add New**
2. **Block Editor → Custom HTML block**
3. **Másolja be a `bud-flight-validator-embed.html` teljes tartalmát**

#### B. API URL módosítása

A beágyazott HTML-ben keresse meg ezt a sort:

```javascript
const BUD_API_URL = 'http://localhost:3000/api/validate'; // ← MÓDOSÍTSA EZT!
```

Változtassa meg a saját szerver címére:

```javascript
// Ha ugyanazon a domainen fut:
const BUD_API_URL = 'https://vanbudapest.com/api/validate';

// Ha külön szerveren:
const BUD_API_URL = 'http://your-server.com:3000/api/validate';
```

#### C. CORS engedélyezése

Ha külön szerveren fut, engedélyezze a WordPresst a `server.js`-ben:

```javascript
const cors = require('cors');

app.use(cors({
  origin: ['https://vanbudapest.com', 'http://vanbudapest.com'],
  credentials: true
}));
```

---

### 3. módszer: Shortcode használat (Haladó)

#### A. functions.php módosítása

Adja hozzá a WordPress témájának `functions.php` fájljához:

```php
<?php
function bud_flight_validator_shortcode() {
    ob_start();
    include(get_template_directory() . '/bud-flight-validator-embed.html');
    return ob_get_clean();
}
add_shortcode('bud_flight_validator', 'bud_flight_validator_shortcode');
?>
```

#### B. HTML fájl elhelyezése

Másolja a `bud-flight-validator-embed.html` fájlt a WordPress téma könyvtárába:

```
/wp-content/themes/your-theme/bud-flight-validator-embed.html
```

#### C. Shortcode használata

Bármely WordPress oldalon / bejegyzésben:

```
[bud_flight_validator]
```

---

### 4. módszer: Plugin létrehozás (Professzionális)

#### A. Plugin struktúra

Hozzon létre egy mappát:
```
/wp-content/plugins/bud-flight-validator/
```

#### B. Főfájl: `bud-flight-validator.php`

```php
<?php
/**
 * Plugin Name: BUD Flight Validator
 * Description: Budapest Airport flight validation tool
 * Version: 1.0
 * Author: VanBudapest.com
 */

function bud_validator_enqueue_scripts() {
    wp_enqueue_style('bud-validator-css', plugins_url('assets/style.css', __FILE__));
    wp_enqueue_script('bud-validator-js', plugins_url('assets/app.js', __FILE__), array(), '1.0', true);

    // API URL átadása JavaScript-nek
    wp_localize_script('bud-validator-js', 'budValidatorConfig', array(
        'apiUrl' => get_option('bud_validator_api_url', 'http://localhost:3000/api/validate')
    ));
}
add_action('wp_enqueue_scripts', 'bud_validator_enqueue_scripts');

function bud_validator_shortcode() {
    ob_start();
    include(plugin_dir_path(__FILE__) . 'templates/validator.html');
    return ob_get_clean();
}
add_shortcode('bud_validator', 'bud_validator_shortcode');

// Admin beállítások oldal
function bud_validator_admin_menu() {
    add_options_page(
        'BUD Flight Validator Settings',
        'BUD Validator',
        'manage_options',
        'bud-validator-settings',
        'bud_validator_settings_page'
    );
}
add_action('admin_menu', 'bud_validator_admin_menu');

function bud_validator_settings_page() {
    ?>
    <div class="wrap">
        <h1>BUD Flight Validator Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('bud_validator_options');
            do_settings_sections('bud_validator_options');
            ?>
            <table class="form-table">
                <tr>
                    <th scope="row">API URL</th>
                    <td>
                        <input type="text" name="bud_validator_api_url"
                               value="<?php echo esc_attr(get_option('bud_validator_api_url')); ?>"
                               class="regular-text">
                        <p class="description">Az alkalmazás szerver URL-je (pl. http://localhost:3000/api/validate)</p>
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

function bud_validator_register_settings() {
    register_setting('bud_validator_options', 'bud_validator_api_url');
}
add_action('admin_init', 'bud_validator_register_settings');
?>
```

#### C. Aktiválás

1. WordPress Admin → Plugins → Installed Plugins
2. Activate "BUD Flight Validator"
3. Settings → BUD Validator → API URL beállítása
4. Használat: `[bud_validator]` shortcode

---

## 🚀 Gyors teszt

### Lokális tesztelés

1. **Szerver indítása:**
```bash
cd budapest-flight-validator
npm start
```

2. **WordPress oldalon:**
- Custom HTML block
- Beillesztés:
```html
<iframe src="http://localhost:3000" width="100%" height="1200px" frameborder="0"></iframe>
```

3. **Előnézet** → Működnie kell!

---

## 🔒 Biztonsági megjegyzések

### HTTPS használata éles környezetben

Ha a WordPress HTTPS-en fut, a validator API-nak is HTTPS-en kell futnia (mixed content blokkolás).

**Megoldás:**
- SSL tanúsítvány a validator szervernek
- Reverse proxy (nginx) használata
- Cloudflare vagy hasonló proxy

### CORS beállítások

Mindig korlátozza a CORS-t a saját domainre:

```javascript
app.use(cors({
  origin: ['https://vanbudapest.com'],
  credentials: true
}));
```

---

## 📱 Mobil responsivitás

A beágyazott verzió automatikusan reszponzív. WordPress oldalon tesztelje:

- Desktop (1920px+)
- Tablet (768px - 1024px)
- Mobile (320px - 768px)

---

## ❓ Gyakori problémák

### "Nem sikerült csatlakozni a szerverhez"

**Megoldás:**
- Ellenőrizze, hogy a szerver fut-e: `npm start`
- Ellenőrizze az API URL-t a beágyazott kódban
- Ellenőrizze a CORS beállításokat

### "Mixed content" hiba (HTTPS oldal + HTTP API)

**Megoldás:**
- Használjon HTTPS-t mindkét oldalon
- Vagy használjon reverse proxy-t

### Iframe nem jelenik meg

**Megoldás:**
- Ellenőrizze az iframe height értékét
- Néhány WordPress téma blokkolhatja az iframe-eket
- Próbálja Custom HTML block-ot használni

---

## 📞 Támogatás

Kérdések esetén: support@vanbudapest.com
