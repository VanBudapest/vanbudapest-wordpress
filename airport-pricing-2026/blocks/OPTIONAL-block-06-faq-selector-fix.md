# OPCIONÁLIS — #6 (FAQ) blokk: szivárgó `h2{}` / `h3{}` szelektorok namespace alá

**Audit-hivatkozás:** 3. Kód/CSS — „Csupasz h2{}, h3{}, h3 span.flag{} selector – nem namespace-elt, oldalszinten hat” · címke: *kötelező A (L-teszt FAIL)*

**Ezt NEM alkalmaztam automatikusan.** Indok lent, a „Mellékhatás” pontban — döntést igényel.

---

## A hiba

A #6 (Airport FAQ – Multilingual) blokk CSS-ében három szelektor namespace nélkül áll:

```css
h2{text-align:center;color:var(--vb-gold);font-size:clamp(1.8rem,4vw,2.6rem);font-weight:800;margin-bottom:2rem;}
h3{color:var(--vb-gold-light);text-align:left;font-weight:700;margin:1.5rem 0 1rem;display:flex;align-items:center;gap:.5rem;}
h3 span.flag{font-size:1.4rem;line-height:1;}
```

…és lejjebb, a mobil media query-ben:

```css
@media(max-width:640px){.vb-inner{padding:1.2rem;}h2{font-size:1.6rem;}}
```

Mivel a blokk `<style>`-ja az oldal `<head>`-jén kívül, de oldalszinten él, ez a négy szabály **az oldal MINDEN `h2`/`h3` elemére** hat — beleértve a Gutenberg-főcímet a #0 blokkban és minden más szekció címsorát.

## A javítás

A #6 blokk `<style>`-jában cseréld a négy szelektort:

| Régi | Új |
|---|---|
| `h2{text-align:center;color:var(--vb-gold);…` | `.vb-section h2{text-align:center;color:var(--vb-gold);…` |
| `h3{color:var(--vb-gold-light);text-align:left;…` | `.vb-section h3{color:var(--vb-gold-light);text-align:left;…` |
| `h3 span.flag{font-size:1.4rem;line-height:1;}` | `.vb-section h3 span.flag{font-size:1.4rem;line-height:1;}` |
| `@media(max-width:640px){.vb-inner{padding:1.2rem;}h2{font-size:1.6rem;}}` | `@media(max-width:640px){.vb-inner{padding:1.2rem;}.vb-section h2{font-size:1.6rem;}}` |

Négy darab `.vb-section ` előtag beszúrása, semmi más. A #6 blokk saját megjelenése **nem változik** (a szekciója `class="vb-section vb-fw"`).

## ⚠ Mellékhatás — ezért kérek rá külön döntést

A #0 blokk Gutenberg-H2-je (**„Budapest & Hungary- Vienna – Airport Transfers”**) jelenleg **ebből a szivárgásból** kapja a megjelenését: 41,6 px, 800-as vastagság, középre zárva. A `color:var(--vb-gold)` odakint érvénytelen változó, ezért lesz fekete.

A javítás után ez a H2 visszaesik a **téma alapértelmezett** címsor-stílusára — vagyis **láthatóan megváltozik a hajtás feletti címsor**.

Ez összefügg az audit 5. szekciójával (címsor-struktúra) és a D-csomaggal (látható H1 / WP-cím csere), ami külön SEO-döntést igényel. Ezért:

- **Ha a #0 H2 amúgy is átalakul** (audit 5. pont) → ezt a javítást vele egy körben érdemes elvégezni.
- **Ha a #0 H2 marad** → a javítással együtt a #0 blokk H2-jére kell egy szándékos stílus (Gutenberg-beállításból vagy scoped CSS-ből), különben „lecsupaszodik”.

## Az új A/D blokkokat ez NEM érinti

A `block-01` és `block-02` szelektorai (`.vbp-a h2`, `.vbp-a .vbp-veh`, `.vbp-d h2`) specifikusabbak a csupasz `h2{}`/`h3{}`-nál, és minden érintett tulajdonságot — köztük a `display`-t — explicit kiírnak.

Böngészőben ellenőrizve (Chromium, a szivárgó szabályokkal szimulálva):

```
.vbp-a h2  : display:block   color:rgb(255,255,255)  text-align:center  Playfair Display  48px
.vbp-a h3  : display:block   color:rgb(255,255,255)  text-align:left    Playfair Display  22px
.vbp-d h2  : display:block   color:rgb(255,255,255)  text-align:center  Playfair Display  40px
```

`display:block` — vagyis a `h3{display:flex}` szivárgás **nem** töri el a jármű-neveket. Ez akkor is így marad, ha a #6 blokkot soha nem javítjuk.
