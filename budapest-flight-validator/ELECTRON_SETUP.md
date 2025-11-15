# 🖥️ Electron Desktop Alkalmazás - Telepítési Útmutató

## Windows Telepíthető .EXE Készítése

Ez az útmutató lépésről-lépésre bemutatja, hogyan készítsen telepíthető Windows alkalmazást a BUD Flight Validator-ból.

---

## ⚡ Gyors Áttekintés

A projekt már **teljes mértékben konfigurálva van** az Electron desktop alkalmazáshoz:

✅ `electron-main.js` - Electron fő folyamat
✅ `server.js` - Módosítva Electron támogatással
✅ `package.json` - Build scriptek konfigurálva
✅ `build/` könyvtár - Ikonok helye

**Egyedül az ikonokat kell hozzáadni!**

---

## 📋 Lépések

### 1. Függőségek Telepítése

```bash
cd budapest-flight-validator
npm install
```

Ez telepíti:
- Electron v33.2.0
- electron-builder v25.1.8
- Összes többi függőség

### 2. Ikonok Előkészítése

#### A. Kiindulás: VanBudapest.com logó

Használja a meglévő **512×512 PNG** logót (QR kódos verzió).

#### B. Ikon konvertálás

**Windows .ico generálása:**

1. Látogasson el: https://icoconvert.com/
2. Töltse fel a 512×512 PNG logót
3. Válassza ki a méreteket:
   - ☑️ 256x256
   - ☑️ 128x128
   - ☑️ 64x64
   - ☑️ 48x48
   - ☑️ 32x32
   - ☑️ 16x16
4. Kattintson: "Convert ICO"
5. Mentse el: `icon.ico`

**macOS .icns generálása (opcionális):**

1. Látogasson el: https://cloudconvert.com/png-to-icns
2. Töltse fel a 512×512 PNG logót
3. Mentse el: `icon.icns`

**Linux .png (opcionális):**

Egyszerűen másolja át a 512×512 PNG-t `icon.png` néven.

#### C. Ikonok elhelyezése

Másolja a generált fájlokat a `build/` mappába:

```
budapest-flight-validator/
└── build/
    ├── icon.ico     ← Windows (KÖTELEZŐ!)
    ├── icon.icns    ← macOS (opcionális)
    └── icon.png     ← Linux (opcionális)
```

**Windows telepítőhöz CSAK az `icon.ico` szükséges!**

### 3. Fejlesztői Teszt (Ablakos Mód)

Indítsa el az alkalmazást development módban:

```bash
npm run electron-dev
```

**Mit vár el:**
- ✅ Felugrik egy natív Windows ablak
- ✅ Címe: "BUD Flight Validator – VanBudapest.com"
- ✅ Benne ugyanaz a felület, mint a böngészőben
- ✅ Drag & drop Excel feltöltés működik
- ✅ Járatok ellenőrzése működik
- ✅ Eredmény letöltés működik

**Ha hiba van:**
- Ellenőrizze, hogy a `build/icon.ico` létezik-e
- Nézze meg a konzol output-ot hibákért

### 4. Windows Telepítő Készítése

Ha a fejlesztői mód működik, készítheti a végleges telepítőt:

```bash
npm run build:win
```

**Ez:**
1. Összecsomagolja az alkalmazást
2. Létrehozza a Windows telepítőt (NSIS)
3. Elmenti a `dist/` mappába

**Folyamat időtartama:** 2-5 perc (első alkalommal)

**Kimenet:**

```
budapest-flight-validator/
└── dist/
    ├── BUD Flight Validator Setup 1.0.0.exe  ← Telepítő
    └── win-unpacked/                         ← Portable verzió
```

### 5. Telepítő Tesztelése

1. Lépjen be a `dist/` mappába
2. Dupla katt: `BUD Flight Validator Setup 1.0.0.exe`
3. Telepítő fut:
   - Válassza ki a telepítési mappát
   - Kattintson "Install"
4. Telepítés után:
   - **Start menüben** megjelenik: "BUD Flight Validator"
   - **Desktop ikonnal** (VanBudapest logó)
   - **Tálcán** a logó ikon

### 6. Alkalmazás Használata

**Indítás:**
- Start menü → BUD Flight Validator
- Desktop ikon
- Keresés: "BUD Flight"

**Működés:**
- Natív Windows alkalmazásként viselkedik
- Nincs szükség böngészőre
- Nincs szükség külön Node.js telepítésre
- Minden be van csomagolva

**Excel feldolgozás:**
1. Húzza be az Excel fájlt az ablakba
2. "Járatok ellenőrzése" gomb
3. Validált fájl automatikus letöltés
4. Bezárhatja az alkalmazást

