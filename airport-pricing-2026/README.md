# Airport Transfer Pricing — új árkártyák (A) + ármátrix (D)

**Oldal:** `/budapest-airport-pick-up-transfer-price/` · Page ID **1351**
**Forrás:** 2026-08-21 audit (`VBauditairportpricing20260821`) + prototípusok (`vb-arkartya-prototipusok`)
**Készült:** 2026-08-22

Tomi választása: **A koncepció (Dark Editorial) felülre, a kártyák helyére** + **D koncepció (ármátrix) alá, a táblázat helyére**, a D-n egy módosítással.

---

## Fájlok

| Fájl | Mit cserél | Hova megy |
|---|---|---|
| `blocks/block-01-airport-pricing-cards-A.html` | **#1** wp:html blokk („Airport Pricing Cards – v2.0 CHRONO-SAFE”) | Gutenberg → az a Custom HTML blokk |
| `blocks/block-02-price-matrix-D.html` | **#2** wp:html blokk (`.vb-pricing-section` – 7 oszlopos táblázat) | Gutenberg → az a Custom HTML blokk |
| `blocks/block-06-faq-selector-fix.md` | #6 szivárgó `h2{}`/`h3{}` — **alkalmazva** | élőben |
| `page-1351-BACKUP-before.txt` | a módosítás előtti nyers tartalom | biztonsági másolat |
| `apply-changes.py` | a teljes transzformáció, assert-ekkel | reprodukálható |
| `preview/airport-pricing-preview.html` | A + D egyben, a WP-környezet szimulálásával | csak előnézet, nem megy fel |

---

## Amit kértél, és amit csináltam

### A koncepció — változatlanul

Ahogy kérted: „ez így, ahogy van, föl is mehet”. A szerkezet, a szövegek, az árak, a képek, a sorrend, az útvonal-váltó, az „Included” sáv — mind a prototípus szerint.

Amit a WordPress miatt **muszáj** volt hozzátenni (megjelenést nem érint):

- a `:root` változók a `.vbp-a` szekcióba kerültek (WP-ben nincs saját `:root`),
- az ikonok `.vbp-a` alá scope-olva,
- full-width a site `.vb-fw` mintája szerint (`100vw` + `calc(50% - 50vw)`),
- a címsorokon explicit `display` — dupla védelem, akkor is állna, ha a #6 szivárgás visszakerülne,
- `srcset` + `sizes` + `width`/`height` minden képen; az első kártyakép `loading="eager" fetchpriority="high"` (audit 10. pont),
- a váltó-script kapott dupla-kötés elleni védelmet (`data-vbp-bound`).

**Két utólagos módosítás Tomi döntése alapján:**

1. **VIE/BTS parkolás (audit 7.6, lezárva).** A prototípus `{{…}}` placeholdere helyére a valós szabály került:
   *„Long-distance rate · tolls & motorway vignettes included · airport parking paid on the spot, at the airport's current local tariff”*
2. **Névegységesítés.** Az A-kártyán is `Luxury Minibus` lett (a `VIP` szó nélkül), alatta változatlanul `Mercedes VIP Sprinter`. Így az A és a D ugyanazt a kategórianevet használja.

### D koncepció — a kért javítással

> „ki kell venni a nevet, csak Luxury minibus, a VIP szót ki kell szedni, mert alatta úgyis ott van, hogy VIP Sprinter”

- Oszlopfej: **`Luxury Minibus VIP` → `Luxury Minibus`**, alatta változatlanul `VIP Sprinter`.
- Ugyanez a mobil kártyán is (hogy ne legyen kétféle név).
- Az elcsúszás ezzel megszűnik: a felirat egy sorba fér, a kép egy vonalba kerül a többivel.

**Plusz egy szerkezeti biztosíték** (láthatatlan, amíg minden felirat egysoros): a jármű-oszlopfejek `vertical-align:top`-ot kaptak. Eddig `vertical-align:bottom` volt, **ez volt az elcsúszás valódi oka** — kétsoros felirat felfelé tolta a képet. Így ha bármikor hosszabb kategórianév kerül be, a képek akkor sem csúsznak el.

