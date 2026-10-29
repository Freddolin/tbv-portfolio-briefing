"""Panels: the standard building blocks for 'The problem', 'How it works' and founder cutaways.
A panel fills the area below the chapter rule. Each panel type has a fixed layout so every
film looks the same; only the words, numbers and images change.

Types: statement, words, tiles, flow, points, beats, stat, image, screens, steps."""
from .base import E, T, TL
from ..config import reading_time

X_ICON = '<svg viewBox="0 0 30 30" fill="none" stroke="#EF7619" stroke-width="3"><path d="M4 4L26 26M26 4L4 26"/></svg>'
CHECK_ICON = '<svg viewBox="0 0 30 30" fill="none" stroke="#EF7619" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16L12 24L27 6"/></svg>'
ARROW = '<svg {a} viewBox="0 0 84 20" fill="none" stroke="#EF7619" stroke-width="2"><path d="M2 10H80M70 3L80 10L70 17"/></svg>'

CSS = r"""
.pn{left:0;top:0;width:1920px;height:1080px}
.pn .ph{left:110px;top:186px;width:1700px;font-size:64px;letter-spacing:-.035em;line-height:1.08}
.pn .pbig{left:110px;top:300px;width:1700px;font-size:104px;letter-spacing:-.045em;line-height:1.04}
.pn .psub{left:110px;width:1700px;font-size:40px;font-weight:400;line-height:1.25}
.pn .wd{left:110px;font-size:88px;letter-spacing:-.04em;line-height:1;white-space:nowrap}
.pn .tile{left:110px;width:900px;height:104px;border-radius:14px}
.dk .pn .tile{border:1.5px solid rgba(245,245,245,.7)} .wm .pn .tile{border:1.5px solid rgba(40,37,36,.45)}
.pn .tile .t{left:32px;top:26px;font-size:40px;letter-spacing:-.02em;white-space:nowrap}
.pn .tile svg{right:32px;top:36px;width:30px;height:30px}
.pn .chip{height:72px;border-radius:36px;padding:0 30px;font-size:30px;line-height:70px;white-space:nowrap}
.dk .pn .chip{border:1.5px solid rgba(245,245,245,.6)} .wm .pn .chip{border:1.5px solid rgba(40,37,36,.45)}
.pn .hub{left:760px;top:400px;width:400px;height:300px;border-radius:16px;border:2.5px solid #EF7619}
.pn .hub .hl{left:0;top:96px;width:400px;text-align:center;font-size:56px;letter-spacing:-.03em;white-space:nowrap}
.pn .hub .hc{left:0;top:178px;width:400px;text-align:center;color:#EF7619 !important}
.pn .hub img{left:60px;top:90px;width:280px;height:90px;object-fit:contain}
.pn .fcap{width:440px;text-align:left}
.pn .row{left:110px;width:1700px;height:120px}
.pn .row .n{left:0;top:34px;font-weight:600;font-size:22px;letter-spacing:.06em;color:var(--orange)}
.pn .row .t{left:86px;top:24px;font-size:46px;letter-spacing:-.025em;white-space:nowrap}
.pn .row .v{right:0;top:30px;font-size:34px;font-weight:400;white-space:nowrap;text-align:right}
.pn .bl{left:110px;top:186px;font-weight:600;font-size:22px;letter-spacing:.09em;text-transform:uppercase;color:var(--orange);white-space:nowrap}
.pn .bh{left:110px;top:236px;width:800px;font-size:76px;letter-spacing:-.035em;line-height:1.05}
.pn .bt{left:110px;width:780px;font-size:34px;font-weight:400;line-height:1.3}
.pn .bimg{left:1000px;top:200px;width:810px;height:700px;border-radius:14px;object-fit:contain;background:rgba(245,245,245,.06)}
.wm .pn .bimg{background:rgba(40,37,36,.06)}
.pn .sv{left:104px;top:330px;font-size:240px;letter-spacing:-.055em;line-height:1;white-space:nowrap}
.pn .st2{left:110px;top:600px;width:1500px;font-size:44px;font-weight:400;line-height:1.25}
.pn .iw{left:260px;top:170px;width:1400px;height:780px;border-radius:14px;overflow:hidden}
.pn .iw img{left:0;top:0;width:1400px;height:780px;object-fit:contain}
.pn .isrc{left:260px;top:966px;font-size:18px}
.pn .scr{left:370px;top:176px;width:1180px;height:610px;border-radius:12px;object-fit:cover;box-shadow:0 0 0 1px rgba(245,245,245,.25)}
.pn .scc{left:0;width:1920px;top:826px;text-align:center;font-size:40px;letter-spacing:-.02em;white-space:nowrap}
.pn .step{width:395px;height:420px}
.pn .step .n{left:0;top:30px;font-weight:600;font-size:22px;letter-spacing:.06em;color:var(--orange)}
.pn .step .t{left:0;top:70px;width:370px;font-size:40px;letter-spacing:-.02em;line-height:1.12}
.pn .step .d{left:0;top:200px;width:370px;font-size:28px;font-weight:400;line-height:1.3}
"""

