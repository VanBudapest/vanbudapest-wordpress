# Client References oldal — v4 újraépítés (2026-08-21)

Élő oldal: https://vanbudapest.com/client-references/ (Page ID 7246)

## Mi történt

A 2026-08-21-i teljes audit (37 törött kép, 0 @media, 24px mobil szövegcsonkolás,
sportolónevek ALT-ban, 175 HTTP-kérés) alapján az oldal teljes újraépítése:

- **17 blokk** (16 eredeti + 1 új StarLadder CS2 Major Budapest 2025 szekció a hero után)
- **63 kép, mind ellenőrzött és élő** (korábban 98-ból 37 törött volt)
- Járműképek a 2026. május óta feltöltött S-Class / V-Class / Sprinter sorozatokból
- StarLadder Major: hivatalos szállítási partner blokk, saját eseményfotókkal + logóval
  (MAJOR-STARLADDER-2025-VB-CS2-MVMDOME-MTKSPORTPARK sorozat, 2026/03)
- Minden szöveg betűre változatlan (automatizált diff-fel ellenőrizve);
  csak az ALT-szövegek frissültek (sportolónevek eltávolítva, téves városnevek javítva)
- Kódszemét törölve: 16× html/body globális selector, 60 halott !important,
  243 inline style, dupla ShortPixel-prefix, wp-block-spacer-ek, rejtett hover-dim trükk
- Új CSS-keretrendszer: `vb-cr-*` namespace, teljes @media kaszkád (1024/781/600/480),
  box-sizing fix, aspect-ratio 3:2 galériák, prefers-reduced-motion, lazy loading + srcset

## Fájlok

- `client-references-v4-post-content.html` — a 7246-os oldal post_content-je (wp:html blokkok)
- `build_page.py` — a tartalom generátora (szöveg-verbatim ellenőrzéssel)

## Scoped CSS (FlowExto plugin, rule_id: vb-cr-page-7246)

```css
body.page-id-7246{overflow-x:hidden}
body.page-id-7246 .wp-block-post-title{display:none}
body.page-id-7246 .entry-content>.wp-block-html{margin-block-start:0;margin-block-end:0}
body.page-id-7246 .entry-content{margin-top:0;margin-bottom:0;padding-top:0;padding-bottom:0}
body.page-id-7246 .wp-block-post-content{margin-top:0;padding-top:0;padding-bottom:0}
body.page-id-7246 #vb-client-references .vb-cr-hero-bg{background-image:url('https://spcdn.shortpixel.ai/spio/ret_img,q_cdnize,to_auto,s_webp:avif/vanbudapest.com/wp-content/uploads/2025/01/hungary-4898894.jpg')}
```

## Visszaállítás

- WP revízió: 26304 (2026-08-05) — `wp_restore_post_revision`
- MCP undo: action_id 757 (tartalom), 758–759 (scoped CSS)
