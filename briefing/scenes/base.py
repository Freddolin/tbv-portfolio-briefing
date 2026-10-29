"""Shared building blocks for all scenes: CSS, element helpers and a small timeline-writer.
Every scene is self-contained: it brings its own background, chapter label and corner logo,
so scenes can be reordered or rebuilt without side effects."""
import html as _h, json
from ..config import COLORS, reading_time

E = lambda s: _h.escape(str(s), quote=False)
def T(s):
    """Escape text but keep explicit line breaks written as <br> or '\\n'."""
    return E(s).replace('&lt;br&gt;', '<br>').replace('\n', '<br>')

CSS = r"""
@font-face{font-family:Archivo;font-weight:400;src:url(node_modules/@fontsource/archivo/files/archivo-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:Archivo;font-weight:500;src:url(node_modules/@fontsource/archivo/files/archivo-latin-500-normal.woff2) format('woff2')}
@font-face{font-family:Archivo;font-weight:600;src:url(node_modules/@fontsource/archivo/files/archivo-latin-600-normal.woff2) format('woff2')}
:root{__VARS__}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#000;width:1920px;height:1080px;overflow:hidden}
#stage{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:Archivo,sans-serif;font-weight:500;color:var(--lg);-webkit-font-smoothing:antialiased;background:var(--dark)}
#stage *{position:absolute}
#stage .st,#stage .st *{position:static}
svg{overflow:visible}
.h{visibility:hidden;opacity:0}
.sc{left:0;top:0;width:1920px;height:1080px}
.sc.dk{background:var(--dark)} .sc.wm{background:var(--warm)}
.cap{font-weight:600;font-size:22px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap}
.dk .cap{color:#cfcbc6} .wm .cap{color:var(--mid)}
.chap{left:110px;top:64px}
#stage .chap b{position:static;font-weight:600;color:var(--orange);margin-right:18px}
#stage .chap span{position:static}
.rule{left:110px;right:110px;top:108px;height:1px}
.dk .rule{background:rgba(245,245,245,.22)} .wm .rule{background:rgba(40,37,36,.25)}
.corner{right:110px;top:46px;height:42px;width:200px;object-fit:contain;object-position:right center}
.dk .tx{color:var(--lg)} .wm .tx{color:var(--dark)}
.dk .sb{color:var(--gray)} .wm .sb{color:var(--mid)}
.hd{left:110px;width:1700px;font-size:96px;letter-spacing:-.04em;line-height:1.04}
.hm{left:110px;width:1700px;font-size:64px;letter-spacing:-.035em;line-height:1.08}
.sub{left:110px;width:1700px;font-size:40px;font-weight:400;letter-spacing:-.01em;line-height:1.25}
.hair{height:1px;transform-origin:left center}
.dk .hair{background:rgba(245,245,245,.3)} .wm .hair{background:rgba(40,37,36,.3)}
.clip{left:0;top:0;width:1920px;height:1080px;object-fit:cover;transform-origin:50% 40%}
.lt3{left:110px;bottom:104px;background:var(--dark);border-radius:14px;padding:24px 38px 30px 34px}
#stage .lt3 div,#stage .lt3 span{position:static;white-space:nowrap}
.lt3 .c{font-weight:600;font-size:20px;letter-spacing:.09em;text-transform:uppercase;color:var(--gray)}
#stage .lt3 .c b{position:static;display:inline-block;width:22px;height:2px;background:var(--orange);vertical-align:middle;margin-right:14px}
.lt3 .n{font-size:54px;letter-spacing:-.03em;color:var(--lg);margin-top:12px;line-height:1}
.lt3 .w{font-size:46px;letter-spacing:-.03em;color:var(--lg);margin-top:12px;line-height:1.08}
.q{left:110px;top:400px;width:1700px;font-size:104px;letter-spacing:-.04em;line-height:1.06}
""".replace('__VARS__', ';'.join(f'--{k}:{v}' for k, v in COLORS.items()))

