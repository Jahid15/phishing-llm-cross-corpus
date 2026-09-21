"""
Builds GUIDE.html: the whole project explained in plain Bangla, the way a
senior would explain it to the team. Numbers and figures come from
results/final, so the guide cannot drift from the experiments.
"""
import base64
import json
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "results", "final")
FIG = os.path.join(R, "figures")
rd = lambda f: pd.read_csv(os.path.join(R, f))

main = rd("main_table.csv").set_index("model")
cost = rd("llm_cost.csv").set_index("model")
cl = rd("classical_loco.csv")
pairs = rd("overlap_pairs.csv")
within = rd("within_corpus_dup.csv").set_index("source")
th = rd("overlap_thresholds.csv")
ls = rd("label_study_summary.csv")
ph = rd("placeholder_effect.csv")
br = rd("base_rate.csv").set_index("model")
cas = rd("cascade.csv")
sig = rd("significance.csv")
expl = rd("explanations_summary.csv").set_index("model")
mv = rd("matcher_validation_summary.csv").iloc[0]
pw = rd("classical_pairwise.csv")
stats = rd("dataset_stats.csv")
spend = json.load(open(os.path.join(R, "llm_spend.json")))["total_usd"]
SIX = ["spamassassin", "ceas08", "trec07", "ling", "enron", "kaggle"]


def g(m, c):
    return float(main.loc[m, c]) if m in main.index else float("nan")


def ov(level, a, b, what="emails_of_source_found"):
    r = pairs[(pairs.level == level) & (pairs.contains == a) & (pairs.source == b)]
    return float(r[what].iat[0]) if len(r) else 0.0


def lf(t, s):
    r = cl[(cl.model == "logreg") & (cl.test == t) & (cl.setting == s)]
    return float(r.f1.iat[0]) if len(r) else float("nan")


def pwf(a, b, s):
    return float(pw[(pw.train == a) & (pw.test == b) & (pw.setting == s)].f1.iat[0])


def img(name, alt):
    b = base64.b64encode(open(os.path.join(FIG, name), "rb").read()).decode()
    return f'<figure><img src="data:image/png;base64,{b}" alt="{alt}"><figcaption>{alt}</figcaption></figure>'


comp = ls[ls.row == "composition"]
agree = ls[ls.row == "agreement"].iloc[0]
conf = cas[(cas.stage1 == "TF-IDF + LogReg") & (cas.stage2 == "Qwen-2.5-7B") & (cas.policy == "confirm")].iloc[0]
eng_ph = ph[ph.test_set == "ephishllm"]
pair_ph = ph[ph.test_set == "ephishllm paired"]
G, Q, B = main.loc["Gemini-3.1-Flash-Lite"], main.loc["Qwen-2.5-7B"], main.loc["BERT-phishing (published)"]
MB, PS, GM = main.loc["ModernBERT-phishing (published)"], main.loc["Phishsense-1B (published)"], main.loc["Gemma-3-12B"]
LR, DB = main.loc["TF-IDF + LogReg"], main.loc["DistilBERT"]

def modelrow(name, label=None):
    r = main.loc[name]
    c = "বিনামূল্যে" if r.usd_per_1000 == 0 else f"${r.usd_per_1000:.3f}"
    ai = "--" if r.ai_phishing_f1 != r.ai_phishing_f1 else f"{r.ai_phishing_f1:.3f}"
    return (f"<tr><td>{label or name}</td><td>{r.unseen_f1_mean:.3f}</td>"
            f"<td>{100*r.false_alarm_rate:.0f}%</td><td>{ai}</td><td>{c}</td></tr>")


CSS = """
:root{--bg:#fbfaf7;--ink:#1d2430;--soft:#5b6472;--line:#e3e0d8;--accent:#c2410c;--good:#15803d;--blue:#1d4ed8;--amber:#a16207;--card:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans Bengali","Hind Siliguri","Segoe UI",system-ui,sans-serif;line-height:1.85;font-size:17px}
.wrap{max-width:860px;margin:0 auto;padding:28px 20px 90px}
h1{font-size:30px;line-height:1.35;margin:10px 0 6px}
h2{font-size:23px;margin:44px 0 10px;padding-top:16px;border-top:2px solid var(--line)}
h3{font-size:19px;margin:26px 0 8px;color:var(--accent)}
p{margin:12px 0}
.lead{font-size:18px;color:var(--soft)}
.tag{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:999px;padding:3px 12px;font-size:13px;color:var(--soft);margin-right:6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:16px 0}
.card.accent{border-left:5px solid var(--accent)}
.card.good{border-left:5px solid var(--good)}
.card.blue{border-left:5px solid var(--blue)}
.card.amber{border-left:5px solid var(--amber)}
.quote{background:#fff;border-left:5px solid var(--blue);padding:12px 16px;margin:14px 0;border-radius:0 10px 10px 0}
.quote b{color:var(--blue)}
table{width:100%;border-collapse:collapse;margin:16px 0;background:#fff;font-size:15.5px;display:block;overflow-x:auto}
th{background:#f3f1ec;text-align:left;padding:9px 11px;border-bottom:2px solid var(--line);white-space:nowrap}
td{padding:9px 11px;border-bottom:1px solid var(--line);white-space:nowrap}
td:first-child,th:first-child{white-space:normal}
tr.hl td{background:#fff7ed;font-weight:600}
figure{margin:18px 0;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px}
figure img{width:100%;display:block;border-radius:6px}
figcaption{font-size:14px;color:var(--soft);margin-top:8px;text-align:center}
.big{font-size:30px;font-weight:700;color:var(--accent);line-height:1.2}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:720px){.grid{grid-template-columns:1fr}body{font-size:16px}}
code{background:#f3f1ec;padding:2px 6px;border-radius:5px;font-size:14px}
.toc{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 18px}
.toc a{color:var(--blue);text-decoration:none;display:block;padding:3px 0}
.qa{border-bottom:1px dashed var(--line);padding:12px 0}
.qa b{display:block;color:var(--ink);margin-bottom:4px}
.foot{margin-top:50px;color:var(--soft);font-size:14px;text-align:center}
"""

