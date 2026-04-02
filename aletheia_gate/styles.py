"""Aletheia Gate — Complete CSS. All visuals driven by class_name= on rx.* components."""

BG   = "#03050d"
BODY = "'Rajdhani', sans-serif"

GLOBAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=JetBrains+Mono:wght@300;400;500;700&family=Rajdhani:wght@300;400;500;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
:root{
  --cyan:#00cfff;--pink:#ff0080;--purple:#9d4edd;--green:#00e5a0;
  --amber:#ffaa00;--red:#ff3355;--bg:#03050d;
  --dim:rgba(220,185,240,0.52);
  --fh:'Orbitron',monospace;--fm:'JetBrains Mono',monospace;--fb:'Rajdhani',sans-serif;
}
html,body{height:100%;background:var(--bg);color:#fff;font-family:var(--fb);overflow-x:hidden;}
::-webkit-scrollbar{width:3px;}
::-webkit-scrollbar-track{background:#020408;}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,var(--pink),var(--cyan),var(--purple));border-radius:2px;}

@keyframes gpulse{0%,100%{opacity:.18;}50%{opacity:.45;}}
@keyframes gshift{0%{background-position:0 0;}100%{background-position:60px 60px;}}
@keyframes scan{0%{top:-2px;opacity:1;}95%{opacity:1;}100%{top:100%;opacity:0;}}
@keyframes scan2{0%{top:-2px;}100%{top:100%;}}
@keyframes flicker{0%,100%{opacity:1;}89%{opacity:1;}90%{opacity:.15;}91%{opacity:1;}94%{opacity:.5;}95%{opacity:1;}}
@keyframes sleft{from{opacity:0;transform:translateX(-36px);}to{opacity:1;transform:translateX(0);}}
@keyframes sup{from{opacity:0;transform:translateY(28px);}to{opacity:1;transform:translateY(0);}}
@keyframes gpink{0%,100%{box-shadow:0 0 8px var(--pink),0 0 18px rgba(255,0,128,.3);}50%{box-shadow:0 0 24px var(--pink),0 0 48px rgba(255,0,128,.5),0 0 80px rgba(255,0,128,.18);}}
@keyframes gcyan{0%,100%{box-shadow:0 0 8px var(--cyan),0 0 18px rgba(0,207,255,.3);}50%{box-shadow:0 0 22px var(--cyan),0 0 44px rgba(0,207,255,.5);}}
@keyframes bpulse{0%,100%{border-color:rgba(255,0,128,.15);}50%{border-color:rgba(255,0,128,.52);}}
@keyframes bholo{0%{border-color:rgba(255,0,128,.22);}25%{border-color:rgba(0,207,255,.28);}50%{border-color:rgba(157,78,221,.22);}75%{border-color:rgba(0,229,160,.22);}100%{border-color:rgba(255,0,128,.22);}}
@keyframes mglow{0%{box-shadow:0 0 50px rgba(255,0,128,.1),inset 0 0 50px rgba(255,0,128,.03);}50%{box-shadow:0 0 50px rgba(0,207,255,.1),inset 0 0 50px rgba(0,207,255,.03);}100%{box-shadow:0 0 50px rgba(255,0,128,.1),inset 0 0 50px rgba(255,0,128,.03);}}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.35;transform:scale(.92);}}
@keyframes pgrow{0%,100%{transform:scale(1);}50%{transform:scale(1.1);}}
@keyframes rot{from{transform:rotate(0);}to{transform:rotate(360deg);}}
@keyframes ticker{0%{transform:translateX(100%);}100%{transform:translateX(-100%);}}
@keyframes ticker2{0%{transform:translateX(0%);}100%{transform:translateX(-200%);}}
@keyframes dstream{0%{background-position:0% 50%;}100%{background-position:200% 50%;}}
@keyframes shimmer{0%{background-position:-200% 0;}100%{background-position:200% 0;}}
@keyframes hlines{0%{background-position:0 0;}100%{background-position:0 80px;}}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:0;}}
@keyframes nflicker{0%,19%,21%,23%,25%,54%,56%,100%{opacity:1;}20%,24%,55%{opacity:.35;}}
@keyframes pbeam{0%{transform:translateX(-100%);}100%{transform:translateX(400%);}}
@keyframes epulse{0%,100%{opacity:.3;transform:scale(1);}50%{opacity:.8;transform:scale(1.12);}}
@keyframes cspark{0%,100%{opacity:.75;}50%{opacity:1;box-shadow:0 0 8px currentColor;}}
@keyframes srev{from{opacity:0;transform:translateX(-8px);}to{opacity:1;transform:translateX(0);}}
@keyframes countup{from{opacity:0;transform:scale(.5);}to{opacity:1;transform:scale(1);}}
@keyframes orb{0%,100%{transform:translate(0,0) scale(1);}25%{transform:translate(28px,-18px) scale(1.08);}50%{transform:translate(-18px,26px) scale(.92);}75%{transform:translate(18px,18px) scale(1.04);}}
@keyframes rglow{0%,100%{filter:drop-shadow(0 0 8px rgba(255,0,128,.55));}50%{filter:drop-shadow(0 0 20px rgba(255,0,128,1)) drop-shadow(0 0 40px rgba(0,207,255,.5));}}
@keyframes rrot{from{transform:rotate(0);}to{transform:rotate(360deg);}}
@keyframes rsweep{from{transform:rotate(-90deg);}to{transform:rotate(270deg);}}
@keyframes lgrow{from{width:0;}to{width:100%;}}
@keyframes nring{0%{box-shadow:0 0 0 0 rgba(255,0,128,.5);}70%{box-shadow:0 0 0 14px rgba(255,0,128,0);}100%{box-shadow:0 0 0 0 rgba(255,0,128,0);}}
@keyframes cbg{0%{background-position:0% 0%;}50%{background-position:100% 100%;}100%{background-position:0% 0%;}}
@keyframes mgpulse{0%,100%{opacity:1;text-shadow:0 0 8px #ff00ff,0 0 16px rgba(255,0,255,.4);}50%{opacity:.65;text-shadow:0 0 16px #ff00ff,0 0 32px rgba(255,0,255,.7),0 0 48px rgba(255,0,255,.35);}}

/* ROOT */
.ag-root{position:relative;min-height:100vh;background:var(--bg);overflow-x:hidden;}
.ag-page{position:relative;z-index:1;}

/* GRID BG */
.ag-grid-bg{
  position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(ellipse 80% 60% at 20% 30%,rgba(255,0,128,.05) 0%,transparent 60%),
    radial-gradient(ellipse 60% 80% at 80% 70%,rgba(0,207,255,.04) 0%,transparent 60%),
    radial-gradient(ellipse 40% 40% at 50% 50%,rgba(157,78,221,.03) 0%,transparent 70%),
    linear-gradient(rgba(255,0,128,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,207,255,.025) 1px,transparent 1px);
  background-size:100% 100%,100% 100%,100% 100%,52px 52px,52px 52px;
  animation:gpulse 6s ease-in-out infinite,gshift 22s linear infinite;
}
.ag-orb{position:fixed;border-radius:50%;pointer-events:none;z-index:0;}
.ag-orb-1{width:600px;height:600px;top:-120px;left:-120px;background:radial-gradient(circle,rgba(255,0,128,.08) 0%,transparent 65%);animation:orb 14s ease-in-out infinite;}
.ag-orb-2{width:800px;height:800px;bottom:-200px;right:-200px;background:radial-gradient(circle,rgba(0,207,255,.06) 0%,transparent 65%);animation:orb 18s ease-in-out infinite reverse;}
.ag-orb-3{width:400px;height:400px;top:40%;left:48%;background:radial-gradient(circle,rgba(157,78,221,.05) 0%,transparent 70%);animation:orb 11s ease-in-out 3s infinite;}

/* NAV */
.ag-nav{position:fixed;top:0;left:0;right:0;z-index:200;background:rgba(3,5,13,.88);backdrop-filter:blur(40px) saturate(180%);border-bottom:1px solid rgba(255,0,128,.18);box-shadow:0 2px 0 rgba(0,207,255,.08),0 20px 40px rgba(0,0,0,.5);}
.ag-nav-inner{max-width:1280px;margin:0 auto;padding:0 52px;height:68px;display:flex;align-items:center;justify-content:space-between;gap:24px;}
.ag-logo-ring{position:relative;width:44px;height:44px;flex-shrink:0;}
.ag-logo-ring-outer{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,var(--pink),var(--cyan),var(--purple),var(--green),var(--pink));animation:rot 4s linear infinite;}
.ag-logo-ring-inner{position:absolute;inset:3px;border-radius:50%;background:var(--bg);display:flex;align-items:center;justify-content:center;font-family:var(--fh);font-size:18px;color:var(--pink);text-shadow:0 0 14px rgba(255,0,128,.7);}
.ag-brand-main{font-family:var(--fh);font-size:13px;font-weight:900;color:var(--pink);letter-spacing:.14em;line-height:1;text-shadow:0 0 16px rgba(255,0,128,.6);animation:nflicker 6s linear infinite;}
.ag-brand-sub{font-family:var(--fh);font-size:7px;color:var(--cyan);letter-spacing:.38em;text-shadow:0 0 8px rgba(0,207,255,.5);}
.ag-nav-links{display:flex;gap:4px;align-items:center;}
.ag-nav-link{font-family:var(--fh);font-size:9px;letter-spacing:.18em;color:rgba(220,185,240,.5);padding:8px 18px;cursor:pointer;transition:all .2s;border-bottom:1px solid transparent;text-transform:uppercase;}
.ag-nav-link:hover{color:var(--cyan);border-bottom-color:var(--cyan);text-shadow:0 0 12px rgba(0,207,255,.7);}
.ag-online-chip{display:flex;align-items:center;gap:6px;padding:5px 12px;border:1px solid rgba(0,229,160,.25);border-radius:20px;background:rgba(0,229,160,.05);font-family:var(--fh);font-size:8px;color:var(--green);letter-spacing:.25em;}
.ag-nav-btn-ghost{font-family:var(--fh);font-size:9px;letter-spacing:.15em;background:transparent;border:1px solid rgba(0,207,255,.3);color:rgba(220,185,240,.6);padding:9px 22px;cursor:pointer;border-radius:3px;transition:all .2s;}
.ag-nav-btn-ghost:hover{border-color:var(--cyan);color:var(--cyan);box-shadow:0 0 16px rgba(0,207,255,.25);}

/* BUTTONS */
.ag-btn{font-family:var(--fh);font-size:11px;letter-spacing:.22em;padding:13px 32px;background:linear-gradient(90deg,rgba(255,0,128,.12),rgba(0,207,255,.08));border:1px solid var(--pink);color:#fff;cursor:pointer;position:relative;overflow:hidden;clip-path:polygon(10px 0%,100% 0%,calc(100% - 10px) 100%,0% 100%);animation:gpink 2s ease-in-out infinite;text-shadow:0 0 12px rgba(255,0,128,.8);transition:all .25s cubic-bezier(.4,0,.2,1);}
.ag-btn::before{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,0,128,.28),rgba(0,207,255,.18),transparent);transform:translateX(-100%);transition:transform .5s cubic-bezier(.4,0,.2,1);}
.ag-btn:hover{background:linear-gradient(90deg,rgba(255,0,128,.24),rgba(0,207,255,.18));transform:translateY(-1px);}
.ag-btn:hover::before{transform:translateX(100%);}
.ag-btn:active{transform:translateY(0) scale(.98);}
.ag-btn-sm{font-size:9px;padding:9px 22px;}
.ag-btn-lg{font-size:12px;padding:17px 52px;}
.ag-btn-ghost{font-family:var(--fh);font-size:10px;letter-spacing:.2em;padding:11px 28px;background:transparent;border:1px solid rgba(0,207,255,.28);color:rgba(220,185,240,.6);cursor:pointer;border-radius:2px;transition:all .25s;}
.ag-btn-ghost:hover{border-color:var(--cyan);color:var(--cyan);box-shadow:0 0 20px rgba(0,207,255,.28);}
.ag-btn-link{font-family:var(--fh);font-size:10px;letter-spacing:.2em;background:transparent;border:none;color:rgba(220,185,240,.5);cursor:pointer;padding:13px 0;transition:all .3s;}
.ag-btn-link:hover{color:var(--cyan);}
.ag-btn-cta-sec{font-family:var(--fh);font-size:9px;letter-spacing:.2em;background:transparent;border:1px solid rgba(0,207,255,.25);color:rgba(220,185,240,.55);padding:17px 36px;cursor:pointer;border-radius:2px;transition:all .3s;}
.ag-btn-cta-sec:hover{border-color:var(--cyan);color:var(--cyan);}

