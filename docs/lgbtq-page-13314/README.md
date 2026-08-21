# LGBTQ+ Luxury Transfers oldal (ID 13314) – 1. kör javítás (2026-08-21)

Élő oldal: https://vanbudapest.com/inclusive-lgbtq-luxury-transfers-budapest/
Audit alap: VBauditLGBTQ1331420260821.html (Evelin-skill, 2026-08-21)

## Mi történt (a felhasználó által jóváhagyott 1. kör)

### 1. Képek (első prioritás)
- Mind a 4 törött képhely megszűnt (a 3 nem létező fájl minden hivatkozása cserélve).
- A hero a jogilag kockázatos 2023-as stockfotó helyett a saját LGBTQ-sorozat
  tömeg+zászlós képét kapta (13319, arc nélkül, 1536×1024).
- Flotta blokk: vezérkép = V-Class + S-Class együtt (25323); alatta valódi,
  május óta feltöltött sorozatképek: V-Class (Mercedes_V-class_VanBudapest-30),
  S-Class (25118), VIP Sprinter (25259), prémium utastér (26376).
  Az E-Class AI-render maradt (az audit szerint helyes jármű) – valódi E-Class
  sorozatkép kiválasztása vizuális ellenőrzést igényel (2. kör).
- Minden „rossz járművet mutató" kép cserélve (nagybusz→Sprinter, Sprinter→S-Class,
  fehér Sprinter→belső tér); a Dubrovnik-„Prága" kép helyett Bratislava Castle (26400).
- A Sziget 2025 színpadkép mindkét (jogilag kockázatos) példánya, a Shutterstock-
  előnézet, az Airbnb-kép és a Széchenyi pool-party kép eltávolítva.
- Ismétlődő képek megszüntetve (1 kép = 1 hely); 14 hibás ALT javítva, hogy azt
  írja, ami a képen van.
