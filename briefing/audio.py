"""Sound: voice-over, interview, music and the final mix. Same chain for every film."""
import re, subprocess, numpy as np
from .config import SR, MUSIC_FILE, INTRO, ALOOP, TWO, BLOOP, MUSIC_TRIM_TARGET, VO_LUFS

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[-800:])
    return r

def decode(path, out, ch=1, af=None):
    run(f'ffmpeg -hide_banner -loglevel error -y -i "{path}" ' + (f'-af "{af}" ' if af else '') + f'-ac {ch} -ar {SR} -f f32le "{out}"')
    x = np.fromfile(out, dtype=np.float32)
    return x.reshape(-1, 2) if ch == 2 else x

def lufs(x, tmp):
    np.asarray(x, np.float32).tofile(tmp)
    ch = 2 if np.asarray(x).ndim == 2 else 1
    r = run(f'ffmpeg -hide_banner -f f32le -ar {SR} -ac {ch} -i "{tmp}" -af ebur128 -f null -').stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])

def act_rms(s):
    fr = s[:len(s) // 480 * 480].reshape(-1, 480); r = np.sqrt((fr ** 2).mean(1)); a = r[r > r.max() * 0.1]
    return float(np.sqrt((a ** 2).mean())) if len(a) else 1e-9

# ---------------- music ----------------
_music = None
def music_track(tmpdir):
    global _music
    if _music is None: _music = decode(MUSIC_FILE, f'{tmpdir}/_music.f32', ch=2)
    return _music

def hit_time(tmpdir):
    """The accent in the original track that lands on the TBV lock-up."""
    x = music_track(tmpdir).mean(1); k = int(0.02 * SR)
    e = np.sqrt(np.convolve(x ** 2, np.ones(k) / k, 'same')); a, b = int(80 * SR), int(87 * SR)
    d = e[a + int(.05 * SR):b] - e[a:b - int(.05 * SR)]
    return (a + int(d.argmax())) / SR + 0.03

def music_loops(jumps, tmpdir):
    x = music_track(tmpdir); n = int(0.03 * SR); h = n // 2; w = np.linspace(0, 1, n)[:, None]
    segs = []; cur = 0
    for p, L, k in jumps:
        P, LL = int(round(p * SR)), int(round(L * SR)); segs.append((cur, P))
        for _ in range(k - 1): segs.append((P - LL, P))
        cur = P
    segs.append((cur, len(x)))
    res = x[segs[0][0]:segs[0][1] + (h if len(segs) > 1 else 0)].copy()
    for a, b in segs[1:]:
        last = (b == len(x)); s_ = x[a - h:(b if last else b + h)].copy()
        res[-n:] = res[-n:] * (1 - w) + s_[:n] * w; res = np.concatenate([res, s_[n:]])
    return res.astype(np.float32)

def tune(hit_full, tmpdir, maxadd=4.2):
    """Loop counts so the music starts MUSIC_TRIM_TARGET into the track and its accent lands on
    the lock-up. Returns (jumps, add): `add` seconds must be inserted before the lock-up."""
    HIT = hit_time(tmpdir); best = None
    for i in range(1, 7):
        for a in range(1, 9):
            for t in range(1, 8):
                for b in range(1, 8):
                    ins = INTRO[1] * (i - 1) + ALOOP[1] * (a - 1) + TWO[1] * (t - 1) + BLOOP[1] * (b - 1)
                    add = HIT + ins - hit_full - MUSIC_TRIM_TARGET
                    if 0 <= add <= maxadd:
                        cost = add + .15 * (a + t + b) + .6 * max(0, b - 4) + .5 * max(0, a - 5) + .6 * max(0, t - 3) + .8 * abs(i - 4) + (.5 if a == 1 else 0)
                        if best is None or cost < best[0]: best = (cost, add, (i, a, t, b))
    if best is None: raise RuntimeError('no music loop combination fits this film length')
    i, a, t, b = best[2]
    return [INTRO + (i,), ALOOP + (a,), TWO + (t,), BLOOP + (b,)], best[1]

# ---------------- voice ----------------
def interview_bus(bus_it, vo_lufs, tmpdir):
    """Clean the interview bus and match its loudness to the voice-over."""
    p = f'{tmpdir}/_it.f32'; bus_it.astype(np.float32).tofile(p)
    run(f'ffmpeg -hide_banner -loglevel error -y -f f32le -ar {SR} -ac 1 -i "{p}" -af "highpass=f=90,afftdn=nr=13:nf=-52:tn=1,adeclick" -f f32le "{p}.c"')
    c = np.fromfile(f'{p}.c', dtype=np.float32)[1200:]          # afftdn adds 25 ms latency
    c = np.concatenate([c, np.zeros(len(bus_it) - len(c), np.float32)]) if len(c) < len(bus_it) else c[:len(bus_it)]
    c.tofile(p); best = None
    lo, hi = 1.0, 14.0
    for _ in range(7):
        mk = (lo + hi) / 2
        run(f'ffmpeg -hide_banner -loglevel error -y -f f32le -ar {SR} -ac 1 -i "{p}" -af "volume=6dB,acompressor=threshold=-18dB:ratio=2.2:attack=10:release=300:makeup={10 ** (mk / 20):.3f},alimiter=limit=0.8:level=false" -f f32le "{p}.o"')
        o = np.fromfile(f'{p}.o', dtype=np.float32); l = lufs(o, f'{tmpdir}/_t.f32')
        if best is None or abs(l - vo_lufs) < abs(best[0] - vo_lufs): best = (l, mk, o.copy())
        if l < vo_lufs: lo = mk
        else: hi = mk
    return best[2][:len(bus_it)], best[0]

def mixdown(voice_st, jumps, hit_full, D, last_voice, out_wav, tmpdir, boost=(7, 14, 0.1), fo=1.4):
    """Duck the music under the voice, lift it after the last word, fade at the end."""
    HIT = hit_time(tmpdir)
    voice_st.astype(np.float32).tofile(f'{tmpdir}/voice_full.f32')
    m = music_loops(jumps, tmpdir); m.tofile(f'{tmpdir}/music.f32')
    ins = sum(L * (k - 1) for p, L, k in jumps); trim = HIT + ins - hit_full
    assert trim >= 0 and len(m) / SR - trim >= D - 0.05, (trim, len(m) / SR, D)
    bm, br, bd = boost
    cmd = (f'ffmpeg -hide_banner -loglevel error -y -f f32le -ar {SR} -ac 2 -i "{tmpdir}/voice_full.f32" -f f32le -ar {SR} -ac 2 -i "{tmpdir}/music.f32" -filter_complex '
           f'"[0:a]volume=-3dB,alimiter=limit=0.84:level=false,asplit=2[voice][sc];[1:a]atrim=start={trim:.4f},asetpts=PTS-STARTPTS,atrim=0:{D},volume=-14dB,'
           f"volume=volume='pow(10,min({bm},max(0,(t-{last_voice + bd:.2f})*{br}))/20)':eval=frame,afade=t=in:st=0:d=0.5,afade=t=out:st={D - fo:.2f}:d={fo}[m];"
           f'[m][sc]sidechaincompress=threshold=0.09:ratio=2.5:attack=15:release=400[md];[voice][md]amix=inputs=2:normalize=0,alimiter=limit=0.84:level=false[a]" '
           f'-map "[a]" -t {D} -ar {SR} -ac 2 "{out_wav}"')
    run(cmd)
    r = run(f'ffmpeg -hide_banner -i "{out_wav}" -af ebur128=peak=true -f null -').stderr
    return dict(lufs=float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1]), peak=float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r)[-1]), trim=round(trim, 3))

