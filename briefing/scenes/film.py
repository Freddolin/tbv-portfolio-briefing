"""The fixed scene types of a portfolio briefing. Each takes a block (start/end in film time,
anchor resolver) plus the company content, and returns a Scene."""
from .base import E, T, TL, Scene, frame, need_for
from . import panels as P
from ..config import CHAPTERS, reading_time

def explainer(b, c, chapter_key, spec):
    """'The problem' and 'How it works': chapter frame + a sequence of panels cued to the voice-over."""
    sid = b.sid; tl = TL(); texts = []
    h = frame(sid, 'dk', CHAPTERS[chapter_key], c['logo_light'])
    pans = spec['panels']
    starts = [b.T(p['at']) if p.get('at') is not None else (b.t_speech if i == 0 else None) for i, p in enumerate(pans)]
    for i in range(len(pans)):
        if starts[i] is None: raise ValueError(f'{chapter_key}: panel {i + 1} needs an "at" anchor')
    starts[0] = min(starts[0], b.t_speech)
    holds = []
    for i, p in enumerate(pans):
        t0 = starts[i] - .1
        t1 = starts[i + 1] - .1 if i + 1 < len(pans) else b.t_end
        ph, pj, pt, ph_holds = P.build(f'{sid}p{i}', p, t0, t1, b.T, c['logo_light'])
        h += ph; tl(pj); texts += pt; holds += ph_holds
        if i + 1 < len(pans) and pt:      # the next panel must not replace this one before it was read
            short = max(t + reading_time(x) for t, x in pt) - (t1 - .35)
            if short > .05: holds.append((pans[i + 1]['at'], short))
    h += '</div>'
    tl.on(f'#{sid}', b.t0); tl.hide(f'#{sid} .chap,#{sid} .rule', b.t_end - .35, .3); tl.off(f'#{sid}', b.t_end + .01)
    # readability: the last panel decides how long the scene must stay
    last = [x for x in texts if x[0] >= starts[-1] - .2]
    sc = Scene(h, '', tl.js(), need_for(last)); sc.holds = holds
    return sc

def handover(b, c):
    """Company logo + origin, then the founder portrait card that opens into the first interview."""
    sid = b.sid; tl = TL(); f = c['founders'][c['interview']['f1'].get('founder', 0)]
    por = c.get('portrait', {}); ins = por.get('inset', [220, 610, 290, 610]); px, py = por.get('x', 0), por.get('y', 0)
    h = (frame(sid, 'dk') + f'<img class="hero" src="{c["logo_light"]}" style="left:660px;top:400px;width:600px;height:170px;object-fit:contain">'
         f'<div class="cap hcap" style="left:0;width:1920px;text-align:center;top:610px">{E(c["origin"])}</div>'
         f'<img id="{sid}por" class="clip" src="">'
         f'<div class="pcap st" style="position:absolute;left:0;top:838px;width:1920px;text-align:center">'
         f'<div style="font-size:54px;letter-spacing:-.03em;color:var(--lg);line-height:1">{E(f["name"])}</div>'
         f'<div class="cap" style="margin-top:16px;font-size:20px">{E(f["role"])}</div></div></div>')
    t_last = b.T('s-1')                      # "Let's hear it from ..."
    tl.on(f'#{sid}', b.t0)
    tl.show(f'#{sid} .hero', b.t_speech - .2, .7, 14); tl.show(f'#{sid} .hcap', b.t_speech + 1.2, .5, 10)
    tm = max(b.t_speech + 3.0, t_last - .3)
    tl.hide(f'#{sid} .hcap', tm - .05, .3)
    tl(f"tl.to('#{sid} .hero',{{y:-330,scale:.42,duration:.7,ease:'power2.inOut'}},{tm:.3f});")
    tl(f"gsap.set('#{sid}por',{{clipPath:'inset({ins[0]}px {ins[1]}px {ins[2]}px {ins[3]}px round 14px)',x:{px},y:{py}}});")
    tl.vin(f'#{sid}por', tm + .4, .5); tl.show(f'#{sid} .pcap', tm + .7, .5, 12)
    tl.hide(f'#{sid} .hero,#{sid} .pcap', b.t_end - .95, .3)
    tl(f"tl.to('#{sid}por',{{clipPath:'inset(0px 0px 0px 0px round 0px)',x:0,y:0,duration:.6,ease:'power2.inOut'}},{b.t_end - .62:.3f});")
    tl.off(f'#{sid}', b.t_end + .05)
    texts = [(b.t_speech + 1.2, c['origin']), (tm + .7, f['name'] + ' ' + f['role'])]
    clip = dict(el=f'#{sid}por', seg='f1', s=b.t_end, pre=tm, end=b.t_end + .1)
    need = max(tm + .7 + 2.6 + .95, b.t_speech + 1.2 + 2.4)
    return Scene(h, '', tl.js(), need, texts, [clip])

