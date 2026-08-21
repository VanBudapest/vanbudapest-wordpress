import re,sys,html,base64

SCOPED = open("scoped_2594.css",encoding="utf-8").read()

# a temaból csak azt vesszük át, ami a hibákat okozta / a kontextust adja
THEME = """
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#ffffff;color:#f4f4f5;
     font-family:'Open Sans',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
     line-height:1.6;overflow-x:hidden;-webkit-font-smoothing:antialiased}
.wp-site-blocks{overflow-x:clip}
.entry-content{background:#fff}
/* a tema is-layout-flow block-gap-je: EZ adta a 36px feher csikokat */
.entry-content > * + *{margin-block-start:36px}
/* a tema altal kiirt WP-cim (Roboto Serif, 64px) */
.wp-block-post-title{font-family:Georgia,'Times New Roman',serif;font-weight:400;
  font-size:clamp(2rem,1.5rem + 2.6vw,4rem);line-height:1.15;color:#111;
  max-width:1200px;margin:0 auto;padding:48px 24px;text-align:center}
"""

def placeholder(src, alt, w=1536, h=1024):
    label = (alt or "")[:70]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
           f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
           f'<stop offset="0" stop-color="#16233f"/><stop offset="1" stop-color="#0a1220"/>'
           f'</linearGradient></defs>'
           f'<rect width="{w}" height="{h}" fill="url(#g)"/>'
           f'<rect x="8" y="8" width="{w-16}" height="{h-16}" fill="none" stroke="#C8B560" stroke-opacity=".35" stroke-width="4"/>'
           f'<text x="{w//2}" y="{h//2-30}" fill="#C8B560" font-family="sans-serif" font-size="46" '
           f'text-anchor="middle" opacity=".9">KEP / IMAGE</text>'
           f'<text x="{w//2}" y="{h//2+40}" fill="#9fb0c9" font-family="sans-serif" font-size="30" '
           f'text-anchor="middle">{html.escape(label)}</text></svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

DIMS = {"083.webp":(1440,1080), "086.webp":(1440,1080)}

def build(src_file, out_file, with_scoped, title):
    c = open(src_file,encoding="utf-8").read()
    c = re.sub(r'<!-- /?wp:html -->','',c)
    c = re.sub(r'<!-- wp:paragraph[^>]*-->|<!-- /wp:paragraph -->','',c)
    def rep(m):
        tag = m.group(0)
        s = re.search(r'src="([^"]+)"',tag); a = re.search(r'alt="([^"]*)"',tag)
        w,h = 1536,1024
        for k,(kw,kh) in DIMS.items():
            if s and k in s.group(1): w,h = kw,kh
        return tag.replace(s.group(1), placeholder(s.group(1), a.group(1) if a else "", w, h))
    c = re.sub(r'<img[^>]*>', rep, c)
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>{THEME}</style>
{'<style>'+SCOPED+'</style>' if with_scoped else ''}
</head><body class="page-id-2594">
<div class="wp-site-blocks"><main class="entry-content">
<h2 class="wp-block-post-title">Clean Luxury Transfers in Budapest | Hygiene &amp; Safety by VanBudapest.com</h2>
{c}
</main></div></body></html>"""
    open(out_file,"w",encoding="utf-8").write(doc)
    print(out_file, len(doc))

build("raw_reconstructed.html","preview_before.html",False,"ELOTTE")
build("raw_patched2.html","preview_after.html",True,"UTANA")