# ---------------- checks ----------------
def blips(x, thr=-42):
    """Isolated speech fragments (a syllable cut off a neighbouring sentence)."""
    n = int(.01 * SR); e = 20 * np.log10(np.sqrt((x[:len(x) // n * n].reshape(-1, n) ** 2).mean(1)) + 1e-9)
    on = e > thr; out = []; i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j + 1 < len(on) and on[j + 1]: j += 1
            pre, post = e[max(0, i - 30):i], e[j + 1:j + 31]
            if (j - i + 1) / 100 < .18 and len(pre) and len(post) and pre.max() < -50 and post.max() < -50: out.append(round(i / 100, 2))
            i = j + 1
        else: i += 1
    return out

def tts_beeps(x):
    """ElevenLabs artefact: a stationary ~660 Hz harmonic tone. Returns suspicious times."""
    try: import parselmouth
    except ImportError: return []
    s = parselmouth.Sound(x.astype(np.float64), sampling_frequency=SR)
    p = s.to_pitch_ac(time_step=0.005, pitch_floor=75, pitch_ceiling=1100, voicing_threshold=0.45)
    f = p.selected_array['frequency']; t = p.xs(); out = []
    hi = (f > 640) & (f < 690); i = 0
    while i < len(hi):
        if hi[i]:
            j = i
            while j + 1 < len(hi) and hi[j + 1]: j += 1
            if (j - i + 1) * .005 >= .04:
                a, b = t[i] - .02, t[j] + .02; seg = x[int(a * SR):int(b * SR)]; N = 16384
                X = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), N)) ** 2; fr = np.fft.rfftfreq(N, 1 / SR); best = 0
                for F in np.arange(655, 672, .5):
                    pk = []
                    for k in range(3, 10):
                        m = np.abs(fr - k * F) < 5; rr = (np.abs(fr - k * F) > 25) & (np.abs(fr - k * F) < 80)
                        pk.append(10 * np.log10(X[m].max() / (np.median(X[rr]) + 1e-20) + 1e-12))
                    best = max(best, float(np.median(pk)))
                if best > 9: out.append(round(float(t[i]), 2))
            i = j + 1
        else: i += 1
    return out