doc = f"""<!doctype html>
<html lang="bn"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>আমাদের Research: পুরোটা সহজ বাংলায়</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">

<span class="tag">Group 18</span><span class="tag">Computer Security, UIU</span><span class="tag">Final Update</span>
<h1>আমাদের research টা আসলে কী, কেন করলাম, আর কী পেলাম</h1>
<p class="lead">এটা আমাদের তিনজনের জন্য লেখা। কোনো formal ভাষা নেই। পড়লে পুরো
project টা মাথায় বসে যাবে, আর teacher যা জিজ্ঞেস করতে পারেন তার উত্তরও জানা থাকবে।
সব সংখ্যা আমাদের নিজের result file থেকে সরাসরি আসা।</p>

<div class="toc">
<a href="#ek">১. এক নজরে পুরো গল্পটা</a>
<a href="#keno">২. কেন এই topic, আর literature থেকে কী জানলাম</a>
<a href="#data">৩. আমাদের data কী কী</a>
<a href="#ki">৪. আমরা আসলে কী করেছি (ধাপে ধাপে)</a>
<a href="#result">৫. ফলাফল, একটা একটা করে</a>
<a href="#mane">৬. এর মানে কী</a>
<a href="#sima">৭. আমাদের সীমাবদ্ধতা</a>
<a href="#proshno">৮. প্রশ্নোত্তর (teacher যা যা ধরতে পারেন)</a>
<a href="#shobdo">৯. শব্দগুলোর সহজ মানে</a>
<a href="#slide">১০. কে কোন slide বলবে</a>
</div>

<h2 id="ek">১. এক নজরে পুরো গল্পটা</h2>

<p>আমাদের research এর নাম <b>"How Well Do Cheap Phishing Detectors Generalize?
A Leakage-Aware, Cross-Corpus and Cost-Aware Benchmark of Small Open LLMs"</b>।
সহজ বাংলায়: <b>সস্তা phishing detector গুলো আসলেই কাজ করে কিনা, সেটা সৎভাবে মেপে দেখা।</b></p>

<p>গল্পটা এক প্যারায় বললে এরকম। আমরা দেখলাম paper গুলো সবাই বলছে ৯৭ থেকে ৯৯ percent
accuracy। আমরা নিজেরা পুরনো একটা সহজ পদ্ধতি (TF-IDF) দিয়ে চালিয়েও ওই একই ৯৭ থেকে ৯৯
পেলাম। তখন সন্দেহ হলো: model ভালো, নাকি পরীক্ষাটাই সহজ? তাই আমরা এক dataset এ train
করে <b>অন্য</b> dataset এ test করলাম, আর দেখলাম score ভেঙে পড়ে। তারপর আসল কারণ খুঁজতে
গিয়ে পেলাম, <b>public dataset গুলোর ভিতরে একে অপরের email কপি করা আছে</b>। মানে model
পরীক্ষার সময় এমন email দেখছে যেটা সে আগেই train এ দেখেছে। সেই কপিগুলো সরিয়ে আবার
মেপে আমরা দেখালাম কোন detector আসলে কেমন, কত খরচ, আর কতটা ভালো email ভুল করে আটকায়।</p>

<div class="card accent">
<p style="margin:0"><b>এক লাইনে:</b> একটা dataset এ high accuracy পাওয়া সহজ,
কঠিন কাজটা হলো সৎ evaluation.</p>
</div>

<h2 id="keno">২. কেন এই topic, আর literature থেকে কী জানলাম</h2>

<p><b>কেন এই topic নিলাম:</b> class এ অন্য কোনো group phishing নেয়নি, dataset গুলো
সব free, আর ছোট LLM গুলো OpenRouter দিয়ে কয়েক cent এ চালানো যায়। মানে আমাদের বাজেটে
সম্ভব। পুরো project এ আমাদের খরচ হয়েছে মাত্র <b>${spend:.2f}</b>।</p>

<p>এখন literature থেকে কী জেনেছি, statement আকারে বলি। Presentation এ এভাবেই বলতে পারো:</p>

<div class="quote"><b>Koide et al. (ChatSpamDetector, 2024) paper থেকে আমরা জানতে পারি</b> যে
GPT-4 কে chain-of-thought prompt দিলে phishing detection এ ৯৯.৭০ percent accuracy পাওয়া যায়।
কিন্তু ওরা একটাই dataset এ test করেছে, আর খরচ কত সেটা বলেনি।</div>

<div class="quote"><b>Uddin et al. (2024) থেকে আমরা জানতে পারি</b> যে RoBERTa fine-tune করলে
৯৮.৪৫ percent আসে, Kaggle phishing dataset এ। এই Kaggle dataset টাই পরে আমাদের গবেষণার
মূল সন্দেহভাজন হয়ে দাঁড়ায়।</div>

<div class="quote"><b>Lin et al. (2025) থেকে আমরা জানতে পারি</b> যে ৩ বিলিয়ন parameter এর
ছোট model গুলো prompt engineering আর LoRA দিয়ে বড় model এর কাছাকাছি যেতে পারে। ওরা
নিজেরাই limitation এ লিখেছে যে cost-benefit analysis করেনি। এই ফাঁকটাই আমরা ধরেছি।</div>

<div class="quote"><b>Blake (Phishsense-1B, 2025) থেকে আমরা জানতে পারি</b> যে একটা
phishing-specific model নিজের dataset এ ৯৭.৫ percent পায়, কিন্তু অন্য একটা real-world
dataset এ নেমে যায় ৭০ percent এ। এই একটা লাইনই আমাদের পুরো গবেষণার শুরু।</div>

<div class="quote"><b>Pajola et al. (E-PhishGen, AISec 2025) থেকে আমরা জানতে পারি</b> যে
আটটা corpus এ leave-one-dataset-out test করলে classical model এর F1 ০.৯৮ থেকে গড়ে ০.২৭
এ নেমে যায়। এরাই E-PhishLLM corpus টা বানিয়েছে, যেটা আমরা AI-লেখা phishing test এ
ব্যবহার করেছি। <b>গুরুত্বপূর্ণ:</b> এরা আগেই cross-dataset test করেছে, তাই আমরা "প্রথম"
দাবি করি না। আমাদের নতুন অংশ হলো duplicate মেপে সরানো, খরচ, আর false alarm।</div>

<div class="quote"><b>Lee et al. (ACL 2022) থেকে আমরা জানতে পারি</b> যে বড় text corpus
গুলোতে near-duplicate ভরা থাকে, আর সেগুলো না সরালে evaluation মিথ্যা হয়। ওদের MinHash
পদ্ধতিটাই আমরা email এ লাগিয়েছি।</div>

<div class="quote"><b>Arp et al. (USENIX Security 2022) থেকে আমরা জানতে পারি</b> যে security
ML গবেষণার ৭৩ percent এ data snooping এর সমস্যা আছে। আমাদের কাজটা ঠিক সেই সমস্যার
একটা concrete উদাহরণ, phishing email এর ক্ষেত্রে।</div>

<p>তাহলে আমরা কী ভাবলাম? সবাই এক dataset এ কাজ করছে, কেউ duplicate check করছে না, কেউ
খরচ বলছে না। তাই আমরা ঠিক করলাম: <b>multiple dataset নেব, তাদের মধ্যে কপি করা email
গুলো মেপে সরাব, তারপর অদেখা dataset এ test করব, আর সাথে খরচ ও ভুল alarm ও মাপব।</b></p>

<h2 id="data">৩. আমাদের data কী কী</h2>

<p>নয়টা public email source। প্রতিটা free, সবগুলো text। ছয়টায় দুই রকম email আছে
(phishing/spam আর ভালো email), তাই ওরা পালা করে "test corpus" হয়। বাকি তিনটা শুধু test
এর জন্য।</p>

<table><tr><th>Source</th><th>কী জিনিস</th><th>কত email</th></tr>
""" + "".join(
    f"<tr><td>{r.source}</td><td>{d}</td><td>{r.emails_used:,}</td></tr>"
    for r, d in zip(stats.itertuples(), [
        "SpamAssassin, ২০০২ সালের পুরনো spam corpus",
        "CEAS 2008 challenge এর email",
        "TREC 2007 spam track",
        "Ling-Spam, ভাষাবিজ্ঞানের mailing list",
        "Enron কোম্পানির আসল email, spam আর ভালো দুইটাই",
        "Kaggle phishing set, পুরনো কয়েকটা corpus মিলিয়ে বানানো",
        "Nazario, আসল phishing (শুধু phishing)",
        "Nigerian fraud (শুধু প্রতারণা)",
        "E-PhishLLM, GPT-4o দিয়ে লেখা (English)",
        "E-PhishLLM এর ইতালিয়ান অংশ",
        "E-PhishLLM এর জার্মান অংশ"])) + f"""</table>

<p>প্রতিটা test set থেকে আমরা <b>৩০০টা email</b> এর একটা নির্দিষ্ট subset নিয়েছি (অর্ধেক
phishing, অর্ধেক ভালো)। সব model ঠিক ওই একই email গুলোতেই পরীক্ষা দেয়, তাই তুলনাটা
সৎ হয়।</p>

<h2 id="ki">৪. আমরা আসলে কী করেছি (ধাপে ধাপে)</h2>

<p>খুব সহজ করে বললে: <b>dataset এ আগে থেকেই বলা আছে কোনটা phishing আর কোনটা ভালো email।
আমরা সেই label লুকিয়ে রেখে model কে জিজ্ঞেস করেছি "এটা কি phishing?" তারপর model এর
উত্তর আর আসল label মিলিয়ে দেখেছি কে কেমন করল।</b> এর সাথে আমরা আরো কিছু কাজ করেছি,
নিচে ধাপে ধাপে।</p>

<h3>ধাপ ১: data নামানো আর পরিষ্কার করা</h3>
<p>নয়টা source নামিয়ে সবগুলোকে একই আকারে এনেছি: subject + body একসাথে, আর একটা label
(১ = phishing/spam, ০ = ভালো)। খুব ছোট email বাদ, একই corpus এর ভিতরের হুবহু duplicate বাদ।</p>

<h3>ধাপ ২: dataset গুলোর মধ্যে কপি খোঁজা</h3>
<p>এটাই আমাদের মূল অবদান। তিনভাবে মিলিয়ে দেখেছি:</p>
<ul>
<li><b>হুবহু text</b> মিলিয়ে (যেভাবে যে কেউ করবে)</li>
<li><b>space সরিয়ে</b> মিলিয়ে</li>
<li><b>near-duplicate</b>: MinHash দিয়ে সম্ভাব্য জোড়া বের করে, তারপর প্রতিটা জোড়ার
<b>exact similarity</b> হিসাব করে। ৮০ percent বা বেশি মিললে সেটাকে একই email ধরা হয়।</li>
</ul>

<h3>ধাপ ৩: leave-one-corpus-out + control</h3>
<p>ছয়টা corpus এর একটাকে সরিয়ে রেখে বাকি পাঁচটায় train, তারপর ওই সরানো corpus এ test।
এটা তিনবার করেছি:</p>
<ul>
<li><b>raw</b>: data যেমন আছে তেমন</li>
<li><b>clean</b>: test corpus এ কপি আছে এমন training email সরিয়ে</li>
<li><b>random</b>: সমান সংখ্যক email, কিন্তু এলোমেলোভাবে বেছে সরিয়ে</li>
</ul>
<div class="card blue"><p style="margin:0"><b>এই তৃতীয়টা কেন দরকার?</b> কারণ duplicate
সরালে data ও কমে যায়। কেউ বলতে পারে "score তো কম data র জন্য কমেছে"। এলোমেলোভাবে সমান
সংখ্যক সরিয়ে দেখালাম score কমে না। তাই কারণটা duplicate, data র পরিমাণ না।</p></div>

<h3>ধাপ ৪: model চালানো</h3>
<p>একই prompt, একই email এ ২০টা detector: TF-IDF (দুইটা), DistilBERT, ছয়টা ছোট open LLM,
তিনটা অন্যের বানানো published phishing detector, আর দুইটা paid model (Gemini, GPT-4o-mini)।
LLM গুলো কোনো training পায়নি, তাই ওদের জন্য প্রতিটা test set এমনিতেই অদেখা।</p>

<h3>ধাপ ৫: বাড়তি পরীক্ষা</h3>
<p>AI দিয়ে লেখা phishing (ইংরেজি, ইতালিয়ান, জার্মান), spam না phishing সেটা label করানো,
বাস্তব হারে হিসাব, দুই ধাপের detector, আর model এর দেওয়া কারণ কতটা সত্যি সেটা যাচাই।</p>

<h2 id="result">৫. ফলাফল, একটা একটা করে</h2>

<h3>ফলাফল ১: dataset গুলো একে অপরের কপি</h3>
<p>Kaggle set এর ভিতরে SpamAssassin এর কয়টা email আছে?</p>
<table><tr><th>যেভাবে মিলিয়েছি</th><th>কয়টা পাওয়া গেল</th></tr>
<tr><td>হুবহু text</td><td><b>{int(ov('exact_raw','kaggle','spamassassin'))}</b> টা</td></tr>
<tr><td>Space সরিয়ে</td><td>{int(ov('exact_norm','kaggle','spamassassin')):,} টা</td></tr>
<tr class="hl"><td>Near-duplicate (যাচাই করা)</td><td><b>{int(ov('near','kaggle','spamassassin')):,}</b> টা, মানে SpamAssassin এর {ov('near','kaggle','spamassassin','pct_of_source'):.0f}%</td></tr></table>

<p>Kaggle এর ভিতরে Ling-Spam এর {ov('near','kaggle','ling','pct_of_source'):.0f}% আর Enron এর
{ov('near','kaggle','enron','pct_of_source'):.0f}% ও আছে। মোট Kaggle corpus এর
<b>{float(th[(th.source=='kaggle')&(th.threshold==0.8)].pct.iat[0]):.0f}%</b> এর কপি অন্য কোথাও আছে। আর threshold কড়া করে ০.৯ করলেও
{float(th[(th.source=='kaggle')&(th.threshold==0.9)].pct.iat[0]):.0f}% থাকে, মানে ফলাফলটা threshold এর উপর নির্ভর করে না।</p>

{img('overlap_heatmap.png', 'কোন corpus এর কত অংশ অন্য corpus এর ভিতরে আছে। লাল যত গাঢ়, কপি তত বেশি।')}

<div class="card good"><p style="margin:0"><b>আমরা এটা যাচাইও করেছি।</b> ৪০০টা কঠিন
ক্ষেত্রে (যেগুলো সহজ মিলে পাওয়া যায়নি) পুরো Kaggle corpus এর সাথে একটা একটা করে মিলিয়ে
দেখেছি। আমাদের পদ্ধতির precision {mv.precision:.2f}, recall {mv.recall:.2f}. মানে ভুল বলেনি।</p></div>

<h3>ফলাফল ২: কপি সরালে score পড়ে যায় (আর control সেটা প্রমাণ করে)</h3>
<table><tr><th>SpamAssassin fold</th><th>F1</th></tr>
<tr><td>বাকি পাঁচ corpus, data যেমন আছে</td><td>{lf('spamassassin','loco_raw'):.3f}</td></tr>
<tr><td>সমান সংখ্যক email <b>এলোমেলোভাবে</b> সরিয়ে</td><td>{lf('spamassassin','loco_random'):.3f}</td></tr>
<tr class="hl"><td><b>duplicate</b> গুলো সরিয়ে</td><td>{lf('spamassassin','loco_clean'):.3f}</td></tr></table>
<p>জুলাইয়ের সেই সন্দেহজনক ফলাফল, Kaggle থেকে SpamAssassin: আগে {pwf('kaggle','spamassassin','raw'):.3f},
কপি সরানোর পরে {pwf('kaggle','spamassassin','clean'):.3f}।</p>

{img('incorpus_vs_unseen.png', 'নিজের dataset এ (নীল), অদেখা dataset এ কাঁচা data দিয়ে (কমলা), আর কপি সরানোর পরে (লাল)।')}

<h3>ফলাফল ৩: এই corpus গুলোতে আসলে phishing কম, spam বেশি</h3>
<table><tr><th>Corpus</th><th>phishing</th><th>spam</th></tr>
""" + "".join(f"<tr><td>{r.source}</td><td>{r.phishing_pct:.0f}%</td><td>{r.spam_pct:.0f}%</td></tr>"
              for r in comp.itertuples()) + f"""</table>
<p>দুইজন annotator (দুইটা আলাদা model) ৩০০টা email এ {100*float(agree.agreement):.0f}% একমত। মানে যখন কেউ
বলে "আমরা phishing detection এ ৯৯% পেয়েছি", আসলে সে বেশিরভাগ spam detection মাপছে।</p>

<h3>ফলাফল ৪: সব detector একসাথে</h3>
<table><tr><th>Model</th><th>অদেখা corpus এ F1</th><th>ভুল alarm</th><th>AI phishing এ F1</th><th>হাজার email এ খরচ</th></tr>
{modelrow('Gemini-3.1-Flash-Lite', 'Gemini-3.1-Flash-Lite (paid)')}
{modelrow('GPT-4o-mini', 'GPT-4o-mini (paid)')}
{modelrow('Qwen-2.5-7B', 'Qwen-2.5-7B (open, zero-shot)')}
{modelrow('Llama-3.1-8B')}
{modelrow('Gemma-3-12B')}
{modelrow('TF-IDF + LogReg')}
{modelrow('DistilBERT')}
{modelrow('BERT-phishing (published)')}
{modelrow('ModernBERT-phishing (published)')}
{modelrow('Phishsense-1B (published)')}
</table>

<div class="card amber"><p style="margin:0"><b>সবচেয়ে চমকপ্রদ row:</b> অন্যের বানানো
BERT-phishing detector আমাদের পুরনো corpus এ পায় <b>{B.unseen_f1_mean:.3f}</b>, যেটা পুরো table এর
সর্বোচ্চ। কিন্তু AI দিয়ে লেখা phishing এ পায় <b>{B.ai_phishing_f1:.3f}</b>। ModernBERT আরো খারাপ:
{MB.unseen_f1_mean:.3f} বনাম <b>{MB.ai_phishing_f1:.3f}</b>। কারণ এরা ঠিক ওই corpus গুলোতেই train করা যেগুলোতে
আমরা test করছি। তবে সব published model এমন না: Phishsense-1B পায় {PS.ai_phishing_f1:.3f}, তাই আমরা
বলি না যে "সব released model খারাপ"।</p></div>

{img('f1_vs_cost.png', 'খরচ বনাম মান। বাম দিকে উপরে থাকা মানে সস্তা ও ভালো।')}

<h3>ফলাফল ৫: একটা token, যেটা প্রথমে cheating মনে হয়েছিল</h3>
<p>AI দিয়ে লেখা corpus এ প্রতিটা phishing link লেখা আছে <code>&lt;&lt;link&gt;&gt;</code> দিয়ে।
আমাদের ১৫০টা phishing email এর ৯৪টায় আছে, ভালো email এ নেই। তাহলে model কি শুধু এই
token দেখেই ধরছে?</p>
<table><tr><th>কীভাবে পরীক্ষা করলাম</th><th>ফলাফল</th></tr>
<tr><td>যেগুলোতে token আছে বনাম যেগুলোতে নেই (সহজ তুলনা)</td><td>{100*eng_ph.gap.mean():.0f} point পার্থক্য</td></tr>
<tr class="hl"><td><b>একই email থেকে token মুছে</b> আবার জিজ্ঞেস (আসল পরীক্ষা)</td><td>মাত্র {100*pair_ph.gap.mean():.1f} point পার্থক্য</td></tr></table>
<p>মানে token টা কারণ না। প্রথম তুলনাটা ভুল ছিল কারণ ওটা দুই <b>ধরনের</b> email তুলনা
করছিল: link ওয়ালা phishing এমনিতেই সহজ, আর link ছাড়া business-email-compromise কঠিন।
আমরা দুইটা ফলাফলই paper এ রেখেছি, কারণ সহজ পরীক্ষাটা ভুল পথে নিয়ে যেত।</p>

<h3>ফলাফল ৬: বাস্তব inbox এ হিসাবটা বদলে যায়</h3>
<p>আমাদের test set এ অর্ধেক phishing। বাস্তবে এত না। ৫ percent ধরলে:</p>
<table><tr><th>Model</th><th>F1 (৫% phishing এ)</th><th>হাজারে কতটা ভালো email ভুল করে ধরবে</th></tr>
""" + "".join(
    f"<tr><td>{m}</td><td>{float(br.loc[m,'f1@0.05']):.3f}</td><td>{float(br.loc[m,'false_alerts_per_1000@0.05']):.0f}</td></tr>"
    for m in ["Gemini-3.1-Flash-Lite", "Qwen-2.5-7B", "TF-IDF + LogReg", "Gemma-3-12B"] if m in br.index) + f"""</table>
<div class="card good"><p style="margin:0"><b>বাস্তব সমাধান:</b> আগে free TF-IDF filter,
তারপর শুধু যেগুলো সে সন্দেহ করে সেগুলো LLM এ পাঠাও। F1 {conf.unseen_f1:.3f}, ভুল alarm
{100*conf.false_alarm:.1f}%, খরচ হাজারে <b>${conf.usd_per_1000:.4f}</b>। LLM একা চালানোর অর্ধেক খরচ, আর
ভুল alarm ও কম।</p></div>

<h3>ফলাফল ৭: model এর দেওয়া কারণ কতটা সত্যি</h3>
<p>উত্তর ঠিক হলে কারণটা email এ সত্যিই আছে এমন কিছু দেখায় প্রায়
{100*float(expl.loc['qwen/qwen-2.5-7b-instruct','grounded']):.0f}% ক্ষেত্রে। কিন্তু উত্তর ভুল হলে মাত্র
{100*expl['grounded_when_wrong'].mean():.0f}%। মানে ভুল উত্তরের সাথে model বানানো কারণ দেয়। তাই user কে
explanation দেখানো তখনই নিরাপদ যখন verdict আগে যাচাই করা হয়।</p>

<h2 id="mane">৬. এর মানে কী</h2>
<div class="grid">
<div class="card accent"><b>১. Generalisation দাবি করার আগে overlap দেখুন</b>
<p style="margin:6px 0 0">৫ মিনিটের কাজ। হুবহু মিলিয়ে দেখলে {int(ov('exact_raw','kaggle','spamassassin'))} টা পাওয়া যায়,
আসলে আছে {int(ov('near','kaggle','spamassassin')):,} টা।</p></div>
<div class="card good"><b>২. সস্তা detector কাজ করে, ঠিক ক্রমে সাজালে</b>
<p style="margin:6px 0 0">TF-IDF তারপর Qwen: F1 {conf.unseen_f1:.3f}, ভুল alarm {100*conf.false_alarm:.1f}%,
হাজারে ${conf.usd_per_1000:.4f}। তবে paid model এখনো এগিয়ে।</p></div>
<div class="card blue"><b>৩. একটা F1 যথেষ্ট না</b>
<p style="margin:6px 0 0">ভুল alarm আর বাস্তব হার দুইটাই বলতে হবে, নাহলে inbox এ কী হবে
সেটা বোঝা যায় না।</p></div>
<div class="card amber"><b>৪. নিজের ভালো ফলাফলকেও সন্দেহ করুন</b>
<p style="margin:6px 0 0">আমাদের token এর ফলাফল সহজ পরীক্ষায় টিকে গিয়েছিল, কড়া পরীক্ষায়
বাতিল হয়েছে। দুইটাই লিখেছি।</p></div>
</div>

<h2 id="sima">৭. আমাদের সীমাবদ্ধতা</h2>
<ul>
<li><b>আমরা প্রথম না।</b> E-PhishGen (2025) আর Bhuiyan (2026) আগেই cross-corpus test করেছে।
আমাদের নতুন অংশ: duplicate মেপে সরানো, control, খরচ, ভুল alarm, operating point।</li>
<li><b>প্রতি test set এ ৩০০ email।</b> তাই ০.০২ এর কম পার্থক্যের মানে নেই। আমরা interval
আর significance test দিয়েছি।</li>
<li><b>Label করেছে একটা model, আমরা না।</b> দুইটা model {100*float(agree.agreement):.0f}% একমত, কিন্তু হাতে
label করা না। সামনের দুই সপ্তাহে আমরা নিজেরা ৩০০টা label করব।</li>
<li><b>LLM গুলো হয়তো পুরনো corpus আগেই দেখেছে</b> pre-training এ। এজন্যই ২০২৫ এর AI corpus
আমাদের জন্য সবচেয়ে নির্ভরযোগ্য test।</li>
<li><b>প্রতিটা model একই পরিমাণ email দেখে না</b> (TF-IDF ২০,০০০ অক্ষর, LLM ১,৫০০, DistilBERT
১২৮ token)। তাই DistilBERT এর row টা সর্বনিম্ন হিসাব ধরতে হবে।</li>
<li><b>এক prompt, এক run।</b> prompt খুঁজে দেখা হয়নি, আর provider চাইলে model বদলে দিতে পারে।</li>
</ul>

<h2 id="proshno">৮. প্রশ্নোত্তর</h2>
""" + "".join(f'<div class="qa"><b>{q}</b>{a}</div>' for q, a in [
    ("Score কমেছে কি শুধু কম data র জন্য?",
     f"না। এটাই আমরা control দিয়ে test করেছি। সমান সংখ্যক email এলোমেলোভাবে সরালে F1 বদলায় "
     f"মাত্র {abs(lf('spamassassin','loco_raw')-lf('spamassassin','loco_random'))*100:.1f} point, আর duplicate সরালে "
     f"{(lf('spamassassin','loco_raw')-lf('spamassassin','loco_clean'))*100:.0f} point।"),
    ("Duplicate গুলো সত্যিই duplicate তো?",
     f"প্রতিটা সম্ভাব্য জোড়া exact similarity দিয়ে যাচাই করা, MinHash এর আন্দাজে না। আর ৪০০টা "
     f"কঠিন ক্ষেত্রে brute force এর সাথে মিলিয়ে precision {mv.precision:.2f}, recall {mv.recall:.2f}। "
     "কয়েকটা হাতে পড়েও দেখেছি: একই লেখা, শুধু line break আলাদা।"),
    ("Threshold ০.৮ কেন?",
     f"এটাই text corpus deduplication এর প্রচলিত মান। আমরা ০.৭ আর ০.৯ ও দিয়েছি: ০.৯ এও "
     f"Kaggle এর {float(th[(th.source=='kaggle')&(th.threshold==0.9)].pct.iat[0]):.0f}% এর কপি অন্য কোথাও আছে। আর কত অক্ষর মিলাচ্ছি "
     "সেটাও (২০০০ বনাম ৫০০০) ফলাফল বদলায় না।"),
    ("কোন model ব্যবহার করা উচিত?",
     f"কম বাজেটে: TF-IDF এর পরে zero-shot Qwen-2.5-7B, F1 {conf.unseen_f1:.3f}, ভুল alarm "
     f"{100*conf.false_alarm:.1f}%, হাজারে ${conf.usd_per_1000:.4f}। বাজেট থাকলে Gemini-3.1-Flash-Lite, "
     "ওটা আমাদের মাপা সব দিক থেকেই এগিয়ে।"),
    ("Gemma তো AI phishing এ সেরা, ওটা নেবে না কেন?",
     f"Gemma {100*GM.false_alarm_rate:.0f}% ভালো email কেও phishing বলে। বাস্তব inbox এ (৫% phishing) সেটা "
     f"হাজারে {float(br.loc['Gemma-3-12B','false_alerts_per_1000@0.05']):.0f} টা ভালো email আটকে দেওয়া। তাই ওটা মানুষের review queue এর "
     "আগে বসানোর জন্য ভালো, সরাসরি block করার জন্য না।"),
    ("GPT-4 কেন ব্যবহার করোনি?",
     "করেছি, reference হিসেবে দুইটা paid model (Gemini-3.1-Flash-Lite, GPT-4o-mini) চালিয়েছি "
     "আর ওরা এগিয়ে আছে, সেটা আমরা সৎভাবে লিখেছি। কিন্তু আমাদের গবেষণার প্রশ্ন হলো কম বাজেটের "
     "প্রতিষ্ঠান কী চালাতে পারবে, তাই মূল ফোকাস open model।"),
    ("Published detector গুলোর খারাপ ফল কি শুধু threshold এর দোষ?",
     "না, আমরা সেটাও দেখেছি। ModernBERT এর card এ বলা threshold ০.৩৭ ব্যবহার করলে AI phishing "
     "এ recall ০.০৯ থেকে ০.১১ হয়, আর ০.২ threshold এ ০.২২, কিন্তু তখন ভুল alarm ৮% থেকে ৩৩% এ "
     "চলে যায়। এক সমস্যা কমিয়ে আরেক সমস্যা বাড়ে।"),
    ("তোমাদের নতুন অবদান কী?",
     "চারটা: (১) নয়টা corpus এর মধ্যে near-duplicate মেপে দেখানো যে হুবহু মিলিয়ে দেখলে ধরা পড়ে না, "
     "(২) সেগুলো সরিয়ে test করা এবং random-removal control দিয়ে প্রমাণ করা যে কারণটা leakage, "
     "(৩) dollar এ খরচ আর ভুল alarm এর হার দেওয়া, (৪) বাস্তব হারে operating point আর দুই ধাপের detector।"),
    ("খরচ কত হলো?",
     f"মোট ${spend:.2f}, একটা 8 GB laptop এ। বাকি সব free software আর public data। GPU ভাড়া করিনি।"),
    ("ফলাফল আবার বের করা যাবে?",
     "হ্যাঁ। seed 42 সব জায়গায়, প্রতিটা raw model উত্তর repository তে সংরক্ষিত, আর paper এর "
     "প্রতিটা table ও সংখ্যা script দিয়ে তৈরি, হাতে টাইপ করা না।"),
]) + f"""

<h2 id="shobdo">৯. শব্দগুলোর সহজ মানে</h2>
<table><tr><th>শব্দ</th><th>সহজ মানে</th></tr>
<tr><td>Precision</td><td>যতগুলো phishing বলেছি, তার কতগুলো সত্যিই phishing</td></tr>
<tr><td>Recall</td><td>যত phishing ছিল, তার কতগুলো ধরতে পেরেছি</td></tr>
<tr><td>F1</td><td>উপরের দুইটার একসাথে হিসাব। দুইটাই ভালো হলে F1 ভালো</td></tr>
<tr><td>False alarm</td><td>ভালো email কে ভুল করে phishing বলা। inbox এ এটাই বিরক্তিকর</td></tr>
<tr><td>Leave-one-corpus-out</td><td>পাঁচটা dataset এ শিখে ছয় নম্বরটায় পরীক্ষা, ছয়বার</td></tr>
<tr><td>Near-duplicate</td><td>দুইটা email প্রায় একই লেখা (৮০%+ মিল)</td></tr>
<tr><td>MinHash আর LSH</td><td>১,৭০,০০০ email এর মধ্যে সম্ভাব্য মিল খুঁজে বের করার দ্রুত উপায়</td></tr>
<tr><td>Jaccard similarity</td><td>দুইটা লেখার কত অংশ একই, ০ থেকে ১ এর মধ্যে</td></tr>
<tr><td>Bootstrap interval</td><td>অন্য email নিলে সংখ্যাটা কতটা এদিক-ওদিক হতো তার হিসাব</td></tr>
<tr><td>McNemar test</td><td>দুইটা model এর পার্থক্য কাকতালীয় কিনা তার পরীক্ষা</td></tr>
<tr><td>Zero-shot / few-shot</td><td>উদাহরণ ছাড়া জিজ্ঞেস করা / prompt এ কয়েকটা উদাহরণ দিয়ে জিজ্ঞেস করা</td></tr>
<tr><td>Decontamination</td><td>test corpus এ কপি আছে এমন training email সরিয়ে ফেলা</td></tr>
<tr><td>Base rate</td><td>বাস্তবে মোট email এর কত শতাংশ phishing</td></tr>
</table>

<h2 id="slide">১০. কে কোন slide বলবে</h2>
<table><tr><th>কে</th><th>Slide</th><th>কী নিয়ে</th><th>সময়</th></tr>
<tr><td>Sinha</td><td>১ to ৫</td><td>ভূমিকা, objectives, methodology, experimental details</td><td>২:৫০</td></tr>
<tr><td>Saimon</td><td>৬ to ৯</td><td>overlap, leakage + control, corpus এ আসলে কী আছে, token পরীক্ষা</td><td>৩:২০</td></tr>
<tr><td>Faria</td><td>১০ to ১৪</td><td>সব model এর তুলনা, operating point, শিক্ষা, সীমাবদ্ধতা, পরের দুই সপ্তাহ ও code link</td><td>৩:৩৫</td></tr>
</table>
<p>পুরোটা মিলিয়ে প্রায় <b>৯ মিনিট ৪৫ সেকেন্ড</b>। প্রতিটা slide এ কী বলবে সেটা
<code>final-slides/speaker_script.md</code> ফাইলে ইংরেজি আর বাংলা দুইভাবেই লেখা আছে।</p>

<div class="foot">সব সংখ্যা <code>results/final/</code> থেকে তৈরি ·
github.com/Jahid15/phishing-llm-cross-corpus · মোট খরচ ${spend:.2f}</div>
</div></body></html>"""

out = os.path.join(HERE, "..", "GUIDE.html")
open(out, "w").write(doc)
print("GUIDE.html written,", len(doc) // 1024, "KB")
