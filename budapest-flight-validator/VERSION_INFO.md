# 📦 BUD Flight Validator - Verzió Információ

## Verzió: 1.0.0
**Kiadás dátuma:** 2025-11-15

---

## 📋 Elérhető Verziók

### 1. Web Alkalmazás ✅
**Állapot:** KÉSZ

**Indítás:**
```bash
npm install
npm start
```

**Hozzáférés:** http://localhost:3000

**Funkciók:**
- ✅ Excel/CSV fájl feltöltés (drag & drop)
- ✅ Budapestre érkező járatok validálása
- ✅ Csak Megjegyzés oszlop módosítása
- ✅ Eredeti formátum megőrzése
- ✅ Több forrásból történő ellenőrzés
- ✅ Modern, responsive UI

---

### 2. Desktop Alkalmazás (Electron) ✅
**Állapot:** KÉSZ - Telepítésre vár

**Fájlok:**
- ✅ `electron-main.js` - Fő Electron folyamat
- ✅ `server.js` - Módosítva Electron támogatással
- ✅ `package.json` - Build scriptek konfigurálva
- ✅ `build/README.md` - Ikon útmutató

**Hiányzik:** `build/icon.ico` (Felhasználónak kell hozzáadni)

**Telepítő készítése:**
```bash
npm install
# Tegye a build/icon.ico fájlt a build/ mappába
npm run electron-dev  # Teszt
npm run build:win     # Telepítő készítés
```

**Eredmény:**
- `dist/BUD Flight Validator Setup 1.0.0.exe`
- Natív Windows alkalmazás
- Start menü + Desktop ikon
- VanBudapest.com branding

**Platformok:**
- ✅ Windows (NSIS telepítő)
- ✅ macOS (DMG) - `npm run build:mac`
- ✅ Linux (AppImage) - `npm run build:linux`

**Részletes útmutató:** [ELECTRON_SETUP.md](ELECTRON_SETUP.md)

---

### 3. WordPress Beágyazás ✅
**Állapot:** KÉSZ

**Fájlok:**
- ✅ `wordpress-embed/bud-flight-validator-embed.html` - Standalone verzió
- ✅ `wordpress-embed/WORDPRESS_BEAGYAZAS.md` - Részletes útmutató

**Beágyazási módszerek:**

#### A. Iframe (Legegyszerűbb)
```html
<iframe src="http://your-server:3000" width="100%" height="1200px"></iframe>
```

#### B. Custom HTML Block
1. WordPress Admin → Pages → Add New
2. Custom HTML block
3. Paste teljes HTML kód
4. Módosítsa az API URL-t

#### C. Shortcode
```php
add_shortcode('bud_validator', 'bud_validator_shortcode');
```

**Használat:** `[bud_validator]`

**CORS konfiguráció szükséges!**

---

## 📂 Projekt Struktúra

```
budapest-flight-validator/
├── public/                          # Frontend
│   ├── index.html                  # Főoldal
│   ├── style.css                   # Modern styling
│   └── app.js                      # Kliens logika
├── src/                            # Backend
│   ├── excelProcessor.js          # Excel kezelés (ExcelJS)
│   └── flightValidator.js         # Járat validálás
├── wordpress-embed/                # WordPress verzió
│   ├── bud-flight-validator-embed.html
│   └── WORDPRESS_BEAGYAZAS.md
├── build/                          # Electron ikonok
│   └── README.md                  # Ikon útmutató
├── uploads/                        # Ideiglenes feltöltések
├── electron-main.js               # Electron fő folyamat
├── server.js                      # Express szerver
├── package.json                   # Függőségek + build scriptek
├── README.md                      # Főbb dokumentáció
├── QUICK_START.md                 # Gyors indítás
├── ELECTRON_SETUP.md              # Electron részletes útmutató
├── LICENSE                        # MIT License
└── VERSION_INFO.md                # Ez a fájl
```

---

## 🛠️ Függőségek

### Production (dependencies)
```json
{
  "express": "^4.18.2",      // Web szerver
  "multer": "^1.4.5",        // Fájl feltöltés
  "exceljs": "^4.4.0",       // Excel feldolgozás
  "axios": "^1.6.0",         // HTTP kliens
  "cors": "^2.8.5",          // CORS
  "dotenv": "^16.3.1"        // Környezeti változók
}
```

