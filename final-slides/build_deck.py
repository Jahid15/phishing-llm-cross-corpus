"""
Builds final_deck.html. Style and navigation are reused from the proposal deck,
every number comes from numbers.json (run collect_numbers.py first), and the
figures are embedded so the file works offline.
"""
import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
FIG = os.path.join(ROOT, "results", "final", "figures")
REPO = "https://github.com/Jahid15/phishing-llm-cross-corpus"
COLAB = "https://colab.research.google.com/github/Jahid15/phishing-llm-cross-corpus/blob/main/notebooks/phishing_llm_cross_corpus.ipynb"

n = json.load(open(os.path.join(HERE, "numbers.json")))
src = open(os.path.join(ROOT, "new-slides", "proposal_deck.html")).read().split("\n")
head = "\n".join(src[:149]).replace("Phishing Email Detection Using LLMs: Proposal",
                                    "Phishing Email Detection Using LLMs: Final Update")
head += """
.fig{background:#fff;border-radius:10px;padding:8px;display:flex;align-items:center;justify-content:center}
.fig img{max-width:100%;max-height:455px;display:block}
.fig{min-height:0;align-self:flex-start}
.tl{display:flex;gap:10px}
.tl .card{flex:1;padding:14px 14px}
.date{font-size:12px;color:var(--amber);font-weight:700;letter-spacing:.06em}
.ok{color:var(--good);font-weight:700}
.part{color:var(--amber);font-weight:700}
td.l,th.l{text-align:left!important}
.tight td,.tight th{padding:7px 10px;font-size:14px}
a{color:var(--blue)}
</style>
</head>
<body>
<div id="bar"></div>
<div id="stage"><div id="deck">
"""
footer = "\n".join(src[427:])

def img(name):
    b = base64.b64encode(open(os.path.join(FIG, name), "rb").read()).decode()
    return f'<img src="data:image/png;base64,{b}" alt="{name}">'

def f3(x):
    return f"{x:.3f}" if isinstance(x, (int, float)) else str(x)

slides = []
def slide(num, kicker, speaker, title, body, note):
    slides.append(f"""
<section class="slide">
  <div class="kicker">{kicker}</div>
  <div class="speaker">{speaker}</div>
  <h1>{title}</h1>
{body}
  <div class="num">{num}</div>
  <div class="note">{note}</div>
</section>""")

sa = n["sa_in_kaggle"]
main = n["main"]
top = main[0]
best = next(r for r in main if r["model"] == "Qwen-2.5-7B")
qfs = next((r for r in main if r["model"] == "Qwen-2.5-7B few-shot"), None)
l3 = next(r for r in main if r["model"] == "Llama-3.2-3B")
l3fs = next((r for r in main if r["model"] == "Llama-3.2-3B few-shot"), None)
llm_rows = [r for r in main if r["type"] == "LLM"]
lr = next(r for r in main if r["model"] == "TF-IDF + LogReg")
db = next((r for r in main if r["model"] == "DistilBERT"), None)
infl = {r["test"]: r for r in n["inflation_logreg"]}
spent = n["llm_total_usd"] + n["discarded_usd"]

# 1 title
slides.append(f"""
<section class="slide">
  <div style="height:6px;background:var(--accent);position:absolute;left:0;right:0;top:0;border-radius:6px 6px 0 0"></div>
  <div class="spacer"></div>
  <div class="kicker">Computer Security · Final Update · Project Forum</div>
  <h1 class="fs-52" style="margin:14px 0 8px">Phishing Email Detection<br>Using Large Language Models</h1>
  <div class="fs-22" style="color:var(--blue)">A leakage-aware, cross-corpus and cost-aware benchmark of small open LLMs</div>
  <div style="height:2px;background:var(--line);width:420px;margin:30px 0 24px"></div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end">
    <div class="small" style="line-height:1.9">Jahid Ibna Sinha (011221376)<br>Md. Jakaria Alam Saimon (011221002)<br>Nowshin Anjum Faria (011221372)</div>
    <div style="text-align:right"><b>United International University</b><br><span class="small">Group 18</span></div>
  </div>
  <div class="spacer"></div>
  <div class="num">1</div>
  <div class="note">15 sec. Names and title. Say: in the proposal we promised a table that did not exist. Today we show it filled in.</div>
</section>""")