/* GLASS */
.ag-glass{background:linear-gradient(135deg,rgba(255,0,128,.055),rgba(0,207,255,.025),rgba(157,78,221,.035));backdrop-filter:blur(32px) saturate(180%);-webkit-backdrop-filter:blur(32px) saturate(180%);border:1px solid rgba(255,0,128,.18);border-radius:6px;position:relative;overflow:hidden;animation:mglow 8s ease-in-out infinite,bholo 7s linear infinite;box-shadow:0 8px 32px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.04);}
.ag-glass::before{content:'';position:absolute;inset:0;background:linear-gradient(105deg,transparent 40%,rgba(255,255,255,.018) 50%,transparent 60%);background-size:200% 100%;animation:shimmer 4.5s ease-in-out infinite;pointer-events:none;z-index:1;}
.ag-glass::after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,207,255,.01) 3px,rgba(0,207,255,.01) 4px);animation:hlines 3s linear infinite;pointer-events:none;z-index:1;}

/* CORNERS */
.ag-c{position:absolute;width:18px;height:18px;border-style:solid;animation:cspark 3s ease-in-out infinite;z-index:2;}
.ag-c-tl{top:0;left:0;border-width:2px 0 0 2px;border-color:var(--pink);animation-delay:0s;}
.ag-c-tr{top:0;right:0;border-width:2px 2px 0 0;border-color:var(--cyan);animation-delay:.75s;}
.ag-c-bl{bottom:0;left:0;border-width:0 0 2px 2px;border-color:var(--cyan);animation-delay:1.5s;}
.ag-c-br{bottom:0;right:0;border-width:0 2px 2px 0;border-color:var(--pink);animation-delay:2.25s;}

/* SCAN */
.ag-scan{position:absolute;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--pink) 35%,var(--cyan) 65%,transparent);filter:blur(.5px);animation:scan 2.5s linear infinite;pointer-events:none;z-index:10;box-shadow:0 0 8px var(--pink),0 0 16px rgba(0,207,255,.4);}
.ag-scan2{position:absolute;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(0,207,255,.5),transparent);animation:scan 2.5s linear infinite 1.25s;pointer-events:none;z-index:10;}

