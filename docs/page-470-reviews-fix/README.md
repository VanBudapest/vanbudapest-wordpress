# Page 470 — Google Reviews / Customer Feedback — audit-alapú javítási kör

**Dátum:** 2026-08-21 · **Oldal:** https://vanbudapest.com/google-reviews-customer-feedback/ (Page ID 470)
**Alap:** VB audit 2026-08-21 (vanbudapest-page-optimizer v3.0 + Evelin-réteg)
**Motor:** Master Prompt v3.0 szabályai szerint — szöveg változatlan, dizájn megtartva + ráncfelvarrás

---

## Mi történt (élesítve)

### 1. Tartalom-újraírás (wp_update_post, bájt-verifikált)

A két, WordPressbe bemásolt **teljes HTML-dokumentum** (saját `doctype`/`html`/`head`/`title`/`body`
tagekkel és prefix nélküli, az egész oldalra szivárgó CSS-sel) ki lett cserélve két tiszta,
namespace-elt szekcióra (`.vb-rev470-intro`, `.vb-rev470-arch`). **Minden látható szöveg
bájtra azonos maradt** (automatizált szöveg-diff: 0 eltérés).

| Javítás | Részlet |
|---|---|
| Scroll-csapda | a `html,body{height:100%}` leak megszűnt (960px → valódi ~8000px oldalmagasság) |
| CSS-szivárgás | 0 csupasz elem-selector maradt; fejléc/lábléc/tipográfia visszaállt a brand-alapra |
| `<title>` 3× → 1× | a body-beli 2 titletag eltávolítva |
| H1 2× → 1× | „Legacy Reviews Archive” H1 → H2 (látvány pineolva CSS-ből, szöveg azonos) |
| 1. értékelő kártya | `<h3>` → `<blockquote>` — egységes a másik 23-mal (a Jost/ritkított téma-H3 stílus eltűnt róla) |
| Fejlesztői komment | `MORE ITEMS CAN BE CONTINUED…` eltávolítva az élesből |
| Üres blokk | `<!-- wp:html /-->` maradékblokk törölve |
| Törött linkek | breadcrumb `/reviews` (404) → kanonikus URL; „Archive >” `http://vanbudapest` (DNS-hiba) → `#list` horgony |
| Képek (4 törött) | #5 galéria 1. csempe → media 18870 (275 KB webp) · #10 nagy csempe → media 24181 (158 KB webp) · #10 3. csempe → media 3816 (57 KB jpg) · #10 2. csempe: csak URL-fix (`;w=627` szemét-szegmens ki) |
| ALT-ok | a két cserélt képen a ténylegesen látható tartalomhoz igazítva |
| Lazy-load | mind a 11 galériakép `loading="lazy" decoding="async"` |
| Akadálymentesség | `aria-label` a 3 szűrő-mezőn, `aria-live` a találatszámlálón (láthatatlan attribútumok) |
| Sorkizárás | lead bekezdés ≥782px justify+hyphens, ≤781px balra (VB-minta) |

### 2. Scoped CSS master szabály (`vb-reviews-470-master`, page=470)

- `body.page-id-470{height:auto;overflow-x:clip;font-family:Raleway;color:#383F40}` — védőháló + brand
- Téma-cím (`wp-block-post-title`) elrejtése ezen az oldalon — megszűnt a cím-duplikáció (A5),
  a SEO-toldalék látszása és a 390px-es árva „M” tördelés
- **Egységes galéria-rács** mindkét Jetpack-galérián: 4/3 arány, `object-fit:cover`, lekerekítés,
  finom árnyék; 3 oszlop → ≤781px 2 → ≤480px 1; csonka utolsó sor középen
- „Archive >” link kontraszt: 3,93:1 → 4,5:1 fölött (#8A6D1F)

### 3. Verifikáció

- **Írás bájt-pontos:** a mentett tartalom SHA-256 = `6165670382dc…` — azonos a lokálisan épített fájllal
- **Invariánsok:** `<img>` 11→11 · `<a>` 4→4 · `<style>` 2→2 · `<script>` 1→1 · doctype 2→0 (szándékos) · title 2→0 (szándékos) · H1 2→1 (szándékos)
- **Élő REST rendered:** 0 doctype, 0 title, 1 H1, 24 blockquote, új kép-URL-ek srcset-tel, dev komment nincs
- **Mind a 4 kép-URL HTTP 200** (CDN-en HEAD-elve)
- **Lokális Playwright QA (harness):** 15/15 szélességen (320–2560px) nincs vízszintes csúszka;
  rács 3/2/1 oszlop; szűrő-script működik (24 → 2 shown országszűrésre); screenshotok a `qa/` mappában
- **MÉG NEM MÉRT élesben, böngészőből:** a scoped CSS tényleges kiíródása + Trustindex-widget render
  (a konténernek nincs közvetlen hálózati hozzáférése a site-hoz — kézi Ctrl+Shift+R ellenőrzés kell)

### 4. Visszaállítási háló

| Elem | Érték |
|---|---|
| Előző revízió (visszaállítási pont) | **23600** (2026-04-26 14:19:19) |
| Új revízió | **26684** (2026-08-21 14:03:25) |
| MCP undo snapshot (tartalom) | action 750 |
| MCP undo snapshot (scoped CSS) | action 751 |
| Backup fájlok | `backup/` mappa (raw, rendered, global CSS, scoped rules — checksummal) |

Baj esetén: `wp_restore_post_revision(470, 23600)` + a scoped szabály törlése
(`wp_css_set_scoped mode=delete rule_id=vb-reviews-470-master`).

---

## NEM nyúltam hozzá — döntést igényel (konzultáció)

1. **A 24 archivált értékelés eredete** (audit 6–7. szekció): 2 szó szerint azonos pár más
   névvel/országgal, 3 közel-azonos pár, sablonos szerkezet. Egyetlen karaktert sem változtattam.
   Kérdés: valódi / régi-visszakereshetetlen / fejlesztési minta? Ettől függ a szekció sorsa.
2. **CTA-sáv (P3):** az oldalon továbbra sincs foglalási link — új tartalom lenne, engedély kell.
3. **AggregateRating schema (P1):** a valós 4,7★/14 adat kimarad a Google-találatból — kis munka, nagy hatás.
4. **Trustindex-sáv a H1 alá (E1):** sorrendváltás, opt-in.
5. **Galéria-tartalom (E3–E5):** duplikált E-Class kép, logókártya a fotók közt, téma-releváns képek — opt-in.
6. **D-csomag:** 3,16 MB TTF → WOFF2 (site-szintű, ~2,8 MB nyereség minden oldalon), dupla Open Sans,
   `| VANBUDAPEST.COM` toldalék a téma-címben — más oldalakat is érint, külön kör + cross-page check.

---

## Fájlok

- `new_content_final.txt` — az élesített post_content pontos másolata
- `vb-reviews-470-master.css` — az élesített scoped CSS
- `scripts/` — a sebészeti csere szkriptjei (minden minta pontosan 1× illeszkedett)
- `backup/` — teljes írás előtti mentések
- `qa/` — lokális Playwright harness + screenshotok (390/781/1440px)
- `live-after/` — élesítés utáni REST rendered pillanatkép