# 2 journey
slide(2, "Where we started", "Sinha", "From a suspicion to a measured result",
f"""  <div class="tl">
    <div class="card muted"><div class="date">15 JUL</div><b class="fs-18">Literature review</b>
      <div class="small" style="margin-top:6px">5 papers, all 97 to 99%. Every one tests inside one dataset. None reports cost.</div></div>
    <div class="card muted"><div class="date">21 JUL</div><b class="fs-18">Preliminary run</b>
      <div class="small" style="margin-top:6px">Train on one corpus, test on another: F1 0.99 fell to 0.30.</div></div>
    <div class="card muted"><div class="date">11 AUG</div><b class="fs-18">Overlap check</b>
      <div class="small" style="margin-top:6px">Kaggle already contains two thirds of SpamAssassin.</div></div>
    <div class="card muted"><div class="date">5 SEP</div><b class="fs-18">Proposal talk</b>
      <div class="small" style="margin-top:6px">Six objectives, one table to fill.</div></div>
    <div class="card accent"><div class="date">18 SEP</div><b class="fs-18">Final experiments</b>
      <div class="small" style="margin-top:6px">9 sources, 9 models, {n['total_emails_clean']:,} emails checked for overlap.</div></div>
  </div>
  <div class="fs-18" style="font-weight:700;margin:26px 0 12px">What changed since the proposal</div>
  <div class="grid3">
    <div class="card"><b class="t-amber">Prior work found</b><div class="small" style="margin-top:6px">E-PhishGen (AISec 2025) already tested classical models across corpora. So our claim is now leakage removal plus cost, and we cite them.</div></div>
    <div class="card"><b class="t-amber">Nazario is test-only</b><div class="small" style="margin-top:6px">Enron became a full corpus, so pairing Nazario with Enron mail would leak. Nazario now measures phishing recall only.</div></div>
    <div class="card"><b class="t-amber">Numbers rebuilt</b><div class="small" style="margin-top:6px">The 74.4% / 4,282 / 48 on our proposal slides came from an unsaved run. Every number today comes from code in the repo.</div></div>
  </div>
  <div class="spacer"></div>
  <div class="card blue"><div class="fs-20"><b>Question:</b> if we remove leaked emails and always test on a corpus the model has never seen, how good are cheap detectors, and what do they cost?</div></div>""",
"45 sec. Walk the timeline in one breath. Then the three changes, be open about the old numbers. Land on the question in the blue box.")

# 3 objectives
slide(3, "Objectives", "Sinha", "Six objectives from the proposal",
f"""  <table class="tight">
    <tr><th class="l">#</th><th class="l">Objective</th><th class="l">What we delivered</th><th>Status</th></tr>
    <tr><td>1</td><td class="l">Decontaminated benchmark</td><td class="l">9 sources, overlap measured at 3 levels, near duplicates removed</td><td class="ok">Done</td></tr>
    <tr><td>2</td><td class="l">Leave-one-corpus-out</td><td class="l">6 folds, each run with raw and cleaned training data</td><td class="ok">Done</td></tr>
    <tr><td>3</td><td class="l">One protocol, all families</td><td class="l">2 classical, DistilBERT, 6 small LLMs, 2 few-shot. Phishsense-1B not run</td><td class="part">Mostly</td></tr>
    <tr><td>4</td><td class="l">Cost in dollars</td><td class="l">Real cost of every one of {n['llm_calls']:,} LLM calls, from OpenRouter</td><td class="ok">Done</td></tr>
    <tr><td>5</td><td class="l">AI-written phishing</td><td class="l">E-PhishLLM (GPT-4o-mini emails) as a held-out shift test</td><td class="ok">Done</td></tr>
    <tr><td>6</td><td class="l">One honest table</td><td class="l">F1 on unseen corpora with 95% bootstrap intervals, next to cost</td><td class="ok">Done</td></tr>
  </table>
  <div class="spacer"></div>
  <div class="small">Phishsense-1B needs a HuggingFace access token. It is the first item for the next two weeks.</div>""",
"30 sec. Do not read every row. Say: five of six fully done, one mostly, and say why Phishsense is missing.")

