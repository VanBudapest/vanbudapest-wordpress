import re, json, hashlib, sys

RAW = 'raw_content.txt'
c0 = open(RAW, encoding='utf-8').read()
c = c0
applied = []

def rep(label, old, new, expect=1):
    """Exact replacement with strict occurrence check."""
    global c
    n = c.count(old)
    assert n == expect, f"FAIL [{label}]: expected {expect} occurrence(s), found {n}\n  old={old[:120]!r}"
    c = c.replace(old, new)
    applied.append(label)

# ---------------------------------------------------------------- 1) #1 CARDS -> Concept A
A = open('/home/user/vanbudapest-wordpress/airport-pricing-2026/blocks/block-01-airport-pricing-cards-A.html', encoding='utf-8').read().rstrip('\n')
D = open('/home/user/vanbudapest-wordpress/airport-pricing-2026/blocks/block-02-price-matrix-D.html', encoding='utf-8').read().rstrip('\n')

def replace_html_block(aria, newcontent, label):
    """Replace the inner content of the wp:html block whose <section> has this aria-label."""
    global c
    hits = [m.start() for m in re.finditer(r'<!-- wp:html -->', c)]
    tgt = None
    for s in hits:
        e = c.find('<!-- /wp:html -->', s)
        if f'aria-label="{aria}"' in c[s:e]:
            assert tgt is None, f"FAIL [{label}]: aria-label not unique"
            tgt = (s, e)
    assert tgt, f"FAIL [{label}]: block with aria-label={aria!r} not found"
    s, e = tgt
    c = c[:s] + '<!-- wp:html -->\n' + newcontent + '\n' + c[e:]
    applied.append(label)

replace_html_block('Airport transfer pricing – VanBudapest', A, '#1 kartyak -> Koncepcio A')
replace_html_block('VanBudapest Pricing Table 2026',        D, '#2 tablazat -> Koncepcio D')

# ---------------------------------------------------------------- 2) #3 luxury: parkolas kulon tetel
rep('#3 parkolas kulon tetel',
 'include every cost: parking fees, flight/train delays, highway tolls, Meet &amp; Greet services, VAT, and all applicable taxes.',
 'include every cost: flight/train delays, highway tolls, Meet &amp; Greet services, VAT, and all applicable taxes. Budapest Airport parking is charged separately and itemised on your confirmation (€12 on arrival, €3 on departure).')

# ---------------------------------------------------------------- 3) #4 motion-v4
rep('#4 quote-includes',
 'Your confirmed quote already includes airport parking, highway tolls, VAT, and a personalized Meet &amp; Greet service.',
 'Your confirmed quote already includes highway tolls, VAT, and a personalized Meet &amp; Greet service. Budapest Airport parking is shown as a separate, itemised line: €12 on arrival, €3 on departure.')

rep('#4 30 -> 60 perc (fo mondat)',
 'To maintain full transparency, all our transfer rates already include these updated airport costs. Each booking covers 30 minutes of parking and waiting time, including your Meet &amp; Greet service inside the terminal.',
 'To maintain full transparency, we show these airport costs as a separate, itemised line instead of hiding them in the fare. The €12 arrival fee covers airport parking and up to 60 minutes of waiting time from landing, including your Meet &amp; Greet service inside the terminal.')

rep('#4 30 -> 60 perc (tullepes)',
 'Should the waiting time exceed 30 minutes, a small additional fee may apply and can be settled directly with the driver.',
 'Should the waiting time exceed 60 minutes, Budapest Airport’s current parking tariff applies and can be settled directly with the driver.')

rep('#4 5-perces kiallas',
 'where a 5-minute parking interval is included in the service.',
 'where a 5-minute drop-off window applies (€3, itemised on your confirmation).')

rep('#4 lista: 30 -> 60 perc varakozas',
 '<li>Up to 30 minutes of complimentary waiting time</li>',
 '<li>Up to 60 minutes of waiting time after landing</li>')

rep('#4 FAQ: parkolas nem all-inclusive',
 '<p>Yes. All rates are flat and all-inclusive, covering taxes, tolls, VAT, and parking. Even if your flight is delayed or traffic is heavy, your fare will not change.</p>',
 '<p>Yes. All rates are flat and all-inclusive, covering taxes, tolls and VAT. Budapest Airport parking is itemised separately: \u20ac12 on arrival (up to 60 minutes of waiting from landing included) and \u20ac3 on departure. Even if your flight is delayed or traffic is heavy, your fare will not change.</p>')

rep('#4 lista: all fees included',
 '<li>Fixed, transparent pricing with all fees included</li>',
 '<li>Fixed, transparent pricing \u2014 airport fees itemised, never hidden</li>')

