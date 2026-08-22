# -*- coding: utf-8 -*-
# 8. kor — RESZPONZIV RETEG a regi szekciokra (#3, #4, #5, #6 = .vb-section).
#
# Egyetlen blokkba kerul (a legkisebbe, #6 FAQ), de MAGAS SPECIFICITASSAL
# (body.page-id-1351 elotag), ezert blokk-sorrendtol fuggetlenul ervenyesul
# mind a negy regi szekciora. Az A-kartyakat (.vbp-a) es a D-matrixot (.vbp-d)
# NEM erinti — azok kulon nevterben vannak.
import re, hashlib

blocks = {i: open(f'b{i}_v7.txt', encoding='utf-8').read() for i in range(4)}
orig   = dict(blocks)

RWD = """
    /* ═══════════════════════════════════════════════════════════════════
       VB RESZPONZIV RETEG · 2026-08
       Hatokore: a regi szekciok (.vb-section = #3, #4, #5, #6).
       Az A-kartyak (.vbp-a) es a D-matrix (.vbp-d) NEM erintett.
       A `body.page-id-1351` elotag miatt a specificitas magasabb, mint a
       blokkok sajat szabalyaie, ezert a blokkok sorrendjetol fuggetlenul nyer.
       ═══════════════════════════════════════════════════════════════════ */

    /* 1) EGYSEGES TARTALMI SAV — pontosan az A-kartyak/D-matrix savja.
          Eddig min(90vw,1320px) volt, ami nagy kijelzon 1320/1296px-et adott,
          szemben az A/D 1240px-evel -> a szovegoszlopok nem estek egy vonalba. */
    body.page-id-1351 .vb-section .vb-inner{
      box-sizing:border-box;width:100%;max-width:1320px;margin-inline:auto;
      padding-inline:clamp(16px,4vw,40px);
    }

    /* 2) OLVASHATO SORHOSSZ. Meres szerint 1920px-en 122 karakter/sor volt
          (optimum 45–75). A torzsszoveg kap egy kozepre igazitott oszlopot;
          a galeriak es a racsok teljes szelesseguek maradnak. */
    body.page-id-1351 .vb-section .vb-inner>p,
    body.page-id-1351 .vb-section .vb-content>p,
    body.page-id-1351 .vb-section .vb-inner>ul,
    body.page-id-1351 .vb-section .vb-content>ul{max-width:62ch;margin-inline:auto}
    body.page-id-1351 .vb-section .vb-faq p{max-width:62ch}

    /* 3) SORKIZARAS csak ott, ahol elfer. 390px-en 35 karakter/sor + justify
          = szethuzott szokozok ("folyok"); ott balra igazitunk. */
    @media (max-width:900px){
      body.page-id-1351 .vb-section,
      body.page-id-1351 .vb-section .vb-inner,
      body.page-id-1351 .vb-section .vb-content{text-align:left}
    }
    body.page-id-1351 .vb-section .vb-inner,
    body.page-id-1351 .vb-section .vb-content{hyphens:auto;overflow-wrap:break-word}

    /* 4) background-attachment:fixed -> az iOS Safari nem tamogatja rendesen
          (elcsuszo hatter, akadozo gorgetes). Erintokepernyon es kis kijelzon ki. */
    @media (max-width:1024px),(hover:none),(prefers-reduced-motion:reduce){
      body.page-id-1351 .vb-section[data-theme="sky"]{background-attachment:scroll}
    }

    /* 5) TAP-TARGETEK: a FAQ-nyitok 26–29px magasak voltak, ez 44px-re no. */
    body.page-id-1351 .vb-section .vb-faq summary{
      min-height:44px;display:flex;align-items:center;padding-block:4px
    }

    /* 6) Kep sose logjon ki a savbol. */
    body.page-id-1351 .vb-section img{max-width:100%}
"""

# a #6 (blokk[3]) style-blokkjanak vegere
ANCHOR = '    @media(max-width:640px){.vb-inner{padding:1.2rem;}.vb-section h2{font-size:1.6rem;}}\n'
n = blocks[3].count(ANCHOR)
assert n == 1, f"horgony: {n}"
blocks[3] = blocks[3].replace(ANCHOR, ANCHOR + RWD)

# ── VEDELMI ELLENORZESEK ────────────────────────────────────────────────
for i in (0, 1, 2):
    assert blocks[i] == orig[i], f"blokk[{i}] nem valtozhat!"
def sub(t, s, e):
    i = t.index(s); j = t.index(e, i) + len(e); return t[i:j]
for name, s, e in (('A-kartyak', '<section class="vbp-a"', '</section>\n<script>'),
                   ('D-matrix',  '<section class="vbp-d"', '</section>\n<!-- /wp:html -->')):
    a = sub(orig[0], s, e)
    print(f"  vedelem: {name} bajtra valtozatlan  (sha1 {hashlib.sha1(a.encode()).hexdigest()[:12]})")
# a szelektorokban (kommentek nelkul) nem szerepelhet az A/D nevter
RWD_CODE = re.sub(r'/\*.*?\*/', '', RWD, flags=re.S)
assert '.vbp-a' not in RWD_CODE and '.vbp-d' not in RWD_CODE, "a reteg nem hivatkozhat az A/D-re"
print("  vedelem: a reteg egyetlen szabalya sem cimzi az A/D nevteret")
assert blocks[3].count('<style>') == 1 and blocks[3].count('</style>') == 1

for i, b in blocks.items():
    open(f'b{i}_v8.txt', 'w', encoding='utf-8').write(b)
print()
for i in range(4):
    d = len(blocks[i]) - len(orig[i])
    print(f"  blokk[{i}]: {len(orig[i])} -> {len(blocks[i])} ({d:+d})" + ('  <-- CSERELNI' if d else '  valtozatlan'))
