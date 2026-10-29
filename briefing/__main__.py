"""python -m briefing <command> <company>

  new <slug>       copy the template into companies/<slug>/
  tts <slug>       print the texts to paste into ElevenLabs (voice-over and intro)
  check <slug>     content rules + script/anchor check, no rendering
  make <slug>      align, cut interviews, build timeline, page and sound
  stills <slug> t1,t2,...   render single frames (film time) for a quick look
  render <slug>    render all frames
  encode <slug>    MP4 under 30 MB with the 'Internal use only' tag
  qa <slug>        automatic checks + contact sheet (build/<slug>/qa.md)
  all <slug>       make + render + encode + qa
"""
import sys, shutil, subprocess
from .config import COMPANIES, ROOT, WEB
from . import build as B, script as S

def main(argv):
    if len(argv) < 2: print(__doc__); return 1
    cmd, slug = argv[0], argv[1]
    if cmd == 'new':
        dst = COMPANIES / slug
        if dst.exists(): raise SystemExit(f'{dst} exists')
        shutil.copytree(ROOT / 'templates' / 'company', dst); print(f'created {dst}'); return 0
    if cmd == 'tts':
        content, sections = B.load(slug)
        print('=== Voice-over (Jessica) ===\n'); print(S.tts_text(sections))
        print('\n=== Intro (Jarnathan) ===\n'); print(B.intro_text(content)); return 0
    if cmd == 'check':
        content, sections = B.load(slug)
        empty = [k for k, v in sections.items() if v.strip() in ('', '...')]
        if empty: print('FILL IN script sections:', ', '.join(empty))
        for w in B.lint(content, sections): print('HINT', w)
        missing = [p for p in [content['voice']['take'], content['voice']['intro'], content['logo_light'], content['logo_dark']]
                   if not (B.paths(slug)[0] / p).exists()]
        if missing: print('MISSING files:', ', '.join(missing))
        print('check done'); return 0
    if cmd == 'make': B.make(slug); return 0
    if cmd == 'stills':
        _, bdir = B.paths(slug)
        subprocess.run(['node', str(WEB / 'render.js'), str(bdir / 'film.html'), 'stills', argv[2], str(bdir / 'stills')], check=True)
        print(f'stills in {bdir / "stills"}'); return 0
    if cmd == 'render': B.render(slug); return 0
    if cmd == 'encode': B.encode(slug); return 0
    if cmd == 'qa': B.qa(slug); return 0
    if cmd == 'all':
        B.make(slug); B.render(slug); B.encode(slug); B.qa(slug); return 0
    print(__doc__); return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