RUNTIME = r"""
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const NS='http://www.w3.org/2000/svg', OR='#EF7619';
const el=(p,tag,at)=>{const e=document.createElementNS(NS,tag); for(const k in at) e.setAttribute(k,at[k]); p.appendChild(e); return e;};
const tl=gsap.timeline({paused:true});
const show=(s,t,d=.5,y0=18)=>tl.fromTo(s,{autoAlpha:0,y:y0},{autoAlpha:1,y:0,duration:d,ease:'power2.out'},t);
const hide=(s,t,d=.35)=>tl.to(s,{autoAlpha:0,duration:d,ease:'power1.in'},t);
const on=(s,t)=>tl.set(s,{autoAlpha:1},t);
const off=(s,t)=>tl.set(s,{autoAlpha:0},t);
const draw=(s,t,d=1,st=0)=>tl.to(s,{strokeDashoffset:0,duration:d,ease:'power1.inOut',stagger:st},t);
const grow=(s,t,d=.6,st=0)=>tl.fromTo(s,{scaleX:0},{scaleX:1,duration:d,ease:'power2.inOut',stagger:st},t);
const vIn=(s,t,d=.25)=>tl.fromTo(s,{autoAlpha:0},{autoAlpha:1,duration:d,ease:'power1.out'},t);
const zoom=(s,t,d,a=1,b=1.04)=>tl.fromTo(s,{scale:a},{scale:b,duration:d,ease:'none',immediateRender:false},t);
const count=(s,t,to,d=1.5,fmt=n=>Math.round(n).toLocaleString('en-US'))=>{const o={v:0}; tl.to(o,{v:to,duration:d,ease:'power2.out',onUpdate:()=>{$(s).textContent=fmt(o.v);}},t);};
const prep=()=>$$('.d').forEach(e=>{ let L=0; try{L=e.getTotalLength();}catch(_){} if(L>0){ e.style.strokeDasharray=L+1; e.style.strokeDashoffset=L+1; } });
"""

SEEK = r"""
window.seek=async t=>{tl.time(t,false);
  for(const c of CLIPS){ const el=$(c.el); if(t>=c.pre && t<c.end){ const i=Math.min(c.n,Math.max(1,Math.floor((t-c.s)*25+1e-6)+1)); const src=c.p+String(i).padStart(4,'0')+'.jpg';
      if(el.dataset.src!==src){el.dataset.src=src;el.src=src;await el.decode();}
      let k=1; for(const [a,b,sc] of (c.punch||[])) if(t>=a&&t<b) k=sc; el.style.scale=String(k); } }
  await new Promise(r=>{let d=false;const f=()=>{if(!d){d=true;r();}};requestAnimationFrame(f);setTimeout(f,60);});
};
CLIPS.forEach(c=>{$(c.el).src=c.p+'0001.jpg';});
window.ready=Promise.all([document.fonts.ready,...$$('img').map(i=>i.decode().catch(()=>{}))]).then(()=>{prep(); return seek(0);}).then(()=>true);
"""

class TL:
    """Collects timeline statements for one scene."""
    def __init__(self): self.out = []
    def __call__(self, s): self.out.append(s); return self
    def show(self, sel, t, d=.5, y0=18): return self(f"show({sel!r},{t:.3f},{d},{y0});")
    def hide(self, sel, t, d=.35): return self(f"hide({sel!r},{t:.3f},{d});")
    def on(self, sel, t): return self(f"on({sel!r},{t:.3f});")
    def off(self, sel, t): return self(f"off({sel!r},{t:.3f});")
    def vin(self, sel, t, d=.25): return self(f"vIn({sel!r},{t:.3f},{d});")
    def draw(self, sel, t, d=1, st=0): return self(f"draw({sel!r},{t:.3f},{d},{st});")
    def grow(self, sel, t, d=.6): return self(f"grow({sel!r},{t:.3f},{d});")
    def zoom(self, sel, t, d, a=1, b=1.04): return self(f"zoom({sel!r},{t:.3f},{d:.3f},{a},{b});")
    def js(self): return '\n'.join(self.out)

def frame(sid, bg='dk', chapter=None, logo=None):
    """Opening tag of a scene: background, rule, chapter label, corner logo."""
    h = f'<div id="{sid}" class="sc {bg} h">'
    if chapter:
        h += f'<div class="rule"></div><div class="chap cap"><b>{chapter[0]}</b><span>{E(chapter[1])}</span></div>'
    if logo:
        h += f'<img class="corner" src="{logo}">'
    return h

class Scene:
    """Result of building a scene: markup, styles, timeline code, and the time its texts need."""
    def __init__(self, html='', css='', js='', need=0.0, texts=None, clips=None):
        self.html, self.css, self.js, self.need = html, css, js, need
        self.texts = texts or []       # (time shown, text) for the readability check
        self.clips = clips or []
        self.holds = []                 # (anchor, seconds): pause the voice-over before anchor

def need_for(texts, end_pad=0.35):
    """Earliest scene end so every text shown is readable long enough."""
    return max([t + reading_time(s) + end_pad for t, s in texts] + [0])
