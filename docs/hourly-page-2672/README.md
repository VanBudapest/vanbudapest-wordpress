# Hourly Rates page (ID 2672) — 2026-08-23 redesign

Live page: https://vanbudapest.com/price-bus-rental-cost-hourly-ride/

Implements the prototypes from the 2026-08-22 audit (`vb-oradij-prototipusok.html`)
and the copy proposal (`vb-hourly-copy-proposal.html`).

## New block order on the page

| # | Block | Source |
|---|-------|--------|
| 0 | `core/cover` — hero + H1 (image replaced 2026-08-23) | live page |
| 1 | `<style>` only — the whole `.vbh-*` stylesheet | `vbh-blocks.css` |
| 2 | **A** — Intro copy + rate cards + hours switcher (3/4/6/8/12 h) | prototype A |
| 3 | **B** — Hourly price calculator | prototype B |
| 4 | **Price Information** — existing approved copy, restyled | live page (kept) |
| 5 | **C** — Hourly Rates at a Glance (rate card, no side-scroll) | prototype C |
| 6 | **F** — How Hourly Hire Works | prototype F |
| 7 | **D** — Day Trips from Budapest | prototype D |
| 8 | **E** — When Hourly Hire Beats Single Transfers | prototype E |
| 9 | promo block (unchanged, moved down) | live page (kept verbatim) |
| 10 | legacy gallery group (`.vb-section`, 12 grids × 4 images) | live page |
| 11 | uniform-tile CSS override for those grids | added 2026-08-23 |

Four own-photo galleries and their stylesheet were then interleaved between the
blocks above, so the final order on the page is:

| # | Block |
|---|-------|
| 0 | hero cover |
| 1 | `.vbh-*` stylesheet |
| 2 | **`.vbg-*` gallery stylesheet** |
| 3 | A — rate cards |
| 4 | **fleet marquee** (18 photos, two auto-scrolling rows) |
| 5 | B — calculator |
| 6 | Price Information |
| 7 | **Budapest strip I** (4 photos) |
| 8 | C — rate card at a glance |
| 9 | F — how hourly hire works |
| 10 | **vans & minibuses bento** (14 photos) |
| 11 | D — day trips |
| 12 | **Budapest strip II** (4 photos) |
| 13 | E — when hourly beats single transfers |
| 14 | **sedans / SUV / EQE mosaic** (14 photos) |
| 15 | promo block |
| 16 | legacy gallery group |
| 17 | uniform-tile CSS |

## Files

- `BACKUP-page-2672-original-2026-08-23.html` — the **raw** `post_content` before the change
  (138 688 chars, 7 `<style>`, 1 `<script>`, 62 `<img>`). Restore point.
- `page-2672-live-after-2026-08-23.html` — the `post_content` **as it is live now**
  (181 104 chars, 8 `<style>`, 1 `<script>`, 0 `<table>`, 0 backslashes).
- `blocks/block_*.html` — each new top-level Gutenberg block on its own, ready to paste.
  `block_GALLERY.html` is the legacy `.vb-section` group after the image repair;
  `block_TILECSS.html` is the uniform-tile override; `block_VBG*.html` are the
  own-photo galleries and their stylesheet.
- `vbg-galleries.css` — the `.vbg-*` gallery stylesheet, extracted.
- `vbh-blocks.css` / `vbh-rate-engine.js` — the stylesheet and the rate engine, extracted.
- `preview-standalone.html` — open in a browser to see all seven sections without WordPress.

## Notes for future edits

- **Never** round-trip `post_content` through a tool that strips `<style>`/`<script>`.
  The raw content is only safe via the WordPress.com `page-sections.*` operations or the
  MCP changelog `before_state`/`after_state` snapshots.
- The rate engine is written **without regular expressions on purpose** — a Gutenberg/KSES
  round trip eats backslashes, which is what broke the previous calculator (it printed
  `€1755` instead of `€1 300` and lost its thousands separator).
- Namespace is `.vbh-*`. The page's older blocks use `.vb-section` / `.vb-fw`; the two
  systems must stay separate or they overwrite each other's backgrounds.
- Full-bleed is `.vbh-fw` (`width:100vw; margin-left:calc(50% - 50vw)`), with
  `margin-top/bottom:0` so there is no white strip between the sections.

## Rates (ÁRAZÁS2026ÚJ.xlsx, 2026-08-22)

**Two bands only** — 3+1 h and 7+1 h, exactly as in the price file. There is no 12-hour band.

| Vehicle | 3–6 h | 7–12 h |
|---|---|---|
| Mercedes E-Class | €65 | €60 |
| Mercedes V-Class | €70 | €65 |
| Mercedes Sprinter | €75 | €70 |
| Mercedes S-Class | €110 | €105 |
| Mercedes VIP Sprinter | €85 | €80 |
| Coach Bus | €120 | €110 |

