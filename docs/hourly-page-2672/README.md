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
- `page-2672-new-content-2026-08-23.html` — the full new `post_content` (177 453 chars).
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
