"""Visual panels: scenes that show instead of tell. Used when a film has no interview footage and
the voice-over needs pictures: product walkthroughs on real screenshots, notification piles,
skylines, portraits, growth bars, funnels and roadmaps.

Types: notify, skyline, ui, faces, bars, funnel, path, units.
Same contract as panels.build: returns (html, js, texts, holds)."""
import json
from .base import E, T, TL

TYPES = ('notify', 'skyline', 'ui', 'faces', 'bars', 'funnel', 'path', 'units')

_I = {
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    'invoice': '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h5"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'sheet': '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M3 9h18M3 14h18M9 4v16M15 4v16"/>',
    'alert': '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
    'building': '<path d="M4 21V5l8-3v19M12 8h8v13M2 21h20M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2"/>',
    'tower': '<path d="M6 21V3h12v18M3 21h18M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
    'euro': '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5a4 4 0 1 0 0 7M7 11h6M7 13.5h6"/>',
    'people': '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2c3 .2 5.5 2.4 5.5 5.8"/>',
    'check': '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.5"/>',
    'wrench': '<path d="M14.5 6.5a4 4 0 0 0 5 5l-8.3 8.3a2.1 2.1 0 0 1-3-3z"/><path d="M14.5 6.5l3-3a4 4 0 0 1 2 5"/>',
    'doc': '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/><path d="M9 14l2 2 4-4"/>',
}

def icon(name, size=40, color='currentColor', sw=1.6):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" style="position:static;display:block">{_I.get(name, _I["doc"])}</svg>')

CSS = r"""
.vx{left:0;top:0;width:1920px;height:1080px}
.nt{width:640px;height:116px;border-radius:18px;background:#F5F5F5;box-shadow:0 22px 44px rgba(0,0,0,.38)}
.nt .ic{left:24px;top:26px;width:64px;height:64px;border-radius:15px;background:#ECE9E4;color:#282524}
.nt .ic svg{position:absolute !important;left:14px;top:14px}
.nt.err .ic{background:#fbe1dc;color:#c0392b}
.nt .t{left:108px;top:22px;width:420px;font-size:30px;letter-spacing:-.02em;color:#282524;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nt .m{left:108px;top:64px;width:420px;font-size:23px;font-weight:400;color:#7d7873;white-space:nowrap}
.nt .tm{right:26px;top:26px;font-size:21px;font-weight:400;color:#7d7873}
.nt .dot{right:28px;top:70px;width:14px;height:14px;border-radius:50%;background:#EF7619}
.uw{border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 30px 80px rgba(0,0,0,.45)}
.uw .ub{left:0;top:0;right:0;height:40px;background:#e9e7e3}
.uw .ub i{top:14px;width:12px;height:12px;border-radius:50%;background:#c9c5bf}
.uw .ub .uu{left:0;right:0;top:9px;text-align:center;font-size:17px;color:#7d7873;font-weight:500}
.uw .uv{left:0;top:40px;overflow:hidden;background:#fff}
.uw .uc{left:0;top:0;transform-origin:0 0}
.uw .uc img{left:0;top:0}
.ubx{border:4px solid #EF7619;border-radius:12px;box-shadow:0 0 0 4000px rgba(25,22,21,.42)}
.ulb{background:rgba(40,37,36,.94);border-radius:40px;padding:0 30px 0 56px;height:68px;line-height:66px;font-size:30px;letter-spacing:-.01em;color:#F5F5F5;white-space:nowrap;box-shadow:0 14px 30px rgba(0,0,0,.35)}
.ulb b{left:26px;top:26px;width:16px;height:16px;border-radius:50%;background:#EF7619}
.ucd{width:600px;border-radius:20px;background:#fff;box-shadow:0 30px 70px rgba(0,0,0,.45);padding:30px 34px 32px}
#stage .ucd *{position:static}
.ucd .k{font-weight:600;font-size:19px;letter-spacing:.09em;text-transform:uppercase;color:#7d7873}
.ucd .hh{font-size:36px;letter-spacing:-.025em;color:#1f1d1c;margin-top:10px;line-height:1.12}
.ucd .r{display:flex;align-items:center;gap:16px;font-size:26px;font-weight:400;color:#3a3634;margin-top:18px}
.ucd .r span.s{margin-left:auto;font-size:19px;font-weight:600;letter-spacing:.04em;padding:6px 14px;border-radius:20px;background:#e5efdc;color:#2f5a1d}
.ucd .btn{display:inline-block;margin-top:28px;font-size:26px;padding:16px 34px;border-radius:40px;background:#0d1d00;color:#fff}
.ucd .btn.ok{background:#2f7a1d}
.ucd .r svg{color:#EF7619}
.ftx{text-align:center}
.fc .ph2{left:0;top:0;border-radius:18px;object-fit:cover}
.fc .n{left:0;font-size:30px;letter-spacing:-.025em;white-space:nowrap}
.fc .r{left:0;font-weight:600;font-size:19px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap}
.br{transform-origin:50% 100%;border-radius:12px 12px 0 0}
.bv{font-size:72px;letter-spacing:-.04em;line-height:1;white-space:nowrap;text-align:center}
.bl2{font-size:28px;font-weight:400;white-space:nowrap;text-align:center}
.bs{font-weight:600;font-size:18px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap;text-align:center;color:var(--orange)}
.fb{height:116px;border-radius:14px;transform-origin:0 50%}
.fv{font-size:62px;letter-spacing:-.04em;line-height:1;white-space:nowrap}
.fl2{font-size:34px;font-weight:400;white-space:nowrap}
.pnode{width:28px;height:28px;border-radius:50%;border:4px solid #EF7619;background:var(--dark)}
.wm .pnode{background:var(--warm)}
.pic{width:128px;height:128px;border-radius:30px}
.dk .pic{border:1.5px solid rgba(245,245,245,.45);color:#F5F5F5} .wm .pic{border:1.5px solid rgba(40,37,36,.4);color:#282524}
.pic svg{position:absolute !important;left:27px;top:27px}
.pt{font-size:46px;letter-spacing:-.025em;line-height:1.1;text-align:center}
.pd{font-size:29px;font-weight:400;line-height:1.3;text-align:center}
.ug{width:92px;height:92px}
.dk .pline{background:rgba(245,245,245,.35)} .wm .pline{background:rgba(40,37,36,.3)}
.vnote{left:110px;top:960px;font-size:24px;font-weight:400;opacity:.75}
"""

