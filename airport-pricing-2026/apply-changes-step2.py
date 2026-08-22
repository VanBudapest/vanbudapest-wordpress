import re

c0 = open('cur.txt', encoding='utf-8').read()
c = c0
log = []

def rep(label, old, new, expect=1):
    global c
    n = c.count(old)
    assert n == expect, f"FAIL [{label}]: {expect} db kellene, {n} van\n  old={old[:150]!r}"
    c = c.replace(old, new)
    log.append(label)

def cut(label, start_marker, end_marker):
    """Kivágja a start_marker-tol az end_marker vegeig (mindketto egyedi kell legyen)."""
    global c
    i = c.find(start_marker)
    assert i >= 0, f"FAIL [{label}]: start nem talalhato"
    assert c.count(start_marker) == 1, f"FAIL [{label}]: start nem egyedi ({c.count(start_marker)})"
    j = c.find(end_marker, i)
    assert j >= 0, f"FAIL [{label}]: end nem talalhato"
    j += len(end_marker)
    # a kovetkezo ures sorokat is levágjuk
    while c[j:j+1] == '\n':
        j += 1
    c = c[:i] + c[j:]
    log.append(label)

# ============================================================ 1) #0 GROUP: padding -> 0
rep('#0 group padding -> 0 (attributum)',
 '"className":"alignfull","style":{"spacing":{"padding":{"top":"calc( 0.5 * var(u002du002dwpu002du002dstyleu002du002drootu002du002dpadding-right, var(u002du002dwpu002du002dcustomu002du002dgapu002du002dhorizontal)))","bottom":"calc( 0.5 * var(u002du002dwpu002du002dstyleu002du002drootu002du002dpadding-right, var(u002du002dwpu002du002dcustomu002du002dgapu002du002dhorizontal)))","left":"var(u002du002dwpu002du002dstyleu002du002drootu002du002dpadding-left, var(u002du002dwpu002du002dcustomu002du002dgapu002du002dhorizontal))","right":"var(u002du002dwpu002du002dstyleu002du002drootu002du002dpadding-right, var(u002du002dwpu002du002dcustomu002du002dgapu002du002dhorizontal))"},"margin":{"top":"0","bottom":"0"}}},"layout":{"type":"constrained","justifyContent":"center"}} -->\n<div class="wp-block-group alignfull" style="margin-top:0;margin-bottom:0;padding-top:calc( 0.5 * var(--wp--style--root--padding-right, var(--wp--custom--gap--horizontal)));padding-right:var(--wp--style--root--padding-right, var(--wp--custom--gap--horizontal));padding-bottom:calc( 0.5 * var(--wp--style--root--padding-right, var(--wp--custom--gap--horizontal)));padding-left:var(--wp--style--root--padding-left, var(--wp--custom--gap--horizontal))">',
 '"className":"alignfull","style":{"spacing":{"padding":{"top":"0","bottom":"0","left":"0","right":"0"},"margin":{"top":"0","bottom":"0"}}},"layout":{"type":"constrained","justifyContent":"center"}} -->\n<div class="wp-block-group alignfull" style="margin-top:0;margin-bottom:0;padding-top:0;padding-right:0;padding-bottom:0;padding-left:0">')

# ============================================================ 2) A #0 CIMSOROK KIVETELE (atkerulnek az A-blokkba)
cut('#0 nyito spacer',
 '<!-- wp:spacer {"height":"calc( 0.25 * var(u002du002dwpu002du002dstyleu002du002drootu002du002dpadding-right, var(u002du002dwpu002du002dcustomu002du002dgapu002du002dhorizontal)))"} -->\n<div style="height:calc( 0.25 * var(--wp--style--root--padding-right, var(--wp--custom--gap--horizontal)))" aria-hidden="true" class="wp-block-spacer"></div>\n<!-- /wp:spacer -->\n\n<!-- wp:heading {"style":{"typography":{"textAlign":"center"}},"className":"vb-page-h2"} -->',
 '<!-- /wp:heading -->')
# ^ ez egyben kivagja: nyito spacer + H2 blokk

cut('#0 spacer + 2 db H6',
 '<!-- wp:spacer {"height":"var:preset|spacing|30","width":"0px"} -->',
 '<h6 class="wp-block-heading has-text-align-center">Airport Transfer Rates \u2014 Budapest (BUD), Bratislava (BTS) &amp; Vienna (VIE)</h6>\n<!-- /wp:heading -->')

