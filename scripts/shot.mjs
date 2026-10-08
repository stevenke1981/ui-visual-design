#!/usr/bin/env node
// Screenshot + overflow measurement for a local HTML page via headless Chrome/Edge (CDP).
// Requires Node 22+ (global WebSocket). No npm dependencies, throwaway browser profile.
//
//   node shot.mjs <page.html|http://127.0.0.1:port/page> <outDir>
//        [--widths 360,768,1280] [--height 900] [--schemes light,dark]
//        [--query "a=1&b=2"] [--state preview.js] [--full]
//
// --state: a JS file evaluated in the page after load, to render a state for
//   *visual preview only* (e.g. set body.dataset.state, fill numbers). Label such
//   screenshots as previews; they are not functional verification.
// Prints one line per shot: OK/OVERFLOW, scrollWidth vs clientWidth, offending elements.
// Exit code 1 if any shot overflows horizontally.
import {spawn} from 'node:child_process';
import {existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, resolve, basename, extname} from 'node:path';
import {pathToFileURL} from 'node:url';

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf('--' + name); return i >= 0 ? args[i + 1] : def; };
const flag = name => args.includes('--' + name);
const valued = new Set(['--widths', '--height', '--schemes', '--query', '--state']);
const [page, outDir] = args.filter((a, i) => !a.startsWith('--') && !valued.has(args[i - 1]));
if (!page || !outDir) { console.error('usage: node shot.mjs <page> <outDir> [--widths ..] [--schemes ..] [--state file.js] [--query ..] [--full]'); process.exit(2); }

const widths = opt('widths', '360,768,1280').split(',').map(Number);
const height = Number(opt('height', '900'));
const schemes = opt('schemes', 'light,dark').split(',');
const query = opt('query', '');
const stateJs = opt('state') ? readFileSync(opt('state'), 'utf8') : '';
let url = /^https?:|^file:/.test(page) ? page : pathToFileURL(resolve(page)).href;
if (query) url += (url.includes('?') ? '&' : '?') + query;
const stem = basename(page.split('?')[0], extname(page.split('?')[0])) || 'page';
mkdirSync(outDir, {recursive: true});

const candidates = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/microsoft-edge',
];
const exe = process.env.CHROME_PATH || candidates.find(existsSync);
if (!exe) { console.error('No Chrome/Edge found; set CHROME_PATH'); process.exit(2); }

const profile = mkdtempSync(join(tmpdir(), 'shot-'));
const port = 9300 + Math.floor(Math.random() * 500);
const browser = spawn(exe, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
  `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`, 'about:blank'], {stdio: 'ignore'});

const sleep = ms => new Promise(r => setTimeout(r, ms));
let target;
for (let i = 0; i < 50 && !target; i++) {
  try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(t => t.type === 'page'); } catch { await sleep(200); }
}
if (!target) { browser.kill(); console.error('browser did not start'); process.exit(2); }

const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let seq = 0; const waiting = new Map(); const events = [];
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); } else events.push(m); };
const send = (method, params = {}) => new Promise((r, j) => { const id = ++seq; waiting.set(id, m => m.error ? j(Error(method + ': ' + m.error.message)) : r(m.result)); ws.send(JSON.stringify({id, method, params})); });
const evaluate = async expr => (await send('Runtime.evaluate', {expression: expr, awaitPromise: true, returnByValue: true})).result.value;

await send('Page.enable');
await send('Runtime.enable');
let overflowed = false;
const measure = `(() => {
  const de = document.documentElement, cw = de.clientWidth;
  const off = [...document.querySelectorAll('body *')].filter(el => { const r = el.getBoundingClientRect(); return r.width && (r.right > cw + 1 || r.left < -1); })
    .slice(0, 5).map(el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\\s+/).join('.') : '') + '(' + Math.round(el.getBoundingClientRect().right) + 'px)');
  return {sw: de.scrollWidth, cw, off, errors: window.__shotErrors || []};
})()`;

try {
  for (const width of widths) for (const scheme of schemes) {
    await send('Emulation.setDeviceMetricsOverride', {width, height, deviceScaleFactor: 1, mobile: width < 600});
    await send('Emulation.setEmulatedMedia', {features: [{name: 'prefers-color-scheme', value: scheme}]});
    await send('Page.addScriptToEvaluateOnNewDocument', {source: 'window.__shotErrors=[];addEventListener("error",e=>__shotErrors.push(String(e.message)));'});
    events.length = 0;
    await send('Page.navigate', {url});
    for (let i = 0; i < 50 && !events.some(e => e.method === 'Page.loadEventFired'); i++) await sleep(100);
    await evaluate('document.fonts ? document.fonts.ready.then(() => 1) : 1');
    if (stateJs) await evaluate(`(async () => { ${stateJs}\n })()`);
    await sleep(150);
    const m = await evaluate(measure);
    const shotParams = {format: 'png'};
    if (flag('full')) {
      const h = await evaluate('document.documentElement.scrollHeight');
      shotParams.clip = {x: 0, y: 0, width, height: Math.min(h, 8000), scale: 1};
      shotParams.captureBeyondViewport = true;
    }
    const {data} = await send('Page.captureScreenshot', shotParams);
    const file = join(outDir, `${stem}${stateJs ? '-preview' : ''}-${width}-${scheme}.png`);
    writeFileSync(file, Buffer.from(data, 'base64'));
    const over = m.sw > m.cw;
    overflowed ||= over;
    console.log(`${over ? 'OVERFLOW' : 'OK      '} ${width}px ${scheme.padEnd(5)} scrollWidth=${m.sw} clientWidth=${m.cw}${over ? ' offenders: ' + m.off.join(', ') : ''}${m.errors.length ? ' JS errors: ' + m.errors.join(' | ') : ''}  -> ${file}`);
  }
} finally {
  ws.close(); browser.kill();
  await sleep(300);
  try { rmSync(profile, {recursive: true, force: true}); } catch {}
}
process.exit(overflowed ? 1 : 0);
