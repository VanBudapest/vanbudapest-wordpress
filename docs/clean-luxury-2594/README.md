# Clean Luxury Transfers (Page ID 2594) — audit-javítások, 2026-08-21

Forrás: `VanBudapest_COVIDHygieneoldal_teljesaudit_20260821.html` (Evelin-skill + Master Prompt v3.0)

| | |
|---|---|
| **URL** | `https://vanbudapest.com/covid-hungary-private-bus-airport-transfer/` — **változatlan** (a slug-csere visszavonva, lásd lent) |
| **Visszaállítási pont** | WP revízió **#23530** (2026-04-25 16:33:52) |
| **Backup (post_content, ELŐTTE)** | `backup_post_content_BEFORE_20260821.html` — 63 719 kar., SHA-256 `bájtpontosan az élő állapot` |
| **Új tartalom (UTÁNA)** | `post_content_AFTER_20260821.html` — 64 009 kar., SHA-256 `143ec3828be9822cd6dbea4efc0fea61b757a2aa2ff0d6bb2daefe4b4c30b574` |

## Adatcsatorna — fontos tanulság

- Az MCP `wp_get_post` **kizárólag a `<style>` / `</style>` tageket vágja le**, minden más (entitások, emoji, inline `style=`, `<details>`) bájtpontos. Ez próbaoldalon mérve.
- Az MCP `wp_update_post` **bájtpontosan ír** — a `<style>` blokkok sértetlenül mennek át (a `VB — Grant unfiltered_html to admins (MCP fix)` WPCode snippet miatt).
- Ezért a raw tartalom determinisztikusan rekonstruálható: minden `</section>` után álló CSS-szövegcsomópontot `<style>`-be kell visszacsomagolni (pontosan 15 db, +225 kar. = 15 × 15).

## Integritás-változástábla

| mérőszám | előtte | utána | szándékos? |
|---|---|---|---|
| kar. | 63 719 | 64 009 | igen |
| `wp:html` | 15 | 15 | változatlan ✔ |
| `<style>` | 15 | 15 | változatlan ✔ |
| `<section>` | 15 | 15 | változatlan ✔ |
| `<img>` | 17 | 17 | változatlan ✔ |
| `<a>` | 33 | 33 | változatlan ✔ |
| `@media` | 6 | 6 | változatlan ✔ |
| `@keyframes` / `!important` / `position:fixed` / `id=` | 0 | 0 | változatlan ✔ |
| H1 / H2 | 1 / 15 | 1 / 15 | változatlan ✔ |
| H3 | 17 | 1 | **igen** — a 16 kontakt-csempe felirat `<h3>` → `<p class="vb-h3">` (nem tartalmi alcím) |
| COVID/pandemic/corona | 21 | 16 | **igen** — mind a 16 a #14 archív blokkban |
| `wp:paragraph` | 4 | 0 | **igen** — 2 üres bekezdés-blokk (kódszemét) törölve |

## Fájlok

- `patch_2594.py` — a sebészeti csere-szkript. Minden csere pontos előfordulás-számot ellenőriz, eltérésnél leáll.
- `scoped-css-2594-master.css` — a `vb-cleanluxury-2594-master` scoped szabály (priority 20, scope: page/2594).
- `redirect-301-wpcode-snippet.php` — **még nincs élesítve**, lásd lent.
- `backup_global_css_20260821.css` — globális Additional CSS (57 194 bájt, SHA-256 `64809fb745ded4fd39027f074691be09211f243ff6d1a8fa02c9d74b2ad0b267`) — NEM módosult.
- `backup_scoped_css_rules_20260821.json` — a 42 scoped szabály írás előtti állapota (utána 43).

## Nyitott pont — 301 átirányítás

A régi URL jelenleg **404**. A WordPress beépített `_wp_old_slug` átirányítása ezen a
permalink-struktúrán **page** típusnál nem sül el: a rewrite csak `pagename` query-vart
állít be, a `wp_old_slug_redirect()` viszont `name`-et vár. (A `_wp_old_slug` meta
be van írva, de önmagában nem elég.)

A megoldás a `redirect-301-wpcode-snippet.php` tartalma WPCode-ba (PHP Snippet,
Run Everywhere, Active). Az MCP nem enged `wpcode` post típust létrehozni
(„post_type »wpcode« is not exposed via UI/public”), ezért ez kézi vagy külön
jóváhagyást igénylő lépés.

---

## Utólagos kör (2026-08-21) — a slug-csere VISSZAVONVA

Döntés: a slug maradjon a régi, mert a 301 átirányításhoz WPCode-beavatkozás
kellett volna. **Minden más javítás érvényben van.**

| lépés | állapot |
|---|---|
| `post_name` | vissza `covid-hungary-private-bus-airport-transfer`-re · a régi URL **200 OK** |
| `_wp_old_slug` meta | törölve (nem kell) |
| WPCode #26547 | **draft + `_wpcode_auto_insert=0`** → inert, nem tud elsülni. Címe: `[INAKTIV] VB 301 slug-atiranyitas - NEM HASZNALNI` |

