const { chromium } = require('playwright');
const path = require('path');

const URL = 'file://' + path.resolve(__dirname, 'mobile-test.html');
const WIDTHS = [320, 360, 390, 414, 430, 480, 600, 768, 781, 820];

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const results = [];

  for (const w of WIDTHS) {
    const page = await browser.newPage({ viewport: { width: w, height: 844 }, deviceScaleFactor: 2 });
    await page.goto(URL, { waitUntil: 'load' });
    await page.waitForTimeout(150);

    const r = await page.evaluate((vw) => {
      const out = { width: vw };
      const de = document.documentElement;
      out.scrollWidth = de.scrollWidth;
      out.clientWidth = de.clientWidth;
      out.overflowPx = de.scrollWidth - de.clientWidth;
      out.pageHeight = de.scrollHeight;

      // every element that sticks out horizontally
      const bad = [];
      document.querySelectorAll('body *').forEach(el => {
        const b = el.getBoundingClientRect();
        if (b.width === 0 && b.height === 0) return;
        const over = Math.round(b.right - vw);
        const under = Math.round(b.left);
        if (over > 1 || under < -1) {
          const cs = getComputedStyle(el);
          if (cs.position === 'fixed') return;
          bad.push({
            tag: el.tagName.toLowerCase(),
            cls: (el.className || '').toString().slice(0, 46),
            left: under, right: Math.round(b.right), over
          });
        }
      });
      out.overflowing = bad.slice(0, 8);
      out.overflowCount = bad.length;

      // sticky bar
      const bar = document.querySelector('.vb-sticky-cta');
      if (bar) {
        const cs = getComputedStyle(bar);
        const b = bar.getBoundingClientRect();
        out.sticky = { display: cs.display, position: cs.position,
                       height: Math.round(b.height), bottom: Math.round(b.bottom),
                       width: Math.round(b.width) };
        const links = [...bar.querySelectorAll('a')].map(a => {
          const lb = a.getBoundingClientRect();
          return { text: a.textContent.trim().slice(0, 14), w: Math.round(lb.width), h: Math.round(lb.height) };
        });
        out.sticky.links = links;
      }
      out.bodyPadBottom = getComputedStyle(document.body).paddingBottom;

      // grid columns per section
      out.grids = [...document.querySelectorAll('.vb-img-grid')].slice(0, 4).map(g => {
        const kids = [...g.children].map(c => Math.round(c.getBoundingClientRect().left));
        const cols = new Set(kids).size;
        return { items: g.children.length, cols: cols === kids.length ? cols : new Set(kids).size };
      });

      // text sizes
      const p = document.querySelector('.vb-lx .vb-content p');
      const h2 = document.querySelector('.vb-lx .vb-title');
      const cap = document.querySelector('.vb-lx figcaption');
      out.fontSizes = {
        p: p ? getComputedStyle(p).fontSize : null,
        h2: h2 ? getComputedStyle(h2).fontSize : null,
        caption: cap ? getComputedStyle(cap).fontSize : null,
        align: p ? getComputedStyle(p).textAlign : null
      };

      // CTA buttons
      const ctas = [...document.querySelectorAll('.vb-lx .vb-cta')].slice(0, 3).map(a => {
        const b = a.getBoundingClientRect();
        return { text: a.textContent.trim().slice(0, 22), w: Math.round(b.width), h: Math.round(b.height) };
      });
      out.ctas = ctas;

      // anchor nav chips
      const chips = [...document.querySelectorAll('.vb-anchor-nav a')].map(a => {
        const b = a.getBoundingClientRect();
        return { t: a.textContent.trim(), w: Math.round(b.width), h: Math.round(b.height), r: Math.round(b.right) };
      });
      out.chips = { count: chips.length, maxRight: Math.max(...chips.map(c => c.r)),
                    minH: Math.min(...chips.map(c => c.h)), sample: chips.slice(0, 3) };

      // section widths — all should span the viewport exactly
      out.sections = [...document.querySelectorAll('section.vb-lx')].map(s => {
        const b = s.getBoundingClientRect();
        return Math.round(b.width);
      });

      // gaps between sections (should be 0)
      const secs = [...document.querySelectorAll('section.vb-lx')];
      const gaps = [];
      for (let i = 1; i < secs.length; i++) {
        const prev = secs[i - 1].getBoundingClientRect();
        const cur = secs[i].getBoundingClientRect();
        gaps.push(Math.round(cur.top - prev.bottom));
      }
      out.sectionGaps = gaps;

      // FAQ summary tap targets
      const sum = document.querySelector('.vb-faq-item summary');
      if (sum) { const b = sum.getBoundingClientRect(); out.faqSummary = { w: Math.round(b.width), h: Math.round(b.height) }; }

      return out;
    }, w);

    results.push(r);
    if ([320, 390, 781].includes(w)) {
      await page.screenshot({ path: `shot-${w}-top.png`, clip: { x: 0, y: 0, width: w, height: 844 } });
      await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
      await page.waitForTimeout(120);
      await page.screenshot({ path: `shot-${w}-bottom.png` });
    }
    await page.close();
  }

  await browser.close();
  console.log(JSON.stringify(results, null, 1));
})();
