"""
Builds PRACTICE.html: every slide with its script next to it, so the three of
us can rehearse without switching windows.

The real presentation still runs from final_deck.html or final_deck.pptx.
This page is only for practice: it has a per slide timer, a speaker filter and
a language switch.
"""
import base64
import html
import json
import os

import script_data as d

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "slides_png")


def img64(no):
    p = os.path.join(PNG, f"slide_{no:02d}.png")
    return base64.b64encode(open(p, "rb").read()).decode()


COLOURS = {"Sinha": "#1d4ed8", "Saimon": "#c2410c", "Faria": "#15803d"}

cards = []
for s in d.SLIDES:
    badge = ""
    if s.get("ask"):
        badge = '<span class="flag ask">audience কে প্রশ্ন করো</span>'
    elif s.get("key"):
        badge = '<span class="flag key">সবচেয়ে গুরুত্বপূর্ণ</span>'
    cards.append(f"""
<section class="slide-card" data-no="{s['no']}" data-who="{s['who']}" data-sec="{s['sec']}">
  <div class="stage"><img src="data:image/png;base64,{img64(s['no'])}" alt="Slide {s['no']}"></div>
  <div class="script">
    <div class="head">
      <span class="num">Slide {s['no']} / {len(d.SLIDES)}</span>
      <span class="who" style="background:{COLOURS[s['who']]}">{s['who']}</span>
      <span class="sec">{s['sec']} sec</span>
      {badge}
    </div>
    <h3>{html.escape(s['title'])}</h3>
    <div class="line en"><span class="lbl">EN</span><p>{html.escape(s['en'])}</p></div>
    <div class="line bn"><span class="lbl">BN</span><p>{html.escape(s['bn'])}</p></div>
    <div class="tip"><b>কীভাবে বলবে:</b> {html.escape(s['tip'])}</div>
  </div>
</section>""")

qa = "".join(f'<div class="qa"><b>{html.escape(q)}</b><p>{html.escape(a)}</p></div>' for q, a in d.QA)
per_speaker = "".join(
    f'<span class="pill" style="border-color:{COLOURS[w]};color:{COLOURS[w]}">{w}: slides '
    f'{ss[0]["no"]}-{ss[-1]["no"]}, {sum(x["sec"] for x in ss)//60}:{sum(x["sec"] for x in ss)%60:02d}</span>'
    for w, ss in d.BY_SPEAKER.items())

CSS = """
:root{--bg:#f6f5f2;--ink:#18202b;--soft:#5d6572;--line:#e2dfd8;--card:#fff;--accent:#c2410c}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans Bengali","Hind Siliguri","Segoe UI",system-ui,sans-serif;line-height:1.75}
header{position:sticky;top:0;z-index:20;background:rgba(246,245,242,.97);border-bottom:1px solid var(--line);padding:10px 16px;backdrop-filter:blur(6px)}
.bar{max-width:1500px;margin:0 auto;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
h1{font-size:17px;margin:0;font-weight:700}
.sub{font-size:13px;color:var(--soft)}
.pill{border:1.5px solid var(--line);border-radius:999px;padding:2px 10px;font-size:12.5px;margin-right:6px;background:#fff}
button{font:inherit;font-size:13.5px;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:8px;padding:6px 12px;cursor:pointer}
button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
button:active{transform:translateY(1px)}
.spacer{flex:1}
#timer{font-variant-numeric:tabular-nums;font-weight:700;font-size:16px;min-width:74px;text-align:center}
#timer.over{color:#b91c1c}
#timer.warn{color:#a16207}
main{max-width:1500px;margin:0 auto;padding:18px 16px 70px}
.slide-card{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(320px,.85fr);gap:18px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:20px;scroll-margin-top:74px}
.slide-card.hide{display:none}
.stage img{width:100%;border-radius:10px;display:block;border:1px solid var(--line)}
.head{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:6px}
.num{font-size:12.5px;color:var(--soft)}
.who{color:#fff;font-size:12.5px;font-weight:700;border-radius:999px;padding:2px 10px}
.sec{font-size:12.5px;color:var(--soft);border:1px solid var(--line);border-radius:999px;padding:1px 9px}
.flag{font-size:12px;font-weight:700;border-radius:999px;padding:2px 10px}
.flag.ask{background:#fef3c7;color:#92400e}
.flag.key{background:#fee2e2;color:#991b1b}
h3{margin:4px 0 10px;font-size:18px}
.line{display:flex;gap:10px;margin:10px 0}
.line p{margin:0;font-size:15.5px}
.lbl{flex:0 0 26px;height:20px;border-radius:5px;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;color:#fff;margin-top:3px}
.en .lbl{background:#1d4ed8}
.bn .lbl{background:#15803d}
.tip{margin-top:12px;background:#fbf7ef;border-left:4px solid var(--accent);border-radius:0 8px 8px 0;padding:9px 12px;font-size:14.5px}
.qa{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin-bottom:10px}
.qa b{display:block;margin-bottom:4px}
.qa p{margin:0;font-size:15px;color:var(--soft)}
h2{font-size:20px;margin:34px 0 12px}
.note{background:#fff;border:1px dashed var(--line);border-radius:12px;padding:12px 16px;font-size:14.5px;color:var(--soft);margin-bottom:18px}
@media(max-width:980px){.slide-card{grid-template-columns:1fr}}
@media print{header{position:static}.slide-card{break-inside:avoid;page-break-inside:avoid}}
"""

