"""Assembles the film page (HTML + GSAP timeline) and the intro ident page."""
import json, re
from .scenes import base as B, panels as P, ds as DS
from .config import FPS

def film(scenes, segs, duration):
    css = B.CSS + P.CSS + DS.CSS + ''.join(dict.fromkeys(s.css for s in scenes if s.css))
    body = '\n'.join(s.html for s in scenes)
    clips = []
    for s in scenes:
        for c in s.clips:
            info = segs[c['seg']]
            clips.append(dict(el=c['el'], s=round(c['s'], 3), n=info['n'], p=info['prefix'], pre=round(c['pre'], 3),
                              end=round(c['end'], 3), punch=c.get('punch', [])))
    js = B.RUNTIME + '\n'.join(s.js for s in scenes) + f'\ntl.to({{}},{{duration:.1}},{duration:.3f});\nconst CLIPS={json.dumps(clips)};\nwindow.DUR={duration:.3f};\n' + B.SEEK
    return ('<!doctype html>\n<html><head><meta charset="utf-8">\n<style>' + css + '</style></head><body>\n<div id="stage">\n'
            + body + '\n</div>\n<script src="node_modules/gsap/dist/gsap.min.js"></script>\n<script>\n' + js + '\n</script>\n</body></html>\n')

IDENT = r"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
""" + B.CSS + r"""
#lock{left:568px;top:470px;width:784px;height:106px;transform-origin:left top}
#capC{left:0;width:1920px;text-align:center;top:640px;font-size:26px;letter-spacing:.14em;color:var(--gray)}
#rule{left:110px;right:110px;top:108px;height:1px;background:rgba(245,245,245,.22);transform-origin:left center}
#capR{right:110px;top:64px;color:#cfcbc6}
.ln{left:110px;font-size:96px;letter-spacing:-.04em;line-height:1;white-space:nowrap}
#capL{left:0;width:1920px;text-align:center;top:392px;font-size:30px;letter-spacing:.14em;color:var(--lg)}
#stage #capL b{position:static;display:inline-block;width:30px;height:2px;background:var(--orange);vertical-align:middle;margin-right:20px}
#hair{left:760px;top:462px;width:400px;height:1px;background:rgba(245,245,245,.35)}
#wm{left:660px;top:500px;width:600px;height:150px;object-fit:contain}
#stage #capC i,#stage #capR i{position:static;font-style:normal;display:inline}
#numC{color:#8a8783}
</style></head><body>
<div id="stage">
  <img id="lock" class="h" src="assets/img/tbv_h_alpha.png">
  <div id="capC" class="cap h">Portfolio briefing <i id="numC">#__NUM__</i></div>
  <div id="rule" class="h"></div>
  <div id="capR" class="cap h">Portfolio briefing <i>#__NUM__</i></div>
  <div class="ln h" id="l1" style="top:300px">Who we backed.</div>
  <div class="ln h" id="l2" style="top:432px">Why.</div>
  <div class="ln h" id="l3" style="top:564px">What it means for Drees &amp; Sommer.</div>
  <div id="capL" class="cap h"><b></b>Our latest investment</div>
  <div id="hair" class="h"></div>
  <img id="wm" class="h" src="__WM__">
</div>
<script src="node_modules/gsap/dist/gsap.min.js"></script>
<script>
const C=__CUES__;
const $$=s=>[...document.querySelectorAll(s)];
const tl=gsap.timeline({paused:true});
const show=(s,t,d=.5,y0=18)=>tl.fromTo(s,{autoAlpha:0,y:y0},{autoAlpha:1,y:0,duration:d,ease:'power2.out'},t);
const hide=(s,t,d=.3)=>tl.to(s,{autoAlpha:0,duration:d,ease:'power1.in'},t);
show('#lock',.15,.7,14);
show('#capC',C.vo+1.0,.5,10);
tl.to('#numC',{color:'#F5F5F5',duration:.35,ease:'power2.out'},C.num);
const tB=C.b1-.8;
hide('#capC',tB-.05,.25);
tl.to('#lock',{x:-458,y:-420,scale:.301,duration:.6,ease:'power2.inOut'},tB);
tl.fromTo('#rule',{autoAlpha:0,scaleX:0},{autoAlpha:1,scaleX:1,duration:.6,ease:'power2.inOut'},tB+.2);
show('#capR',tB+.45,.4,0);
show('#l1',C.b1,.45,26); show('#l2',C.b2,.45,26); show('#l3',C.b3,.45,26);
hide('.ln',C.s2end+.2,.3);
show('#capL',C.c,.45,12);
tl.fromTo('#hair',{autoAlpha:0,scaleX:0},{autoAlpha:1,scaleX:1,duration:.6,ease:'power2.inOut'},C.c+.15);
show('#wm',C.end+.05,.45,12);
hide(['#wm','#capL','#hair','#lock','#rule','#capR'],C.end+1.35,.3);
tl.to({}, {duration:.1}, C.end+1.7);
window.DUR=C.end+1.72;
window.seek=async t=>{tl.time(t,false); await new Promise(r=>{let d=false;const f=()=>{if(!d){d=true;r();}};requestAnimationFrame(f);setTimeout(f,50);});};
window.ready=Promise.all([document.fonts.ready,...$$('img').map(i=>i.decode().catch(()=>{}))]).then(()=>seek(0)).then(()=>true);
</script>
</body></html>
"""

def ident(num, wordmark, cues):
    return IDENT.replace('__NUM__', str(num)).replace('__WM__', wordmark).replace('__CUES__', json.dumps(cues))

def ident_cues(take_words, offset=0.5):
    """Cue times from the aligned intro voice (placed at `offset` s)."""
    w = [(a, s + offset, e + offset) for a, s, e in take_words]
    idx = lambda word, after=0: next(i for i, x in enumerate(w) if x[0] == word and i >= after)
    i_num = idx('number'); i_who = idx('who'); i_why = idx('why', i_who); i_what = idx('what', i_why)
    i_som = idx('sommer', i_what); i_this = idx('this', i_som)
    return dict(vo=offset, num=round(w[i_num + 1][1], 2), b1=round(w[i_who][1], 2), b2=round(w[i_why][1], 2),
                b3=round(w[i_what - 1][1] if w[i_what - 1][0] == 'and' else w[i_what][1], 2), s2end=round(w[i_som][2], 2),
                c=round(w[i_this][1], 2), end=round(w[-1][2] + .2, 2))
