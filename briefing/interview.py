"""Founder interview segments: cut frames and audio from the source files.

content.yaml:
  interview:
    f1:                       # four fixed segments f1..f4 (see docs/PROCESS.md)
      founder: 0              # index into founders
      parts:                  # one or more selects, played back to back
        - {video: media/a.mp4, in: 12.4, dur: 9.8}                         # audio from the same file
        - {video: media/b.mp4, in: 0, dur: 6.2, audio: media/rec.wav, ain: 24.3}   # separate recorder
"""
import subprocess, hashlib, json, os, numpy as np
from pathlib import Path
from .config import FPS, SR

def _ts(v):
    if isinstance(v, (int, float)): return float(v)
    parts = [float(x) for x in str(v).split(':')]
    t = 0.0
    for p in parts: t = t * 60 + p
    return t

def _run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[-800:])
    return r

def prepare(company_dir, segs, out_dir):
    """Extract frames + raw mono audio for every segment. Cached by spec hash.
    Returns {seg: dict(n, dur, frames_prefix, audio (np.float32), joins)}."""
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True); res = {}
    for key, seg in segs.items():
        parts = seg['parts']
        spec = json.dumps(parts, sort_keys=True); hsh = hashlib.md5(spec.encode()).hexdigest()[:10]
        d = out_dir / key; mark = d / f'.ok_{hsh}'
        joins, t, audios = [], 0.0, []
        if not mark.exists():
            if d.exists():
                for f in d.iterdir(): f.unlink()
            d.mkdir(exist_ok=True); idx = 1
            for k, p in enumerate(parts):
                vin, dur = _ts(p['in']), _ts(p['dur'])
                n = int(round(dur * FPS))
                src = Path(company_dir) / p['video']
                tmp = d / f'_p{k}'; tmp.mkdir(exist_ok=True)
                _run(f'ffmpeg -hide_banner -loglevel error -y -ss {vin:.3f} -i "{src}" -frames:v {n} '
                     f'-vf "fps={FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" -q:v 3 "{tmp}/f_%04d.jpg"')
                got = sorted(tmp.iterdir())
                for f in got:
                    f.rename(d / f'f_{idx:04d}.jpg'); idx += 1
                tmp.rmdir()
                asrc = Path(company_dir) / p.get('audio', p['video']); ain = _ts(p.get('ain', p['in']))
                _run(f'ffmpeg -hide_banner -loglevel error -y -ss {ain:.3f} -t {dur:.3f} -i "{asrc}" -vn -ac 1 -ar {SR} -f f32le "{d}/_a{k}.f32"')
            mark.touch()
        n_tot = len([f for f in d.iterdir() if f.name.startswith('f_')])
        for k, p in enumerate(parts):
            a = np.fromfile(d / f'_a{k}.f32', dtype=np.float32)
            if k: joins.append(round(t, 3))
            audios.append(a); t += _ts(p['dur'])
        res[key] = dict(n=n_tot, dur=n_tot / FPS, prefix=f'clips/{key}/f_', audio=_join(audios), joins=joins)
    return res

def _join(chunks, xf=0.012):
    """Concatenate audio parts with short fades so cuts never click."""
    n = int(xf * SR); out = []
    for c in chunks:
        c = c.copy()
        if len(c) > 2 * n: c[:n] *= np.linspace(0, 1, n); c[-n:] *= np.linspace(1, 0, n)
        out.append(c)
    return np.concatenate(out) if out else np.zeros(0, np.float32)