⚠️ **Amit el kell mondani:** a #26547-es snippet korábban a „VB Mobil Menu v2.1
(2026-08-14)" elavult DRAFT-ot tartalmazta, és a bővítmény changelogja **nem
mentett `before_state`-et** (`mcp_get_change_detail` → `before_state: null`),
ezért a v2.1 törzse a szerverről nem állítható vissza. Ez nem kritikus: az élő
verzió a **v3.3 (#26556)**, és a **v3.1 (#26550)** + **v3.2 (#26551)** draftok
érintetlenek. A v2.1 forrása a snippet saját jegyzete szerint:
`03-WEBSITE-VANBUDAPEST/webdev/mobil-menu-v2/`.

### Ami maradt a helyén (a slug-visszaállítás ezeket NEM érinti)

- COVID kiszedve a #10 blokkból; a #14 archív blokkban marad (16 említés)
- törött kép pótolva, 4 duplikált kép lecserélve → **0 duplikált kép-URL**
- hero ALT + `fetchpriority`, 16 képre `loading=lazy` + `decoding=async`
- 16 social link, hero CTA, 8 emoji-kép, halott CSS, 2 üres bekezdés
- H3→P a kontakt-csempéken, 8 `aria-label`, `lang` attribútumok
- scoped CSS MASTER (`vb-cleanluxury-2594-master`)
- meta description, OG-kép 1200×630 / 231 KB

Aktuális `post_content`: 64 042 kar. ·
SHA-256 `84e640d3c18b2d60f8306a3593892deda070279632bf85cb0844d95534fd92f9`

### Reszponzív mérés (Chromium 1194, 15 szélesség, lokális blokk-render)

`measure.json` · előtte/utána képernyőképek: `visual-report.html`

- **0 vízszintes túllógás** 320–2560 px-en, előtte és utána is
- galéria-oszlop: előtte 1/2/3/4/5/**8** → utána fix **1/2/3**
- oldalmagasság: 900 px-en **−29%**, 1440 px-en **−26%**, 390 px-en −8%
  (mobilon kisebb, mert a #14 microcopy szándékosan **nagyobb** lett: 11–13 px → 14–15,5 px)

A mérés a 15 `wp:html` blokk lokális újrarenderelésén készült (valódi kód +
valódi inline CSS + az új scoped CSS), a téma fejléce/lábléce és a fényképek
nélkül — az abszolút magasságok ezért kisebbek az élő oldalénál, az arányok és
az oszlopszámok viszont valósak.

---

## Kép-méretezés javítás (2026-08-21, 3. kör)

**Gyökérok:** a galéria flex-cellái `min-width:auto`-val futottak. Amíg a
`loading="lazy"` képek nem töltöttek be, a rács jó volt; betöltés után viszont a
kép saját 1536 px-es intrinsic mérete szétfeszítette a cellát, és **1 kép került
egy sorba, teljes szélességben**. 2560 px-en ez 776×517 px-es „bélyegképet",
a #8 blokkban 1080×720 px-es képet jelentett.

**Javítás** (`vb-cleanluxury-2594-master`, priority 20):

| | |
|---|---|
| `min-width:0` + `max-width:100%` a galéria- és split-képekre | a flex-basis végre érvényesül |
| galéria-doboz `max-width:min(1140px,92vw)` + `margin-inline:auto` | 1920/2560 px-en sem fúvódik fel |
| oszlopszám | `<820px` 2 · `820–1099px` 3 · `≥1100px` 4 |
| `.vb-split__media` `max-width:420px` | a #8 blokk képei 340 px-en megállnak |

**Mérés végiggörgetés után** (`verify.js` → `verify_after.txt`), hogy minden
lazy kép betöltsön:

- legnagyobb galéria-kép **bármekkora képernyőn: 273 px** (előtte 776 px)
- 0 vízszintes túllógás mind a 15 szélességen
- oldalmagasság: 2560 px-en **−33%**, 1440 px-en **−30%**, 390 px-en **−18%**
- az egyetlen „kilógó" elem a hero `img.vb-bg__image` — ez szándékos
  (`transform:scale(1.03)`, a szekció `overflow:hidden`-je levágja)

## Mi maradt hátra az auditból

Tételes lista: `audit-hatralevo-tetelek.html`, illetve a `visual-report.html`
végén. Nyolc csoport: (1) üzleti döntést igénylő állítások, (2) szövegmódosítás,
(3) képek (ALT-ok, width/height, srcset, origin-súly, CDN-purge), (4) tartalom
törlése, (5) globális, (6) konverzió/SEO javaslatok, (7) amit szándékosan
kihagytam, (8) amit innen nem tudok megmérni.