def founder(b, c, seg_key, seg):
    """Interview segment: full-frame clip, lower third, optional cutaways and (f4) the three words."""
    sid = b.sid; tl = TL(); texts = []
    fo = c['founders'][seg.get('founder', 0)]
    h = frame(sid, 'dk') + f'<img id="{sid}v" class="clip" src="">'
    t = b.t_speech                            # clip time 0 in film time
    tl.vin(f'#{sid}', b.t0 - .2, .25)
    tl.zoom(f'#{sid}v', b.t0 - .2, b.t_end - b.t0 + .2, 1, 1.04)
    cut = seg.get('cutaways', [])
    if seg_key == 'f4' and seg.get('words'):
        ws = seg['words']
        h += (f'<div class="lt3 h" id="{sid}lw"><div class="c"><b></b>{E(fo["name"])} on The Bau Ventures</div>'
              + ''.join(f'<div class="w" id="{sid}w{i}">{E(w["text"])}</div>' for i, w in enumerate(ws)) + '</div>')
        tl(f"gsap.set('#{sid}w0',{{autoAlpha:0}}); gsap.set([{','.join(repr(f'#{sid}w{i}') for i in range(1, len(ws)))}],{{height:0,marginTop:0,autoAlpha:0,overflow:'hidden'}});" if len(ws) > 1 else f"gsap.set('#{sid}w0',{{autoAlpha:0}});")
        tl(f"tl.fromTo('#{sid}lw',{{autoAlpha:0,y:16}},{{autoAlpha:1,y:0,duration:.45,ease:'power2.out'}},{t + ws[0]['at'] - .3:.3f});")
        for i, w in enumerate(ws):
            tw = t + w['at']
            if i == 0: tl(f"tl.to('#{sid}w0',{{autoAlpha:1,duration:.2}},{tw:.3f});")
            else: tl(f"tl.to('#{sid}w{i}',{{height:50,marginTop:12,autoAlpha:1,duration:.3}},{tw:.3f});")
            texts.append((tw, w['text']))
    elif seg.get('lower_third', True):
        h += f'<div class="lt3 h" id="{sid}lt"><div class="c"><b></b>{E(fo["role"])}</div><div class="n">{E(fo["name"])}</div></div>'
        tl(f"tl.fromTo('#{sid}lt',{{autoAlpha:0,y:16}},{{autoAlpha:1,y:0,duration:.45,ease:'power2.out'}},{t + .3:.3f});")
        tl.hide(f'#{sid}lt', t + 4.2, .3)
    # cutaways: full-frame panels over the clip while the founder keeps talking
    for i, cw in enumerate(cut):
        a, z = t + cw['at'], t + cw['until']
        bg = cw.get('bg', 'wm')
        cid = f'{sid}c{i}'
        ch = f'<div id="{cid}" class="sc {bg} h">'
        if cw.get('caption'): ch += f'<div class="cap" style="left:110px;top:120px">{E(cw["caption"])}</div>'
        ph, pj, pt, _ = P.build(f'{cid}p', cw['panel'], a + .1, z, lambda an, a=a: a + float(an), c['logo_light'] if bg == 'dk' else c['logo_dark'])
        h += ch + ph + '</div>'
        tl.vin(f'#{cid}', a - .15, .3); tl(pj); tl.hide(f'#{cid}', z - .12, .3)
        if cw.get('caption'): tl.show(f'#{cid} .cap', a + .1, .4, 0)
        texts += pt
        short = [s for (ts, s) in pt if z - ts < 2.2]
        if short: b.warnings.append(f'{seg_key} cutaway {i + 1}: "{short[0]}" shows < 2.2 s before the cutaway ends')
    h += '</div>'
    tl.off(f'#{sid}', b.t_end + .05)
    # punch-ins hide the jump where two interview parts meet (unless a cutaway covers it)
    punch = []
    for k, j in enumerate(seg['_joins']):
        jt = t + j
        if any(t + cw['at'] - .2 <= jt <= t + cw['until'] + .2 for cw in cut): continue
        nxt = seg['_joins'][k + 1] + t if k + 1 < len(seg['_joins']) else b.t_end + 1
        if k % 2 == 0: punch.append([round(jt, 3), round(nxt, 3), 1.08])
    clip = dict(el=f'#{sid}v', seg=seg_key, s=t, pre=b.t0 - .3, end=b.t_end + .1, punch=punch)
    need = 0
    if seg_key == 'f4' and seg.get('words'):
        need = need_for([texts[-1]], .3)
    return Scene(h, '', tl.js(), need, texts, [clip])