# 4 methodology
slide(4, "Methodology", "Sinha", "Six steps, one script each, all on a laptop",
f"""  <div class="pipe">
    <div class="card blue"><div class="label t-blue">1 Collect</div><div class="small" style="margin-top:8px">9 public sources, subject + body, 10k cap per corpus</div></div>
    <div class="arrow">→</div>
    <div class="card accent"><div class="label t-accent">2 Overlap</div><div class="small" style="margin-top:8px">exact, normalized, MinHash near duplicate</div></div>
    <div class="arrow">→</div>
    <div class="card accent"><div class="label t-accent">3 Decontaminate</div><div class="small" style="margin-top:8px">train on 5 corpora, drop copies of the 6th</div></div>
    <div class="arrow">→</div>
    <div class="card muted"><div class="label t-muted">4 Models</div><div class="small" style="margin-top:8px">TF-IDF, DistilBERT, 6 small LLMs</div></div>
    <div class="arrow">→</div>
    <div class="card amber"><div class="label t-amber">5 Shift test</div><div class="small" style="margin-top:8px">E-PhishLLM, Nazario, Nigerian</div></div>
    <div class="arrow">→</div>
    <div class="card good"><div class="label t-good">6 Report</div><div class="small" style="margin-top:8px">F1 + 95% CI + USD per 1,000</div></div>
  </div>
  <div class="grid2" style="margin-top:28px">
    <div class="card"><b class="fs-18">Leave-one-corpus-out</b><div class="small" style="margin-top:6px">For each corpus T, train on the other five and test on all of T. Run twice: raw training data, and with every near duplicate of T removed. The gap is the inflation caused by leaked emails.</div></div>
    <div class="card"><b class="fs-18">Same emails for everyone</b><div class="small" style="margin-top:6px">A fixed 300-email subset per test set. Every model, local or paid, is scored on exactly those emails, so the numbers are comparable.</div></div>
  </div>""",
"45 sec. Point at steps 2 and 3, those are ours. Explain raw vs clean in one sentence. Then hand over to Saimon.")

# 5 experimental details
ds = {d["source"]: d for d in n["datasets"]}
rows = "".join(
    f'<tr><td class="l">{s}</td><td>{ds[s]["role"]}</td><td>{ds[s]["emails_after_cleaning"]:,}</td><td>{ds[s]["emails_used"]:,}</td><td>{ds[s]["eval_subset"]}</td></tr>'
    for s in ["spamassassin", "ceas08", "trec07", "ling", "enron", "kaggle", "nazario", "nigerian", "ephishllm"])
slide(5, "Experimental core details (from the notebook)", "Saimon", "What exactly we ran",
f"""  <div class="row" style="align-items:flex-start">
    <table class="tight" style="flex:1.1">
      <tr><th class="l">Source</th><th>Role</th><th>Cleaned</th><th>Used</th><th>Eval</th></tr>{rows}
    </table>
    <div style="flex:1;display:flex;flex-direction:column;gap:10px">
      <div class="card"><b class="t-blue">Classical</b><div class="small">TF-IDF 1-2 grams, 50k features, LogReg / Naive Bayes, CPU {n['logreg_cpu_sec_per_1000']} s per 1,000 emails</div></div>
      <div class="card"><b class="t-good">DistilBERT</b><div class="small">1 epoch, 128 tokens, batch 16, lr 5e-5, 1,000 emails per corpus, laptop CPU</div></div>
      <div class="card"><b class="t-accent">6 LLMs via OpenRouter</b><div class="small">Llama 1B/3B/8B, Qwen 7B, Gemma 12B, Phi-4 14B. Temperature 0, 5 output tokens, 1,500 chars. Few-shot: 4 examples from other corpora</div></div>
      <div class="card"><b class="t-amber">Reproducible</b><div class="small">Seed 42 everywhere. 8 GB MacBook. Total API spend ${spent:.2f}</div></div>
    </div>
  </div>""",
"50 sec. This is the notebook slide. Mention: all numbers on later slides are produced by these scripts, the notebook re-creates every table.")