Böngészőben mérve, 1440 px-en mind a 6 fejlécképre:

```
imgTop=2324  lines=1  "Business Car"    / "Mercedes E-Class"
imgTop=2324  lines=1  "Premium Van"     / "Mercedes V-Class"
imgTop=2324  lines=1  "Minibus"         / "Mercedes Sprinter"
imgTop=2324  lines=1  "Luxury Car VIP"  / "Mercedes S-Class"
imgTop=2324  lines=1  "Luxury Minibus"  / "VIP Sprinter"
imgTop=2324  lines=1  "Coach Bus"       / "Setra · MAN · Mercedes"
✅ mind a 6 kép azonos vonalon
```

Egyéb D-változtatás:

- a `600x400` képméret **nem létezik** a médiatárban (a prototípus ilyet hivatkozott) — a `srcset` a ténylegesen regisztrált méretekre állt át: `300x200`, `768x512`,
- a mobil (≤900 px) ágból kikerült egy teljesen halott `@media` blokk (a táblázatot amúgy is `display:none` rejti mobilon) — 0 vizuális változás,
- a `Book` gombok elérték a 44 px-es érintési célt (audit 8. pont).

---

## Reszponzív mérés — az audit teszt-mátrixával

Chromium/Playwright, ugyanaz a 15 szélesség, amivel az audit a hibákat kimérte.
Az eredeti oldal: **5/15 FAIL**. Az új blokkok:

```
W     scrollW/innerW   D-tábla scroll   verdict
320   320/320          288/288          PASS
360   360/360          328/328          PASS
390   390/390          358/358          PASS
414   414/414          381/381          PASS
430   430/430          396/396          PASS
480   480/480          442/442          PASS
600   600/600          552/552          PASS
768   768/768          707/707          PASS   ← eddig FAIL (levágott kártya)
775   775/775          713/713          PASS   ← eddig FAIL
900   900/900          828/828          PASS
1024  1024/1024        944/944          PASS   ← eddig FAIL (görgethető tábla)
1280  1280/1280        1200/1200        PASS   ← eddig FAIL
1440  1440/1440        1240/1240        PASS   ← eddig FAIL (6. kártya láthatatlan)
1920  1920/1920        1240/1240        PASS
2560  2560/2560        1240/1240        PASS

ALL PASS (15/15)
```

Sehol nincs oldalszintű vízszintes görgetés, és a D-táblázat sehol nem görgethető vízszintesen (≤900 px-en járműkártyákra esik szét).

---

## ✅ Feltöltve az élő oldalra — 2026-08-22

Az oldal (page 1351) frissítve. A csatorna a **WordPress.com MCP `page-sections.replace`** volt: top-level blokkonkénti, optimista zárolással (`expected_block_hash` + `expected_content_hash`), így a nem érintett blokkok hozzá sem értek.

| Top-level blokk | Mi történt |
|---|---|
| **[0]** `core/group` | Főcím (`vb-page-h2` osztály) + **A kártyák** + **D mátrix** + #3 parkolási szöveg |
| **[1]** `core/columns` | #4 motion-v4: 60 perc, parkolás külön tétel (7 mondat) |
| **[6]** `core/columns` | #6 FAQ: szivárgó szelektorok namespace alá + EN/DE/ES parkolási szövegek |
| [2] [3] [4] [5] [7] | **bájtra változatlan** — ellenőrizve |

Írás utáni ellenőrzés: `_content_warnings: []`, a `<style>` 6 db, `<script>` 2 db (a régi lightbox + az új útvonal-váltó), `<link>` 9 db — mind ép.

### Miért nem az ADMIN_WP MCP-vel ment

Az `ADMIN_WP_WORDPRESS` MCP **olvasása veszteséges**, ezt méréssel igazoltam egy eldobható próbaoldalon (utána törölve):

