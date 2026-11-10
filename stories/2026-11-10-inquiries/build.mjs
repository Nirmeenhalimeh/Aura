// Renders today's 4 stories to 1080x1920 PNGs: node build.mjs
// Text sits between y=260 and y=1560 (Instagram covers the top and bottom with its UI).
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const {chromium} = createRequire(import.meta.url)('playwright'); // the globally installed Playwright

const DIR = path.dirname(fileURLToPath(import.meta.url));
const C = {ink: '#0E0F13', ivory: '#F4F1EA', gold: '#C9A46A', navy: '#0B1930'};

const face = (w) =>
  ['arabic', 'latin']
    .map(
      (s) => `@font-face{font-family:Plex;font-weight:${w};src:url(fonts/ibm-plex-sans-arabic-${s}-${w}-normal.woff2) format('woff2');${
        s === 'arabic' ? 'unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF,U+200C-200F;' : ''
      }}`,
    )
    .join('');

const page = (body, bg, extra = '') => `<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>
${face(400)}${face(700)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px}
body{background:${bg};font-family:Plex,'Noto Color Emoji',sans-serif;color:${C.ivory};position:relative;overflow:hidden}
.safe{position:absolute;left:96px;right:96px;top:260px;bottom:360px;display:flex;flex-direction:column}
.gold{color:${C.gold}}
.rule{width:120px;height:3px;background:${C.gold};border-radius:2px}
${extra}
</style></head><body>${body}</body></html>`;

const warm = `radial-gradient(900px 900px at 85% 12%, rgba(201,164,106,0.28), rgba(201,164,106,0) 70%),
  radial-gradient(700px 700px at 10% 95%, rgba(201,164,106,0.10), rgba(201,164,106,0) 70%), ${C.ink}`;

const s1Body = (shadow) => `
<div class="safe" style="justify-content:center;gap:44px${shadow ? ';text-shadow:0 2px 24px rgba(0,0,0,0.55)' : ''}">
  <p style="font-size:52px;line-height:1.45;opacity:.85">بالاستطلاع الماضي سألتكن عن الاستفسارات…</p>
  <div>
    <p class="gold" style="font-size:150px;font-weight:700;line-height:1.15;white-space:nowrap">7 من أصل 10</p>
    <p style="font-size:64px;font-weight:700;line-height:1.4">صوّتوا: «ما عم توصلني» 🔎</p>
  </div>
  <div class="rule"></div>
  <p style="font-size:58px;line-height:1.4">فقررت أكتب عنها اليوم.</p>
</div>`;

const stories = {
  's1-poll-link': page(s1Body(false), warm),
  's1-overlay-for-your-photo': page(s1Body(true), 'transparent'),
  's2-to-carousel': page(
    `<div class="safe" style="gap:36px">
      <p style="font-size:54px;line-height:1.45">أول ردة فعل لما ما في استفسارات:<br>«لازم أنشر أكتر».</p>
      <p class="gold" style="font-size:112px;font-weight:700;line-height:1.15">مو بالضرورة.</p>
      <p style="font-size:56px;font-weight:700;line-height:1.4">في 4 نقاط بتستاهل الفحص قبل 👇</p>
    </div>`,
    warm,
  ),
  's3-listening-poll': page(
    `<div class="safe" style="gap:40px;padding-top:180px">
      <div class="rule"></div>
      <p style="font-size:76px;font-weight:700;line-height:1.4">لما ما يوصلك ولا استفسار لفترة، شو أول شي بتعمليه؟</p>
    </div>`,
    C.navy,
  ),
  's4-qualified-invite': page(
    `<div style="position:absolute;top:0;bottom:0;right:96px;width:3px;background:${C.gold};opacity:.9"></div>
    <div class="safe" style="right:150px;justify-content:center;gap:48px;color:${C.ink}">
      <p style="font-size:66px;font-weight:700;line-height:1.4">فحصتي النقاط الأربعة…<br>وما عرفتي وين الفجوة عندك؟</p>
      <p style="font-size:56px;line-height:1.4">هون بيجي دور <span style="font-weight:700;border-bottom:5px solid ${C.gold};padding-bottom:2px">التشخيص</span>:</p>
      <p style="font-size:46px;line-height:1.6;opacity:.78">بنراجع الحساب والبيانات، وبنحدد شو اللي عم يصير فعليًا قبل ما تغيّري أي شي.</p>
      <p style="align-self:flex-start;font-size:58px;font-weight:700;line-height:1.3;border:3px solid ${C.gold};border-radius:24px;padding:30px 44px">ابعتيلي «تشخيص» برسالة 🤍</p>
    </div>`,
    C.ivory,
  ),
};

const browser = await chromium.launch();
const tab = await browser.newPage({viewport: {width: 1080, height: 1920}, deviceScaleFactor: 1});
for (const [name, html] of Object.entries(stories)) {
  const file = path.join(DIR, `${name}.html`);
  fs.writeFileSync(file, html);
  await tab.goto('file://' + file);
  await tab.evaluate(() => document.fonts.ready);
  await tab.screenshot({path: path.join(DIR, 'out', `${name}.png`), omitBackground: name.includes('overlay')});
  fs.unlinkSync(file);
  console.log('→ out/' + name + '.png');
}
await browser.close();
