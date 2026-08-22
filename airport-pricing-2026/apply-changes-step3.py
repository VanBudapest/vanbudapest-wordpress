import re

c0 = open('live_final2.txt', encoding='utf-8').read()
c = c0
log = []

def rep(label, old, new, expect=1):
    global c
    n = c.count(old)
    assert n == expect, f"FAIL [{label}]: {expect} kellene, {n} van\n  old={old[:160]!r}"
    c = c.replace(old, new)
    log.append(label)

# ---------------------------------------------------------------- 1) Elutes: "Hungary- Vienna" -> "Hungary – Vienna"
rep('Elutes javitva: Hungary – Vienna',
 '<h2>Budapest &amp; Hungary- Vienna – Airport Transfers</h2>',
 '<h2>Budapest &amp; Hungary – Vienna – Airport Transfers</h2>')

# ---------------------------------------------------------------- 2) #3 galeria: width/height + lazy (CLS)
CDN = 'https://spcdn.shortpixel.ai/spio/ret_img,q_cdnize,to_auto,s_webp:avif/vanbudapest.com/wp-content/uploads/'
gal = [
  ('2025/05/budapest-hungary-private-transfer-S-class.png', 'Mercedes S-Class luxury transfer',  1536, 1024),
  ('2025/05/vanbudapest-luxury-vip-sprinter-minibus.png',   'Luxury Sprinter minibus',           1536, 1024),
  ('2025/03/interior1.jpg',                                 'Vehicle interior luxury seating',   1600, 1066),
  ('2025/01/hungary-luxury-vip-transfer.png',               'Hungary VIP luxury transfer',       1536, 1024),
]
for path, alt, w, h in gal:
    old = f'<img src="{CDN}{path}" alt="{alt}">'
    new = f'<img src="{CDN}{path}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'
    rep(f'#3 kep width/height: {path.split("/")[-1]}', old, new)

# ---------------------------------------------------------------- 3) Ajanlatadas: mindenhol 12–24 ora
rep('#3 ajanlat 12 -> 12–24 ora',
 'We’re committed to sending you a personalized quotation within 12 hours.',
 'We’re committed to sending you a personalized quotation within 12–24 hours.')

rep('#5 ajanlat 12 -> 12–24 ora',
 'We’ll follow up within 12 hours to confirm your booking',
 'We’ll follow up within 12–24 hours to confirm your booking')

# ---------------------------------------------------------------- 4) Sofor a terminalban: 10 -> 15 perc
rep('#4 sofor 10 -> 15 perc',
 'enter the terminal approximately 10 minutes after landing',
 'enter the terminal approximately 15 minutes after landing')

# ---------------------------------------------------------------- 5) "25% discount" mondat torlese (premium oldal)
rep('#5 25% discount mondat torolve',
 'Plus, for a limited time, enjoy a 25% discount on your next Budapest Airport Transfer. Whether you',
 'Whether you')


# ---------------------------------------------------------------- 6) Lightbox: elveszett "\n" maradvanyok ("n" szemet a DOM-ban)
#    A #4 blokk lightbox-scriptjebol egy korabbi (nem-hu) mentesi csatorna leszedte a backslash-eket,
#    igy a 'n' betuk szoveges csomopontkent bekerultek a nagyitott kep melle.
rep('#4 lightbox „n" szemet eltavolitva',
 """lb.innerHTML='n        <button class="vb-lightbox-close" aria-label="Close">✕</button>"""
 """n        <figure class="vb-lightbox-figure"><img alt="Expanded image"></figure>n      ';""",
 """lb.innerHTML='<button class="vb-lightbox-close" aria-label="Close">✕</button>"""
 """<figure class="vb-lightbox-figure"><img alt="Expanded image"></figure>';""")

# ---------------------------------------------------------------- 7) Coach kartya: ures cel-oldal -> flotta oldal, egyseges felirat
#    A /coach-bus-vehicle-options/ (page 17870) publikalt, de a tartalma URES -> ures oldal jelent meg.
#    A tobbi 5 kartyaval egyseges: "Vehicle details →" + flotta oldal.
rep('#1 Coach kartya linkje -> flotta oldal, „Vehicle details"',
 '<a class="vbp-link" href="https://vanbudapest.com/coach-bus-vehicle-options/">Coach options &#8594;</a>',
 '<a class="vbp-link" href="https://vanbudapest.com/our-fleet-vip-limousines-coaches-sedans-luxury-vans/">Vehicle details &#8594;</a>')

open('new3.txt', 'w', encoding='utf-8').write(c)
print(f"Lepesek: {len(log)}")
for x in log: print("  OK -", x)
print(f"\nMeret: {len(c0)} -> {len(c)} ({len(c)-len(c0):+d})")