/* INPUTS */
.ag-input{background:rgba(255,0,128,.04);border:1px solid rgba(255,0,128,.2);border-bottom:2px solid rgba(255,0,128,.75);color:#fff;font-family:var(--fm);font-size:13px;line-height:1.45;min-height:44px;padding:10px 16px;outline:none;transition:all .3s;border-radius:4px 4px 0 0;caret-color:var(--cyan);display:block;}
.ag-input:focus{border-color:rgba(255,0,128,.55);background:rgba(255,0,128,.07);box-shadow:0 0 20px rgba(255,0,128,.15);}
.ag-input::placeholder{color:rgba(255,0,128,.3);}
.ag-textarea{width:100%;background:rgba(255,0,128,.04);border:1px solid rgba(255,0,128,.2);border-bottom:2px solid rgba(255,0,128,.75);color:#fff;font-family:var(--fm);font-size:13px;line-height:1.45;padding:10px 16px;outline:none;resize:vertical;min-height:90px;transition:all .3s;border-radius:4px 4px 0 0;caret-color:var(--cyan);display:block;}
.ag-textarea:focus{border-color:rgba(255,0,128,.55);background:rgba(255,0,128,.07);}
.ag-textarea::placeholder{color:rgba(255,0,128,.3);}

/* DOTS */
.ag-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0;}
.ag-dot-g{background:var(--green);box-shadow:0 0 8px var(--green),0 0 16px rgba(0,229,160,.35);animation:pulse 2.5s infinite;}
.ag-dot-p{background:var(--pink);box-shadow:0 0 8px var(--pink),0 0 16px rgba(255,0,128,.35);animation:pulse 2s infinite;}
.ag-dot-c{background:var(--cyan);box-shadow:0 0 8px var(--cyan),0 0 16px rgba(0,207,255,.35);animation:pulse 1.8s infinite;}
.ag-dot-v{background:var(--purple);box-shadow:0 0 8px var(--purple),0 0 16px rgba(157,78,221,.35);animation:pulse 2.2s infinite;}
.ag-dot-a{background:var(--amber);box-shadow:0 0 6px var(--amber);}
.ag-dot-off{background:rgba(255,255,255,.2);}

/* HUD */
.ag-h{font-family:var(--fh);font-size:8px;letter-spacing:.25em;color:var(--dim);text-transform:uppercase;}
.ag-h-sm{font-family:var(--fh);font-size:7px;letter-spacing:.22em;color:var(--dim);text-transform:uppercase;}
.ag-h-p{color:var(--pink);text-shadow:0 0 8px rgba(255,0,128,.5);}
.ag-h-c{color:var(--cyan);text-shadow:0 0 8px rgba(0,207,255,.5);}
.ag-h-g{color:var(--green);text-shadow:0 0 8px rgba(0,229,160,.5);}
.ag-mono{font-family:var(--fm);}
.ag-flicker{animation:flicker 6s linear infinite;}
.ag-nflicker{animation:nflicker 5s linear infinite;}
.ag-holo{background:linear-gradient(135deg,var(--pink),var(--cyan),var(--purple),var(--green));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;background-size:300% 300%;animation:cbg 4s ease-in-out infinite;}
.ag-col-p{color:var(--pink);text-shadow:0 0 10px rgba(255,0,128,.5);}
.ag-col-c{color:var(--cyan);text-shadow:0 0 10px rgba(0,207,255,.5);}
.ag-col-v{color:var(--purple);text-shadow:0 0 10px rgba(157,78,221,.5);}

/* HERO */
.ag-hero{min-height:100vh;padding:100px 60px 60px;position:relative;overflow:hidden;}
.ag-hero-wrap{max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:40px;flex-wrap:wrap;}
.ag-hero-l{flex:1;min-width:340px;max-width:620px;animation:sleft .9s ease both;}
.ag-hero-r{flex:0 0 470px;display:flex;align-items:center;justify-content:center;position:relative;}
.ag-sbadge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border:1px solid rgba(0,229,160,.3);border-radius:20px;background:rgba(0,229,160,.05);font-family:var(--fh);font-size:9px;color:var(--green);letter-spacing:.3em;}
.ag-eline{height:1px;width:40px;background:linear-gradient(90deg,var(--pink),transparent);}
.ag-ebrow{font-family:var(--fm);font-size:11px;color:var(--pink);letter-spacing:.35em;}
.ag-t1{font-family:var(--fh);font-size:clamp(58px,7.5vw,106px);font-weight:900;color:var(--pink);line-height:.9;letter-spacing:.04em;text-shadow:0 0 40px rgba(255,0,128,.7),0 0 80px rgba(255,0,128,.3),-3px 0 rgba(0,207,255,.3),3px 0 rgba(157,78,221,.3);animation:nflicker 7s linear infinite;}
.ag-t2{font-family:var(--fh);font-size:clamp(54px,7vw,98px);font-weight:900;background:linear-gradient(135deg,var(--cyan),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 28px rgba(0,207,255,.5));line-height:.95;}
.ag-tgwrap{border-left:3px solid var(--pink);padding-left:18px;box-shadow:-3px 0 18px rgba(255,0,128,.2);}
.ag-tg1{font-family:var(--fm);font-size:13px;letter-spacing:.4em;color:rgba(220,185,240,.55);}
.ag-tg2{font-family:var(--fm);font-size:10px;letter-spacing:.3em;color:rgba(0,207,255,.38);}
.ag-copy{font-family:var(--fb);font-size:18px;color:rgba(220,185,240,.55);line-height:1.8;max-width:540px;border-left:1px solid rgba(255,0,128,.15);padding-left:18px;}
.ag-stats{display:flex;gap:0;border:1px solid rgba(255,0,128,.14);border-radius:6px;overflow:hidden;background:rgba(255,0,128,.03);}
.ag-si{flex:1;padding:18px 26px;border-right:1px solid rgba(255,0,128,.12);}
.ag-si:last-child{border-right:none;}
.ag-sv{font-family:var(--fh);font-size:28px;font-weight:900;line-height:1;animation:countup .7s cubic-bezier(.4,0,.2,1) both;}
.ag-sl{font-family:var(--fh);font-size:7px;letter-spacing:.2em;color:rgba(220,185,240,.45);margin-top:5px;}
.ag-sv-c{color:var(--cyan);text-shadow:0 0 18px rgba(0,207,255,.5);}
.ag-sv-g{color:var(--green);text-shadow:0 0 18px rgba(0,229,160,.5);}
.ag-sv-p{color:var(--pink);text-shadow:0 0 18px rgba(255,0,128,.5);}