JS = """
const cards = [...document.querySelectorAll('.slide-card')];
let lang = 'both', who = 'All', idx = 0, left = 0, tick = null;

function visible(){ return cards.filter(c => !c.classList.contains('hide')); }
function apply(){
  cards.forEach(c => c.classList.toggle('hide', who !== 'All' && c.dataset.who !== who));
  document.body.classList.toggle('only-en', lang === 'en');
  document.body.classList.toggle('only-bn', lang === 'bn');
  const v = visible();
  const total = v.reduce((a, c) => a + (+c.dataset.sec), 0);
  document.getElementById('total').textContent =
    v.length + ' slides · ' + Math.floor(total/60) + ':' + String(total%60).padStart(2,'0');
  idx = Math.min(idx, Math.max(0, v.length - 1));
  show(idx, false);
}
function show(i, scroll = true){
  const v = visible(); if (!v.length) return;
  idx = (i + v.length) % v.length;
  const c = v[idx];
  if (scroll) c.scrollIntoView({behavior:'smooth', block:'start'});
  reset(+c.dataset.sec);
}
function fmt(s){ const m = Math.floor(Math.abs(s)/60), r = Math.abs(s)%60;
  return (s < 0 ? '-' : '') + m + ':' + String(r).padStart(2,'0'); }
function paint(){
  const t = document.getElementById('timer');
  t.textContent = fmt(left);
  t.classList.toggle('over', left < 0);
  t.classList.toggle('warn', left >= 0 && left <= 5);
}
function reset(sec){ clearInterval(tick); tick = null; left = sec; paint();
  document.getElementById('play').textContent = 'শুরু'; }
function toggle(){
  if (tick){ clearInterval(tick); tick = null; document.getElementById('play').textContent = 'চালু'; return; }
  document.getElementById('play').textContent = 'থামাও';
  tick = setInterval(() => { left--; paint(); }, 1000);
}
document.querySelectorAll('[data-who-btn]').forEach(b => b.onclick = () => {
  who = b.dataset.whoBtn;
  document.querySelectorAll('[data-who-btn]').forEach(x => x.classList.toggle('on', x === b));
  apply();
});
document.querySelectorAll('[data-lang]').forEach(b => b.onclick = () => {
  lang = b.dataset.lang;
  document.querySelectorAll('[data-lang]').forEach(x => x.classList.toggle('on', x === b));
  apply();
});
document.getElementById('prev').onclick = () => show(idx - 1);
document.getElementById('next').onclick = () => show(idx + 1);
document.getElementById('play').onclick = toggle;
addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT') return;
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown'){ e.preventDefault(); show(idx + 1); }
  else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp'){ e.preventDefault(); show(idx - 1); }
  else if (e.key === ' '){ e.preventDefault(); toggle(); }
});
apply();
"""

doc = f"""<!doctype html>
<html lang="bn"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Practice: slide আর script একসাথে</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}
body.only-en .bn{{display:none}} body.only-bn .en{{display:none}}
</style></head><body>

<header><div class="bar">
  <div>
    <h1>Practice: slide আর script একসাথে</h1>
    <div class="sub" id="total"></div>
  </div>
  <div class="spacer"></div>
  <button data-who-btn="All" class="on">সবাই</button>
  <button data-who-btn="Sinha">Sinha</button>
  <button data-who-btn="Saimon">Saimon</button>
  <button data-who-btn="Faria">Faria</button>
  <span style="width:10px"></span>
  <button data-lang="both" class="on">EN+BN</button>
  <button data-lang="en">EN</button>
  <button data-lang="bn">BN</button>
  <span style="width:10px"></span>
  <button id="prev">◀</button>
  <span id="timer">0:00</span>
  <button id="play">শুরু</button>
  <button id="next">▶</button>
</div></header>

<main>
<div class="note">
  উপরে নিজের নাম চাপলে শুধু তোমার slide গুলো থাকবে। ▶ চাপলে পরের slide, আর
  <b>শুরু</b> চাপলে ওই slide এর সময় গোনা শুরু হয় (সময় পেরিয়ে গেলে লাল হয়ে যাবে)।
  Keyboard এ তীর চিহ্ন দিয়েও যাওয়া যায়, space দিলে timer চালু বা বন্ধ হয়।<br>
  ভাগ: {per_speaker}<br>
  <b>মনে রাখো:</b> আসল presentation এই page থেকে না, <code>final_deck.html</code> অথবা
  <code>final_deck.pptx</code> থেকে হবে। এটা শুধু মুখস্থ করার জন্য।
</div>

{''.join(cards)}

<h2>যে প্রশ্নগুলো আসবেই</h2>
{qa}
<div class="note" style="margin-top:20px">পুরো research টা বিস্তারিত বুঝতে চাইলে
<code>GUIDE.html</code> খোলো। সব সংখ্যা <code>results/final/</code> থেকে তৈরি।</div>
</main>

<script>{JS}</script>
</body></html>"""

out = os.path.join(HERE, "PRACTICE.html")
open(out, "w").write(doc)
print("PRACTICE.html written,", len(doc) // 1024, "KB")
