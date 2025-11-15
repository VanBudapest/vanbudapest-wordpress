# 🛬 BUD Érkező Járatszám Ellenőrző

**Budapest Liszt Ferenc Nemzetközi Repülőtér (BUD) érkezési járatok automatikus validálása Excel fájlokból**

## 📋 Áttekintés

Ez az alkalmazás automatikusan ellenőrzi a Budapestre (BUD) érkező repülőjáratok adatait Excel/CSV táblázatokból. A rendszer több hivatalos forrásból gyűjt adatokat, és a hibákat kizárólag a **Megjegyzés** oszlopban rögzíti, miközben az eredeti fájl formázását és struktúráját 100%-osan megőrzi.

### ✨ Főbb jellemzők

- ✅ **Excel formátum megőrzése**: Az eredeti fájl teljes struktúrája, formázása, színezése változatlan marad
- ✅ **Csak Megjegyzés módosítása**: Kizárólag a "Megjegyzés" vagy "Notes" oszlopot írja felül
- ✅ **Több forrás ellenőrzés**: Budapest Airport, AviationStack, FlightRadar24 adatok
- ✅ **Automatikus validálás**: Létezés, célállomás, dátum, időpont ellenőrzés
- ✅ **Modern web UI**: Drag & drop fájl feltöltés, valós idejű progress
- ✅ **Gyors feldolgozás**: Párhuzamos járat-ellenőrzés
- 🖥️ **Desktop alkalmazás**: Electron-alapú Windows/Mac/Linux telepíthető verzió
- 🌐 **WordPress integráció**: Beágyazható HTML verzió

### 📦 Elérhető verziók

1. **Web alkalmazás** - Node.js szerver + böngésző
2. **Desktop alkalmazás** - Telepíthető Windows .exe (Electron)
3. **WordPress beágyazás** - Standalone HTML verzió

---

## 🚀 Gyors kezdés

### Előfeltételek

- **Node.js** >= 16.x
- **npm** >= 8.x

### Telepítés

```bash
cd budapest-flight-validator

# Függőségek telepítése
npm install

# .env fájl létrehozása (opcionális)
cp .env.example .env

# Szerver indítása
npm start
```

Az alkalmazás elérhető: **http://localhost:3000**

### Fejlesztői mód (auto-reload)

```bash
npm run dev
```

---

## 📂 Projekt struktúra

```
budapest-flight-validator/
├── public/                    # Frontend fájlok
│   ├── index.html            # Főoldal
│   ├── style.css             # Modern CSS styling
│   └── app.js                # Frontend logika
├── src/                       # Backend modulok
│   ├── excelProcessor.js     # Excel fájl feldolgozás
│   └── flightValidator.js    # Járat validáció logika
├── uploads/                   # Ideiglenes feltöltések
├── server.js                  # Express szerver
├── package.json              # Függőségek
├── .env.example              # Környezeti változók sablon
└── README.md                 # Ez a fájl
```

---

## 📊 Excel fájl formátum

### Kötelező oszlopok

Az Excel/CSV fájlnak tartalmaznia kell az alábbi oszlopokat (a sorrend tetszőleges):

| Oszlop neve (magyar) | Oszlop neve (angol) | Kötelező? | Példa érték |
|---------------------|---------------------|-----------|-------------|
| Járatszám           | Flight Number       | ✅ Igen    | FR8025      |
| Dátum               | Date                | ✅ Igen    | 2025-11-15  |
| Idő/Időpont         | Time                | ⚠️ Opcionális | 10:30    |
| Megjegyzés          | Notes               | ✅ Igen (üres) | -        |

### Példa táblázat

```csv
Járatszám,Dátum,Idő,Megjegyzés
FR8025,2025-11-15,10:30,
W63701,2025-11-15,11:45,
LH1345,2025-11-15,14:20,
OS711,2025-11-15,09:15,
```

### Támogatott fájl formátumok

- `.xlsx` - Excel 2007+ (ajánlott)
- `.xls` - Excel régebbi formátum
- `.csv` - CSV (vesszővel elválasztott)

**Maximum fájlméret:** 10 MB

---

## 🔍 Validálási logika

A rendszer minden járatot az alábbi sorrendben ellenőriz:

### 1️⃣ Járat létezése

**Ellenőrzés:** Létezik-e a járatszám az adott dátumra?

**Hiba esetén:**
```
HIBA: Ez a járatszám erre a dátumra nem található a hivatalos forrásokban.
```

### 2️⃣ Célállomás ellenőrzés

**Ellenőrzés:** A járat Budapestre (BUD) érkezik-e?

**Hiba esetén:**
```
HIBA: Ez a járat nem Budapestre érkezik. Útvonal: STN → VIE.
```

