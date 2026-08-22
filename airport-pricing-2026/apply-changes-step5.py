# -*- coding: utf-8 -*-
# 5. kor — CSAK TORLES. Az ASZF-fel utkozo allitasokat kivesszuk,
# NEM potoljuk ki az ASZF szerinti szabalyokkal. (Tomi: "csak szedd ki")
#
# Teszt, amit egy mondatra alkalmaztam — akkor utkozik, ha azt allitja, hogy
#   (a) az oldalon KOZOLT ar a vegleges fizetendo ar, vagy
#   (b) semmilyen tovabbi dij nem merulhet fel.
# ASZF 6.2: "Az arak IRANYADOAK, az aktualis es vegleges dij minden esetben az
#            irasos visszaigazolasban kerul rogzitesre."
# ASZF 6.3: kiemelt idoszakban eltero dijazas, dec. 23 - jan. 2. +100% felar.
# ASZF 6.1/6.5: a parkolas NEM resze a viteldijnak; 60 perc feletti varakozas felaras.
#
# Amit MEGTARTOTTAM, mert az ASZF alatamasztja: mi van benne (utdij, AFA, Meet & Greet),
# a tetelesen kiirt 12 EUR / 3 EUR, a 60 perc varakozas, es hogy keses/forgalom nem drágit.

import re

blocks = {i: open(f'cur_b{i}.txt', encoding='utf-8').read() for i in range(4)}
orig   = dict(blocks)
log    = []

def rep(bi, label, old, new, expect=1):
    n = blocks[bi].count(old)
    assert n == expect, f"FAIL [b{bi} {label}]: {expect} kellene, {n} van\n  old={old[:170]!r}"
    blocks[bi] = blocks[bi].replace(old, new)
    log.append((bi, label))

def drop_details(bi, label, summary):
    """Kivagja a teljes <details>...</details> blokkot a megadott summary alapjan.
    Ket HTML-stilust kezel: egysoros (<details><summary>..) es tordelt (<details>\n  <summary>..)."""
    b = blocks[bi]
    s = f'<summary>{summary}</summary>'
    si = b.find(s)
    assert si >= 0, f"FAIL [b{bi} {label}]: nincs meg a summary"
    assert b.count(s) == 1, f"FAIL [b{bi} {label}]: nem egyedi ({b.count(s)})"
    i = b.rfind('<details>', 0, si)
    assert i >= 0, f"FAIL [b{bi} {label}]: nincs nyito <details>"
    j = b.find('</details>', si) + len('</details>')
    # a sor eleji behuzast es a kovetkezo sortorest is levagjuk
    k = i
    while k > 0 and b[k-1] in ' \t': k -= 1
    if b[k-1:k] == '\n': k -= 1
    blocks[bi] = b[:k] + b[j:]
    log.append((bi, label))

# ══════════════════════════════ BLOKK [0] — A-kartyak + D-matrix + #3
rep(0, 'A-blokk eyebrow: „Fixed, published rates" kivéve',
 '<p class="vbp-eyebrow">Fixed, published rates · Since 1988</p>',
 '<p class="vbp-eyebrow">Since 1988</p>')

rep(0, '#3: „include every cost" -> „include"',
 'All prices listed below are in EUR and include every cost: flight/train delays,',
 'All prices listed below are in EUR and include: flight/train delays,')

rep(0, '#3: „all-inclusive pricing” -> „clear pricing” (a parkolás külön tétel)',
 'We believe in providing clear, all-inclusive pricing to make your travel planning stress-free.',
 'We believe in providing clear pricing to make your travel planning stress-free.')

# ══════════════════════════════ BLOKK [1] — #4 Motion-v4
rep(1, '#4: „the fare you see is the fare you pay" + „no surprises and no hidden fees" kivéve',
 'At VanBudapest, the fare you see is the fare you pay. Every airport transfer is offered at a fixed, all-inclusive rate, meaning no surprises and no hidden fees. Your confirmed quote already includes',
 'Your confirmed quote already includes')

