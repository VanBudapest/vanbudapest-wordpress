# Careers oldal (13604) — javítási jelentés · 2026-08-21

**Oldal:** https://vanbudapest.com/luxury-transportation-careers/ · Page ID: 13604
**Alap:** VanBudapest_Careers_oldalaudit_20260821.html (Evelin-skill audit)
**Csatorna:** kizárólag scoped CSS (`vb-careers-13604-master` szabály) + médiatár + featured image.
**A post_content-hez egyetlen bájt erejéig sem nyúltunk** — a 0 revíziós helyzet miatt ez volt az egyetlen biztonságos út.

## Elvégzett javítások (jóváhagyott kör)

| # | Tétel | Megoldás |
|---|-------|----------|
| 1 | #1 blokk bekezdései aranyból vissza **fehérre** (kaszkád-baleset) | scoped CSS |
| 2 | #2 kártya-gombok + sticky gomb ghost-ból vissza **tömör aranyra** | scoped CSS |
| 3 | #1 blokk elveszett függőleges belső tere visszaállítva (80px) | scoped CSS |
| 4 | **Fekete .vb-footer csík** a #3 blokkban semlegesítve (site-lábléc CSS szivárgott be) | scoped CSS, !important |
| 5 | Fordított szivárgás a valódi láblécre (font-weight:600, 1.05rem, letter-spacing) semlegesítve | scoped CSS |
| 6 | **Blokkok közötti 36px fehér varratok** eltüntetve — folyamatos navy háttér | scoped CSS |
| 7 | 320–367px kártya-levágás (48px) javítva: `minmax(min(320px,100%),1fr)` | scoped CSS |
| 8 | Mobil sticky sáv: `fixed` → `sticky` a #2 blokkon belül — **nem takarja többé a #3 blokkot és a lábléc fizetési logóit** | scoped CSS |
| 9 | Sorkizárt szöveg: ≤781px balra zárt, ≥782px justify + hyphens:auto | scoped CSS |
| 10 | Címek fix rem → `clamp()` (320px-en nem lóg ki, desktopon változatlan méret) | scoped CSS |
| 11 | `prefers-reduced-motion` kivétel | scoped CSS |
| 12 | Bevezető kép aspect-ratio (CLS-védelem) | scoped CSS |
| 13 | Fejléc-logó átfedés enyhítése 1200–1500px között (wrapper oldalpadding 110px) | scoped CSS |
| 14 | **4 licenc-kockázatos kép cserélve** (audit: kötelező) — fal.ai flux-2-pro + nano-banana-2/edit, arc/felirat/logó nélkül, vision-QA után: <br>• Customer Service → concierge-pult (ID 26705) <br>• Marketing (OG-kép is volt!) → navy-arany moodboard (ID 26706) <br>• Social Media → Lánchíd + telefon (ID 26707) <br>• Host/Hostess → budapesti báltermi welcome-pult (ID 26708) | scoped CSS `content:url()` |
| 15 | **OG/featured kép**: 13611 (stock, 474×316) → **10795** (V-Class Hősök tere, 1536×1024) | featured image |

## Verifikáció

- Lokális Chromium harness (before/after, 320/390/768/1440): minden mérés PASS — nincs vízszintes csúszka, varratok 36px→0, kártya 320px-en már nem lóg ki (368→272px jobb szél), gombok tömör aranyak, lábléc font-weight 400-ra állt vissza, a lábléc saját megjelenése érintetlen.
- Élő oldal (mshots screenshot + vision QA, 1280px): tömör arany gombok ✓, fehér bevezető bekezdések ✓, folyamatos sötét háttér ✓, arany záró sor (nincs fekete csík) ✓, customer service kártyán az új arc-nélküli kép ✓, törött kép 0 ✓.
- Mind a 4 új kép CDN-en HEAD 200 (AVIF/WebP, 27–60 KB).
- Tartalom-ujjlenyomat a munka előtt és után: SHA-256 `dc89a3bd…d51b0003` — **változatlan** (bitre egyezik az auditéval).

## Visszaállítás

- Scoped CSS: a `vb-careers-13604-master` szabály törlése (plugin undo action_id: 781); teljes szabály-backup: `scoped_css_rules_backup_20260821_1434.json`
- Featured image vissza: `wp_set_featured_image(13604, 13611)`
- Új képek: attachment 26705, 26706, 26707, 26708 (törölhetők, ha vissza kell állni)

## Nem nyúltunk hozzá (jóváhagyás hiányában) — döntést igényel

1. „Introductory Section" H3 — látható fejlesztői munkacím, de **szöveg** (C-csomag, tételes jóváhagyás kell).
2. Chauffeur.jpg duplikáció (2 kártya ugyanazzal a képpel), Sales/Tour Guide/S-Class képek — audit szerint opt-in.
3. Hero-kép a cím mögé, 4 oszlopos rács / középre zárt utolsó sor, Playfair címek, sticky sáv karcsúsítása — opt-in dizájn.
4. ALT-szövegek a tartalomban (a képcsere CSS-szintű, a HTML alt nem változott), aria-label, mailto tárgysor, width/height attribútumok — tartalom-szerkesztést (Application Password) igényel.
5. Cím-hármas (rejtett H1 / téma-cím / blokk-cím), „award-winning" a metában, téma-font (1,64 MB TTF) — C/D csomag.

## Költség (fal.ai)

4× flux-2-pro (~$0,10) + 4× nano-banana-2/edit ($0,32) + vision QA (~$0,02) ≈ **$0,45**

---

## Kiegészítés (2026-08-21, v2)

Tomi kérésére a **4 kártyakép-csere visszavonva** — az eredeti képek maradnak a karrier-kártyákon
(a scoped CSS 10. szekciója eltávolítva, undo action_id: 782). Minden más javítás változatlanul él.
A generált képek a médiatárban maradtak (ID 26705–26708), később bármikor felhasználhatók vagy törölhetők.
Az OG/featured kép (13611 → 10795, V-Class Hősök tere) egyelőre az új — szólj, ha ezt is vissza kell állítani.
