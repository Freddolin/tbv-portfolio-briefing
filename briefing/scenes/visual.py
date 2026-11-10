"""Visual panels: scenes that show instead of tell. Used when a film has no interview footage and
the voice-over needs pictures: product walkthroughs on real screenshots, notification piles,
skylines, portraits, growth bars, funnels and roadmaps.

Types: notify, skyline, ui, faces, bars, funnel, path, units, stack, origin, loop, pressure, colleague, market, moves.
Same contract as panels.build: returns (html, js, texts, holds)."""
import json
from .base import E, T, TL

TYPES = ('notify', 'skyline', 'ui', 'faces', 'bars', 'funnel', 'path', 'units', 'stack', 'origin', 'loop', 'pressure', 'colleague', 'market', 'moves')

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
    'down': '<path d="M3 6l6 6 4-4 8 8"/><path d="M15 16h6v-6"/>',
}

CURSOR = ('<svg viewBox="0 0 24 24" width="46" height="46" style="position:static;display:block">'
          '<path d="M5 2.5l13.5 12.2-6.1.6 3.6 7.1-2.9 1.4-3.5-7.2-4.6 4.2z" fill="#fff" stroke="#1f1d1c" stroke-width="1.4" stroke-linejoin="round"/></svg>')

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
.ucd .k{font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;color:#7d7873}
.ucd .hh{font-size:36px;letter-spacing:-.025em;color:#1f1d1c;margin-top:10px;line-height:1.12}
.ucd .r{display:flex;align-items:center;gap:16px;font-size:26px;font-weight:400;color:#3a3634;margin-top:18px}
.ucd .r span.s{margin-left:auto;font-size:21px;font-weight:600;letter-spacing:.04em;padding:6px 14px;border-radius:20px;background:#e5efdc;color:#2f5a1d}
.ucd .btn{display:inline-block;margin-top:28px;font-size:26px;padding:16px 34px;border-radius:40px;background:#0d1d00;color:#fff}
.ucd .btn.ok{background:#2f7a1d}
.ucd .r svg{color:#EF7619}
.ftx{text-align:center}
.fc .ph2{left:0;top:0;border-radius:18px;object-fit:cover;filter:grayscale(1) contrast(1.08)}
.fc .n{left:0;font-size:30px;letter-spacing:-.025em;white-space:nowrap}
.fc .r{left:0;font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap}
.br{transform-origin:50% 100%;border-radius:12px 12px 0 0}
.bv{font-size:72px;letter-spacing:-.04em;line-height:1;white-space:nowrap;text-align:center}
.bl2{font-size:28px;font-weight:400;white-space:nowrap;text-align:center}
.bs{font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap;text-align:center;color:var(--orange)}
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

/* shared: big statement in the left column, visual on the right */
.vbig{left:110px;width:860px;font-size:92px;letter-spacing:-.045em;line-height:1.04}
.vcard{border-radius:22px;background:#F5F5F5;box-shadow:0 30px 70px rgba(0,0,0,.45)}
.vcard .k{left:34px;top:28px;font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;color:#7d7873}
.vcard .tt{left:34px;top:62px;font-size:40px;letter-spacing:-.025em;color:#1f1d1c;white-space:nowrap}
.vchip{font-weight:600;font-size:21px;letter-spacing:.08em;text-transform:uppercase;padding:9px 16px;border-radius:22px;white-space:nowrap}
.vdark{border-radius:22px;background:rgba(245,245,245,.05);border:1.5px solid rgba(245,245,245,.25)}
/* pressure */
.jbn{font-size:150px;letter-spacing:-.05em;line-height:1;color:#1f1d1c}
.jbl{font-size:30px;font-weight:400;color:#4a4643;white-space:nowrap}
.mlab{font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap}
/* colleague */
.twin{width:560px;height:96px;border-radius:16px;background:#F5F5F5;box-shadow:0 22px 44px rgba(0,0,0,.38);color:#282524}
.twin .ic{left:24px;top:24px}
.twin .l{left:84px;top:30px;font-size:30px;white-space:nowrap;color:#282524}
.twin .x{right:22px;top:30px;width:36px;height:36px;border-radius:50%;background:#ECE9E4}
.trow{left:30px;width:690px;height:96px;border-radius:16px}
.trow .av{left:16px;top:14px;width:68px;height:68px;border-radius:50%;background:#4a4643;color:#F5F5F5;font-size:24px;text-align:center;line-height:68px}
.trow .av svg{position:absolute !important;left:14px;top:14px}
.trow .r1{left:106px;top:16px;font-size:32px;letter-spacing:-.015em;white-space:nowrap;color:#F5F5F5}
.trow .r2{left:106px;top:56px;font-size:22px;font-weight:400;white-space:nowrap;color:#a9a39d}
.trow.w{background:rgba(239,118,25,.14);border:2px solid #EF7619}
.trow.w .av{background:#0d1d00}
.trow .on{right:22px;top:30px}
/* market */
.mkv{left:104px;top:300px;font-size:200px;letter-spacing:-.055em;line-height:1;white-space:nowrap}
.mkl{left:110px;top:540px;width:760px;font-size:34px;font-weight:400;line-height:1.25}
.mkr{left:110px;width:800px;height:76px}
.mkr .ic{left:0;top:6px;width:60px;height:60px;border-radius:14px;border:1.5px solid #EF7619;color:#EF7619}
.mkr .ic svg{position:absolute !important;left:12px;top:12px}
.mkr .a{left:84px;top:2px;font-size:32px;letter-spacing:-.015em;white-space:nowrap}
.mkr .b{left:84px;top:42px;font-size:24px;font-weight:400;white-space:nowrap}
.mkc{font-weight:600;font-size:22px;letter-spacing:.08em;text-transform:uppercase;padding:10px 18px;border-radius:24px;border:1.5px solid rgba(245,245,245,.5);color:#F5F5F5;background:var(--dark);white-space:nowrap}
.mkin{text-align:center;color:#1f1d1c;font-size:26px;line-height:1.15;letter-spacing:-.01em}
/* moves */
.mv{border-radius:22px;background:rgba(245,245,245,.05);border:1.5px solid rgba(245,245,245,.22)}
.mv .vz{left:0;top:0;height:250px;border-bottom:1.5px solid rgba(245,245,245,.14)}
.mv .n{left:34px;top:282px;font-weight:600;font-size:22px;letter-spacing:.06em;color:var(--orange)}
.mv .t{left:34px;top:318px;font-size:42px;letter-spacing:-.03em;white-space:nowrap}
.mv .d{left:34px;top:376px;font-size:27px;font-weight:400;line-height:1.3}
.mpill{height:70px;line-height:70px;padding:0 30px;border-radius:40px;font-size:30px;white-space:nowrap}
.mic{width:96px;height:96px;border-radius:24px;border:1.5px solid rgba(245,245,245,.45);color:#F5F5F5}
.mic svg{position:absolute !important;left:20px;top:20px}
.mic.o{border-color:#EF7619;color:#EF7619;background:rgba(239,118,25,.1)}
.mcoin{width:120px;height:30px;border-radius:50%;background:#EF7619;border:2px solid #b8560c}
.mseat{width:76px;height:76px;border-radius:50%;background:#4a4643;color:#F5F5F5}
.mseat svg{position:absolute !important;left:16px;top:16px}
.mrn{width:76px;height:76px;border-radius:50%;text-align:center;line-height:76px;font-size:21px;font-weight:600;letter-spacing:0}
.mrn.tb{background:#F5F5F5;color:#1f1d1c}
.mrn.o{background:#EF7619;color:#1f1d1c}
.mrn.o svg{position:absolute !important;left:16px;top:16px}
.mrl{font-weight:600;font-size:17px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap;text-align:center}
.mseat.e{background:transparent;border:2.5px dashed #EF7619;color:#EF7619;font-size:44px;text-align:center;line-height:68px}

.ucur{width:46px;height:46px;z-index:5}
/* stack: the product as a building, floor by floor */
.skt{left:110px;top:300px;width:820px;font-size:96px;letter-spacing:-.045em;line-height:1.04}
.sks{left:110px;width:800px;font-size:40px;font-weight:400;line-height:1.25}
.skf{border-radius:16px;border:2px dashed rgba(245,245,245,.42);background:rgba(245,245,245,.035)}
.skf.live{border:2px solid #EF7619;background:rgba(239,118,25,.13)}
.skf .ic{left:26px;width:64px;height:64px;border-radius:15px;border:1.5px solid rgba(245,245,245,.4);color:#F5F5F5}
.skf.live .ic{border-color:#EF7619;color:#EF7619}
.skf .ic svg{position:absolute !important;left:13px;top:13px}
.skf .t1{left:116px;font-size:36px;letter-spacing:-.02em;white-space:nowrap;color:#F5F5F5}
.skf .t2{left:116px;font-size:24px;font-weight:400;white-space:nowrap;color:#a9a39d}
.skf .tg{right:26px;font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap;padding:8px 14px;border-radius:20px;border:1.5px solid rgba(245,245,245,.4);color:#cfcbc6}
.skf.live .tg{background:#EF7619;border-color:#EF7619;color:#1f1d1c}
/* origin: two partners bring a problem to the studio */
.oav{width:116px;height:116px;border-radius:50%;background:#3a3634;border:2px solid rgba(245,245,245,.35);color:#F5F5F5;font-size:40px;letter-spacing:-.02em;text-align:center;line-height:112px}
.onm{font-size:40px;letter-spacing:-.025em;white-space:nowrap}
.orl{font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap;line-height:1.35}
.opb{width:600px;border-radius:22px;background:#F5F5F5;box-shadow:0 30px 70px rgba(0,0,0,.45)}
.opb .k{left:36px;top:30px;font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;color:#c0392b}
.opb .tt{left:36px;top:66px;width:530px;font-size:40px;letter-spacing:-.025em;line-height:1.12;color:#1f1d1c}
.opb .r2{left:36px;font-size:27px;font-weight:400;color:#4a4643;width:530px;line-height:1.25}
.otb{border-radius:22px;border:2px solid #EF7619;background:rgba(239,118,25,.08)}
.otb .k{left:0;width:100%;text-align:center;font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;color:#EF7619}
/* loop: build, test, validate */
.lpn{width:30px;height:30px;border-radius:50%;border:4px solid #EF7619;background:var(--dark)}
.lpn.on{background:#EF7619}
.lpl{font-size:34px;letter-spacing:-.02em;white-space:nowrap;line-height:1.1}
#stage .lpl small{display:block;position:static;font-size:23px;font-weight:400;color:#a9a39d;letter-spacing:0;margin-top:6px}
.lav{filter:grayscale(1) contrast(1.08);width:104px;height:104px;border-radius:50%;object-fit:cover;border:3px solid var(--dark)}
.lwf{border-radius:16px;background:#33302e;border:1.5px solid rgba(245,245,245,.3);box-shadow:0 24px 50px rgba(0,0,0,.4)}
.lwf i{background:rgba(245,245,245,.16);border-radius:6px}
.lwf .lk{left:22px;top:14px;font-weight:600;font-size:21px;letter-spacing:.09em;text-transform:uppercase;color:#cfcbc6}
.lsh{border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.lcap{font-size:52px;letter-spacing:-.035em;line-height:1.08;white-space:nowrap}
/* funnel: a real funnel, values inside, labels outside */
.fnv{font-size:66px;letter-spacing:-.04em;line-height:1;white-space:nowrap;text-align:center}
.fnl{font-size:38px;letter-spacing:-.02em;white-space:nowrap}
.fns{font-size:27px;font-weight:400;white-space:nowrap}
.dk .fnk{background:rgba(245,245,245,.35)}
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
            texts.append((t, f"{p['items'][i]['title']} {p['items'][i].get('meta', '')}"))
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
            events.append((t, s_.get('at'), move + (2.4 if (s_.get('box') or s_.get('label')) else .2)))
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
                   f'<div class="btn ok b2" style="position:absolute;opacity:0">{E(o.get("done", "Done"))}</div>'
                   + (f'<div class="ucur" style="position:absolute;left:96px;top:58px;opacity:0">{CURSOR}</div>' if o.get('click_at') is not None else '')
                   + '</div>') if o.get('button') else ''
            h += (f'<div class="ucd uo{j} h" style="left:{ox}px;top:{oy}px"><div class="k">{E(o.get("kicker", ""))}</div>'
                  f'<div class="hh">{E(o.get("title", ""))}</div>{rows}{btn}</div>')
            tl(f"tl.fromTo('#{pid} .uo{j}',{{autoAlpha:0,x:60}},{{autoAlpha:1,x:0,duration:.5,ease:'power3.out'}},{t - .1:.3f});")
            r_ts = _times(o, len(o.get('rows', [])), T0, t + .35, te, key='row_at', gap=.35) if o.get('row_at') else [t + .35 + r_i * .35 for r_i in range(len(o.get('rows', [])))]
            for r_i, tr in enumerate(r_ts):
                tl(f"tl.fromTo(document.querySelectorAll('#{pid} .uo{j} .r')[{r_i}],{{opacity:0,x:-10}},{{opacity:1,x:0,duration:.3}},{tr - .05:.3f});")
            texts.append((t, f'{o.get("title", "")} ' + ' '.join(r_['text'] for r_ in o.get('rows', []))))
            nrows = len(o.get('rows', []))
            events.append((t, o['at'], .35 + nrows * .35 + (.8 if o.get('click_at') is not None else 2.3)))
            if o.get('click_at') is not None: events.append((T0(o['click_at']), o['click_at'], 2.4))
            if o.get('button') and o.get('click_at') is not None:
                tc = T0(o['click_at'])
                tl(f"tl.fromTo('#{pid} .uo{j} .ucur',{{opacity:0,x:260,y:170}},{{opacity:1,x:0,y:0,duration:.75,ease:'power2.inOut'}},{tc - .8:.3f});")
                tl(f"tl.to('#{pid} .uo{j} .ucur',{{scale:.85,duration:.1,yoyo:true,repeat:1}},{tc - .02:.3f});")
                tl(f"tl.to('#{pid} .uo{j} .ucur',{{opacity:0,x:40,y:60,duration:.4}},{tc + 1.2:.3f});")
                tl(f"tl.to('#{pid} .uo{j} .b1',{{scale:.92,duration:.12,yoyo:true,repeat:1}},{tc:.3f});")
                tl(f"tl.to('#{pid} .uo{j} .b1',{{opacity:0,duration:.15}},{tc + .24:.3f});")
                tl(f"tl.fromTo('#{pid} .uo{j} .b2',{{opacity:0,scale:.9}},{{opacity:1,scale:1,duration:.3,ease:'back.out(2)'}},{tc + .24:.3f});")
                texts.append((tc + .24, o.get('done', 'Done')))
            if te < t_end - .4: tl.hide(sel(f'.uo{j}'), te - .3, .3)
        events.sort(key=lambda e: e[0])
        for (ta_, a_, need), (tb_, b_, _) in zip(events, events[1:]):
            if b_ is not None and b_ != a_ and tb_ - ta_ < need - .05: holds.append((b_, round(need - (tb_ - ta_), 2)))

    elif k == 'faces':
        n = len(p['items']); gap = 40; w = (1700 - gap * (n - 1)) / n; ph = min(460, w * 1.36)
        top = 300 if p.get('head') else 250
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

    elif k == 'funnel':                      # a real funnel: stages narrow downwards, value inside, label outside
        n = len(p['items']); vmax = max(float(it['value']) for it in p['items'])
        top0 = 310 if p.get('head') else 220; sh = p.get('stage_h', 168); gap = 14; cx = p.get('cx', 660)
        wmax, wmin = 1100, 360
        ws = [wmin + (wmax - wmin) * (float(it['value']) / vmax) ** .6 for it in p['items']]
        ws.append(ws[-1] * .62)
        svg = '<svg class="vx" viewBox="0 0 1920 1080">'
        lab = ''
        for i, it in enumerate(p['items']):
            y = top0 + i * (sh + gap); a, b_ = ws[i] / 2, ws[i + 1] / 2
            last = i == n - 1 and p.get('accent_last', True)
            col = '#EF7619' if last else ('rgba(245,245,245,.92)' if i == 0 else 'rgba(245,245,245,.78)')
            svg += f'<path class="fnp fnp{i}" fill="{col}" d="M{cx - a:.0f} {y}H{cx + a:.0f}L{cx + b_:.0f} {y + sh}H{cx - b_:.0f}Z"/>'
            tcol = '#1f1d1c'
            lab += f'<div class="fnv fnv{i}" style="left:{cx - 200}px;width:400px;top:{y + sh / 2 - 34:.0f}px;color:{tcol}">{E(it.get("display", it["value"]))}</div>'
            lx = cx + wmax / 2 + 90
            lab += (f'<div class="hair fnk fnk{i}" style="left:{cx + a + 24:.0f}px;top:{y + sh / 2:.0f}px;width:{lx - cx - a - 48:.0f}px"></div>'
                    f'<div class="fnl tx fnl{i}" style="left:{lx:.0f}px;top:{y + sh / 2 - (40 if it.get("sub") else 22):.0f}px">{E(it["label"])}</div>')
            if it.get('sub'): lab += f'<div class="fns sb fns{i}" style="left:{lx:.0f}px;top:{y + sh / 2 + 12:.0f}px">{E(it["sub"])}</div>'
        svg += '</svg>'
        h += svg + lab
        for i, t in enumerate(_times(p, n, T0, t_start, t_end)):
            it = p['items'][i]
            tl(f"tl.fromTo('#{pid} .fnp{i}',{{autoAlpha:0,y:-30}},{{autoAlpha:1,y:0,duration:.55,ease:'power3.out'}},{t - .15:.3f});")
            tl.show(sel(f'.fnv{i}'), t + .1, .35, 0)
            tl(f"count('#{pid} .fnv{i}',{t + .1:.3f},{float(it['value'])},.8,n=>(n>={float(it['value']) - .5}?{json.dumps(str(it.get('display', it['value'])))}:Math.round(n).toLocaleString('en-US')));")
            tl.grow(sel(f'.fnk{i}'), t + .2, .4); tl.show(sel(f'.fnl{i}'), t + .3, .35, 0)
            texts.append((t + .3, f"{it.get('display', it['value'])} {it['label']}"))
            if it.get('sub'):
                ts_ = T0(it['sub_at']) if it.get('sub_at') is not None else t + .8
                tl.show(sel(f'.fns{i}'), ts_, .35, 0); texts.append((ts_, it['sub']))
        if p.get('note'):
            h += f'<div class="vnote tx">{E(p["note"])}</div>'; tl.show(sel('.vnote'), t_start + .5, .4, 0)

    elif k == 'path':
        n = len(p['items']); y = 600 if p.get('head') else 540; x0, x1 = 300, 1620
        if p.get('sub'):
            h += f'<div class="psub sb pathsub" style="top:276px;font-size:34px">{T(p["sub"])}</div>'
            tsub = T0(p['sub_at']) if p.get('sub_at') is not None else t_start + .4
            tl.show(sel('.pathsub'), tsub, .45, 10); texts.append((tsub, p['sub']))
            y += 40
        if n == 1: x0 = x1 = 960
        dx = (x1 - x0) / max(1, n - 1); cw = min(560, dx - 40) if n > 1 else 700
        h += f'<div class="hair pline pl0" style="left:{x0 - 140}px;top:{y}px;width:{x1 - x0 + 280}px;height:2px"></div>'
        tfs = 46 if n <= 3 else 40                      # title size; long titles wrap, the text moves down with them
        for i, it in enumerate(p['items']):
            x = x0 + dx * i
            lines = sum(max(1, -(-int(len(part) * tfs * .5) // int(cw))) for part in str(it['title']).split('<br>'))
            h += (f'<div class="pnode pn{i}" style="left:{x - 14:.0f}px;top:{y - 13}px"></div>'
                  f'<div class="pic pc{i}" style="left:{x - 64:.0f}px;top:{y - 196}px">{icon(it.get("icon", "check"), 72, "currentColor", 1.4)}</div>'
                  f'<div class="pt tx pt{i}" style="left:{x - cw / 2:.0f}px;width:{cw:.0f}px;top:{y + 52}px;font-size:{tfs}px">{T(it["title"])}</div>'
                  f'<div class="pd sb pd{i}" style="left:{x - cw / 2:.0f}px;width:{cw:.0f}px;top:{y + 60 + int(tfs * 1.12) * lines}px">{T(it.get("text", ""))}</div>')
        tl.grow(sel('.pl0'), t_start + .1, 1.2)
        for i, t in enumerate(_times(p, n, T0, t_start, t_end)):
            tl(f"tl.fromTo('#{pid} .pn{i}',{{autoAlpha:0,scale:0}},{{autoAlpha:1,scale:1,duration:.4,ease:'back.out(2)'}},{t - .15:.3f});")
            tl.show(sel(f'.pc{i}'), t - .05, .45, 18); tl.show(sel(f'.pt{i}'), t + .05, .4, 10); tl.show(sel(f'.pd{i}'), t + .2, .4, 10)
            texts.append((t + .05, f"{p['items'][i]['title']} {p['items'][i].get('text', '')}"))

    elif k == 'units':                       # a big number and a grid of buildings filling up (one icon per `per` units)
        n = int(round(float(p['value']) / float(p.get('per', 100)))); cols = p.get('cols', 8); sz = p.get('icon_size', 92); gap = p.get('gap', 26)
        gx = 1810 - cols * sz - (cols - 1) * gap; gy = 300
        h += (f'<div class="sv tx uvn h" style="left:104px;top:330px">0</div>'
              f'<div class="st2 sb uvl" style="top:600px;width:760px">{T(p.get("label", ""))}</div>')
        for i in range(n):
            r, c_ = divmod(i, cols)
            h += f'<div class="ug ug{i}" style="left:{gx + c_ * (sz + gap)}px;top:{gy + r * (sz + gap)}px;width:{sz}px;height:{sz}px;color:{"#EF7619" if i == n - 1 else "#F5F5F5"}">{icon("building", sz, "currentColor", 1.3 if sz > 60 else 1.6)}</div>'
        t = T0(p['value_at']) if p.get('value_at') is not None else t_start + .3
        tl.show(sel('.uvn'), t - .1, .3, 0)
        disp = json.dumps(p.get('display', ''))
        tl(f"count('#{pid} .uvn',{t:.3f},{float(p['value'])},1.6,n=>(n>={float(p['value']) - .5}&&{disp})?{disp}:Math.round(n).toLocaleString('en-US'));")
        tl(f"tl.fromTo('#{pid} .ug',{{autoAlpha:0,scale:.6}},{{autoAlpha:1,scale:1,duration:.3,ease:'back.out(2)',stagger:{1.5 / max(1, n):.3f}}},{t:.3f});")
        tl.show(sel('.uvl'), t + .5, .4, 10); texts.append((t + .5, p.get('label', '')))
        if p.get('extra'):
            h += f'<div class="uvx tx" style="left:110px;top:720px;width:760px;font-size:44px;letter-spacing:-.02em;line-height:1.15">{T(p["extra"])}</div>'
            tx_ = T0(p['extra_at']) if p.get('extra_at') is not None else t + 1.4
            tl.show(sel('.uvx'), tx_, .45, 12); texts.append((tx_, p['extra']))
        if p.get('note'):
            h += f'<div class="vnote tx">{E(p["note"])}</div>'; tl.show(sel('.vnote'), t + .6, .4, 0)


    elif k == 'stack':                       # version one as the ground floor, the roadmap builds the house on top
        fl = p['floors']; n = len(fl)
        base = 930; fh = 132; g = 14; x0 = p.get('x', 1010); w = 1810 - x0
        h += f'<div class="skt tx">{T(p["text"])}</div>'
        ty = 300 + 100 * (str(p['text']).count('<br>') + 1) + 40
        for j, (sk, ak) in enumerate((('sub', 'sub_at'), ('sub2', 'sub2_at'))):
            if p.get(sk):
                cls = 'tx' if j else 'sb'
                h += f'<div class="sks {cls} sks{j}" style="top:{ty}px">{T(p[sk])}</div>'
                ty += 52 * (len(str(p[sk])) // 46 + 1) + 14
        svg = f'<svg class="vx" viewBox="0 0 1920 1080" fill="none"><path class="d skg" stroke="rgba(245,245,245,.6)" stroke-width="2.5" d="M{x0 - 40} {base}H1850"/>'
        ytop = base - n * (fh + g)
        svg += f'<path class="d skr" stroke="#EF7619" stroke-width="3" stroke-linejoin="round" d="M{x0 - 10} {ytop + 4}L{x0 + w / 2:.0f} {ytop - 96}L{1820} {ytop + 4}"/></svg>'
        h += svg
        if p.get('roof'):
            h += f'<div class="cap skrl" style="left:{x0}px;width:{w}px;top:{ytop - 140}px;text-align:center;color:var(--orange)">{E(p["roof"])}</div>'
        for i, f_ in enumerate(fl):
            y = base - (i + 1) * (fh + g) + g
            live = ' live' if f_.get('live') else ''
            h += (f'<div class="skf{live} skf{i}" style="left:{x0}px;top:{y}px;width:{w}px;height:{fh}px">'
                  f'<div class="ic" style="top:{(fh - 64) / 2:.0f}px">{icon(f_.get("icon", "building"), 38, "currentColor", 1.6)}</div>'
                  f'<div class="t1" style="top:{fh / 2 - 40:.0f}px">{E(f_["title"])}</div>'
                  f'<div class="t2" style="top:{fh / 2 + 8:.0f}px">{E(f_.get("text", ""))}</div>'
                  f'<div class="tg" style="top:{fh / 2 - 20:.0f}px">{E(f_.get("tag", "Roadmap"))}</div></div>')
        tl.show(sel('.skt'), t_start + .1, .6); texts.append((t_start + .1, p['text']))
        tl.draw(sel('.skg'), t_start + .05, .7)
        later = [i for i, f_ in enumerate(fl) if not f_.get('live')]
        ts = _times(p, len(later), T0, t_start, t_end)
        live_i = next((i for i, f_ in enumerate(fl) if f_.get('live')), -1)
        for i, f_ in enumerate(fl):
            if f_.get('live'):
                tl(f"tl.fromTo('#{pid} .skf{i}',{{autoAlpha:0,y:40}},{{autoAlpha:1,y:0,duration:.6,ease:'power3.out'}},{t_start + .35:.3f});")
                texts.append((t_start + .35, f"{f_['title']} {f_.get('text', '')}"))
                if p.get('pulse_at') is not None:
                    tl(f"tl.to('#{pid} .skf{i}',{{scale:1.03,duration:.25,yoyo:true,repeat:1,ease:'power1.inOut'}},{T0(p['pulse_at']):.3f});")
        for i, t in zip(later, ts):
            dy = 70 if i < live_i else -70          # floors below the live one rise up, floors above drop in
            tl(f"tl.fromTo('#{pid} .skf{i}',{{autoAlpha:0,y:{dy}}},{{autoAlpha:1,y:0,duration:.55,ease:'power3.out'}},{t - .15:.3f});")
            texts.append((t, f"{fl[i]['title']} {fl[i].get('text', '')}"))
        tr = T0(p['roof_at']) if p.get('roof_at') is not None else (max(ts) + .3 if ts else t_start + 1)
        tl.draw(sel('.skr'), tr - .1, .7)
        if p.get('roof'): tl.show(sel('.skrl'), tr + .3, .4, 8); texts.append((tr + .3, p['roof']))
        for j, (sk, ak) in enumerate((('sub', 'sub_at'), ('sub2', 'sub2_at'))):
            if p.get(sk):
                tsb = T0(p[ak]) if p.get(ak) is not None else t_start + 1 + j
                tl.show(sel(f'.sks{j}'), tsb, .5, 10); texts.append((tsb, p[sk]))

    elif k == 'origin':                      # two partners spot a problem and bring it to the studio
        ppl = p['people']; pr = p['problem']
        for i, pe in enumerate(ppl):
            y = 390 + i * 200
            ini = ''.join(w_[0] for w_ in pe['name'].split()[:2])
            h += (f'<div class="og og{i}" style="left:110px;top:{y}px;width:640px;height:150px">'
                  f'<div class="oav">{E(ini)}</div><div class="onm tx" style="left:150px;top:18px">{E(pe["name"])}</div>'
                  f'<div class="orl sb" style="left:152px;top:72px">{T(pe.get("role", ""))}</div></div>')
        px, py = 690, 390
        h += (f'<div class="opb" style="left:{px}px;top:{py}px;height:380px"><div class="k">{E(pr.get("kicker", "The problem"))}</div>'
              f'<div class="tt">{T(pr["title"])}</div>'
              f'<svg class="opc" style="left:36px;top:206px" width="300" height="120" viewBox="0 0 300 120" fill="none">'
              f'<path d="M0 118H300" stroke="#c9c5bf" stroke-width="2"/>'
              f'<path class="d opl" d="M4 20C60 24 90 40 130 52S210 92 296 104" stroke="#c0392b" stroke-width="5" stroke-linecap="round"/></svg>'
              f'<div class="sb" style="left:36px;top:330px;font-size:20px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:#7d7873">{E(pr.get("chart", "Margin"))}</div>'
              f'<div class="r2" style="left:360px;top:214px;width:210px">{T(pr.get("text", ""))}</div></div>')
        bx, by, bw, bh = 1400, 420, 410, 320
        h += (f'<div class="otb" style="left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px">'
              f'<img src="assets/img/tbv_h_alpha.png" style="left:{(bw - 340) / 2:.0f}px;top:{bh / 2 - 46:.0f}px;width:340px;height:46px">'
              f'<div class="k" style="top:{bh / 2 + 30:.0f}px">{E(p.get("to_caption", "Studio · Build First"))}</div></div>')
        h += (f'<svg class="vx" viewBox="0 0 1920 1080" fill="none">'
              f'<path class="d oa1" stroke="#EF7619" stroke-width="3" d="M{px + 610} {py + 190}H{bx - 18}"/>'
              f'<path class="d oa2" stroke="#EF7619" stroke-width="3" stroke-linejoin="round" d="M{bx - 34} {py + 174}L{bx - 16} {py + 190}L{bx - 34} {py + 206}"/></svg>')
        tp = _times(p, len(ppl), T0, t_start, t_end, key='people_at')
        for i, t in enumerate(tp):
            tl(f"tl.fromTo('#{pid} .og{i}',{{autoAlpha:0,x:-40}},{{autoAlpha:1,x:0,duration:.5,ease:'power3.out'}},{t - .1:.3f});")
            texts.append((t, f"{ppl[i]['name']} {ppl[i].get('role', '')}"))
        tq = T0(pr['at']) if pr.get('at') is not None else tp[-1] + 1
        tl(f"tl.fromTo('#{pid} .opb',{{autoAlpha:0,y:50,rotation:-1.5}},{{autoAlpha:1,y:0,rotation:0,duration:.55,ease:'back.out(1.4)'}},{tq - .1:.3f});")
        tl.draw(sel('.opl'), tq + .4, 1.4); texts.append((tq, pr['title']))
        if pr.get('text'):
            h = h.replace('<div class="r2"', '<div class="r2 opr"', 1)
            tr = T0(pr['text_at']) if pr.get('text_at') is not None else tq + 1.2
            tl.show(sel('.opr'), tr, .4, 8); texts.append((tr, pr['text']))
        tt = T0(p['to_at']) if p.get('to_at') is not None else tq + 3
        tl(f"tl.fromTo('#{pid} .otb',{{autoAlpha:0,scale:.92}},{{autoAlpha:1,scale:1,duration:.5,ease:'back.out(1.6)'}},{tt - .5:.3f});")
        texts.append((tt - .5, 'The Bau Ventures'))
        tl.draw(sel('.oa1'), tt - .1, .5); tl.draw(sel('.oa2'), tt + .35, .2)
        tl(f"tl.to('#{pid} .og',{{opacity:.45,duration:.5}},{tt + .1:.3f});")
        tl(f"tl.to('#{pid} .opb',{{x:{bx + bw / 2 - px - 300:.0f},scale:.5,autoAlpha:0,duration:.8,ease:'power2.in'}},{tt + .6:.3f});")
        tl(f"tl.to('#{pid} .oa1,#{pid} .oa2',{{opacity:0,duration:.3}},{tt + 1.1:.3f});")
        tl(f"tl.to('#{pid} .otb',{{boxShadow:'0 0 0 10px rgba(239,118,25,.18)',duration:.35,yoyo:true,repeat:1}},{tt + 1.3:.3f});")

    elif k == 'loop':                        # build, test, validate in a loop; prototypes turn into the real product
        cx, cy, R = p.get('cx', 590), p.get('cy', 600), p.get('r', 250)
        nodes = p['nodes']; nn = len(nodes)
        import math
        svg = (f'<svg class="vx" viewBox="0 0 1920 1080" fill="none">'
               f'<circle class="d lpc" cx="{cx}" cy="{cy}" r="{R}" stroke="rgba(245,245,245,.35)" stroke-width="3" transform="rotate(-90 {cx} {cy})"/>'
               f'<g class="lpd"><circle cx="{cx}" cy="{cy - R}" r="11" fill="#EF7619"/></g></svg>')
        h += svg
        angs = [-90 + 360 * i / nn for i in range(nn)]
        for i, (nd, a) in enumerate(zip(nodes, angs)):
            x = cx + R * math.cos(math.radians(a)); y = cy + R * math.sin(math.radians(a))
            h += f'<div class="lpn lpn{i}" style="left:{x - 15:.0f}px;top:{y - 15:.0f}px"></div>'
            if a < -60: lx, ly, al = x - 300, y - 112, 'center'
            elif math.cos(math.radians(a)) > 0: lx, ly, al = x + 34, y - 10, 'left'
            else: lx, ly, al = x - 634, y - 10, 'right'
            h += f'<div class="lpl tx lpl{i}" style="left:{lx:.0f}px;top:{ly:.0f}px;width:600px;text-align:{al}">{E(nd["title"])}<small>{E(nd.get("text", ""))}</small></div>'
        h += f'<div class="cap lpk" style="left:{cx - 200}px;width:400px;top:{cy - 104}px;text-align:center;color:var(--orange)">{E(p.get("center", "Build First"))}</div>'
        for i, ph in enumerate(p.get('team', [])):
            h += f'<img class="lav lav{i}" src="{ph}" style="left:{cx - 104 + i * 104 - 14 * i:.0f}px;top:{cy - 54}px">'
        if p.get('team_caption'):
            h += f'<div class="sb lavc" style="left:{cx - 200}px;width:400px;top:{cy + 66}px;text-align:center;font-size:24px;font-weight:400">{E(p["team_caption"])}</div>'
        wx, wy, ww, wh = 1140, 320, 600, 390
        nps = p.get('prototypes', 3)
        for i in range(nps):
            ox, oy = wx + 22 * i, wy + 50 * i
            bars = ''.join(f'<i style="left:{180 + (j % 2) * 10}px;top:{110 + j * 46}px;width:{360 - j * 40 - i * 20}px;height:22px"></i>' for j in range(4))
            h += (f'<div class="lwf lwf{i}" style="left:{ox}px;top:{oy}px;width:{ww}px;height:{wh}px">'
                  f'<i style="left:22px;top:56px;width:130px;height:{wh - 80}px"></i><i style="left:180px;top:56px;width:{ww - 210}px;height:30px;background:rgba(239,118,25,.35)"></i>{bars}'
                  f'<div class="lk">{E(p.get("proto_label", "Prototype"))} {i + 1}</div></div>')
        fin = p.get('final')
        if fin:
            v = fin.get('view'); sz = fin['size']; FW, FH = 690, 440
            sc_ = FW / v[2]
            h += (f'<div class="lsh" style="left:1120px;top:340px;width:{FW}px;height:{FH}px"><div style="left:0;top:0;width:{FW}px;height:30px;background:#e9e7e3"></div>'
                  f'<img src="{fin["src"]}" style="left:{-v[0] * sc_:.0f}px;top:{30 - v[1] * sc_:.0f}px;width:{sz[0] * sc_:.0f}px;height:{sz[1] * sc_:.0f}px"></div>')
            h += f'<div class="lcap tx" style="left:1120px;top:220px">{T(fin.get("caption", ""))}</div>'
            if fin.get('tag'): h += f'<div class="cap ltag" style="left:1120px;top:812px;color:var(--orange)">{E(fin["tag"])}</div>'
        tl.draw(sel('.lpc'), t_start + .05, .7)
        tl.show(sel('.lpk'), t_start + .1, .4, 0); texts.append((t_start + .3, p.get('center', 'Build First')))
        tl(f"tl.fromTo('#{pid} .lpd',{{autoAlpha:0}},{{autoAlpha:1,duration:.3}},{t_start + 1.0:.3f});")
        spin_d = max(1.0, t_end - t_start - 1.0)
        tl(f"tl.fromTo('#{pid} .lpd',{{rotation:0,svgOrigin:'{cx} {cy}'}},{{rotation:{360 * max(1, round(spin_d / 3.2))},svgOrigin:'{cx} {cy}',duration:{spin_d:.2f},ease:'none'}},{t_start + 1.0:.3f});")
        if p.get('team'):
            tt = T0(p['team_at']) if p.get('team_at') is not None else t_start + .6
            tl(f"tl.fromTo('#{pid} .lav',{{autoAlpha:0,scale:.7}},{{autoAlpha:1,scale:1,duration:.45,ease:'back.out(1.8)',stagger:.15}},{tt - .1:.3f});")
            if p.get('team_caption'): tl.show(sel('.lavc'), tt + .3, .4, 6); texts.append((tt + .3, p['team_caption']))
        tn = _times(p, nn, T0, t_start + .8, t_end, key='node_at')
        for i, t in enumerate(tn):
            tl(f"tl.fromTo('#{pid} .lpn{i}',{{autoAlpha:0,scale:0}},{{autoAlpha:1,scale:1,duration:.35,ease:'back.out(2)'}},{t - .15:.3f});")
            tl(f"tl.to('#{pid} .lpn{i}',{{backgroundColor:'#EF7619',duration:.3}},{t + .2:.3f});")
            tl.show(sel(f'.lpl{i}'), t, .4, 8); texts.append((t, f"{nodes[i]['title']} {nodes[i].get('text', '')}"))
            if i < nps:
                tl(f"tl.fromTo('#{pid} .lwf{i}',{{autoAlpha:0,y:30,rotation:{(-2, 1.5, -1)[i % 3]}}},{{autoAlpha:1,y:0,rotation:0,duration:.5,ease:'power3.out'}},{t + .1:.3f});")
        if fin:
            tf = T0(fin['at']) if fin.get('at') is not None else tn[-1] + 1.5
            tl(f"tl.to('#{pid} .lwf',{{autoAlpha:0,y:-20,duration:.4,stagger:.06}},{tf - .3:.3f});")
            tl(f"tl.fromTo('#{pid} .lsh',{{autoAlpha:0,y:60,scale:.94}},{{autoAlpha:1,y:0,scale:1,duration:.7,ease:'power3.out'}},{tf:.3f});")
            tl.show(sel('.lcap'), tf + .1, .5, 12); texts.append((tf + .1, fin.get('caption', '')))
            if fin.get('tag'):
                tg = T0(fin['tag_at']) if fin.get('tag_at') is not None else tf + .8
                tl.show(sel('.ltag'), tg, .4, 8); texts.append((tg, fin['tag']))


    elif k == 'pressure':                    # statement left; right: a job ad nobody fills, then margins squeezed
        lines = str(p['text']).count('<br>') + 1
        h += f'<div class="vbig tx vb0" style="top:330px">{T(p["text"])}</div>'
        y2 = 330 + int(92 * 1.04 * lines) + 70
        if p.get('text2'): h += f'<div class="vbig tx vb1" style="top:{y2}px">{T(p["text2"])}</div>'
        job = p.get('job') or {}
        h += (f'<div class="vcard pj" style="left:1060px;top:200px;width:750px;height:310px"><div class="k">{E(job.get("kicker", "Job ad"))}</div>'
              f'<div class="tt">{E(job.get("title", "Property manager"))}</div>'
              f'<div class="jbn pjn" style="left:34px;top:130px">1</div>'
              f'<div class="jbl" style="left:{34 + 110 if job.get("months", 8) < 10 else 34 + 190}px;top:196px">{E(job.get("unit", "months unfilled"))}</div>'
              f'<div class="vchip pjc" style="right:30px;top:32px;background:#fbe1dc;color:#c0392b">{E(job.get("status", "Still open"))}</div></div>')
        W_, H_ = 750, 380
        h += (f'<div class="vcard pm" style="left:1060px;top:560px;width:{W_}px;height:{H_}px"><div class="k">{E(p.get("chart_kicker", "Property management"))}</div>'
              f'<svg style="left:0;top:0" width="{W_}" height="{H_}" viewBox="0 0 {W_} {H_}" fill="none">'
              f'<path d="M50 320H700" stroke="#c9c5bf" stroke-width="2"/>'
              f'<path class="pma" d="M50 150L700 138L700 172L50 262Z" fill="rgba(239,118,25,.22)" opacity="0"/>'
              f'<path class="d pmf" d="M50 150L700 138" stroke="#7d7873" stroke-width="5" stroke-linecap="round"/>'
              f'<path class="d pmc" d="M50 262C220 250 380 222 520 196S650 176 700 172" stroke="#c0392b" stroke-width="5" stroke-linecap="round"/></svg>'
              f'<div class="mlab pml1" style="left:540px;top:96px;color:#7d7873">{E(p.get("fees", "Fees"))}</div>'
              f'<div class="mlab pml2" style="left:560px;top:206px;color:#c0392b">{E(p.get("costs", "Costs"))}</div>'
              f'<div class="mlab pml3" style="left:70px;top:190px;color:#b8560c">{E(p.get("margin", "Margin"))}</div></div>')
        tl.show(sel('.vb0'), t_start + .1, .6); texts.append((t_start + .1, p['text']))
        tj = T0(job['at']) if job.get('at') is not None else t_start + .4
        tl(f"tl.fromTo('#{pid} .pj',{{autoAlpha:0,x:60}},{{autoAlpha:1,x:0,duration:.5,ease:'power3.out'}},{tj:.3f});")
        tl(f"count('#{pid} .pjn',{tj + .3:.3f},{job.get('months', 8)},1.2);")
        tl(f"tl.fromTo('#{pid} .pjc',{{scale:.6,autoAlpha:0}},{{scale:1,autoAlpha:1,duration:.35,ease:'back.out(2)'}},{tj + 1.3:.3f});")
        texts.append((tj, f"{job.get('title', '')} {job.get('unit', '')}"))
        t2 = T0(p['text2_at']) if p.get('text2_at') is not None else t_start + 2
        if p.get('text2'): tl.show(sel('.vb1'), t2, .6); texts.append((t2, p['text2']))
        tl(f"tl.fromTo('#{pid} .pm',{{autoAlpha:0,x:60}},{{autoAlpha:1,x:0,duration:.5,ease:'power3.out'}},{t2 - .2:.3f});")
        tl.draw(sel('.pmf'), t2 + .05, .6); tl.draw(sel('.pmc'), t2 + .15, .8)
        tl(f"tl.to('#{pid} .pma',{{opacity:1,duration:.5}},{t2 + .7:.3f});")
        tl.show(sel('.pml1'), t2 + .4, .3, 0); tl.show(sel('.pml2'), t2 + .55, .3, 0); tl.show(sel('.pml3'), t2 + .6, .4, 0)
        texts.append((t2 + .6, 'Fees Costs Margin'))

    elif k == 'colleague':                   # not another tool on the pile: a new member of the team
        h += f'<div class="vbig tx vb0" style="top:330px">{T(p["text"])}</div>'
        if p.get('text2'): h += f'<div class="vbig tx vb1" style="top:{330 + int(92 * 1.04 * (str(p["text"]).count("<br>") + 1)) + 50}px">{T(p["text2"])}</div>'
        tools = p.get('tools', [])
        for i, tw in enumerate(tools):
            h += (f'<div class="twin tw{i}" style="left:{1150 + (i % 2) * 70}px;top:{250 + i * 112}px;transform:rotate({(-1.5, 1.2, -.8, 1.6, -1)[i % 5]}deg)">'
                  f'<div class="ic">{icon(tw.get("icon", "doc"), 38)}</div><div class="l">{E(tw["label"])}</div><div class="x"></div></div>')
        team = p.get('team', [])
        rows = len(team) + 1
        ch = 120 + rows * 112
        h += (f'<div class="vdark ptm" style="left:1060px;top:{560 - ch / 2:.0f}px;width:750px;height:{ch}px">'
              f'<div class="cap" style="left:30px;top:30px">{E(p.get("team_kicker", "The team"))}</div>')
        for i, m in enumerate(team):
            h += (f'<div class="trow tr{i}" style="top:{84 + i * 112}px"><div class="av">{icon(m.get("icon", "people"), 40)}</div>'
                  f'<div class="r1">{E(m["role"])}</div><div class="r2">{E(m.get("text", ""))}</div></div>')
        wi = len(team)
        h += (f'<div class="trow w tr{wi}" style="top:{84 + wi * 112}px"><div class="av"><img src="{logo_light}" style="left:9px;top:22px;width:50px;height:24px;object-fit:contain"></div>'
              f'<div class="r1">{E(p.get("walter_role", "walter"))}</div><div class="r2">{E(p.get("walter_text", "AI colleague"))}</div>'
              f'<div class="vchip on" style="background:#EF7619;color:#1f1d1c">{E(p.get("walter_tag", "New"))}</div></div></div>')
        tl.show(sel('.vb0'), t_start + .1, .6); texts.append((t_start + .1, p['text']))
        for i in range(len(tools)):
            tl(f"tl.fromTo('#{pid} .tw{i}',{{autoAlpha:0,y:-40}},{{autoAlpha:1,y:0,duration:.35,ease:'back.out(1.6)'}},{t_start + .15 + i * .12:.3f});")
        texts.append((t_start + .15, ' '.join(tw['label'] for tw in tools)))
        tx_ = T0(p['cross_at']) if p.get('cross_at') is not None else t_start + 1.2
        tl(f"tl.to('#{pid} .twin .x',{{backgroundColor:'#c0392b',duration:.25,stagger:.05}},{tx_:.3f});")
        t2 = T0(p['text2_at']) if p.get('text2_at') is not None else t_start + 2
        tl(f"tl.to('#{pid} .twin',{{autoAlpha:0,y:60,duration:.35,stagger:.04,ease:'power2.in'}},{t2 - .45:.3f});")
        if p.get('text2'): tl.show(sel('.vb1'), t2, .6); texts.append((t2, p['text2']))
        tl(f"tl.fromTo('#{pid} .ptm',{{autoAlpha:0,x:60}},{{autoAlpha:1,x:0,duration:.45,ease:'power3.out'}},{t2 - .15:.3f});")
        for i in range(len(team)):
            tl(f"tl.fromTo('#{pid} .tr{i}',{{autoAlpha:0}},{{autoAlpha:1,duration:.3}},{t2 + .05 + i * .1:.3f});")
        tw_ = T0(p['walter_at']) if p.get('walter_at') is not None else t2 + .9
        tl(f"tl.fromTo('#{pid} .tr{wi}',{{autoAlpha:0,y:30,scale:.96}},{{autoAlpha:1,y:0,scale:1,duration:.5,ease:'back.out(1.8)'}},{tw_:.3f});")
        texts.append((tw_, f"{p.get('walter_role', 'walter')} {p.get('walter_text', '')}"))

    elif k == 'market':                      # the market as a circle; walter starts as a small orange circle inside it
        cx, cy, R = 1390, 600, 330
        h += (f'<div class="tx mkv">0</div><div class="sb mkl">{T(p.get("label", ""))}</div>')
        for i, r_ in enumerate(p.get('rows', [])):
            h += (f'<div class="mkr mkr{i}" style="top:{660 + i * 96}px"><div class="ic">{icon(r_.get("icon", "check"), 34, "currentColor", 1.8)}</div>'
                  f'<div class="a tx">{E(r_["title"])}</div><div class="b sb">{E(r_.get("text", ""))}</div></div>')
        if p.get('rings'):
            rg = p['rings']; vmax = max(float(x['value']) for x in rg); RR = p.get('ring_r', 330); cx = p.get('cx', 1250); bottom = 945
            svgr = '<svg class="vx" viewBox="0 0 1920 1080" fill="none">'
            labs = ''
            for i, x in enumerate(rg):
                r = RR * (float(x['value']) / vmax) ** .5; cyi = bottom - r; st = x.get('style', 'solid')
                fill = {'faint': 'rgba(245,245,245,.04)', 'solid': 'rgba(245,245,245,.09)', 'orange': '#EF7619'}[st]
                stroke = {'faint': 'rgba(245,245,245,.45)', 'solid': 'rgba(245,245,245,.8)', 'orange': '#EF7619'}[st]
                dash = ' stroke-dasharray="8 8"' if st == 'faint' else ''
                svgr += f'<circle class="mrg mrg{i}" cx="{cx}" cy="{cyi:.0f}" r="{r:.0f}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"{dash} style="transform-origin:{cx}px {bottom}px"/>'
                if st == 'orange':
                    lx = cx + r + p.get('label_dx', 200)
                    svgr += f'<path class="d mrl{i}" d="M{cx + r + 8:.0f} {cyi:.0f}H{lx - 14:.0f}" stroke="#EF7619" stroke-width="2"/>'
                    labs += (f'<div class="tx mrv{i}" style="left:{lx:.0f}px;top:{cyi - 40:.0f}px;font-size:48px;letter-spacing:-.03em;white-space:nowrap;color:var(--orange)">{E(x["display"])}</div>'
                             f'<div class="cap mrc{i}" style="left:{lx:.0f}px;top:{cyi + 18:.0f}px;line-height:1.35">{T(x.get("label", ""))}</div>')
                else:
                    ty = bottom - 2 * r + (44 if i == 0 else r * .55)
                    labs += (f'<div class="cap mrc{i}" style="left:{cx - 300}px;width:600px;top:{ty:.0f}px;text-align:center">{T(x.get("label", ""))}</div>'
                             f'<div class="tx mrv{i}" style="left:{cx - 300}px;width:600px;top:{ty + 30:.0f}px;text-align:center;font-size:52px;letter-spacing:-.035em">{E(x["display"])}</div>')
            h += svgr + '</svg>' + labs
            for i, x in enumerate(rg):
                tr = T0(x['at']) if x.get('at') is not None else t_start + .3
                if x.get('style') == 'orange':
                    tl(f"tl.fromTo('#{pid} .mrg{i}',{{autoAlpha:0,scale:0}},{{autoAlpha:1,scale:1,duration:.6,ease:'back.out(2)'}},{tr - .1:.3f});")
                    tl.draw(sel(f'.mrl{i}'), tr + .3, .4)
                else:
                    tl(f"tl.fromTo('#{pid} .mrg{i}',{{autoAlpha:0,scale:.85}},{{autoAlpha:1,scale:1,duration:.7,ease:'power3.out'}},{tr - .1:.3f});")
                tl.show(sel(f'.mrc{i}'), tr + .2, .4, 6); tl.show(sel(f'.mrv{i}'), tr + .35, .4, 6)
                texts.append((tr + .35, f"{x.get('label', '')} {x['display']}"))
        r0, r1 = p.get('start_r', 100), p.get('grow_r', 150)
        old = not p.get('rings')
        if old: h += (f'<svg class="vx" viewBox="0 0 1920 1080" fill="none">'
              f'<circle class="mko" cx="{cx}" cy="{cy}" r="{R}" fill="rgba(245,245,245,.06)" opacity="0"/>'
              f'<circle class="d mkoc" cx="{cx}" cy="{cy}" r="{R}" stroke="rgba(245,245,245,.6)" stroke-width="3" transform="rotate(-90 {cx} {cy})"/>'
              f'<circle class="mkx" cx="{cx + 150}" cy="{cy + 60}" r="140" fill="rgba(245,245,245,.10)" stroke="rgba(245,245,245,.45)" stroke-width="2" stroke-dasharray="8 8" opacity="0"/>'
              f'<circle class="mki" cx="{cx - 90}" cy="{cy + 40}" r="{r0}" fill="#EF7619"/></svg>')
        if old: h += f'<div class="cap mkt" style="left:{cx - 300}px;width:600px;top:{cy - R + 120}px;text-align:center">{E(p.get("circle_label", "Market"))}</div>'
        if old: h += f'<div class="mkin mkil" style="left:{cx - 90 - 100}px;width:200px;top:{cy + 40 - 16}px">{T(p.get("start_label", "Start"))}</div>'
        if old: h += f'<div class="sb mkxl" style="left:{cx + 110}px;width:220px;top:{cy + 30}px;font-size:24px;text-align:center;line-height:1.2">{T(p.get("alongside_label", "Existing software"))}</div>'
        chips = p.get('chips', [])
        pos = [(cx - 270, cy + R + 34), (cx - 85, cy + R + 34), (cx + 85, cy + R + 34)]
        for i, ch_ in enumerate(chips):
            x, y = pos[i % 3]
            h += f'<div class="mkc mkc{i}" style="left:{x}px;top:{y}px">{E(ch_)}</div>'
        if old:
            tl.draw(sel('.mkoc'), t_start + .1, 1.0)
            tl(f"tl.to('#{pid} .mko',{{opacity:1,duration:.6}},{t_start + .6:.3f});")
            tl.show(sel('.mkt'), t_start + .5, .4, 0); texts.append((t_start + .5, p.get('circle_label', '')))
        for i, t in enumerate(_times(p, len(chips), T0, t_start + .6, t_end, key='chips_at', gap=.4)):
            tl(f"tl.fromTo('#{pid} .mkc{i}',{{autoAlpha:0,scale:.7}},{{autoAlpha:1,scale:1,duration:.35,ease:'back.out(2)'}},{t - .1:.3f});")
            texts.append((t, chips[i]))
        tv = T0(p['value_at']) if p.get('value_at') is not None else t_start + 1
        tl.show(sel('.mkv'), tv - .1, .3, 0)
        disp = json.dumps(p.get('display', ''))
        tl(f"count('#{pid} .mkv',{tv:.3f},{float(p['value'])},1.4,n=>n>={float(p['value']) - .05}?{disp}:'€'+n.toFixed(1)+'bn');")
        tl.show(sel('.mkl'), tv + .4, .45, 10); texts.append((tv + .4, p.get('label', '')))
        rows = p.get('rows', []); trs = _times(p, len(rows), T0, tv + 2, t_end, key='row_at')
        for i, t in enumerate(trs):
            tl(f"tl.fromTo('#{pid} .mkr{i}',{{autoAlpha:0,x:-30}},{{autoAlpha:1,x:0,duration:.45,ease:'power3.out'}},{t - .1:.3f});")
            texts.append((t, f"{rows[i]['title']} {rows[i].get('text', '')}"))
        if trs and old:
            tl(f"gsap.set('#{pid} .mki',{{scale:0,transformOrigin:'50% 50%'}});")
            tl(f"tl.to('#{pid} .mki',{{scale:1,duration:.55,ease:'back.out(1.8)'}},{trs[0] - .1:.3f});")
            tl.show(sel('.mkil'), trs[0] + .3, .35, 0)
        if len(trs) > 1 and old:
            tl(f"tl.to('#{pid} .mkx',{{opacity:1,duration:.5}},{trs[1] - .1:.3f});"); tl.show(sel('.mkxl'), trs[1] + .2, .35, 0)
            texts.append((trs[1] + .2, p.get('alongside_label', '')))
        if len(trs) > 2 and old:
            sc = r1 / r0
            tl(f"tl.to('#{pid} .mki',{{scale:{sc:.3f},duration:1.6,ease:'power2.inOut'}},{trs[2]:.3f});")
        if p.get('note'):
            h += f'<div class="vnote tx">{E(p["note"])}</div>'; tl.show(sel('.vnote'), tv + .4, .4, 0)

    elif k == 'moves':                       # next steps as cards, each with a small moving picture
        its = p['items']; n = len(its); gap = 34; w = (1700 - gap * (n - 1)) / n
        top = 320 if p.get('head') else 240
        for i, it in enumerate(its):
            x = 110 + i * (w + gap); kd = it.get('kind'); vz = ''
            if kd == 'flip':
                vz = (f'<div class="mpill mf0" style="left:{w / 2 - 100:.0f}px;top:90px;width:200px;text-align:center;background:rgba(245,245,245,.12);color:#e6e2dd">{E(it.get("from", "Pilot"))}</div>'
                      f'<div class="mpill mf1" style="left:{w / 2 - 110:.0f}px;top:90px;width:220px;text-align:center;background:#b0cc9b;color:#0d1d00;opacity:0">{E(it.get("to", "Paying"))}</div>')
            elif kd == 'shift':
                vz = (f'<div class="mic ms0" style="left:{w / 2 - 150:.0f}px;top:76px">{icon(it.get("icon_from", "building"), 56)}</div>'
                      f'<svg class="ms1" style="left:{w / 2 - 44:.0f}px;top:108px" width="88" height="32" viewBox="0 0 88 32" fill="none"><path class="d msa" d="M4 16H80M68 4L82 16L68 28" stroke="#EF7619" stroke-width="3"/></svg>'
                      f'<div class="mic o ms2" style="left:{w / 2 + 54:.0f}px;top:76px">{icon(it.get("icon_to", "tower"), 56)}</div>')
            elif kd == 'coins':
                vz = ''.join(f'<div class="mcoin mc{j}" style="left:{w / 2 - 60:.0f}px;top:{170 - j * 26}px"></div>' for j in range(5))
                vz += f'<div class="mic ms2" style="left:{w / 2 + 80:.0f}px;top:70px;width:76px;height:76px;border-radius:50%">{icon("people", 40)}</div>'
            elif kd == 'round':              # today only TBV; external investors join the round
                xs = (w / 2 - 120, w / 2, w / 2 + 120)
                vz += f'<div class="mrl sb" style="left:{xs[0] - 70:.0f}px;width:140px;top:8px">{E(it.get("own_label", "Today"))}</div>'
                vz += f'<div class="mrl mrlx" style="left:{(xs[1] + xs[2]) / 2 - 130:.0f}px;width:260px;top:8px;color:var(--orange)">{E(it.get("new_label", "+ External"))}</div>'
                vz += f'<div class="mrn tb mr0" style="left:{xs[0] - 38:.0f}px;top:36px">{E(it.get("own", "TBV"))}</div>'
                for j in (1, 2):
                    vz += f'<div class="mrn o mr{j}" style="left:{xs[j] - 38:.0f}px;top:36px">{icon("euro", 44, "#1f1d1c", 2)}</div>'
                vz += (f'<svg style="left:0;top:0" width="{w:.0f}" height="250" viewBox="0 0 {w:.0f} 250" fill="none">'
                       + ''.join(f'<path class="d ml{j}" d="M{xs[j]:.0f} 116C{xs[j]:.0f} 150 {w / 2:.0f} 140 {w / 2:.0f} 172" stroke="{"#F5F5F5" if j == 0 else "#EF7619"}" stroke-width="3"/>' for j in range(3))
                       + '</svg>')
                vz += f'<img class="mlg" src="{logo_light}" style="left:{w / 2 - 80:.0f}px;top:180px;width:160px;height:44px;object-fit:contain">'
            elif kd == 'seats':
                for j in range(3):
                    vz += f'<div class="mseat mt{j}" style="left:{w / 2 - 176 + j * 88:.0f}px;top:86px">{icon("people", 44)}</div>'
                vz += f'<div class="mseat e mt3" style="left:{w / 2 + 88:.0f}px;top:86px">+</div>'
            h += (f'<div class="mv mv{i}" style="left:{x:.0f}px;top:{top}px;width:{w:.0f}px;height:600px"><div class="vz" style="width:{w:.0f}px">{vz}</div>'
                  f'<div class="n">0{i + 1}</div><div class="t tx">{E(it["title"])}</div><div class="d sb" style="width:{w - 68:.0f}px">{T(it.get("text", ""))}</div></div>')
        for i, t in enumerate(_times(p, n, T0, t_start, t_end)):
            it = its[i]; kd = it.get('kind'); s_ = f'#{pid} .mv{i}'
            tl(f"tl.fromTo('{s_}',{{autoAlpha:0,y:40}},{{autoAlpha:1,y:0,duration:.5,ease:'power3.out'}},{t - .15:.3f});")
            texts.append((t, f"{it['title']} {it.get('text', '')}"))
            if kd == 'flip':
                tl(f"tl.to('{s_} .mf0',{{rotationX:90,autoAlpha:0,duration:.25,ease:'power1.in'}},{t + .7:.3f});")
                tl(f"tl.fromTo('{s_} .mf1',{{rotationX:-90,opacity:0}},{{rotationX:0,opacity:1,duration:.3,ease:'back.out(2)'}},{t + .95:.3f});")
            elif kd == 'shift':
                tl(f"tl.fromTo('{s_} .ms0',{{autoAlpha:0,scale:.7}},{{autoAlpha:1,scale:1,duration:.35}},{t + .1:.3f});")
                tl.draw(f'{s_} .msa', t + .45, .5)
                tl(f"tl.fromTo('{s_} .ms2',{{autoAlpha:0,scale:.7}},{{autoAlpha:1,scale:1,duration:.4,ease:'back.out(2)'}},{t + .9:.3f});")
            elif kd == 'coins':
                tl(f"tl.fromTo('{s_} .mcoin',{{autoAlpha:0,y:-40}},{{autoAlpha:1,y:0,duration:.3,ease:'bounce.out',stagger:.14}},{t + .1:.3f});")
                tl(f"tl.fromTo('{s_} .ms2',{{autoAlpha:0,scale:.7}},{{autoAlpha:1,scale:1,duration:.4,ease:'back.out(2)'}},{t + .9:.3f});")
            elif kd == 'round':
                tl(f"tl.fromTo('{s_} .mr0,{s_} .mlg',{{autoAlpha:0,scale:.7}},{{autoAlpha:1,scale:1,duration:.35,ease:'back.out(2)'}},{t + .05:.3f});")
                tl.draw(f'{s_} .ml0', t + .3, .4)
                tl(f"tl.fromTo('{s_} .mr1,{s_} .mr2',{{autoAlpha:0,scale:.4,y:-30}},{{autoAlpha:1,scale:1,y:0,duration:.45,ease:'back.out(2)',stagger:.2}},{t + .8:.3f});")
                tl(f"tl.to('{s_} .ml1,{s_} .ml2',{{strokeDashoffset:0,duration:.45,stagger:.2}},{t + 1.1:.3f});")
                tl(f"tl.fromTo('{s_} .mrlx',{{autoAlpha:0}},{{autoAlpha:1,duration:.3}},{t + 1.0:.3f});")
                tl(f"tl.fromTo('{s_} .mrl.sb',{{autoAlpha:0}},{{autoAlpha:1,duration:.3}},{t + .3:.3f});")
                tl(f"tl.to('{s_} .mlg',{{scale:1.12,duration:.25,yoyo:true,repeat:1}},{t + 1.7:.3f});")
            elif kd == 'seats':
                tl(f"tl.fromTo('{s_} .mseat',{{autoAlpha:0,scale:.6}},{{autoAlpha:1,scale:1,duration:.3,ease:'back.out(2)',stagger:.12}},{t + .1:.3f});")
                tl(f"tl.to('{s_} .mt3',{{scale:1.15,duration:.35,yoyo:true,repeat:3,ease:'power1.inOut'}},{t + .8:.3f});")

    else:
        raise ValueError(f'unknown visual panel type {k}')
    h += '</div>'
    tl.hide(f'#{pid}', t_end - .35, .3)
    return h, tl.js(), [x for x in texts if x[1]], holds
