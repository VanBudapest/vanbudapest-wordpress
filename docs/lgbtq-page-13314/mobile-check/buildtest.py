# -*- coding: utf-8 -*-
"""Build a faithful local copy of page 13314 for mobile layout measurement.

The live domain is blocked from this container, so images are replaced with
same-aspect placeholders. Everything that drives layout (markup, classes,
width/height attributes, the scoped stylesheet, the theme's constrained
container) is kept as it is in production.
"""
import re, html

SRC = 'page13314-v4.html'
CSS = '/home/user/vanbudapest-wordpress/docs/lgbtq-page-13314/scoped-13314.css'
OUT = 'mobile-test.html'

body = open(SRC, encoding='utf-8').read()
css = open(CSS, encoding='utf-8').read()

# strip the wp:html block comments (WordPress does not render them)
body = re.sub(r'<!-- /?wp:html -->\n?', '', body)

def placeholder(m):
    tag = m.group(0)
    w = re.search(r'\bwidth="(\d+)"', tag)
    h = re.search(r'\bheight="(\d+)"', tag)
    W = int(w.group(1)) if w else 1200
    H = int(h.group(1)) if h else 900
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' "
           f"viewBox='0 0 {W} {H}'><rect width='100%' height='100%' fill='%23888'/></svg>")
    tag = re.sub(r'src="[^"]*"', f'src="data:image/svg+xml;utf8,{svg}"', tag)
    # keep width/height attrs so aspect-ratio matches production
    if not w:
        tag = tag.replace('<img ', f'<img width="{W}" height="{H}" ', 1)
    return tag

body = re.sub(r'<img\b[^>]*/>', placeholder, body)

# the FAQ section uses a background image from the blocked domain; swap for a flat colour
css = re.sub(r"url\('https://vanbudapest\.com[^']*'\)[^;]*", "linear-gradient(#2b2b3d,#2b2b3d)", css)

doc = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>13314 mobile test</title>
<style>
/* --- minimal reproduction of the block theme's frame --- */
*{{margin:0}}
body{{font-family:"Raleway",system-ui,sans-serif;line-height:1.65;font-size:16px;color:#383f40;background:#fff}}
.wp-site-blocks{{display:flow-root}}
.entry-content.is-layout-constrained > *{{max-width:780px;margin-left:auto;margin-right:auto}}
.entry-content.is-layout-constrained > .vb-lx{{max-width:100vw}}
h1,h2{{font-family:"Roboto Serif",Georgia,serif;font-weight:200;line-height:1.1}}
.wp-block-post-title{{font-size:3rem;padding:0 20px}}
.site-header,.site-footer{{padding:20px;background:#f4f4f4;font-size:.9rem}}
/* --- page-scoped stylesheet, exactly as deployed --- */
{css}
</style>
</head><body>
<div class="wp-site-blocks">
  <header class="site-header">VanBudapest.com — header placeholder</header>
  <div class="entry-content is-layout-constrained">
    <h2 class="wp-block-post-title">Your Journey, Your Pride – Discreet Luxury Transfers Across Budapest &amp; Beyond</h2>
{body}
  </div>
  <footer class="site-footer">Footer placeholder · © 2026 VanBudapest.com — All rights reserved.</footer>
</div>
</body></html>
"""
open(OUT, 'w', encoding='utf-8').write(doc)
print('OK', len(doc), 'bytes |', doc.count('<section'), 'sections |', doc.count('<img'), 'images')
