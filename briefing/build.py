"""End-to-end build of one company film: align -> cut interviews -> timeline -> page -> mix -> render -> encode -> QA."""
import json, os, re, math, shutil, subprocess, time
from pathlib import Path
import numpy as np, yaml
from .config import (ROOT, COMPANIES, BUILD, WEB, FPS, SR, VO_LUFS, TAG_IMAGE, SIZE_LIMIT_BYTES, AUDIO_KBPS,
                     INTRO_TEXT, NUM_WORDS, MIX_LUFS_RANGE, PEAK_MAX_DB)
from . import script as S, align as A, interview as I, timeline as TLN, page as PG, audio as AU

def paths(slug):
    c = COMPANIES / slug; b = BUILD / slug
    return c, b

def load(slug):
    c, _ = paths(slug)
    content = yaml.safe_load(open(c / 'content.yaml', encoding='utf-8'))
    content['_dir'] = str(c)
    content.setdefault('logo_light', content.get('logo', {}).get('light'))
    content.setdefault('logo_dark', content.get('logo', {}).get('dark'))
    sections = S.load(c / 'script.md')
    return content, sections

def intro_text(content):
    return INTRO_TEXT.format(num_word=NUM_WORDS[int(content['number'])])

def _links(bdir, cdir):
    bdir.mkdir(parents=True, exist_ok=True)
    for name, target in (('node_modules', ROOT / 'node_modules'), ('assets', ROOT / 'assets'), ('media', cdir / 'media')):
        p = bdir / name
        if p.is_symlink() or p.exists():
            if p.is_symlink(): p.unlink()
            else: continue
        p.symlink_to(target)

def prepare(slug, log=print):
    """Alignment + interview extraction. Cached in build/<slug>/."""
    content, sections = load(slug); cdir, bdir = paths(slug); _links(bdir, cdir)
    vo = cdir / content['voice']['take']
    x = AU.decode(vo, bdir / '_vo.f32', af=f'loudnorm=I={VO_LUFS}:TP=-1.5:LRA=11')
    take = A.Take(vo, sections, x, content.get('pronounce'))
    log(f'voice-over aligned: {take.dur:.1f}s, {len(take.words)} words')
    intro = cdir / content['voice']['intro']
    ix = AU.decode(intro, bdir / '_intro.f32')
    iw, _ = A.align_take(intro, intro_text(content))
    cues = PG.ident_cues(iw)
    segs = I.prepare(cdir, content['interview'], bdir / 'clips')
    log('interviews: ' + ', '.join(f'{k} {v["dur"]:.1f}s' for k, v in segs.items()))
    return content, sections, take, x, ix, cues, segs

def make(slug, log=print):
    """Timeline, page and sound. Returns a summary dict (also written to build/<slug>/build.json)."""
    content, sections, take, vo_x, intro_x, cues, segs = prepare(slug, log)
    cdir, bdir = paths(slug)
    TOFF = round(cues['end'] + 1.72, 2)
    blocks, scenes, place, D = TLN.build(content, take, segs)
    close = blocks[-1]
    jumps, add = AU.tune(TOFF + close.t_lock, str(bdir))
    pad = {k: add / 4 for k in ('ds_a', 'ds_b', 'ds_c', 'ds_d')}
    blocks, scenes, place, D = TLN.build(content, take, segs, pad)
    close = blocks[-1]; hit_full = TOFF + close.t_lock
    D = round(math.ceil(D * FPS) / FPS, 3)
    (bdir / 'film.html').write_text(PG.film(scenes, segs, D), encoding='utf-8')
    wm = content['logo_light']
    (bdir / 'ident.html').write_text(PG.ident(content['number'], wm, cues), encoding='utf-8')
    # ---- sound
    N = int(round(D * SR)); vo_bus = np.zeros(N, np.float32); it_bus = np.zeros(N, np.float32)
    def put(bus, src, a, b, t, fade=.012):
        s_ = src[int(round(a * SR)):int(round(b * SR))].copy(); n = int(fade * SR)
        if len(s_) > 2 * n: s_[:n] *= np.linspace(0, 1, n); s_[-n:] *= np.linspace(1, 0, n)
        j = int(round(t * SR)); s_ = s_[:max(0, N - j)]; bus[j:j + len(s_)] += s_
    for kind, key, a, b, t in place:
        if kind == 'vo': put(vo_bus, vo_x, a, b, t)
        else: put(it_bus, segs[key]['audio'], a, b, t, .08)
    vo_l = AU.lufs(vo_bus, str(bdir / '_t.f32'))
    it_c, it_l = AU.interview_bus(it_bus, vo_l, str(bdir))
    bus = vo_bus + it_c
    full = np.zeros((int(round((TOFF + D) * SR)), 2), np.float32)
    j = int(.5 * SR); full[j:j + len(intro_x)] += (intro_x * .9886)[:, None][:len(full) - j]
    j = int(round(TOFF * SR)); full[j:j + N] += bus[:, None]
    last_voice = TOFF + close.t_audio_end
    mix = AU.mixdown(full, jumps, hit_full, TOFF + D, last_voice, str(bdir / 'mix.wav'), str(bdir))
    summary = dict(slug=slug, toff=TOFF, film=D, total=round(TOFF + D, 3), music=[j_[2] for j_ in jumps], music_add=round(add, 2),
                   vo_lufs=vo_l, interview_lufs=it_l, mix=mix, ident_cues=cues,
                   blocks=[dict(key=b.key, t0=round(b.t0, 2), end=round(b.t_end, 2)) for b in blocks],
                   warnings=[w for b in blocks for w in b.warnings])
    (bdir / 'build.json').write_text(json.dumps(summary, indent=1))
    log(f'film {D:.1f}s + ident {TOFF:.1f}s, mix {mix["lufs"]} LUFS / peak {mix["peak"]} dB, music loops {summary["music"]}')
    for w in summary['warnings']: log('WARNING ' + w)
    return summary