| Amit írtam | Amit visszaolvastam |
|---|---|
| `<style>…</style>` | tag nélkül, csak a CSS szövege |
| `<script>` / `<link>` | eltűnik |
| `'PROBE\n  LINE-TWO'` | `'PROBEn  LINE-TWO'` |
| `/\d+\.\d+/g` | `/d+.d+/g` — a regex tönkremegy |

Az **írás** viszont hibátlan. Vagyis a hiba az olvasó rétegben van — de emiatt a kiolvasott tartalmat **soha nem szabad visszaírni**. A WordPress.com MCP `pages.get` + `context=edit` adja a hibátlan nyerset (ezzel dolgoztam), a `page-sections.*` pedig blokk-szintű, biztonságos írást.

### Biztonsági másolat

- `page-1351-BACKUP-before.txt` — a teljes nyers tartalom a módosítás **előtt** (hiteles, `context=edit`)
- `page-1351-AFTER-live.txt` — a jelenlegi élő tartalom
- `apply-changes.py` — a transzformáció, tételes `assert`-ekkel (minden csere pontosan 1× illeszkedhet)

Visszaállítás: a backup tartalma visszaírható ugyanezen az úton; a WordPress revíziók is megvannak.

### Két apró, nem funkcionális eltérés a mentés után

1. A **ShortPixel** bővítmény a mentéskor átírta a mobil-kártyák kép-URL-jeit `spcdn.shortpixel.ai/...`-ra — ez a site saját CDN-optimalizálása, az oldal többi képe is így néz ki. Nem hiba, sőt.
2. A WordPress escape-elt két `&` jelet **HTML-kommentben** (`GALLERY 2: Fleet & city vibes` → `&amp;`). Kommentben van, nincs hatása.

**Következő lépés: `seo-deploy` skill** — ShortPixel CDN cache-bump + inkognitós ellenőrzés desktopon és mobilon.

## Az audit többi pontja — mi generálható, mi nem

### ✅ Ez a két blokk megoldotta

| Audit-tétel | Hol |
|---|---|
| #1 kártyarács túlcsordulás (768–891, 1440–1759 px) | A koncepció, 15/15 PASS |
| Hiányzó ikonok (KSES kiszűrte az inline `<svg>`-t) | CSS mask + data-URI, mindkét blokk |
| #2 táblázat vízszintes görgetés ≤1280 px | D koncepció, ≤900 px-en kártyák |
| Parkolási jegyzet 9 px-es betűvel, 6× ismételve | D: egy összevont sor; A: kártyánként olvasható méretben |
| „Swipe to see all vehicles 👆” emoji-hint | megszűnt a régi blokkal együtt |
| Érintési célok < 44 px | gombok `min-height:48px` / `44px` |
| `srcset` + `sizes` + `width`/`height` hiánya | a 12 kártya/mátrix képen kész |
| Első kártyakép `lazy` (LCP) | `eager` + `fetchpriority="high"` |
| Ikon nélküli „3 2 2” (akadálymentesség) | ikon **és** szó: „3 passengers” |
| Kártya ↔ táblázat kétféle névrendszer | A és D azonos neveket és sorrendet használ |

### ✅ Tomi négy kérése — mind kész

| Kérés | Mi történt |
|---|---|
| **VIE/BTS parkolás** | „a helyszínen, a mindenkori helyi szabályozás szerinti összeg” — beírva az útvonal-váltó jegyzetébe |
| **Névegységesítés** | `Luxury Minibus` az A-kártyán is (VIP szó nélkül), a D-ben már úgy volt |
| **„Minden szivárgásnak meg kell szűnnie”** | A #6 blokk `h2{}`, `h3{}`, `h3 span.flag{}` és a media query `h2{}` szelektora `.vb-section` alá került. Az egész oldalon **0 namespace nélküli szelektor** maradt (mind a 6 blokk ellenőrizve). A #0 blokk főcíme `vb-page-h2` osztályt kapott + saját, nem szivárgó szabályt — a megjelenése **változatlan** (mérve: 41,6 px / 800 / középre zárt, ugyanaz, mint korábban) |
| **„Mindenhol 60 perc”** | Lásd lent |

