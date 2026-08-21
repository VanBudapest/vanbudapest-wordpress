#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild both jetpack tiled galleries on page 470 with the June 2026 S/E/V-Class fleet set.
12 tiles in gallery #5, 6 tiles in gallery #10. Text blocks untouched."""
import re, sys, hashlib

U = "https://vanbudapest.com/wp-content/uploads/2026/06/"
P = "https://i0.wp.com/vanbudapest.com/wp-content/uploads/2026/06/"

def img(mid, fname, w, h, alt):
    assert len(alt) <= 100, f"alt too long ({len(alt)}): {alt}"
    return (f'<figure class="tiled-gallery__item"><img alt="{alt}" data-height="{h}" data-id="{mid}" '
            f'data-link="{U}{fname}" data-url="{U}{fname}" data-width="{w}" '
            f'src="{P}{fname}?ssl=1" data-amp-layout="responsive" loading="lazy" decoding="async" /></figure>')

G5 = [
 (25107,"Mercedes_S-class_VanBudapest-28.webp",1620,1080,"Mercedes S-Class quilted leather interior with blue ambient lighting for Budapest VIP transfers"),
 (24967,"Mercedes_E-class_VanBudapest-26.webp",2560,1632,"Mercedes E-Class interior with cream leather seats and digital dashboard for Budapest transfers"),
 (25206,"Mercedes_V-class_VanBudapest-14.webp",1620,1080,"Mercedes V-Class interior with three black leather seats for private Budapest group transfers"),
 (25112,"Mercedes_S-class_VanBudapest-33.webp",1620,1080,"Black Mercedes S-Class sedan ready in the garage for a premium Budapest airport transfer"),
 (24957,"Mercedes_E-class_VanBudapest-16.webp",1632,2560,"Mercedes E-Class rear seats in black leather, prepared for a private Budapest transfer"),
 (25204,"Mercedes_V-class_VanBudapest-12.webp",1620,1080,"Mercedes V-Class cabin with black leather seats and refreshments for Budapest airport transfers"),
 (25086,"Mercedes_S-class_VanBudapest-07.webp",1620,1080,"Mercedes S-Class rear-seat entertainment with blue ambient lighting for VIP Budapest journeys"),
 (24972,"Mercedes_E-class_VanBudapest-31.webp",1620,1080,"Black Mercedes E-Class prepared for an hourly chauffeur service in Budapest"),
 (25213,"Mercedes_V-class_VanBudapest-21.webp",720,1080,"Black Mercedes V-Class with open doors showing the premium interior before a Budapest transfer"),
 (25104,"Mercedes_S-class_VanBudapest-25.webp",1620,1080,"Mercedes S-Class rear cabin configured for executive work between Budapest meetings"),
 (25210,"Mercedes_V-class_VanBudapest-18.webp",1620,1080,"Professional VanBudapest chauffeur driving a luxury Mercedes on a private Budapest transfer"),
 (25088,"Mercedes_S-class_VanBudapest-09.webp",1620,1080,"Mercedes S-Class interior with cream leather seats for premium Budapest private transfers"),
]
G10 = [
 (25215,"Mercedes_V-class_VanBudapest-23.webp",1620,1080,"Mercedes V-Class with open sliding door waiting for passengers at a Budapest pickup"),
 (24966,"Mercedes_E-class_VanBudapest-25-1536x979.webp",1536,979,"Mercedes E-Class interior with cream leather seats for Budapest airport private transfers"),
 (25119,"Mercedes_S-class_VanBudapest-40.webp",1620,1080,"Mercedes S350d luxury sedan in the VanBudapest garage for premium airport transfers"),
 (25203,"Mercedes_V-class_VanBudapest-11.webp",1620,1080,"Black leather passenger cabin inside a Mercedes-Benz V-Class for Budapest group transfers"),
 (24962,"Mercedes_E-class_VanBudapest-21-1536x979.webp",1536,979,"Open Mercedes E-Class luggage compartment prepared for a Budapest airport transfer"),
 (25217,"Mercedes_V-class_VanBudapest-25.webp",1620,1080,"Mercedes V-Class interior with premium black leather seating for private Budapest transfers"),
]

def gallery_block(items, cols, align_cls, style_cls, colwidths):
    ids = ",".join(str(i[0]) for i in items)
    half = (len(items)+1)//2
    col1 = "".join(img(*i) for i in items[:half])
    col2 = "".join(img(*i) for i in items[half:])
    return (f'<!-- wp:jetpack/tiled-gallery {{"align":"full",{style_cls}"columns":{cols},'
            f'"columnWidths":[{colwidths}],"ids":[{ids}]}} -->\n'
            f'<div class="wp-block-jetpack-tiled-gallery alignfull {align_cls}"><div class="">'
            f'<div class="tiled-gallery__gallery"><div class="tiled-gallery__row">'
            f'<div class="tiled-gallery__col" style="flex-basis:50%">{col1}</div>'
            f'<div class="tiled-gallery__col" style="flex-basis:50%">{col2}</div>'
            f'</div></div></div></div>\n<!-- /wp:jetpack/tiled-gallery -->')

new_g5  = gallery_block(G5, 2, "is-style-columns", '"className":"is-style-columns",', '["50","50"]')
new_g10 = gallery_block(G10, 2, "is-style-rectangular", "", '["50","50"]')

cur = open('new_content_final.txt', encoding='utf-8').read()
blocks = list(re.finditer(r'<!-- wp:jetpack/tiled-gallery .*?<!-- /wp:jetpack/tiled-gallery -->', cur, re.S))
assert len(blocks) == 2, f"found {len(blocks)} gallery blocks"
out = cur[:blocks[0].start()] + new_g5 + cur[blocks[0].end():blocks[1].start()] + new_g10 + cur[blocks[1].end():]

open('new_content_v3.txt','w',encoding='utf-8').write(out)
import re as r
print("imgs:", len(r.findall(r'<img[\s>]', out)), "| len:", len(out), "| sha256:", hashlib.sha256(out.encode()).hexdigest())
print("lazy:", out.count('loading="lazy"'), "| galleries:", out.count('wp:jetpack/tiled-gallery -->'))
# total weight of chosen originals (KB, known sizes; 1536 variants estimated <=300KB each)
kb = [103,460,155,158,396,115,80,452,113,102,113,94, 345,300,82,124,300,114]
print("est. total image weight ~", sum(kb), "KB")