---

## 🛠️ További Build Opciók

### macOS Telepítő (ha van macOS gépje)

```bash
npm run build:mac
```

Kimenet: `dist/BUD Flight Validator-1.0.0.dmg`

### Linux AppImage

```bash
npm run build:linux
```

Kimenet: `dist/BUD Flight Validator-1.0.0.AppImage`

### Portable verzió (telepítő nélkül)

A `dist/win-unpacked/` mappában található egy portable verzió:

- Nincs telepítés
- Egyszerűen másolja bárhova
- Futtatja: `BUD Flight Validator.exe`

---

## 📦 Telepítő Terjesztése

### A. Telepítő megosztása

1. **Feltöltés:**
   - Google Drive / Dropbox
   - Saját weboldal
   - GitHub Releases

2. **Letöltési link megosztása:**
   ```
   Töltse le: BUD Flight Validator Setup 1.0.0.exe (XX MB)
   ```

3. **Telepítés:**
   - Felhasználók egyszerűen futtatják
   - Nincs szükség Node.js tudásra

### B. Verziószám frissítése

A `package.json`-ben:

```json
{
  "version": "1.0.0"  ← Növelje: "1.0.1", "1.1.0", "2.0.0"
}
```

Majd újra build: `npm run build:win`

### C. Automatikus frissítés (haladó)

Használja az `electron-updater` csomagot:
- https://www.electron.build/auto-update

---

## ⚙️ Testreszabás

### Ablak beállítások

`electron-main.js` fájlban:

```javascript
mainWindow = new BrowserWindow({
  width: 1200,        // ← Szélesség
  height: 800,        // ← Magasság
  minWidth: 1000,     // ← Min szélesség
  minHeight: 700,     // ← Min magasság
  backgroundColor: '#667eea',  // ← Háttér szín
  title: 'BUD Flight Validator – VanBudapest.com',  // ← Címsor
  autoHideMenuBar: true,  // ← Menüsor elrejtése
  // ...
});
```

### Fejlesztői eszközök engedélyezése

`electron-main.js`-ben:

```javascript
// Fejlesztési módban:
mainWindow.webContents.openDevTools();
```

### Splash screen hozzáadása

További információ:
- https://www.electronjs.org/docs/latest/tutorial/tutorial-first-app

---

## 🐛 Hibaelhárítás

### "npm ERR! Electron download failed"

**Megoldás:**
```bash
npm cache clean --force
npm install
```

### "Build failed: icon.ico not found"

**Megoldás:**
- Ellenőrizze: `build/icon.ico` létezik-e
- Fájlnév pontosan `icon.ico` (kisbetűvel!)

### "NSIS Error: Can't load installer"

**Megoldás:**
- Windows Defender / Antivirus kikapcsolása ideiglenesen
- Újra build: `npm run build:win`

### Telepítő nem indul "SmartScreen" miatt

**Ez normális!** A Windows SmartScreen blokkolja az ismeretlen kiadókat.

**Megoldás:**
1. Kattintson: "More info"
2. Kattintson: "Run anyway"

**Professzionális megoldás:**
- Code Signing tanúsítvány vásárlása (Digicert, Sectigo)
- Aláírt telepítő → nincs SmartScreen figyelmeztetés

### Alkalmazás lassan indul

**Normális!** Az első indítás 3-5 másodperc lehet.

**Optimalizálás:**
- V8 snapshot használata
- Lazy loading moduloknak

---

## 📊 Build Statisztikák

**Várt fájlméretek:**

- Telepítő (.exe): ~100-150 MB
- Telepített alkalmazás: ~200-250 MB
- Portable verzió: ~180-220 MB

**Miért ilyen nagy?**
- Teljes Node.js runtime (~50 MB)
- Chromium rendering engine (~100 MB)
- Alkalmazás kódja (~50 MB)
- Node modules (~50 MB)

**Ez normális és nem optimalizálható jelentősen.**

---

## 🎯 Következő lépések

1. ✅ Készítse el az `icon.ico` fájlt
2. ✅ Tesztelje: `npm run electron-dev`
3. ✅ Build: `npm run build:win`
4. ✅ Telepítse és tesztelje az .exe-t
5. ✅ Ossza meg a felhasználókkal!

---

## 📞 Támogatás

**Electron dokumentáció:**
- https://www.electronjs.org/docs/latest/

**electron-builder dokumentáció:**
- https://www.electron.build/

**Kérdések:**
- support@vanbudapest.com

---

**Elkészítette:** VanBudapest.com
**Verzió:** 1.0.0
**Utolsó frissítés:** 2025-11-15
