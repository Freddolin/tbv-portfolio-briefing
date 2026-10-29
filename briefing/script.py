"""Voice-over script: one markdown file per company, one '## <section>' per block of the film.
The text under each heading is exactly what goes into ElevenLabs."""
import re
from .config import SCRIPT_SECTIONS

def load(path):
    secs, cur = {}, None
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^##\s+(\w+)\s*$', line)
        if m:
            cur = m.group(1); secs[cur] = []
            continue
        if line.startswith('#') or cur is None:
            continue
        if line.strip().startswith('<!--'):
            continue
        secs[cur].append(line.rstrip('\n'))
    out = {k: ' '.join(' '.join(v).split()) for k, v in secs.items()}
    missing = [k for k in SCRIPT_SECTIONS if not out.get(k)]
    extra = [k for k in out if k not in SCRIPT_SECTIONS]
    if missing or extra:
        raise ValueError(f'script sections missing {missing} / unknown {extra}; expected {SCRIPT_SECTIONS}')
    return {k: out[k] for k in SCRIPT_SECTIONS}

def tts_text(sections):
    """Text to paste into ElevenLabs: sections in film order, separated by blank lines."""
    return '\n\n'.join(sections[k] for k in SCRIPT_SECTIONS)

def sentences(text):
    """Split a section into sentences the way alignment and anchors see them."""
    parts = re.split(r'(?<=[.?!:])\s+|\s*\[pause\]\s*', text.strip())
    return [p.strip() for p in parts if p and words(p)]

def words(text):
    t = re.sub(r'\[[a-z ]+\]', ' ', text.lower())
    t = t.replace('’', "'")
    t = re.sub(r"[^a-z0-9'\- ]", ' ', t.replace('\n', ' '))
    return [w.strip("'-") for w in t.split() if w.strip("'-")]