### 60 perc — tételesen

Javítva (**várakozási idő**, 2 hely a #4-ben):
- „Each booking covers **30** minutes of parking and waiting time” → a €12 fedezi a parkolást és **60 perc** várakozást a landolástól
- „Should the waiting time exceed **30** minutes” → **60** perc, utána a BUD mindenkori díjszabása
- „Up to **30** minutes of complimentary waiting time” → „Up to **60** minutes of waiting time after landing”

**Szándékosan NEM nyúltam hozzá 3 helyen:** az EN/DE/ES FAQ-ban a „30 minutes / 30 Minuten / 30 minutos” a **menetidőre** vonatkozik („a trip usually takes around 30 minutes during off-peak hours and up to 60–70 minutes during rush hour”), nem a várakozásra. Ezt 60-ra írni tárgyi hiba lett volna.

### „Parkolás benne van az árban” — 9 ellentmondás javítva

A táblázat és az ÁSZF szerint a parkolás **külön tétel** (+12 € / +3 €). Ezek a mondatok mind ehhez igazodtak:

| Blokk | Hol |
|---|---|
| #3 | „include every cost: **parking fees**, …” |
| #4 | „Your confirmed quote already includes **airport parking**…” |
| #4 | „all our transfer rates already include these updated airport costs” |
| #4 | „a 5-minute **parking interval is included** in the service” |
| #4 | FAQ: „covering taxes, tolls, VAT, **and parking**” |
| #4 | lista: „Fixed, transparent pricing **with all fees included**” |
| #6 EN | „…terminal, **parking fees**, highway tolls…” · „include every cost: waiting time, tolls, **parking**…” |
| #6 DE | „…**Parkgebühren**, Autobahngebühren…” · „…Maut, **Parkgebühren**, Steuern…” |
| #6 ES | „…**tasas de estacionamiento**, peajes…” · „…peajes, **estacionamiento**, impuestos…” |

Mindegyik helyére a tételes kiírás került (EN/DE/ES-ben is): **€12 érkezéskor** (60 perc várakozással) és **€3 induláskor**, a visszaigazoláson tételesen.

### ❌ Nem kódolható — tartalom vagy médiatár kell

Ezekhez nem nyúltam, mert vagy szöveget érintenek, vagy feltöltést igényelnek:

- **C-csomag maradéka (nyitott döntések):** „10 → 15 perc” (mikor megy be a sofőr a terminálba — az audit szerint Tomi 15 percet mondott, az oldalon 10 áll), menetidő-ellentmondás (40–45 perc vs. 30 / 60–70 perc), „12 óra vs. 12–24 óra” ajánlatadás, lemondási FAQ 3 járműsávra bontása, „25% discount” (tiltott szó + él-e még?), „Luxury Car VIP **2024**” évszám, „Hungary- Vienna” elírás.
  → Ezekhez **egyenként kell döntés** — nem találgatok. Szólj, melyik mehet, és egy körben javítom.
- **B-csomag (képek):** 2 magánrepülő stock-kép licenc-cseréje, „Travel route” base64-nevű kép, a 404-es `placeholder-default.jpg`, 11 nagy kép tömörítése, Hősök tere-i kategóriaszett feltöltése, `og:image`.
- **D-csomag (globális):** látható H1 / WP-cím, `_fbp` Set-Cookie → edge-cache, GTM-konténerek, DE/ES FAQ Lingexto-oldalakra + hreflang, FAQPage schema.

---

## Előnézet

```
preview/airport-pricing-preview.html
preview/shot-1440.png
preview/shot-390.png
```

Az előnézet **szándékosan tartalmazza** a #6 blokk szivárgó `h2{}`/`h3{}` szabályait, hogy látszódjon: az új blokkok ellenállnak nekik.