rep(1, '#4 intro: „fixed all-inclusive pricing” -> „fixed pricing”',
 'with private airport transfers, fixed all-inclusive pricing, and a luxury fleet',
 'with private airport transfers, fixed pricing, and a luxury fleet')

drop_details(1, '#4 FAQ „Are the prices really fixed?" torolve',
 'Are the prices really fixed?')

# ══════════════════════════════ BLOKK [2] — #5 Summary
rep(2, '#5: „These are final prices and will not be charged any additional fees." kivéve',
 'our fixed prices are valid for one-way trips. These are final prices and will not be charged any additional fees. The fixed-price applies,',
 'our fixed prices are valid for one-way trips. The fixed-price applies,')

rep(2, '#5: „Final Fixed Prices – No Hidden Costs" szekció törölve',
 '''    <h3>Final Fixed Prices – No Hidden Costs</h3>\n'''
 '''    <p>At vanbudapest.com, we guarantee final fixed prices. Even if your flight is delayed or traffic is heavy, your fare remains the same. You’ll always know the exact price in advance – no surprises, no stress.</p>\n\n''',
 '')

# ══════════════════════════════ BLOKK [3] — #6 FAQ (EN / DE / ES)
# --- 1. kerdes: „mit tartalmaz az ar"
rep(3, '#6 EN q1: „all-inclusive" + „no hidden charges" + „final price you pay" kivéve',
 '<p>Our transfer prices are all-inclusive. The fixed fare covers flight-delay monitoring, Meet & Greet inside the terminal, highway tolls, and all taxes/VAT – with no hidden charges. Budapest Airport parking is itemised separately: €12 on arrival (including up to 60 minutes of waiting from landing) and €3 on departure. The price shown is always the final price you pay.</p>',
 '<p>The fixed fare covers flight-delay monitoring, Meet & Greet inside the terminal, highway tolls, and all taxes/VAT. Budapest Airport parking is itemised separately: €12 on arrival (including up to 60 minutes of waiting from landing) and €3 on departure.</p>')

rep(3, '#6 DE q1: „Endpreise" + „keine versteckten Zusatzkosten" kivéve',
 '<p>Unsere Transferpreise sind Endpreise und beinhalten alles. Flugüberwachung bei Verspätungen, Meet & Greet direkt im Terminal, Autobahngebühren sowie alle Steuern und MwSt. sind im Preis enthalten. Die Parkgebühr am Flughafen Budapest wird separat ausgewiesen: 12 € bei Ankunft (inkl. bis zu 60 Minuten Wartezeit ab der Landung) und 3 € bei Abfahrt. Es gibt keine versteckten Zusatzkosten – der angezeigte Preis ist der Endpreis.</p>',
 '<p>Flugüberwachung bei Verspätungen, Meet & Greet direkt im Terminal, Autobahngebühren sowie alle Steuern und MwSt. sind im Preis enthalten. Die Parkgebühr am Flughafen Budapest wird separat ausgewiesen: 12 € bei Ankunft (inkl. bis zu 60 Minuten Wartezeit ab der Landung) und 3 € bei Abfahrt.</p>')

rep(3, '#6 ES q1: „todo incluido" + „sin cargos adicionales" + „precio final" kivéve',
 '<p>Nuestros precios son todo incluido. La tarifa fija cubre todo: seguimiento del vuelo en caso de retrasos, servicio de recepción (Meet & Greet) dentro de la terminal, peajes e impuestos (IVA), sin cargos adicionales. Las tasas de estacionamiento del aeropuerto de Budapest se facturan por separado: 12 € a la llegada (incluye hasta 60 minutos de espera desde el aterrizaje) y 3 € a la salida. El precio mostrado es el precio final que pagará.</p>',
 '<p>La tarifa fija cubre: seguimiento del vuelo en caso de retrasos, servicio de recepción (Meet & Greet) dentro de la terminal, peajes e impuestos (IVA). Las tasas de estacionamiento del aeropuerto de Budapest se facturan por separado: 12 € a la llegada (incluye hasta 60 minutos de espera desde el aterrizaje) y 3 € a la salida.</p>')

