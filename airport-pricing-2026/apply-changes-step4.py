# -*- coding: utf-8 -*-
b0 = open('b3_cur.txt', encoding='utf-8').read()
b  = b0
log = []

def rep(label, old, new, expect=1):
    global b
    n = b.count(old)
    assert n == expect, f"FAIL [{label}]: {expect} kellene, {n} van\n  old={old[:150]!r}"
    b = b.replace(old, new)
    log.append(label)

# ============================================================ 1) HALOTT CSS: .vb-page-h2
# A 2. korben athozott H2 mar az A-blokkban van, ezt az osztalyt semmi nem hasznalja.
rep('halott CSS: .vb-page-h2 torolve',
 '''\n    /* A #0 blokk Gutenberg-cimsora sajat, nem szivargo szabalyt kap: */\n'''
 '''    .vb-page-h2{text-align:center;font-size:clamp(1.8rem,4vw,2.6rem);font-weight:800;margin-bottom:2rem;}\n'''
 '''    @media(max-width:640px){.vb-page-h2{font-size:1.6rem;}}''',
 '')

# ============================================================ 2) LEMONDASI FAQ — az ASZF VII. fejezete szerint
# Forras: VanBudapest_ASZF_HU.docx — 7.2.1 / 7.2.2 / 7.2.3 savok, 7.2.4(a) tranzakcios koltseg,
#         7.5.2 dijmentes modositas, 7.1.2 csak e-mailben, 7.3 kiemelt idoszakok.
# A regi szoveg csak a 72/48 orat ismerte, es azt a minibuszokra is kiterjesztette (DE/ES kifejezetten
# "Minivans"/"minivans"-t irt) — az ASZF szerint a V-Class/Sprinter savja 7 nap, nem 72 ora.

rep('#6 EN lemondasi FAQ -> ASZF 7.2',
 '<p>Our cancellation policy depends on vehicle type. For smaller vehicles, cancellations made more than 72 hours before pickup are fully refundable; between 48–72 hours receive 50% refund; less than 48 hours or no-show are non-refundable. A small processing fee applies to all cancellations. Modifications are free if made at least three days before pickup.</p>',
 '<p>Our cancellation policy depends on the vehicle category, calculated from the confirmed pickup time:</p>'
 '<p><b>Cars (Mercedes E-Class, S-Class):</b> 72 hours or more before pickup — full refund; 72–48 hours — 50% refund; under 48 hours or no-show — no refund.</p>'
 '<p><b>Minibuses (Mercedes V-Class, Sprinter):</b> 7 days or more — full refund; 7 days to 72 hours — 50% refund; under 72 hours or no-show — no refund.</p>'
 '<p><b>Coaches and VIP Sprinters:</b> 21 days or more — full refund; 21 to 14 days — 50% refund; under 14 days or no-show — no refund.</p>'
 '<p>Refunds are subject to a 3% transaction cost (minimum &euro;20). Changes to the pickup time or place are free at least 72 hours before pickup. Cancellations are valid in writing only, by email to info@vanbudapest.com. Peak periods and major events may follow stricter terms, which are always stated in your confirmation.</p>')

rep('#6 DE lemondasi FAQ -> ASZF 7.2',
 '<p>Unsere Stornierungsbedingungen richten sich nach der Fahrzeugkategorie. Bei PKWs und Minivans sind Stornierungen bis 72 Stunden vor Abholung vollständig erstattbar, 48–72 Stunden vorher 50%, und unter 48 Stunden nicht mehr erstattbar. Eine kleine Bearbeitungsgebühr fällt bei jeder Stornierung an. Änderungen sind kostenfrei, wenn sie mindestens drei Tage vorher erfolgen.</p>',
 '<p>Unsere Stornierungsbedingungen richten sich nach der Fahrzeugkategorie, gerechnet ab der bestätigten Abholzeit:</p>'
 '<p><b>PKW (Mercedes E-Klasse, S-Klasse):</b> ab 72 Stunden vorher — volle Erstattung; 72–48 Stunden vorher — 50%; unter 48 Stunden oder No-Show — keine Erstattung.</p>'
 '<p><b>Minibusse (Mercedes V-Klasse, Sprinter):</b> ab 7 Tagen vorher — volle Erstattung; 7 Tage bis 72 Stunden vorher — 50%; unter 72 Stunden oder No-Show — keine Erstattung.</p>'
 '<p><b>Reisebusse und VIP-Sprinter:</b> ab 21 Tagen vorher — volle Erstattung; 21 bis 14 Tage vorher — 50%; unter 14 Tagen oder No-Show — keine Erstattung.</p>'
 '<p>Von jeder Erstattung werden Transaktionskosten von 3% (mindestens 20 &euro;) abgezogen. Änderungen von Abholzeit oder -ort sind bis 72 Stunden vorher kostenfrei. Stornierungen sind ausschließlich schriftlich per E-Mail an info@vanbudapest.com gültig. In Hochsaison und bei Großveranstaltungen können strengere Bedingungen gelten; diese stehen in Ihrer Buchungsbestätigung.</p>')

rep('#6 ES lemondasi FAQ -> ASZF 7.2',
 '<p>Nuestra política de cancelación depende del tipo de vehículo. Para sedanes y minivans, las cancelaciones hechas con más de 72 horas de antelación tienen reembolso total; entre 48–72 horas, 50%; con menos de 48 horas o no presentarse, no hay reembolso. Se aplica una pequeña tarifa de procesamiento. Las modificaciones son gratuitas si se realizan al menos tres días antes del traslado.</p>',
 '<p>Nuestra política de cancelación depende de la categoría del vehículo, calculada desde la hora de recogida confirmada:</p>'
 '<p><b>Turismos (Mercedes Clase E, Clase S):</b> 72 horas o más antes — reembolso total; entre 72 y 48 horas — 50%; menos de 48 horas o no presentarse — sin reembolso.</p>'
 '<p><b>Minibuses (Mercedes Clase V, Sprinter):</b> 7 días o más antes — reembolso total; entre 7 días y 72 horas — 50%; menos de 72 horas o no presentarse — sin reembolso.</p>'
 '<p><b>Autocares y VIP Sprinter:</b> 21 días o más antes — reembolso total; entre 21 y 14 días — 50%; menos de 14 días o no presentarse — sin reembolso.</p>'
 '<p>De todo reembolso se descuentan los costes de transacción del 3% (mínimo 20 &euro;). Los cambios de hora o lugar de recogida son gratuitos hasta 72 horas antes. Las cancelaciones solo son válidas por escrito, por correo electrónico a info@vanbudapest.com. En temporada alta y grandes eventos pueden aplicarse condiciones más estrictas, siempre indicadas en su confirmación.</p>')

open('b3_v4.txt', 'w', encoding='utf-8').write(b)
print(f"Lepesek: {len(log)}")
for x in log: print("  OK -", x)
print(f"\nMeret: {len(b0)} -> {len(b)} ({len(b)-len(b0):+d})")