Every total includes the +1 garage hour, so 12 h with you is billed as 13 h:
780 / 845 / 910 / 1 365 / 1 040 / 1 430.


## What was done on the live page (2026-08-23)

Written block by block through the WordPress.com `page-sections.*` operations, so the
blocks that were not part of this task were never rewritten and could not be damaged.
Every write returned `_content_warnings: []` and each block was verified byte-for-byte
against `blocks/block_*.html` afterwards.

Removed: the old `Pricing table` group (the `.vb-hourly-cards--v20` cards, the
`Budapest - Hourly ride` H3), the old `.vb-hcalc` calculator with its horizontally
scrolling price table, the standalone intro `core/html` block (its copy now lives inside
block A) and the `core/separator` that sat between the hero and block A.

Kept untouched: the H1, the promo block (moved up one level out of its column wrapper),
and the legacy blocks below the promo.

### Second pass, same day

- **Intro copy folded into block A.** "Curious about the cost of renting a vehicle in
  Budapest?" now renders as `.vbh-ask` (italic Playfair, `--vb-gold-light`) directly under
  the H2 `Private Driver & Mercedes by the Hour`, with the original paragraph below it as
  `.vbh-lead`. The wording is unchanged — it was moved, not rewritten. The old standalone
  block above the cards was then deleted so the copy is not duplicated.
- **Two rate bands only**, per ÁRAZÁS2026ÚJ.xlsx. The engine is now
  `rate(v, h) { return h >= 7 ? v.r[1] : v.r[0]; }` with two-value `r` arrays; block C lost
  its third column, its `t3` rows and every `7–11 h` label; the hours switcher label went
  from `long day · lowest rate` to `long day`. Hours 8–12 all bill at the 7+1 rate.
- **Hero image replaced**: `BLACK-MERCEDES.png` (id 25987, 1672×941, 16:9), `sizeSlug: full`
  so it is not upscaled, a navy `#0A1F44` overlay at 60 % so the white H1 is legible, and a
  real `alt`. The previous white Sprinter render is untouched in the media library.
- The `core/separator` between the hero and block A was removed, so the cover's navy runs
  straight into block A's navy with a measured 0 px gap.

Side effect worth knowing: ShortPixel re-prefixed its own CDN URL onto the
`background-image:url()` values in the old calculator on **every** save, so those URLs had
grown to five nested `spcdn.shortpixel.ai/spio/...` prefixes. Removing that block removed
the problem. ShortPixel also CDN-ized the `-600x400` image URLs in blocks B and C once
(normal, not nested) — that is why those two blocks differ from `blocks/block_B.html`
and `blocks/block_C.html` by exactly the CDN prefix.

### Third pass — broken images (2026-08-23)

Every image URL on the page was HEAD-checked from the server (the container cannot
reach vanbudapest.com; the egress policy blocks it, so the checks ran through the
WordPress HTTP API). 66 distinct references, **11 broken `<img>` slots**, all of them
inside the legacy gallery group.

Six were the *same picture under a filename that no longer exists* — repaired by
pointing at the file that is actually on disk, so the artwork did not change:

| Grid | Was (404) | Now |
|---|---|---|
| B, L | `2020/04/7416d-castle-transfer-budapest.jpg` | `…-1.webp` |
| D ×2 | `res.cloudinary.com/dmrjcw98n/…47/…28.webp` (401) | the local `2022/05/…47/…28.webp` |
| F | `2024/05/budapest_jichang_shuttle-1.jpeg` | `…-1-1.webp` |
| I | `2025/06/Matild-Palace-1.jpg` | `Matild-Palace.jpg` |

Five files are genuinely gone from the server, so they were replaced from the media
library with pictures that fit the grid's theme, and the `alt` text was rewritten to
match what is now shown:

| Grid | Was | Now | New alt |
|---|---|---|---|
| E | `puskas-stadium-budapest-rent-bus-arena.jpg` | `2026/07/Athletics5.png` | Budapest stadium at dusk |
| E | `puskas-stadium-transfer-bus.jpg` | `2026/06/vb-img-1781984373031.png` | Chauffeur at event venue |
| E | `puskas-stadium-budapest-rent-bus-hungary.jpg` | `2026/07/ferencvaros-europa-league-2026-27-hero-1.jpg` | Budapest match night |
| G | `Holloko_Easter_Festival_Hungary_2025.jpg` | `2026/06/7ecacd3f-…-332f6ae63e6e.png` | Budapest skyline sunset |
| I | `lgbtq-vanbudapest.jpg` | `2025/11/pride.lgbtq_.vanbudapest.webp` | Pride parade Budapest |