def question(b, c, text, bg):
    sid = b.sid; tl = TL()
    logo = c['logo_light'] if bg == 'dk' else c['logo_dark']
    h = frame(sid, bg, None, logo) + f'<div class="q tx h">{T(text)}</div></div>'
    tl.on(f'#{sid}', b.t0); tl.show(f'#{sid} .q', b.t_speech - .15, .6)
    tl.hide(f'#{sid} .q', b.t_end - .35, .3); tl.off(f'#{sid}', b.t_end + .25)
    return Scene(h, '', tl.js(), need_for([(b.t_speech - .15, text)]), [(b.t_speech - .15, text)])

WHY_CSS = r"""
.why .row{left:110px;width:880px;height:150px}
.why .row .n{left:0;top:38px;font-weight:600;font-size:22px;letter-spacing:.06em;color:var(--orange)}
.why .row .t{left:86px;top:26px;font-size:44px;letter-spacing:-.025em;line-height:1.12;color:var(--dark);width:790px}
.why .card{left:1090px;top:196px;width:720px;height:700px;border-radius:14px;background:var(--dark);overflow:hidden}
.why .cp{left:0;top:0;width:720px;height:700px}
.why .cp .cap{left:56px;top:52px;color:#cfcbc6}
.why .cp .big{left:52px;top:180px;font-size:150px;letter-spacing:-.05em;line-height:1;color:var(--lg);white-space:nowrap}
.why .cp .bs{left:56px;top:380px;width:610px;font-size:32px;line-height:1.25;color:var(--lg);font-weight:400}
.why .cp .ol{left:56px;width:608px;height:130px}
.why .cp .ol .hr{left:0;top:0;width:608px;height:1px;background:rgba(245,245,245,.28);transform-origin:left center}
.why .cp .ol .t{left:0;top:30px;font-size:56px;letter-spacing:-.035em;line-height:1;color:var(--lg);white-space:nowrap}
.why .cp .ol .c{left:0;top:98px;font-weight:600;font-size:19px;letter-spacing:.09em;text-transform:uppercase;color:var(--gray);white-space:nowrap}
.why .cp .tx2{left:56px;top:170px;width:610px;font-size:46px;letter-spacing:-.025em;line-height:1.15;color:var(--lg)}
"""

