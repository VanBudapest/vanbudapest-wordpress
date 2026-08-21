const { chromium } = require('playwright');
const widths = [320,360,390,414,430,480,600,768,775,900,1024,1280,1440,1920,2560];
async function main(){const b = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || undefined });
const page = await (await b.newContext()).newPage();
await page.goto('file://' + process.cwd() + '/qa_harness.html');
const results = [];
for (const w of widths) {
  await page.setViewportSize({ width: w, height: 900 });
  await page.waitForTimeout(80);
  const r = await page.evaluate(() => {
    const de = document.documentElement;
    const items = [...document.querySelectorAll('.tiled-gallery__item')];
    const g1 = [...document.querySelectorAll('.wp-block-jetpack-tiled-gallery')][0];
    const g1items = [...g1.querySelectorAll('.tiled-gallery__item')].map(i=>i.getBoundingClientRect());
    // columns = distinct x positions in first gallery
    const xs = [...new Set(g1items.map(r=>Math.round(r.x)))];
    return {
      scrollW: de.scrollWidth, clientW: de.clientWidth,
      scrollH: de.scrollHeight, bodyH: document.body.getBoundingClientRect().height,
      cols: xs.length, itemW: Math.round(g1items[0]?.width||0),
      titleHidden: getComputedStyle(document.querySelector('.wp-block-post-title')).display === 'none',
    };
  });
  results.push({w, ...r, E2: r.scrollW <= r.clientW ? 'PASS' : 'FAIL'});
}
console.table(results);
// functional checks at 1280
await page.setViewportSize({ width: 1280, height: 900 });
const fx = await page.evaluate(() => {
  const out = {};
  out.h1 = document.querySelectorAll('h1').length;
  out.blockquotes = document.querySelectorAll('.vb-rev470-arch blockquote').length;
  out.listAnchor = !!document.getElementById('list');
  out.countText0 = document.getElementById('count').textContent;
  document.getElementById('country').value = 'US';
  document.getElementById('country').dispatchEvent(new Event('change'));
  out.countTextUS = document.getElementById('count').textContent;
  document.getElementById('country').value = '';
  document.getElementById('country').dispatchEvent(new Event('change'));
  out.countTextAll = document.getElementById('count').textContent;
  const q = document.getElementById('q'); q.value = 'csaba';
  q.dispatchEvent(new Event('input'));
  out.countTextCsaba = document.getElementById('count').textContent;
  // archive link color
  const link = document.querySelector('.entry-content > p a[href="#list"]');
  out.archiveLinkColor = link ? getComputedStyle(link).color : null;
  // leak check: does block CSS affect elements OUTSIDE the namespaces?
  const probe = document.createElement('p'); probe.textContent='probe'; document.body.appendChild(probe);
  out.probeColor = getComputedStyle(probe).color; // should be body #383F40
  return out;
});
console.log(JSON.stringify(fx, null, 1));
// screenshots
for (const w of [390, 781, 1440]) {
  await page.setViewportSize({ width: w, height: 1000 });
  await page.waitForTimeout(80);
  await page.screenshot({ path: `qa_shot_${w}.png`, fullPage: true });
}
await b.close();
}
main().catch(e=>{console.error(e);process.exit(1)});
