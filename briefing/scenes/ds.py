"""'With Drees & Sommer': four fixed screens, one per voice-over paragraph:
 A rows (why it matters), B boxes (who brings what), C cards (use cases by team), D people + next steps.
Self-contained: own warm background, rule, chapter label and corner logo, namespaced classes (ds*).
Screens are placed at internal timeline times (usually after the film's own end) and spliced in
via the film's time map. Every screen dict carries 't0' (start), 't1' (end) and cue times."""
import html as _h
E = _h.escape

CSS = r"""
#stage .dsS{left:0;top:0;width:1920px;height:1080px;background:var(--warm)}
.dsS .dsRule{left:110px;right:110px;top:108px;height:1px;background:rgba(40,37,36,.25)}
.dsS .dsChap{left:110px;top:64px;font-weight:600;font-size:22px;letter-spacing:.09em;text-transform:uppercase;color:var(--mid);white-space:nowrap}
#stage .dsS .dsChap b{position:static;color:var(--orange);margin-right:18px}
#stage .dsS .dsChap span{position:static}
.dsS .dsLogo{right:110px;top:42px;height:44px;width:180px;object-fit:contain;object-position:right center}
.dsS .dsCap{left:110px;top:176px;font-weight:600;font-size:22px;letter-spacing:.09em;text-transform:uppercase;color:var(--mid);white-space:nowrap}
.dsS .dsHd{left:110px;top:220px;font-size:60px;letter-spacing:-.035em;line-height:1.05;color:var(--dark);white-space:nowrap}
.dsS .dsHw{top:236px;font-size:58px;letter-spacing:-.035em;line-height:1;color:var(--dark);white-space:nowrap}
.dsS .dsEnd{left:110px;font-size:42px;letter-spacing:-.03em;color:var(--dark);white-space:nowrap}
#stage .dsS .dsEnd b{position:static;display:inline-block;width:40px;height:3px;background:var(--orange);vertical-align:middle;margin-right:26px}
.dsS .dsHair{left:0;top:0;height:1px;background:rgba(40,37,36,.3);transform-origin:left center}
/* A: rows (title + description) */
.dsS .dsRow{left:110px;width:1700px;height:120px}
.dsS .dsRow .n{left:0;top:30px;font-weight:600;font-size:22px;letter-spacing:.06em;color:var(--orange)}
.dsS .dsRow .t{left:86px;top:22px;font-size:40px;letter-spacing:-.025em;color:var(--dark);white-space:nowrap}
.dsS .dsRow .d{left:86px;top:76px;font-size:26px;font-weight:400;color:var(--mid);white-space:nowrap}
/* A: transitions (from -> to) */
.dsS .dsTr{left:110px;width:1700px;height:100px}
.dsS .dsTr .f{left:0;top:30px;font-size:36px;letter-spacing:-.02em;color:var(--mid);white-space:nowrap}
.dsS .dsTr svg{left:700px;top:40px;width:80px;height:20px}
.dsS .dsTr .to{left:840px;top:30px;font-size:36px;letter-spacing:-.02em;color:var(--dark);white-space:nowrap}
/* B: three boxes */
.dsS .dsMb{top:330px;width:500px;height:440px;border-radius:14px;border:1.5px solid rgba(40,37,36,.3)}
.dsS .dsMb.dk{background:var(--dark);border-color:var(--dark)}
.dsS .dsMb .c{left:40px;top:40px;font-weight:600;font-size:22px;letter-spacing:.09em;text-transform:uppercase;color:var(--mid);white-space:nowrap}
.dsS .dsMb.dk .c{color:#cfcbc6}
.dsS .dsMb .mt{left:40px;top:92px;width:430px;font-size:40px;letter-spacing:-.025em;line-height:1.1;color:var(--dark)}
.dsS .dsMb.dk .mt{color:var(--lg)}
.dsS .dsMb .ml{left:40px;top:200px;width:430px;font-size:27px;line-height:1.5;font-weight:400;color:var(--mid)}
.dsS .dsMb.dk .ml{color:#cfcbc6}
.dsS .dsAr{top:540px;width:84px;height:20px}
/* C: cards */
.dsS .dsUc{top:300px;height:548px;border-radius:14px}
.dsS .dsUc.dk{background:var(--dark)}
.dsS .dsUc.lt{border:1.5px solid rgba(40,37,36,.3)}
.dsS .dsUc.dv{border:1.5px dashed rgba(40,37,36,.4)}
.dsS .dsUc .un{left:32px;top:30px;font-weight:600;font-size:22px;letter-spacing:.06em;color:var(--orange)}
.dsS .dsUc .ubu{left:76px;top:32px;font-weight:600;font-size:16px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap}
.dsS .dsUc.dk .ubu{color:#cfcbc6} .dsS .dsUc.lt .ubu,.dsS .dsUc.dv .ubu{color:var(--mid)}
.dsS .dsUc .udev{right:24px;top:24px;font-weight:600;font-size:16px;letter-spacing:.09em;text-transform:uppercase;color:var(--mid);border:1.5px solid rgba(40,37,36,.35);border-radius:8px;padding:6px 10px;white-space:nowrap}
.dsS .dsUc .ut{left:32px;top:74px;font-size:31px;letter-spacing:-.02em;line-height:1.12;white-space:nowrap}
.dsS .dsUc.dk .ut{color:var(--lg)} .dsS .dsUc.lt .ut,.dsS .dsUc.dv .ut{color:var(--dark)}
.dsS .dsUc .uk{left:32px;top:170px;font-weight:600;font-size:16px;letter-spacing:.09em;text-transform:uppercase;color:var(--gray)}
.dsS .dsUc.lt .uk,.dsS .dsUc.dv .uk{color:var(--mid)}
.dsS .dsUc .ug{left:32px;top:196px;font-size:22px;line-height:1.3;font-weight:400}
.dsS .dsUc.dk .ug{color:#cfcbc6} .dsS .dsUc.lt .ug,.dsS .dsUc.dv .ug{color:var(--mid)}
.dsS .dsUc .uh{left:32px;top:282px;height:1px;background:rgba(245,245,245,.25)}
.dsS .dsUc.lt .uh,.dsS .dsUc.dv .uh{background:rgba(40,37,36,.25)}
.dsS .dsUc .ubs{left:32px;top:304px}
#stage .dsS .dsUc .ubs .ub{position:relative;font-size:23px;line-height:1.28;padding-left:26px;margin-bottom:14px}
.dsS .dsUc.dk .ub{color:var(--lg)} .dsS .dsUc.lt .ub,.dsS .dsUc.dv .ub{color:var(--dark)}
#stage .dsS .dsUc .ub::before{content:'';position:absolute;left:0;top:13px;width:14px;height:2px;background:var(--orange)}
.dsS .dsCEnd{left:110px;top:880px;width:1700px;font-size:30px;line-height:1.3;letter-spacing:-.015em;color:var(--dark)}
/* D: people + steps */
.dsS .dsPc{left:110px;top:330px;font-weight:600;font-size:22px;letter-spacing:.09em;text-transform:uppercase;color:var(--mid);white-space:nowrap}
.dsS .dsNm{left:110px;font-size:76px;letter-spacing:-.04em;line-height:1;color:var(--dark);white-space:nowrap}
.dsS .dsNr{left:110px;font-size:22px;font-weight:400;color:var(--mid);white-space:nowrap}
.dsS .dsSt{left:1010px;width:800px;height:170px}
.dsS .dsSt .c{left:0;top:26px;font-weight:600;font-size:20px;letter-spacing:.09em;text-transform:uppercase;color:var(--orange);white-space:nowrap}
.dsS .dsSt .t{left:0;top:62px;width:800px;font-size:36px;letter-spacing:-.02em;line-height:1.15;color:var(--dark)}
.dsS .dsSt .d{left:0;top:112px;width:800px;font-size:24px;line-height:1.3;font-weight:400;color:var(--mid)}
"""

