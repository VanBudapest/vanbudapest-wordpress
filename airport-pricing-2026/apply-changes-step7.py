# -*- coding: utf-8 -*-
# 7. kor — GALERIA-BOVITES.
#   Csak a GALERIAKAT erinti. Az A-kartyakat es a D-matrixot NEM (byte-azonos marad).
#   19 uj kep a medistarbol, mind az 5 kategoriabol (E / S / V-Class, Sprinter, VIP Sprinter),
#   2025. majusa utani feltoltesekbol.
import re, hashlib

CDN = 'https://spcdn.shortpixel.ai/spio/ret_img,q_cdnize,to_auto,s_webp:avif/vanbudapest.com/wp-content/uploads/'

blocks = {i: open(f'b{i}_v6.txt', encoding='utf-8').read() for i in range(4)}
orig   = dict(blocks)
log    = []

def rep(bi, label, old, new, expect=1):
    n = blocks[bi].count(old)
    assert n == expect, f"FAIL [b{bi} {label}]: {expect} kellene, {n} van\n  old={old[:170]!r}"
    blocks[bi] = blocks[bi].replace(old, new)
    log.append((bi, label))

# ══════════════════════════════════════════════════════════════════ 1) UJ GALERIA-CSS
# Sajat nevter (.vbg-*), hogy ne utkozzon a meglevo .vb-gallery / .vb-card szabalyokkal,
# amik blokkok kozott is atszivarognak. Fix oszlopszam -> minden sor teljes, nincs arva csempe.
VBG_CSS = """
    /* ===== VBG · flotta-galeria (2026-08) — fix oszlopszam, egyforma csempek ===== */
    .vbg{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:26px 0 8px}
    .vbg figure{position:relative;margin:0;border-radius:14px;overflow:hidden;
      background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);
      box-shadow:0 10px 28px rgba(0,0,0,.28);
      transition:transform .35s ease,box-shadow .35s ease,border-color .35s ease}
    .vbg figure:hover{transform:translateY(-4px);border-color:rgba(200,181,96,.55);
      box-shadow:0 18px 40px rgba(0,0,0,.42)}
    .vbg img{display:block;width:100%;height:100%;aspect-ratio:4/3;object-fit:cover;
      transition:transform .6s ease}
    .vbg figure:hover img{transform:scale(1.05)}
    .vbg figcaption{position:absolute;left:0;right:0;bottom:0;padding:30px 10px 9px;
      font:600 11px/1.35 'Montserrat','Segoe UI',system-ui,sans-serif;letter-spacing:.06em;
      color:#fff;text-align:center;text-shadow:0 1px 3px rgba(0,0,0,.6);
      background:linear-gradient(180deg,rgba(5,14,35,0),rgba(5,14,35,.9))}
    @media (max-width:900px){.vbg{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}
    /* Telefonon vizszintesen huzhato, nagy csempek — ugyanaz a minta, mint az arkartyaknal */
    @media (max-width:560px){
      .vbg{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;
        padding-bottom:10px;scrollbar-width:thin;scrollbar-color:rgba(200,181,96,.6) transparent}
      .vbg figure{flex:0 0 78%;scroll-snap-align:center}
      .vbg figcaption{font-size:12px;padding:34px 12px 11px}
    }
    @media (prefers-reduced-motion:reduce){.vbg figure,.vbg img{transition:none}
      .vbg figure:hover{transform:none}.vbg figure:hover img{transform:none}}
"""

def fig(path, alt, cap):
    return (f'<figure><img src="{CDN}{path}" alt="{alt}" loading="lazy" decoding="async">'
            f'<figcaption>{cap}</figcaption></figure>')

def gallery(label, items):
    inner = '\n        '.join(fig(*it) for it in items)
    return f'<div class="vbg" aria-label="{label}">\n        {inner}\n      </div>'

# ══════════════════════════════════════════════════════════════════ 2) BLOKK [0] — #3 galeria (4 -> 8)
rep(0, '#3 CSS: .vbg hozzaadva',
 '    @media (max-width:640px) { .vb-inner { padding: 1.5rem; } .vb-inner h2 { font-size: 1.6rem; } }\n',
 '    @media (max-width:640px) { .vb-inner { padding: 1.5rem; } .vb-inner h2 { font-size: 1.6rem; } }\n' + VBG_CSS)

G3_OLD = re.search(r'<div class="vb-gallery" aria-label="Luxury fleet gallery">.*?</div>',
                   blocks[0], re.S).group(0)
