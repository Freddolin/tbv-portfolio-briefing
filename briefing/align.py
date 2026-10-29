"""Forced alignment of a voice-over take against its script (pocketsphinx), plus safe cut points.
Gives word, sentence and section times; everything on screen is cued from these."""
import re, subprocess, difflib, numpy as np
from .config import SR
from . import script as S

# pronunciations pocketsphinx does not know (ARPAbet). Companies add their own via content.yaml 'pronounce'.
EXTRA = {'dreso': 'D R EH S OW', 'sommer': 'S AA M ER', "sommer's": 'S AA M ER Z', 'bau': 'B AW', 'proptech': 'P R AA P T EH K',
         'contech': 'K AA N T EH K', 'capex': 'K AE P EH K S', 'prefab': 'P R IY F AE B', 'prefabricated': 'P R IY F AE B R AH K EY T AH D',
         'decarbonisation': 'D IY K AA R B AH N AH Z EY SH AH N', 'programmes': 'P R OW G R AE M Z', 'optimises': 'AA P T AH M AY Z AH Z',
         'qr': 'K Y UW AA R', 'dach': 'D AE K'}

_DI = [('tion', 'SH AH N'), ('sch', 'SH'), ('tch', 'CH'), ('ch', 'CH'), ('sh', 'SH'), ('th', 'TH'), ('ph', 'F'), ('ck', 'K'), ('ng', 'NG'),
       ('qu', 'K W'), ('ee', 'IY'), ('ea', 'IY'), ('oo', 'UW'), ('ou', 'AW'), ('ow', 'OW'), ('ai', 'EY'), ('ay', 'EY'), ('ei', 'AY'),
       ('ie', 'IY'), ('oa', 'OW'), ('au', 'AO'), ('er', 'ER'), ('ar', 'AA R'), ('or', 'AO R'), ('ur', 'ER')]
_SI = dict(a='AE', b='B', c='K', d='D', e='EH', f='F', g='G', h='HH', i='IH', j='JH', k='K', l='L', m='M', n='N', o='AA', p='P',
           q='K', r='R', s='S', t='T', u='AH', v='V', w='W', x='K S', y='IY', z='Z')
_DIG = dict(zip('0123456789', ['Z IH R OW', 'W AH N', 'T UW', 'TH R IY', 'F AO R', 'F AY V', 'S IH K S', 'S EH V AH N', 'EY T', 'N AY N']))

def g2p(w):
    """Crude letter-to-sound fallback, good enough for alignment of names."""
    w = w.lower().replace("'", ''); out = []; i = 0
    while i < len(w):
        for d, p in _DI:
            if w.startswith(d, i):
                out.append(p); i += len(d); break
        else:
            c = w[i]
            if c in _DIG: out.append(_DIG[c])
            elif c in _SI and not (c == 'e' and i == len(w) - 1 and len(w) > 2): out.append(_SI[c])
            i += 1
    return ' '.join(out) or 'AH'

def align_take(audio_path, text, extra=None):
    """Return [(word, start, end)] for every word of `text` in the take."""
    extra = {**EXTRA, **(extra or {})}
    raw = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(audio_path), '-ar', '16000', '-ac', '1', '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    from pocketsphinx import Decoder
    d = Decoder(samprate=16000, bestpath=False, loglevel='FATAL')
    ws = S.words(text)
    for w in set(ws):
        if d.lookup_word(w) is None:
            if w in extra: d.add_word(w, extra[w], True)
            elif '-' in w and all(d.lookup_word(p) for p in w.split('-')):
                d.add_word(w, ' '.join(d.lookup_word(p) for p in w.split('-')), True)
            else: d.add_word(w, g2p(w), True)
    d.set_align_text(' '.join(ws))
    d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
    al = d.get_alignment()
    if al is not None: res = [(s.name, s.start / 100, (s.start + s.duration) / 100) for s in al]
    else: res = [(s.word, s.start_frame / 100, (s.end_frame + 1) / 100) for s in d.seg()]
    res = [(re.sub(r'\(\d+\)$', '', a), b, c) for a, b, c in res if a not in ('<s>', '</s>', '<sil>', '[NOISE]')]
    if len(res) != len(ws):
        raise RuntimeError(f'alignment failed: {len(res)} of {len(ws)} words; check that the take matches the script')
    return res, len(raw) / 32000

def envelope(audio_f32, hop=0.01):
    n = int(hop * SR)
    x = audio_f32[:len(audio_f32) // n * n].reshape(-1, n)
    return 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1e-9)

