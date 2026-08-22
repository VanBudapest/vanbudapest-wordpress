# -*- coding: utf-8 -*-
# 6. kor — MINDEN CTA gomb/link uj lapon nyiljon.
#   target="_blank"  -> uj ful
#   rel="noopener"   -> a megnyilo lap ne fejen at a window.opener-hez (biztonsag + teljesitmeny)
# A mailto: linket SZANDEKOSAN kihagyom: ott a target="_blank" csak egy ures fület nyit,
# a levelezo ugyis kulon alkalmazasban indul.
import re

blocks = {i: open(f'b{i}_v5.txt', encoding='utf-8').read() for i in range(4)}
orig   = dict(blocks)
log    = []

# a CTA-osztalyok, amelyekre vonatkozik
CTA_CLASSES = ('vbp-btn', 'vbp-link', 'vb-cta')

def add_blank(bi):
    """Minden CTA-osztalyu <a> tag-re raakasztja a target/rel attributumokat."""
    b = blocks[bi]
    n = 0
    def sub(m):
        nonlocal n
        tag = m.group(0)
        if 'target=' in tag:            # mar van rajta -> nem nyulunk hozza
            return tag
        cls = re.search(r'class="([^"]*)"', tag)
        if not cls or not any(c in cls.group(1).split() for c in CTA_CLASSES):
            return tag
        n += 1
        return tag[:-1] + ' target="_blank" rel="noopener">'
    blocks[bi] = re.sub(r'<a\b[^>]*>', sub, b)
    if n:
        log.append((bi, f'{n} db CTA link -> target="_blank" rel="noopener"'))
    return n

total = 0
for i in range(4):
    total += add_blank(i)

# ---- ellenorzesek
assert total == 25, f"25 CTA linket vartam, {total} lett"
allhtml = ''.join(blocks.values())
tags = re.findall(r'<a\b[^>]*>', allhtml)
cta  = [t for t in tags if (re.search(r'class="([^"]*)"', t) and
        any(c in re.search(r'class="([^"]*)"', t).group(1).split() for c in CTA_CLASSES))]
assert len(cta) == 25, len(cta)
assert all('target="_blank"' in t and 'rel="noopener"' in t for t in cta), 'nem mindegyiken van rajta'
mailto = [t for t in tags if 'mailto:' in t]
assert len(mailto) == 1 and 'target=' not in mailto[0], 'a mailto-t nem szabad megfogni'

for i, b in blocks.items():
    open(f'b{i}_v6.txt', 'w', encoding='utf-8').write(b)

print(f"CTA linkek osszesen: {total}\n")
for bi, lab in log: print(f"  OK - [b{bi}] {lab}")
print()
for i in range(4):
    d = len(blocks[i]) - len(orig[i])
    print(f"  blokk[{i}]: {len(orig[i])} -> {len(blocks[i])} ({d:+d})" + ('  <-- CSERELNI' if d else '  valtozatlan'))