G3 = gallery('Luxury fleet gallery', [
  ('2025/05/budapest-hungary-private-transfer-S-class.png',        'Mercedes S-Class luxury transfer',            'Mercedes S-Class'),
  ('2025/05/vanbudapest-luxury-vip-sprinter-minibus.png',          'Luxury Sprinter minibus',                    'Luxury VIP Sprinter'),
  ('2025/03/interior1.jpg',                                        'Vehicle interior luxury seating',            'Interior · lounge seating'),
  ('2025/01/hungary-luxury-vip-transfer.png',                      'Hungary VIP luxury transfer',                'Hungary · VIP transfer'),
  # --- uj ---
  ('2026/06/Mercedes_S-class_VanBudapest-10.webp',                 'Mercedes-Benz S-Class sedan for premium Budapest airport transfers', 'S-Class · exterior'),
  ('2026/06/Mercedes_S-class_VanBudapest-28.webp',                 'Mercedes S-Class interior with quilted leather seats and ambient lighting', 'S-Class · quilted leather'),
  ('2026/08/V-CLASS_VANBUDAPEST_FLEET_MERCEDES-02.webp',           'Black Mercedes V-Class luxury van for Budapest airport transfers', 'Mercedes V-Class'),
  ('2026/06/Mercedes_VIP_Sprinter_minibus_VanBudapest-05.webp',    'Luxury Mercedes VIP Sprinter minibus interior with premium leather seats', 'VIP Sprinter · cabin'),
])
rep(0, '#3 galeria: 4 -> 8 kep, uj .vbg racs', G3_OLD, G3)

# ══════════════════════════════════════════════════════════════════ 3) BLOKK [1] — #4 galeriak
rep(1, '#4 CSS: .vbg hozzaadva',
 '    @media (prefers-reduced-motion:reduce){ .vb-dot{ animation:none; } .vb-card{ transition:none; } }\n',
 '    @media (prefers-reduced-motion:reduce){ .vb-dot{ animation:none; } .vb-card{ transition:none; } }\n' + VBG_CSS)

def swap_gallery(label, items):
    old = re.search(r'<div class="vb-gallery" aria-label="' + re.escape(label) + r'">.*?</div>',
                    blocks[1], re.S).group(0)
    rep(1, f'#4 „{label}”: {old.count("<figure")} -> {len(items)} kep', old, gallery(label, items))

# --- 1) Airport terminals: 2 -> 4
swap_gallery('Airport terminals gallery', [
  ('2025/10/Budapest-Airport-BUD-vanbudapest.jpg',                 'Budapest Airport BUD terminal',              'Budapest Airport (BUD)'),
  ('2025/10/bratislava-airport-terminal-vanbudapest.webp',         'Bratislava Airport terminal',                'Bratislava Airport (BTS)'),
  ('2026/06/Mercedes_VIP_Sprinter_minibus_VanBudapest-44.webp',    'Mercedes VIP Sprinter vans at the Budapest airport transfer facility', 'VIP Sprinter · airport pickup'),
  ('2026/06/Mercedes_S-class_VanBudapest-42.webp',                 'Mercedes S-Class in the Budapest airport transfer garage', 'S-Class · airport garage'),
])

# --- 2) Budapest travel moments: 3 -> 8 (kulsok)
swap_gallery('Budapest travel moments gallery', [
  ('2025/01/budapest-hungary-2025-luxury-private-transfer-12.jpg', 'Luxury transfer in Budapest',                'Luxury transfer · Budapest'),
  ('V-Class-fleet/kulso/vanbudapest-mercedes-v-class-wedding-car-budapest-038.webp', 'Mercedes in Budapest',   'Mercedes · city arrival'),
  ('V-Class-fleet/kulso/vanbudapest-mercedes-v-class-wedding-car-budapest-017.webp', 'Budapest skyline with car', 'Budapest skyline'),
  # --- uj ---
  ('2026/08/V-CLASS_VANBUDAPEST_FLEET_MERCEDES-05.webp',           'Black Mercedes V-Class parked on a Budapest street', 'V-Class · Budapest street'),
  ('2026/08/vanbudapest-vclass-bratislava-luxury-arrival-1.webp',  'Mercedes V-Class arriving beside the Danube in Bratislava', 'V-Class · Bratislava arrival'),
  ('2026/06/Mercedes_E-class_VanBudapest-38.webp',                 'Mercedes E-Class sedan with illuminated taillights, Budapest airport transfer', 'E-Class · evening transfer'),
  ('2026/05/black-sprinter-budapest-disposal-05.webp',             'Mercedes-Benz Sprinter for private airport and group transfers in Budapest', 'Sprinter · group transfer'),
  ('2026/06/Mercedes_VIP_Sprinter_minibus_VanBudapest-37.webp',    'Black Mercedes VIP Sprinter for Budapest airport private transfers', 'VIP Sprinter · Budapest'),
])

# --- 4) Extra visuals: 3 -> 8 (belsok)
swap_gallery('Extra visuals gallery', [
  ('2025/02/OIP.jpeg',                                             'Iconic travel moment',                       'Travel moment'),
  ('2025/02/letoltes-1.jpeg',                                      'Service quality',                            'Service quality'),
  ('2022/01/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcGQxOS0zLTE0MzEwYS5qcGc.webp', 'Travel route', 'Routes across CEE'),
  # --- uj ---
  ('2026/06/Mercedes_S-class_VanBudapest-09.webp',                 'Mercedes S-Class interior with cream leather seats', 'S-Class · cream leather'),
  ('2026/06/Mercedes_S-class_VanBudapest-25.webp',                 'Mercedes-Benz S-Class rear cabin set up for executive work', 'S-Class · executive cabin'),
  ('2026/08/V-CLASS_VANBUDAPEST_FLEET_MERCEDES-17.webp',           'Interior of a Mercedes V-Class minivan for Budapest airport transfers', 'V-Class · cabin'),
  ('2026/08/V-CLASS_VANBUDAPEST_FLEET_MERCEDES-26.webp',           'Mercedes V-Class interior with premium grey leather seats', 'V-Class · grey leather'),
  ('2026/05/black-sprinter-budapest-disposal-20.webp',             'Mercedes-Benz Sprinter minibus interior with leather seats and modern lighting', 'Sprinter · minibus cabin'),
])

