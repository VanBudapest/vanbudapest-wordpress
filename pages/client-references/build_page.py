# -*- coding: utf-8 -*-
"""VanBudapest Client References page rebuild (v4).
Generates new post_content: 17 wp:html blocks, namespaced vb-cr-* CSS,
verbatim original texts, new curated galleries, new StarLadder Major block.
"""

U = "https://vanbudapest.com/wp-content/uploads/"

def img(path, alt, w=None, h=None, sized=None, srcset=None, sizes=None, extra=""):
    src = U + (sized if sized else path)
    a = f'<img src="{src}" alt="{alt}"'
    if w and h:
        a += f' width="{w}" height="{h}"'
    if srcset:
        a += f' srcset="{srcset}"'
    if sizes:
        a += f' sizes="{sizes}"'
    a += f' loading="lazy" decoding="async"{extra}>'
    return a

def sl_variants(num, ext="webp"):
    base = f"2026/03/MAJOR-STARLADDER-2025-VB-CS2-MVMDOME-MTKSPORTPARK-{num}"
    return base, (
        f"{U}{base}-768x512.{ext} 768w, {U}{base}-1024x683.{ext} 1024w, "
        f"{U}{base}-1536x1024.{ext} 1536w, {U}{base}-2048x1366.{ext} 2048w"
    )

def gal(cls, imgs, extra_cls=""):
    inner = "\n    ".join(imgs)
    return f'<div class="vb-cr-gal {cls}{(" " + extra_cls) if extra_cls else ""}">\n    {inner}\n  </div>'

FRAMEWORK_CSS = """
  .vb-cr{position:relative;width:100vw;max-width:100vw !important;margin-left:calc(50% - 50vw) !important;margin-right:calc(50% - 50vw) !important;margin-top:0;margin-bottom:0;box-sizing:border-box;padding:clamp(64px,7vw,108px) 0;font-family:'Montserrat',system-ui,-apple-system,sans-serif;overflow:visible}
  .vb-cr, .vb-cr *{box-sizing:border-box}
  .vb-cr-wrap{max-width:1320px;margin:0 auto;padding:0 clamp(18px,4vw,28px)}
  .vb-cr-txt{max-width:920px;margin:0 auto;text-align:center}
  .vb-cr-txt p{font-size:clamp(1rem,1.12vw,1.13rem);line-height:1.85;margin:0 0 20px;text-align:left}
  .vb-cr-txt ul{list-style:none;margin:6px 0 22px;padding:0;text-align:left}
  .vb-cr-txt li{font-size:clamp(.98rem,1.08vw,1.1rem);line-height:1.8;margin:0 0 12px}
  .vb-cr h2{font-size:clamp(1.65rem,2.6vw,2.35rem);line-height:1.3;letter-spacing:.5px;margin:0 0 10px;font-weight:700;text-align:center}
  .vb-cr h2::after{content:"";display:block;width:56px;height:3px;background:#C8B560;border-radius:2px;margin:18px auto 26px}
  .vb-cr h3{font-size:clamp(.95rem,1.1vw,1.06rem);letter-spacing:2.5px;text-transform:uppercase;font-weight:600;margin:0 0 22px;text-align:center}
  .vb-cr h4{font-size:clamp(1.05rem,1.2vw,1.2rem);letter-spacing:.5px;margin:26px 0 14px;text-align:center}
  .vb-cr-cta{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-top:34px}
  .vb-cr-btn{display:inline-block;padding:15px 34px;border-radius:50px;font-weight:600;font-size:.98rem;letter-spacing:.5px;text-decoration:none;transition:transform .3s ease,box-shadow .3s ease,background .3s ease,color .3s ease}
  .vb-cr-btn--gold{background:#C8B560;color:#0A1F44;box-shadow:0 4px 16px rgba(200,181,96,.35)}
  .vb-cr-btn--gold:hover{background:#B78D38;transform:translateY(-2px);box-shadow:0 8px 24px rgba(200,181,96,.45)}
  .vb-cr-btn--line{border:2px solid #C8B560;color:#C8B560}
  .vb-cr-btn--line:hover{background:#C8B560;color:#0A1F44;transform:translateY(-2px)}
  .vb-cr-gal{display:grid;gap:clamp(12px,1.6vw,20px);max-width:1320px;margin:clamp(34px,4vw,54px) auto 0;padding:0 clamp(18px,4vw,28px)}
  .vb-cr-gal img{width:100%;height:100%;aspect-ratio:3/2;object-fit:cover;border-radius:14px;display:block;box-shadow:0 2px 12px rgba(5,14,35,.10);transition:transform .35s ease,box-shadow .35s ease}
  .vb-cr-gal img:hover{transform:translateY(-4px) scale(1.015);box-shadow:0 10px 26px rgba(5,14,35,.2)}
  .vb-cr-gal--g2{grid-template-columns:repeat(2,1fr)}
  .vb-cr-gal--g3{grid-template-columns:repeat(3,1fr)}
  .vb-cr-gal--g4{grid-template-columns:repeat(4,1fr)}
  .vb-cr--navy{background:linear-gradient(180deg,#0A1F44 0%,#12306A 100%);color:#EDF1F8}
  .vb-cr--navydeep{background:linear-gradient(180deg,#12306A 0%,#0A1F44 55%,#081733 100%);color:#EDF1F8}
  .vb-cr--cream{background:#F5F0E8;color:#1E2637}
  .vb-cr--white{background:#FFFFFF;color:#1E2637}
  .vb-cr--navy h2,.vb-cr--navydeep h2{color:#E5D9A8}
  .vb-cr--navy h3,.vb-cr--navydeep h3{color:#C8B560}
  .vb-cr--navy h4,.vb-cr--navydeep h4{color:#E5D9A8}
  .vb-cr--navy strong,.vb-cr--navydeep strong{color:#E5D9A8}
  .vb-cr--navy a:not(.vb-cr-btn),.vb-cr--navydeep a:not(.vb-cr-btn){color:#C8B560;text-decoration:none;font-weight:600}
  .vb-cr--cream h2,.vb-cr--white h2,.vb-cr--cream h4,.vb-cr--white h4{color:#0A1F44}
  .vb-cr--cream h3,.vb-cr--white h3{color:#8A6F2F}
  .vb-cr--cream strong,.vb-cr--white strong{color:#0A1F44}
  .vb-cr--cream a:not(.vb-cr-btn),.vb-cr--white a:not(.vb-cr-btn){color:#8A6F2F;text-decoration:none;font-weight:600}
  .vb-cr--cream .vb-cr-btn--line,.vb-cr--white .vb-cr-btn--line{border-color:#0A1F44;color:#0A1F44}
  .vb-cr--cream .vb-cr-btn--line:hover,.vb-cr--white .vb-cr-btn--line:hover{background:#0A1F44;color:#C8B560}
  @media(max-width:1024px){.vb-cr-gal--g4{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:781px){.vb-cr-gal--g3{grid-template-columns:repeat(2,1fr)}.vb-cr-gal--g2{grid-template-columns:1fr}.vb-cr{padding:clamp(48px,9vw,72px) 0}}
  @media(max-width:480px){.vb-cr-gal{gap:10px}}
  @media(prefers-reduced-motion:reduce){.vb-cr,.vb-cr *{transition:none !important;animation:none !important}}
"""

