const { chromium } = require('playwright'); const path=require('path');
const WIDTHS=[320,360,390,414,430,480,600,768,775,900,1024,1280,1440,1920,2560];
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const rows=[];
for (const w of WIDTHS){
  const ctx=await b.newContext({viewport:{width:w,height:900}});const p=await ctx.newPage();
  await p.goto('file://'+path.resolve('preview_after.html'),{waitUntil:'load'});
  // teljes vegiggorgetes -> minden lazy kep betolt
  await p.evaluate(async()=>{ const step=700;
    for(let y=0;y<document.body.scrollHeight;y+=step){ window.scrollTo(0,y);
      await new Promise(r=>setTimeout(r,12)); }
    window.scrollTo(0,0); });
  await p.waitForTimeout(400);
  const m=await p.evaluate(()=>{
    const d=document.documentElement,bd=document.body;
    const imgs=[...document.querySelectorAll('.vb-section img')];
    const wide=imgs.map(i=>Math.round(i.getBoundingClientRect().width));
    const g=document.querySelectorAll('.vb-gallery');
    const cols=[...g].map(gg=>{const im=[...gg.querySelectorAll('img')];
      if(!im.length)return 0;const t=im[0].getBoundingClientRect().top;
      return im.filter(x=>Math.abs(x.getBoundingClientRect().top-t)<3).length;});
    const gal=[...document.querySelectorAll('.vb-gallery img')].map(i=>i.getBoundingClientRect());
    const split=[...document.querySelectorAll('.vb-split__media img')].map(i=>Math.round(i.getBoundingClientRect().width));
    // tul kilogo elem kereses
    const over=[...document.querySelectorAll('.vb-section *')].filter(e=>{
      const r=e.getBoundingClientRect(); return r.right>d.clientWidth+1||r.left<-1;
    }).slice(0,3).map(e=>e.tagName+'.'+(e.className||'').toString().split(' ')[0]);
    return {h:Math.max(bd.scrollHeight,d.scrollHeight),sw:d.scrollWidth,cw:d.clientWidth,
      maxImg:Math.max(...wide), galMax:gal.length?Math.round(Math.max(...gal.map(r=>r.width))):0,
      cols, split, over};
  });
  rows.push({w,...m}); await ctx.close();
}
console.log('szél. | magasság | túllógás | legnagyobb kép | galéria-kép | oszlop #6/#10 | #8 kép | kilógó elem');
for(const r of rows){
  console.log(`${String(r.w).padStart(5)} | ${String(r.h).padStart(8)} | ${(r.sw>r.cw?'IGEN ***':'nincs  ').padEnd(8)} | ${String(r.maxImg).padStart(14)} | ${String(r.galMax).padStart(11)} | ${String(r.cols.join('/')).padStart(13)} | ${String(r.split[0]||0).padStart(6)} | ${r.over.join(',')||'-'}`);
}
await b.close();})();