def _render_page(page, frames, out, workers):
    out.mkdir(parents=True, exist_ok=True)
    step = math.ceil(frames / workers); procs = []
    for k in range(workers):
        a, b = k * step, min(frames, (k + 1) * step)
        if a >= b: continue
        procs.append(subprocess.Popen(['node', str(WEB / 'render.js'), str(page), str(a), str(b), str(out)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True))
    errs = [p.communicate()[0] for p in procs]
    bad = [e for e in errs if 'PAGE EXC' in e]
    if bad: raise RuntimeError('render errors:\n' + '\n'.join(bad)[:2000])

def render(slug, workers=None, log=print):
    _, bdir = paths(slug); s = json.loads((bdir / 'build.json').read_text())
    workers = workers or max(2, os.cpu_count() or 2)
    t = time.time()
    for name in ('frames_ident', 'frames_film', 'frames'):
        shutil.rmtree(bdir / name, ignore_errors=True)
    nI = int(round(s['toff'] * FPS)); nF = int(round(s['film'] * FPS))
    _render_page(bdir / 'ident.html', nI, bdir / 'frames_ident', workers)
    _render_page(bdir / 'film.html', nF, bdir / 'frames_film', workers)
    full = bdir / 'frames'; full.mkdir(); i = 0
    for d in ('frames_ident', 'frames_film'):
        for f in sorted((bdir / d).iterdir()): (full / f'f_{i:05d}.jpg').symlink_to(f); i += 1
    log(f'rendered {i} frames in {time.time() - t:.0f}s')
    return i

def encode(slug, log=print):
    c, bdir = paths(slug); content, _ = load(slug); s = json.loads((bdir / 'build.json').read_text())
    D = s['total']; out = bdir / f'Portfolio_Briefing_{int(content["number"]):02d}_{content["company"]}.mp4'
    kbps = int((SIZE_LIMIT_BYTES * .985 * 8 / D) / 1000 - AUDIO_KBPS - 12)
    for attempt in range(3):
        fc = '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]'
        base = f'ffmpeg -hide_banner -loglevel error -y -framerate {FPS} -i "{bdir}/frames/f_%05d.jpg" -loop 1 -i "{TAG_IMAGE}"'
        AU.run(f'{base} -filter_complex "{fc}" -map "[v]" -c:v libx264 -preset slow -b:v {kbps}k -pass 1 -passlogfile "{bdir}/x264" -r {FPS} -an -t {D} -f mp4 /dev/null')
        AU.run(f'{base} -i "{bdir}/mix.wav" -filter_complex "{fc}" -map "[v]" -map 2:a -c:v libx264 -preset slow -b:v {kbps}k -pass 2 -passlogfile "{bdir}/x264" '
               f'-r {FPS} -c:a aac -b:a {AUDIO_KBPS}k -ar {SR} -movflags +faststart -t {D} "{out}"')
        size = out.stat().st_size
        if size <= SIZE_LIMIT_BYTES: break
        kbps = int(kbps * SIZE_LIMIT_BYTES / size * .97)
    log(f'{out.name}: {size / 1e6:.2f} MB at {kbps} kbit/s')
    return out

def lint(content, sections):
    """Content rules every film must follow (see docs/RULES.md). Returns warnings."""
    texts = list(sections.values())
    def walk(o):
        if isinstance(o, str): texts.append(o)
        elif isinstance(o, dict): [walk(v) for k, v in o.items() if not k.startswith('_') and not k.endswith('_at')
                                   and k not in ('interview', 'type', 'kind', 'style', 'bg', 'src', 'video', 'audio', 'at', 'pronounce')]
        elif isinstance(o, list): [walk(v) for v in o]
    walk({k: v for k, v in content.items() if k not in ('voice', 'logo', 'logo_light', 'logo_dark', 'portrait')})
    for seg in content.get('interview', {}).values():
        for cw in seg.get('cutaways', []): walk(cw.get('panel', {})); walk(cw.get('caption', ''))
        for w in seg.get('words', []): walk(w.get('text', ''))
    blob = ' | '.join(texts)
    rules = [(r'\b(January|February|March|April|June|July|August|September|October|November|December)\b', 'date / month (keep it timeless)'),
             (r'(?<!Founded )(?<!founded )\b20\d\d\b', 'year (keep it timeless)'), (r'\b(this|next|last) (week|month|quarter|year)\b', 'relative date'),
             (r'\bQ[1-4]\b', 'quarter'), (r'\b(upcoming|tomorrow|soon to be)\b', 'upcoming event'),
             (r'\b(valuation|stake|ticket|term sheet|pre-money|post-money|co-invest\w*|cap table)\b', 'deal terms (never in the film)'),
             (r'\b(approved|approval|budget (is |was )?(approved|signed|released)|signed off)\b', 'operational detail (budget/approval)'), (r'\bco-creation\b', 'check wording "co-creation" with the partner')]
    out = []
    for rx, why in rules:
        for m in re.finditer(rx, blob, re.I): out.append(f'{why}: "...{blob[max(0, m.start() - 30):m.end() + 30].strip()}..."')
    return out

def qa(slug, log=print):
    """Automatic checks. Writes build/<slug>/qa.md and a contact sheet."""
    content, sections = load(slug); cdir, bdir = paths(slug); s = json.loads((bdir / 'build.json').read_text())
    rep = [f'# QA {content["company"]}', '']
    def item(ok, text): rep.append(('- [x] ' if ok else '- [ ] ') + text)
    # texts on screen
    scan = bdir / 'scan.json'
    subprocess.run(['node', str(WEB / 'scan_text.js'), str(scan), '0.1'], env={**os.environ, 'FILM': str(bdir / 'film.html')}, check=True, capture_output=True)
    runs = json.loads(scan.read_text())['runs']
    short = [r for r in runs if r['d'] < 2.0 and len(r['text']) >= 6 and r['t1'] < s['film'] - .2]
    item(not short, f'every text readable >= 2 s ({len(short)} short)')
    for r in short: rep.append(f'  - {r["t0"] + s["toff"]:.1f}s "{r["text"][:60]}" {r["d"]:.1f}s')
    # sound
    vo = np.fromfile(bdir / '_vo.f32', dtype=np.float32); beeps = AU.tts_beeps(vo)
    item(not beeps, f'no ElevenLabs beeps in the voice-over take ({beeps})')
    full = np.fromfile(bdir / 'voice_full.f32', dtype=np.float32).reshape(-1, 2)[:, 0]
    bl = AU.blips(full); item(not bl, f'no cut-off syllables ({bl})')
    m = s['mix']; item(MIX_LUFS_RANGE[0] <= m['lufs'] <= MIX_LUFS_RANGE[1] and m['peak'] <= PEAK_MAX_DB, f'loudness {m["lufs"]} LUFS, peak {m["peak"]} dB')
    flags = A.asr_check(cdir / content['voice']['take'], A.Take(cdir / content['voice']['take'], sections, vo, content.get('pronounce')))
    item(not flags, f'speech recognition agrees with the script ({len(flags)} sentences to listen to)')
    for f in flags: rep.append(f'  - {f[0]} at {f[1]}s: "{f[3][:70]}"')
    # content rules
    lw = lint(content, sections); item(not lw, f'content rules ({len(lw)} hints)')
    for w in lw: rep.append(f'  - {w}')
    for w in s['warnings']: rep.append(f'- [ ] {w}')
    mp4 = sorted(bdir.glob('Portfolio_Briefing_*.mp4'))
    if mp4:
        sz = mp4[-1].stat().st_size; item(sz <= SIZE_LIMIT_BYTES, f'file size {sz / 1e6:.2f} MB')
        _sheet(mp4[-1], bdir / 'contact_sheet.jpg')
        rep.append(f'\nContact sheet: {bdir / "contact_sheet.jpg"}')
    rep.append('\nStill to do by a person: watch the whole film once with sound; check names, logos and portrait crop.')
    (bdir / 'qa.md').write_text('\n'.join(rep))
    log('\n'.join(rep))

def _sheet(mp4, out, every=5):
    AU.run(f'ffmpeg -hide_banner -loglevel error -y -i "{mp4}" -vf "fps=1/{every},scale=384:216,drawtext=text=\'%{{pts\\:hms}}\':x=6:y=6:fontsize=16:fontcolor=red,tile=6x10" -frames:v 1 "{out}"')
