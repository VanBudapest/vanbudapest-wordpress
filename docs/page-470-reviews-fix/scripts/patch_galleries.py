#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Surgical gallery fixes for page 470. Operates on a byte-exact copy of raw content.
Every replacement pattern MUST occur exactly once — otherwise abort."""
import sys, re

def sub1(s, old, new, label):
    n = s.count(old)
    if n != 1:
        print(f"ABORT: pattern '{label}' occurs {n}x (must be exactly 1)"); sys.exit(1)
    print(f"OK: {label} (1x) replaced")
    return s.replace(old, new, 1)

raw = open(sys.argv[1], encoding='utf-8').read()
out = raw

# ---------- GALLERY #5 : tile 1 (Vip-Services-1024x512.jpg, 404) -> media 18870 ----------
old_img5 = ('<img alt="Luxury Mercedes sedan with open door showing beige interior, professional chauffeur in dark suit hol" '
 'data-height="1000" data-id="10506" data-link="https://vanbudapest.com/luxury-premium-travel-vip-budapest-hungary/vip-services/" '
 'data-url="https://vanbudapest.com/wp-content/uploads/2025/01/Vip-Services-1024x512.jpg" data-width="2000" '
 'src="https://i0.wp.com/vanbudapest.com/wp-content/uploads/2025/01/Vip-Services-1024x512.jpg?ssl=1" data-amp-layout="responsive" />')
new_img5 = ('<img alt="Luxury black Mercedes sedan with open rear door and cream leather interior for Budapest VIP transfer" '
 'data-height="1728" data-id="18870" data-link="https://vanbudapest.com/wp-content/uploads/2026/02/vanbudapest-budapest-airport-transfer-hourly-chauffeur-private-hungary-019.webp" '
 'data-url="https://vanbudapest.com/wp-content/uploads/2026/02/vanbudapest-budapest-airport-transfer-hourly-chauffeur-private-hungary-019.webp" data-width="3936" '
 'src="https://i0.wp.com/vanbudapest.com/wp-content/uploads/2026/02/vanbudapest-budapest-airport-transfer-hourly-chauffeur-private-hungary-019.webp?ssl=1" data-amp-layout="responsive" loading="lazy" decoding="async" />')
out = sub1(out, old_img5, new_img5, "gallery5-tile1-img")
out = sub1(out, '"ids":[10506,11460,11459,11733,11454,11388,11386,11280]',
                '"ids":[18870,11460,11459,11733,11454,11388,11386,11280]', "gallery5-ids")

# ---------- GALLERY #10 : tile 1 big (chengshi_guanguang, 404) -> media 24181 ----------
old_g10a = ('<img alt="Chain Bridge Budapest with lion statue, iconic Hungarian landmark for luxury airport transfers and p" '
 'data-height="4024" data-id="8024" data-link="https://vanbudapest.com/2024/05/20/%e5%b8%83%e8%be%be%e4%bd%a9%e6%96%af%e7%a7%81%e4%ba%ba%e4%ba%a4%e9%80%9a%e6%9c%8d%e5%8a%a1-%e9%ab%98%e5%93%81%e8%b4%a8%e6%8e%a5%e9%80%81/chengshi_guanguang_budapest-2/" '
 'data-url="https://vanbudapest.com/wp-content/uploads/2024/05/chengshi_guanguang_budapest-1.jpg;w=750" data-width="6048" '
 'src="https://i0.wp.com/vanbudapest.com/wp-content/uploads/2024/05/chengshi_guanguang_budapest-1.jpg;w=750?ssl=1" data-amp-layout="responsive" />')
new_g10a = ('<img alt="Budapest panorama with the Danube, Parliament and Chain Bridge, backdrop of VanBudapest transfers" '
 'data-height="1080" data-id="24181" data-link="https://vanbudapest.com/wp-content/uploads/2026/05/budapest-panorama-buda-castle-parliament-599.webp" '
 'data-url="https://vanbudapest.com/wp-content/uploads/2026/05/budapest-panorama-buda-castle-parliament-599.webp" data-width="1440" '
 'src="https://i0.wp.com/vanbudapest.com/wp-content/uploads/2026/05/budapest-panorama-buda-castle-parliament-599.webp?ssl=1" data-amp-layout="responsive" loading="lazy" decoding="async" />')
out = sub1(out, old_g10a, new_g10a, "gallery10-tile1-img")

# ---------- GALLERY #10 : tile 2 — URL-only fix (file exists, ';w=627' segment breaks it) ----------
old_g10b_url = 'data-url="https://vanbudapest.com/wp-content/uploads/2023/01/group-event-transportation-budapest-hungary.jpg;w=627" data-width="627" src="https://i0.wp.com/vanbudapest.com/wp-content/uploads/2023/01/group-event-transportation-budapest-hungary.jpg;w=627?ssl=1" data-amp-layout="responsive" />'
new_g10b_url = 'data-url="https://vanbudapest.com/wp-content/uploads/2023/01/group-event-transportation-budapest-hungary.jpg" data-width="627" src="https://i0.wp.com/vanbudapest.com/wp-content/uploads/2023/01/group-event-transportation-budapest-hungary.jpg?ssl=1" data-amp-layout="responsive" loading="lazy" decoding="async" />'
out = sub1(out, old_g10b_url, new_g10b_url, "gallery10-tile2-url")

# ---------- GALLERY #10 : tile 3 (van_rental...;w=750, 404) -> media 3816 (sibling shot, exists) ----------
old_g10c = ('<img alt="Black Mercedes luxury minivan parked in Budapest courtyard - premium private airport transfer servic" '
 'data-height="768" data-id="3815" data-link="https://vanbudapest.com/private-transfer-hungarian-grand-prix-f1-race/van_rental_long-distance_transfer_hungary_budapest_vip_private_service_private_transport/" '
 'data-url="https://vanbudapest.com/wp-content/uploads/V-Class-fleet/kulso/vanbudapest-mercedes-v-class-vip-minibus-hungary-064.webp;w=750" data-width="1024" '
 'src="https://i0.wp.com/vanbudapest.com/wp-content/uploads/2022/02/van_rental_long-distance_transfer_hungary_budapest_vip_private_service_private_transport.jpg;w=750?ssl=1" data-amp-layout="responsive" />')
new_g10c = ('<img alt="Black Mercedes luxury minivan parked in Budapest courtyard - premium private airport transfer servic" '
 'data-height="768" data-id="3816" data-link="https://vanbudapest.com/wp-content/uploads/2022/02/van_rental_long-distance_transfer_hungary_budapest_vip_private_small-transport.jpg" '
 'data-url="https://vanbudapest.com/wp-content/uploads/2022/02/van_rental_long-distance_transfer_hungary_budapest_vip_private_small-transport.jpg" data-width="1024" '
 'src="https://i0.wp.com/vanbudapest.com/wp-content/uploads/2022/02/van_rental_long-distance_transfer_hungary_budapest_vip_private_small-transport.jpg?ssl=1" data-amp-layout="responsive" loading="lazy" decoding="async" />')
out = sub1(out, old_g10c, new_g10c, "gallery10-tile3-img")
out = sub1(out, '"ids":[8024,5899,3815]', '"ids":[24181,5899,3816]', "gallery10-ids")

# lazy-load a maradék 7 ep galeria-kepre (blokk #5) — img tagek, amiken meg nincs loading=
import re as _re
def add_lazy(m):
    tag = m.group(0)
    if 'loading=' in tag: return tag
    return tag.replace(' />', ' loading="lazy" decoding="async" />')
before = out.count('loading="lazy"')
out = _re.sub(r'<img [^>]*data-amp-layout="responsive" */>', add_lazy, out)
print(f"lazy added: {out.count(chr(108)+'oading=')-before} additional imgs")

open(sys.argv[2],'w',encoding='utf-8').write(out)
print("written:", sys.argv[2], "len:", len(out))
