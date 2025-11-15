# 🚀 Gyors Indítás - BUD Járat Ellenőrző

## 📦 Válassza ki a megfelelő verziót!

### 1️⃣ Web Alkalmazás (Böngészős)
- Lokális vagy szerver futtatás
- Leggyorsabb kezdés
- **Ideális:** Fejlesztéshez, teszteléshez

### 2️⃣ Desktop Alkalmazás (Windows/Mac/Linux)
- Telepíthető .exe/.dmg
- Nincs szükség böngészőre
- **Ideális:** Végfelhasználóknak, irodai használatra

### 3️⃣ WordPress Beágyazás
- Integrált a meglévő weboldallal
- **Ideális:** Weboldal látogatóknak

---

## 🌐 Web Alkalmazás - 3 lépésben használatra kész!

### 1️⃣ Telepítés

```bash
cd budapest-flight-validator
npm install
```

### 2️⃣ Indítás

```bash
npm start
```

### 3️⃣ Használat

Nyissa meg böngészőjében:

```
http://localhost:3000
```

---

## 📋 Első használat

### Excel fájl előkészítése

Hozzon létre egy Excel táblázatot az alábbi oszlopokkal:

| Járatszám | Dátum      | Idő   | Megjegyzés |
|-----------|------------|-------|------------|
| FR8025    | 2025-11-15 | 10:30 |            |
| W63701    | 2025-11-15 | 11:45 |            |
| LH1345    | 2025-11-15 | 14:20 |            |

**FONTOS:**
- A "Megjegyzés" vagy "Notes" oszlopot hagyja üresen!
- A rendszer csak ezt az oszlopot fogja módosítani

### Fájl feltöltése

1. Húzza a fájlt a feltöltő területre (drag & drop)
   VAGY
2. Kattintson a "Fájl kiválasztása" gombra

### Ellenőrzés indítása

1. Kattintson: **"🔍 Járatok ellenőrzése"**
2. Várjon pár másodpercet
3. A módosított fájl automatikusan letöltődik!

---

## ✅ Sikeres ellenőrzés jele

A **Megjegyzés** oszlopban csak hibás járatok esetén jelenik meg szöveg:

- **Üres cella** = Minden adat helyes ✅
- **Szöveg a cellában** = Hiba vagy eltérés ⚠️

---

## 🎯 Példa eredmény

**Eredeti táblázat:**

| Járatszám | Dátum      | Idő   | Megjegyzés |
|-----------|------------|-------|------------|
| FR8025    | 2025-11-15 | 10:30 |            |
| FR9999    | 2025-11-15 | 10:30 |            |
| LH1345    | 2025-11-16 | 14:20 |            |

**Ellenőrzés után:**

| Járatszám | Dátum      | Idő   | Megjegyzés |
|-----------|------------|-------|------------|
| FR8025    | 2025-11-15 | 10:30 | *(üres)*   |
| FR9999    | 2025-11-15 | 10:30 | HIBA: Ez a járatszám erre a dátumra nem található... |
| LH1345    | 2025-11-16 | 14:20 | KORREKCIÓ: A járat érkezik Budapestre, de... |

---

## 🛠️ Hibaelhárítás

### Port foglalt?

```bash
# Változtassa meg a portot:
PORT=3001 npm start
```

### Telepítési hiba?

```bash
rm -rf node_modules
npm install
```

### További segítség

Olvassa el a részletes [README.md](README.md) dokumentációt!

---

---

## 🖥️ Desktop Alkalmazás - Windows Telepítő

### 1️⃣ Telepítés

```bash
cd budapest-flight-validator
npm install
```

### 2️⃣ Ikon hozzáadása

1. VanBudapest.com logó (512×512 PNG) konvertálása .ico-ba
2. Online konverter: https://icoconvert.com/
3. Mentés: `build/icon.ico`

### 3️⃣ Fejlesztői teszt

```bash
npm run electron-dev
```

Felugrik egy natív Windows ablak az alkalmazással!

### 4️⃣ Telepítő készítése

```bash
npm run build:win
```

Eredmény: `dist/BUD Flight Validator Setup 1.0.0.exe`

### 📘 Részletes útmutató

Lásd: [ELECTRON_SETUP.md](ELECTRON_SETUP.md)

---

## 🌐 WordPress Beágyazás

### 1️⃣ HTML kód másolása

Nyissa meg: `wordpress-embed/bud-flight-validator-embed.html`

### 2️⃣ WordPress Admin

1. Pages → Add New
2. Add Block → Custom HTML
3. Paste HTML code

### 3️⃣ API URL módosítása

Keresse meg a kódban:

```javascript
const BUD_API_URL = 'http://localhost:3000/api/validate';
```

Változtassa meg:

```javascript
const BUD_API_URL = 'https://vanbudapest.com/api/validate';
```

### 4️⃣ Publish

Kész! Az alkalmazás beágyazva a WordPress oldalon.

### 📘 Részletes útmutató

Lásd: [wordpress-embed/WORDPRESS_BEAGYAZAS.md](wordpress-embed/WORDPRESS_BEAGYAZAS.md)

---

**Kellemes használatot! 🛬**