ARROW = '<svg {a} viewBox="0 0 84 20" fill="none" stroke="#EF7619" stroke-width="2"><path d="M2 10H80M70 3L80 10L70 17"/></svg>'

def frame(sid, chap, logo):
    return (f'<div id="{sid}" class="dsS h"><div class="dsRule"></div>'
            f'<div class="dsChap"><b>{chap[0]}</b><span>{E(chap[1])}</span></div>'
            + (logo if logo.startswith('<') else f'<img class="dsLogo" src="{logo}">'))

def screen_rows(sid, chap, logo, s):
    h = frame(sid, chap, logo)
    if s.get('cap'): h += f'<div class="dsCap">{E(s["cap"])}</div>'
    h += f'<div class="dsHd" style="top:{s.get("hdTop",226)}px">{s["head"]}</div>'
    y = s.get('rowTop', 380); step = s.get('rowStep', 130)
    for i, (t, d) in enumerate(s['rows']):
        h += (f'<div class="dsRow" style="top:{y+i*step}px"><div class="dsHair" style="width:1700px"></div>'
              f'<div class="n">0{i+1}</div><div class="t">{E(t)}</div><div class="d">{E(d)}</div></div>')
    if s.get('end'): h += f'<div class="dsEnd" style="top:{s.get("endTop",900)}px"><b></b>{E(s["end"])}</div>'
    return h + '</div>'