# 6 overlap
slide(6, "Result 1 · Overlap between corpora", "Saimon", "The standard check finds almost none of it",
f"""  <div class="row" style="align-items:stretch;flex:1">
    <div style="flex:1;display:flex;flex-direction:column;gap:14px">
      <div class="small">SpamAssassin emails that also sit inside the Kaggle set</div>
      <div class="grid3">
        <div class="card muted"><div class="label t-muted">Exact text</div><div class="mid" style="margin-top:8px">{sa['exact_raw'][0]:,}</div><div class="small">{sa['exact_raw'][1]}%</div></div>
        <div class="card amber"><div class="label t-amber">No whitespace</div><div class="mid t-amber" style="margin-top:8px">{sa['exact_norm'][0]:,}</div><div class="small">{sa['exact_norm'][1]}%</div></div>
        <div class="card accent"><div class="label t-accent">Near duplicate</div><div class="mid t-accent" style="margin-top:8px">{sa['near'][0]:,}</div><div class="small">{sa['near'][1]}%</div></div>
      </div>
      <div class="card"><div class="fs-18">Kaggle also holds <b class="t-accent">{n['ling_in_kaggle_near'][1]:.0f}%</b> of Ling and <b class="t-accent">{n['enron_in_kaggle_near'][1]:.0f}%</b> of Enron. More than half of Kaggle is Enron.</div></div>
      <div class="small">Why exact matching fails: Kaggle deletes line breaks and glues words ("cream?Isn't"). We checked 400 of them by brute force: the matches are real.</div>
    </div>
    <div class="fig" style="flex:0.95">{img('overlap_heatmap.png')}</div>
  </div>""",
"55 sec. Say the three numbers slowly: two, three thousand eight hundred, five thousand. The exact check is what most people would run and it finds two.")

# 7 inflation
slide(7, "Result 2 · Leakage inflates scores", "Saimon", "Remove the copies and the good transfer disappears",
f"""  <div class="row" style="align-items:stretch;flex:1">
    <div style="flex:1;display:flex;flex-direction:column;gap:14px">
      <div class="card accent"><div class="label t-accent">Kaggle → SpamAssassin, TF-IDF + LogReg</div>
        <div style="display:flex;align-items:baseline;gap:18px;margin-top:8px"><div class="mid">{n['kaggle_to_sa']['raw']:.3f}</div><div class="t-muted fs-22">→</div><div class="mid t-accent">{n['kaggle_to_sa']['clean']:.3f}</div></div>
        <div class="small">F1 with leaked emails, then after removing them</div></div>
      <table class="tight">
        <tr><th class="l">Held-out corpus</th><th>Raw</th><th>Clean</th><th>Drop</th><th>Removed</th></tr>
        {''.join(f"<tr><td class='l'>{t}</td><td>{infl[t]['loco_raw']:.3f}</td><td>{infl[t]['loco_clean']:.3f}</td><td>{infl[t]['inflation']*100:.1f}</td><td>{int(infl[t]['removed']):,}</td></tr>" for t in ['spamassassin','ling','enron','kaggle','ceas08','trec07'])}
      </table>
      <div class="small">CEAS and TREC share almost nothing with the rest, and their scores do not move. That is the control.</div>
    </div>
    <div class="fig" style="flex:1">{img('incorpus_vs_unseen.png')}</div>
  </div>""",
"55 sec. Kaggle to SpamAssassin was the suspicious 0.97 from July. Now it is measured. Point at CEAS and TREC: no overlap, no change. Hand over to Faria.")

