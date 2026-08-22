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

---

## ✅ 2. kör — címsor-összevonás + fehér csíkok megszüntetése (2026-08-22)

### Címsorok

Minden felsorolt cím megmaradt, de a fehér sávból a sötét blokk fejlécébe került — az A-blokk saját, duplikált „Airport Transfer Rates” H2-je helyére:

```
[fehér]  RELIABLE – CLEAN BUS & VAN: Budapest Airport Pick Up   ← WP-cím, marad
─────────────────────────────────────────────────────────────
[sötét]  FIXED, PUBLISHED RATES · SINCE 1988
         Budapest & Hungary- Vienna – Airport Transfers          ← volt #0 H2
         AIRPORT TRANSFERS TO BUDAPEST – RELIABLE, COMFORTABLE…  ← volt #0 H6
         AIRPORT TRANSFER RATES — BUDAPEST (BUD), BRATISLAVA…    ← volt #0 H6
         Private chauffeur transfers between your Budapest…
         [BUD | VIE | BTS]  →  kártyák
```

A szövegek karakterre pontosan mentek át (a „Budapest” utáni **két szóköz** is). A H2/H6 szintek változatlanok, csak a helyük és a stílusuk más — a `vbp-kicker` osztály reprodukálja a téma kiskapitális H6-megjelenését, aranyszínben.

A `vb-page-h2` osztály és a hozzá tartozó szabály feleslegessé vált (a Gutenberg-H2 elköltözött) — a #6 blokkban maradt 2 sor halott CSS, ártalmatlan, következő körben kitakarítható.

### Fehér csíkok — mi okozta és mi lett velük

| Forrás | Db | Megoldás |
|---|---|---|
| `core/separator` | 3 | törölve |
| `core/spacer` | 5 | törölve |
| üres `core/paragraph` | 2 | törölve |
| **üres `core/group`** („Hero Product 3 Split” — csak 2 spacert tartalmazott) | 1 | törölve |
| a #0 group `padding` | — | `0` mind a 4 oldalon |
| WP blokk-wrapperek margói | — | page-scoped szabály (`body.page-id-1351`) |

Top-level blokkok: **8 → 4**. A `<style>` (6), `<script>` (2), `<link>` (9) és `<img>` (35) darabszám változatlan.

### Mérés a VALÓDI élő tartalomból

`tools/measure-section-gaps.mjs`, a WP/téma résképző szabályainak szándékos szimulálásával:

```
✅ 0px  vbp-a → vbp-d
✅ 0px  vbp-d → vb-section (Luxury Beyond)
✅ 0px  vb-section → vb-section (motion-v4)
✅ 0px  vb-section → vb-section (Summary)
✅ 0px  vb-section → vb-section (FAQ)
```

A hat sötét szekció hézagmentesen összeér. A WP-cím alatt marad ~24 px levegő (a téma címsor-margója) — szándékos, hogy a nagy fekete cím ne tapadjon rá a sötét blokkra.

### Feltöltés

`page-sections.remove` ×4 (hátulról előre, hogy az indexek ne csússzanak) + `page-sections.replace` ×1, mindegyik optimista zárolással. `_content_warnings: []` minden lépésnél.

---

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

- **C-csomag maradéka (nyitott döntések):** ~~10 → 15 perc~~, ~~12 óra → 12–24 óra~~, ~~25% discount~~, ~~„Hungary- Vienna” elírás~~ — **mind kész a 3. körben.**
  ~~lemondási FAQ 3 járműsávra bontása~~ — a 4. körben bekerült az ÁSZF szerint, majd az **5. körben Tomi döntése alapján teljesen kikerült** (nem pótoljuk ki).
  Nyitva maradt: **menetidő-ellentmondás** (40–45 perc vs. a FAQ 30 / 60–70 perce — ugyanarra az útra),
  **„Luxury Car VIP 2024”** évszám. (A kiemelt időszaki felár kérdése az 5. körben megoldva: az ütköző állítások kikerültek.)
  → Ezekhez **egyenként kell döntés** — nem találgatok. Szólj, melyik mehet, és egy körben javítom.