def screen_trans(sid, chap, logo, s):
    h = frame(sid, chap, logo)
    if s.get('cap'): h += f'<div class="dsCap">{E(s["cap"])}</div>'
    for (txt, x) in s['heads']:
        h += f'<div class="dsHw" style="left:{x}px">{E(txt)}</div>'
    for i, (f, t) in enumerate(s['rows']):
        h += (f'<div class="dsTr" style="top:{350+i*100}px"><div class="dsHair" style="width:1700px"></div>'
              f'<div class="f">{E(f)}</div>' + ARROW.format(a='') + f'<div class="to">{E(t)}</div></div>')
    if s.get('end'): h += f'<div class="dsEnd" style="top:{s.get("endTop",800)}px"><b></b>{E(s["end"])}</div>'
    return h + '</div>'

def screen_boxes(sid, chap, logo, s):
    h = frame(sid, chap, logo)
    h += f'<div class="dsHd" style="top:186px;font-size:60px">{E(s["head"])}</div>'
    for i, (c, t, lines, dk) in enumerate(s['boxes']):
        h += (f'<div class="dsMb{" dk" if dk else ""}" style="left:{110+i*600}px"><div class="c">{E(c)}</div>'
              f'<div class="mt">{E(t)}</div><div class="ml">{"<br>".join(E(l) for l in lines)}</div></div>')
    h += ARROW.format(a='class="dsAr" style="left:618px"') + ARROW.format(a='class="dsAr" style="left:1218px"')
    if s.get('end'): h += f'<div class="dsEnd" style="top:846px"><b></b>{E(s["end"])}</div>'
    return h + '</div>'

def screen_cards(sid, chap, logo, s):
    h = frame(sid, chap, logo)
    h += f'<div class="dsHd" style="top:186px;font-size:{s.get("hdSize",56)}px">{E(s["head"])}</div>'
    n = len(s['cards']); gap = 40; W = (1700 - gap*(n-1)) / n
    for i, c in enumerate(s['cards']):
        cls = c.get('style', 'dk')
        tw = W - 64
        h += (f'<div class="dsUc {cls}" style="left:{110+i*(W+gap):.0f}px;width:{W:.0f}px"><div class="un">0{i+1}</div>'
              + (f'<div class="ubu">{E(c["bu"])}</div>' if c.get('bu') else '')
              + ('<div class="udev">In development</div>' if c.get('dev') else '')
              + f'<div class="ut">{c["title"]}</div><div class="uk">{E(c.get("klabel","Client trigger"))}</div>'
              f'<div class="ug" style="width:{tw:.0f}px">{E(c["trigger"])}</div><div class="uh" style="width:{tw:.0f}px"></div>'
              f'<div class="ubs" style="width:{tw:.0f}px">' + ''.join(f'<div class="ub">{E(b)}</div>' for b in c['bullets']) + '</div></div>')
    if s.get('end'): h += f'<div class="dsCEnd">{E(s["end"])}</div>'
    return h + '</div>'

