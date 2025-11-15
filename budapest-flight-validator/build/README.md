# Build Resources - Ikonok

Ez a mappa tartalmazza az alkalmazás ikonjait különböző platformokhoz.

## Szükséges fájlok

### Windows
- **icon.ico** - Windows ikon (256x256, 128x128, 64x64, 48x48, 32x32, 16x16)

### macOS
- **icon.icns** - macOS ikon csomag (1024x1024, 512x512, 256x256, 128x128, 64x64, 32x32, 16x16)

### Linux
- **icon.png** - Linux ikon (512x512 PNG)

## Ikon készítése

### 1. Kiindulás: VanBudapest.com logó
Használja a meglévő 512×512 PNG logót (QR kódos verzió).

### 2. Online konverterek

**Windows .ico készítése:**
- https://icoconvert.com/
- https://convertio.co/png-ico/
- Töltse fel a 512×512 PNG-t
- Válassza ki a méreteket: 256, 128, 64, 48, 32, 16
- Mentse el: `icon.ico`

**macOS .icns készítése:**
- https://cloudconvert.com/png-to-icns
- https://iconverticons.com/online/
- Töltse fel a 512×512 PNG-t
- Mentse el: `icon.icns`

**Linux .png:**
- Egyszerűen nevezze át a 512×512 PNG-t: `icon.png`

### 3. Másolás

Másolja a generált fájlokat ebbe a mappába:
```
budapest-flight-validator/build/
├── icon.ico     ← Windows
├── icon.icns    ← macOS
└── icon.png     ← Linux
```

## Tesztelés

A build után az ikon jelenik meg:
- Windows: Start menü, Desktop parancsikon, tálca
- macOS: Applications mappa, Dock
- Linux: Application launcher

## Troubleshooting

Ha az ikon nem jelenik meg:
1. Ellenőrizze a fájlneveket (kis/nagybetű!)
2. Ellenőrizze a fájlméreteket (ne legyenek túl nagyok)
3. Újra build-elje az alkalmazást: `npm run build:win`
