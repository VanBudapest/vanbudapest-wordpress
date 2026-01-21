# VanBudapest Mobil Alkalmazás

React Native (Expo) alapú mobil alkalmazás a vanbudapest.com weboldalhoz.

## Funkciók

- **Tartalom böngészés**: WordPress bejegyzések és oldalak megjelenítése
- **Keresés**: Bejegyzések keresése a tartalomban
- **Foglalás**: Időpont foglalási rendszer szolgáltatásokhoz
- **Rólunk**: Kapcsolati információk és social media linkek

## Technológiák

- React Native 0.73
- Expo SDK 50
- TypeScript
- React Navigation 6
- Axios (API kommunikáció)
- date-fns (dátum kezelés)

## Telepítés

```bash
# Navigálj az app mappába
cd vanbudapest-app

# Telepítsd a függőségeket
npm install

# Indítsd el a fejlesztői szervert
npm start
```

## Futtatás

```bash
# iOS szimulátoron
npm run ios

# Android emulátoron
npm run android

# Web böngészőben
npm run web
```

## Projekt struktúra

```
vanbudapest-app/
├── App.tsx                 # Belépési pont
├── src/
│   ├── components/         # Újrahasználható komponensek
│   │   ├── PostCard.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── ErrorMessage.tsx
│   │   └── SearchBar.tsx
│   ├── screens/            # Képernyők
│   │   ├── HomeScreen.tsx
│   │   ├── PostDetailScreen.tsx
│   │   ├── SearchScreen.tsx
│   │   ├── BookingScreen.tsx
│   │   └── AboutScreen.tsx
│   ├── navigation/         # Navigáció
│   │   └── AppNavigator.tsx
│   ├── services/           # API szolgáltatások
│   │   ├── wordpress.ts
│   │   └── booking.ts
│   ├── hooks/              # React hooks
│   │   └── useWordPress.ts
│   ├── types/              # TypeScript típusok
│   │   └── index.ts
│   └── utils/              # Segédfüggvények
│       └── helpers.ts
└── assets/                 # Képek, ikonok
```

## WordPress API

Az alkalmazás a WordPress.com REST API-t használja:
- Alap URL: `https://public-api.wordpress.com/rest/v1.1/sites/vanbudapest.com`
- Dokumentáció: https://developer.wordpress.com/docs/api/

### Használt végpontok

- `GET /posts` - Bejegyzések listázása
- `GET /posts/{id}` - Egyedi bejegyzés
- `GET /pages` - Oldalak listázása
- `GET /categories` - Kategóriák

## Build (produkció)

```bash
# EAS Build telepítése
npm install -g eas-cli

# Android APK/AAB
eas build --platform android

# iOS IPA
eas build --platform ios
```

## Testreszabás

### Színek módosítása

Szerkesztd a `src/utils/helpers.ts` fájlt:

```typescript
export const colors = {
  primary: '#2E7D32',       // Fő szín
  primaryDark: '#1B5E20',
  primaryLight: '#4CAF50',
  // ...
};
```

### Szolgáltatások módosítása

Szerkesztd a `src/services/booking.ts` fájlt:

```typescript
export const SERVICES = [
  { id: 'massage', name: 'Masszázs', duration: 60, price: '15.000 Ft' },
  // Adj hozzá új szolgáltatásokat...
];
```

## Licensz

MIT