def screen_people(sid, chap, logo, s):
    h = frame(sid, chap, logo)
    h += f'<div class="dsHd" style="top:186px;font-size:60px">{E(s["head"])}</div>'
    h += f'<div class="dsPc">{E(s["pcap"])}</div>'
    for i, (nm, role) in enumerate(s['people']):
        h += f'<div class="dsNm" style="top:{384+i*150}px">{E(nm)}</div>'
        if role: h += f'<div class="dsNr" style="top:{474+i*150}px">{E(role)}</div>'
    for i, (c, t, d) in enumerate(s['steps']):
        h += (f'<div class="dsSt" style="top:{330+i*200}px"><div class="dsHair" style="width:800px"></div>'
              f'<div class="c">{E(c)}</div><div class="t">{E(t)}</div><div class="d">{E(d)}</div></div>')
    return h + '</div>'

BUILD = {'rows': screen_rows, 'trans': screen_trans, 'boxes': screen_boxes, 'cards': screen_cards, 'people': screen_people}

def js_screen(sid, s):
    """GSAP cues on the film's own timeline `tl`."""
    t0, t1 = s['t0'], s['t1']; q = s['cues']; k = s['kind']
    J = [f"tl.set('#{sid}',{{autoAlpha:1}},{t0});"]
    def sh(sel, t, d=.5, y=18): J.append(f"tl.fromTo({sel},{{autoAlpha:0,y:{y}}},{{autoAlpha:1,y:0,duration:{d},ease:'power2.out'}},{t});")
    def gr(sel, t): J.append(f"tl.fromTo({sel},{{scaleX:0}},{{scaleX:1,duration:.6,ease:'power2.inOut'}},{t});")
    S = f"'#{sid} "
    J.append(f"gsap.set(['#{sid} .dsCap','#{sid} .dsHd','#{sid} .dsHw','#{sid} .dsRow','#{sid} .dsTr','#{sid} .dsEnd','#{sid} .dsMb','#{sid} .dsAr','#{sid} .dsUc','#{sid} .dsCEnd','#{sid} .dsPc','#{sid} .dsNm','#{sid} .dsNr','#{sid} .dsSt'],{{autoAlpha:0}});")
    if 'cap' in q: sh(f"'#{sid} .dsCap'", q['cap'], .45, 8)
    if 'head' in q: sh(f"'#{sid} .dsHd'", q['head'], .55)
    for i, t in enumerate(q.get('heads', [])): sh(f"document.querySelectorAll('#{sid} .dsHw')[{i}]", t, .45, 20)
    for i, t in enumerate(q.get('items', [])):
        cls = {'rows': 'dsRow', 'trans': 'dsTr', 'boxes': 'dsMb', 'cards': 'dsUc', 'people': 'dsSt'}[k]
        sh(f"document.querySelectorAll('#{sid} .{cls}')[{i}]", t, .5, 20)
        if k in ('rows', 'trans', 'people'): gr(f"document.querySelectorAll('#{sid} .{cls} .dsHair')[{i}]", t)
        if k == 'boxes' and i > 0:
            J.append(f"tl.fromTo(document.querySelectorAll('#{sid} .dsAr')[{i-1}],{{autoAlpha:0,x:-14}},{{autoAlpha:1,x:0,duration:.35,ease:'power2.out'}},{t-.25});")
    if k == 'people':
        if 'pcap' in q: sh(f"'#{sid} .dsPc'", q['pcap'], .45, 10)
        for i, t in enumerate(q.get('names', [])):
            sh(f"document.querySelectorAll('#{sid} .dsNm')[{i}]", t, .55)
            J.append(f"if(document.querySelectorAll('#{sid} .dsNr')[{i}]) tl.fromTo(document.querySelectorAll('#{sid} .dsNr')[{i}],{{autoAlpha:0}},{{autoAlpha:1,duration:.4}},{t+.2});")
    if 'end' in q: sh(f"'#{sid} .dsEnd, #{sid} .dsCEnd'", q['end'], .5, 12)
    J.append(f"hide('#{sid} > *:not(.dsRule):not(.dsChap):not(.dsLogo)',{t1},.3);")
    J.append(f"tl.set('#{sid}',{{autoAlpha:0}},{s.get('t_off', t1 + .55)});")
    return '\n'.join(J)

