# -*- coding: utf-8 -*-
"""10. kor - a regi szekciok teljes szelessege + cimsor-elvalasztas."""
import re, hashlib

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
assert len(blocks) == 4
B = 3

ANCHOR = """    /* kepaláirasok: az uj .vbg figcaption mar kozepen van, a regi .vb-card is legyen */
    body.page-id-1351 .vb-section .vb-card small{text-align:center}
"""
ADD = ANCHOR + """
    /* 8) TELJES SZELESSEG. A .vb-fw csak `width:100vw`-t kapott, `max-width`-et
          nem, ezert a sablon egy max-width szabalya visszaszoritotta: mobilon
          feher sav maradt a szekcio jobb oldalan. Az A-kartyak es a D-matrix
          azert jok, mert ott a `max-width:100vw` ki van irva. Ugyanaz ide is. */
    body.page-id-1351 .vb-section.vb-fw{max-width:100vw}

    /* 9) A cimsorok ne toredezzenek elvalasztojellel ("Ex-pectations", "Premi-um"):
          a 8. korben felvett hyphens:auto rajuk is oroklodott. A text-wrap:balance
          egyenletesebb sortoresre bontja a kozepre igazitott cimsorokat. */
    body.page-id-1351 .vb-section h1,
    body.page-id-1351 .vb-section h2,
    body.page-id-1351 .vb-section h3,
    body.page-id-1351 .vb-section h4,
    body.page-id-1351 .vb-section h5,
    body.page-id-1351 .vb-section h6{hyphens:manual;text-wrap:balance}
"""
assert blocks[B].count(ANCHOR) == 1, 'nincs meg a horgony'
blocks[B] = blocks[B].replace(ANCHOR, ADD)

A_START, A_END = '<section class="vbp-a"', '</section>\n<script>'
D_START, D_END = '<section class="vbp-d"', '</section>\n<!-- /wp:html -->'
def sub(s, a, b):
    i = s.find(a); assert i >= 0, a
    j = s.find(b, i); assert j >= 0, b
    return s[i:j+len(b)]
for name, s, e in (('A-kartyak', A_START, A_END), ('D-matrix', D_START, D_END)):
    x, y = sub(orig[0], s, e), sub(blocks[0], s, e)
    assert x == y, '!!! A %s MEGVALTOZOTT !!!' % name
    print('%-10s valtozatlan  sha1 %s' % (name, hashlib.sha1(y.encode()).hexdigest()[:12]))
for i in (0, 1, 2):
    assert blocks[i] == orig[i]
new_css = ADD[len(ANCHOR):]
assert '\\' not in new_css
code = re.sub(r'/\*.*?\*/', '', new_css, flags=re.S)
assert '.vbp-a' not in code and '.vbp-d' not in code
assert re.search(r'([^ ])\1{8,}', blocks[B]) is None, 'hosszu ismetlodo futam'

out = live[:tl[B][1]] + blocks[B] + live[tl[B][2]:]
open('new10_page.txt', 'w', encoding='utf-8').write(out)
open('b3_v10.txt', 'w', encoding='utf-8').write(blocks[B])
print('blokk[3]: %d -> %d | oldal: %d -> %d' % (len(orig[B]), len(blocks[B]), len(live), len(out)))
