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
| `blocks/OPTIONAL-block-06-faq-selector-fix.md` | #6 szivárgó `h2{}`/`h3{}` — **döntést kér, nem alkalmaztam** | — |
| `preview/airport-pricing-preview.html` | A + D egyben, a WP-környezet szimulálásával | csak előnézet, nem megy fel |

---

## Amit kértél, és amit csináltam

### A koncepció — változatlanul

Ahogy kérted: „ez így, ahogy van, föl is mehet”. A szerkezet, a szövegek, az árak, a képek, a sorrend, az útvonal-váltó, az „Included” sáv — mind a prototípus szerint.

Amit a WordPress miatt **muszáj** volt hozzátenni (megjelenést nem érint):

- a `:root` változók a `.vbp-a` szekcióba kerültek (WP-ben nincs saját `:root`),
- az ikonok `.vbp-a` alá scope-olva,
- full-width a site `.vb-fw` mintája szerint (`100vw` + `calc(50% - 50vw)`),
- a címsorokon explicit `display` — hogy a #6 blokk szivárgó `h3{display:flex}` szabálya ne törje szét (lásd OPTIONAL fájl),
- `srcset` + `sizes` + `width`/`height` minden képen; az első kártyakép `loading="eager" fetchpriority="high"` (audit 10. pont),
- a váltó-script kapott dupla-kötés elleni védelmet (`data-vbp-bound`).

**Egy tartalmi eltérés a prototípustól, amit jelezni akarok:** a prototípus VIE/BTS jegyzete `{{VIE parking rule – to be confirmed}}` placeholdert tartalmazott. Placeholder nem mehet ki élő ügyféloldalra, kitalálni pedig nem szabad (audit 7.6 — nyitott kérdés). Ezért a jegyzet VIE/BTS-nél most csak annyi: *„Long-distance rate · tolls & motorway vignettes included”* — a placeholder rész kimaradt. **Ha van VIE/BTS reptéri parkolási tétel, szólj, és beírom.**

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

## ⚠ Feltöltés — MCP-vel NEM lehet, és ez fontos

Az audit „Kritikus figyelmeztetés” pontja igaznak bizonyult, én is leellenőriztem:

**Az MCP `wp_get_post` veszteséges olvasás.** A visszaadott `post_content`-ben:

- `<style>` / `</style>` tag: **0 db** (a CSS *szövege* bent van — 297 `!important`, 12 `@media` —, csak a tag nincs)
- `<script>` / `</script>` tag: **0 db**
- `<link>` tag: **0 db**

Ellenőrizve a `wp-json/wp/v2/pages/1351` renderelt kimenetén: ott a tag **ott van**
(`…aria-label="Airport transfer pricing – VanBudapest"><style>`). Vagyis a tárolt tartalom ép, **az MCP olvasó-rétege ejti el a tagokat**.

**Következmény:** ha a `wp_update_page`-nek visszaírnám azt, amit kiolvastam, a **#3–#6 blokkok teljes CSS-e tag nélkül maradna** — a stíluslapok szövegként jelennének meg az oldalon, és a #4 blokk lightbox-scriptje elveszne. A #4 blokk scriptjének pontos tartalmát semmilyen elérhető csatornán nem tudom visszanyerni (a REST-fetch ~50 KB-nál levágódik, a `Range` fejlécet a szerver figyelmen kívül hagyja, a sandbox hálózata pedig a vanbudapest.com-ot tiltja).

**Ezért nem írtam az oldalra.** Két biztonságos út van:

### 1. Kézi bemásolás (most azonnal, kockázat nélkül)

Csak a két érintett blokkhoz nyúlsz, a #3–#6 hozzá sem ér:

1. `/wp-admin` → Oldalak → *RELIABLE – CLEAN BUS & VAN: Budapest Airport Pick Up* (ID 1351)
2. **Előtte:** a nyitva felejtett Gutenberg-fül ügye (audit: a legutóbbi revízió 2026-07-18, újabb a `post_modified`-nál) — ha valakinél nyitva van a szerkesztő, zárja be mentés nélkül.
3. Keresd meg az **első** Custom HTML blokkot (a 6 árkártya, „Airport Pricing Cards – v2.0 CHRONO-SAFE” kommenttel kezdődik) → jelöld ki a teljes tartalmát → illeszd be a `blocks/block-01-airport-pricing-cards-A.html` teljes tartalmát.
4. A **második** Custom HTML blokk (`vb-pricing-section`, a 7 oszlopos táblázat) → ugyanígy a `blocks/block-02-price-matrix-D.html`.
5. Frissítés → utána **`seo-deploy` skill** (ShortPixel CDN cache-bump, inkognitós ellenőrzés desktopon és mobilon).

### 2. Application Password (ha azt akarod, hogy én írjam)

Ezzel a `?context=edit` → `content.raw` úton a nyers tartalom hiánytalanul kiolvasható, és sebészileg csak a két blokk cserélődik. Ha kapok egyet, megcsinálom és le is ellenőrzöm.

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

### ⚠ Kódolható, de döntést kér — nem alkalmaztam

- **#6 szivárgó `h2{}`/`h3{}`** → `blocks/OPTIONAL-block-06-faq-selector-fix.md`. Kész a patch, de **látható mellékhatása van a #0 blokk főcímére**, ami az audit 5. pontjához és a D-csomaghoz tartozik.
- **VIE/BTS parkolási szabály** (audit 7.6) → placeholder helye üresen; egy mondat kell tőletek.

### ❌ Nem kódolható — tartalom vagy médiatár kell

Ezekhez nem nyúltam, mert vagy szöveget érintenek, vagy feltöltést igényelnek:

- **C-csomag (ténybeli):** 30 → 60 perc (3 hely), „parking included” 6 helyen, 10 → 15 perc, menetidő- és 12/12–24 h ellentmondás, lemondási FAQ 3 sávra, „25% discount”, „2024” évszám, „Hungary- Vienna” elírás.
  → Ezek a #3–#6 blokkok **szövegében** vannak. **Fontos:** az új A/D blokkok már a *helyes* tényt írják (60 perc, parkolás külön tétel, +12 € / +3 €), tehát amíg a régi mondatok ott vannak, az oldal **önmagával** kerül ellentmondásba. Érdemes ezt a kört hamar meglépni.
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