def build(screens, chap, logo):
    """screens: list of (sid, screen dict). Returns (html, css, js)."""
    html = '<div id="dsBase" class="dsS h"></div>' + ''.join(BUILD[s['kind']](sid, chap, logo, s) for sid, s in screens)
    t0 = min(s['t0'] for _, s in screens); t1 = max(s['t1'] for _, s in screens)
    js = (f"tl.set('#dsBase',{{autoAlpha:1}},{t0-.01:.3f}); tl.set('#dsBase',{{autoAlpha:0}},{t1+.4:.3f});\n"
          + '\n'.join(js_screen(sid, s) for sid, s in screens))
    return html, CSS, js

def screen(b, c, letter, spec):
    """One D&S screen as a film block. Items are cued to voice-over anchors (default: sentence starts)."""
    from .base import Scene, need_for
    from ..config import CHAPTERS
    s = dict(spec); k = s['kind']; sid = b.sid
    n = {'rows': len(s.get('rows', [])), 'trans': len(s.get('rows', [])), 'boxes': len(s.get('boxes', [])), 'cards': len(s.get('cards', [])), 'people': len(s.get('steps', []))}[k]
    ats = s.get('at')
    if ats: items = [round(b.T(a) - .1, 3) for a in ats]
    elif b.nsent >= n: items = [round(b.T(f's{j}') - .1, 3) for j in range(b.nsent - n, b.nsent)]
    else: items = [round(b.t_speech + .4 + i * (b.t_audio_end - b.t_speech - .4) / n, 3) for i in range(n)]
    q = dict(head=round(b.t_speech + (.2 if k == 'rows' else -.3), 3), items=items)
    if k in ('rows', 'trans'): q['cap'] = round(b.t0 + .2, 3)
    if k == 'trans':
        q['head'] = None; q.pop('head')
        q['heads'] = [round(b.T(a) - .05, 3) for a in s.get('heads_at', [])] or [round(b.t_speech + .3 + i * .8, 3) for i in range(len(s['heads']))]
    if s.get('end'): q['end'] = round(items[-1] + 1.3, 3)
    if k == 'people':
        q['pcap'] = round(b.t_speech + .1, 3)
        q['names'] = [round(b.T(a) - .05, 3) for a in s.get('names_at', [])] or [round(b.t_speech + .5 + i * 1.0, 3) for i in range(len(s['people']))]
    s.update(t0=b.t0, t1=round(b.t_end - .35, 3), t_off=round(b.t_end + .25, 3), cues=q)
    logo = f'<img class="dsLogo" src="{c["logo_dark"]}">'
    html = BUILD[k](sid, CHAPTERS['ds'], logo, s)
    js = js_screen(sid, s)
    texts = [(q.get('head', q.get('heads', [0])[-1]), s.get('head', ''))] + [(t, f'item {i + 1}') for i, t in enumerate(items)]
    if k == 'trans':
        texts = [(t, h_[0]) for t, h_ in zip(q['heads'], s['heads'])] + [(t, ' '.join(r)) for t, r in zip(items, s['rows'])]
    if k == 'cards':
        texts = [(q['head'], s['head'])] + [(t, ' '.join([cd['title']] + cd['bullets'])) for t, cd in zip(items, s['cards'])]
    elif k == 'rows':
        texts = [(q['head'], s['head'])] + [(t, ' '.join(r)) for t, r in zip(items, s['rows'])]
    elif k == 'boxes':
        texts = [(q['head'], s['head'])] + [(t, ' '.join([bx[1]] + list(bx[2]))) for t, bx in zip(items, s['boxes'])]
    elif k == 'people':
        texts = [(q['head'], s['head'])] + [(t, ' '.join(st)) for t, st in zip(items, s['steps'])]
    if s.get('end'): texts.append((q['end'], s['end']))
    last = max(texts, key=lambda x: x[0])[0]
    # cards are dense: the whole screen needs time after the last card, not just the last line
    need = need_for([x for x in texts if x[0] >= last - .01], .35)
    if k == 'cards': need = max(need, items[-1] + 4.0)
    return Scene(html, '', js, need, texts)