# scattered pile positions for notification cards (left, top, rotation)
_PILE = [(250, 190, -2.2), (990, 236, 1.6), (420, 352, 1.2), (1110, 428, -1.6), (230, 536, -.8), (900, 606, 2.0),
         (560, 716, 1.4), (1140, 790, -1.2), (640, 300, .6), (700, 640, -.6)]

def _times(p, n, T0, t_start, t_end, key='item_at', gap=.6):
    """Cue times for n items. Anchors may be given for some items; missing ones (None) sit between their
    neighbours, trailing ones follow the last anchor `gap` seconds apart. No anchors at all: one every `gap` s."""
    ats = list(p.get(key) or [])
    ats += [None] * (n - len(ats))
    ts = [T0(a) if a is not None else None for a in ats[:n]]
    if ts and ts[0] is None: ts[0] = t_start + .5
    for i in range(n):
        if ts[i] is not None: continue
        j = i
        while j < n and ts[j] is None: j += 1
        if j < n:
            for k in range(i, j): ts[k] = ts[i - 1] + (ts[j] - ts[i - 1]) * (k - i + 1) / (j - i + 1)
        else:
            for k in range(i, n): ts[k] = ts[k - 1] + gap
    return ts

def build(pid, p, t_start, t_end, T0, logo_light=None):
    k = p['type']; tl = TL(); texts = []; holds = []
    h = f'<div id="{pid}" class="pn h">'
    tl.on(f'#{pid}', t_start)
    sel = lambda c: f'#{pid} {c}'
    if p.get('head'):
        h += f'<div class="ph tx">{T(p["head"])}</div>'
        tl.show(sel('.ph'), t_start + .1, .55); texts.append((t_start + .1, p['head']))

    if k == 'notify':
        n = len(p['items']); ts = _times(p, n, T0, t_start, t_end)
        for i, it in enumerate(p['items']):
            x, y, r = _PILE[i % len(_PILE)]
            if p.get('head'): y += 110
            err = ' err' if it.get('kind') == 'error' else ''
            h += (f'<div class="nt{err}" style="left:{x}px;top:{y}px;transform:rotate({r}deg);z-index:{i + 1}">'
                  f'<div class="ic">{icon(it.get("icon", "mail"), 36)}</div><div class="t">{E(it["title"])}</div>'
                  f'<div class="m">{E(it.get("meta", ""))}</div><div class="tm">{E(it.get("time", ""))}</div>'
                  + ('' if it.get('time') else '<div class="dot"></div>') + '</div>')
        for i, t in enumerate(ts):
            tl(f"tl.fromTo(document.querySelectorAll('#{pid} .nt')[{i}],{{autoAlpha:0,y:-46,scale:.93}},{{autoAlpha:1,y:0,scale:1,duration:.45,ease:'back.out(1.7)'}},{t - .05:.3f});")
            texts.append((t, ''))
        if p.get('caption'):
            h += f'<div class="vnote tx">{E(p["caption"])}</div>'; tl.show(sel('.vnote'), ts[-1] + .3, .4, 0); texts.append((ts[-1] + .3, p['caption']))

    elif k == 'skyline':
        hs = p.get('heights', [260, 380, 300, 460, 340, 420, 280, 360, 320])
        n = len(hs); base = 860; gap = 34; w = (1700 - gap * (n - 1)) / n
        svg = f'<svg class="vx" viewBox="0 0 1920 1080" fill="none" stroke="#F5F5F5" stroke-width="2.5">'
        svg += f'<path class="d sk0" d="M90 {base}H1830"/>'
        cards = ''
        for i, bh in enumerate(hs):
            x = 110 + i * (w + gap); y = base - bh
            svg += f'<path class="d skb skb{i}" d="M{x:.0f} {base}V{y}H{x + w:.0f}V{base}"/>'
            for r in range(y + 40, base - 40, 56):
                for cx in (x + w * .3, x + w * .62):
                    svg += f'<rect class="skw skw{i}" x="{cx - 9:.0f}" y="{r}" width="18" height="24" rx="2" stroke="rgba(245,245,245,.45)" stroke-width="1.6" opacity="0"/>'
            for j in range(1 + (i * 7) % 3):
                cards += (f'<div class="skc skc{i}" style="left:{x + w / 2 - 70 + (j % 2) * 18:.0f}px;top:{y - 62 - j * 46:.0f}px;width:140px;height:38px;'
                          f'border-radius:10px;background:#F5F5F5;box-shadow:0 8px 18px rgba(0,0,0,.35)"><div style="left:12px;top:12px;width:14px;height:14px;border-radius:50%;background:#EF7619"></div>'
                          f'<div style="left:36px;top:15px;width:{60 + j * 14}px;height:8px;border-radius:4px;background:#c9c5bf"></div></div>')
        svg += '</svg>'
        h += svg + cards
        ts = _times(p, n, T0, t_start, t_end)
        tl.draw(sel('.sk0'), t_start + .05, .8)
        for i, t in enumerate(ts):
            tl.draw(sel(f'.skb{i}'), t - .1, .7)
            tl(f"tl.to('#{pid} .skw{i}',{{opacity:1,duration:.4,stagger:.02}},{t + .3:.3f});")
            tl(f"tl.fromTo('#{pid} .skc{i}',{{autoAlpha:0,y:-20}},{{autoAlpha:1,y:0,duration:.35,ease:'back.out(1.8)',stagger:.12}},{t + .45:.3f});")
        texts.append((t_start, ''))

    elif k == 'ui':
        L, Tp, W, H = p.get('window', [210, 150, 1500, 844])
        VW, VH = W, H - 40
        IW, IH = p['size']
        def cam(v):
            x, y, w, hh = v; s = min(VW / w, VH / hh)
            return (VW - w * s) / 2 - x * s, (VH - hh * s) / 2 - y * s, s
        h += (f'<div class="uw" style="left:{L}px;top:{Tp}px;width:{W}px;height:{H}px"><div class="ub"><i style="left:18px"></i><i style="left:38px"></i><i style="left:58px"></i>'
              f'<div class="uu">{E(p.get("url", "walter"))}</div></div>'
              f'<div class="uv" style="width:{VW}px;height:{VH}px"><div class="uc" style="width:{IW}px;height:{IH}px"><img src="{p["src"]}" style="width:{IW}px;height:{IH}px"></div>')
        steps = p.get('steps', [])
        ts = [T0(s_['at']) if s_.get('at') is not None else t_start + .3 for s_ in steps]
        v0 = p.get('start', steps[0]['view'] if steps and steps[0].get('view') else [0, 0, IW, IH])
        x0, y0, s0 = cam(v0)
        boxes = ''; labels = ''
        cur = (x0, y0, s0)
        for i, (s_, t) in enumerate(zip(steps, ts)):
            if s_.get('view'): cur = cam(s_['view'])
            cx, cy, cs = cur
            if s_.get('box'):
                bx, by, bw, bh = s_['box']
                boxes += f'<div class="ubx ubx{i} h" style="left:{cx + bx * cs - 8:.0f}px;top:{cy + by * cs - 8:.0f}px;width:{bw * cs + 16:.0f}px;height:{bh * cs + 16:.0f}px"></div>'
                lx, ly = L + cx + bx * cs - 8, Tp + 40 + cy + (by + bh) * cs + 26
                if ly + 70 > Tp + H - 10: ly = Tp + 40 + cy + by * cs - 98
            else:
                lx, ly = L + 40, Tp + H - 110
            if s_.get('label'):
                lx = max(L - 40, min(lx, L + W - 40 - 22 * len(s_['label'])))
                labels += f'<div class="ulb ulb{i} h" style="left:{lx:.0f}px;top:{ly:.0f}px"><b></b>{E(s_["label"])}</div>'
        h += boxes + '</div></div>' + labels
        tl(f"gsap.set('#{pid} .uc',{{x:{x0:.1f},y:{y0:.1f},scale:{s0:.4f}}});")
        tl.show(sel('.uw'), t_start + .05, .6, 30)
        cur = (x0, y0, s0)
        events = []                              # (time, anchor, seconds it needs before the next thing happens)
        for i, (s_, t) in enumerate(zip(steps, ts)):
            nxt = ts[i + 1] if i + 1 < len(ts) else t_end
            move = 0
            if s_.get('view'):
                nx, ny, ns = cam(s_['view'])
                if (round(nx), round(ny), round(ns, 3)) != (round(cur[0]), round(cur[1]), round(cur[2], 3)):
                    move = 1.0
                    tl(f"tl.to('#{pid} .uc',{{x:{nx:.1f},y:{ny:.1f},scale:{ns:.4f},duration:1.0,ease:'power2.inOut'}},{t - .15:.3f});")
                cur = (nx, ny, ns)
            ta = t - .15 + move
            events.append((t, s_.get('at'), move + (1.6 if (s_.get('box') or s_.get('label')) else .2)))
            if s_.get('box'):
                tl(f"tl.fromTo('#{pid} .ubx{i}',{{autoAlpha:0,scale:1.04}},{{autoAlpha:1,scale:1,duration:.35,ease:'power2.out'}},{ta:.3f});")
                tl.hide(sel(f'.ubx{i}'), max(nxt - .15, ta + .5), .25)
            if s_.get('label'):
                tl.show(sel(f'.ulb{i}'), ta + .15, .35, 12); texts.append((ta + .15, s_['label']))
                tl.hide(sel(f'.ulb{i}'), max(nxt - .15, ta + .6), .25)
        for j, o in enumerate(p.get('overlays', [])):
            t = T0(o['at']); te = T0(o['until']) if o.get('until') else t_end
            ox, oy = o.get('pos', [L + W - 640, Tp + 120])
            rows = ''.join(f'<div class="r">{icon(r_.get("icon", "check"), 30, "#EF7619", 2)}<span>{E(r_["text"])}</span>'
                           + (f'<span class="s">{E(r_["status"])}</span>' if r_.get('status') else '') + '</div>' for r_ in o.get('rows', []))
            btn = (f'<div style="position:relative;height:90px"><div class="btn b1" style="position:absolute">{E(o["button"])}</div>'
                   f'<div class="btn ok b2" style="position:absolute;opacity:0">{E(o.get("done", "Done"))}</div></div>') if o.get('button') else ''
            h += (f'<div class="ucd uo{j} h" style="left:{ox}px;top:{oy}px"><div class="k">{E(o.get("kicker", ""))}</div>'
                  f'<div class="hh">{E(o.get("title", ""))}</div>{rows}{btn}</div>')
            tl(f"tl.fromTo('#{pid} .uo{j}',{{autoAlpha:0,x:60}},{{autoAlpha:1,x:0,duration:.5,ease:'power3.out'}},{t - .1:.3f});")
            for r_i in range(len(o.get('rows', []))):
                tl(f"tl.fromTo(document.querySelectorAll('#{pid} .uo{j} .r')[{r_i}],{{opacity:0}},{{opacity:1,duration:.3}},{t + .35 + r_i * .35:.3f});")
            texts.append((t, f'{o.get("title", "")} ' + ' '.join(r_['text'] for r_ in o.get('rows', []))))
            nrows = len(o.get('rows', []))
            events.append((t, o['at'], .35 + nrows * .35 + (.6 if o.get('click_at') is not None else 1.0)))
            if o.get('click_at') is not None: events.append((T0(o['click_at']), o['click_at'], 1.1))
            if o.get('button') and o.get('click_at') is not None:
                tc = T0(o['click_at'])
                tl(f"tl.to('#{pid} .uo{j} .b1',{{scale:.92,duration:.12,yoyo:true,repeat:1}},{tc:.3f});")
                tl(f"tl.to('#{pid} .uo{j} .b1',{{opacity:0,duration:.15}},{tc + .24:.3f});")
                tl(f"tl.fromTo('#{pid} .uo{j} .b2',{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.3,ease:'back.out(2)'}},{tc + .24:.3f});")
                texts.append((tc + .24, o.get('done', 'Done')))
            if te < t_end - .4: tl.hide(sel(f'.uo{j}'), te - .3, .3)
        events.sort(key=lambda e: e[0])
        for (ta_, a_, need), (tb_, b_, _) in zip(events, events[1:]):
            if b_ is not None and b_ != a_ and tb_ - ta_ < need - .05: holds.append((b_, round(need - (tb_ - ta_), 2)))

    elif k == 'faces':
        n = len(p['items']); gap = 40; w = (1700 - gap * (n - 1)) / n; ph = min(420, w * 1.25)
        top = 300 if p.get('head') else 220
        for i, it in enumerate(p['items']):
            x = 110 + i * (w + gap)
            h += (f'<div class="fc fc{i}" style="left:{x:.0f}px;top:{top}px;width:{w:.0f}px;height:{ph + 140:.0f}px">'
                  f'<img class="ph2" src="{it["photo"]}" style="width:{w:.0f}px;height:{ph:.0f}px">'
                  f'<div class="n tx" style="top:{ph + 26:.0f}px">{E(it["name"])}</div>'
                  f'<div class="r sb" style="top:{ph + 80:.0f}px">{E(it.get("role", ""))}</div></div>')
        for i, t in enumerate(_times(p, n, T0, t_start, t_end)):
            tl(f"tl.fromTo('#{pid} .fc{i}',{{autoAlpha:0,y:40}},{{autoAlpha:1,y:0,duration:.55,ease:'power3.out'}},{t - .1:.3f});")
            tl(f"tl.fromTo('#{pid} .fc{i} img',{{scale:1.08}},{{scale:1,duration:1.4,ease:'power2.out'}},{t - .1:.3f});")
            texts.append((t, p['items'][i]['name']))

    elif k == 'bars':
        n = len(p['items']); vmax = max(float(it['value']) for it in p['items'])
        base = 860; hmax = 430; span = 1500; bw = min(230, span / n * .5)
        top_off = 0
        h += f'<div class="hair hb0" style="left:160px;top:{base}px;width:1600px"></div>'
        for i, it in enumerate(p['items']):
            cx = 210 + span * (i + .5) / n; bh = max(8, hmax * float(it['value']) / vmax)
            col = 'var(--orange)' if i == n - 1 else 'rgba(245,245,245,.88)'
            h += (f'<div class="br br{i}" style="left:{cx - bw / 2:.0f}px;top:{base - bh:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px;background:{col}"></div>'
                  f'<div class="bv tx bv{i}" style="left:{cx - 200:.0f}px;width:400px;top:{base - bh - 92:.0f}px">0</div>'
                  f'<div class="bl2 sb blx{i}" style="left:{cx - 200:.0f}px;width:400px;top:{base + 22}px">{E(it["label"])}</div>')
            if it.get('tag'): h += f'<div class="bs bsx{i}" style="left:{cx - 200:.0f}px;width:400px;top:{base + 68}px">{E(it["tag"])}</div>'
        tl.grow(sel('.hb0'), t_start + .1, .7)
        for i, t in enumerate(_times(p, n, T0, t_start, t_end)):
            it = p['items'][i]
            tl(f"tl.fromTo('#{pid} .br{i}',{{scaleY:0}},{{scaleY:1,duration:.8,ease:'power3.out'}},{t - .1:.3f});")
            tl.show(sel(f'.bv{i}'), t - .1, .3, 0)
            fmt = json.dumps(it.get('display', ''))
            tl(f"count('#{pid} .bv{i}',{t - .1:.3f},{float(it['value'])},.8,n=>({fmt}||Math.round(n).toLocaleString('en-US')));")
            tl.show(sel(f'.blx{i}'), t, .35, 8); texts.append((t, f"{it['label']} {it['value']}"))
            if it.get('tag'): tl.show(sel(f'.bsx{i}'), t + .2, .35, 8)
        if p.get('note'):
            h += f'<div class="vnote tx">{E(p["note"])}</div>'; tl.show(sel('.vnote'), t_start + .5, .4, 0)

    elif k == 'funnel':
        n = len(p['items']); vmax = max(float(it['value']) for it in p['items'])
        top0 = 330 if p.get('head') else 250; step = 150; wmax = 1150
        for i, it in enumerate(p['items']):
            w = max(170, wmax * float(it['value']) / vmax); y = top0 + i * step
            last = i == n - 1 and p.get('accent_last', True)
            col = 'var(--orange)' if last else 'rgba(245,245,245,.9)'; tcol = '#F5F5F5' if last else '#282524'
            h += (f'<div class="fb fb{i}" style="left:110px;top:{y}px;width:{w:.0f}px;background:{col}"></div>'
                  f'<div class="fv fv{i}" style="left:140px;top:{y + 27}px;color:{tcol}">{E(it.get("display", it["value"]))}</div>'
                  f'<div class="fl2 tx flx{i}" style="left:{110 + w + 34:.0f}px;top:{y + 36}px">{E(it["label"])}</div>')
        for i, t in enumerate(_times(p, n, T0, t_start, t_end)):
            tl(f"tl.fromTo('#{pid} .fb{i}',{{scaleX:0}},{{scaleX:1,duration:.7,ease:'power3.out'}},{t - .1:.3f});")
            tl.show(sel(f'.fv{i}'), t + .25, .35, 0); tl.show(sel(f'.flx{i}'), t + .35, .35, 0)
            texts.append((t + .35, f"{p['items'][i].get('display', p['items'][i]['value'])} {p['items'][i]['label']}"))
        if p.get('note'):
            h += f'<div class="vnote tx">{E(p["note"])}</div>'; tl.show(sel('.vnote'), t_start + .5, .4, 0)

    elif k == 'path':
        n = len(p['items']); y = 600 if p.get('head') else 540; x0, x1 = 300, 1620
        if n == 1: x0 = x1 = 960
        dx = (x1 - x0) / max(1, n - 1); cw = min(560, dx - 40) if n > 1 else 700
        h += f'<div class="hair pline pl0" style="left:{x0 - 140}px;top:{y}px;width:{x1 - x0 + 280}px;height:2px"></div>'
        for i, it in enumerate(p['items']):
            x = x0 + dx * i
            lines = 1 + str(it['title']).count('<br>')
            h += (f'<div class="pnode pn{i}" style="left:{x - 14:.0f}px;top:{y - 13}px"></div>'
                  f'<div class="pic pc{i}" style="left:{x - 64:.0f}px;top:{y - 196}px">{icon(it.get("icon", "check"), 72, "currentColor", 1.4)}</div>'
                  f'<div class="pt tx pt{i}" style="left:{x - cw / 2:.0f}px;width:{cw:.0f}px;top:{y + 52}px">{T(it["title"])}</div>'
                  f'<div class="pd sb pd{i}" style="left:{x - cw / 2:.0f}px;width:{cw:.0f}px;top:{y + 52 + 58 * lines}px">{T(it.get("text", ""))}</div>')
        tl.grow(sel('.pl0'), t_start + .1, 1.2)
        for i, t in enumerate(_times(p, n, T0, t_start, t_end)):
            tl(f"tl.fromTo('#{pid} .pn{i}',{{autoAlpha:0,scale:0}},{{autoAlpha:1,scale:1,duration:.4,ease:'back.out(2)'}},{t - .15:.3f});")
            tl.show(sel(f'.pc{i}'), t - .05, .45, 18); tl.show(sel(f'.pt{i}'), t + .05, .4, 10); tl.show(sel(f'.pd{i}'), t + .2, .4, 10)
            texts.append((t + .05, f"{p['items'][i]['title']} {p['items'][i].get('text', '')}"))

    elif k == 'units':                       # a big number and a grid of buildings filling up (one icon per `per` units)
        n = int(round(float(p['value']) / float(p.get('per', 100)))); cols = p.get('cols', 8); sz = 92; gap = 26
        gx = 1810 - cols * sz - (cols - 1) * gap; gy = 300
        h += (f'<div class="sv tx uvn" style="left:104px;top:330px">0</div>'
              f'<div class="st2 sb uvl" style="top:600px;width:760px">{T(p.get("label", ""))}</div>')
        for i in range(n):
            r, c_ = divmod(i, cols)
            h += f'<div class="ug ug{i}" style="left:{gx + c_ * (sz + gap)}px;top:{gy + r * (sz + gap)}px;color:{"#EF7619" if i == n - 1 else "#F5F5F5"}">{icon("building", sz, "currentColor", 1.3)}</div>'
        t = T0(p['value_at']) if p.get('value_at') is not None else t_start + .3
        tl.show(sel('.uvn'), t - .1, .3, 0)
        disp = json.dumps(p.get('display', ''))
        tl(f"count('#{pid} .uvn',{t:.3f},{float(p['value'])},1.6,n=>(n>={float(p['value']) - .5}&&{disp})?{disp}:Math.round(n).toLocaleString('en-US'));")
        tl(f"tl.fromTo('#{pid} .ug',{{autoAlpha:0,scale:.6}},{{autoAlpha:1,scale:1,duration:.3,ease:'back.out(2)',stagger:{1.5 / max(1, n):.3f}}},{t:.3f});")
        tl.show(sel('.uvl'), t + .5, .4, 10); texts.append((t + .5, p.get('label', '')))
        if p.get('note'):
            h += f'<div class="vnote tx">{E(p["note"])}</div>'; tl.show(sel('.vnote'), t + .6, .4, 0)

    else:
        raise ValueError(f'unknown visual panel type {k}')
    h += '</div>'
    tl.hide(f'#{pid}', t_end - .35, .3)
    return h, tl.js(), [x for x in texts if x[1]], holds
