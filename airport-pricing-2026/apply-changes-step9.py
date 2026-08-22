# -*- coding: utf-8 -*-
"""9. kor - cimsorok kozepre + a regi szekciok mobil igazitasa.
   Csak a blokk[3] (#6 FAQ) <style>-jaba ir; a body.page-id-1351 elotag miatt
   az egesz oldal .vb-section szekcioira hat. Az A-kartyakat (.vbp-a) es a
   D-matrixot (.vbp-d) nem erinti."""
import re, hashlib, sys

SRC = '/home/user/vanbudapest-wordpress/airport-pricing-2026/page-1351-AFTER-live.txt'
live = open(SRC, encoding='utf-8').read()

def toplevel(s):
    out, depth, start = [], 0, None
    for m in re.finditer(r'<!-- (/?)wp:([a-z0-9/-]+)(?: (\{.*?\}))? (/)?-->', s):
        closing, selfclose = m.group(1) == '/', m.group(4) == '/'
        if selfclose:
            if depth == 0: out.append((m.group(2), m.start(), m.end()))
            continue
        if not closing:
            if depth == 0: start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0: out.append((m.group(2), start, m.end()))
    return out

tl = toplevel(live)
blocks = [live[a:b] for _, a, b in tl]
orig = list(blocks)
assert len(blocks) == 4, len(blocks)

B = 3  # #6 FAQ blokk - itt el a reszponziv reteg

# ---- 1) 3. pont: mobilon kozepre igazitas (eddig balra) -------------------
OLD3 = """    /* 3) SORKIZARAS csak ott, ahol elfer. 390px-en 35 karakter/sor + justify
          = szethuzott szokozok ("folyok"); ott balra igazitunk. */
    @media (max-width:900px){
      body.page-id-1351 .vb-section,
      body.page-id-1351 .vb-section .vb-inner,
      body.page-id-1351 .vb-section .vb-content{text-align:left}
    }
"""
NEW3 = """    /* 3) IGAZITAS KIS KIJELZON. 390px-en 35 karakter/sor + justify = szethuzott
          szokozok ("folyok"), a balra igazitas viszont elutott a kozepre igazitott
          A-kartyaktol es D-matrixtol. Ezert mobilon minden kozepre kerul. */
    @media (max-width:900px){
      body.page-id-1351 .vb-section,
      body.page-id-1351 .vb-section .vb-inner,
      body.page-id-1351 .vb-section .vb-content{text-align:center}
      /* a listajelolok kovessek a szoveget, ne ragadjanak a bal szelre */
      body.page-id-1351 .vb-section .vb-list,
      body.page-id-1351 .vb-section .vb-list li{padding-left:0}
      body.page-id-1351 .vb-section .vb-list li::before{
        position:static;display:inline-block;margin-right:.45rem;vertical-align:.08em}
      body.page-id-1351 .vb-section .vb-inner ul{margin-left:0;list-style-position:inside}
    }
"""
assert blocks[B].count(OLD3) == 1, 'a 3. pont nincs meg'
blocks[B] = blocks[B].replace(OLD3, NEW3)

# ---- 2) 5. pont: a FAQ-nyito legyen kozepre igazithato blokk --------------
OLD5 = """    /* 5) TAP-TARGETEK: a FAQ-nyitok 26–29px magasak voltak, ez 44px-re no. */
    body.page-id-1351 .vb-section .vb-faq summary{
      min-height:44px;display:flex;align-items:center;padding-block:4px
    }
"""
NEW5 = """    /* 5) TAP-TARGETEK: a FAQ-nyitok 26–29px magasak voltak, ez 44px-re no.
          A +/− jel az abszolut bal szelrol a szoveg ele kerul, igy az egesz
          kerdes egy egysegkent all kozepre. */
    body.page-id-1351 .vb-section .vb-faq summary{
      display:block;min-height:44px;padding-block:10px;padding-left:0;text-align:center
    }
    body.page-id-1351 .vb-section .vb-faq summary::before{
      position:static;display:inline;margin-right:.45rem;top:auto;left:auto
    }
"""
assert blocks[B].count(OLD5) == 1, 'az 5. pont nincs meg'
blocks[B] = blocks[B].replace(OLD5, NEW5)