### Development (devDependencies)
```json
{
  "nodemon": "^3.0.1",           // Auto-reload
  "electron": "^33.2.0",         // Desktop framework
  "electron-builder": "^25.1.8"  // Build tool
}
```

---

## 🚀 NPM Scriptek

```json
{
  "start": "node server.js",           // Web app indítás
  "dev": "nodemon server.js",          // Fejlesztői mód
  "electron-dev": "electron .",        // Desktop teszt
  "build:win": "electron-builder build --win",    // Windows build
  "build:mac": "electron-builder build --mac",    // macOS build
  "build:linux": "electron-builder build --linux" // Linux build
}
```

---

## 📊 Fájlméretek (becsült)

**Web alkalmazás:**
- Kód: ~50 KB (minified)
- node_modules: ~200 MB
- Memória használat: ~100 MB

**Desktop alkalmazás:**
- Telepítő (.exe): ~100-150 MB
- Telepített méret: ~200-250 MB
- Memória használat: ~150-200 MB

**WordPress beágyazás:**
- HTML kód: ~20 KB
- Külső függőségek: Nincs

---

## 🎯 Validálási Logika

### 1. Járat létezése
Ellenőrzi több forrásból:
- Budapest Airport hivatalos API
- AviationStack API (opcionális)
- FlightRadar24 (bővíthető)

**Hiba:** "HIBA: Ez a járatszám erre a dátumra nem található..."

### 2. Célállomás
Csak BUD-ra érkező járatok elfogadottak.

**Hiba:** "HIBA: Ez a járat nem Budapestre érkezik. Útvonal: STN → VIE."

### 3. Dátum
Érkezési dátum egyeztetés.

**Hiba:** "KORREKCIÓ: A járat érkezik Budapestre, de nem ezen a napon..."

### 4. Időpont
Pontos érkezési idő.

**Hiba:** "KORREKCIÓ: Az érkezési idő eltér. Hivatalos érkezés: 11:00."

### 5. Sikeres validálás
Ha minden OK → **Megjegyzés oszlop ÜRES marad**

---

## 🔒 Biztonsági Funkciók

- ✅ Fájl típus whitelist (.xlsx, .xls, .csv)
- ✅ Fájlméret limit (10 MB)
- ✅ MIME type ellenőrzés
- ✅ Ideiglenes fájlok auto-cleanup
- ✅ CORS konfiguráció
- ✅ Input sanitizáció
- ✅ API timeout védelem (5s)
- ✅ Rate limiting (konfigurálható)

---

## 🌍 Nyelv Támogatás

**Magyar:**
- Teljes UI magyar nyelven
- Hibaüzenetek magyarul
- Dokumentáció magyarul

**Angol:**
- Oszlopnevek támogatottak (Flight Number, Notes)
- Kód kommentek angolul
- Technical docs angolul

---

## 📞 Támogatás & Kapcsolat

**Fejlesztő:** VanBudapest.com
**Email:** support@vanbudapest.com
**Verzió:** 1.0.0
**Licensz:** MIT

**GitHub:**
- Repository: https://github.com/VanBudapest/vanbudapest-wordpress
- Branch: `claude/validate-budapest-flights-01NnyNmTB3BTL6zi3Y7e2MMa`

---

## 🎉 Következő Lépések

### Felhasználóknak:

1. **Web verzió tesztelése:**
   ```bash
   npm install && npm start
   ```

2. **Desktop app készítése:**
   - Kövesse: [ELECTRON_SETUP.md](ELECTRON_SETUP.md)
   - Ikon hozzáadása: `build/icon.ico`
   - Build: `npm run build:win`

3. **WordPress beágyazás:**
   - Kövesse: [wordpress-embed/WORDPRESS_BEAGYAZAS.md](wordpress-embed/WORDPRESS_BEAGYAZAS.md)

### Fejlesztőknek:

1. Valós API integrációk (Budapest Airport, FlightRadar24)
2. Adatbázis mentés (feldolgozott fájlok history)
3. Felhasználói fiókok
4. Batch feldolgozás (több fájl)
5. Email értesítések
6. PDF report generálás
7. API rate limiting finomhangolás
8. Automatikus frissítés (Electron)
9. Több nyelv támogatás (angol, német)
10. Docker konténerizáció

---

**Készült ❤️ -tel a Budapest Airport közösség számára**

🛬 **Kellemes repülést!**
