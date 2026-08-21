# Clean Luxury Transfers (Page ID 2594) — audit-javítások, 2026-08-21

Forrás: `VanBudapest_COVIDHygieneoldal_teljesaudit_20260821.html` (Evelin-skill + Master Prompt v3.0)

| | |
|---|---|
| **Régi URL** | `https://vanbudapest.com/covid-hungary-private-bus-airport-transfer/` |
| **Új URL** | `https://vanbudapest.com/clean-hungary-private-bus-airport-transfer/` |
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

## Utólagos kör (2026-08-21, jóváhagyás után)

### 1. #10 galéria 4. képe → V-Class flotta-fotó
`55106-disinfected-…-5.jpg` (a #6 galéria duplikátuma) → média **21048**
(`/V-Class-fleet/flotta/…-086.webp`, 1440×1080, 281 KB).
Ezzel **0 duplikált kép-URL** maradt az oldalon.
Új `post_content` SHA-256: `84e640d3c18b2d60f8306a3593892deda070279632bf85cb0844d95534fd92f9` (64 042 kar.).
⚠️ Ezt a képet én nem láttam — az audit sem ellenőrizte vizuálisan. Ha rendszám
vagy nem odaillő tartalom látszik rajta, egyetlen `<img>` cseréje a javítás.

### 2. TikTok-link
Marad a jelenlegi `tiktok.com/@vanbudapest` (döntés szerint). A Facebook / X /
Instagram már a jóváhagyott hivatalos fiókokra mutat.

### 3. 301 átirányítás — WPCode snippet #26547

A snippet elkészült és **publikálva** van:

| | |
|---|---|
| Post ID | **26547** |
| Cím | `VB 301 - Clean Luxury (2594) regi COVID slug atiranyitas` |
| Típus / hely | `wpcode_type=php` · `wpcode_location=everywhere` |
| Státusz | publish, `_wpcode_auto_insert=1`, `_wpcode_priority=10` |
| Korábbi tartalom | „VB Mobil Menu v2.1" elavult draft — bájtpontosan visszaállítható az MCP snapshotból (**action_id 820**) |

**Még nem fut**, mert a WPCode az aktív snippeteket a `wpcode_snippets`
option-ben gyorsítótárazza, és ezt csak a saját mentési útvonala építi újra —
a `wp_update_post` nem váltja ki. A gyorsítótár írás előtti állapota:
`backup_wpcode_snippets_20260821.json`.

**Amit tenni kell (kb. 10 másodperc):**
WP Admin → **Code Snippets** → „VB 301 - Clean Luxury (2594)…" megnyitása →
**Update** gomb. Ez újraépíti a gyorsítótárat, és a 301 azonnal él.

Ellenőrzés utána:
`https://vanbudapest.com/covid-hungary-private-bus-airport-transfer/` →
**301** → `https://vanbudapest.com/clean-hungary-private-bus-airport-transfer/`
