// usage: FILM=build/x/film.html node web/scan_text.js out.json [step]
// Samples the film in output time and records, for every element that carries its own text,
// whether it is readable (effective opacity > .6, not covered at its centre). Writes runs per element.
const { chromium } = require('playwright-core');
const path = require('path'), fs = require('fs');
(async () => {
  const out = process.argv[2], step = +(process.argv[3] || 0.1);
  const exe = process.env.CHROME || ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome', '/usr/bin/chromium', '/usr/bin/google-chrome'].find(p => fs.existsSync(p));
  const browser = await chromium.launch({ executablePath: exe, args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(process.env.FILM));
  await page.evaluate(() => window.ready);
  await page.evaluate(() => {
    const own = e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
    window.__T = [...document.querySelectorAll('#stage *')].filter(e => !e.closest('svg') && own(e).length >= 3);
    window.__T.forEach((e, i) => e.dataset.ti = i);
    const opaque = e => { const cs = getComputedStyle(e); const m = cs.backgroundColor.match(/rgba?\(([^)]+)\)/); const al = m ? (m[1].split(',').length > 3 ? +m[1].split(',')[3] : 1) : 0; return e.tagName === 'IMG' || al > .5 || (cs.backgroundImage && cs.backgroundImage !== 'none'); };
    const T = new Set(window.__T);
    document.querySelectorAll('#stage *').forEach(e => { e.style.pointerEvents = (T.has(e) || (!e.closest('svg') && opaque(e))) ? 'auto' : 'none'; });
    window.__probe = () => window.__T.map(e => {
      let op = 1, x = e;
      while (x && x.id !== 'stage') { const cs = getComputedStyle(x); if (cs.visibility === 'hidden' || cs.display === 'none') return 0; op *= +cs.opacity; x = x.parentElement; }
      if (op < .6) return 0;
      const r = e.getBoundingClientRect(); if (r.width < 2 || r.height < 2) return 0;
      const cx = Math.min(1919, Math.max(0, r.left + Math.min(r.width, 60) / 2)), cy = Math.min(1079, Math.max(0, r.top + r.height / 2));
      const top = document.elementFromPoint(cx, cy);
      if (!top) return 0;
      return (top === e || e.contains(top) || top.contains(e)) ? 1 : 0;
    });
  });
  const dur = await page.evaluate(() => window.DUR);
  const texts = await page.evaluate(() => window.__T.map(e => ({ id: e.id || '', cls: e.className && e.className.baseVal === undefined ? e.className : '', text: [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').trim().slice(0, 90) })));
  const vis = texts.map(() => []);
  for (let t = 0; t < dur; t += step) {
    await page.evaluate(t => window.seek(t), t);
    const v = await page.evaluate(() => window.__probe());
    v.forEach((b, i) => vis[i].push(b));
  }
  const runs = [];
  vis.forEach((arr, i) => {
    let s = -1;
    arr.concat([0]).forEach((b, k) => {
      if (b && s < 0) s = k;
      if (!b && s >= 0) { runs.push({ i, text: texts[i].text, id: texts[i].id, t0: +(s * step).toFixed(2), t1: +(k * step).toFixed(2), d: +((k - s) * step).toFixed(2) }); s = -1; }
    });
  });
  fs.writeFileSync(out, JSON.stringify({ dur, step, runs }, null, 1));
  console.log('done', out, runs.length);
  await browser.close();
})();