### 3️⃣ Dátum validálás

**Ellenőrzés:** A járat az adott napon érkezik-e BUD-ra?

**Hiba esetén:**
```
KORREKCIÓ: A járat érkezik Budapestre, de nem ezen a napon. Hivatalos érkezés: 2025-11-16 10:30.
```

### 4️⃣ Időpont validálás

**Ellenőrzés:** Az érkezési időpont megegyezik-e?

**Hiba esetén:**
```
KORREKCIÓ: Az érkezési idő eltér. Hivatalos érkezés: 11:00.
```

### 5️⃣ Sikeres validálás

Ha minden adat helyes → **A Megjegyzés oszlop ÜRES marad**

---

## 🌐 Használat - Web felület

### 1. Nyissa meg a böngészőt

```
http://localhost:3000
```

### 2. Töltsön fel egy Excel fájlt

**Két módszer:**
- Kattintson a "Fájl kiválasztása" gombra
- Húzza a fájlt a feltöltő területre (drag & drop)

### 3. Indítsa el az ellenőrzést

Kattintson a **"🔍 Járatok ellenőrzése"** gombra

### 4. Töltse le az eredményt

A módosított Excel fájl automatikusan letöltődik:
- Fájlnév: `budapest-flights-validated.xlsx`
- Csak a Megjegyzés oszlop módosul
- Minden más változatlan marad

---

## 🛠️ API használat

### Endpoint: `POST /api/validate`

**Fájl feltöltés multipart/form-data-val**

```javascript
const formData = new FormData();
formData.append('excelFile', fileInput.files[0]);

const response = await fetch('http://localhost:3000/api/validate', {
  method: 'POST',
  body: formData
});

const blob = await response.blob();
// Fájl letöltése...
```

### Példa cURL-lel

```bash
curl -X POST http://localhost:3000/api/validate \
  -F "excelFile=@flights.xlsx" \
  --output validated-flights.xlsx
```

### Válasz formátum

**Sikeres:**
- HTTP 200
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Body: Módosított Excel fájl

**Hiba esetén:**
```json
{
  "success": false,
  "error": "Nem található 'Járatszám' vagy 'Flight Number' oszlop."
}
```

---

## ⚙️ Konfiguráció

### Környezeti változók (.env)

```env
PORT=3000

# API kulcsok (opcionális - az app működik nélkülük is)
AVIATIONSTACK_API_KEY=your_api_key_here
```

### API kulcsok beszerzése (opcionális)

Az alkalmazás **működik API kulcsok nélkül is** publikus adatok alapján. Jobb pontossághoz használhat:

1. **AviationStack** (ingyenes tier):
   - Regisztráció: https://aviationstack.com/
   - 500 kérés/hó ingyenesen

2. **FlightRadar24** (prémium):
   - API hozzáférés: https://www.flightradar24.com/premium

---

## 🧪 Tesztelés

### Sablon fájl letöltése

A webes felületen kattintson a **"📥 Sablon letöltése"** gombra, vagy használja a beépített sablon generátort:

```bash
# A szerver fut, nyissa meg:
http://localhost:3000
# Kattintson: "Sablon letöltése"
```

### Példa tesztfájl

```csv
Járatszám,Dátum,Idő,Megjegyzés
FR8025,2025-11-15,10:30,
FR9999,2025-11-15,10:30,
LH1345,2025-11-16,14:20,
OS711,2025-11-15,09:00,
```

**Várható eredmény:**
- FR8025: Üres (helyes)
- FR9999: "HIBA: Ez a járatszám erre a dátumra nem található..."
- LH1345: "KORREKCIÓ: A járat érkezik Budapestre, de nem ezen a napon..."
- OS711: "KORREKCIÓ: Az érkezési idő eltér..."

---

## 🔒 Biztonsági funkciók

- ✅ Fájl típus ellenőrzés (csak Excel/CSV)
- ✅ Fájlméret limit (10 MB)
- ✅ Ideiglenes fájlok automatikus törlése
- ✅ CORS védelem
- ✅ Input sanitizáció
- ✅ Timeout védelem API hívásoknál

---

## 🖥️ Desktop Alkalmazás (Electron)

### Windows Telepíthető .EXE Készítése

**Részletes útmutató:** [ELECTRON_SETUP.md](ELECTRON_SETUP.md)

#### Gyors lépések:

```bash
# 1. Függőségek telepítése
npm install

# 2. Ikonok hozzáadása
# Tegye a build/icon.ico fájlt a build/ mappába

# 3. Fejlesztői teszt
npm run electron-dev

# 4. Windows telepítő készítése
npm run build:win
```