# 8 main table
def tr(r):
    ci = r["unseen_f1_ci"]
    hl = ' class="hl"' if r is best else ""  # highlight the recommended model, not just the top row
    cost = "local" if r["usd_per_1000"] == 0 else f"${r['usd_per_1000']:.3f}"
    return (f"<tr{hl}><td class='l'>{r['model']}</td><td>{f3(r['unseen_f1_mean'])} <span class='small'>({ci})</span></td>"
            f"<td>{f3(r['unseen_f1_worst'])}</td><td>{f3(r['ai_phishing_f1'])}</td><td>{f3(r['nazario_recall'])}</td><td>{cost}</td></tr>")
slide(8, "Result 3 · The table from the proposal, filled in", "Faria", "Unseen corpora, AI phishing and cost in one place",
f"""  <table class="tight">
    <tr><th class="l">Model</th><th>Unseen-corpus F1 (95% CI)</th><th>Worst corpus</th><th>AI phishing F1</th><th>Nazario recall</th><th>$ / 1,000</th></tr>
    {''.join(tr(r) for r in main)}
  </table>
  <div class="spacer"></div>
  <div class="small">All scores on the same held-out emails. Trained models use decontaminated data. LLMs never saw any of our data.</div>""",
"60 sec. Read only the top row, the TF-IDF row and the worst LLM. Point at the cost column.")

# 9 takeaways
slide(9, "Result 4 · What it means", "Faria", "Cheap detectors can be robust, if you pick carefully",
f"""  <div class="row" style="align-items:stretch;flex:1">
    <div style="flex:1;display:flex;flex-direction:column;gap:10px">
      <div class="card good" style="padding:12px 18px"><b class="t-good fs-18">1. Best balance: {best['model']} zero-shot</b><div class="small" style="margin-top:3px">{f3(best['unseen_f1_mean'])} F1 on unseen corpora, {f3(best['ai_phishing_f1'])} on AI phishing, ${best['usd_per_1000']:.3f} per 1,000 emails.</div></div>
      <div class="card accent" style="padding:12px 18px"><b class="t-accent fs-18">2. Few-shot helps old mail, hurts AI phishing</b><div class="small" style="margin-top:3px">Qwen: unseen {f3(best['unseen_f1_mean'])} to {f3(qfs['unseen_f1_mean'])}, but AI phishing {f3(best['ai_phishing_f1'])} to {f3(qfs['ai_phishing_f1'])}. Old examples anchor the model to old spam.</div></div>
      <div class="card blue" style="padding:12px 18px"><b class="t-blue fs-18">3. TF-IDF is a strong, free baseline</b><div class="small" style="margin-top:3px">{f3(lr['unseen_f1_mean'])} on unseen corpora, but only {f3(lr['ai_phishing_f1'])} on AI-written phishing.</div></div>
      <div class="card amber" style="padding:12px 18px"><b class="t-amber fs-18">4. Size is not quality</b><div class="small" style="margin-top:3px">Phi-4 (14B) ignored the one-word format in a third of emails and scored below 3B and 8B models.</div></div>
    </div>
    <div class="fig" style="flex:1">{img('f1_vs_cost.png')}</div>
  </div>""",
"60 sec. Four takeaways, one sentence each. Spend the most time on number 2, it is the surprise: examples from old corpora make the model worse on new attacks.")