HERO_CSS = """
  #vb-client-references{min-height:clamp(480px,74vh,800px);display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,#0A1F44 0%,#12306A 100%);color:#fff}
  #vb-client-references .vb-cr-hero-bg{position:absolute;inset:0;background:url('https://vanbudapest.com/wp-content/uploads/2025/01/hungary-4898894.jpg') center/cover no-repeat;opacity:.35;z-index:0}
  #vb-client-references .vb-cr-hero-glow{position:absolute;inset:0;background:radial-gradient(circle at 50% 22%,rgba(200,181,96,.18),transparent 70%);z-index:1}
  #vb-client-references .vb-cr-wrap{position:relative;z-index:2;text-align:center}
  #vb-client-references h1{font-size:clamp(2rem,3.4vw,3.3rem);line-height:1.25;margin:0 0 22px;font-weight:700;background:linear-gradient(90deg,#E5D9A8,#C8B560 55%,#B78D38);-webkit-background-clip:text;background-clip:text;color:#C8B560;-webkit-text-fill-color:transparent}
  #vb-client-references .vb-cr-lead{font-size:clamp(1.02rem,1.35vw,1.24rem);line-height:1.9;color:#F3F5FA;max-width:880px;margin:0 auto 40px;text-align:center}
  #vb-client-references .vb-cr-lead a{color:#C8B560;text-decoration:none;font-weight:600}
"""

SL_CSS = """
  #vb-starladder-major{background:radial-gradient(1200px 500px at 50% -10%,rgba(245,197,24,.10),transparent 60%),linear-gradient(180deg,#081733 0%,#0A1F44 45%,#0B1B3A 100%);color:#EAF0FB}
  #vb-starladder-major::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.018) 0 1px,transparent 1px 4px);pointer-events:none}
  #vb-starladder-major .vb-cr-wrap{position:relative}
  #vb-starladder-major .vb-sl-badge{display:inline-flex;align-items:center;gap:10px;border:1px solid rgba(245,197,24,.6);color:#F5C518;font-size:.78rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;padding:9px 20px;border-radius:40px;margin:0 0 24px;background:rgba(245,197,24,.06)}
  #vb-starladder-major h2{color:#F7F9FE}
  #vb-starladder-major h2 .vb-sl-y{color:#F5C518}
  #vb-starladder-major h2::after{background:#F5C518}
  #vb-starladder-major .vb-cr-txt p{color:#C9D4E8;text-align:center}
  #vb-starladder-major .vb-sl-chips{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:26px 0 8px}
  #vb-starladder-major .vb-sl-chips span{border:1px solid rgba(200,214,236,.25);color:#AEBDD8;font-size:.75rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;padding:8px 16px;border-radius:8px;background:rgba(10,25,55,.5)}
  #vb-starladder-major .vb-sl-grid{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:clamp(120px,15vw,215px);gap:clamp(12px,1.6vw,18px);max-width:1320px;margin:clamp(36px,4vw,56px) auto 0;padding:0 clamp(18px,4vw,28px)}
  #vb-starladder-major .vb-sl-grid img{width:100%;height:100%;object-fit:cover;border-radius:12px;display:block;border:1px solid rgba(245,197,24,.22);box-shadow:0 4px 18px rgba(3,8,20,.5);transition:transform .35s ease,box-shadow .35s ease,border-color .35s ease}
  #vb-starladder-major .vb-sl-grid img:hover{transform:translateY(-4px) scale(1.012);border-color:rgba(245,197,24,.55);box-shadow:0 12px 30px rgba(3,8,20,.65)}
  #vb-starladder-major .vb-sl-a{grid-column:span 2;grid-row:span 2}
  #vb-starladder-major .vb-sl-b{grid-row:span 2}
  #vb-starladder-major .vb-sl-c{grid-column:span 2}
  #vb-starladder-major .vb-sl-titlewrap{position:relative;padding:clamp(28px,4vw,54px) 0 clamp(10px,1.5vw,18px)}
  #vb-starladder-major .vb-sl-logo-bg{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:min(460px,82%);height:auto;opacity:.3;border-radius:16px;pointer-events:none;-webkit-mask-image:radial-gradient(ellipse 70% 70% at center,#000 35%,transparent 78%);mask-image:radial-gradient(ellipse 70% 70% at center,#000 35%,transparent 78%)}
  #vb-starladder-major .vb-sl-titlewrap h2{position:relative;z-index:1;text-shadow:0 2px 20px rgba(3,8,20,.9),0 0 46px rgba(3,8,20,.7)}
  #vb-starladder-major .vb-cr-cta{margin-top:clamp(34px,4vw,48px)}
  #vb-starladder-major .vb-cr-btn--gold{background:#F5C518;color:#081733;box-shadow:0 4px 18px rgba(245,197,24,.35)}
  #vb-starladder-major .vb-cr-btn--gold:hover{background:#ffd84a;box-shadow:0 8px 26px rgba(245,197,24,.5)}
  @media(max-width:1024px){#vb-starladder-major .vb-sl-grid{grid-template-columns:repeat(2,1fr);grid-auto-rows:clamp(140px,24vw,230px)}#vb-starladder-major .vb-sl-a{grid-column:span 2;grid-row:span 2}#vb-starladder-major .vb-sl-b{grid-row:span 2}#vb-starladder-major .vb-sl-c{grid-column:auto}}
  @media(max-width:600px){#vb-starladder-major .vb-sl-grid{grid-template-columns:repeat(2,1fr);grid-auto-rows:clamp(110px,26vw,170px)}}
"""

# ---------------------------------------------------------------- blocks ----
blocks = []

# 01 HERO -------------------------------------------------------------------
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Client References Hero (Block 1, v4 rebuild) -->
<section id="vb-client-references" class="vb-cr">
<style>{FRAMEWORK_CSS}{HERO_CSS}</style>
  <div class="vb-cr-hero-bg" aria-hidden="true"></div>
  <div class="vb-cr-hero-glow" aria-hidden="true"></div>
  <div class="vb-cr-wrap">
    <h1>Client References and Event Transportation Expertise – Van and Bus Rentals in Budapest, Hungary</h1>
    <p class="vb-cr-lead">Our client references demonstrate that <a href="https://vanbudapest.com">VanBudapest.com</a> delivers high quality event transportation services for every type of occasion. Over the past decades we have earned the trust of event organizers, corporate partners, sports clubs, couples and travelers by providing reliable, comfortable and bespoke transport solutions.</p>
    <div class="vb-cr-cta">
      <a href="https://vanbudapest.com/our-fleet-vip-limousines-coaches-sedans-luxury-vans/" class="vb-cr-btn vb-cr-btn--gold">View Our Fleet 🚐</a>
      <a href="https://vanbudapest.com/google-reviews-customer-feedback/" class="vb-cr-btn vb-cr-btn--line">Client Feedback ⭐</a>
    </div>
  </div>