def quiet_point(env, a, b, hop=0.01):
    """Quietest moment between a and b (s)."""
    i0, i1 = int(a / hop), max(int(a / hop) + 1, int(b / hop))
    w = env[i0:i1]
    sm = np.convolve(w, np.ones(3) / 3, 'same')
    return (i0 + int(sm.argmin())) * hop + hop / 2

class Take:
    """A voice-over take mapped onto script sections and sentences."""
    def __init__(self, audio_path, sections, audio_f32, extra=None):
        self.sections = sections
        text = S.tts_text(sections)
        self.words, self.dur = align_take(audio_path, text, extra)
        self.env = envelope(audio_f32)
        self.sec = {}; i = 0
        for k, t in sections.items():
            sents = []
            for snt in S.sentences(t):
                n = len(S.words(snt)); seg = self.words[i:i + n]; i += n
                sents.append(dict(text=snt, start=seg[0][1], end=seg[-1][2], words=seg))
            self.sec[k] = sents
        # refine the very first onset by energy (alignment puts it at 0)
        first = self.sec[list(sections)[0]][0]
        on = np.argmax(self.env > self.env.max() - 40) * 0.01
        first['start'] = max(first['start'], on - 0.02)
        keys = list(sections)
        self.bounds = {}
        for j, k in enumerate(keys):
            s0, s1 = self.sec[k][0]['start'], self.sec[k][-1]['end']
            lo = max(0.0, s0 - 0.15); hi = min(self.dur, s1 + 0.45)
            if j > 0:
                pe = self.sec[keys[j - 1]][-1]['end']; lo = max(lo, quiet_point(self.env, pe - .03, s0 + .03))
            if j + 1 < len(keys):
                ns = self.sec[keys[j + 1]][0]['start']; hi = min(hi, quiet_point(self.env, s1 - .03, ns + .03))
            self.bounds[k] = (round(lo, 3), round(hi, 3))

    def start(self, k): return self.sec[k][0]['start']
    def end(self, k): return self.sec[k][-1]['end']

    def find(self, k, anchor, after=0.0):
        """Time (take seconds) of an anchor inside section k.
        anchor: 's2' = start of sentence 2 (0-based), 'e2' = end of sentence 2, float = seconds after section start,
        or text = start of the first matching word sequence at/after `after`."""
        sents = self.sec[k]
        if isinstance(anchor, (int, float)): return self.start(k) + float(anchor)
        a = str(anchor).strip()
        m = re.fullmatch(r'([se])(-?\d+)', a)
        if m:
            j = int(m.group(2))
            if not -len(sents) <= j < len(sents): raise KeyError(f'anchor "{anchor}": section {k} has only {len(sents)} sentences (s0..s{len(sents) - 1})')
            s = sents[j]
            return s['start'] if m.group(1) == 's' else s['end']
        target = S.words(a)
        flat = [w for s in sents for w in s['words']]
        for i in range(len(flat) - len(target) + 1):
            if flat[i][1] + 1e-6 >= after and [w[0] for w in flat[i:i + len(target)]] == target:
                return flat[i][1]
        raise KeyError(f'anchor "{anchor}" not found in section {k} (after {after:.2f}s)')

    def find_end(self, k, anchor):
        target = S.words(str(anchor)); flat = [w for s in self.sec[k] for w in s['words']]
        for i in range(len(flat) - len(target) + 1):
            if [w[0] for w in flat[i:i + len(target)]] == target: return flat[i + len(target) - 1][2]
        raise KeyError(f'anchor "{anchor}" not found in section {k}')

def asr_check(audio_path, take, min_ratio=0.35, min_words=4):
    """Free speech recognition per sentence; low similarity flags a sentence to listen to."""
    from pocketsphinx import Decoder
    raw = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(audio_path), '-ar', '16000', '-ac', '1', '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    d = Decoder(samprate=16000, loglevel='FATAL'); flags = []
    for k, sents in take.sec.items():
        for s in sents:
            if len(S.words(s['text'])) < min_words: continue
            seg = raw[int(max(0, s['start'] - .15) * 16000) * 2:int((s['end'] + .15) * 16000) * 2]
            d.start_utt(); d.process_raw(seg, full_utt=True); d.end_utt()
            h = d.hyp().hypstr if d.hyp() else ''
            r = difflib.SequenceMatcher(None, S.words(s['text']), h.split()).ratio()
            if r < min_ratio: flags.append((k, round(s['start'], 2), round(r, 2), s['text']))
    return flags
