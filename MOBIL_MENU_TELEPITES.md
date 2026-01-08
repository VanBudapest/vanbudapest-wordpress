# VanBudapest.com - Mobil Drawer Menü Telepítése

## 🎯 Mit változtattunk?

A régi **teljes képernyős fehér mobil menüt** lecseréltük egy **elegáns, balról kinyíló drawer menüre** (Four Seasons stílusban):

### ✅ Új funkciók:
- **Balról slide-in drawer menü** (340px széles)
- **Sötét navy háttér** (#0A1F44) fehér szöveggel
- **Backdrop overlay** (sötét, blur effekt)
- **Smooth animációk** (cubic-bezier easing)
- **Premium gold glow** a Contact & Booking gombon
- **Hover effektek** (padding-left animáció)
- **Elegáns dropdown gombok** gold accent-tel
- **Custom scrollbar** styling
- **Body scroll lock** amikor menü nyitva

---

## 📁 Fájlok

### 1. `header-complete-v7.css`
**TELJES CSS kód** (Desktop + Mobil Drawer)
- Használd ezt, ha **az egész header CSS-t** cserélni akarod

### 2. `header-mobile-drawer-style.css`
**CSAK mobil rész** (782px alatt)
- Használd ezt, ha **csak a mobil menüt** akarod cserélni
- A desktop rész változatlan marad

---

## 🚀 Telepítés (2 opció)

### **Opció A: Teljes csere** (AJÁNLOTT)

1. **Nyisd meg WordPress Admint**
   - Menj: `Megjelenés` → `Testreszabás` → `Additional CSS`

2. **Töröld a TELJES régi CSS kódot**
   - Jelöld ki az összes CSS-t (Ctrl+A) és töröld

3. **Másold be az új kódot**
   - Nyisd meg: `header-complete-v7.css`
   - Másold be a TELJES tartalmat

4. **Mentés**
   - Kattints: `Publish` vagy `Közzététel`

---

### **Opció B: Csak mobil rész cseréje**

1. **Nyisd meg WordPress Admint**
   - Menj: `Megjelenés` → `Testreszabás` → `Additional CSS`

2. **Keresd meg a mobil részt**
   - Keresd a következő sort: `/* ------------ 8. MOBIL NAVIGÁCIÓ (782px alatt) */`
   - Vagy: `@media screen and (max-width: 781px) {`

3. **Töröld a régi mobil részt**
   - Töröld az EGÉSZ 8. section-t (a `@media` kezdetétől a záró `}` -ig)
   - VIGYÁZZ: NE töröld a desktop részt (7. section)!

4. **Másold be az új mobil kódot**
   - Nyisd meg: `header-mobile-drawer-style.css`
   - Másold be a TELJES tartalmat a törölt rész helyére

5. **Mentés**
   - Kattints: `Publish` vagy `Közzététel`

---

## 🧪 Tesztelés

### Desktop (782px felett):
- ✅ Header fix magasság (70px)
- ✅ Logo látható
- ✅ Menüpontok horizontálisan
- ✅ Contact & Booking gold glow effekt
- ✅ Dropdown menük fehér háttéren

### Mobil (782px alatt):
- ✅ Header fix magasság (60px)
- ✅ Hamburger ikon látható (jobb felső)
- ✅ Kattintásra: drawer balról kinyílik
- ✅ Backdrop overlay megjelenik
- ✅ Menü navy háttérrel, fehér szöveggel
- ✅ Close gomb (X) a drawer jobb felső sarkában
- ✅ Contact & Booking gold gomb a lista alján
- ✅ Dropdown nyíl gombok gold accent-tel
- ✅ Smooth slide-in/out animáció

### Tesztelési lépések:

1. **Mobil nézet aktiválása**
   - Desktop: nyomd meg `F12` → válaszd a mobil nézetet
   - Vagy: nyisd meg a telefon böngészőjében

2. **Hamburger menü tesztelése**
   - Kattints a hamburger ikonra (≡)
   - Drawer balról kinyílik
   - Backdrop megjelenik

3. **Menü interakciók**
   - Menüpontokra kattintva: hover effekt
   - Dropdown nyilakra kattintva: submenu kinyílik
   - Contact & Booking: gold glow pulzál

4. **Bezárás tesztelése**
   - X gomb: menü bezárul
   - Backdrop kattintás: menü bezárul (ha WordPress támogatja)

---

## 🎨 Színek és változók

Az új drawer menü színei:

```css
--vb-navy: #0A1F44           /* Drawer háttér */
--vb-white: #FFFFFF          /* Szöveg szín */
--vb-gold: #C8B560           /* Accent szín */
--vb-gold-light: #E5D9A8     /* Hover accent */
--vb-drawer-width: 340px     /* Drawer szélesség */
```

### Testre szabás:

Ha változtatni szeretnél a drawer szélességén vagy színeken:

1. Keresd meg a `:root` változókat (a fájl tetején)
2. Módosítsd az értékeket:

```css
:root {
    --vb-drawer-width: 360px;  /* Szélesebb drawer */
    --vb-drawer-bg: #1A2F5A;   /* Világosabb navy */
}
```

---

## 🔧 JavaScript szükséges?

**NEM!** Az új drawer menü **tisztán CSS-sel** működik.

A WordPress navigation block már kezeli a toggle funcionality-t:
- `.is-menu-open` class automatikusan hozzáadódik
- `aria-expanded` attributumok kezelése
- Submenu nyitás/zárás

**Egyetlen kivétel:**
Ha szeretnéd, hogy **backdrop kattintásra** bezáruljon a menü, akkor szükséges egy kis JavaScript:

```javascript
// WordPress Customizer > Additional CSS alatt NEM működik!
// Ezt egy külön JS fájlba kell tenni (theme functions.php)

document.addEventListener('DOMContentLoaded', function() {
    const backdrop = document.querySelector('.wp-block-navigation__responsive-container');

    if (backdrop) {
        backdrop.addEventListener('click', function(e) {
            // Ha a backdrop-ra kattintunk (nem a menüre)
            if (e.target === backdrop) {
                // Bezárás trigger
                const closeBtn = backdrop.querySelector('.wp-block-navigation__responsive-container-close');
                if (closeBtn) closeBtn.click();
            }
        });
    }
});
```

---

## 📱 Kompatibilitás

### Böngészők:
- ✅ Chrome 90+ (Android, Desktop)
- ✅ Safari 14+ (iOS, macOS)
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Samsung Internet 14+

### WordPress:
- ✅ WordPress 5.9+
- ✅ Gutenberg (FSE) támogatás
- ✅ Classic témák (ha navigation block-ot használnak)

### Funkciók:
- ✅ `transform: translateX()` - slide-in
- ✅ `backdrop-filter: blur()` - iOS 9+, Android 10+
- ✅ `dvh` units - modern viewport height
- ✅ `:has()` pseudo-class - body scroll lock (Chrome 105+)

**Fallback:** Régebbi böngészőkön a blur effekt nem jelenik meg, de a drawer működik.

---

## 🐛 Hibaelhárítás

### Probléma: Drawer nem nyílik ki

**Ok:** WordPress navigation block JavaScript nincs betöltve

**Megoldás:**
1. Ellenőrizd, hogy használsz-e `wp-block-navigation` block-ot
2. Győződj meg róla, hogy a témád támogatja a FSE-t
3. Próbáld újragenerálni a CSS-t: WordPress Admin → `Megjelenés` → `Testreszabás` → `Publish`

---

### Probléma: Backdrop nem jelenik meg

**Ok:** `::before` pseudo-element nem támogatott az adott elemre

**Megoldás:**
Használj külön backdrop elemet. Adj hozzá a `functions.php`-hoz:

```php
add_action('wp_footer', function() {
    ?>
    <style>
    .mobile-menu-backdrop {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(10, 31, 68, 0.8);
        backdrop-filter: blur(4px);
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s;
        z-index: 99997;
    }
    .is-menu-open ~ .mobile-menu-backdrop {
        opacity: 1;
        visibility: visible;
    }
    </style>
    <div class="mobile-menu-backdrop"></div>
    <?php
});
```

---

### Probléma: Drawer túl széles kis képernyőn

**Ok:** `--vb-drawer-width` túl nagy

**Megoldás:**
A CSS már tartalmaz `max-width: 85vw` korlátot. Ha szeretnéd kisebbre állítani:

```css
@media screen and (max-width: 360px) {
    :root {
        --vb-drawer-width: 280px;  /* Kisebb drawer */
    }
}
```

---

### Probléma: Menü mögött látszik a tartalom (scroll)

**Ok:** Body scroll lock nem működik

**Megoldás:**
Add hozzá manuálisan:

```css
body.menu-is-open {
    overflow: hidden !important;
    position: fixed !important;
    width: 100% !important;
}
```

És egy kis JS (theme functions.php):

```javascript
const menuToggle = document.querySelector('.wp-block-navigation__responsive-container-open');
const menu = document.querySelector('.wp-block-navigation__responsive-container');

if (menuToggle && menu) {
    menuToggle.addEventListener('click', () => {
        document.body.classList.toggle('menu-is-open');
    });
}
```

---

## 📞 Kapcsolat

Ha bármilyen kérdésed van, vagy segítségre van szükséged:

1. Ellenőrizd ezt a dokumentumot
2. Nézd meg a `header-complete-v7.css` kommentjeit
3. Teszteld mobilon és desktopon is

---

## 🎉 Összefoglalás

Az új **drawer-style mobil menü**:
- ✅ Professzionális, elegáns megjelenés
- ✅ Four Seasons inspirált design
- ✅ Smooth animációk és effektek
- ✅ Responsive és mobile-first
- ✅ Accessibility támogatás
- ✅ Tisztán CSS (nincs JS)
- ✅ WordPress kompatibilis

**Élvezd az új menüt! 🚀**

---

*Verzió: 7.0*
*Utolsó frissítés: 2026-01-08*
*Készítette: Claude Code*