Grid G's slot held a Hollókő village photo inside a grid titled *Budapest Scenes*, so a
Budapest skyline replaced it; the Pride photo keeps the original intent of the LGBTQ+
slot with a file that still exists.

All 48 gallery cards, all 4 bento cards, the block CSS (byte-identical) and every
paragraph of copy survived the rewrite unchanged — only the 11 image sources, their
link targets and 5 `alt` strings differ. After the write all 66 references and all 44
lightbox links return 200.

### Uniform gallery tiles

The grids used `height:auto`, so a row of mixed aspect ratios left empty navy strips
under the shorter pictures. Block 11 fixes it without touching the gallery markup:

    .vb-section .vb-grid .vb-card img,
    .vb-section .vb-bento-grid .vb-bento-card img{
      width:100%;height:auto;aspect-ratio:3/2;
      object-fit:cover;object-position:center top;display:block}

`cover` scales proportionally and only crops what cannot fit; `center top` takes that
crop off the **bottom**. The block sits after the gallery so it wins on source order,
and each selector carries one extra class so it also wins on specificity. Measured in
Chromium at 1440 / 768 / 390 px with sources from 1:1 to 2.29:1: all 13 grids uniform,
card height minus image height = 2 px everywhere (the card's own 1 px borders).

### Fourth pass — own-photo galleries (2026-08-23)

54 photographs the owner supplied as their own — 8 Budapest locations and 46 fleet
shots — distributed across four galleries so neither kind clumps in one place. All 54
URLs were HEAD-checked from the server first; all returned 200.

| Gallery | Placement | Photos | Layout |
|---|---|---|---|
| The Mercedes You Actually Get | after the rate cards | 18 fleet | two auto-scrolling rows, opposite directions, edge fades |
| Where Your Hours Take You | after Price Information | 4 Budapest | 4-up portrait strip, tiles 2–3 offset downward |
| Room for the Whole Group | after How Hourly Hire Works | 14 vans | 4-column bento, dense packing |
| The City You See From the Car | after Day Trips | 4 Budapest | same offset strip |
| Every Class, Photographed | after When Hourly Hire Wins | 14 sedans/SUV/EQE + chauffeur | auto-fit mosaic |

Written as six separate `page-sections.insert` calls (stylesheet + five sections) from
the bottom of the page upward, so no earlier index shifted mid-run and no existing
block was rewritten. Every write returned `_content_warnings: []`.

Notes:

- The marquee is **CSS-only** — a flex track holding each row twice, animated to
  `translateX(-50%)`, so the loop is seamless with no JavaScript. It pauses on hover
  and stops entirely under `prefers-reduced-motion: reduce`.
- Tiles use `object-fit: cover` on a fixed `aspect-ratio`, the same rule as the legacy
  grids, so mixed source ratios still tile evenly.
- Captions sit in `<figcaption>` and fade in on hover or keyboard focus
  (`:focus-within`), so they are reachable without a mouse.
- Every image carries `loading="lazy"` and `decoding="async"` except the first three
  marquee tiles, which are the only ones above the fold.
- Alt text is derived from what the filename reliably encodes (the vehicle class) or,
  for the four files whose names say nothing, from the alt already stored in the media
  library. Nothing about the photographs was invented.
- Measured in Chromium at 1440 / 768 / 390 px with source ratios from 3:4 to 2:1:
  all 12 full-bleed sections span the viewport exactly, **every gap between them is
  0 px**, and there is no horizontal page scroll.

## Still open — needs a decision

1. **The promo block still uses banned words** (left in place on purpose for now) — `discount` × 6 (`vanbudapest-rules`:
   never write discount / affordable / budget / cheap). It was kept verbatim because
   removing it was not part of this task. Its message (7 h+ lower rate, full-day rate)
   is now covered by blocks A, B, C and F, so it can be dropped or rewritten.
2. `affordable` × 1 and `budget` × 1 remain in block 17 (the untouched
   "Transparent and Reliable Pricing" columns block).
3. **S-Class is now €110 / €105** on the new blocks, per ÁRAZÁS2026ÚJ.xlsx. The old FAQ
   block further down the page still says "around €135 per hour" (EN/DE/ES) — those three
   answers now contradict the rate cards and need the same correction.
4. ~~12 h band~~ — **resolved**: the price file has only 3+1 and 7+1, so the third band
   was removed from the engine, from block C (totals, column heads, legends) and from the
   hours switcher label in block A.
5. ~~Hero image / invisible H1~~ — **resolved**: the cover now uses `BLACK-MERCEDES.png`
   with a 60 % `#0A1F44` overlay and a descriptive `alt`, and the H1 reads white on navy.
6. The `MOST POPULAR` badge on the V-Class is a marketing choice, confirmed by the owner
   (V-Class is the most-booked category). It is not derived from booking data, so it should
   not be presented as a statistic anywhere.
