import pw from '/home/user/vanbudapest-wordpress/node_modules/playwright/index.js';
const { chromium } = pw;
const br = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium' });
const SEC = ['vbp-a (A-kártyák)','vbp-d (D-mátrix)','#3 Luxury Beyond','#4 Motion-v4','#5 Summary','#6 FAQ'];
for (const w of [1920,1440,1024,600,390,320]) {
  const p = await br.newPage({ viewport:{width:w,height:900} });
  await p.goto('file://'+process.cwd()+'/audit8.html'); await p.waitForTimeout(600);
  const r = await p.evaluate(() => {
    const secs=[...document.querySelectorAll('section')];
    return secs.map(s=>{
      const inner=s.querySelector('.vb-inner,.vbp-wrap');
      const ib=inner?inner.getBoundingClientRect():null;
      // valodi torzsszoveg: a leghosszabb <p>
      const ps=[...s.querySelectorAll('p')].filter(e=>e.textContent.trim().length>120);
      const p0=ps.sort((a,b)=>b.textContent.length-a.textContent.length)[0];
      let fs=null,al=null,ch=null,lh=null;
      if(p0){const st=getComputedStyle(p0); fs=parseFloat(st.fontSize); al=st.textAlign;
        lh=Math.round(parseFloat(st.lineHeight)/fs*100)/100;
        // valos karakter/sor: szelesseg / atlagos karakterszelesseg meressel
        const probe=document.createElement('span'); probe.style.cssText='visibility:hidden;position:absolute;white-space:pre';
        probe.style.font=st.font||`${st.fontWeight} ${st.fontSize}/${st.lineHeight} ${st.fontFamily}`;
        probe.textContent='abcdefghijklmnopqrstuvwxyz '; document.body.appendChild(probe);
        const cw=probe.getBoundingClientRect().width/27; probe.remove();
        ch=Math.round(p0.getBoundingClientRect().width/cw);}
      const h=s.querySelector('h2,h3');
      const bg=getComputedStyle(s).backgroundAttachment;
      return {inner:ib?Math.round(ib.width):null, fs, al, lh, ch,
              h:h?Math.round(parseFloat(getComputedStyle(h).fontSize)):null, bg};
    });
  });
  console.log(`\n══════ ${w}px ══════`);
  r.forEach((s,i)=>console.log(
    `  ${SEC[i].padEnd(20)} sáv ${String(s.inner).padStart(4)}px · törzs ${s.fs}px/${s.lh} ${String(s.al).padEnd(7)}`
    + ` · ${String(s.ch).padStart(3)} karakter/sor · h ${s.h}px · bg-attach:${s.bg}`));
  await p.close();
}
await br.close();
