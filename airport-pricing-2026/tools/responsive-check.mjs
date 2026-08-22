import pw from '/home/user/vanbudapest-wordpress/node_modules/playwright/index.js';
const { chromium } = pw;
const br = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium' });
const W=[2560,1920,1600,1440,1366,1280,1180,1024,912,820,768,600,540,430,414,390,375,360,344,320];
let bad=0;
for (const w of W) {
  const p = await br.newPage({ viewport:{width:w,height:800} });
  await p.goto('file://'+process.cwd()+'/audit8.html'); await p.waitForTimeout(400);
  const r = await p.evaluate(() => {
    const vw=document.documentElement.clientWidth, R=e=>e&&e.getBoundingClientRect();
    const aw=R(document.querySelector('.vbp-a .vbp-wrap'));
    const i4=document.querySelector('[data-component="vb-motion-v4"] .vb-inner');
    const cs=i4&&getComputedStyle(i4), b4=R(i4);
    const c4=b4?[Math.round(b4.left+parseFloat(cs.paddingLeft)),Math.round(b4.right-parseFloat(cs.paddingRight))]:null;
    let over=0; document.querySelectorAll('.entry-content *').forEach(e=>{
      const b=e.getBoundingClientRect(); if(b.width>0&&(b.right>vw+1||b.left<-1)){
        let q=e.parentElement,sc=false; while(q&&q!==document.body){const s=getComputedStyle(q);
          if(s.overflowX==='auto'||s.overflowX==='scroll'){sc=true;break;} q=q.parentElement;}
        if(!sc&&getComputedStyle(e).position!=='fixed') over++;}});
    let minTap=999; document.querySelectorAll('.vb-section summary').forEach(e=>minTap=Math.min(minTap,Math.round(R(e).height)));
    const ps=[...document.querySelectorAll('.vb-content>p')].filter(e=>e.textContent.length>150);
    let ch=null,al=null;
    if(ps[0]){const st=getComputedStyle(ps[0]); al=st.textAlign;
      const pr=document.createElement('span'); pr.style.cssText='visibility:hidden;position:absolute;white-space:pre';
      pr.style.font=st.font||`${st.fontWeight} ${st.fontSize}/${st.lineHeight} ${st.fontFamily}`;
      pr.textContent='abcdefghijklmnopqrstuvwxyz '; document.body.appendChild(pr);
      ch=Math.round(R(ps[0]).width/(pr.getBoundingClientRect().width/27)); pr.remove();}
    const secs=[...document.querySelectorAll('section')],gaps=[];
    for(let i=0;i<secs.length-1;i++) gaps.push(Math.round(R(secs[i+1]).top-R(secs[i]).bottom));
    return {pageOver:document.documentElement.scrollWidth-vw, over,
      aligned: aw&&c4&&Math.round(aw.left)===c4[0]&&Math.round(aw.right)===c4[1], ch, al, minTap,
      gapsOk: gaps.every(g=>g===0)};
  });
  const good = r.pageOver===0 && r.over===0 && r.aligned && r.ch>=40 && r.ch<=78 && r.minTap>=44 && r.gapsOk;
  if(!good) bad++;
  console.log(`${good?'✅':'❌'} ${String(w).padStart(4)}px  túlcs ${r.pageOver}/${r.over}  sáv-illesztés ${r.aligned?'ok':'ELTÉR'}  `
    +`${String(r.ch).padStart(3)} kar/sor ${r.al.padEnd(7)}  tap ${r.minTap}px  rések ${r.gapsOk?'0px':'!!'}`);
  await p.close();
}
console.log(`\n${bad===0?'MIND A '+W.length+' SZÉLESSÉG RENDBEN':bad+' PROBLÉMÁS'}`);
await br.close();
