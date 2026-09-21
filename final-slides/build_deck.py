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
.fig{background:#fff;border-radius:10px;padding:8px;display:flex;align-items:center;justify-content:center;min-height:0;align-self:flex-start}
.fig img{max-width:100%;max-height:455px;display:block}
.tl{display:flex;gap:10px}
.tl .card{flex:1;padding:14px 14px}
.date{font-size:12px;color:var(--amber);font-weight:700;letter-spacing:.06em}
.ok{color:var(--good);font-weight:700}
.part{color:var(--amber);font-weight:700}
td.l,th.l{text-align:left!important}
.tight td,.tight th{padding:7px 10px;font-size:14px}
.tiny td,.tiny th{padding:5px 8px;font-size:13px}
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


f3 = lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else str(x)
pct = lambda x: f"{100 * x:.0f}%"

main = {r["model"]: r for r in n["main"]}
cost = {r["model"]: r for r in n["llm_cost"]}
loco = {(r["model"], r["test"], r["setting"]): r for r in n["classical_loco"]}
within = {r["source"]: r for r in n["within_corpus_dup"]}
thr = {(r["source"], r["threshold"]): r for r in n["overlap_thresholds"]}
label_rows = n["label_study_summary"]
comp = [r for r in label_rows if r["row"] == "composition"]
agree = [r for r in label_rows if r["row"] == "agreement"][0]
base = {r["model"]: r for r in n["base_rate"]}
casc = n["cascade"]
ph_rows = [r for r in n["placeholder_effect"] if r["test_set"] == "ephishllm"]
ph = {r["model"]: r for r in ph_rows}
expl = {r["model"]: r for r in n["explanations_summary"]}
mv = n["matcher_validation_summary"][0]
sa = n["sa_in_kaggle"]
SIX = ["spamassassin", "ceas08", "trec07", "ling", "enron", "kaggle"]


def lf1(test, setting):
    r = loco.get(("logreg", test, setting))
    return r["f1"] if r else float("nan")


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
  <div class="note">15 sec. In the proposal we showed an empty table. Today it is filled in, and we also found things we did not expect.</div>
</section>""")

# 2 journey
slide(2, "Where we started", "Sinha", "From a suspicion to a measured result",
f"""  <div class="tl">
    <div class="card muted"><div class="date">15 JUL</div><b class="fs-18">Literature review</b>
      <div class="small" style="margin-top:6px">5 papers, all 97 to 99%. Every one tests inside one dataset.</div></div>
    <div class="card muted"><div class="date">21 JUL</div><b class="fs-18">Preliminary run</b>
      <div class="small" style="margin-top:6px">Train on one corpus, test on another: F1 0.99 fell to 0.30.</div></div>
    <div class="card muted"><div class="date">5 SEP</div><b class="fs-18">Proposal</b>
      <div class="small" style="margin-top:6px">Six objectives and one empty table.</div></div>
    <div class="card accent"><div class="date">21 SEP</div><b class="fs-18">Final study</b>
      <div class="small" style="margin-top:6px">{n['total_emails_clean']:,} emails checked for overlap, {n['llm_calls']:,} model calls, ${n['total_spend_usd']:.2f}.</div></div>
  </div>
  <div class="fs-18" style="font-weight:700;margin:26px 0 12px">What we corrected after review</div>
  <div class="grid3">
    <div class="card"><b class="t-amber">We are not first</b><div class="small" style="margin-top:6px">Two 2025-26 papers already test across corpora. Ours is what they skip: removing the overlap, cost, and false alarms.</div></div>
    <div class="card"><b class="t-amber">We added a control</b><div class="small" style="margin-top:6px">Decontamination also shrinks the training set, so we remove the same number of emails at random to prove the cause.</div></div>
    <div class="card"><b class="t-amber">We verify exactly</b><div class="small" style="margin-top:6px">Every duplicate pair is confirmed with exact similarity, and the matcher is checked against brute force.</div></div>
  </div>
  <div class="spacer"></div>
  <div class="card blue"><div class="fs-20"><b>Question:</b> if we remove leaked emails and always test on a corpus the model has never seen, how good are cheap detectors, what do they cost, and how much good mail do they block?</div></div>""",
"35 sec. Timeline in one breath, then the three corrections. Be open that we are not the first to test across corpora.")

# 3 objectives
slide(3, "Objectives", "Sinha", "The six from the proposal, plus what review added",
f"""  <table class="tight">
    <tr><th class="l">#</th><th class="l">Objective</th><th class="l">Delivered</th><th>Status</th></tr>
    <tr><td>1</td><td class="l">Decontaminated benchmark</td><td class="l">9 sources, 3 levels of matching, exact verification, matcher validated</td><td class="ok">Done</td></tr>
    <tr><td>2</td><td class="l">Leave-one-corpus-out</td><td class="l">6 folds, raw, decontaminated, and a random-removal control</td><td class="ok">Done</td></tr>
    <tr><td>3</td><td class="l">One protocol, all families</td><td class="l">classical, DistilBERT, 6 small LLMs, 3 published detectors, 2 commercial</td><td class="ok">Done</td></tr>
    <tr><td>4</td><td class="l">Cost in dollars</td><td class="l">measured charge for every one of {n['llm_calls']:,} calls</td><td class="ok">Done</td></tr>
    <tr><td>5</td><td class="l">AI-written phishing</td><td class="l">English, Italian, German, plus sanitised copies</td><td class="ok">Done</td></tr>
    <tr><td>6</td><td class="l">One honest table</td><td class="l">F1, false alarms, cost, with paired intervals and significance tests</td><td class="ok">Done</td></tr>
    <tr class="hl"><td>+</td><td class="l">Added after review</td><td class="l">label study, base-rate analysis, two-stage detectors, explanation quality</td><td class="ok">Done</td></tr>
  </table>""",
"35 sec. All six done. Point at the last row: review made the project bigger, not smaller.")

# 4 methodology
slide(4, "Methodology", "Sinha", "Six steps, and one control that decides the argument",
f"""  <div class="pipe">
    <div class="card blue"><div class="label t-blue">1 Collect</div><div class="small" style="margin-top:8px">9 public sources</div></div>
    <div class="arrow">→</div>
    <div class="card accent"><div class="label t-accent">2 Overlap</div><div class="small" style="margin-top:8px">MinHash, then exact Jaccard</div></div>
    <div class="arrow">→</div>
    <div class="card accent"><div class="label t-accent">3 Decontaminate</div><div class="small" style="margin-top:8px">train on 5, test on the 6th</div></div>
    <div class="arrow">→</div>
    <div class="card muted"><div class="label t-muted">4 Models</div><div class="small" style="margin-top:8px">11 detectors, same emails</div></div>
    <div class="arrow">→</div>
    <div class="card amber"><div class="label t-amber">5 Shift tests</div><div class="small" style="margin-top:8px">AI-written, sanitised, it/de</div></div>
    <div class="arrow">→</div>
    <div class="card good"><div class="label t-good">6 Report</div><div class="small" style="margin-top:8px">F1, false alarms, cost</div></div>
  </div>
  <div class="grid2" style="margin-top:26px">
    <div class="card accent"><b class="fs-18 t-accent">The control that makes it evidence</b><div class="small" style="margin-top:6px">Removing duplicates also removes data. So we run a third setting that removes the <b>same number</b> of training emails at random. If that changes nothing, the drop is the duplicates.</div></div>
    <div class="card"><b class="fs-18">Same emails for everyone</b><div class="small" style="margin-top:6px">A fixed 300-email subset per test set. Local, open and paid models are all scored on exactly those emails.</div></div>
  </div>""",
"40 sec. Spend the time on the control box. That is the answer to the first question any examiner asks.")

# 5 experimental details
ds = {d["source"]: d for d in n["datasets"]}
rows = "".join(
    f'<tr><td class="l">{s}</td><td>{ds[s]["role"]}</td><td>{ds[s]["emails_used"]:,}</td><td>{ds[s]["eval_subset"]}</td></tr>'
    for s in ["spamassassin", "ceas08", "trec07", "ling", "enron", "kaggle", "nazario", "nigerian",
              "ephishllm", "ephishllm_it", "ephishllm_de"] if s in ds)
slide(5, "Experimental core details (from the notebook)", "Sinha", "What exactly we ran",
f"""  <div class="row" style="align-items:flex-start">
    <table class="tiny" style="flex:1">
      <tr><th class="l">Source</th><th>Role</th><th>Used</th><th>Eval</th></tr>{rows}
    </table>
    <div style="flex:1.05;display:flex;flex-direction:column;gap:9px">
      <div class="card"><b class="t-blue">Classical</b><div class="small">TF-IDF 1-2 grams, 50k features, LogReg / Naive Bayes, {n['logreg_cpu_sec_per_1000']} s per 1,000 emails</div></div>
      <div class="card"><b class="t-good">DistilBERT</b><div class="small">1 epoch, 128 tokens, 1,000 emails per corpus, laptop CPU, raw and decontaminated</div></div>
      <div class="card"><b class="t-accent">11 detectors through one protocol</b><div class="small">6 small open LLMs (1B to 14B), 3 published phishing models, Gemini-3.1-Flash-Lite and GPT-4o-mini. Temperature 0, 1,500 chars</div></div>
      <div class="card"><b class="t-amber">Reproducible</b><div class="small">Seed 42, 8 GB MacBook, every raw answer saved, total API spend ${n['total_spend_usd']:.2f}</div></div>
    </div>
  </div>""",
"45 sec. This is the notebook slide. Say: every table that follows is produced by these scripts from these files.")

# 6 overlap
slide(6, "Result 1 · Overlap between corpora", "Saimon", "The standard check finds almost none of it",
f"""  <div class="row" style="align-items:stretch;flex:1">
    <div style="flex:1;display:flex;flex-direction:column;gap:12px">
      <div class="small">SpamAssassin emails that also sit inside the Kaggle set</div>
      <div class="grid3">
        <div class="card muted"><div class="label t-muted">Exact text</div><div class="mid" style="margin-top:8px">{sa['exact_raw'][0]:,}</div><div class="small">{sa['exact_raw'][1]}%</div></div>
        <div class="card amber"><div class="label t-amber">No whitespace</div><div class="mid t-amber" style="margin-top:8px">{sa['exact_norm'][0]:,}</div><div class="small">{sa['exact_norm'][1]}%</div></div>
        <div class="card accent"><div class="label t-accent">Near duplicate</div><div class="mid t-accent" style="margin-top:8px">{sa['near'][0]:,}</div><div class="small">{sa['near'][1]}%</div></div>
      </div>
      <div class="card"><div class="fs-18">{thr[('kaggle', 0.8)]['pct']:.0f}% of the Kaggle corpus has a near copy in another corpus. At the stricter 0.9 threshold it is still {thr[('kaggle', 0.9)]['pct']:.0f}%.</div></div>
      <div class="card good"><div class="small"><b class="t-good">Verified.</b> Every pair is confirmed with exact similarity, not an estimate. Against brute force on 400 hard cases the matcher has precision {mv['precision']:.2f} and recall {mv['recall']:.2f}.</div></div>
      <div class="small">Inside a single corpus, {min(within[s]['eval_with_near_dup_in_own_train_pct'] for s in SIX):.0f} to {max(within[s]['eval_with_near_dup_in_own_train_pct'] for s in SIX):.0f}% of its own test emails have a near copy in its training part.</div>
    </div>
    <div class="fig" style="flex:0.9">{img('overlap_heatmap.png')}</div>
  </div>""",
"55 sec. Say the three numbers slowly. Then the verification line: this is the part a reviewer attacks, and we checked it.")

# 7 leakage + control
slide(7, "Result 2 · Leakage inflates scores", "Saimon", "And the control shows it is the duplicates, not the data",
f"""  <div class="row" style="align-items:stretch;flex:1">
    <div style="flex:1.05;display:flex;flex-direction:column;gap:12px">
      <table class="tight">
        <tr><th class="l">Held-out corpus</th><th>Raw</th><th>Random removal</th><th>Decontaminated</th></tr>
        {''.join(f"<tr{' class=hl' if t in ('spamassassin','ling') else ''}><td class='l'>{t}</td><td>{lf1(t,'loco_raw'):.3f}</td><td>{lf1(t,'loco_random'):.3f}</td><td>{lf1(t,'loco_clean'):.3f}</td></tr>" for t in SIX)}
      </table>
      <div class="card accent"><div class="fs-20">Remove the same number of emails <b>at random</b>: nothing changes.<br>Remove the <b>duplicates</b>: up to 12 points disappear.</div></div>
      <div class="small">Kaggle to SpamAssassin transfer, the suspicious result from July: {n['kaggle_to_sa']['raw']:.3f} before, {n['kaggle_to_sa']['clean']:.3f} after. CEAS and TREC, which share nothing, do not move at all.</div>
    </div>
    <div class="fig" style="flex:1">{img('incorpus_vs_unseen.png')}</div>
  </div>""",
"60 sec. This is the strongest slide. Read the three columns across one row, then the red box. Then hand to Faria.")

# 8 labels
slide(8, "Result 3 · What the benchmarks actually contain", "Saimon", "Most of the phishing in these corpora is not phishing",
f"""  <div class="row" style="align-items:stretch;flex:1">
    <div style="flex:1;display:flex;flex-direction:column;gap:14px">
      <table class="tight">
        <tr><th class="l">Corpus</th><th>Positives</th><th>Phishing</th><th>Spam</th></tr>
        {''.join(f"<tr><td class='l'>{r['source']}</td><td>{int(r['n_positives'])}</td><td>{r['phishing_pct']:.0f}%</td><td>{r['spam_pct']:.0f}%</td></tr>" for r in comp)}
      </table>
      <div class="card amber"><div class="fs-20 t-amber" style="font-weight:700">Only {min(r['phishing_pct'] for r in comp):.0f} to {max(r['phishing_pct'] for r in comp):.0f}% of the "phishing" emails are phishing.</div>
        <div class="small" style="margin-top:6px">The rest is ordinary bulk advertising. Two annotators, agreement {100*agree['agreement']:.0f}%.</div></div>
      <div class="small">So a paper reporting "phishing detection" on these corpora is mostly reporting spam detection. Every model we tested is slightly better on the phishing part than on the spam part.</div>
    </div>
    <div class="card blue" style="flex:0.8;display:flex;flex-direction:column;justify-content:center">
      <div class="label t-blue">Why this matters</div>
      <div class="small" style="margin-top:10px;line-height:1.7">Nazario is real credential phishing and is the only corpus that is purely phishing. It is also the set where the classical models are weakest.<br><br>We keep the published labels, but we now know what they mean, and we report detection separately for the two kinds.</div>
    </div>
  </div>""",
"45 sec. This surprises people. Say the headline number, then that we used two annotators rather than trusting one model.")

# 9 AI phishing, presented by Saimon
pair_rows = [r for r in n["placeholder_effect"] if r["test_set"] == "ephishllm paired"]
pairm = {r["model"]: r for r in pair_rows}


def phrow(m):
    a_, b_ = ph.get(m), pairm.get(m)
    if not a_:
        return ""
    paired = f"{b_['gap']:+.2f}" if b_ else "&ndash;"
    return (f"<tr><td class='l'>{m}</td><td>{a_['recall_with_placeholder']:.2f}</td>"
            f"<td>{a_['recall_without']:.2f}</td><td class='t-amber'>{a_['gap']:+.2f}</td>"
            f"<td class='t-good'>{paired}</td></tr>")


slide(9, "Result 4 · A token that looked like a shortcut", "Saimon", "We checked our own good result, twice",
f"""  <div class="row" style="align-items:stretch;flex:1">
    <div style="flex:1.15;display:flex;flex-direction:column;gap:11px">
      <div class="card amber" style="padding:11px 16px"><div class="small"><b class="t-amber">The worry.</b> The AI corpus writes links as the token <code>&lt;&lt;link&gt;&gt;</code>: in 94 of 150 phishing emails, in none of the legitimate ones. If models react to the token, our AI-phishing numbers mean nothing.</div></div>
      <table class="tight">
        <tr><th class="l">Recall on AI phishing</th><th>With token</th><th>Without</th><th>Split gap</th><th>Paired gap</th></tr>
        {phrow('Qwen-2.5-7B')}{phrow('Llama-3.1-8B')}{phrow('Gemma-3-12B')}{phrow('TF-IDF + LogReg')}
      </table>
      <div class="card good" style="padding:11px 16px"><div class="small"><b class="t-good">Two tests, two answers.</b> Comparing emails that have the token with emails that do not suggests it is worth {sum(r['gap'] for r in ph_rows)/len(ph_rows)*100:.0f} points. But removing the token from the <b>same</b> emails changes recall by {sum(r['gap'] for r in pair_rows)/max(1,len(pair_rows))*100:.1f} points.</div></div>
      <div class="small">The first test was confounded: emails with links are simply easier than text-only business-email-compromise lures. The result stands.</div>
    </div>
    <div class="card blue" style="flex:0.7;display:flex;flex-direction:column;justify-content:center">
      <div class="label t-blue">The lesson</div>
      <div class="small" style="margin-top:10px;line-height:1.7">When you suspect a shortcut, change that one thing on the same data.<br><br>The quick comparison would have made us report a finding that is not there.</div>
    </div>
  </div>""",
"40 sec. Tell it as a story: we suspected our own good number, ran the obvious test, it said we were right to worry, then the proper paired test said otherwise. Report both.")

# 10 main table
def mrow(m, hl=False):
    r = main.get(m)
    if not r:
        return ""
    c = "local" if r["usd_per_1000"] == 0 else f"${r['usd_per_1000']:.3f}"
    inc = f"{r['in_corpus_f1']:.3f}" if isinstance(r["in_corpus_f1"], (int, float)) and r["in_corpus_f1"] != "" else "&ndash;"
    return (f"<tr{' class=hl' if hl else ''}><td class='l'>{m}</td><td>{inc}</td><td>{r['unseen_f1_mean']:.3f}</td>"
            f"<td>{100*r['false_alarm_rate']:.0f}%</td><td>{r['ai_phishing_f1']:.3f}</td><td>{c}</td></tr>")


order = [("Gemini-3.1-Flash-Lite", True), ("GPT-4o-mini", False), ("Qwen-2.5-7B", True), ("Llama-3.1-8B", False),
         ("Gemma-3-12B", False), ("Llama-3.2-3B", False), ("Phi-4-14B", False), ("Llama-3.2-1B", False),
         ("TF-IDF + LogReg", False), ("DistilBERT", False),
         ("BERT-phishing (published)", False), ("Phishsense-1B (published)", False)]
slide(10, "Result 5 · Every detector on the same emails", "Faria", "Unseen corpora, false alarms, AI phishing and cost",
f"""  <table class="tiny">
    <tr><th class="l">Model</th><th>In-corpus F1</th><th>Unseen-corpus F1</th><th>False alarms</th><th>AI phishing F1</th><th>$ / 1,000</th></tr>
    {''.join(mrow(m, hl) for m, hl in order)}
  </table>
  <div class="spacer"></div>
  <div class="small">Trained models use decontaminated data. The published detectors were trained on the same corpora we test on, which is why their unseen-corpus column and their AI-phishing column disagree so strongly.</div>""",
"55 sec. Three rows only: Gemini (best, paid), Qwen (best open), and a published detector (high on our corpora, low on AI mail).")

# 11 operating points
def brow(m):
    r = base.get(m)
    return (f"<tr><td class='l'>{m}</td><td>{r['recall']:.2f}</td><td>{100*r['false_alarm']:.0f}%</td>"
            f"<td>{r['f1@0.05']:.3f}</td><td>{r['false_alerts_per_1000@0.05']:.0f}</td></tr>") if r else ""


conf = next((c for c in casc if c["stage1"] == "TF-IDF + LogReg" and c["stage2"] == "Qwen-2.5-7B" and c["policy"] == "confirm"), None)
resc = next((c for c in casc if c["stage1"] == "Qwen-2.5-7B" and c["stage2"] == "Gemma-3-12B" and c["policy"] == "rescue"), None)
slide(11, "Result 6 · Operating points", "Faria", "A balanced test set is not a mailbox",
f"""  <div class="row" style="align-items:stretch;flex:1">
    <div style="flex:1.1;display:flex;flex-direction:column;gap:12px">
      <div class="small">Recomputed for a mailbox where 5% of mail is phishing</div>
      <table class="tight">
        <tr><th class="l">Model</th><th>Recall</th><th>False alarms</th><th>F1 at 5%</th><th>Wrongly flagged per 1,000</th></tr>
        {brow('Gemini-3.1-Flash-Lite')}{brow('Qwen-2.5-7B')}{brow('TF-IDF + LogReg')}{brow('Gemma-3-12B')}
      </table>
      <div class="small">Gemma looked best on AI phishing. In a real inbox it would flag {base['Gemma-3-12B']['false_alerts_per_1000@0.05']:.0f} good emails in every 1,000.</div>
    </div>
    <div style="flex:0.95;display:flex;flex-direction:column;gap:12px">
      <div class="card good"><div class="label t-good">Cheap two-stage detector</div>
        <div class="fs-20" style="margin-top:8px">TF-IDF first, LLM only on what it flags</div>
        <div class="small" style="margin-top:6px">F1 {conf['unseen_f1']:.3f}, false alarms {100*conf['false_alarm']:.1f}%, <b>${conf['usd_per_1000']:.4f} per 1,000</b>, about half the cost of the LLM alone and fewer false alarms than either part.</div></div>
      <div class="card amber"><div class="label t-amber">Recall-first version</div>
        <div class="small" style="margin-top:8px">Let Gemma re-check what Qwen cleared: AI-phishing recall {resc['ai_phishing_recall']:.2f}, but {100*resc['false_alarm']:.0f}% false alarms. That is a review queue, not a blocker.</div></div>
    </div>
  </div>""",
"50 sec. The point: the ranking changes with the base rate, and combining two cheap models beats either one.")

# 12 what it means, including the explanation study
q = expl.get("qwen/qwen-2.5-7b-instruct", {})
gm = expl.get("google/gemma-3-12b-it", {})
slide(12, "What it means", "Faria", "Four things we would tell another team",
f"""  <div class="grid2">
    <div class="card accent" style="padding:13px 18px"><b class="t-accent fs-18">1. Check overlap before claiming generalisation</b><div class="small" style="margin-top:5px">Five minutes of near-duplicate matching. Exact matching finds {sa['exact_raw'][0]} of {sa['near'][0]:,} shared emails.</div></div>
    <div class="card good" style="padding:13px 18px"><b class="t-good fs-18">2. Cheap detectors work, in the right order</b><div class="small" style="margin-top:5px">TF-IDF in front of Qwen: F1 {conf['unseen_f1']:.3f}, {100*conf['false_alarm']:.1f}% false alarms, ${conf['usd_per_1000']:.4f} per 1,000. A paid model is still better on every axis.</div></div>
    <div class="card blue" style="padding:13px 18px"><b class="t-blue fs-18">3. Report false alarms and the base rate</b><div class="small" style="margin-top:5px">At 5% phishing the ranking changes. One F1 number cannot tell you what a detector does to an inbox.</div></div>
    <div class="card amber" style="padding:13px 18px"><b class="t-amber fs-18">4. Be suspicious of your own good numbers</b><div class="small" style="margin-top:5px">Our token finding survived the quick test and died on the paired one. We report both.</div></div>
  </div>
  <div class="card" style="margin-top:16px"><div class="small"><b>One more measurement.</b> We asked two models for a reason with every verdict and had a third model judge it. When the verdict is right, the reason points at something really in the email {100*q.get('grounded',0):.0f}% of the time (Qwen) and {100*gm.get('grounded',0):.0f}% (Gemma). When the verdict is wrong, only about {100*(q.get('grounded_when_wrong',0)+gm.get('grounded_when_wrong',0))/2:.0f}% do: a wrong answer usually comes with an invented reason.</div></div>
  <div class="spacer"></div>
  <div class="card" style="text-align:center"><div class="fs-24" style="font-weight:700">High accuracy on one dataset is easy. <span class="t-accent">Honest evaluation is the hard part.</span></div></div>""",
"40 sec. One sentence per card. Read the explanation box quickly, then the closing line, then go on to limitations.")

# 13 limitations
slide(13, "Limitations", "Faria", "What this study does not show",
"""  <div class="grid2">
    <div class="card"><b class="fs-18">We are not first to test across corpora</b><div class="small" style="margin-top:6px">E-PhishGen (2025) and Bhuiyan (2026) did. Ours adds decontamination, cost and false alarms.</div></div>
    <div class="card"><b class="fs-18">300 emails per test set</b><div class="small" style="margin-top:6px">Interval about plus or minus 0.015, so small differences are not meaningful. We report intervals and significance tests.</div></div>
    <div class="card"><b class="fs-18">Our annotator is a model</b><div class="small" style="margin-top:6px">Two models, 86% agreement on a shared sample, but not hand-labelled by us.</div></div>
    <div class="card"><b class="fs-18">LLM pre-training is unknown</b><div class="small" style="margin-top:6px">The old corpora may be inside these models already. The 2025 AI corpus is the cleanest test we have.</div></div>
    <div class="card"><b class="fs-18">Different input budgets</b><div class="small" style="margin-top:6px">TF-IDF sees 20,000 characters, LLMs 1,500, DistilBERT 128 tokens. DistilBERT's row is a lower bound.</div></div>
    <div class="card"><b class="fs-18">One prompt, one run</b><div class="small" style="margin-top:6px">No prompt search, and providers can change a model behind the same name.</div></div>
  </div>""",
"35 sec. Say the first three clearly. Owning these is what makes the rest believable.")

# 14 next two weeks and the code
slides.append(f"""
<section class="slide">
  <div class="kicker">Scope of improvements within 2 weeks · Source code</div>
  <div class="speaker">Faria</div>
  <h1>What we finish next, and where everything lives</h1>
  <div class="grid2">
    <div class="card blue"><div class="date">DAYS 1 TO 7</div><b class="fs-18">Hand-labelled subset and calibration</b>
      <div class="small" style="margin-top:6px">The three of us label 300 positives ourselves, so the spam versus phishing claim no longer rests on a model. Then we ask each LLM for a confidence and set the operating point per corpus.</div></div>
    <div class="card amber"><div class="date">DAYS 8 TO 14</div><b class="fs-18">Bigger tests and a reusable tool</b>
      <div class="small" style="margin-top:6px">1,000 emails per set for the top three models to tighten the intervals, and the deduplication script packaged so other groups can run it on their own corpora. Budget left: about $3 of $5.</div></div>
  </div>
  <div class="grid2" style="margin-top:16px">
    <div class="card" style="border-color:var(--line)"><div class="label t-blue">GITHUB</div><div class="fs-19" style="margin-top:6px;word-break:break-all"><a href="{REPO}">{REPO.replace('https://','')}</a></div>
      <div class="small" style="margin-top:4px">code, every raw model answer, paper, research log, team guide</div></div>
    <div class="card" style="border-color:var(--line)"><div class="label t-accent">COLAB NOTEBOOK</div><div class="fs-17" style="margin-top:6px;word-break:break-all"><a href="{COLAB}">notebooks/phishing_llm_cross_corpus.ipynb</a></div>
      <div class="small" style="margin-top:4px">rebuilds every table and figure in seconds</div></div>
  </div>
  <div class="spacer"></div>
  <div class="grid3">
    <div class="card"><div class="label t-muted">Total spend</div><div class="mid" style="margin-top:4px">${n['total_spend_usd']:.2f}</div><div class="small">of a $5 budget</div></div>
    <div class="card"><div class="label t-muted">Model calls</div><div class="mid" style="margin-top:4px">{n['llm_calls']:,}</div><div class="small">all answers saved</div></div>
    <div class="card"><div class="label t-muted">Hardware</div><div class="mid" style="margin-top:4px">1 laptop</div><div class="small">8 GB, no GPU rental</div></div>
  </div>
  <div class="small" style="text-align:center;margin-top:10px">Thank you. Questions?</div>
  <div class="num">14</div>
  <div class="note">35 sec. Two blocks of plan, then the links, then the three numbers. Stop after "thank you".</div>
</section>""")

html = head + "\n".join(slides) + "\n\n</div></div>\n" + footer
html = html.replace("else if (e.key==='0') go(9);",
                    "else if (e.key==='0') go(9);\n  else if (e.key==='-') go(10);\n  else if (e.key==='=') go(11);")
open(os.path.join(HERE, "final_deck.html"), "w").write(html)
print("final_deck.html written,", len(slides), "slides")