- **B-csomag (képek):** 2 magánrepülő stock-kép licenc-cseréje, „Travel route” base64-nevű kép, a 404-es `placeholder-default.jpg`, 11 nagy kép tömörítése, Hősök tere-i kategóriaszett feltöltése, `og:image`.
- **D-csomag (globális):** látható H1 / WP-cím, `_fbp` Set-Cookie → edge-cache, GTM-konténerek, DE/ES FAQ Lingexto-oldalakra + hreflang, FAQPage schema.

---

## ✅ 3. kör — az audit jóváhagyott pontjai (2026-08-22)

A C-csomagból amit jóváhagytál, mind kint van. `apply-changes-step3.py`, 9 lépés,
mindegyik `assert n == expect` ellenőrzéssel, 3 blokk cserével.

| # | Amit kértél | Mi történt | Hol |
|---|---|---|---|
| 1 | „ezt javíthatod, hogy ne legyen gáz” | `Hungary- Vienna` → `Hungary – Vienna` | #1 A-blokk H2 |
| 2 | „ITT A 12-24 A JÓ, ERRE KELL JAVÍTANI MINDENT!” | `within 12 hours` → `within 12–24 hours` (2 hely) | #3, #5 |
| 3 | „A 15 A VALÓS, MINDENHOL EZ LEGYEN!” | `10 minutes after landing` → `15 minutes` | #4 |
| 4 | „EZ PRÉMIUM OLDAL, EZÉRT NEM LENNE SZABAD EZT KIÍRNI” | a 25%-os mondat törölve | #5 |
| 5 | „CSINÁLD MEG!” (CLS) | 4 képre `width`/`height` + `loading="lazy"` | #3 galéria |
| 6 | Coach kártya üres oldalra vitt | link → flotta oldal, felirat → `Vehicle details →` | #1 A-blokk |
| + | (magamtól, kódhiba) | lightbox `'n'` szemét eltávolítva | #4 script |

### A 25%-os kedvezmény — hol volt

A **#5 Summary** blokkban, önálló mondatként:

> *„Plus, for a limited time, enjoy a 25% discount on your next Budapest Airport Transfer.”*

Mivel önálló mondat volt, tisztán kivehető — a bekezdés többi része érintetlen.

### CLS — pontosítás a korábbi becsléshez

Először 17 képet mondtam. **Blokkonként megmérve valójában 4 volt veszélyben.**
A #4 blokk 13 képét a saját CSS-e védi:

```css
.vb-card img{ display:block; width:100%; height:auto; aspect-ratio: 4/3; object-fit:cover; }
```

Az `aspect-ratio` ugyanúgy lefoglalja a helyet, mint a `width`/`height` — ott nincs ugrás.
Egyedül a **#3 „Luxury Beyond” galéria** 4 képének nem volt semmilyen védelme
(`.vb-card img{width:100%;height:auto;object-fit:cover}` — magasság-foglalás nélkül).
Ez a 4 kép kapott most `width`/`height`-ot.

### A Coach kártya „üres oldala” — mi volt a baj

A `Coach options →` link a **17870-es oldalra** mutatott:

| | |
|---|---|
| Cím | „Coach Bus Category (34-49 seats) — Vehicle Options” |
| Státusz | `publish` |
| Tartalom | **üres string** |
| Utolsó mentés | 2026-01-25 |

Publikált oldal, nulla tartalommal — ezért jelent meg üres lap.
A link most a flotta oldalra megy, a felirat pedig egységes a másik 5 kártyáéval.
**Az üres 17870-es oldalhoz nem nyúltam** — ha kell rá busz-tartalom, az külön kör.

### A lightbox `'n'` szemét

A #4 blokk lightbox-scriptjében ez állt:

```js
lb.innerHTML='n        <button …>✕</button>n        <figure …></figure>n      ';
```

