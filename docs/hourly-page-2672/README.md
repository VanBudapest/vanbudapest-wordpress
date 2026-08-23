# Hourly Rates page (ID 2672) — 2026-08-23 redesign

Live page: https://vanbudapest.com/price-bus-rental-cost-hourly-ride/

Implements the prototypes from the 2026-08-22 audit (`vb-oradij-prototipusok.html`)
and the copy proposal (`vb-hourly-copy-proposal.html`).

## New block order on the page

| # | Block | Source |
|---|-------|--------|
| 1 | `<style>` only — the whole `.vbh-*` stylesheet | `vbh-blocks.css` |
| 2 | **A** — Rate cards + hours switcher (3/4/6/8/12 h) | prototype A |
| 3 | **B** — Hourly price calculator | prototype B |
| 4 | **Price Information** — existing approved copy, restyled | live page (kept) |
| 5 | **C** — Hourly Rates at a Glance (rate card, no side-scroll) | prototype C |
| 6 | **F** — How Hourly Hire Works | prototype F |
| 7 | **D** — Day Trips from Budapest | prototype D |
| 8 | **E** — When Hourly Hire Beats Single Transfers | prototype E |
| 9 | promo block (unchanged, moved down) | live page (kept verbatim) |

## Files

- `BACKUP-page-2672-original-2026-08-23.html` — the **raw** `post_content` before the change
  (138 688 chars, 7 `<style>`, 1 `<script>`, 62 `<img>`). Restore point.
- `page-2672-live-after-2026-08-23.html` — the `post_content` **as it is live now**
  (179 797 chars, 6 `<style>`, 1 `<script>`, 82 `<img>`, 0 `<table>`, 0 backslashes).
- `blocks/block_*.html` — each new top-level Gutenberg block on its own, ready to paste.
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

| Vehicle | 3–6 h | 7–11 h | 12 h |
|---|---|---|---|
| Mercedes E-Class | €65 | €60 | €55 |
| Mercedes V-Class | €70 | €65 | €60 |
| Mercedes Sprinter | €75 | €70 | €65 |
| Mercedes S-Class | €110 | €105 | €100 |
| Mercedes VIP Sprinter | €85 | €80 | €75 |
| Coach Bus | €120 | €110 | €100 |

Every total includes the +1 garage hour.


## What was done on the live page (2026-08-23)

Written block by block through the WordPress.com `page-sections.*` operations, so the
blocks that were not part of this task were never rewritten and could not be damaged.
Every write returned `_content_warnings: []` and each block was verified byte-for-byte
against `blocks/block_*.html` afterwards.

Removed: the old `Pricing table` group (the `.vb-hourly-cards--v20` cards, the
`Budapest - Hourly ride` H3) and the old `.vb-hcalc` calculator with its horizontally
scrolling price table.

Kept untouched: hero + H1, the intro block, the promo block (moved up one level out of
its column wrapper), and blocks 12–20.

Side effect worth knowing: ShortPixel re-prefixed its own CDN URL onto the
`background-image:url()` values in the old calculator on **every** save, so those URLs had
grown to five nested `spcdn.shortpixel.ai/spio/...` prefixes. Removing that block removed
the problem. ShortPixel also CDN-ized the `-600x400` image URLs in blocks B and C once
(normal, not nested) — that is why those two blocks differ from `blocks/block_B.html`
and `blocks/block_C.html` by exactly the CDN prefix.

## Still open — needs a decision

1. **The promo block still uses banned words** — `discount` × 6 (`vanbudapest-rules`:
   never write discount / affordable / budget / cheap). It was kept verbatim because
   removing it was not part of this task. Its message (7 h+ lower rate, full-day rate)
   is now covered by blocks A, B, C and F, so it can be dropped or rewritten.
2. `affordable` × 1 and `budget` × 1 remain in block 17 (the untouched
   "Transparent and Reliable Pricing" columns block).
3. **S-Class is now €110 / €105** on the new blocks, per ÁRAZÁS2026ÚJ.xlsx. The old FAQ
   block further down the page still says "around €135 per hour" (EN/DE/ES) — those three
   answers now contradict the rate cards and need the same correction.
4. **12 h band**: the new blocks price 12 h at the `DISCOUNT` band (E-Class €715).
   If city hourly hire should stay on the 7 h+ rate (€780), flip `APPLY_12` to `false`
   in the rate engine and update the `12 h` cells in block C.
5. The hero image is still the 2025 ChatGPT render with an empty `alt`, and the H1 is
   still invisible white-on-white — both were outside this task.
