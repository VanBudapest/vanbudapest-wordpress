#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the new post_content for page 470 from work_content_v2.txt (gallery-patched MCP raw)
+ rendered blocks 1 & 7 (lossless channel). Text nodes are carried over byte-exact."""
import re, sys, hashlib

def sub1(s, old, new, label):
    n = s.count(old)
    if n != 1:
        print(f"ABORT: '{label}' occurs {n}x (need exactly 1)"); sys.exit(1)
    return s.replace(old, new, 1)

# ---------- CSS for the new intro block (visuals identical to the old embedded doc, namespaced) ----------
CSS1 = """
  .vb-rev470-intro{
    --bg:#ffffff;--panel:#ffffff;--text:#0A2342;--muted:#334766;
    --accent:#0A2342;--accent-strong:#001A33;--border:#C7D3EA;
    box-sizing:border-box;width:100%;margin:0;
    background:var(--bg);color:var(--text);line-height:1.7;
    -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
  .vb-rev470-intro *,.vb-rev470-intro *::before,.vb-rev470-intro *::after{box-sizing:border-box}
  .vb-rev470-intro .wrap{max-width:980px;padding:32px 20px 60px;margin:0 auto}
  .vb-rev470-intro .breadcrumb a{color:var(--accent);text-decoration:none}
  .vb-rev470-intro .breadcrumb a:hover{color:var(--accent-strong);text-decoration:underline}
  .vb-rev470-intro .title{font-family:inherit;font-size:clamp(28px,4vw,40px);margin:12px 0 8px;font-weight:800;color:var(--text);letter-spacing:.2px;line-height:1.2;overflow-wrap:anywhere}
  .vb-rev470-intro .lead{font-size:clamp(16px,1.6vw,18px);max-width:72ch;color:var(--muted)}
  .vb-rev470-intro .card{background:var(--panel);border-radius:16px;padding:26px;margin-top:22px;border:1px solid var(--border);box-shadow:0 4px 12px rgba(0,0,0,.05)}
  .vb-rev470-intro .card h2{font-family:inherit;margin:0 0 10px;font-size:clamp(24px,3vw,34px);color:var(--text);letter-spacing:normal;text-transform:none}
  .vb-rev470-intro .features{padding-left:20px;margin:0}
  .vb-rev470-intro .features li{margin:10px 0;color:var(--text)}
  .vb-rev470-intro .features li::marker{color:var(--accent)}
  .vb-rev470-intro .features b{color:var(--accent)}
  @media (min-width:782px){
    .vb-rev470-intro .lead{text-align:justify;text-justify:inter-word;-webkit-hyphens:auto;hyphens:auto}
  }
  @media (max-width:781px){
    .vb-rev470-intro .lead{text-align:left;-webkit-hyphens:none;hyphens:none}
  }
  @media (max-width:480px){
    .vb-rev470-intro .wrap{padding:24px 16px 44px}
  }
""".strip('\n')

# ---------- CSS for the new archive block (same design values, namespaced) ----------
CSS7 = """
  .vb-rev470-arch{
    --vb-deepblue:#0A1F44;--vb-gold:#C8B560;--vb-ink:#111111;--vb-bg:#ffffff;
    --vb-card:#fafafa;--vb-border:#e5e5e5;
    box-sizing:border-box;width:100%;margin:0;padding:0;
    background:var(--vb-bg);color:var(--vb-ink)}
  .vb-rev470-arch *,.vb-rev470-arch *::before,.vb-rev470-arch *::after{box-sizing:border-box}
  .vb-rev470-arch .wrap{max-width:1060px;margin:0 auto;padding:28px 18px 64px}
  .vb-rev470-arch header{padding:18px 16px 12px}
  .vb-rev470-arch .eyebrow{letter-spacing:.12em;text-transform:uppercase;font-size:12px;color:#555}
  .vb-rev470-arch .vb-arch-title{font-family:inherit;margin:6px 0 4px;font-size:30px;line-height:1.15;color:var(--vb-deepblue);font-weight:700;letter-spacing:normal;text-transform:none}
  .vb-rev470-arch .sub{color:#444;max-width:780px}
  .vb-rev470-arch .controls{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 8px}
  .vb-rev470-arch .input{border:1px solid var(--vb-border);border-radius:10px;padding:10px 12px;font:inherit;min-width:0}
  .vb-rev470-arch .select{border:1px solid var(--vb-border);border-radius:10px;padding:10px 12px;font:inherit;background:#fff;min-width:0}
  .vb-rev470-arch .count{margin-left:auto;color:#666;font-size:13px}
  .vb-rev470-arch .grid{display:grid;grid-template-columns:repeat(12,1fr);gap:16px;margin-top:10px;scroll-margin-top:80px}
  .vb-rev470-arch .col{grid-column:span 12;min-width:0}
  .vb-rev470-arch .card{background:var(--vb-card);border:1px solid var(--vb-border);border-radius:16px;box-shadow:0 8px 24px rgba(0,0,0,.05)}
  .vb-rev470-arch .card-body{padding:16px 18px}
  .vb-rev470-arch .meta{display:flex;flex-wrap:wrap;gap:8px 12px;color:#555;font-size:13px;margin-bottom:6px}
  .vb-rev470-arch .pill{display:inline-block;border:1px solid var(--vb-border);border-radius:999px;padding:4px 10px;background:#fff}
  .vb-rev470-arch blockquote{margin:0;font-size:16px;line-height:1.55;font-family:inherit;font-style:normal;border:0;padding:0}
  .vb-rev470-arch .date{margin-top:10px;font-size:12px;color:#666}
  .vb-rev470-arch .note{margin-top:20px;color:#666;font-size:12px}
  @media (min-width:880px){
    .vb-rev470-arch .col{grid-column:span 6}
  }
  @media (max-width:480px){
    .vb-rev470-arch .wrap{padding:20px 14px 44px}
    .vb-rev470-arch .controls{gap:8px}
    .vb-rev470-arch .input,.vb-rev470-arch .select{width:100%}
    .vb-rev470-arch .count{margin-left:0}
  }
""".strip('\n')

# ================= BLOCK 1 =================
b1 = open('rendered_block1.html', encoding='utf-8').read()
m = re.search(r'<body>\n(.*)\n</body>', b1, re.S)
body1 = m.group(1)
body1 = sub1(body1, '<a href="/reviews">Customer Feedback</a>',
                    '<a href="https://vanbudapest.com/google-reviews-customer-feedback/">Customer Feedback</a>',
             'breadcrumb-link-fix')
new_block1 = ('<section class="vb-rev470-intro">\n<style>\n' + CSS1 + '\n</style>\n' + body1 + '\n</section>')

# ================= BLOCK 7 =================
b7 = open('rendered_block7.html', encoding='utf-8').read()
m = re.search(r'<body>\n(.*)\n</body>', b7, re.S)
body7 = m.group(1)
# h1 -> h2 (text unchanged)
body7 = sub1(body7, '<h1>Legacy Reviews Archive</h1>', '<h2 class="vb-arch-title">Legacy Reviews Archive</h2>', 'arch-h1-to-h2')
# first card: h3 -> blockquote (consistent with the other 23)
first_q = '<h3>“Vanbudapest.com provided an excellent service. Our driver, Csaba, was incredibly friendly and helpful. The minivan was clean and comfortable, making our airport transfer smooth and enjoyable.”</h3>'
first_q_new = first_q.replace('<h3>', '<blockquote>').replace('</h3>', '</blockquote>')
body7 = sub1(body7, first_q, first_q_new, 'first-card-h3-to-blockquote')
# dev comment out
body7 = re.sub(r"[ \t]*<!-- MORE ITEMS CAN BE CONTINUED HERE[^>]*-->\n?", "", body7, count=1)
assert 'MORE ITEMS' not in body7
# ITEM marker comment out
body7 = body7.replace('      <!-- ITEM -->\n', '')
assert '<!-- ITEM -->' not in body7
# a11y labels (invisible attributes only)
body7 = sub1(body7, '<input id="q" class="input" placeholder="Search name or text…" />',
                    '<input id="q" class="input" placeholder="Search name or text…" aria-label="Search name or text" />', 'aria-q')
body7 = sub1(body7, '<select id="country" class="select">',
                    '<select id="country" class="select" aria-label="Filter by country">', 'aria-country')
body7 = sub1(body7, '<select id="year" class="select">',
                    '<select id="year" class="select" aria-label="Filter by year">', 'aria-year')
body7 = sub1(body7, '<div class="count" id="count"></div>',
                    '<div class="count" id="count" aria-live="polite"></div>', 'aria-count')
new_block7 = ('<section class="vb-rev470-arch">\n<style>\n' + CSS7 + '\n</style>\n' + body7 + '\n</section>')

# ================= ASSEMBLY =================
work = open('work_content_v2.txt', encoding='utf-8').read()

# old block1: first wp:html block (starts at 0)
m = re.match(r'<!-- wp:html -->\n(.*?)\n<!-- /wp:html -->', work, re.S)
assert m and m.start() == 0
work = work[:m.start()] + '<!-- wp:html -->\n' + new_block1 + '\n<!-- /wp:html -->' + work[m.end():]

# empty self-closing block out
work = sub1(work, '<!-- /wp:spacer -->\n\n<!-- wp:html /-->\n\n<!-- wp:jetpack', '<!-- /wp:spacer -->\n\n<!-- wp:jetpack', 'drop-empty-html-block')

# old block7: the wp:html block that contains 'Legacy Reviews Archive'
blocks = list(re.finditer(r'<!-- wp:html -->\n(.*?)\n?<!-- /wp:html -->', work, re.S))
tgt = [b for b in blocks if 'Legacy Reviews Archive' in b.group(1)]
assert len(tgt) == 1, f"legacy block found {len(tgt)}x"
b = tgt[0]
work = work[:b.start()] + '<!-- wp:html -->\n' + new_block7 + '\n<!-- /wp:html -->' + work[b.end():]

# archive link fix in paragraph block
work = sub1(work, '<a href="http://vanbudapest" target="_blank" rel="noreferrer noopener">Archive &gt;</a>',
                  '<a href="#list">Archive &gt;</a>', 'archive-link-fix')

open('new_content_final.txt', 'w', encoding='utf-8').write(work)
print("final len:", len(work), "sha256:", hashlib.sha256(work.encode()).hexdigest())