Ezek elveszett `\n`-ek: egy korábbi mentési csatorna leszedte a backslash-eket, és
a magára maradt `n` betűk **szöveges csomópontként bekerültek a nagyított kép mellé**.
A backup fájlban is így volt, tehát **nem az én köreim okozták** — de mivel úgyis
ezt a blokkot írtam, egy körben kijavítottam:

```js
lb.innerHTML='<button …>✕</button><figure …></figure>';
```

Backslash nélkül, hogy egy következő mentés se tudja újra elrontani.
Az egész oldalon **0 backslash** van — más ilyen sérülés nincs.

### Feltöltés — blokkonként, bájtra ellenőrizve

| Blokk | Méret | `_content_warnings` | Bájtazonos |
|---|---|---|---|
| [2] #5 Summary | 8 733 | `[]` | ✅ |
| [1] #4 Motion-v4 | 21 527 | `[]` | ✅ |
| [0] Pricing group (A + D + #3) | 50 692 | `[]` | ✅ |

Minden írás után visszaolvasva: a cél-blokk bájtra egyezik a helyivel, a **másik három
blokk bájtra változatlan**, és a teljes oldal megegyezik az elvárt tartalommal (96 972 karakter).

---

## ✅ 4. kör — halott CSS + a lemondási FAQ az ÁSZF szerint (2026-08-22)

Egy blokk (`[3]`, #6 FAQ), két dolog. `apply-changes-step4.py`, 4 lépés, bájtra ellenőrizve.

### 1) Halott CSS kivéve

A 2. körben a `.vb-page-h2` osztályt azért kapta meg a #0 blokk H2-je, hogy a szivárgó
`h2{}` namespace-elése után is megtartsa a kinézetét. Utána azt a H2-t áthoztuk az
A-blokkba, így az osztály **használat nélkül maradt**: a CSS-ben kétszer definiálva,
egyetlen elemen sem. Most kivéve (−181 bájt).

### 2) Lemondási FAQ — EN / DE / ES, az ÁSZF VII. fejezete szerint

Forrás: `VanBudapest_ASZF_HU.docx` (Tomi küldte 2026-08-22).

**Ami a lapon állt:** csak a 72/48 órás sáv, és azt a minibuszokra is kiterjesztette.
A német kifejezetten *„Bei PKWs **und Minivans**"*, a spanyol *„Para sedanes **y minivans**"* —
az ÁSZF szerint viszont a V-Class/Sprinter sávja **7 nap**, nem 72 óra. A publikált szöveg
tehát **kedvezőbb feltételt ígért, mint az ÁSZF** — ez a kockázatosabb irány.

**Ami most áll, ÁSZF 7.2 szerint:**

| Kategória | 100% | 50% | 0% |
|---|---|---|---|
| **7.2.1** Személygépkocsi (E-Class, S-Class) | ≥ 72 óra | 72–48 óra | < 48 óra / no-show |
| **7.2.2** Minibusz (V-Class, Sprinter) | ≥ 7 nap | 7 nap – 72 óra | < 72 óra / no-show |
| **7.2.3** Autóbusz és VIP Sprinter | ≥ 21 nap | 21–14 nap | < 14 nap / no-show |

Plusz, szintén az ÁSZF-ből: **3% tranzakciós költség, min. 20 €** (7.2.4/a) · **módosítás
72 órán belülig díjmentes** (7.5.2) · **lemondás kizárólag e-mailben**, `info@vanbudapest.com`
(7.1.2) · **kiemelt időszakban szigorúbb rend lehet, a visszaigazolás az irányadó** (7.3, 7.3.3).

Mindhárom nyelven ugyanaz a tartalom, kategóriánként külön `<p><b>…</b></p>` sorban —
így olvasható marad a `<details>`-en belül.

### Az ÁSZF megerősítette a korábbi köröket

Két dolgot, amit már kint volt, most utólag alá tudtam támasztani:

| Amit publikáltunk | ÁSZF |
|---|---|
| €12 érkezéskor, **60 perc** várakozással | *„12 EUR parkolási díj… maximum 1 óra várakozási időt foglal magában"* |
| €3 induláskor, **5 perc** kiállással | *„3 EUR parkolási díj… legfeljebb 5 perc időtartamot tartalmaz"* |
| „beyond that, the airport's current tariff applies **on the spot**" | *„az egy órát meghaladó várakozás feláras (a BUD mindenkori díjszabása szerint) **a helyszínen kell fizetni**"* |

### ⚠️ Új, nyitott ellentmondás: kiemelt időszaki felár

Az **ÁSZF 6.3** szerint kiemelt időszakokban (karácsony–szilveszter, munkaszüneti napok,
nagy események) eltérő díjazás alkalmazható, és **2026. december 23. – 2027. január 2.
között +100% felár** is lehet; a végleges ár mindig az árajánlatban szerepel.

Az oldal viszont *„Fixed, published rates"*, *„the fare you see is the fare you pay"*,
*„no surprises and no hidden fees"* állításokkal publikálja a 2026-os táblázatot,
és sehol nem jelzi, hogy ez alapdíj, amitől kiemelt időszakban el lehet térni.

A kettő összeegyeztethető (a fix ár a **visszaigazolás után** fix), de ez a lapon nincs kimondva.
→ **Döntés kell**: kell-e egy rövid kiegészítés a D-mátrix alá, pl.
*„Base rates. Peak periods and major events are quoted individually — your confirmed price is then fixed."*
Ehhez nem nyúltam, mert kereskedelmi döntés.

### ℹ️ A `vanbudapest-rules` skill jóváhagyott-link listája elavult

A skill „Coach Options" sorában még a `https://vanbudapest.com/coach-bus-vehicle-options/`
szerepel — az az oldal (17870) publikált, de a tartalma **üres string**. A 3. körben Tomi
kérésére a kártya-link a flotta oldalra került. A skill listáját érdemes frissíteni,
vagy az üres oldalt feltölteni.

---

## ✅ 5. kör — CSAK TÖRLÉS: minden ÁSZF-fel ütköző állítás ki (2026-08-22)

Tomi döntése: *„Vedd ki azokat amik ellenkeznek az ÁSZF-el, de ne pótold ki a jelenlegi
ÁSZF szerinti szabályokkal, csak szedd ki."* — tehát a 4. körben beírt ÁSZF-sávok is
kikerültek, helyettük **semmi** nem jött. `apply-changes-step5.py`, 24 lépés, mind a 4 blokk.

### A teszt, amit egy mondatra alkalmaztam

Egy állítás akkor ütközik, ha azt mondja, hogy

- **(a)** az oldalon **közölt** ár a végleges fizetendő ár, vagy
- **(b)** semmilyen további díj nem merülhet fel.

Ez azért ez, mert az **ÁSZF 6.2** szó szerint ezt írja:

> *„Az árak **irányadóak**, az aktuális és végleges díj minden esetben az **írásos
> visszaigazolásban** kerül rögzítésre."*

…és az ÁSZF ugyanitt **erre az oldalra linkel** mint az irányadó árak helyére.
Plusz **6.3**: kiemelt időszakban eltérő díjazás, dec. 23. – jan. 2. között **+100%** felár.
Plusz **6.1/6.5**: a parkolás nem része a viteldíjnak, a 60 perc feletti várakozás feláras.
Plusz **6.1/6.6**: a többletcsomag-szállítás költsége a Megrendelőt terheli.

### Ami kikerült

| Blokk | Mi volt ott |
|---|---|
| #1 (A) | eyebrow: „**Fixed, published rates** · Since 1988" → csak „Since 1988" |
| #3 | „…and **include every cost**:" → „…and include:" · „clear, **all-inclusive** pricing" → „clear pricing" |
| #4 | „**At VanBudapest, the fare you see is the fare you pay. Every airport transfer is offered at a fixed, all-inclusive rate, meaning no surprises and no hidden fees.**" — törölve |
| #4 | h3: „Transparent, **All-Inclusive** Pricing" → „Transparent Pricing" |
| #4 | intro: „fixed **all-inclusive** pricing" → „fixed pricing" |
| #4 | FAQ „Are the prices really fixed?" — **teljes kérdés törölve** |
| #5 | „**These are final prices and will not be charged any additional fees.**" — törölve |
| #5 | „**Final Fixed Prices – No Hidden Costs**" szekció (h3 + bekezdés) — **teljesen törölve** |
| #6 EN/DE/ES | 1. kérdés: „all-inclusive" / „Endpreise" / „todo incluido", „no hidden charges" / „keine versteckten Zusatzkosten" / „sin cargos adicionales", „the final price you pay" / „der angezeigte Preis ist der Endpreis" / „el precio final que pagará" — törölve |
| #6 EN/DE/ES | késés-kérdés: „…flight delays, traffic, **or waiting time**" → „…flight delays or traffic" (60 perc felett feláras) |
| #6 EN/DE/ES | „Are the prices fixed with no hidden fees?" / „Sind die Preise endgültig…?" / „¿Los precios son fijos…?" — **mindhárom kérdés törölve** |
| #6 EN/DE/ES | lemondási kérdés — **mindhárom törölve** (a 4. körben beírt ÁSZF-sávokkal együtt) |
| #6 EN/DE/ES | „luggage trailer **free of charge**" / „**ohne Aufpreis**" / „**sin coste adicional**" → a díjmentesség-ígéret törölve |

### Ami MARADT (mert az ÁSZF alátámasztja)

- mi van a viteldíjban: útdíj, autópálya-matrica, Meet & Greet, ÁFA → **ÁSZF 6.1**
- a tételes **€12 érkezés / €3 indulás**, a **60 perc** várakozás, és hogy azon felül
  a reptér mindenkori tarifája a helyszínen fizetendő → **ÁSZF 6.5**
- „nincs felár késésért vagy forgalomért" → a visszaigazolt ár utólag nem változik
- „Since 1988" → jóváhagyott brand line

### A csomagszállító pótkocsi — ez az egy, ami üzleti döntés

Az ÁSZF **6.1** kifejezetten kiveszi a viteldíjból *„a Megrendelő hibájából szükségessé váló
további jármű vagy csomagszállító eszköz költségeit"*, a **6.6** pedig azt írja, hogy a
kapacitást meghaladó csomag esetén *„külön jármű vagy csomagszállítás szükséges, amelynek
szervezése és költsége a Megrendelőt terheli"*. Az oldal viszont mindhárom nyelven
**díjmentesnek** ígérte. A „free of charge / ohne Aufpreis / sin coste adicional" ezért kikerült,
a mondat maga maradt. **Ha előre bejelentett nagy csoportnál tényleg ingyenes, ezt vissza lehet tenni** —
egy szó, és megy.

### Feltöltés — 4 blokk, bájtra ellenőrizve

| Blokk | Méret | `_content_warnings` | Bájtazonos |
|---|---|---|---|
| [2] #5 Summary | 8 733 → 8 397 | `[]` | ✅ |
| [3] #6 FAQ | 12 421 | `[]` | ✅ |
| [1] #4 Motion-v4 | 20 935 | `[]` | ✅ |
| [0] Pricing group | 50 641 | `[]` | ✅ |

Teljes oldal: 98 488 → **92 408** karakter, és bájtra egyezik az elvárttal.
Mérés utána: 6 szekció, mind az 5 rés **0 px**, vízszintes túlcsordulás **0** — 1440-en és 390-en is.
A FAQ 31 → **24** kérdés (7 nyelvenként).

### Skill-fájlok is javítva

A `/coach-bus-vehicle-options/` (üres oldal) linkje kikerült **mindkét** helyről, ahol szerepelt:

- `vanbudapest-rules` → „Jóváhagyott linkek" tábla
- `vanbudapest-brand-guide` → „Coach Options" sor

Így a flotta oldal maradt az egyetlen jóváhagyott jármű-link. `grep` a synced skillekre: **0 találat**.

---

## ✅ 6. kör — minden CTA új lapon nyílik (2026-08-22)

`apply-changes-step6.py`. Az oldal **mind a 25 CTA-linkje** megkapta:

```html
target="_blank" rel="noopener"
```

| Osztály | Db | Mi ez |
|---|---|---|
| `.vbp-btn` | **18** | „Book E-Class / V-Class / …" — 6 az A-kártyákon, 6 a D-mátrix táblázatában, 6 a mobil járműkártyákon |
| `.vbp-link` | **6** | „Vehicle details →" az A-kártyákon |
| `.vb-cta` | **1** | „Book VIP Transfer" a #4 blokk alján |
| **összesen** | **25** | |

### Miért `rel="noopener"` is

A `target="_blank"` önmagában odaadja a megnyíló lapnak a `window.opener` hivatkozást a
szülő lapra. A modern böngészők ezt már alapból blokkolják, de kiírva biztos, és a régebbi
böngészőkben egy külön böngészőfolyamatot is kap a lap (gyorsabb). Nulla kockázat, ezért kiírtam.

### A `mailto:` linket szándékosan kihagytam

A #5 blokkban van egy `mailto:info@vanbudapest.com`. Erre a `target="_blank"` csak egy
**üres fület** nyitna a levelezőprogram indítása mellé — rosszabb élmény, nem jobb.
Ez maradt úgy, ahogy volt. (Összes `<a>` az oldalon: 26 — ebből 25 CTA + 1 mailto.)

### Ellenőrzés

Nem csak az attribútumot néztem meg, hanem **valódi kattintást** is szimuláltam
(Playwright, Chromium): a `.vbp-btn`-re kattintva a böngésző tényleg **új lapot nyitott**
(1 → 2 lap). A layout változatlan: 6 szekció, mind az 5 rés 0 px, vízszintes túlcsordulás 0.

| Blokk | Méret | `_content_warnings` | Bájtazonos |
|---|---|---|---|
| [1] #4 Motion-v4 | 20 935 → 20 966 | `[]` | ✅ |
| [0] Pricing group | 50 641 → 51 385 | `[]` | ✅ |

A #5 és a #6 blokkban nincs CTA-link, azokat nem kellett bántani.

### Amire figyelni kell a jövőben

Ez a beállítás **az oldal tartalmában** van, nem globális. Ha új CTA-gomb kerül az oldalra,
arra külön rá kell tenni a `target="_blank" rel="noopener"`-t. A fejléc/lábléc menü
**téma-szintű**, arra ez nem vonatkozik — ha az is kell, az külön munka (téma vagy globális JS).

---

## ✅ 7. kör — galéria-bővítés: +19 kép, új rács (2026-08-22)

`apply-changes-step7.py`. **A kártyákat és a táblázatot nem érinti** — ezt nem ígérgetem,
hanem a script minden futáskor ellenőrzi és leáll, ha mégis megváltoznának:

```
vedelmi ellenorzes: A-kartyak bajtra valtozatlan  (25318 kar., sha1 72adaccf4b4f)
vedelmi ellenorzes: D-matrix  bajtra valtozatlan  (18051 kar., sha1 1bda3bd3e885)
```

A feltöltés után az **élő tartalomból** újramérve is ugyanez a két SHA1 jött ki.

### Mi került be — 19 új kép, mind az 5 kategóriából

Mind 2025. májusa utáni feltöltés, mind a médiatárból (`media.list` API), és
mind a 19 útvonal **visszaellenőrizve az API `source_url` mezőjéhez** (19/19 pontos egyezés).

| Kategória | Db | Forrás-szett |
|---|---|---|
| Mercedes S-Class | 5 | `2026/06/Mercedes_S-class_VanBudapest-*` |
| Mercedes V-Class | 5 | `2026/08/V-CLASS_VANBUDAPEST_FLEET_MERCEDES-*` + bratislava |
| VIP Sprinter | 4 | `2026/06/Mercedes_VIP_Sprinter_minibus_VanBudapest-*` |
| Mercedes E-Class | 3 | `2026/06/Mercedes_E-class_VanBudapest-*` |
| Sprinter (minibusz) | 2 | `2026/05/black-sprinter-budapest-disposal-*` |

| Galéria | Volt | Lett |
|---|---|---|
| #3 „Luxury fleet gallery” | 4 | **8** |
| #4 „Airport terminals” | 2 | **4** |
| #4 „Budapest travel moments” (külsők) | 3 | **8** |
| #4 „Extra visuals” (belsők) | 3 | **8** |
| #4 „Final highlight” | 1 | **4** |
| #4 „Policy & inclusivity” | 3 | 3 — *nem nyúltam hozzá, ez nem flotta-galéria* |

Az oldalon 35 → **54** kép.

### Az új rács — `.vbg`

Saját névtér, hogy ne ütközzön a meglévő `.vb-gallery` / `.vb-card` szabályokkal
(azok blokkok között is átszivárognak, mert mindegyik `.vb-section`-ben van definiálva).

- **Fix oszlopszám**, nem `auto-fit`: 4 oszlop → 2 oszlop ≤900px → vízszintes,
  snap-elő carousel ≤560px (ugyanaz a minta, mint az árkártyáknál).
- Minden csempe **azonos méretű** (`aspect-ratio:4/3` + `object-fit:cover`) — a magasság
  akkor sem csúszik el, ha a képek eredeti aránya eltér.
- A felirat **a képre ült rá** gradiens sávval, nem alá — így nincs rojtos alsó él,
  minden csempe pontosan egyforma magas.
- Hover: 4px emelés + 1.05× képnagyítás; `prefers-reduced-motion` esetén kikapcsol.
- A #4 lightbox-szelektora `'.vb-card img'` → `'.vb-card img, .vbg img'`, tehát az új
  képek is nagyban nyílnak kattintásra.

### Szimmetria — megmérve, nem megsaccolva

A csempeszám minden galériában osztható 4-gyel **és** 2-vel, tehát egyetlen töréspontban
sincs árva csempe. Playwrightból mérve, három szélességen:

| | csempe | oszlop × sor | egyforma szél. | egyforma mag. |
|---|---|---|---|---|
| 1440px | 285×214 | 4 × 2 (a 8-asoknál) | ✅ | ✅ |
| 900px | 363×273 | 2 × 4 | ✅ | ✅ |
| 390px | 244×183 | carousel, 1 sor | ✅ | ✅ |

És a **szöveghez igazodás**, szintén mérve — a galéria bal/jobb éle pontosan a bekezdések éle:

| | szöveg él | galéria él | egyezik |
|---|---|---|---|
| 1440px | 130 / 1310 | 130 / 1310 | ✅ |
| 900px | 81 / 819 | 81 / 819 | ✅ |
| 390px | 39 / 351 | 39 / 351 | ✅ |

Vízszintes túlcsordulás mindhárom szélességen **0**, a 6 szekció közti 5 rés továbbra is **0 px**.

### CLS

Az új képeken nincs `width`/`height` attribútum — **nem is kell**: a `.vbg img` CSS-ben
`aspect-ratio:4/3` van, ami ugyanúgy lefoglalja a helyet a betöltés előtt.
Mind a 19 kép `loading="lazy" decoding="async"`.

### Ami nyitva maradt

A #4 „Extra visuals” galériában **benne maradt a két magánrepülő-kép** — a kérés bővítés
volt, nem csere, ezért nem vettem ki őket. Most 8-ból 2, tehát felhígultak, de ha törölni
kell őket, az egy sor.

---

## Előnézet

```
preview/airport-pricing-preview.html
preview/shot-1440.png
preview/shot-390.png
```

Az előnézet **szándékosan tartalmazza** a #6 blokk szivárgó `h2{}`/`h3{}` szabályait, hogy látszódjon: az új blokkok ellenállnak nekik.
