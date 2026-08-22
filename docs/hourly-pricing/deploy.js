/* ===================================================================
   VanBudapest — óradíj-motor (A és B blokk közös)
   -------------------------------------------------------------------
   ÁRFORRÁS: ÁRAZÁS2026ÚJ.xlsx → „Alap árak" lap
     r[0] = B15 „Hourly Rate (min 3+1h)"  → 3–6 óra
     r[1] = B16 „Hourly Rate (min 7+1h)"  → 7 órától
     r[2] = B17 „Hourly Rate DISCOUNT"    → NEM publikált ár (lásd TIER3_FROM)
   SÁVOZÁS: ÁSZF 6.4. — minden foglalás +1 logisztikai (garázs) órát tartalmaz.
   =================================================================== */
(function(){
  function boot(){
  if(!document.querySelector('.vbh-a') && !document.querySelector('.vbh-b')) return;
  var V=[
    {key:'e', name:'Mercedes E-Class',      cat:'Business Car',       pax:'3',     r:[65,60,55]},
    {key:'v', name:'Mercedes V-Class',      cat:'Premium Van',        pax:'6–7',   r:[70,65,60]},
    {key:'m', name:'Mercedes Sprinter',     cat:'Minibus',            pax:'14–20', r:[75,70,65]},
    {key:'s', name:'Mercedes S-Class',      cat:'Luxury Car VIP',     pax:'3',     r:[110,105,100]},
    {key:'vs',name:'Mercedes VIP Sprinter', cat:'Luxury Minibus VIP', pax:'8',     r:[85,80,75]},
    {key:'c', name:'Coach Bus',             cat:'Coach Bus',          pax:'49',    r:[120,110,100]}
  ];

  /* --- SÁVOZÁS ---------------------------------------------------
     TIER2_FROM = 7   → az Excel B16 sora („min 7+1h"), publikált.
     TIER3_FROM = null→ a B17 („DISCOUNT") sáv BELSŐ ÁR, NEM JELENÍTHETŐ MEG.
       Döntés 2026-08-22: az ügyfél felé kizárólag két sáv publikálható.
       Alátámasztja: sem az Excel, sem az ÁSZF nem rendel hozzá óraküszöböt,
       az ÁSZF 6.2. szerint pedig a kedvezmény „nagyobb volumenű, többnapos
       vagy rendszeres megrendelések esetén" egyedi, írásos megállapodás.
       Ezt az értéket ne állítsd át külön jóváhagyás nélkül.
     --------------------------------------------------------------- */
  var TIER2_FROM = 7;
  var TIER3_FROM = null;

  function rate(v,h){
    if(TIER3_FROM && h>=TIER3_FROM) return v.r[2];
    if(h>=TIER2_FROM) return v.r[1];
    return v.r[0];
  }
  function fmt(n){ return '€'+String(n).replace(/\B(?=(\d{3})+(?!\d))/g,'\u00A0'); }

  /* ---- A: óraváltó ---- */
  var aBtns=[].slice.call(document.querySelectorAll('.vbh-a .vbh-hours button'));
  function setA(h){
    aBtns.forEach(function(b){ b.setAttribute('aria-pressed', String(parseInt(b.getAttribute('data-h'),10)===h)); });
    [].slice.call(document.querySelectorAll('.vbh-a .vbh-card')).forEach(function(card){
      var k=card.getAttribute('data-veh');
      var v=V.filter(function(x){return x.key===k})[0]; if(!v) return;
      var rt=rate(v,h), billed=h+1;
      card.querySelector('.v').textContent=String(rt*billed).replace(/\B(?=(\d{3})+(?!\d))/g,'\u00A0');
      card.querySelector('.h').textContent=h+' h with you + 1 garage h = '+billed+' h billed · '+fmt(rt)+' / h';
      /* a kiemelt sáv MINDIG a ténylegesen számolt óradíj sora */
      card.querySelector('.r1').classList.toggle('on', rt===v.r[0]);
      card.querySelector('.r2').classList.toggle('on', rt!==v.r[0]);
    });
  }
  aBtns.forEach(function(b){ b.addEventListener('click', function(){ setA(parseInt(this.getAttribute('data-h'),10)); }); });
  setA(3);

  /* ---- B: kalkulátor ---- */
  if(!document.getElementById('vbhSum')) return;
  var selV=0, selH=3;
  var vBtns=[].slice.call(document.querySelectorAll('#vbhVeh .vbh-vcard'));
  var dBtns=[].slice.call(document.querySelectorAll('#vbhDur button'));
  function updB(){
    var v=V[selV], rt=rate(v,selH), billed=selH+1, tot=rt*billed;
    vBtns.forEach(function(b){ b.setAttribute('aria-pressed', String(parseInt(b.getAttribute('data-v'),10)===selV)); });
    dBtns.forEach(function(b){ b.setAttribute('aria-pressed', String(parseInt(b.getAttribute('data-h'),10)===selH)); });
    document.getElementById('vbhSumVeh').textContent=v.name;
    document.getElementById('vbhSumCat').textContent=v.cat+' · '+v.pax+' passengers';
    document.getElementById('vbhSumTot').textContent=fmt(tot);
    document.getElementById('vbhEqH').textContent=selH+' h';
    document.getElementById('vbhEqB').textContent=billed+' h';
    document.getElementById('vbhEqR').textContent=fmt(rt)+' / h';
    var tier=document.getElementById('vbhTier');
    if(v.r[0]>rt){
      tier.textContent='Lower rate applied from '+TIER2_FROM+' hours — you pay '+fmt(rt)+' / h instead of '+fmt(v.r[0])+' / h (saving '+fmt((v.r[0]-rt)*billed)+' on this booking).';
      tier.classList.add('on');
    } else { tier.classList.remove('on'); tier.textContent=''; }
    document.getElementById('vbhCta').setAttribute('href','https://vanbudapest.com/contact-customer-reviews/?vehicle='+v.key+'&hours='+selH);
    document.getElementById('vbhStickyT').firstChild.nodeValue=fmt(tot);
    document.getElementById('vbhStickyS').textContent=v.name.replace('Mercedes ','')+' · '+billed+' h billed';
  }
  vBtns.forEach(function(b){ b.addEventListener('click', function(){ selV=parseInt(this.getAttribute('data-v'),10); updB(); }); });
  dBtns.forEach(function(b){ b.addEventListener('click', function(){ selH=parseInt(this.getAttribute('data-h'),10); updB(); }); });
  updB();
}
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
})();