def _items_at(p, key, n, T0, t_start, t_end):
    """Cue times for n items: anchors from the panel spec, else spread evenly."""
    ats = p.get(key)
    if ats:
        return [T0(a) for a in ats]
    span = max(0.6, (t_end - t_start - 1.2))
    return [t_start + 0.8 + i * span / max(1, n) for i in range(n)]

def build(pid, p, t_start, t_end, T0, logo_light=None):
    """One panel. T0(anchor) -> film time. Returns (html, js, texts, holds);
    holds = [(anchor, seconds)]: an item is replaced too early, the voice-over needs a pause before `anchor`."""
    k = p['type']; tl = TL(); texts = []; holds = []; h = f'<div id="{pid}" class="pn h">'
    tl.on(f'#{pid}', t_start)
    sel = lambda c: f'#{pid} {c}'
    if k == 'statement':
        h += f'<div class="pbig tx">{T(p["text"])}</div>'
        top = 300 + 125 * (str(p['text']).count('<br>') + 1) + 30
        if p.get('sub'): h += f'<div class="psub sb" style="top:{top}px">{T(p["sub"])}</div>'
        tl.show(sel('.pbig'), t_start + .1, .6); texts.append((t_start + .1, p['text']))
        if p.get('sub'):
            ts = T0(p['sub_at']) if p.get('sub_at') is not None else t_start + .9
            tl.show(sel('.psub'), ts, .5, 10); texts.append((ts, p['sub']))
    elif k == 'words':
        if p.get('head'): h += f'<div class="ph tx">{T(p["head"])}</div>'
        top0 = 330 if p.get('head') else 220
        step = min(110, (900 - top0) // max(1, len(p['words'])))
        for i, w in enumerate(p['words']): h += f'<div class="wd tx" style="top:{top0 + i * step}px">{E(w)}</div>'
        if p.get('head'): tl.show(sel('.ph'), t_start + .1, .55); texts.append((t_start + .1, p['head']))
        for i, t in enumerate(_items_at(p, 'word_at', len(p['words']), T0, t_start, t_end)):
            tl(f"show(document.querySelectorAll('#{pid} .wd')[{i}],{t - .05:.3f},.4,24);"); texts.append((t, p['words'][i]))
    elif k == 'tiles':
        icon = {'x': X_ICON, 'check': CHECK_ICON}.get(p.get('mark', 'x'), '')
        if p.get('head'): h += f'<div class="ph tx">{T(p["head"])}</div>'
        top0 = 330 if p.get('head') else 220
        for i, it in enumerate(p['items']): h += f'<div class="tile" style="top:{top0 + i * 126}px"><div class="t tx">{E(it)}</div>{icon}</div>'
        if p.get('head'): tl.show(sel('.ph'), t_start + .1, .55); texts.append((t_start + .1, p['head']))
        for i, t in enumerate(_items_at(p, 'item_at', len(p['items']), T0, t_start, t_end)):
            tl(f"show(document.querySelectorAll('#{pid} .tile')[{i}],{t - .05:.3f},.45,16);"); texts.append((t, p['items'][i]))
    elif k == 'flow':
        ins, outs = p.get('inputs', []), p.get('outputs', [])
        if p.get('head'): h += f'<div class="ph tx">{T(p["head"])}</div>'
        cy = 550
        svg = '<svg class="pn" style="left:0;top:0" viewBox="0 0 1920 1080" fill="none" stroke-width="2">'
        for i, it in enumerate(ins):
            y = cy + (i - (len(ins) - 1) / 2) * 110
            h += f'<div class="chip tx fin" style="left:110px;top:{y - 36:.0f}px">{E(it)}</div>'
            svg += f'<path class="d fl" stroke="rgba(180,180,180,.8)" d="M560 {y:.0f}C660 {y:.0f} 660 {cy} 756 {cy}"/>'
        for i, it in enumerate(outs):
            y = cy + (i - (len(outs) - 1) / 2) * 110
            h += f'<div class="chip tx fout" style="left:1330px;top:{y - 36:.0f}px">{E(it)}</div>'
            svg += f'<path class="d fr" stroke="#EF7619" d="M1164 {cy}C1250 {cy} 1240 {y:.0f} 1326 {y:.0f}"/>'
        svg += '</svg>'
        hub = p.get('hub', 'logo')
        inner = f'<img src="{logo_light}">' if hub == 'logo' and logo_light else f'<div class="hl tx">{E(hub)}</div>'
        if p.get('hub_caption'): inner += f'<div class="hc cap">{E(p["hub_caption"])}</div>'
        h += svg + f'<div class="hub">{inner}</div>'
        if p.get('caption'): h += f'<div class="psub sb fcap2" style="top:880px">{T(p["caption"])}</div>'
        if p.get('head'): tl.show(sel('.ph'), t_start + .1, .55); texts.append((t_start + .1, p['head']))
        ti = _items_at(p, 'input_at', len(ins), T0, t_start, (t_start + t_end) / 2)
        for i, t in enumerate(ti):
            tl(f"show(document.querySelectorAll('#{pid} .fin')[{i}],{t:.3f},.4,10);"); texts.append((t, ins[i]))
        th = T0(p['hub_at']) if p.get('hub_at') is not None else (ti[-1] + .7 if ti else t_start + .8)
        tl.draw(sel('.fl'), th - .35, .6, .06); tl.show(sel('.hub'), th, .5, 12); texts.append((th, hub if hub != 'logo' else 'logo'))
        to = _items_at(p, 'output_at', len(outs), T0, th + .5, t_end) if outs else []
        if outs and not p.get('output_at'): to = [th + 1.0 + i * .5 for i in range(len(outs))]
        for i, t in enumerate(to):
            tl(f"draw(document.querySelectorAll('#{pid} .fr')[{i}],{t - .3:.3f},.5);")
            tl(f"show(document.querySelectorAll('#{pid} .fout')[{i}],{t:.3f},.4,10);"); texts.append((t, outs[i]))
        if p.get('caption'):
            tc = T0(p['caption_at']) if p.get('caption_at') is not None else (to[-1] + .8 if to else th + 1.2)
            tl.show(sel('.fcap2'), tc, .45, 10); texts.append((tc, p['caption']))
    elif k == 'points':
        h += f'<div class="ph tx">{T(p["head"])}</div>'
        for i, it in enumerate(p['items']):
            lab, val = (it, '') if isinstance(it, str) else (it.get('label', ''), it.get('value', ''))
            h += (f'<div class="row" style="top:{400 + i * 130}px"><div class="hair" style="left:0;top:0;width:1700px"></div>'
                  f'<div class="n">0{i + 1}</div><div class="t tx">{E(lab)}</div><div class="v sb">{E(val)}</div></div>')
        tl.show(sel('.ph'), t_start + .1, .55); texts.append((t_start + .1, p['head']))
        for i, t in enumerate(_items_at(p, 'item_at', len(p['items']), T0, t_start, t_end)):
            tl(f"show(document.querySelectorAll('#{pid} .row')[{i}],{t - .05:.3f},.45,16);")
            tl(f"grow(document.querySelectorAll('#{pid} .row .hair')[{i}],{t - .05:.3f},.6);")
            it = p['items'][i]; texts.append((t, it if isinstance(it, str) else f"{it.get('label','')} {it.get('value','')}"))
    elif k == 'beats':
        n = len(p['items']); ts = _items_at(p, 'item_at', n, T0, t_start, t_end)
        for i, b in enumerate(p['items']):
            h += f'<div class="bt_{i} h" style="left:0;top:0;width:1920px;height:1080px">'
            h += f'<div class="bl">0{i + 1}&nbsp;&nbsp;{E(b.get("label", ""))}</div><div class="bh tx">{T(b["head"])}</div>'
            if b.get('text'): h += f'<div class="bt sb" style="top:{236 + 84 * (str(b["head"]).count("<br>") + 1) + 40}px">{T(b["text"])}</div>'
            if b.get('image'): h += f'<img class="bimg" src="{b["image"]}">'
            h += '</div>'
        for i, t in enumerate(ts):
            nxt = ts[i + 1] if i + 1 < n else None
            tl.show(sel(f'.bt_{i}'), t - .05, .45, 14); texts.append((t, b_text(p['items'][i])))
            if nxt is not None:
                tl.hide(sel(f'.bt_{i}'), nxt - .35, .25)
                short = t + reading_time(b_text(p['items'][i])) - (nxt - .35)
                if short > .05 and p.get('item_at'): holds.append((p['item_at'][i + 1], short))
    elif k == 'stat':
        h += (f'<div class="ph tx">{T(p.get("head", ""))}</div><div class="sv tx" data-v="{p["value"]}">0</div>'
              f'<div class="st2 sb">{T(p.get("label", ""))}</div>')
        if p.get('head'): tl.show(sel('.ph'), t_start + .1, .55); texts.append((t_start + .1, p['head']))
        tv = T0(p['value_at']) if p.get('value_at') is not None else t_start + .6
        tl.show(sel('.sv'), tv - .1, .3, 0)
        pre, suf = p.get('prefix', ''), p.get('suffix', '')
        tl(f"count('#{pid} .sv',{tv:.3f},{float(p['value'])},1.4,n=>{pre!r}+Math.round(n).toLocaleString('en-US')+{suf!r});")
        tl.show(sel('.st2'), tv + .6, .45, 10); texts.append((tv + .6, p.get('label', '')))
    elif k == 'image':
        h += f'<div class="iw"><img src="{p["src"]}"></div>'
        if p.get('caption'): h += f'<div class="cap" style="left:260px;top:126px">{E(p["caption"])}</div>'
        if p.get('source'): h += f'<div class="isrc cap sb">{E(p["source"])}</div>'
        tl.show(sel('.iw'), t_start + .1, .6, 20); tl.zoom(sel('.iw img'), t_start + .1, max(1, t_end - t_start), 1, 1.06)
        if p.get('caption'): tl.show(sel('.cap'), t_start + .3, .45, 0); texts.append((t_start + .3, p['caption']))
        if p.get('source'): tl.show(sel('.isrc'), t_start + .6, .45, 0)
    elif k == 'screens':
        n = len(p['items']); ts = _items_at(p, 'item_at', n, T0, t_start, t_end)
        for i, it in enumerate(p['items']):
            h += f'<img class="scr scr{i} h" src="{it["src"]}"><div class="scc tx scc{i} h">{E(it.get("caption", ""))}</div>'
        for i, t in enumerate(ts):
            nxt = ts[i + 1] if i + 1 < n else t_end
            tl(f"tl.fromTo('#{pid} .scr{i}',{{autoAlpha:0,y:26}},{{autoAlpha:1,y:0,duration:.5,ease:'power2.out'}},{t:.3f});")
            tl.zoom(f'#{pid} .scr{i}', t + .5, max(1, nxt - t), 1, 1.04)
            if i + 1 < n: tl.off(f'#{pid} .scr{i}', nxt + .35)
            if p['items'][i].get('caption'):
                tl.show(f'#{pid} .scc{i}', t + .4, .4, 10); texts.append((t + .4, p['items'][i]['caption']))
                if i + 1 < n:
                    tl.hide(f'#{pid} .scc{i}', nxt - .2, .2)
                    short = t + .4 + reading_time(p['items'][i]['caption']) - (nxt - .2)
                    if short > .05 and p.get('item_at'): holds.append((p['item_at'][i + 1], short))
    elif k == 'steps':
        if p.get('head'): h += f'<div class="ph tx">{T(p["head"])}</div>'
        n = len(p['items']); wcol = (1700 - 40 * (n - 1)) / n
        for i, it in enumerate(p['items']):
            h += (f'<div class="step" style="left:{110 + i * (wcol + 40):.0f}px;top:380px;width:{wcol:.0f}px"><div class="hair" style="left:0;top:0;width:{wcol:.0f}px"></div>'
                  f'<div class="n">0{i + 1}</div><div class="t tx">{T(it["title"])}</div><div class="d sb">{T(it.get("text", ""))}</div></div>')
        if p.get('head'): tl.show(sel('.ph'), t_start + .1, .55); texts.append((t_start + .1, p['head']))
        for i, t in enumerate(_items_at(p, 'item_at', n, T0, t_start, t_end)):
            tl(f"show(document.querySelectorAll('#{pid} .step')[{i}],{t - .05:.3f},.45,16);")
            tl(f"grow(document.querySelectorAll('#{pid} .step .hair')[{i}],{t - .05:.3f},.6);")
            texts.append((t, f"{p['items'][i]['title']} {p['items'][i].get('text', '')}"))
    else:
        raise ValueError(f'unknown panel type {k}')
    h += '</div>'
    tl.hide(f'#{pid}', t_end - .35, .3)
    return h, tl.js(), texts, holds

def b_text(b): return f"{b.get('head', '')} {b.get('text', '')}"