# ============================================================ 3) SEPARATOROK + URES ELEMEK a #0 group-on belul
SEP = '<!-- wp:separator -->\n<hr class="wp-block-separator has-alpha-channel-opacity" />\n<!-- /wp:separator -->\n\n'
n = c.count(SEP)
assert n == 2, f"FAIL: 2 separator kellene a group-ban, {n} van"
c = c.replace(SEP, '')
log.append('#0 group: 2 separator torolve')

cut('#0 zaro ures paragraph + spacer',
 '<!-- wp:paragraph -->\n<p></p>\n<!-- /wp:paragraph -->\n\n<!-- wp:spacer {"height":"calc( 0.25 * var(u002du002dwpu002du002dstyleu002du002drootu002du002dpadding-right, var(u002du002dwpu002du002dcustomu002du002dgapu002du002dhorizontal)))"} -->',
 '<!-- /wp:spacer -->')

# ============================================================ 4) TOP-LEVEL: spacer + separator + URES group + zaro paragraph
cut('top-level 27px spacer + separator + URES "Hero Product 3 Split" group',
 '<!-- wp:spacer {"height":"27px"} -->',
 '<div style="height:calc( 0.25 * var(--wp--style--root--padding-right, var(--wp--custom--gap--horizontal)))" aria-hidden="true" class="wp-block-spacer"></div>\n<!-- /wp:spacer --></div>\n<!-- /wp:group -->')

assert c.rstrip().endswith('<!-- /wp:paragraph -->'), "a vegen nem ures paragraph all"
c = c.rstrip()[:-len('<!-- wp:paragraph -->\n<p></p>\n<!-- /wp:paragraph -->')].rstrip() + '\n'
log.append('top-level zaro ures paragraph torolve')

# ============================================================ 5) A-BLOKK FEJLEC: a #0 cimsorai ide kerulnek
rep('A-blokk fejlec: cimsorok lehozva',
 '''  <div class="vbp-wrap">
    <p class="vbp-eyebrow">Fixed, published rates · Since 1988</p>
    <h2>Airport Transfer Rates</h2>
    <p class="vbp-sub">Private chauffeur transfers between your Budapest address and Budapest (BUD), Vienna (VIE) or Bratislava (BTS) airport. One price per vehicle, not per person.</p>''',
 '''  <div class="vbp-wrap">
    <p class="vbp-eyebrow">Fixed, published rates · Since 1988</p>
    <h2>Budapest &amp; Hungary- Vienna – Airport Transfers</h2>
    <h6 class="vbp-kicker"><strong>Airport Transfers to Budapest  – Reliable, Comfortable, and Stress-Free</strong></h6>
    <h6 class="vbp-kicker">Airport Transfer Rates — Budapest (BUD), Bratislava (BTS) &amp; Vienna (VIE)</h6>
    <p class="vbp-sub">Private chauffeur transfers between your Budapest address and Budapest (BUD), Vienna (VIE) or Bratislava (BTS) airport. One price per vehicle, not per person.</p>''')

# ============================================================ 6) A-BLOKK CSS: kicker + a WP wrapperek reseinek nullazasa
rep('A-blokk CSS: kicker + wrapper-resek',
 '''  .vbp-a .vbp-sub{display:block;text-align:center;color:#c9d3e6;font-size:clamp(15px,1.6vw,17px);max-width:640px;margin:0 auto 30px}''',
 '''  .vbp-a .vbp-sub{display:block;text-align:center;color:#c9d3e6;font-size:clamp(15px,1.6vw,17px);max-width:640px;margin:14px auto 30px}
  .vbp-a .vbp-kicker{display:block;margin:10px 0 0;font:600 clamp(11px,1.15vw,13px)/1.5 var(--vb-font-head);letter-spacing:.14em;text-transform:uppercase;color:var(--vb-gold-light);text-align:center}
  .vbp-a .vbp-kicker strong{font-weight:700;color:#fff}
  /* Az oldal blokk-wrapperei ne hagyjanak feher rest a szekciok kozott (csak ezen az oldalon) */
  body.page-id-1351 .wp-block-columns,
  body.page-id-1351 .wp-block-column,
  body.page-id-1351 .wp-block-group{margin-block-start:0;margin-block-end:0;row-gap:0}
  body.page-id-1351 .entry-content>*{margin-block-start:0;margin-block-end:0}''')

open('new2.txt', 'w', encoding='utf-8').write(c)
print(f"Lepesek: {len(log)}")
for x in log: print("  OK -", x)
print(f"\nMeret: {len(c0)} -> {len(c)} ({len(c)-len(c0):+d})")
