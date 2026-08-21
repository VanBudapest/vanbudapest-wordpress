const { chromium } = require('playwright');
const path = require('path');
const WIDTHS = [320,360,390,414,430,480,600,768,775,900,1024,1280,1440,1920,2560];
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const out = {};
  for (const file of ['preview_before.html','preview_after.html']) {
    out[file] = [];
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto('file://' + path.resolve(file), { waitUntil: 'load' });
    for (const w of WIDTHS) {
      await page.setViewportSize({ width: w, height: 900 });
      await page.waitForTimeout(120);
      const m = await page.evaluate(() => {
        const d = document.documentElement, b = document.body;
        const gal = document.querySelector('.vb-gallery');
        let cols = 0;
        if (gal) { const imgs=[...gal.querySelectorAll('img')];
          if (imgs.length){ const t=imgs[0].getBoundingClientRect().top;
            cols = imgs.filter(i=>Math.abs(i.getBoundingClientRect().top-t)<3).length; } }
        return { height: Math.max(b.scrollHeight, d.scrollHeight),
                 scrollW: d.scrollWidth, clientW: d.clientWidth,
                 galleryCols: cols };
      });
      out[file].push({ w, ...m, overflow: m.scrollW > m.clientW });
    }
    await ctx.close();
  }
  console.log(JSON.stringify(out, null, 1));
  await browser.close();
})();
