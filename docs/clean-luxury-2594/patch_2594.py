#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VanBudapest.com - page 2594 (Clean Luxury / Hygiene & Safety) surgical content patch.
Every replacement is byte-exact and asserts an exact occurrence count.
Input : raw_reconstructed.html  (post_content with <style> tags restored)
Output: raw_patched.html
"""
import re, sys, hashlib

SRC = "raw_reconstructed.html"
DST = "raw_patched.html"

c = open(SRC, encoding="utf-8").read()
log = []

def rep(old, new, n, label):
    """Replace `old` with `new`, asserting exactly n occurrences."""
    global c
    found = c.count(old)
    if found != n:
        sys.exit("STOP [%s]: expected %d occurrence(s), found %d\n  needle: %r" % (label, n, found, old[:160]))
    c = c.replace(old, new)
    log.append("%-52s %dx  OK" % (label, n))

# --------------------------------------------------------------------------
# 1) COVID -> Clean / Hygiene & Safety  (block #10 only; block #14 archive stays)
# --------------------------------------------------------------------------
rep('<h2 class="vb-h2">Beyond the Pandemic: Our Ongoing Hygiene Philosophy</h2>',
    '<h2 class="vb-h2">Our Ongoing Hygiene Philosophy</h2>',
    1, "COVID/blk10 H2 'Beyond the Pandemic'")

rep('COVID-19 catalyzed a global focus on sanitation, but our dedication to cleanliness predates the pandemic and will continue long after.',
    'A worldwide focus on sanitation set new expectations for passenger transport, but our dedication to cleanliness predates it and will continue long after.',
    1, "COVID/blk10 lead sentence")

rep('During the pandemic we elevated these protocols by adding disinfectant treatments, SAO and ozone processing.',
    'We later elevated these protocols by adding disinfectant treatments, SAO and ozone processing.',
    1, "COVID/blk10 'During the pandemic'")

# --------------------------------------------------------------------------
# 2) Images
# --------------------------------------------------------------------------
# 2a) hero: wrong ALT + LCP hints
rep('<img class="vb-bg__image" src="https://vanbudapest.com/wp-content/uploads/2025/01/vip-limousine-budapest-rent.jpg" alt="VIP limousine in Budapest at night" />',
    '<img class="vb-bg__image" src="https://vanbudapest.com/wp-content/uploads/2025/01/vip-limousine-budapest-rent.jpg" alt="Rear cabin of a Mercedes S-Class with cream leather seats - VanBudapest chauffeur service, Budapest" fetchpriority="high" decoding="async" />',
    1, "hero IMG alt + fetchpriority=high")

# 2b) blk #6 slot 4: BROKEN image (404 on origin and CDN) -> media #1967
rep('<img src="https://vanbudapest.com/wp-content/uploads/vb-image-audit/placeholder-default.jpg" alt="Disinfected vehicle interior Budapest airport" />',
    '<img src="https://vanbudapest.com/wp-content/uploads/2020/05/18abe-disinfected-clean-vehicle-budapest-airport-7-1.jpg" alt="Gloved hand wiping the center console of a premium vehicle with a microfiber cloth - VanBudapest disinfection routine, Budapest" />',
    1, "blk6 BROKEN img -> media 1967")

# 2c) blk #8: duplicate of blk #6 and wrong subject for "Driver Health" -> media #440
rep('<img class="vb-img" src="https://vanbudapest.com/wp-content/uploads/2020/05/1f6f8-disinfected-clean-vehicle-budapest-airport-12-2.jpg" alt="Budapest chauffeur hygiene protocols" />',
    '<img class="vb-img" src="https://vanbudapest.com/wp-content/uploads/2020/06/budapest-driver-masks-gloves-1.jpg" alt="VanBudapest chauffeur wearing a mask and gloves while disinfecting a passenger seat, Budapest" />',
    1, "blk8 duplicate img -> media 440")

# 2d) blk #10 slot 1: covid_* filename -> media #3697
rep('<img src="https://vanbudapest.com/wp-content/uploads/2021/11/covid_hungary_transfer_safety.png" alt="Private transfer safety measures in Budapest" />',
    '<img src="https://vanbudapest.com/wp-content/uploads/2022/01/disinfected-and-cleaned-bus.jpeg" alt="Chauffeur in a dark suit wiping the dashboard of a premium transfer vehicle, Budapest" />',
    1, "blk10 covid_*.png -> media 3697")

# 2e) blk #10 slot 2: duplicate of blk #6 -> media #3700
rep('<img src="https://vanbudapest.com/wp-content/uploads/2022/01/8_van-and-bus-budapest-private-transfer-service-with-safety-precautions-program.jpg" alt="Safety precautions in Budapest van transfers" />',
    '<img src="https://vanbudapest.com/wp-content/uploads/2022/01/washing-cleaining-budapest-private-bus.jpg" alt="Passenger seat of a Mercedes-Benz van being cleaned with a microfiber cloth, Budapest" />',
    1, "blk10 duplicate img 2 -> media 3700")

# 2f) blk #10 slot 3: duplicate of blk #6 -> media #1934
rep('<img src="https://vanbudapest.com/wp-content/uploads/2022/01/7_pumps-ozone-safety-transfers-budapest.jpg" alt="Ozone pumps used in transfer cleaning" />',
    '<img src="https://vanbudapest.com/wp-content/uploads/2020/05/c7bcb-disinfected-clean-vehicle-budapest-airport-8-1.jpg" alt="Steam cleaning of the leather upholstery in a VanBudapest transfer vehicle, Budapest" />',
    1, "blk10 duplicate img 3 -> media 1934")

# --------------------------------------------------------------------------
# 3) Links
# --------------------------------------------------------------------------
rep('href="https://vanbudapest.com/contact/"',
    'href="https://vanbudapest.com/contact-customer-reviews/"',
    1, "hero CTA: 301 -> direct approved URL")

rep('href="https://www.facebook.com/vanbudapest"',
    'href="https://www.facebook.com/people/VanBudapestcom/61581875129965/"',
    4, "social: Facebook -> official")

rep('href="https://x.com/vanbudapest"',
    'href="https://x.com/BudapestVan"',
    4, "social: X (404) -> official")

rep('href="https://www.instagram.com/vanbudapest/"',
    'href="https://www.instagram.com/van_bus_budapest_/"',
    4, "social: Instagram -> official")
# TikTok deliberately untouched - not on the approved list, ownership unverified.

# --------------------------------------------------------------------------
# 4) Emoji <img> elimination (8 render-time requests) - plain text stays
# --------------------------------------------------------------------------
rep('>\U0001F4DE Phone: +36 70 753 6333<', '>Phone: +36 70 753 6333<', 4, "emoji: phone receiver removed")
rep('>\U0001F4AC WhatsApp Chat<',          '>WhatsApp Chat<',          4, "emoji: speech balloon removed")

# --------------------------------------------------------------------------
# 5) Heading semantics: contact tile labels are captions, not H3 outline entries
# --------------------------------------------------------------------------
rep('<h3 class="vb-h3">Email</h3>', '<p class="vb-h3">Email</p>', 4, "contact tile H3 -> P (Email)")
rep('<h3 class="vb-h3">Book&nbsp;<span style="white-space:nowrap">Now</span></h3>',
    '<p class="vb-h3">Book&nbsp;<span style="white-space:nowrap">Now</span></p>', 4, "contact tile H3 -> P (Book Now)")
rep('<h3 class="vb-h3">Social Media</h3>', '<p class="vb-h3">Social Media</p>', 4, "contact tile H3 -> P (Social)")
rep('<h3 class="vb-h3">Phone &amp; WhatsApp</h3>', '<p class="vb-h3">Phone &amp; WhatsApp</p>', 4, "contact tile H3 -> P (Phone)")

# --------------------------------------------------------------------------
# 6) a11y: label-content-name-mismatch (Lighthouse FAIL, 8 elements)
# --------------------------------------------------------------------------
rep(' href="mailto:info@vanbudapest.com" aria-label="Email">',
    ' href="mailto:info@vanbudapest.com">', 4, "a11y: drop aria-label on Email tile")
rep(' href="https://vanbudapest.com/contact-customer-reviews/" aria-label="Book Now">',
    ' href="https://vanbudapest.com/contact-customer-reviews/">', 4, "a11y: drop aria-label on Book Now tile")

# --------------------------------------------------------------------------
# 7) a11y: lang attributes on the multilingual FAQ paragraphs
# --------------------------------------------------------------------------
rep('<p>Transporte privado seguro en Budapest:', '<p lang="es">Transporte privado seguro en Budapest:', 1, "lang=es")
rep('<p>Sichere Privattransfers in Budapest:',   '<p lang="de">Sichere Privattransfers in Budapest:',   1, "lang=de")
rep('<p>布达佩斯私人接送服务', '<p lang="zh-Hans">布达佩斯私人接送服务', 1, "lang=zh-Hans")
rep('<p>Tiszta és biztonságos személyszállítás Budapesten:', '<p lang="hu">Tiszta és biztonságos személyszállítás Budapesten:', 1, "lang=hu")

# --------------------------------------------------------------------------
# 8) Dead CSS (.vb-tile - 0 usages in the document) - proven code garbage
# --------------------------------------------------------------------------
assert 'class="vb-tile"' not in c and ' vb-tile ' not in c, "STOP: .vb-tile is actually used"
rep('\n  /* Optional card/tile pattern – for future blocks, same visual language */'
    '\n  .vb-tile{background:rgba(10,31,68,.35); border:1px solid rgba(200,181,96,.22); border-radius:var(--vb-radius); box-shadow:var(--vb-elev); backdrop-filter:blur(6px); color:var(--vb-white);}'
    '\n  .vb-tile:hover{box-shadow:var(--vb-elev), var(--vb-gold-glow); border-color:rgba(200,181,96,.6);} \n',
    '', 1, "dead CSS: .vb-tile rules removed")

# --------------------------------------------------------------------------
# 9) Code garbage: two empty paragraph blocks at the end of the document
# --------------------------------------------------------------------------
rep('''

<!-- wp:paragraph {"align":"justify"} -->
<p class="has-text-align-justify"></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p></p>
<!-- /wp:paragraph -->''', '', 1, "code garbage: 2 empty paragraph blocks")

# --------------------------------------------------------------------------
# 10) loading="lazy" + decoding="async" on every non-hero image
# --------------------------------------------------------------------------
def add_loading(m):
    tag = m.group(0)
    if 'vb-bg__image' in tag:          # hero = LCP element, must stay eager
        return tag
    if 'loading=' in tag:
        return tag
    return tag[:-2].rstrip() + ' loading="lazy" decoding="async" />'

before = len(re.findall(r'<img[^>]*/>', c))
c = re.sub(r'<img[^>]*/>', add_loading, c)
n_lazy = c.count('loading="lazy"')
assert before == 17, "STOP: expected 17 self-closing <img>, found %d" % before
assert n_lazy == 16, "STOP: expected 16 lazy images, got %d" % n_lazy
log.append("%-52s %dx  OK" % ("loading=lazy + decoding=async (non-hero)", n_lazy))

# --------------------------------------------------------------------------
# Integrity fingerprint
# --------------------------------------------------------------------------
open(DST, "w", encoding="utf-8").write(c)
orig = open(SRC, encoding="utf-8").read()

def counts(s):
    return {
        "chars":       len(s),
        "wp:html":     len(re.findall(r'<!-- wp:html -->', s)),
        "<style>":     s.count("<style>"),
        "<section":    len(re.findall(r'<section', s)),
        "<img":        len(re.findall(r'<img', s)),
        "<a ":         len(re.findall(r'<a ', s)),
        "@media":      len(re.findall(r'@media', s)),
        "@keyframes":  len(re.findall(r'@keyframes', s)),
        "!important":  len(re.findall(r'!important', s)),
        "position:fixed": len(re.findall(r'position:fixed', s)),
        "id=":         len(re.findall(r'\bid=', s)),
        "<h1":         len(re.findall(r'<h1', s, re.I)),
        "<h2":         len(re.findall(r'<h2', s, re.I)),
        "<h3":         len(re.findall(r'<h3', s, re.I)),
        "COVID(any)":  len(re.findall(r'(?i)covid|pandemic|corona', s)),
        "wp:paragraph":len(re.findall(r'wp:paragraph', s)),
    }

a, b = counts(orig), counts(c)
print("\n".join(log))
print("\n=== INTEGRITY / CHANGE TABLE ===")
print("%-18s %10s %10s  %s" % ("metric", "before", "after", "delta"))
for k in a:
    d = b[k] - a[k]
    print("%-18s %10s %10s  %s" % (k, a[k], b[k], ("%+d" % d) if d else "unchanged"))
print("\nSHA-256 new content:", hashlib.sha256(c.encode()).hexdigest())
print("bytes:", len(c.encode("utf-8")))
