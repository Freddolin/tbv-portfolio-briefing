// node web/render.js <page.html> <first frame> <last frame (excl.)> <out dir> [fps]
// Renders frames of a GSAP film page by seeking its paused timeline. Run several in parallel for speed.
const path = require('path'), fs = require('fs');
const { chromium } = require('playwright-core');
const exe = () => process.env.CHROME || ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome', '/usr/bin/chromium', '/usr/bin/google-chrome']
  .find(p => fs.existsSync(p));
(async () => {
  const [page_, a, b, out, fps_] = process.argv.slice(2); const fps = +(fps_ || 25);
  const browser = await chromium.launch({ executablePath: exe(), args: ['--allow-file-access-from-files', '--font-render-hinting=none', '--disable-lcd-text'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('PAGE EXC:', e.message));
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('PAGE', m.type(), m.text()); });
  await page.goto('file://' + path.resolve(page_));
  await page.evaluate(() => window.ready);
  fs.mkdirSync(out, { recursive: true });
  if (a === 'stills') {
    for (const t of b.split(',').map(Number)) {
      await page.evaluate(t => window.seek(t), t);
      await page.screenshot({ path: `${out}/s_${t.toFixed(2).padStart(7, '0')}.jpg`, type: 'jpeg', quality: 82 });
    }
  } else {
    for (let f = +a; f < +b; f++) {
      await page.evaluate(t => window.seek(t), f / fps);
      await page.screenshot({ path: `${out}/f_${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
    }
  }
  await browser.close();
})();