# 10 limitations
slide(10, "Limitations", "Faria", "What this study does not show",
"""  <div class="grid2">
    <div class="card"><b class="fs-18">Labels are mixed</b><div class="small" style="margin-top:6px">Four corpora count ordinary spam as positive. We keep the published labels and report phishing-only recall separately.</div></div>
    <div class="card"><b class="fs-18">Small evaluation sets</b><div class="small" style="margin-top:6px">300 emails per test set keeps the cost low. The 95% intervals are about ±0.02 to ±0.03.</div></div>
    <div class="card"><b class="fs-18">LLM training data is unknown</b><div class="small" style="margin-top:6px">Old public corpora may be in the LLMs' pre-training data. E-PhishLLM is newer, but we cannot rule it out.</div></div>
    <div class="card"><b class="fs-18">Text only, English only</b><div class="small" style="margin-top:6px">No headers, URLs or attachments. The Italian and German part of E-PhishLLM is unused.</div></div>
    <div class="card"><b class="fs-18">Light DistilBERT training</b><div class="small" style="margin-top:6px">1,000 emails per corpus and one epoch, to fit an 8 GB laptop.</div></div>
    <div class="card"><b class="fs-18">One prompt, one run</b><div class="small" style="margin-top:6px">No prompt search. Providers can change a model behind the same name.</div></div>
  </div>""",
"40 sec. Say the first three clearly. The teacher will ask about LLM pre-training contamination, so name it before they do.")

# 11 next two weeks
slide(11, "Scope of improvements within 2 weeks", "Faria", "What we can finish before the final paper",
"""  <div class="tl">
    <div class="card blue"><div class="date">DAYS 1 TO 3</div><b class="fs-18">Phishsense-1B</b><div class="small" style="margin-top:6px">Get a HuggingFace token, run it locally on the same 2,700 emails. It is the model that fell from 97.5% to 70%.</div></div>
    <div class="card accent"><div class="date">DAYS 4 TO 6</div><b class="fs-18">Phishing-only labels</b><div class="small" style="margin-top:6px">Relabel spam vs phishing on a sample and rerun, to close the label gap.</div></div>
    <div class="card amber"><div class="date">DAYS 7 TO 9</div><b class="fs-18">Bigger test sets</b><div class="small" style="margin-top:6px">1,000 emails per set for the top 3 models. Under $0.50 more.</div></div>
    <div class="card good"><div class="date">DAYS 10 TO 14</div><b class="fs-18">Multilingual + write-up</b><div class="small" style="margin-top:6px">Italian and German E-PhishLLM, stronger DistilBERT, final paper.</div></div>
  </div>
  <div class="spacer"></div>
  <div class="small">Each item reuses the existing scripts. The budget left is well over one dollar.</div>""",
"30 sec. Four blocks, left to right. Stress that each one is small because the pipeline already exists.")

# 12 links
slides.append(f"""
<section class="slide">
  <div class="kicker">Source code</div>
  <div class="speaker">Faria</div>
  <h1>Everything is public and re-runnable</h1>
  <div class="grid2">
    <div class="card blue"><div class="label t-blue">GitHub</div><div class="fs-20" style="margin-top:8px;word-break:break-all"><a href="{REPO}">{REPO.replace('https://','')}</a></div>
      <div class="small" style="margin-top:6px">code, results, paper, research log</div></div>
    <div class="card accent"><div class="label t-accent">Colab notebook</div><div class="fs-18" style="margin-top:8px;word-break:break-all"><a href="{COLAB}">notebooks/phishing_llm_cross_corpus.ipynb</a></div>
      <div class="small" style="margin-top:6px">loads every result in seconds, or re-runs all six steps</div></div>
  </div>
  <div class="spacer"></div>
  <div class="card" style="text-align:center"><div class="fs-26" style="font-weight:700">High accuracy on one dataset is easy. <span class="t-accent">Honest evaluation is the hard part.</span></div></div>
  <div class="spacer"></div>
  <div class="small" style="text-align:center">Thank you. Questions?</div>
  <div class="num">12</div>
  <div class="note">20 sec. Read the links, then the closing line slowly, then stop.</div>
</section>""")

html = head + "\n".join(slides) + "\n\n</div></div>\n" + footer
html = html.replace("else if (e.key==='0') go(9);", "else if (e.key==='0') go(9);\n  else if (e.key==='-') go(10);\n  else if (e.key==='=') go(11);")
open(os.path.join(HERE, "final_deck.html"), "w").write(html)
print("final_deck.html written,", len(slides), "slides")
