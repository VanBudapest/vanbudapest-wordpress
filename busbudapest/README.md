# Bus Budapest — busbudapest.wordpress.com implementáció

A Claude Design `Bus Budapest.dc.html` prototípus (lásd `design/`) élő implementációja
a busbudapest.wordpress.com (busbudapest.com) WordPress.com **Simple** oldalon.

## Mi hol van élesben

| Elem | Hely |
|------|------|
| Főoldal (page ID **9**, slug `home`) | https://busbudapest.com/ — 4 top-level blokk: nav (wp:html) · hero→vélemények (wp:html) · quote (wp:group + columns + Jetpack form) · FAQ+footer (wp:html) |
| Site-szintű CSS (`site.css`) | Global Styles `css` mező (Site Editor → Styles → Additional CSS) — a sanitizer érintetlenül átengedte |
| `front-page` sablon | Site Editor → Templates — üres sablon (nincs téma-fejléc/lábléc/cím, kötetlen szélesség); a főoldal automatikusan ezt használja |
| Quote űrlap | Jetpack Form — a beküldések a wp-admin **Visszajelzések** menübe és a site-tulajdonos e-mailjére mennek |

## Architektúra (belt-and-braces)

A WordPress.com Simple oldalakon a KSES **kiszűri** a `<style>` blokkot, a `<script>`-et és a
`<nav>` taget, az inline style-okból pedig a `transform`, `color-scheme`, `resize`,
`scroll-margin-top` tulajdonságokat és az `rgba()` függvényt (empirikusan igazolva).
Ezért:

- **Alap-elrendezés**: kizárólag inline style-ok, önmagukban reszponzív mintákkal
  (auto-fit grid, flex-wrap, clamp(), 1px-gap hajszálvonal, 8 jegyű hex az rgba helyett,
  `position:relative;top:` a translateY helyett). A CSS nélkül is működik.
- **Finomítás** (`site.css` a Global Styles-ban): media query-k, hover, sticky
  admin-bar offset, Jetpack űrlap-stílus, `body.home` fallbackok arra az esetre,
  ha a főoldal valaha kötött sablonban renderelne.

## Tudatos placeholder-ek (a designból, cserélendők élesítés előtt)

- **WhatsApp**: `+36 70 000 0000` (wa.me link) — 3 helyen (hero, quote, footer)
- **E-mail**: `hello@busbudapest.com` — 2 helyen (quote, footer)
- **Vélemények**: 3 minta "SAMPLE — REPLACE" jelöléssel
- **Fotók**: kép-sáv + 4 flotta-kártya sraffozott placeholder ("Photo coming soon")
- Footer felirat: "PLACEHOLDER SITE — REPLACE CONTACT & PHOTOS BEFORE LAUNCH"

## Betűtípusok

Archivo / Space Mono Google Fonts a Simple oldalon nem tölthető be (a sanitizer
minden @import-ot kiszűr, a Font Library nem elérhető ezen a csomagon). Font-stackek:
`'Archivo','Inter',Helvetica,Arial,sans-serif` és `'Space Mono','Courier New',monospace`
— az Inter a téma betöltött alapfontja, a Courier New rendszer-mono.

## Karbantartás

- A tartalom blokkonként szerkeszthető: `page-sections.list` → `page-sections.replace`
  (WordPress.com MCP). Az editorban a quote-szekció columns blokkjára SOHA ne nyomj
  "Attempt Block Recovery"-t (a kézzel írt inline style-t törölné; a site.css duplikálja).
- A CSS frissítése: `site.css` → Global Styles `css` mező (`global-styles.update`).