- Évszám-függő feliratok („Pride 2025") évszám-semlegesre írva.

### 2. Kódtisztítás
- A post_contentben 0 `<style>`, 0 `<script>`: minden korábbi inline CSS/JS és a
  KSES-től csonkolt kódmaradványok törölve.
- A teljes stílus egyetlen, KIZÁRÓLAG a 13314-es oldalra szkópolt szabályban él
  (StifLi Flex MCP scoped CSS, rule_id: `vb-lgbtq-13314`, priority 10).
- Minden selector a `.vb-lx` namespace alatt – nincs `:root`, nincs generikus
  `.vb-section`, semmi nem szivárog más blokkra vagy oldalra.
- A 10 végtelen háttéranimáció és a `background-attachment:fixed` törölve
  (statikus gradiensek); a FAQ JS-accordion helyett natív `<details>/<summary>`.
- Kontraszt-javítás: töltött CTA-gombok (arany/navy), a sárga blokkon navy
  szöveg, a narancs/piros blokkok mélyebb tónusai – nincs több 1,04:1-es gomb.
- Sorkizárás megszüntetve (text-align:left), reszponzív kaszkád 1024/781/480,
  a rács-minmax `min(100%,260px)` – nincs 320px-es túllógás.
- Brand-szabály javítások: „35 years" → „Since 1988", „at least basic English" → „English".

### 3. Elrendezés
- Középre zárt tartalom (max-width 1320px, auto margó), faltól-falig háttércsík
  (`width:100vw; margin:0 calc(50% - 50vw)`), a blokkok között 0 rés
  (blokk-gap kiütve csak ezekre a szekciókra).

## Fájlok
- `page-13314-content.html` – a post_content pontos, feltöltött állapota
- `scoped-13314.css` – a 13314-re szkópolt stíluslap (rule_id: vb-lgbtq-13314)

## Visszavonás
- Tartalom: StifLi changelog action 784/785 (mcp_rollback_change)
- Scoped CSS: action 783

---

# 2. kör (2026-08-21) — a kért 13 tétel

### 1. fal.ai képek (hero + Pride Fleet)
- Hero: **26715** – fekete V-Class szivárványos gyalogátkelőn, Andrássy-jellegű
  homlokzatokkal, arany órában. `nano-banana-2/edit`, a saját 26345-ös V-Class
  fotóból, hogy a jármű a valódi legyen. Arc és olvasható rendszám nincs rajta.
- Pride Fleet (#8 első kártya): **26716** – ugyanaz a V-Class, elmosott Pride-tömeggel
  és zászlókkal a háttérben.
- Mindkettő átment a vizuális minőség-ellenőrzésen (torzulás, embléma, arc nincs).

### 6–8. Vizuálisan ellenőrzött képcserék
A `fal-ai/any-llm/vision` modellel minden jelöltet leírattam, mielőtt cseréltem:
- **E-Class**: `24942` (valódi fekete E-Class külső) az AI-render helyett
- **S-Class belsők**: `25104` (utastér) és `25105` (hátsó ülések képernyőkkel)
  a 568 px-es életlen `S2-1.jpg` és az álló `S-interior.jpg` helyett
- **VIP Sprinter lounge**: `25250` a „RYK Interior" munkacímű kép helyett

### 10. Ár-oldalak a CTA-kban
- Airport blokk: „Luxury VIP" → **Airport Transfer Prices** (`/budapest-airport-pick-up-transfer-price/`)
- Hourly blokk: „Luxury VIP" → **Hourly Ride Prices** (`/price-bus-rental-cost-hourly-ride/`)

### 11. FAQPage schema
A 20 kérdés `application/ld+json` FAQPage blokkban, a HTML-ből generálva
(a kérdés-sorszámok és a markup nélkül), a látható accordionnal szinkronban.

### 12. Horgony-navigáció + sticky mobil CTA
- 7 chip a hero alatt (Discretion · Chauffeurs · Fleet · Airports · Hourly · Pride · FAQ),
  a szekciókon `id` + `scroll-margin-top: 96px`
- ≤781 px-en alul rögzített sáv: „Book Now" + „★ WhatsApp" (a FAQ blokk alsó
  paddingja megnövelve, hogy ne takarjon tartalmat)

### 13. Emoji-stratégia
Emoji kikerült mind a 9 H2-ből (snippet-zaj és felolvasás miatt), de megmaradt
a feliratokban és alcímekben — az oldal hangneme így nem változik.

### 15. Téma-betűk woff2-ben (globális)
A téma (Organic Chrono) 18 családot deklarál **variable TTF**-ként; ebből ez az
oldalkészlet hármat használ: Roboto Serif (h1/h2), Raleway (törzs), Jost (h3–h6,
gombok, navigáció). A globális Additional CSS elejére 16 `@font-face` került,
amelyek ugyanezeket a családokat **woff2**-ből töltik (latin + latin-ext + cyrillic
subsetek, `font-display: swap`). A téma saját TTF-szabályai érintetlenek: minden
olyan karakterre, ami kívül esik a megadott unicode-range-eken, automatikus
tartalékként működnek. Fájl: `global-fonts-woff2.css`. Visszavonás: action 797.

### 16. srcset minden képen
Mind a 38 kép megkapta a `wp-image-{ID}` osztályt és egy kézzel hangolt `sizes`
értéket, így a WordPress `wp_filter_content_tags` generálja az srcset-et:
- hero és teljes szélességű figure: `(max-width: 781px) 100vw, 1100px`
- középre zárt figure: `… 900px`
- 3 oszlopos rács: `(max-width: 480px) 100vw, (max-width: 1024px) 50vw, 420px`
- 2 oszlopos rács: `(max-width: 781px) 100vw, 640px`
Élőben ellenőrizve: a renderelt HTML-ben minden képnek van srcset+sizes.
A Vienna reptéri kép fájlként létezett, de nem volt médiatári bejegyzése —
újra feltöltve (**26722**), így az is kapott srcset-et.

### 4. ShortPixel
A plugin `autoMediaLibrary` + `doBackgroundProcess` bekapcsolva, `createWebp` és
`createAvif` igen, `deliverWebp: 0` (a formátumváltást a CDN végzi Accept alapján).
A >1 MB-os origin fájlok problémáját ezen az oldalon az srcset oldja meg: a
`lgbtq-budapest-transfer.png` (1,2 MB, 1776 px) helyett a rácsban a 768 px-es
változat töltődik. A **bulk újraoptimalizálás wp-admin művelet** (Media →
Bulk ShortPixel), MCP-ből nem indítható — ez maradt Tominak/Evelinnek.

### 5. LCP/INP mérés
A Google PageSpeed API a WordPress szerver IP-jéről `quota_limit_value: 0`
hibát ad (nem csak kimerült napi keret — a projektnek nincs engedélyezve).
Az Ahrefs Site Audit „Insufficient plan". Mérés n8n-ből, másik kimenő IP-ről
megkísérelve — az eredményt lásd a session jelentésében.

### 3. Fordítások (de 25458 / es 25465 / fr 25485)
Mindhárom **publikált és stale**. A Lingexto `translate` ability kódból tiltja az
élő fordítás felülírását (published-biztonság + emberi review) — ez szándékos
termékdöntés, nem került megkerülésre. Helyette a **képhibák** javítva mindhárom
nyelven, a fordított szöveghez nyúlás nélkül: törött fájlok, jogi kockázatú képek
és téves járműképek cserélve az `image-map.md` szerint.
A szöveg-szinkronizálás a wp-admin Lingexto frissítés-útján történhet.

## Fájlok (2. kör után)
- `page-13314-content.html` – a post_content aktuális, feltöltött állapota (v3)
- `scoped-13314.css` – a 13314-re szkópolt teljes stíluslap
- `global-fonts-woff2.css` – a globális Additional CSS-be beszúrt woff2 blokk
- `image-map.md` – a fordításokra alkalmazott képcsere-térkép

## Visszavonási pontok (StifLi changelog)
| Mit | action_id |
|---|---|
| Scoped CSS (1. kör) | 783 |
| Oldaltartalom v1 | 785 |
| Scoped CSS (horgony + sticky) | 794 |
| Oldaltartalom v2 | 796 |
| Globális font-CSS | 797 |
| Scoped CSS (figure max-width) | 799 |
| Oldaltartalom v3 | 801 |

## Továbbra is nyitott
- Ajánlások/„(verified)" hitelesítése vagy valódi Google-értékelésre cserélése
  (üzleti döntés — az audit 12d/1 pontja)
- Évszak-semleges Prága-kép (a médiatárban nincs Prága-fotó; fal.ai vagy saját archív)
- ShortPixel bulk újraoptimalizálás (wp-admin)
- de/es/fr szöveg-szinkronizálás a Lingexto admin frissítés-útján
