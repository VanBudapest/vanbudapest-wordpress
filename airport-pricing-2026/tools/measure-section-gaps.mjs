// Megmeri a sotet szekciok kozotti fuggoleges reseket (feher csikok) a rendereld oldalon.
// Hasznalat: node tools/measure-section-gaps.mjs   (a fullpage2.html-t varja a scratchpadben)
// A WP/tema alapertelmezett res-kepzo szabalyait szandekosan szimulalja, hogy a javitas
// akkor is bizonyitott legyen, ha a tema kesobb visszahozza oket.
import { chromium } from 'playwright';
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage(); const errs=[];
p.on('pageerror',e=>errs.push(e.message));
for(const h of ['**://vanbudapest.com/**','**://spcdn.shortpixel.ai/**'])
  await p.route(h, r=>r.fulfill({status:200,contentType:'image/svg+xml',body:'<svg xmlns="http://www.w3.org/2000/svg" width="768" height="512"><rect width="768" height="512" fill="#12306A"/></svg>'}));
await p.goto('file:///tmp/claude-0/-home-user-vanbudapest-wordpress/24778f6f-251c-572c-9669-577efe7059ef/scratchpad/fullpage2.html');
await p.setViewportSize({width:1440,height:1000});
await p.waitForTimeout(1400);
const r=await p.evaluate(()=>{
  const secs=[...document.querySelectorAll('.vbp-a,.vbp-d,.vb-section')];
  const out=secs.map(s=>{const b=s.getBoundingClientRect();
    return {cls:s.className.split(' ').slice(0,2).join('.'),top:Math.round(b.top+scrollY),bottom:Math.round(b.bottom+scrollY),w:Math.round(b.width)};});
  const gaps=[];
  for(let i=1;i<out.length;i++) gaps.push({between:`${out[i-1].cls} → ${out[i].cls}`, gap:out[i].top-out[i-1].bottom});
  // első sötét szekció teteje vs a cím alja
  const title=document.querySelector('.wp-block-post-title').getBoundingClientRect();
  return {out,gaps,titleBottom:Math.round(title.bottom+scrollY),firstSecTop:out[0].top,
    kickers:[...document.querySelectorAll('.vbp-a .vbp-kicker')].map(k=>k.textContent.trim().slice(0,52)),
    h2:document.querySelector('.vbp-a h2').textContent.trim(),
    eyebrow:document.querySelector('.vbp-a .vbp-eyebrow').textContent.trim()};
});
console.log('=== SZEKCIÓK ===');
r.out.forEach(s=>console.log(`  ${s.cls.padEnd(26)} top=${String(s.top).padStart(6)} bottom=${String(s.bottom).padStart(6)} w=${s.w}`));
console.log('\n=== RÉSEK A SZEKCIÓK KÖZÖTT (0 kell) ===');
r.gaps.forEach(g=>console.log(`  ${g.gap===0?'✅':'❌'} ${String(g.gap).padStart(4)}px  ${g.between}`));
console.log(`\n  cím alja=${r.titleBottom}  első sötét szekció teteje=${r.firstSecTop}  → rés=${r.firstSecTop-r.titleBottom}px`);
console.log('\n=== A-BLOKK FEJLÉC ===');
console.log('  eyebrow:',r.eyebrow);
console.log('  H2     :',r.h2);
r.kickers.forEach(k=>console.log('  kicker :',k));
console.log('\nJS hibák:',errs.length?errs:'nincs');
await p.screenshot({path:'/tmp/claude-0/-home-user-vanbudapest-wordpress/24778f6f-251c-572c-9669-577efe7059ef/scratchpad/gap-1440.png',clip:{x:0,y:0,width:1440,height:1600}});
await b.close();
