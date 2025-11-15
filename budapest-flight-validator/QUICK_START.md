# 🚀 Gyors Indítás - BUD Járat Ellenőrző

## 3 lépésben használatra kész!

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

**Kellemes használatot! 🛬**