/* RADAR */
.ag-rw{position:relative;}
.ag-ro1{position:absolute;inset:-40px;border-radius:50%;border:1px solid rgba(255,0,128,.06);animation:rrot 28s linear infinite;}
.ag-ro2{position:absolute;inset:-65px;border-radius:50%;border:1px solid rgba(0,207,255,.04);animation:rrot 40s linear infinite reverse;}
.ag-rhalo{position:absolute;inset:-30px;border-radius:50%;background:radial-gradient(circle,rgba(255,0,128,.09) 0%,transparent 70%);animation:epulse 3s ease-in-out infinite;pointer-events:none;}
.ag-radar{position:relative;width:440px;height:440px;animation:rglow 3s ease-in-out infinite;}
.ag-rring{position:absolute;border-radius:50%;border:1px solid;top:50%;left:50%;transform:translate(-50%,-50%);}
.ag-rr1{width:86%;height:86%;border-color:rgba(255,0,128,.12);}
.ag-rr2{width:68%;height:68%;border-color:rgba(255,0,128,.09);}
.ag-rr3{width:50%;height:50%;border-color:rgba(255,0,128,.07);}
.ag-rr4{width:32%;height:32%;border-color:rgba(255,0,128,.05);}
.ag-rr5{width:14%;height:14%;border-color:rgba(255,0,128,.04);}
.ag-rgrid{position:absolute;inset:0;border-radius:50%;background:repeating-conic-gradient(rgba(0,207,255,.04) 0deg 1deg,transparent 1deg 30deg);}
.ag-rarc{position:absolute;border-radius:50%;top:50%;left:50%;transform:translate(-50%,-50%);box-sizing:border-box;}
.ag-ra{width:80%;height:80%;background:conic-gradient(from -90deg,rgba(255,0,128,.85) 0deg,rgba(255,0,128,.85) 313deg,rgba(255,0,128,.12) 313deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 14px),#fff calc(100% - 13px));mask:radial-gradient(farthest-side,transparent calc(100% - 14px),#fff calc(100% - 13px));filter:drop-shadow(0 0 10px rgba(255,0,128,.6));}
.ag-rb{width:63%;height:63%;background:conic-gradient(from -90deg,rgba(0,207,255,.85) 0deg,rgba(0,207,255,.85) 327deg,rgba(0,207,255,.12) 327deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 14px),#fff calc(100% - 13px));mask:radial-gradient(farthest-side,transparent calc(100% - 14px),#fff calc(100% - 13px));filter:drop-shadow(0 0 10px rgba(0,207,255,.6));}
.ag-rc{width:46%;height:46%;background:conic-gradient(from -90deg,rgba(0,229,160,.85) 0deg,rgba(0,229,160,.85) 259deg,rgba(0,229,160,.12) 259deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 14px),#fff calc(100% - 13px));mask:radial-gradient(farthest-side,transparent calc(100% - 14px),#fff calc(100% - 13px));filter:drop-shadow(0 0 10px rgba(0,229,160,.6));}
.ag-rd{width:29%;height:29%;background:conic-gradient(from -90deg,rgba(191,95,255,.85) 0deg,rgba(191,95,255,.85) 338deg,rgba(191,95,255,.12) 338deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 14px),#fff calc(100% - 13px));mask:radial-gradient(farthest-side,transparent calc(100% - 14px),#fff calc(100% - 13px));filter:drop-shadow(0 0 10px rgba(191,95,255,.6));}
.ag-rsc{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,0,128,0) -30deg,rgba(255,0,128,.35) 0deg,rgba(255,0,128,0) 5deg);animation:rrot 4s linear infinite;}
.ag-rs{position:absolute;top:50%;left:50%;width:2.5px;height:48%;background:linear-gradient(to top,rgba(255,0,128,.98),transparent);transform-origin:bottom center;transform:translateX(-50%);animation:rsweep 4s linear infinite;box-shadow:0 0 16px rgba(255,0,128,.9),0 0 32px rgba(255,0,128,.4);}
.ag-rcen{position:absolute;top:50%;left:50%;width:12px;height:12px;border-radius:50%;background:#fff;transform:translate(-50%,-50%);box-shadow:0 0 20px var(--cyan),0 0 40px rgba(0,207,255,.6);}
.ag-blip{position:absolute;width:8px;height:8px;border-radius:50%;transform:translate(-50%,-50%);animation:pgrow 2s ease-in-out infinite;}
.ag-blip::after{content:'';position:absolute;inset:-4px;border-radius:50%;border:1px solid currentColor;opacity:.4;animation:pgrow 2s ease-in-out infinite;}
.ag-b1{top:35%;left:64%;background:var(--green);color:var(--green);box-shadow:0 0 10px var(--green);animation-delay:.2s;}
.ag-b2{top:62%;left:70%;background:var(--pink);color:var(--pink);box-shadow:0 0 10px var(--pink);animation-delay:.8s;}
.ag-b3{top:72%;left:35%;background:var(--amber);color:var(--amber);box-shadow:0 0 10px var(--amber);animation-delay:.5s;}
.ag-b4{top:28%;left:30%;background:var(--cyan);color:var(--cyan);box-shadow:0 0 10px var(--cyan);animation-delay:1.1s;}
.ag-rlbl{position:absolute;font-family:var(--fh);font-size:8px;white-space:nowrap;background:rgba(3,5,13,.9);padding:5px 10px;border-radius:3px;letter-spacing:.12em;transform:translate(-50%,-50%);}
.ag-rl1{top:14%;left:55%;color:var(--cyan);border:1px solid rgba(0,207,255,.3);text-shadow:0 0 8px rgba(0,207,255,.7);box-shadow:0 0 10px rgba(0,207,255,.2);}
.ag-rl2{top:50%;left:92%;color:var(--green);border:1px solid rgba(0,229,160,.3);text-shadow:0 0 8px rgba(0,229,160,.7);box-shadow:0 0 10px rgba(0,229,160,.2);}
.ag-rl3{top:86%;left:52%;color:var(--pink);border:1px solid rgba(255,0,128,.3);text-shadow:0 0 8px rgba(255,0,128,.7);box-shadow:0 0 10px rgba(255,0,128,.2);}
.ag-rl4{top:50%;left:9%;color:#bf5fff;border:1px solid rgba(191,95,255,.3);text-shadow:0 0 8px rgba(191,95,255,.7);box-shadow:0 0 10px rgba(191,95,255,.2);}
.ag-rcore{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) translateY(14px);font-family:var(--fh);font-size:8px;color:var(--cyan);letter-spacing:.3em;opacity:.65;text-shadow:0 0 8px rgba(0,207,255,.5);pointer-events:none;}

/* TICKER */
.ag-tkwrap{overflow:hidden;white-space:nowrap;border-top:1px solid rgba(255,0,128,.12);border-bottom:1px solid rgba(255,0,128,.08);background:rgba(3,5,13,.9);}
.ag-tkrow{padding:7px 0;}
.ag-tkrow2{padding:7px 0;background:rgba(0,207,255,.015);}
.ag-tki{display:inline-block;animation:ticker 30s linear infinite;font-family:var(--fm);font-size:11px;color:var(--pink);opacity:.85;letter-spacing:.05em;}
.ag-tki2{display:inline-block;animation:ticker2 38s linear infinite;font-family:var(--fm);font-size:11px;color:var(--cyan);opacity:.7;letter-spacing:.05em;}

/* SECTIONS */
.ag-sec{padding:100px 60px;max-width:1200px;margin:0 auto;position:relative;}
.ag-kicker{font-family:var(--fm);font-size:10px;letter-spacing:.5em;}
.ag-stitle{font-family:var(--fh);font-size:38px;font-weight:900;letter-spacing:.05em;animation:nflicker 8s linear infinite;}

/* FLOW */
.ag-fgrid{display:flex;align-items:stretch;max-width:1080px;margin:0 auto;position:relative;gap:0;}
.ag-fline{position:absolute;top:36px;left:12%;right:12%;height:1px;background:linear-gradient(90deg,transparent,var(--cyan),var(--purple),var(--green),transparent);opacity:.4;}
.ag-fbeam{position:absolute;top:0;left:0;width:50px;height:100%;background:linear-gradient(90deg,transparent,#fff,transparent);animation:pbeam 3s linear infinite;}
.ag-fi{flex:1;text-align:center;padding:0 22px;position:relative;z-index:1;animation:sup .5s ease both;}
.ag-ficon{width:70px;height:70px;border-radius:50%;margin:0 auto 22px;display:flex;align-items:center;justify-content:center;font-size:26px;transition:all .3s;}
.ag-ficon:hover{transform:scale(1.08);}
.ag-fstep{font-family:var(--fh);font-size:9px;letter-spacing:.25em;}
.ag-ftitle{font-family:var(--fh);font-size:12px;font-weight:700;letter-spacing:.1em;color:#fff;}
.ag-fdesc{font-family:var(--fb);font-size:13px;color:rgba(220,185,240,.5);line-height:1.7;}

/* CAP CARDS */
.ag-cgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px;max-width:1080px;margin:0 auto;}
.ag-card{padding:36px;position:relative;background:linear-gradient(135deg,rgba(255,0,128,.055),rgba(0,207,255,.025));backdrop-filter:blur(32px);border:1px solid rgba(255,0,128,.16);border-radius:6px;overflow:hidden;cursor:default;transition:all .4s cubic-bezier(.4,0,.2,1);animation:bholo 7s linear infinite;}
.ag-card::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at top left,var(--ag-acc,#ff0080)08,transparent 60%);pointer-events:none;z-index:0;}
.ag-card:hover{transform:translateY(-8px) scale(1.01);}
.ag-cc{position:absolute;width:18px;height:18px;border-style:solid;opacity:.7;z-index:2;animation:cspark 3s ease-in-out infinite;}
.ag-cc-tl{top:0;left:0;border-width:2px 0 0 2px;border-color:var(--ag-acc,#ff0080);}
.ag-cc-tr{top:0;right:0;border-width:2px 2px 0 0;border-color:var(--cyan);animation-delay:.75s;}
.ag-cc-bl{bottom:0;left:0;border-width:0 0 2px 2px;border-color:var(--cyan);animation-delay:1.5s;}
.ag-cc-br{bottom:0;right:0;border-width:0 2px 2px 0;border-color:var(--ag-acc,#ff0080);animation-delay:2.25s;}
.ag-cicon{width:54px;height:54px;border-radius:10px;margin-bottom:22px;display:flex;align-items:center;justify-content:center;font-size:22px;position:relative;z-index:1;transition:all .3s;}
.ag-cicon:hover{transform:scale(1.12);}
.ag-ctitle{font-family:var(--fh);font-size:10px;letter-spacing:.2em;margin-bottom:16px;position:relative;z-index:1;}
.ag-cdesc{font-family:var(--fb);font-size:14px;color:rgba(220,185,240,.55);line-height:1.7;position:relative;z-index:1;}
.ag-cexplore{font-family:var(--fh);font-size:8px;letter-spacing:.18em;margin-top:18px;opacity:.5;transition:opacity .3s;position:relative;z-index:1;}
.ag-card:hover .ag-cexplore{opacity:1;}

/* PILLARS */
.ag-pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px;max-width:1080px;margin:0 auto;}
.ag-pc{padding:32px;position:relative;background:linear-gradient(135deg,rgba(255,0,128,.04),rgba(0,207,255,.02));backdrop-filter:blur(24px);border:1px solid rgba(0,207,255,.15);border-radius:6px;transition:all .3s;}
.ag-pc:hover{border-color:rgba(0,207,255,.4);box-shadow:0 0 30px rgba(0,207,255,.12);transform:translateY(-4px);}
.ag-pcc{position:absolute;width:16px;height:16px;border-style:solid;opacity:.6;}
.ag-pcc-tl{top:0;left:0;border-width:2px 0 0 2px;border-color:var(--cyan);}
.ag-pcc-tr{top:0;right:0;border-width:2px 2px 0 0;border-color:var(--pink);}
.ag-pcc-bl{bottom:0;left:0;border-width:0 0 2px 2px;border-color:var(--pink);}
.ag-pcc-br{bottom:0;right:0;border-width:0 2px 2px 0;border-color:var(--cyan);}
.ag-ptitle{font-family:var(--fh);font-size:10px;letter-spacing:.2em;margin-bottom:20px;}
.ag-pdot{width:5px;height:5px;border-radius:50%;flex-shrink:0;}
.ag-pitem{font-family:var(--fm);font-size:11px;color:rgba(220,185,240,.55);}

/* CTA */
.ag-cta{padding:110px 60px;text-align:center;position:relative;background:linear-gradient(180deg,transparent,rgba(255,0,128,.04),transparent);border-top:1px solid rgba(255,0,128,.1);border-bottom:1px solid rgba(255,0,128,.1);overflow:hidden;}
.ag-cta-amb{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:700px;height:350px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,0,128,.07) 0%,transparent 70%);animation:epulse 4s ease-in-out infinite;pointer-events:none;}
.ag-cta-t1{font-family:var(--fh);font-size:clamp(32px,4.5vw,58px);font-weight:900;letter-spacing:.05em;}
.ag-cta-t2{font-family:var(--fh);font-size:clamp(32px,4.5vw,58px);font-weight:900;letter-spacing:.05em;animation:nflicker 5s linear infinite;}
.ag-cta-copy{font-family:var(--fb);font-size:17px;color:rgba(220,185,240,.55);max-width:500px;margin:0 auto;line-height:1.8;}

/* FOOTER */
.ag-foot{padding:44px 60px;border-top:1px solid rgba(255,0,128,.1);background:rgba(2,3,8,.96);backdrop-filter:blur(20px);}
.ag-foot-in{max-width:1200px;margin:0 auto;}
.ag-foot-brand{font-family:var(--fh);font-size:12px;color:var(--pink);font-weight:700;letter-spacing:.15em;text-shadow:0 0 10px rgba(255,0,128,.4);}
.ag-foot-tag{font-family:var(--fm);font-size:10px;color:rgba(220,185,240,.35);}
.ag-foot-link{font-family:var(--fm);font-size:10px;color:rgba(220,185,240,.4);cursor:pointer;transition:color .2s;}
.ag-foot-link:hover{color:var(--cyan);}
.ag-foot-state{font-family:var(--fh);font-size:8px;color:rgba(220,185,240,.4);letter-spacing:.15em;}

/* AUTH */
.ag-auth{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:40px;position:relative;z-index:2;}
.ag-vign{position:fixed;inset:0;background:radial-gradient(ellipse at center,transparent 28%,rgba(2,4,10,.75) 100%);pointer-events:none;z-index:1;}
.ag-acard{width:100%;max-width:440px;position:relative;z-index:3;animation:sup .7s ease both;}
.ag-acard-w{max-width:480px;}
.ag-alogo{position:relative;width:80px;height:80px;margin:0 auto 18px;}
.ag-alogor{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,var(--pink),var(--cyan),var(--purple),var(--green),var(--pink));animation:rot 4s linear infinite;}
.ag-alogoi{position:absolute;inset:3px;border-radius:50%;background:var(--bg);display:flex;align-items:center;justify-content:center;font-family:var(--fh);font-size:28px;color:var(--pink);text-shadow:0 0 20px rgba(255,0,128,.7);animation:flicker 6s linear infinite;}
.ag-spin{position:relative;}
.ag-sr{position:absolute;border-radius:50%;border:2px solid transparent;box-sizing:border-box;}
.ag-sr1{inset:0;border-top-color:var(--pink);border-right-color:var(--cyan);animation:rot .8s linear infinite;}
.ag-sr2{inset:8px;border-bottom-color:var(--purple);border-left-color:var(--green);animation:rot 1.3s linear infinite reverse;}
.ag-sr3{inset:16px;border-top-color:var(--amber);animation:rot 2s linear infinite;}
.ag-score{position:absolute;inset:22px;border-radius:50%;background:rgba(255,0,128,.1);display:flex;align-items:center;justify-content:center;font-family:var(--fh);font-size:14px;color:var(--pink);}
.ag-dtitle{font-family:var(--fh);font-size:14px;color:var(--pink);animation:pulse .6s ease-in-out infinite;text-shadow:0 0 20px rgba(255,0,128,.7);}
.ag-dsub{font-family:var(--fm);font-size:10px;color:rgba(220,185,240,.45);}
.ag-dsub2{font-family:var(--fm);font-size:9px;color:rgba(220,185,240,.35);}
.ag-lbar{height:2px;border-radius:2px;overflow:hidden;background:rgba(255,0,128,.08);}
.ag-lfill{height:100%;background:linear-gradient(90deg,transparent,var(--pink),var(--cyan),var(--purple),transparent);background-size:200% 100%;animation:dstream .7s linear infinite;width:100%;}
.ag-terms{background:rgba(255,0,128,.04);border:1px solid rgba(255,0,128,.15);border-left:2px solid rgba(255,0,128,.4);border-radius:4px;padding:14px 18px;}
.ag-ttitle{font-family:var(--fh);font-size:8px;letter-spacing:.2em;color:var(--pink);margin-bottom:6px;}
.ag-tbody{font-family:var(--fm);font-size:10px;color:rgba(220,185,240,.45);line-height:1.7;}
.ag-aswitch{font-family:var(--fm);font-size:11px;color:rgba(220,185,240,.45);text-align:center;}
.ag-alink{color:var(--pink);cursor:pointer;transition:all .2s;}
.ag-alink:hover{text-shadow:0 0 12px rgba(255,0,128,.7);}
.ag-back{font-family:var(--fm);font-size:10px;color:rgba(0,207,255,.45);cursor:pointer;letter-spacing:.1em;transition:all .2s;}
.ag-back:hover{color:var(--cyan);}
.ag-nodes{display:flex;justify-content:center;gap:8px;}
.ag-nd{width:8px;height:8px;border-radius:50%;}
.ag-nd1{background:var(--pink);box-shadow:0 0 8px var(--pink);animation:pulse .5s infinite 0s;}
.ag-nd2{background:var(--purple);box-shadow:0 0 8px var(--purple);animation:pulse .5s infinite .15s;}
.ag-nd3{background:var(--cyan);box-shadow:0 0 8px var(--cyan);animation:pulse .5s infinite .3s;}
.ag-nd4{background:var(--green);box-shadow:0 0 8px var(--green);animation:pulse .5s infinite .45s;}
.ag-err{font-family:var(--fm);font-size:11px;color:var(--red);padding:10px 14px;background:rgba(255,51,85,.06);border:1px solid rgba(255,51,85,.25);border-left:3px solid var(--red);border-radius:0 4px 4px 0;}

/* SIDEBAR */
.ag-sb{width:210px;min-width:210px;min-height:100vh;border-right:1px solid rgba(255,0,128,.12);background:rgba(2,3,8,.94);backdrop-filter:blur(40px) saturate(180%);display:flex;flex-direction:column;position:sticky;top:0;z-index:100;flex-shrink:0;overflow:hidden;box-shadow:4px 0 30px rgba(255,0,128,.06),8px 0 60px rgba(0,0,0,.5);}
.ag-sb::after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,207,255,.008) 3px,rgba(0,207,255,.008) 4px);animation:hlines 4s linear infinite;pointer-events:none;z-index:0;}
.ag-sbl{padding:18px 18px 14px;border-bottom:1px solid rgba(255,0,128,.12);}
.ag-sbst{padding:10px 18px;border-bottom:1px solid rgba(255,0,128,.08);background:rgba(0,229,160,.03);}
.ag-ni{font-family:var(--fh);font-size:9px;letter-spacing:.18em;color:rgba(220,185,240,.42);padding:12px 18px;cursor:pointer;transition:all .25s cubic-bezier(.4,0,.2,1);border-left:2px solid transparent;display:flex;align-items:center;gap:12px;text-transform:uppercase;position:relative;}
.ag-ni::after{content:'';position:absolute;left:0;top:0;bottom:0;width:0;background:linear-gradient(90deg,rgba(255,0,128,.1),transparent);transition:width .25s;}
.ag-ni:hover{color:rgba(255,0,128,.7);border-left-color:rgba(255,0,128,.5);}
.ag-ni:hover::after{width:100%;}
.ag-ni-a{color:var(--pink);border-left-color:var(--pink);background:linear-gradient(90deg,rgba(255,0,128,.09),transparent);text-shadow:0 0 12px rgba(255,0,128,.8);}
.ag-ni-a::after{width:100%;}
.ag-niico{font-size:15px;transition:all .3s;}
.ag-ni-a .ag-niico{text-shadow:0 0 14px rgba(255,0,128,.9);}
.ag-sbscore{padding:12px 18px;text-align:center;border-top:1px solid rgba(255,0,128,.1);background:rgba(255,0,128,.03);}
.ag-scorelbl{font-family:var(--fh);font-size:7px;letter-spacing:.22em;color:rgba(220,185,240,.35);}
.ag-scorenum{font-family:var(--fh);font-size:32px;font-weight:900;}
.ag-sbop{padding:10px 18px 6px;border-top:1px solid rgba(255,0,128,.08);}
.ag-oplbl{font-family:var(--fh);font-size:7px;letter-spacing:.22em;color:rgba(220,185,240,.28);}
.ag-opname{font-family:var(--fm);font-size:11px;color:var(--cyan);letter-spacing:.05em;text-shadow:0 0 10px rgba(0,207,255,.35);}
.ag-termbtn{font-family:var(--fh);font-size:8px;letter-spacing:.15em;color:#fff;padding:9px;border-radius:3px;cursor:pointer;text-align:center;border:1px solid rgba(255,0,128,.4);background:rgba(255,0,128,.08);box-shadow:0 0 15px rgba(255,0,128,.18);animation:gpink 2.5s ease-in-out infinite;text-shadow:0 0 10px rgba(255,0,128,.55);transition:all .25s;}
.ag-termbtn:hover{background:rgba(255,0,128,.16);}

/* TOPBAR */
.ag-tb{padding:13px 28px;border-bottom:1px solid rgba(255,0,128,.1);background:rgba(2,3,8,.92);backdrop-filter:blur(40px);position:sticky;top:0;z-index:10;box-shadow:0 2px 20px rgba(0,0,0,.4),0 1px 0 rgba(255,0,128,.14);}
.ag-tbbar{width:3px;height:18px;background:linear-gradient(180deg,var(--pink),var(--cyan));border-radius:2px;box-shadow:0 0 8px var(--pink);}
.ag-tbpage{font-family:var(--fh);font-size:11px;letter-spacing:.3em;color:var(--pink);text-shadow:0 0 12px rgba(255,0,128,.55);}
.ag-tbmsg{display:flex;align-items:center;gap:8px;padding:5px 12px;border:1px solid rgba(0,207,255,.2);border-radius:3px;background:rgba(0,207,255,.04);}
.ag-tbmsgt{font-family:var(--fm);font-size:11px;color:var(--cyan);}
.ag-svc{display:flex;align-items:center;gap:6px;padding:5px 10px;border-radius:3px;transition:all .3s;}

/* DASHBOARD */
.ag-dash{padding:36px 44px;animation:sleft .5s ease;}
.ag-dash-t{font-family:var(--fh);font-size:28px;font-weight:900;letter-spacing:.06em;text-shadow:0 0 20px rgba(255,0,128,.18);}
.ag-dash-s{font-family:var(--fm);font-size:10px;color:rgba(220,185,240,.45);}
.ag-pipe{padding:18px 24px;}
.ag-pnode{flex:1;text-align:center;padding:8px 10px;border-radius:6px;transition:all .3s;}
.ag-pnode-a{background:rgba(255,0,128,.09);border:1px solid rgba(255,0,128,.3);}
.ag-pnode-d{background:rgba(0,229,160,.04);border:1px solid transparent;}
.ag-pnode-p{background:transparent;border:1px solid transparent;}
.ag-pdot-wrap{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--fh);font-size:12px;margin:0 auto 8px;}
.ag-pdot-a{background:rgba(255,0,128,.18);border:2px solid var(--pink);color:var(--pink);box-shadow:0 0 16px rgba(255,0,128,.5);animation:nring 1.5s ease-in-out infinite,pulse 1.5s ease-in-out infinite;}
.ag-pdot-d{background:rgba(0,229,160,.1);border:2px solid var(--green);color:var(--green);box-shadow:0 0 10px rgba(0,229,160,.3);}
.ag-pdot-p{background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.1);color:rgba(220,185,240,.3);}
.ag-plbl{font-family:var(--fh);font-size:7px;letter-spacing:.1em;text-align:center;}
.ag-psub{font-family:var(--fm);font-size:7px;color:rgba(220,185,240,.38);text-align:center;}
.ag-pconn{width:28px;height:2px;flex-shrink:0;border-radius:1px;overflow:hidden;position:relative;}
.ag-pconn-f{height:100%;border-radius:1px;}
.ag-pconn-b{position:absolute;top:0;left:0;width:40px;height:100%;background:linear-gradient(90deg,transparent,#fff,transparent);animation:pbeam 3s linear infinite;}
.ag-stile{padding:18px 22px;position:relative;overflow:hidden;border-radius:6px;transition:all .3s;}
.ag-stile:hover{transform:translateY(-2px);}
.ag-stile-ico{font-family:var(--fh);font-size:16px;}
.ag-stile-val{font-family:var(--fh);font-size:26px;font-weight:900;animation:pulse 3s ease-in-out infinite;}
.ag-stile-bg{position:absolute;inset:0;pointer-events:none;}
.ag-mrow{padding:11px 0;border-bottom:1px solid rgba(0,245,255,.05);transition:all .2s;}
.ag-mrow:hover{background:rgba(255,0,128,.025);padding-left:4px;}
.ag-mname{font-family:var(--fh);font-size:10px;color:#fff;letter-spacing:.05em;width:95px;}
.ag-mscore{font-family:var(--fh);font-size:13px;font-weight:900;width:38px;text-align:right;}
.ag-mlat{font-family:var(--fm);font-size:10px;color:rgba(220,185,240,.42);width:56px;text-align:right;}
.ag-bwrap{flex:1;height:5px;border-radius:3px;overflow:hidden;background:rgba(255,255,255,.05);}
.ag-bfill{height:100%;border-radius:3px;transition:width 1.2s cubic-bezier(.4,0,.2,1);position:relative;overflow:hidden;}
.ag-bfill::after{content:'';position:absolute;top:0;right:0;width:30px;height:100%;background:rgba(255,255,255,.6);filter:blur(4px);animation:pbeam 2.5s ease-in-out infinite;}
.ag-rwrap{padding:24px;}
.ag-drad{position:relative;width:300px;height:300px;animation:rglow 3s ease-in-out infinite;}
.ag-drr{position:absolute;border-radius:50%;border:1px solid;top:50%;left:50%;transform:translate(-50%,-50%);}
.ag-dsw{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,0,128,0) -30deg,rgba(255,0,128,.35) 0deg,rgba(255,0,128,0) 5deg);animation:rrot 4s linear infinite;}
.ag-dswl{position:absolute;top:50%;left:50%;width:2.5px;height:48%;background:linear-gradient(to top,rgba(255,0,128,.98),transparent);transform-origin:bottom center;transform:translateX(-50%);animation:rsweep 4s linear infinite;box-shadow:0 0 16px rgba(255,0,128,.9);}
.ag-dcen{position:absolute;top:50%;left:50%;width:10px;height:10px;border-radius:50%;background:#fff;transform:translate(-50%,-50%);box-shadow:0 0 16px var(--cyan),0 0 32px rgba(0,207,255,.5);}
.ag-empty-i{font-family:var(--fh);font-size:44px;color:rgba(220,185,240,.12);animation:pulse 3s infinite;}
.ag-empty-t{font-family:var(--fm);font-size:12px;color:rgba(220,185,240,.28);}

/* INTERROGATION */
.ag-intpg{animation:sleft .5s ease;}
.ag-tdr{width:10px;height:10px;border-radius:50%;}
.ag-tdr-r{background:#ff3355;box-shadow:0 0 5px #ff3355;}
.ag-tdr-a{background:var(--amber);box-shadow:0 0 5px var(--amber);}
.ag-tdr-g{background:var(--green);box-shadow:0 0 5px var(--green);}
.ag-live{font-family:var(--fh);font-size:8px;color:var(--cyan);letter-spacing:.15em;padding:3px 8px;border-radius:2px;background:rgba(0,207,255,.08);border:1px solid rgba(0,207,255,.3);text-shadow:0 0 8px var(--cyan);animation:pulse .8s infinite;}
.ag-sbox{padding:18px;min-height:140px;background:rgba(0,0,0,.5);border-radius:4px;border:1px solid rgba(0,207,255,.08);box-shadow:inset 0 0 30px rgba(0,207,255,.03);}
.ag-stxt{font-family:var(--fm);font-size:13px;color:#e0ffe0;white-space:pre-wrap;line-height:1.75;}
.ag-cur{font-family:var(--fm);font-size:14px;color:var(--cyan);display:inline;text-shadow:0 0 10px var(--cyan);animation:blink .7s step-end infinite;}
.ag-seg{padding:14px 18px;border-radius:0 6px 6px 0;margin-bottom:10px;background:rgba(255,255,255,.02);animation:srev .4s ease both;transition:all .3s;}
.ag-seg:hover{background:rgba(255,255,255,.04);}
.ag-segico{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--fh);font-size:10px;flex-shrink:0;}
.ag-seglbl{font-family:var(--fh);font-size:8px;letter-spacing:.15em;}
.ag-segconf{font-family:var(--fm);font-size:10px;color:rgba(220,185,240,.5);}
.ag-segtxt{font-family:var(--fm);font-size:13px;color:#fff;line-height:1.65;}
.ag-segr{font-family:var(--fm);font-size:11px;color:var(--amber);font-style:italic;}
.ag-meter{padding:20px 14px;width:125px;flex-shrink:0;position:sticky;top:0;height:550px;overflow-y:auto;}
.ag-mbwrap{position:relative;width:36px;height:360px;background:rgba(255,255,255,.04);border:1px solid rgba(255,0,128,.15);border-radius:4px;overflow:hidden;margin:0 auto;}
.ag-mbfill{position:absolute;bottom:0;width:100%;border-radius:3px;transition:height 1.2s cubic-bezier(.4,0,.2,1);}
.ag-mtick{position:absolute;left:0;right:0;height:1px;background:rgba(255,255,255,.06);}
.ag-mscore{font-family:var(--fh);font-size:24px;font-weight:900;white-space:nowrap;}
.ag-mrisk{font-family:var(--fh);font-size:7px;letter-spacing:.12em;}
.ag-msegs{font-family:var(--fm);font-size:10px;color:rgba(220,185,240,.45);}

/* VAULT */
.ag-vltpg{animation:sleft .5s ease;}
.ag-vtbl{overflow:hidden;border-radius:6px;}
.ag-vth{padding:10px 18px;border-bottom:1px solid rgba(255,0,128,.15);background:rgba(255,0,128,.03);}
.ag-vcol{font-family:var(--fh);font-size:7px;letter-spacing:.2em;color:rgba(220,185,240,.38);}
.ag-vrow{padding:12px 18px;border-bottom:1px solid rgba(0,245,255,.05);cursor:default;transition:all .2s;}
.ag-vrow:hover{background:rgba(255,0,128,.04);padding-left:22px;}
.ag-vid{font-family:var(--fm);font-size:10px;color:var(--cyan);text-shadow:0 0 6px rgba(0,207,255,.3);overflow:hidden;white-space:nowrap;text-overflow:ellipsis;}
.ag-vq{font-family:var(--fm);font-size:11px;color:rgba(220,185,240,.75);overflow:hidden;white-space:nowrap;text-overflow:ellipsis;}
.ag-vscore{font-family:var(--fh);font-size:14px;font-weight:900;}
.ag-rbadge{font-family:var(--fh);font-size:8px;padding:4px 10px;border-radius:2px;letter-spacing:.1em;text-align:center;}

/* ENGINE */
.ag-engpg{animation:sleft .5s ease;}
.ag-engrid{display:grid;grid-template-columns:1fr 1fr;gap:24px;}
.ag-pan{padding:28px;overflow:hidden;}
.ag-slbl{font-family:var(--fm);font-size:11px;color:rgba(220,185,240,.5);}
.ag-sval{font-family:var(--fh);font-size:16px;font-weight:900;}
.ag-tog{display:flex;align-items:center;padding:8px 0;border-bottom:1px solid rgba(0,245,255,.06);}
.ag-toglbl{font-family:var(--fm);font-size:11px;color:rgba(220,185,240,.5);text-transform:uppercase;flex:1;}
.ag-togsw{position:relative;width:42px;height:20px;border-radius:10px;cursor:pointer;transition:all .3s;flex-shrink:0;}
.ag-togknob{position:absolute;top:3px;width:14px;height:14px;border-radius:50%;transition:left .3s cubic-bezier(.4,0,.2,1);}
.ag-apih{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
.ag-apilbl{font-family:var(--fh);font-size:8px;letter-spacing:.2em;}
.ag-connbadge{display:flex;align-items:center;gap:5px;}
.ag-connlbl{font-family:var(--fh);font-size:7px;letter-spacing:.12em;}
.ag-sysrow{display:flex;justify-content:space-between;align-items:center;padding:11px 0;border-bottom:1px solid rgba(0,245,255,.06);}
.ag-sysn{font-family:var(--fm);font-size:11px;color:rgba(220,185,240,.5);}
.ag-sysv{font-family:var(--fh);font-size:9px;letter-spacing:.1em;}

/* TERMINATE */
.ag-twrap{display:flex;align-items:center;justify-content:center;height:85vh;}
.ag-tpg{padding:64px;max-width:600px;}
.ag-tico{font-family:var(--fh);font-size:72px;color:var(--pink);text-shadow:0 0 30px var(--pink),0 0 60px rgba(255,0,128,.5);animation:pulse 1.2s infinite;}
.ag-tr1{position:absolute;inset:-20px;border-radius:50%;border:1px solid rgba(255,0,128,.15);animation:pulse 2s infinite;}
.ag-tr2{position:absolute;inset:-40px;border-radius:50%;border:1px solid rgba(255,0,128,.08);animation:pulse 2s infinite .5s;}
.ag-ttl{font-family:var(--fh);font-size:26px;font-weight:900;letter-spacing:.06em;color:var(--pink);text-shadow:0 0 20px var(--pink),0 0 40px rgba(255,0,128,.4);animation:nflicker 4s linear infinite;}
.ag-tdiv{height:1px;width:80%;background:linear-gradient(90deg,transparent,var(--pink),transparent);box-shadow:0 0 8px var(--pink);}
.ag-tcopy{font-family:var(--fm);font-size:13px;color:rgba(220,185,240,.52);text-align:center;max-width:420px;line-height:1.8;white-space:pre-line;}
.ag-twico{font-size:18px;}
.ag-twmsg{font-family:var(--fh);font-size:7px;letter-spacing:.1em;text-align:center;}
.ag-tstat{font-family:var(--fh);font-size:13px;color:var(--pink);animation:pulse .8s infinite;text-shadow:0 0 15px rgba(255,0,128,.7);}
"""

# ── Appended fixes ────────────────────────────────────────────────────────────
_FIX_CSS = """
/* Fix: small button variant — no clip-path so text never wraps */
.ag-btn-sm {
  font-family: var(--fh);
  font-size: 10px;
  letter-spacing: .18em;
  padding: 10px 20px;
  background: linear-gradient(90deg, rgba(255,0,128,.12), rgba(0,207,255,.08));
  border: 1px solid var(--pink);
  color: #fff;
  cursor: pointer;
  white-space: nowrap;
  border-radius: 3px;
  animation: gpink 2s ease-in-out infinite;
  text-shadow: 0 0 10px rgba(255,0,128,.7);
  transition: all .25s;
  flex-shrink: 0;
}
.ag-btn-sm:hover {
  background: linear-gradient(90deg, rgba(255,0,128,.24), rgba(0,207,255,.18));
  transform: translateY(-1px);
}

/* Fix: shell content area takes full available width */
.ag-sb { flex-shrink: 0; }

/* Fix: vault table header alignment */
.ag-vth {
  padding: 10px 18px;
  border-bottom: 1px solid rgba(255,0,128,.15);
  background: rgba(255,0,128,.03);
  display: flex;
  align-items: center;
  gap: 16px;
}
.ag-vrow {
  padding: 12px 18px;
  border-bottom: 1px solid rgba(0,245,255,.05);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all .2s;
}
.ag-vrow:hover { background: rgba(255,0,128,.04); }

/* Fix: segment confidence display — inline with status */
.ag-segconf {
  font-family: var(--fm);
  font-size: 11px;
  color: rgba(220,185,240,.6);
  font-weight: 600;
}

/* Fix: dashboard/engine/interrogation full width */
.ag-dash, .ag-engpg, .ag-intpg, .ag-vltpg { width: 100%; min-width: 0; }

/* Fix: page content wrapper */
.ag-page-content { width: 100%; min-width: 0; overflow-x: hidden; }
"""

GLOBAL_CSS = GLOBAL_CSS + _FIX_CSS

_WEB_CSS = """
/* Web verification panel */
.ag-web-panel { padding:18px 22px; }
.ag-web-title { font-family:var(--fh);font-size:9px;letter-spacing:.25em;color:var(--cyan);text-transform:uppercase;margin-bottom:14px;text-shadow:0 0 8px rgba(0,207,255,.5); }
.ag-web-summary { font-family:var(--fm);font-size:11px;color:rgba(220,185,240,.6);line-height:1.6;margin-bottom:14px;padding:10px 14px;background:rgba(0,207,255,.04);border-left:2px solid rgba(0,207,255,.3);border-radius:0 4px 4px 0; }
.ag-web-score-row { display:flex;align-items:center;gap:12px;margin-bottom:14px; }
.ag-web-score-lbl { font-family:var(--fh);font-size:8px;letter-spacing:.2em;color:rgba(220,185,240,.45); }
.ag-web-score-val { font-family:var(--fh);font-size:18px;font-weight:900;color:var(--cyan);text-shadow:0 0 12px rgba(0,207,255,.5); }
.ag-web-bar { flex:1;height:4px;border-radius:2px;overflow:hidden;background:rgba(255,255,255,.05); }
.ag-web-bar-fill { height:100%;border-radius:2px;background:linear-gradient(90deg,var(--cyan),var(--green));transition:width 1s ease;box-shadow:0 0 8px rgba(0,207,255,.4); }
.ag-fact-row { display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid rgba(0,245,255,.05); }
.ag-fact-ico { font-size:12px;flex-shrink:0;margin-top:1px; }
.ag-fact-txt { font-family:var(--fm);font-size:11px;color:rgba(220,185,240,.7);line-height:1.5;flex:1; }
.ag-source-count { font-family:var(--fh);font-size:8px;color:rgba(220,185,240,.4);letter-spacing:.15em;margin-top:10px; }
"""
GLOBAL_CSS = GLOBAL_CSS + _WEB_CSS

_FACT_CSS = """
/* Fact check errors panel */
.ag-fc-panel { padding:18px 22px; }
.ag-fc-title { font-family:var(--fh);font-size:9px;letter-spacing:.25em;color:var(--red);text-transform:uppercase;margin-bottom:14px;text-shadow:0 0 8px rgba(255,51,85,.5); }
.ag-fc-checker { font-family:var(--fm);font-size:10px;color:rgba(220,185,240,.4);margin-bottom:12px; }
.ag-fc-error { padding:12px 14px;margin-bottom:10px;border-left:3px solid var(--red);background:rgba(255,51,85,.06);border-radius:0 6px 6px 0; }
.ag-fc-claim { font-family:var(--fm);font-size:11px;color:rgba(255,255,255,.7);margin-bottom:6px; }
.ag-fc-claim-lbl { font-family:var(--fh);font-size:7px;letter-spacing:.2em;color:var(--red);margin-bottom:3px; }
.ag-fc-correct { font-family:var(--fm);font-size:11px;color:var(--green);margin-bottom:4px; }
.ag-fc-correct-lbl { font-family:var(--fh);font-size:7px;letter-spacing:.2em;color:var(--green);margin-bottom:3px; }
.ag-fc-conf { font-family:var(--fh);font-size:8px;color:rgba(220,185,240,.4);letter-spacing:.12em; }
.ag-fc-penalty { font-family:var(--fh);font-size:9px;color:var(--red);letter-spacing:.15em;text-shadow:0 0 8px rgba(255,51,85,.4); }
.ag-fc-ok { font-family:var(--fm);font-size:11px;color:var(--green);padding:10px 14px;background:rgba(0,229,160,.05);border-left:3px solid var(--green);border-radius:0 6px 6px 0;text-shadow:0 0 6px rgba(0,229,160,.3); }
"""
GLOBAL_CSS = GLOBAL_CSS + _FACT_CSS