</section>
<!-- /wp:html -->""")

# 02 STARLADDER MAJOR (NEW) --------------------------------------------------
sl545, ss545 = sl_variants(545)
sl474, ss474 = sl_variants(474)
sl557, ss557 = sl_variants(557)
sl639, ss639 = sl_variants(639)
sl621, ss621 = sl_variants(621)
sl455 = "2026/03/MAJOR-STARLADDER-2025-VB-CS2-MVMDOME-MTKSPORTPARK-455"
ss455 = (f"{U}{sl455}-768x960.webp 768w, {U}{sl455}-1229x1536.webp 1229w")

blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — StarLadder CS2 Major Budapest 2025 (Block 2, NEW, v4) -->
<section id="vb-starladder-major" class="vb-cr">
<style>{SL_CSS}</style>
  <div class="vb-cr-wrap" style="text-align:center">
    <span class="vb-sl-badge">★ Official Transportation Partner</span>
    <div class="vb-sl-titlewrap">
      <img class="vb-sl-logo-bg" src="{U}2025/11/Starladder-Major-Budapest-2025.jpg" alt="" aria-hidden="true" width="1100" height="700" loading="lazy" decoding="async">
      <h2>StarLadder <span class="vb-sl-y">Counter-Strike 2</span> Major Budapest 2025</h2>
    </div>
    <div class="vb-cr-txt">
      <p>In 2025, Budapest hosted one of the biggest events in global esports — the StarLadder Counter-Strike 2 Major — and <a href="https://vanbudapest.com">VanBudapest.com</a> served as the tournament&#8217;s official transportation partner. Throughout the championship, our fleet and chauffeurs moved professional teams, talent and event staff between Budapest Airport, the official hotels and the competition venues, the MVM Dome and the MTK Sportpark, precisely on tournament schedule.</p>
      <p>Esports runs on split-second timing, and so do we. This partnership is documented proof of our experience in esports event logistics — secure team transfers, flexible standby vehicles and discreet VIP service for players and organizers alike. Planning a gaming event, LAN final or esports bootcamp in Budapest? You are looking at the transportation partner that has already delivered on the Major stage.</p>
    </div>
    <div class="vb-sl-chips">
      <span>CS2 Major · Budapest 2025</span>
      <span>MVM Dome</span>
      <span>MTK Sportpark</span>
      <span>Teams · Talent · VIP</span>
    </div>
  </div>
  <div class="vb-sl-grid">
    <img class="vb-sl-a" src="{U}{sl545}-2048x1366.webp" alt="StarLadder CS2 Major Budapest arena with fire pyrotechnics and packed stands at the MVM Dome" width="2048" height="1366" srcset="{ss545}" sizes="(max-width:1024px) 100vw, 50vw" loading="lazy" decoding="async">
    <img class="vb-sl-b" src="{U}{sl455}-1229x1536.webp" alt="Counter-Strike 2 tournament main stage at the StarLadder Budapest Major" width="1229" height="1536" srcset="{ss455}" sizes="(max-width:1024px) 50vw, 25vw" loading="lazy" decoding="async">
    <img src="{U}{sl474}-1536x1024.webp" alt="StarLadder Budapest Major arena screen during the player entry show" width="1536" height="1024" srcset="{ss474}" sizes="(max-width:1024px) 50vw, 25vw" loading="lazy" decoding="async">
    <img src="{U}{sl557}-1536x1024.webp" alt="Championship podium celebration with confetti at the StarLadder Major Budapest" width="1536" height="1024" srcset="{ss557}" sizes="(max-width:1024px) 50vw, 25vw" loading="lazy" decoding="async">
    <img class="vb-sl-c" src="{U}{sl639}-1536x1024.webp" alt="VanBudapest chauffeur beside a Mercedes minibus on StarLadder Major transfer duty at Budapest Airport" width="1536" height="1024" srcset="{ss639}" sizes="(max-width:1024px) 50vw, 50vw" loading="lazy" decoding="async">
    <img class="vb-sl-c" src="{U}{sl621}-1536x1024.webp" alt="StarLadder Major Budapest team transfer badges held at the airport terminal" width="1536" height="1024" srcset="{ss621}" sizes="(max-width:1024px) 50vw, 50vw" loading="lazy" decoding="async">
  </div>
  <div class="vb-cr-cta">
    <a href="https://vanbudapest.com/contact-customer-reviews/" class="vb-cr-btn vb-cr-btn--gold">BOOK NOW</a>
  </div>
</section>
<!-- /wp:html -->""")

