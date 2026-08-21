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

## 2. körre maradt (audit szerint)
- fal.ai képek: hero „V-Class szivárványos zebránál", Pride-fleet kép, évszak-
  semleges Prága (a médiatárban nincs Prága-kép) – vanbudapest-fal-media skill
- Valódi E-Class sorozatkép kiválasztása (vizuális ellenőrzéssel)
- de/es/fr fordítások frissítése (Lingexto stale-ellenőrzés – a képcserék ott még nem élnek)
- Ajánlások/“(verified)” hitelesítése vagy Google-bizonyítékra cserélése
- Ár-oldalak bekötése a CTA-kba; FAQPage schema; emoji-stratégia; téma-betű woff2;
  ShortPixel újrafuttatás a >1 MB-os origin fájlokra