# --- 5) Final highlight: 1 -> 4
swap_gallery('Final highlight image', [
  ('V-Class-fleet/flotta/vanbudapest-luxury-van-airport-shuttle-budapest-030.webp', 'Premium chauffeur detail', 'Premium details'),
  # --- uj ---
  ('2026/08/V-CLASS_VANBUDAPEST_FLEET_MERCEDES-01.webp',           'Black Mercedes V-Class for premium Budapest airport transfers', 'V-Class · fleet'),
  ('2026/06/Mercedes_E-class_VanBudapest-36.webp',                 'Black Mercedes E-Class sedan in a modern Budapest parking garage', 'E-Class · Budapest'),
  ('2026/06/Mercedes_VIP_Sprinter_minibus_VanBudapest-35.webp',    'Black Mercedes VIP Sprinter for premium Budapest airport transfers', 'VIP Sprinter · premium'),
])

# --- lightbox: az uj .vbg kepek is nyiljanak nagyban
rep(1, '#4 lightbox: .vbg kepek is kattinthatok',
 "var cards=root.querySelectorAll('.vb-card img');",
 "var cards=root.querySelectorAll('.vb-card img, .vbg img');")

# ══════════════════════════════════════════════════════════════════ 4) VEDELMI ELLENORZESEK
# Az A-kartyak es a D-matrix BYTE-AZONOS kell maradjon.
def sub(txt, start, end):
    i = txt.index(start); j = txt.index(end, i) + len(end)
    return txt[i:j]

A_START, A_END = '<section class="vbp-a"', '</section>\n<script>'
D_START, D_END = '<section class="vbp-d"', '</section>\n<!-- /wp:html -->'
for name, s, e in (('A-kartyak', A_START, A_END), ('D-matrix', D_START, D_END)):
    a, b = sub(orig[0], s, e), sub(blocks[0], s, e)
    assert a == b, f"!!! A {name} MEGVALTOZOTT — ez tilos !!!"
    print(f"  vedelmi ellenorzes: {name} bajtra valtozatlan  "
          f"({len(a)} kar., sha1 {hashlib.sha1(a.encode()).hexdigest()[:12]})")
# a route-valto JS is erintetlen
assert orig[0].count("var labels={bud:'BUD',vie:'VIE',bts:'BTS'};") == 1
assert blocks[0].count("var labels={bud:'BUD',vie:'VIE',bts:'BTS'};") == 1

# uj kepek szama
allhtml = blocks[0] + blocks[1]
newpaths = ['Mercedes_S-class_VanBudapest-10','Mercedes_S-class_VanBudapest-28','FLEET_MERCEDES-02',
            'VIP_Sprinter_minibus_VanBudapest-05','VIP_Sprinter_minibus_VanBudapest-44',
            'Mercedes_S-class_VanBudapest-42','FLEET_MERCEDES-05','vclass-bratislava',
            'Mercedes_E-class_VanBudapest-38','disposal-05','VIP_Sprinter_minibus_VanBudapest-37',
            'Mercedes_S-class_VanBudapest-09','Mercedes_S-class_VanBudapest-25','FLEET_MERCEDES-17',
            'FLEET_MERCEDES-26','disposal-20','FLEET_MERCEDES-01','Mercedes_E-class_VanBudapest-36',
            'VIP_Sprinter_minibus_VanBudapest-35']
assert len(newpaths) == 19
for p in newpaths:
    assert allhtml.count(p) == 1, f"{p}: {allhtml.count(p)}"

# minden .vbg galeria csempeszama oszthato 4-gyel ES 2-vel (szimmetrikus minden torespontban)
for bi in (0, 1):
    for m in re.finditer(r'<div class="vbg" aria-label="([^"]+)">(.*?)</div>', blocks[bi], re.S):
        lab, body = m.group(1), m.group(2)
        n = body.count('<figure>')
        assert n % 4 == 0, f"[b{bi}] „{lab}”: {n} csempe — nem oszthato 4-gyel"
        print(f"  .vbg „{lab}”: {n} csempe (4 oszlop -> {n//4} teli sor, 2 oszlop -> {n//2} teli sor)")

for i, b in blocks.items():
    open(f'b{i}_v7.txt', 'w', encoding='utf-8').write(b)

print(f"\nLepesek: {len(log)}")
for bi, lab in log: print(f"  OK - [b{bi}] {lab}")
print()
for i in range(4):
    d = len(blocks[i]) - len(orig[i])
    print(f"  blokk[{i}]: {len(orig[i])} -> {len(blocks[i])} ({d:+d})" + ('  <-- CSERELNI' if d else '  valtozatlan'))