# ---- 3) 7. pont: cimsorok es cimkek kozepre, minden kijelzon --------------
OLD6 = """    /* 6) Kep sose logjon ki a savbol. */
    body.page-id-1351 .vb-section img{max-width:100%}
"""
NEW6 = OLD6 + """
    /* 7) CIMSOROK ES CIMKEK KOZEPRE — minden kijelzomereten.
          Eddig a .vb-section h3 balra allt (#4, #5, #6 szekcio), a tobbi cimsor
          mar kozepen volt. Az A-kartyakat (.vbp-a) es a D-matrixot (.vbp-d) ez
          sem erinti: azok sajat, mar kozepre igazitott cimsorokkal jonnek. */
    body.page-id-1351 .vb-section h2,
    body.page-id-1351 .vb-section h3,
    body.page-id-1351 .vb-section h4,
    body.page-id-1351 .vb-section h5,
    body.page-id-1351 .vb-section h6{text-align:center}
    /* a #6 nyelvi cimsorai flex-sorok voltak (zaszlo + szoveg): blokkka alakitva
       a zaszlo a szoveggel egyutt, egy egysegkent kerul kozepre */
    body.page-id-1351 .vb-section h3{display:block}
    body.page-id-1351 .vb-section h3 span.flag{
      display:inline-block;margin-right:.45rem;vertical-align:-.12em}
    /* kepaláirasok: az uj .vbg figcaption mar kozepen van, a regi .vb-card is legyen */
    body.page-id-1351 .vb-section .vb-card small{text-align:center}
"""
assert blocks[B].count(OLD6) == 1, 'a 6. pont nincs meg'
blocks[B] = blocks[B].replace(OLD6, NEW6)

# ---- VEDOKORLAT: az A-kartyak es a D-matrix bytera valtozatlan ------------
A_START, A_END = '<section class="vbp-a"', '</section>\n<script>'
D_START, D_END = '<section class="vbp-d"', '</section>\n<!-- /wp:html -->'
def sub(s, a, b):
    i = s.find(a); assert i >= 0, a
    j = s.find(b, i); assert j >= 0, b
    return s[i:j+len(b)]
for name, s, e in (('A-kartyak', A_START, A_END), ('D-matrix', D_START, D_END)):
    x, y = sub(orig[0], s, e), sub(blocks[0], s, e)
    assert x == y, '!!! A %s MEGVALTOZOTT - ez tilos !!!' % name
    print('%-10s valtozatlan  sha1 %s  (%d kar)' % (name, hashlib.sha1(y.encode()).hexdigest()[:12], len(y)))
for i in (0, 1, 2):
    assert blocks[i] == orig[i], 'blokk[%d] nem maradhat valtozatlan!' % i

# ---- semmi visszaper, semmi A/D-hivatkozas az uj CSS-ben ------------------
new_css = NEW3 + NEW5 + NEW6
assert '\\' not in new_css
code = re.sub(r'/\*.*?\*/', '', new_css, flags=re.S)
assert '.vbp-a' not in code and '.vbp-d' not in code, 'az uj CSS nem nyulhat az A/D blokkhoz'

out = live[:tl[B][1]] + blocks[B] + live[tl[B][2]:]
open('new9_page.txt', 'w', encoding='utf-8').write(out)
open('b3_v9.txt', 'w', encoding='utf-8').write(blocks[B])
print('blokk[3]: %d -> %d kar' % (len(orig[B]), len(blocks[B])))
print('oldal   : %d -> %d kar' % (len(live), len(out)))

# ---- a dekorativ vonalak lecserelese ------------------------------------
# 64 es 63 hosszu "=" futam volt a komment-keretben; ezek atvitelnel konnyen
# elcsusznak (a 8. korben tenylegesen elcsusztak). Sima kommentre cserelem.
import re as _re
_b = blocks[B]
_b = _re.sub(r'/\* ═+\n', '/* ---------------------------------------------------------------\n', _b)
_b = _re.sub(r'\n\s*═+ \*/', '\n       --------------------------------------------------------------- */', _b)
assert '═' not in _b, 'maradt dekorativ karakter'
assert len(_re.findall(r'-{3,}', _b)) == 2, _re.findall(r'-{3,}', _b)
blocks[B] = _b
out = live[:tl[B][1]] + blocks[B] + live[tl[B][2]:]
open('new9_page.txt', 'w', encoding='utf-8').write(out)
open('b3_v9.txt', 'w', encoding='utf-8').write(blocks[B])
print('dekoracio cserelve; blokk[3] = %d kar, oldal = %d kar' % (len(blocks[B]), len(out)))