# 03 PRESTIGIOUS -------------------------------------------------------------
g = gal("vb-cr-gal--g3", [
    img("2026/02/budapest-fina-world-championships-water-polo-vip-transfer.jpg", "FINA World Championships water polo arena in Budapest", 2048, 1151),
    img("2026/07/Athletics3.png", "VanBudapest Sprinter in front of the World Athletics Championships stadium in Budapest", 1448, 1086),
    img("2026/04/puskas-arena-group-transfers-stadium-events-budapest-10.webp", "Puskás Aréna on match day, Budapest", 1920, 843),
    img("2025/09/spar-budapest-marathon-hungary-vanbudapest.jpg", "Budapest marathon event gate near the Hungarian Parliament"),
    img("2021/09/hungexpo-contact.jpg", "Event shuttle V-Class fleet at Hungexpo, Budapest", 1536, 1024),
    img("2025/12/hungarian-grand-prix-2025-hungaroring-circuit-overview.jpg", "Hungaroring circuit at sunset, Formula 1 Hungarian Grand Prix", 1536, 1024),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Prestigious Event References (Block 3, v4) -->
<section id="vb-prestigious-events" class="vb-cr vb-cr--cream">
  <div class="vb-cr-wrap">
    <h2>Prestigious Event References</h2>
    <div class="vb-cr-txt">
      <p>We are proud to have supported many high profile events in Hungary and across Europe. Our long term partnerships and repeat engagements show that our services are valued by organizers and participants alike:</p>
      <ul>
        <li><strong>• FINA World Championships – Budapest:</strong> We provided seamless transportation for attendees of multiple FINA events, including the FINA World Championships and World Cup competitions. Our coordination ensured athletes and VIP guests enjoyed punctual transfers and comfortable rides.</li>
        <li><strong>• Opera House Budapest Events &amp; Wizz Air Budapest Half Marathon:</strong> Participants and spectators relied on our vans and minibuses to move between venues and accommodation. We offered luxury vehicles and group shuttles to keep the event on schedule.</li>
        <li><strong>• Tour de Hongrie:</strong> As the official transportation partner for Hungary&#8217;s premier cycling race, we delivered efficient and reliable rides for cyclists, support teams and media crews.</li>
        <li><strong>• Budapest World Championships – Judo:</strong> Our services ensured that athletes, coaches and VIPs attending the Judo World Championships traveled safely and comfortably.</li>
        <li><strong>• Eucharistic Congress – IEC2020 at Hungexpo:</strong> Delegates experienced the convenience of our tailored event shuttles during the international Eucharistic Congress.</li>
        <li><strong>• Formula 1 Hungarian Grand Prix – Hungaroring:</strong> Fans and enthusiasts depended on our transportation services to reach the race circuit, demonstrating our ability to handle high profile sporting events.</li>
        <li><strong>• 17th FINA World Championships &amp; Other Aquatic Events:</strong> We ensured smooth logistics for swimmers, coaches and media at this globally recognized aquatic sports event.</li>
      </ul>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 04 EVENT EXPERTISE ---------------------------------------------------------
g = gal("vb-cr-gal--g4", [
    img("2025/07/ozora.jpg", "Ozora Festival Hungary"),
    img("2025/09/autumn-cultural-festivals-budapest-hungary-vanbudapest.webp", "Autumn Cultural Festivals Budapest"),
    img("2026/03/magyar-zaszlo-hatterben-csak-media-fotosok-sajto-homalyosan-sajtotajekoztato-impozans.png", "International press conference with media photographers in Budapest"),
    img("2026/04/champions-league-final-2026-budapest-vip-transfers-36.webp", "Mercedes transfer vehicle for the UEFA Champions League Final 2026 in Budapest"),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Event Expertise Expansion (Block 4, v4) -->
<section id="vb-event-expertise" class="vb-cr vb-cr--white">
  <div class="vb-cr-wrap">
    <h2>Expanding Our Event Expertise</h2>
    <div class="vb-cr-txt">
      <p>These references are only a snapshot of our experience. <a href="https://vanbudapest.com">VanBudapest.com</a> regularly supports music festivals, international congresses, trade shows, fashion weeks, technology expos and diplomatic conferences. Our team is currently preparing to be an official transportation provider for the UEFA Champions League Final 2026 in Budapest and we are already coordinating travel for club delegations, sponsors and VIP guests.</p>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 05 CORPORATE ---------------------------------------------------------------
g = gal("vb-cr-gal--g3", [
    img("V-Class-fleet/belso/vanbudapest-mercedes-v-class-chauffeur-hire-budapest-091.webp", "VIP transfer services Budapest"),
    img("V-Class-fleet/belso/vanbudapest-premium-mercedes-van-hungary-transfer-092.webp", "Airport transfer Budapest"),
    img("2026/06/Mercedes_S-class_VanBudapest-12.webp", "Mercedes S-Class executive sedan for corporate transfers in Budapest", 1620, 1080),
    img("2026/06/Mercedes_S-class_VanBudapest-25.webp", "Mercedes S-Class rear cabin configured for executive work between Budapest meetings", 1620, 1080),
    img("2022/10/papp-arena-budapest-2022.jpg", "Papp Arena corporate events Budapest"),
    img("2026/06/Mercedes_VIP_Sprinter_minibus_VanBudapest-35.webp", "Black Mercedes Sprinter for corporate shuttle service in Budapest", 1620, 1080),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Corporate &amp; Conference Transportation (Block 5, v4) -->
<section id="vb-corporate-transport" class="vb-cr vb-cr--navy">
  <div class="vb-cr-wrap">
    <h2>Corporate &amp; Conference Transportation</h2>
    <h3>Trusted by Global Brands</h3>
    <div class="vb-cr-txt">
      <p>We work with companies across diverse industries—including oil and energy, finance, insurance, cosmetics, technology and manufacturing—to deliver tailored transportation solutions for their meetings and events. Clients trust us to move senior executives, guests and employees between airports, hotels, conference centres and entertainment venues.</p>
      <h4>Comprehensive Corporate Services</h4>
      <ul>
        <li><strong>• Conference and seminar shuttles:</strong> from large conventions and product launches to intimate board meetings.</li>
        <li><strong>• Corporate roadshows and hospitality programs:</strong> we handle itineraries across multiple cities and countries.</li>
        <li><strong>• Employee shuttle services:</strong> daily or hourly transfers for staff training, team building or off site retreats.</li>
        <li><strong>• Executive transport:</strong> discreet chauffeured sedans and SUVs for CEOs, boards and VIP clients.</li>
      </ul>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 06 SPORTS ------------------------------------------------------------------
g = gal("vb-cr-gal--g4", [
    img("2025/12/hungarian-grand-prix-2025-hungaroring-aerial-view.jpg", "Aerial view of the Hungaroring during the Hungarian Grand Prix", 2048, 1365),
    img("2026/07/Athletics2.png", "Runners on the track at the World Athletics Championships in Budapest", 1536, 1024),
    img("2026/07/Aquatic-Sports.png", "Aquatic sports arena in Budapest", 1536, 1024),
    img("2026/07/ferencvaros-europa-league-2026-27-hero-1.jpg", "Football fans in a Budapest stadium on a European match night", 1599, 900),
    img("2026/04/champions-league-final-2026-budapest-vip-transfers-44.webp", "Puskás Aréna, venue of the UEFA Champions League Final in Budapest"),
    img("2026/07/football8.png", "Football match day transfer in Budapest"),
    img("2026/02/budapest-fina-world-championships-vip-event-transportation.jpg", "FINA World Championships pool in Budapest"),
    img("2026/06/Mercedes_VIP_Sprinter_minibus_VanBudapest-43.webp", "VanBudapest VIP Sprinter minibuses ready for team charter in Budapest", 1620, 1080),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Sports Events &amp; Fan Transportation (Block 6, v4) -->
<section id="vb-sports-events" class="vb-cr vb-cr--cream">
  <div class="vb-cr-wrap">
    <h2>Sports Events &amp; Fan Transportation</h2>
    <h3>Expertise in Sports Logistics</h3>
    <div class="vb-cr-txt">
      <p>From football matches and basketball tournaments to running races, cycling tours and motor sports, we understand the tight schedules and large crowds associated with athletic events. Our services include:</p>
      <ul>
        <li><strong>• Team bus charters:</strong> spacious coaches and minibuses with extra legroom, equipment storage and privacy for athletes.</li>
        <li><strong>• Fan shuttles:</strong> dedicated routes from city centres, hotels and airports to stadiums and arenas.</li>
        <li><strong>• Support for international competitions:</strong> logistics for media crews, sponsor delegations and VIP hospitality.</li>
      </ul>
      <p>Research into charter bus services notes that major customer segments include sports teams and fans, who seek ample legroom and equipment storage. We tailor our fleet to meet these requirements—supplying high capacity buses, comfortable minivans and luxury sprinters. For high demand events, we offer <strong>sports travel charter bus rentals</strong>, a niche keyword that helps attract online searches.</p>
    </div>
    <div class="vb-cr-cta">
      <a href="https://vanbudapest.com/contact-customer-reviews/" class="vb-cr-btn vb-cr-btn--gold">Book Now 🎟️</a>
      <a href="https://vanbudapest.com/champions-league-final-2026-budapest-vip-transfers/" class="vb-cr-btn vb-cr-btn--line">UEFA Champions League Final 2026 ⚽</a>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 07 UPCOMING ----------------------------------------------------------------
g = gal("vb-cr-gal--g3", [
    img("2025/02/uefa-champions-league-cup.png", "UEFA Champions League Cup"),
    img("2026/06/Mercedes_VIP_Sprinter_minibus_VanBudapest-44.webp", "VIP Sprinter fleet for team and delegation transport", 1620, 1080),
    img("2022/01/Bfured.jpeg", "Sailing regatta on Lake Balaton at Balatonfüred, aerial view"),
    img("2026/07/icesports7.png", "Indoor sports arena filled with spectators in Budapest"),
    img("2026/06/Mercedes_S-class_VanBudapest-10.webp", "Mercedes S-Class for private VIP transfers in Budapest", 1620, 1080),
    img("2026/08/V-CLASS_VANBUDAPEST_FLEET_MERCEDES-04.webp", "Mercedes V-Class for private group transfers in Budapest", 1440, 1080),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Upcoming Events (Block 7, v4) -->
<section id="vb-upcoming-events" class="vb-cr vb-cr--white">
  <div class="vb-cr-wrap">
    <h2>Upcoming Events</h2>
    <div class="vb-cr-txt">
      <ul>
        <li><strong>• UEFA Champions League Final (2026):</strong> We are gearing up to provide comprehensive transportation for teams, officials and supporters during this prestigious event.</li>
        <li><strong>• National and regional football tournaments:</strong> We serve local club matches, European Championship qualifiers and youth tournaments.</li>
        <li><strong>• Cycling &amp; running events:</strong> Our team supports marathons, half marathons and cycling tours across Hungary and neighbouring countries.</li>
      </ul>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 08 WEDDINGS ----------------------------------------------------------------
g = gal("vb-cr-gal--g4", [
    img("2023/01/events-private-budapest-transport.jpg", "Private events luxury vans Budapest"),
    img("2023/01/hungary-events-private-budapest-transport.jpg", "Budapest event shuttle"),
    img("2023/01/private-event-elegant-wedding-budapest-transfer.jpg", "Elegant wedding transfer Budapest"),
    img("2026/08/V-CLASS_VANBUDAPEST_FLEET_MERCEDES-08.webp", "Elegant black Mercedes V-Class for wedding guest transport", 1440, 1080),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Weddings &amp; Personal Celebrations (Block 8, v4) -->
<section id="vb-weddings" class="vb-cr vb-cr--navy">
  <div class="vb-cr-wrap">
    <h2>Weddings &amp; Personal Celebrations</h2>
    <h3>Elegant &amp; Stress Free Wedding Transport</h3>
    <div class="vb-cr-txt">
      <p>Your wedding day should be memorable for all the right reasons. Our wedding transportation services include:</p>
      <ul>
        <li>• Bridal party shuttles and VIP cars between ceremony and reception venues.</li>
        <li>• Guest transportation using minibuses, coaches or luxury vans to ensure everyone arrives together and on time.</li>
        <li>• Bachelor/Bachelorette parties and prom nights—party buses and mini coaches with entertainment systems.</li>
      </ul>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 09 CELEBRATIONS & YOUTH ----------------------------------------------------
g = gal("vb-cr-gal--g3", [
    img("V-Class-fleet/kulso/vanbudapest-mercedes-v-class-private-luxury-transfer-068.webp", "Mercedes V-Class for private celebrations in Budapest"),
    img("V-Class-fleet/belso/vanbudapest-mercedes-v-class-corporate-transfer-070.webp", "Minivan transfer Budapest"),
    img("2024/11/coach-hire-hungary-46-1.png", "Coach hire Hungary for group celebrations"),
    img("2025/09/create-a-high-resolution-highly-detailed-image-that-showcases-a-modern.png", "Modern safe student transport Budapest"),
    img("2025/09/budapest-kossuth-ter-hungarian-parliament-school-trip-coach-autumn-1.png", "School trip coach at Kossuth Square by the Hungarian Parliament", 1024, 1024),
    img("2025/09/lake-balaton-tihany-school-trip-coach-bus-autumn-hungary.jpg.png", "Lake Balaton school trip coach bus"),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Celebrations &amp; Private Parties + Educational Trips (Block 9, v4) -->
<section id="vb-celebrations-youth" class="vb-cr vb-cr--cream">
  <div class="vb-cr-wrap">
    <h2>Celebrations &amp; Private Parties</h2>
    <div class="vb-cr-txt">
      <p>Beyond weddings, we provide transport for anniversaries, birthdays, graduation parties, quinceañeras and family reunions. Our large fleet allows us to accommodate small intimate gatherings or hundreds of guests. We can also arrange vehicles with wheelchair lifts and ADA compliant features for accessibility.</p>
      <h3 style="margin-top:30px">Educational Trips &amp; Youth Programs</h3>
      <p>We recognize the unique needs of schools, universities, summer camps and youth organizations. Safety is our top priority:</p>
      <ul>
        <li>• School group transportation: modern buses with seatbelts, airbags and experienced drivers to take students on field trips and study tours.</li>
        <li>• Camp shuttles: door to door pickup for day camps, sports academies and music workshops.</li>
        <li>• Academic conferences and competitions: transport for debate teams, robotics contests and academic Olympiads.</li>
      </ul>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 10 AIRPORT -----------------------------------------------------------------
g = gal("vb-cr-gal--g2", [
    img("2025/09/austria-alps-mountains-vanbudapest.jpg", "Austria Alps transfer VanBudapest"),
    img("2025/09/bratislava-christmas-market-slovakia-vanbudapest.jpg", "Christmas market day trip to Prague Old Town by Mercedes V-Class"),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Airport Transfers &amp; Hourly Services (Block 10, v4) -->
<section id="vb-airport-services" class="vb-cr vb-cr--navy">
  <div class="vb-cr-wrap">
    <h2>Airport Transfers &amp; Hourly Services</h2>
    <h3>Airport Shuttles &amp; Transfers</h3>
    <div class="vb-cr-txt">
      <p>Operating 24/7, our airport transportation services cover Budapest Ferenc Liszt International Airport, Vienna International Airport, Bratislava Airport and other regional hubs. We offer:</p>
      <ul>
        <li>• Private airport shuttles for individuals or small groups.</li>
        <li>• Group transfers with minibuses and coaches for delegations and tour groups.</li>
        <li>• Meet and greet services, flight tracking and luggage assistance.</li>
      </ul>
      <p>To improve visibility for these services, digital marketing experts advise optimizing content with terms like &#8220;airport shuttle&#8221; and &#8220;airport transportation&#8221;. Our website highlights our on time performance, mobile friendly booking and competitive pricing.</p>
      <h4>Hourly &amp; Point to Point Services</h4>
      <p>Whether you require transportation for a few hours or an entire day, we provide hourly ride services in Budapest, across Hungary and in neighbouring capitals such as Vienna and Bratislava. Clients choose these flexible options for business meetings, city tours, shopping trips, nightlife and personal errands.</p>
    </div>
    <div class="vb-cr-cta">
      <a href="https://vanbudapest.com/contact-customer-reviews/" class="vb-cr-btn vb-cr-btn--gold">Book Now ✈️</a>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 11 CITY TOURS --------------------------------------------------------------
g = gal("vb-cr-gal--g3", [
    img("2025/09/villany-wine-region-cabernet-franc-vanbudapest.jpg", "Villány wine region tour VanBudapest"),
    img("2025/09/tokaj-wine-region-aszu-unesco-vanbudapest.jpg", "Tokaj wine region UNESCO tour VanBudapest"),
    img("2025/09/etyek-wine-region-budapest-vineyards-vanbudapest.jpg.jpg", "Etyek wine region vineyards VanBudapest"),
    img("2025/06/447380719.jpg", "Fine dining experience on a private tour"),
    img("V-Class-fleet/flotta/vanbudapest-premium-mercedes-van-hungary-transfer-038.webp", "VanBudapest Mercedes V-Class fleet with chauffeurs in Budapest"),
    img("2025/02/Kurtoskalacs_1.webp", "Hungarian chimney cake cultural experience VanBudapest"),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — City Tours, Wine Routes &amp; Cultural Experiences (Block 11, v4) -->
<section id="vb-city-tours" class="vb-cr vb-cr--cream">
  <div class="vb-cr-wrap">
    <h2>City Tours, Wine Routes &amp; Cultural Experiences</h2>
    <div class="vb-cr-txt">
      <p>We curate bespoke tours showcasing the history, culture and gastronomy of Central Europe. Options include:</p>
      <ul>
        <li>• Budapest city tours covering UNESCO World Heritage sites, ruin pubs and thermal baths.</li>
        <li>• Danube Bend &amp; countryside excursions exploring castles, vineyards and charming villages.</li>
        <li>• Vienna and Bratislava day trips with highlights such as Schönbrunn Palace, the Hofburg, Bratislava Castle and the Old Town.</li>
        <li>• Wine tours in Hungary&#8217;s Tokaj region or Austria&#8217;s Wachau Valley, with comfortable buses and knowledgeable guides.</li>
      </ul>
      <p>For global visibility, marketing experts encourage incorporating keywords like &#8220;sightseeing tour&#8221;, &#8220;city tour&#8221; and &#8220;wine tour&#8221;. Our content emphasises the convenience of group tours and the luxury of private excursions.</p>
      <h3 style="margin-top:30px">International &amp; Cross Border Transportation</h3>
      <p>With Schengen zone access and an experienced logistics team, we coordinate cross border travel for corporate delegations, sports teams and tour groups. Services include:</p>
      <ul>
        <li>• Multiple city itineraries across Hungary, Austria, Slovakia, Czech Republic, Slovenia, Croatia and beyond.</li>
        <li>• Customs and immigration assistance for non EU visitors.</li>
        <li>• Coordination with foreign partners to ensure seamless handovers and consistent service standards.</li>
      </ul>
      <p>Our ability to handle complex logistics and route planning distinguishes us from local competitors and appeals to international clientele.</p>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 12 FLEET -------------------------------------------------------------------
g = gal("vb-cr-gal--g3", [
    img("2025/05/vanbudapest-luxury-vip-sprinter-minibus.png", "VanBudapest Luxury VIP Sprinter Minibus"),
    img("2025/05/budapest-hungary-private-transfer-V-class.png", "Mercedes V-Class Budapest private transfer"),
    img("2025/05/budapest-hungary-private-transfer-S-class.png", "Mercedes S-Class chauffeur service Budapest"),
    img("2026/06/Mercedes_S-class_VanBudapest-42.webp", "Mercedes S-Class from the 2026 VanBudapest fleet at the Budapest airport garage", 1620, 1080),
    img("2026/08/V-CLASS_VANBUDAPEST_FLEET_MERCEDES-45.webp", "Luxury black Mercedes SUV from the 2026 VanBudapest fleet"),
    img("2026/06/Mercedes_VIP_Sprinter_minibus_VanBudapest-39.webp", "Mercedes VIP Sprinter vans from the 2026 VanBudapest fleet", 1620, 1080),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Our Fleet &amp; Capacity (Block 12, v4) -->
<section id="vb-fleet-capacity" class="vb-cr vb-cr--navydeep">
  <div class="vb-cr-wrap">
    <h2>Our Fleet &amp; Capacity</h2>
    <div class="vb-cr-txt">
      <p>We maintain a diverse fleet of modern, comfortable vehicles to suit any requirement:</p>
      <ul>
        <li>• Luxury sedans and executive cars for VIP transfers and discrete travel.</li>
        <li>• Premium minivans and sprinter vans for small groups (6–8 passengers) with ample luggage space.</li>
        <li>• Mercedes V Class and similar luxury minivans for business and leisure trips.</li>
        <li>• Minibuses (15–24 passengers) for medium sized groups, corporate shuttles and family celebrations.</li>
        <li>• Full size coaches and luxury buses (50+ passengers) for conferences, sports teams, school trips and large tours.</li>
      </ul>
      <p>We also offer specialty vehicles, including limo buses, vintage wedding cars, double decker coaches and wheelchair accessible buses. Each vehicle undergoes regular maintenance and safety checks, and all are equipped with air conditioning, comfortable seating, seatbelts, onboard Wi Fi (on request), PA systems and optional refreshments.</p>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 13 SAFETY ------------------------------------------------------------------
g = gal("vb-cr-gal--g2", [
    img("2021/05/d1a9b-meet-and-greet-service-budapest-transfer.jpg", "Meet and greet chauffeur Budapest"),
    img("2021/05/6bb53-meet-greet-budapest-driver-pick-up-airport-help.jpg", "Professional driver Budapest pickup"),
])
blocks.append(f"""<!-- wp:html -->
<!-- VanBudapest.com — Safety, Quality &amp; Professionalism (Block 13, v4) -->
<section id="vb-safety-quality" class="vb-cr vb-cr--navy">
  <div class="vb-cr-wrap">
    <h2>Safety, Quality &amp; Professionalism</h2>
    <h3>Experienced Drivers</h3>
    <div class="vb-cr-txt">
      <p>Our chauffeurs are the backbone of our service. They are:</p>
      <ul>
        <li>• Licensed and professionally trained, with years of experience in passenger transportation.</li>
        <li>• Multilingual, assisting international guests in English, German, French and other languages.</li>
        <li>• Punctual and courteous, ensuring guests feel welcome and secure.</li>
      </ul>
      <h4>Focus on Safety</h4>
      <p>We adhere to strict safety protocols and continuously update our fleet with advanced safety features. To build trust online, industry experts recommend addressing common customer questions about safety protocols and driver qualifications. We publish detailed information about our training programs, vehicle maintenance schedules and insurance coverage.</p>
      <h4>Reliability &amp; Flexibility</h4>
      <p>Whether you need a simple point to point transfer or a complex multi day itinerary, we adapt to your schedule. Our operations team monitors flight arrivals, traffic conditions and event schedules to adjust pickups and routes in real time. We also offer 24/7 customer support and dedicated coordinators for large events.</p>
    </div>
  </div>
  {g}
</section>
<!-- /wp:html -->""")

# 14 WHY CHOOSE --------------------------------------------------------------
blocks.append("""<!-- wp:html -->
<!-- VanBudapest.com — Why Choose VanBudapest.com (Block 14, v4) -->
<section id="vb-why-choose" class="vb-cr vb-cr--white">
  <div class="vb-cr-wrap">
    <h2>Why Choose VanBudapest.com?</h2>
    <div class="vb-cr-txt">
      <ul>
        <li><strong>• Decades of Experience:</strong> Since 1988, we have been providing transportation solutions in Budapest and across Europe. Our history shows stability and reliability.</li>
        <li><strong>• Trusted by Leading Organizations:</strong> We serve prestigious sporting bodies like UEFA, FIFA, national sports federations, and corporate giants in oil, finance, insurance, cosmetics, IT and more.</li>
        <li><strong>• Comprehensive Services:</strong> We cover airport transfers, city tours, wedding shuttles, corporate roadshows, sports team travel, educational trips, cruise transfers, VIP events, music festivals, film productions, factory visits, trade shows, product launches and even camp transportation. Our ability to manage everything from small family gatherings to multi thousand person conferences sets us apart.</li>
        <li><strong>• Regional &amp; Global Coverage:</strong> We operate extensively in Budapest, Hungary, and all major cities, including Vienna, Bratislava, Prague, Krakow and Zagreb. We also serve international routes across Europe.</li>
        <li><strong>• Modern, Diverse Fleet:</strong> Our vehicles range from elegant sedans and luxury minivans to minibuses and large coaches, ensuring the right fit for every event.</li>
        <li><strong>• Competitive Pricing &amp; Discounts:</strong> We offer transparent pricing and online reservation discounts of up to 10%, encouraging early bookings.</li>
      </ul>
      <h3 style="margin-top:30px">Areas of Expertise</h3>
      <ul>
        <li>• Corporate meetings, incentives, conferences and exhibitions (MICE).</li>
        <li>• Sporting events, from amateur leagues to world championships.</li>
        <li>• Weddings, galas, balls and private celebrations.</li>
        <li>• Concerts, festivals, fashion shows and cultural events.</li>
        <li>• Trade shows, product launches and promotional tours.</li>
        <li>• School trips, university excursions and youth camps.</li>
        <li>• VIP travel, executive roadshows and celebrity tours.</li>
        <li>• City tours, sightseeing excursions and wine tastings.</li>
      </ul>
    </div>
  </div>
</section>
<!-- /wp:html -->""")

# 15 CONTACT CTA -------------------------------------------------------------
blocks.append("""<!-- wp:html -->
<!-- VanBudapest.com — Contact &amp; CTA (Block 15, v4) -->
<section id="vb-contact-cta" class="vb-cr vb-cr--navydeep">
  <div class="vb-cr-wrap">
    <h2>Get in Touch</h2>
    <div class="vb-cr-txt">
      <p style="text-align:center">Contact us today at <a href="mailto:info@vanbudapest.com">info@vanbudapest.com</a> to discuss your upcoming event, request a customized quote or arrange a site visit. Let our team craft a transportation plan that aligns perfectly with your needs, budget and schedule. With <a href="https://vanbudapest.com">VanBudapest.com</a>, you can focus on your event while we handle every aspect of your guests&#8217; journey.</p>
    </div>
    <div class="vb-cr-cta">
      <a href="https://vanbudapest.com/contact-customer-reviews/" class="vb-cr-btn vb-cr-btn--gold">Book Now ✉️</a>
    </div>
    <div class="vb-cr-cta" style="margin-top:16px">
      <a href="https://vanbudapest.com/contact-customer-reviews/" class="vb-cr-btn vb-cr-btn--line">Visit our Contact Page →</a>
    </div>
  </div>
</section>
<!-- /wp:html -->""")

# 16 SEO FOOTER NOTE ---------------------------------------------------------
blocks.append("""<!-- wp:html -->
<!-- VanBudapest.com — SEO Footer Microcopy (Block 16, v4) -->
<section id="vb-seo-footer-note" class="vb-cr vb-cr--cream" style="padding:clamp(40px,4vw,56px) 0">
<style>
  #vb-seo-footer-note .vb-cr-note{max-width:940px;margin:0 auto;padding:0 clamp(18px,4vw,28px);font-size:12.5px;line-height:1.75;color:#6C7686;text-align:left}
  #vb-seo-footer-note .vb-cr-note p{margin:0 0 12px}
  #vb-seo-footer-note .vb-cr-note strong{color:#4E5866}
  #vb-seo-footer-note .vb-cr-note a{color:#8A6F2F;text-decoration:none}
</style>
  <div class="vb-cr-note">
      <p>These references showcase our commitment to providing top-quality event transportation services for a diverse range of occasions in Budapest, earning the trust of event organizers and participants alike.</p>
      <p><strong>FINA BUDAPEST EVENT | FINA World Championships BUDAPEST:</strong> Our reliable event transportation services were trusted for attendees of the prestigious FINA World Championships, ensuring timely and comfortable arrivals.</p>
      <p><strong>OPERA HOUSE BUDAPEST EVENTS | WIZZ AIR BUDAPEST HALF MARATHON:</strong> Participants of the Wizz Air Budapest Half Marathon experienced hassle-free transportation, enjoying a luxurious ride to the event&#8217;s vibrant locations.</p>
      <p><strong>Tour de Hongrie:</strong> vanbudapest.com played a crucial role in the success of Tour de Hongrie, providing efficient and reliable transportation solutions for both participants and organizers.</p>
      <p><strong>UNIVERSITY SPORTS FESTIVAL BUDAPEST:</strong> Attendees of the University Sports Festival in Budapest benefited from our professional event transportation services, contributing to the overall success of the gathering.</p>
      <p><strong>Budapest World Championships – JUDO:</strong> Our services were essential for those attending the Budapest World Championships in Judo, ensuring a smooth and comfortable journey to and from the event.</p>
      <p><strong>HUNGEXPO BUDAPEST EVENT | Eucharistic Congress – IEC2020:</strong> Participants of the Eucharistic Congress in Budapest experienced the convenience of our event transportation, enhancing their overall event experience.</p>
      <p><strong>BUDAPEST, HUNGARY – HUNGARORING | F1 GP:</strong> Fans and enthusiasts traveling to the F1 Grand Prix at Hungaroring relied on our transportation services, contributing to the success of this high-profile event.</p>
      <p>The 17th FINA World Championships were held in Budapest, Hungary: vanbudapest.com played a pivotal role in ensuring smooth transportation for attendees of this globally recognized aquatic sports event.</p>
      <p>Explore more of our references here.</p>
      <p>Looking for a reliable and high-quality event transportation solution in Budapest or Hungary for 2025?<br>
      If you&#8217;re planning an event in Budapest or in Hungary, let vanbudapest.com help alleviate your transportation concerns. Make your reservation now and take advantage of our online discounts, saving you up to 10% on the total price. Contact us today to learn more about our event transportation services and get started.</p>
      <p>Efficient and Reliable Event Transportation – Choose vanbudapest.com for All Your Event Transportation Needs in Hungary. Contact us today for a quote: <a href="mailto:info@vanbudapest.com">info@vanbudapest.com</a></p>
      <p>Look no further than vanbudapest.com With years of experience in the industry, our team is well equipped to handle all of your event transportation needs. From small groups to large-scale events, we offer complete transfer handling and a range of modern vehicles, including minibuses and buses, all driven by professional and knowledgeable drivers. Contact us today to find out how we can help make your next event a success!</p>
      <p>With a fleet of modern and well-maintained vehicles, we can accommodate groups of any size. Whether you need airport transfers, transportation for sightseeing tours, or transportation for an important meeting or event, we&#8217;ve got you covered. Our drivers are highly trained, knowledgeable, and professional, ensuring that your guests arrive at the event on time and in comfort.</p>
      <p>When it comes to event transportation, you want to make sure that everything runs smoothly and that your guests arrive at the event comfortably and on time. With vanbudapest.com, you can have peace of mind knowing that your event transportation needs will be handled by professionals. Our company specializes in providing high-end private transportation services in Budapest, Hungary, and we have a reputation for delivering the highest quality services to our clients.</p>
  </div>
</section>
<!-- /wp:html -->""")

# 17 FAQ ---------------------------------------------------------------------
blocks.append("""<!-- wp:html -->
<!-- VanBudapest.com — FAQ Section: Client References / Services (Block 17, v4) -->
<section id="vb-faq-client-references" class="vb-cr vb-cr--white">
<style>
  #vb-faq-client-references .vb-cr-faq{max-width:940px;margin:0 auto;padding:0 clamp(18px,4vw,28px);text-align:left}
  #vb-faq-client-references .vb-cr-faq > div{background:#FBFAF7;border:1px solid #E8E4D8;border-radius:14px;padding:18px 22px;margin:0 0 14px;font-size:1rem;line-height:1.8;color:#2A3245;transition:box-shadow .3s ease,transform .3s ease}
  #vb-faq-client-references .vb-cr-faq > div:hover{box-shadow:0 6px 18px rgba(10,31,68,.08);transform:translateY(-2px)}
  #vb-faq-client-references .vb-cr-faq strong{color:#0A1F44}
</style>
  <div class="vb-cr-wrap">
    <h2>FAQ – Client References / Services</h2>
  </div>
  <div class="vb-cr-faq">
      <div><strong>1. What kinds of events do you provide references and services for?</strong><br>
      VanBudapest offers transportation services for sporting events, conferences, festivals, VIP gatherings, large-scale travel, and international occasions — as shown by our references (e.g. FINA World Championships, marathons, auto races, etc.).</div>
      <div><strong>2. How do you choose which references to feature?</strong><br>
      We highlight key events and partnerships where our services played an important role in transportation logistics, and for which we received positive client feedback. These references demonstrate our credibility.</div>
      <div><strong>3. What does it mean that &#8220;references&#8221; are displayed on the site?</strong><br>
      It shows that previous clients entrusted us with similar tasks, and we successfully delivered. It adds proof to our quality, not just decoration.</div>
      <div><strong>4. Can I have my event featured as a reference too?</strong><br>
      Yes — after an event, if you're open to providing documentation (photos, permissions, feedback), we&#8217;d be happy to list it among our references.</div>
      <div><strong>5. How can I verify that the references are real?</strong><br>
      Our referenced events are public (e.g. FINA world championships, Tour de Hongrie). Many are organized by recognized institutions and have media coverage. If needed, we can also share contactable references, photos, or testimonials.</div>
      <div><strong>6. Are your reference events only in Budapest or all over Hungary?</strong><br>
      Although many references are in Budapest, our services are not limited to the city — we operate throughout Hungary and in the surrounding region for large event transport.</div>
      <div><strong>7. What kinds of vehicles and capacities do you use for large events?</strong><br>
      We deploy modern buses, minivans, comfortable transfer vehicles, and VIP cars. Capacity is flexible, ranging from small groups to several hundreds, depending on your needs.</div>
      <div><strong>8. How do you ensure every guest arrives to the event on time?</strong><br>
      We prepare detailed schedules considering traffic, route planning, and buffer times. Experienced drivers and coordinators monitor logistics, and we maintain live communication in case adjustments are needed.</div>
      <div><strong>9. What happens if an unexpected situation occurs (e.g. road closure)?</strong><br>
      VanBudapest is flexible: we have alternative routes preplanned, redirect early if needed, and our drivers and operations staff continuously monitor conditions to implement the best solution.</div>
      <div><strong>10. How do I request a quote and what are your payment terms?</strong><br>
      We prepare a custom quote once you share your requirements via form or direct contact. The price includes vehicles, operations, drivers, insurance, and coordination. Payment terms (deposit, installments, final invoice) are agreed upon in advance.</div>
  </div>
</section>
<!-- /wp:html -->""")

content = "\n\n".join(blocks) + "\n"
open("new_content.html", "w").write(content)
print("blocks:", len(blocks), "| chars:", len(content))
print("imgs:", content.count("<img"), "| style tags:", content.count("<style"))