# --- keses-kerdes: a „varakozasi ido" nem lehet benne (60 perc felett felaras)
rep(3, '#6 EN: „or waiting time" kivéve (60 perc felett feláras)',
 'there are no additional charges for flight delays, traffic, or waiting time.',
 'there are no additional charges for flight delays or traffic.')

rep(3, '#6 DE: „oder Wartezeiten" kivéve',
 'entstehen keine zusätzlichen Gebühren für Flugverspätungen, Verkehr oder Wartezeiten.',
 'entstehen keine zusätzlichen Gebühren für Flugverspätungen oder Verkehr.')

rep(3, '#6 ES: „o tiempo de espera" kivéve',
 'no hay cargos adicionales por retrasos, tráfico o tiempo de espera.',
 'no hay cargos adicionales por retrasos o tráfico.')

# --- „fix ar / nincs rejtett dij" kerdes: teljes torles
drop_details(3, '#6 EN „Are the prices fixed with no hidden fees?" törölve',
 'Are the prices fixed with no hidden fees?')
drop_details(3, '#6 DE „Sind die Preise endgültig…?" törölve',
 'Sind die Preise endgültig und gibt es keine versteckten Gebühren?')
drop_details(3, '#6 ES „¿Los precios son fijos…?" törölve',
 '¿Los precios son fijos y no hay tarifas ocultas?')

# --- lemondasi kerdes: teljes torles (nem potoljuk ASZF-szoveggel)
drop_details(3, '#6 EN lemondási kérdés törölve',
 'What is your cancellation policy if I need to cancel or change my booking?')
drop_details(3, '#6 DE lemondási kérdés törölve',
 'Wie ist Ihre Stornierungs- und Umbuchungsrichtlinie?')
drop_details(3, '#6 ES lemondási kérdés törölve',
 '¿Cuál es su política de cancelación si necesito cancelar o cambiar mi reserva?')

rep(1, '#4 h3: „Transparent, All-Inclusive Pricing” -> „Transparent Pricing”',
 '<h3>Transparent, All-Inclusive Pricing</h3>',
 '<h3>Transparent Pricing</h3>')

# --- csomagszallito potkocsi: az ASZF 6.1/6.6 szerint a tobbletcsomag-szallitas
#     koltsege a Megrendelot terheli, tehat a „free of charge” igeret utkozik.
rep(3, '#6 EN: „luggage trailer free of charge” -> „luggage trailer”',
 'we can provide a luggage trailer free of charge.',
 'we can provide a luggage trailer.')
rep(3, '#6 DE: „Gepäckanhänger ohne Aufpreis” -> „Gepäckanhänger”',
 'stellen wir einen Gepäckanhänger ohne Aufpreis zur Verfügung.',
 'stellen wir einen Gepäckanhänger zur Verfügung.')
rep(3, '#6 ES: „remolque … sin coste adicional” -> „remolque …”',
 'proporcionamos un remolque para equipaje sin coste adicional.',
 'proporcionamos un remolque para equipaje.')

# ══════════════════════════════ mentes
for i, b in blocks.items():
    open(f'b{i}_v5.txt', 'w', encoding='utf-8').write(b)

print(f"Lepesek: {len(log)}\n")
for bi, lab in log: print(f"  OK - [b{bi}] {lab}")
print()
for i in range(4):
    d = len(blocks[i]) - len(orig[i])
    flag = '  <-- CSERELNI' if d else '  valtozatlan'
    print(f"  blokk[{i}]: {len(orig[i])} -> {len(blocks[i])} ({d:+d}){flag}")
