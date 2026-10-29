"""Turns content + aligned voice-over + interview segments into a film: one block after another,
every block as long as its audio and its texts need. No hand-set timings anywhere."""
from .config import BLOCK_ORDER

LEAD = dict(problem=.5, handover=.3, how=.5, q_ds=.45, why=.6, ds_a=.55, ds_b=.5, ds_c=.5, ds_d=.5, q_founders=.45, q_words=.45, close=.4)
TAIL = dict(problem=.8, handover=.25, how=.7, q_ds=.35, why=.8, ds_a=.7, ds_b=.7, ds_c=.7, ds_d=.8, q_founders=.35, q_words=.35, close=.0)

class Block:
    def __init__(self, key, idx, t0):
        self.key, self.idx, self.t0 = key, idx, t0
        self.sid = f'b{idx:02d}{key.replace("_", "")}'
        self.warnings = []

def build(content, take, segs, pad=None):
    """take: align.Take of the voice-over; segs: interview.prepare() result.
    pad: optional extra seconds per block key (music fit). Returns (blocks, scenes, audio placements, duration)."""
    from .scenes import film as F, ds as DS
    pad = pad or {}
    t = 0.0; blocks, scenes, place = [], [], []
    for i, key in enumerate(BLOCK_ORDER):
        b = Block(key, i, t)
        if key in segs:                                    # interview
            seg = content['interview'][key]; info = segs[key]
            seg = dict(seg, _joins=info['joins'])
            b.t_speech = t + .05; b.t_audio_end = b.t_speech + info['dur']
            b.t_end = b.t_audio_end + .15 + pad.get(key, 0)
            sc = F.founder(b, content, key, seg)
            if sc.need > b.t_end:
                b.warnings.append(f'{key}: last words need {sc.need - b.t_end:.1f}s more; holding the last frame')
                b.t_end = sc.need; sc = F.founder(b, content, key, seg)
            place.append(('int', key, 0.0, info['dur'], b.t_speech))
        else:                                              # voice-over block
            delays = {}                                    # take time of a cut -> seconds of pause inserted there
            for _ in range(6):
                b = _vo_block(Block(key, i, t), key, take, delays, pad)
                sc = _scene(F, DS, b, content, key)
                if sc.need > b.t_end + 1e-3:
                    b.t_end = sc.need; sc = _scene(F, DS, b, content, key)
                todo = [(a, s_) for a, s_ in sc.holds if s_ > .05]
                if not todo: break
                for a, s_ in todo:
                    cut = _cut_before(take, key, a)
                    delays[cut] = round(delays.get(cut, 0) + s_ + .1, 3)
            else:
                b.warnings.append(f'{key}: could not give every text enough time')
            for lo, hi in b.chunks: place.append(('vo', key, lo, hi, b.M(lo)))
        blocks.append(b); scenes.append(sc); t = b.t_end
    return blocks, scenes, place, t

def _vo_block(b, key, take, delays, pad):
    """Voice-over block with optional pauses (delays) at cut points inside the section."""
    t = b.t0; off = t + LEAD[key] - take.start(key)
    splits = sorted(delays.items())
    def M(tau): return tau + off + sum(d for s_, d in splits if s_ <= tau + 1e-6)
    b.M = M; b.nsent = len(take.sec[key]); b.off = off
    b.t_speech = M(take.start(key)); b.t_audio_end = M(take.end(key))
    b.T = lambda anchor, k=key: M(take.find(k, anchor))
    lo, hi = take.bounds[key]; pts = [lo] + [s_ for s_, _ in splits if lo < s_ < hi] + [hi]
    b.chunks = list(zip(pts[:-1], pts[1:]))
    b.t_end = b.t_audio_end + TAIL[key] + pad.get(key, 0)
    if key == 'close':
        b.t_lock = max(b.t_audio_end + .6, b.T('s1') + 2.6 + .4) + pad.get(key, 0)
        b.t_end = b.t_lock + 3.4
    return b

def _cut_before(take, key, anchor):
    """Quiet moment right before an anchor: where a pause can be inserted without cutting a word."""
    from .align import quiet_point
    ta = take.find(key, anchor)
    flat = [w for s in take.sec[key] for w in s['words']]
    prev = [w[2] for w in flat if w[2] <= ta + 1e-6]
    pe = prev[-1] if prev else ta - .2
    return round(quiet_point(take.env, min(pe, ta) - .03, ta + .03), 3)

def _scene(F, DS, b, c, key):
    if key == 'problem': return F.explainer(b, c, 'problem', c['problem'])
    if key == 'how': return F.explainer(b, c, 'how', c['how'])
    if key == 'handover': return F.handover(b, c)
    if key == 'q_ds': return F.question(b, c, c.get('questions', {}).get('q_ds', 'What does that mean<br>for Drees & Sommer?'), 'dk')
    if key == 'q_founders': return F.question(b, c, c.get('questions', {}).get('q_founders', 'What do the founders<br>get from us?'), 'wm')
    if key == 'q_words': return F.question(b, c, c.get('questions', {}).get('q_words', 'The Bau Ventures,<br>in three words?'), 'wm')
    if key == 'why': return F.why(b, c, c['why'])
    if key.startswith('ds_'): return DS.screen(b, c, key[-1], c['ds'][key[-1]])
    if key == 'close': return F.close(b, c, c['close'])
    raise KeyError(key)