**Eredmény:**
- `dist/BUD Flight Validator Setup 1.0.0.exe` - Telepítő
- Natív Windows alkalmazás
- Start menü és Desktop ikon
- Nincs szükség böngészőre

**Más platformok:**

```bash
npm run build:mac    # macOS .dmg
npm run build:linux  # Linux AppImage
```

### Electron Előnyök

- ✅ Telepíthető Windows/Mac/Linux alkalmazás
- ✅ Nincs szükség böngészőre
- ✅ Natív ablak kezelés
- ✅ Automatikus frissítés (konfigurálható)
- ✅ VanBudapest.com ikon az alkalmazásban
- ✅ Nincs szükség Node.js ismerethez a felhasználóknak

---

## 🌐 WordPress Integráció

### Beágyazás WordPress Oldalba

**Részletes útmutató:** [wordpress-embed/WORDPRESS_BEAGYAZAS.md](wordpress-embed/WORDPRESS_BEAGYAZAS.md)

#### 1. módszer: Iframe (Legegyszerűbb)

```html
<iframe
    src="http://your-server.com:3000"
    width="100%"
    height="1200px"
    frameborder="0">
</iframe>
```

#### 2. módszer: Standalone HTML

A `wordpress-embed/bud-flight-validator-embed.html` fájlt:

1. Másolja WordPress Custom HTML blockba
2. Módosítsa az API URL-t:
   ```javascript
   const BUD_API_URL = 'https://vanbudapest.com/api/validate';
   ```
3. Publikálja az oldalt

#### 3. módszer: Shortcode

```php
// functions.php
function bud_validator_shortcode() {
    include 'bud-flight-validator-embed.html';
}
add_shortcode('bud_validator', 'bud_validator_shortcode');
```

Használat bármely WordPress oldalon:
```
[bud_validator]
```

### WordPress Előnyök

- ✅ Teljes integráció a meglévő weboldallal
- ✅ Ugyanaz a design nyelv
- ✅ SEO optimalizált
- ✅ Nincs külön domain szükséges
- ✅ WordPress felhasználók számára elérhető

---

## 🐛 Hibaelhárítás

### "Cannot find module" hiba

```bash
# Törölje és telepítse újra a függőségeket
rm -rf node_modules package-lock.json
npm install
```

### "Port already in use" hiba

```bash
# Változtassa meg a portot a .env fájlban:
PORT=3001
```

### Excel fájl nem nyílik meg

- Ellenőrizze, hogy a fájl valóban .xlsx/.xls formátumú
- Próbálja meg újra menteni az Excel-ben "Excel Workbook (.xlsx)" néven

### "Nem található oszlop" hiba

Győződjön meg róla, hogy a fejléc (1. sor) tartalmazza:
- "Járatszám" VAGY "Flight Number"
- "Megjegyzés" VAGY "Notes"

---

## 📦 Függőségek

| Csomag | Verzió | Leírás |
|--------|--------|--------|
| express | ^4.18.2 | Web szerver framework |
| multer | ^1.4.5 | Fájl feltöltés kezelése |
| exceljs | ^4.4.0 | Excel fájl olvasás/írás |
| axios | ^1.6.0 | HTTP kliens API hívásokhoz |
| cors | ^2.8.5 | CORS middleware |
| dotenv | ^16.3.1 | Környezeti változók |

---

## 🤝 Közreműködés

### Új funkció vagy hibajavítás

1. Fork a repository
2. Hozzon létre feature branch-et: `git checkout -b feature/UjFunkció`
3. Commit: `git commit -m 'Új funkció hozzáadása'`
4. Push: `git push origin feature/UjFunkció`
5. Nyisson Pull Request-et

---

## 📄 Licenc

MIT License - lásd a [LICENSE](LICENSE) fájlt részletekért.

---

## 📞 Támogatás

**Kérdések vagy problémák esetén:**
- GitHub Issues: [Új issue nyitása](https://github.com/your-repo/issues)
- Email: support@example.com

---

## 🎯 Roadmap

### Tervezett funkciók:

- [ ] Több munkalap támogatása
- [ ] Batch feldolgozás (több fájl egyszerre)
- [ ] Részletes statisztikák (sikeres/sikertelen járatok)
- [ ] Export PDF jelentésként
- [ ] Email értesítések
- [ ] Felhasználói fiókok és mentett ellenőrzések
- [ ] API rate limiting
- [ ] Docker konténerizáció

---

## 🙏 Köszönetnyilvánítás

- **Budapest Airport** - Repülési adatok forrása
- **AviationStack** - API szolgáltatás
- **ExcelJS** - Excel feldolgozás library

---

**Készítve ❤️-tel a Budapest Airport közösség számára**

🛬 **Kellemes repülést!**