def why(b, c, spec):
    sid = b.sid; tl = TL(); texts = []
    h = frame(sid, 'wm', CHAPTERS['why'], c['logo_dark']) + '<div class="why" style="left:0;top:0;width:1920px;height:1080px">'
    h += '<div class="hdx tx h" style="left:110px;top:186px;font-size:104px;letter-spacing:-.04em;line-height:1;white-space:nowrap">Why we invested</div>'
    h += '<div class="card h">'
    for i, r in enumerate(spec['rows']):
        cd = r.get('card', {}); k = cd.get('type', 'text'); h += f'<div class="cp h" id="{sid}cp{i}"><div class="cap">{E(cd.get("caption", ""))}</div>'
        if k == 'stat':
            h += f'<div class="big" id="{sid}cv{i}">0</div><div class="bs">{T(cd.get("label", ""))}</div>'
        elif k in ('list', 'people'):
            for j, it in enumerate(cd['items']):
                nm, rl = (it, '') if isinstance(it, str) else (it.get('name', ''), it.get('role', ''))
                fs = 56 if len(nm) <= 16 else 44 if len(nm) <= 24 else 36
                h += f'<div class="ol" style="top:{150 + j * (170 if k == "people" else 150)}px"><div class="hr"></div><div class="t" style="font-size:{fs}px">{E(nm)}</div>' + (f'<div class="c">{E(rl)}</div>' if rl else '') + '</div>'
        else:
            h += f'<div class="tx2">{T(cd.get("text", ""))}</div>'
        h += '</div>'
    h += '</div>'
    for i, r in enumerate(spec['rows']):
        h += f'<div class="row h" id="{sid}r{i}" style="top:{392 + i * 150}px"><div class="hair" style="left:0;top:0;width:880px"></div><div class="n">0{i + 1}</div><div class="t">{T(r["title"])}</div></div>'
    h += '</div></div>'
    tl.on(f'#{sid}', b.t0); tl.show(f'#{sid} .hdx', b.t_speech - .1, .6); texts.append((b.t_speech - .1, 'Why we invested'))
    ts = [b.T(r.get('at', f's{i + 1}')) - .1 for i, r in enumerate(spec['rows'])]
    tl.vin(f'#{sid} .card', ts[0], .4)
    for i, r in enumerate(spec['rows']):
        tl.show(f'#{sid}r{i}', ts[i], .5); tl(f"grow('#{sid}r{i} .hair',{ts[i]:.3f},.6);")
        if i: tl.hide(f'#{sid}cp{i - 1}', ts[i] - .15, .25)
        tl.vin(f'#{sid}cp{i}', ts[i] + .1, .35); texts.append((ts[i], r['title']))
        cd = r.get('card', {})
        if cd.get('type') == 'stat':
            pre, suf = cd.get('prefix', ''), cd.get('suffix', '')
            tc = b.T(cd['at']) if cd.get('at') is not None else ts[i] + .6
            tl(f"count('#{sid}cv{i}',{tc:.3f},{float(cd['value'])},1.4,n=>{pre!r}+Math.round(n).toLocaleString('en-US')+{suf!r});")
            texts.append((tc + 1.4, cd.get('label', '')))
        elif cd.get('type') in ('list', 'people'):
            for j, it in enumerate(cd['items']):
                tj = b.T(cd['item_at'][j]) if cd.get('item_at') else ts[i] + .5 + j * .45
                tl(f"show(document.querySelectorAll('#{sid}cp{i} .ol')[{j}],{tj:.3f},.45,18); grow(document.querySelectorAll('#{sid}cp{i} .ol .hr')[{j}],{tj:.3f},.5);")
                texts.append((tj, it if isinstance(it, str) else it.get('name', '')))
        else:
            texts.append((ts[i] + .1, cd.get('text', '')))
    tl.hide(f'#{sid} .why,#{sid} .chap,#{sid} .rule', b.t_end - .35, .3); tl.off(f'#{sid}', b.t_end + .25)
    holds = []
    for i in range(1, len(ts)):                 # a card is replaced when the next row appears
        titles = {r['title'] for r in spec['rows']} | {'Why we invested'}
        prev = [(t, x) for t, x in texts if ts[i - 1] - .01 <= t < ts[i] - .05 and x not in titles]
        if prev:
            short = max(t + reading_time(x) for t, x in prev) - (ts[i] - .15)
            if short > .05: holds.append((spec['rows'][i].get('at', f's{i + 1}'), short))
    sc = Scene(h, WHY_CSS, tl.js(), need_for([x for x in texts if x[0] >= ts[-1] - .2]), texts); sc.holds = holds
    return sc

def close(b, c, spec):
    sid = b.sid; tl = TL()
    h = (frame(sid, 'dk') + f'<img class="hero" src="{c["logo_light"]}" style="left:660px;top:390px;width:600px;height:170px;object-fit:contain">'
         f'<div class="tag tx" style="left:0;width:1920px;top:600px;text-align:center;font-size:46px;letter-spacing:-.025em">{E(spec["tagline"])}</div>'
         f'<img class="tbv" src="assets/img/tbv_h_alpha.png" style="left:568px;top:480px;width:784px;height:106px">'
         f'<div class="cap tcap" style="left:0;width:1920px;top:650px;text-align:center">Part of The Bau Ventures portfolio</div></div>')
    for s_ in ('.tbv', '.tcap', '.hero', '.tag'): tl(f"gsap.set('#{sid} {s_}',{{autoAlpha:0}});")
    tl.on(f'#{sid}', b.t0)
    tl.show(f'#{sid} .hero', b.t_speech - .1, .6, 14)
    tt = b.T(spec.get('tagline_at', 's1')) - .1
    tl.show(f'#{sid} .tag', tt, .6, 12)
    tl.hide(f'#{sid} .hero,#{sid} .tag', b.t_lock - .4, .35)
    tl.show(f'#{sid} .tbv', b.t_lock, .6, 10); tl.show(f'#{sid} .tcap', b.t_lock + .35, .5, 8)
    texts = [(tt, spec['tagline']), (b.t_lock + .35, 'Part of The Bau Ventures portfolio')]
    return Scene(h, '', tl.js(), max(tt + 2.6 + .4, b.t_lock + 3.2), texts)
