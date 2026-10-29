# TBV Portfolio Briefing

Template and build pipeline for The Bau Ventures' internal portfolio briefing films
(one per portfolio company: who we backed, why, and what it means for Drees & Sommer).
Every film is built the same way: same structure, look, music, voices, cuts and checks.
Only `companies/<slug>/content.yaml`, `script.md` and the media change.

Internal use only. Private repository.

## Quick start

```bash
pip install -r requirements.txt --break-system-packages   # numpy, pyyaml, pocketsphinx, praat-parselmouth
npm install                                               # gsap, archivo font, playwright-core
# needs ffmpeg and a Chromium (CHROME=/path/to/chrome if not found automatically)

python -m briefing new acme            # creates companies/acme/ from the template
# write companies/acme/script.md + content.yaml, put media into companies/acme/media/
python -m briefing check acme          # content rules
python -m briefing tts acme            # texts for ElevenLabs (voice-over + intro)
python -m briefing make acme           # align, cut interviews, timeline, page, sound
python -m briefing stills acme 5,40,90 # quick look at single frames (film time)
python -m briefing all acme            # make + render + encode + QA  (~20 min)
```

Output: `build/acme/Portfolio_Briefing_NN_Acme.mp4` and `build/acme/qa.md`.

## Docs
- [docs/PROCESS.md](docs/PROCESS.md): the steps, from research to delivery
- [docs/RULES.md](docs/RULES.md): content rules and sign-off
- [docs/CONTENT.md](docs/CONTENT.md): `content.yaml` reference
- `companies/optiml/`: complete example (media not in git)

## Layout
```
briefing/            python package (python -m briefing ...)
  config.py          fixed standards: colours, structure, readability, music, delivery
  script.py align.py voice-over script + forced alignment
  interview.py       cuts frames and audio from the founder interview
  timeline.py        blocks one after another, timed by the audio and by reading time
  scenes/            the fixed scene types (panels, why, D&S screens, founder, close)
  audio.py           music loops, interview clean-up, mix, sound checks
  build.py           make / render / encode / qa
web/                 render.js (frames), scan_text.js (readability check)
assets/              music, TBV lock-up, internal-use tag
templates/company/   starting point for a new company
companies/<slug>/    content.yaml, script.md, media/ (media is git-ignored)
```