# ---------------------------------------------------------------- 4) #6 FAQ EN / DE / ES
rep('#6 EN q1',
 'The fixed fare covers everything – including flight-delay monitoring, Meet & Greet inside the terminal, parking fees, highway tolls, and all taxes/VAT – with no hidden charges.',
 'The fixed fare covers flight-delay monitoring, Meet & Greet inside the terminal, highway tolls, and all taxes/VAT – with no hidden charges. Budapest Airport parking is itemised separately: €12 on arrival (including up to 60 minutes of waiting from landing) and €3 on departure.')

rep('#6 EN q-fix',
 'All prices are final and include every cost: waiting time, tolls, parking, taxes, and VAT.',
 'All prices are final and include every cost: waiting time, tolls, taxes, and VAT. Budapest Airport parking is itemised separately: €12 on arrival (up to 60 minutes of waiting from landing included) and €3 on departure.')

rep('#6 DE q1',
 'Flugüberwachung bei Verspätungen, Meet & Greet direkt im Terminal, Parkgebühren, Autobahngebühren sowie alle Steuern und MwSt. sind im Preis enthalten.',
 'Flugüberwachung bei Verspätungen, Meet & Greet direkt im Terminal, Autobahngebühren sowie alle Steuern und MwSt. sind im Preis enthalten. Die Parkgebühr am Flughafen Budapest wird separat ausgewiesen: 12 € bei Ankunft (inkl. bis zu 60 Minuten Wartezeit ab der Landung) und 3 € bei Abfahrt.')

rep('#6 DE q-fix',
 'Alle üblichen Kosten wie Wartezeit, Maut, Parkgebühren, Steuern und MwSt. sind bereits enthalten.',
 'Alle üblichen Kosten wie Wartezeit, Maut, Steuern und MwSt. sind bereits enthalten. Die Parkgebühr am Flughafen Budapest wird separat ausgewiesen: 12 € bei Ankunft (inkl. bis zu 60 Minuten Wartezeit ab der Landung) und 3 € bei Abfahrt.')

rep('#6 ES q1',
 'La tarifa fija cubre todo: seguimiento del vuelo en caso de retrasos, servicio de recepción (Meet & Greet) dentro de la terminal, tasas de estacionamiento, peajes e impuestos (IVA), sin cargos adicionales.',
 'La tarifa fija cubre todo: seguimiento del vuelo en caso de retrasos, servicio de recepción (Meet & Greet) dentro de la terminal, peajes e impuestos (IVA), sin cargos adicionales. Las tasas de estacionamiento del aeropuerto de Budapest se facturan por separado: 12 € a la llegada (incluye hasta 60 minutos de espera desde el aterrizaje) y 3 € a la salida.')

rep('#6 ES q-fix',
 'Incluyen todo: tiempo de espera, peajes, estacionamiento, impuestos e IVA.',
 'Incluyen todo: tiempo de espera, peajes, impuestos e IVA. Las tasas de estacionamiento del aeropuerto de Budapest se facturan por separado: 12 € a la llegada (incluye hasta 60 minutos de espera desde el aterrizaje) y 3 € a la salida.')

# ---------------------------------------------------------------- 5) #6 SZIVARGO SZELEKTOROK -> namespace
rep('#6 leak: h2{',            '\n    h2{',            '\n    .vb-section h2{')
rep('#6 leak: h3{',            '\n    h3{',            '\n    .vb-section h3{')
rep('#6 leak: h3 span.flag{',  '\n    h3 span.flag{',  '\n    .vb-section h3 span.flag{')
rep('#6 leak: @media h2{',
 '@media(max-width:640px){.vb-inner{padding:1.2rem;}h2{font-size:1.6rem;}}',
 '@media(max-width:640px){.vb-inner{padding:1.2rem;}.vb-section h2{font-size:1.6rem;}}\n    /* A #0 blokk Gutenberg-cimsora sajat, nem szivargo szabalyt kap: */\n    .vb-page-h2{text-align:center;font-size:clamp(1.8rem,4vw,2.6rem);font-weight:800;margin-bottom:2rem;}\n    @media(max-width:640px){.vb-page-h2{font-size:1.6rem;}}')

# ---------------------------------------------------------------- 6) #0 H2: sajat osztaly, hogy a megjeleneset megtartsa
rep('#0 H2 className',
 '<!-- wp:heading {"style":{"typography":{"textAlign":"center"}}} -->\n<h2 class="wp-block-heading has-text-align-center">Budapest &amp; Hungary- Vienna - Airport Transfers</h2>',
 '<!-- wp:heading {"style":{"typography":{"textAlign":"center"}},"className":"vb-page-h2"} -->\n<h2 class="wp-block-heading has-text-align-center vb-page-h2">Budapest &amp; Hungary- Vienna - Airport Transfers</h2>')

open('new_content.txt', 'w', encoding='utf-8').write(c)
print(f"Alkalmazott modositasok: {len(applied)}")
for a in applied: print("  OK -", a)
print(f"\nMeret: {len(c0)} -> {len(c)} ({len(c)-len(c0):+d})")
