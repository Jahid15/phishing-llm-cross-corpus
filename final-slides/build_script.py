"""Writes speaker_script.md for the current deck, with numbers from numbers.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
n = json.load(open(os.path.join(HERE, "numbers.json")))
main = {r["model"]: r for r in n["main"]}
loco = {(r["model"], r["test"], r["setting"]): r for r in n["classical_loco"]}
comp = [r for r in n["label_study_summary"] if r["row"] == "composition"]
base = {r["model"]: r for r in n["base_rate"]}
casc = n["cascade"]
ph = {r["model"]: r for r in n["placeholder_effect"] if r["test_set"] == "ephishllm"}
pair = [r for r in n["placeholder_effect"] if r["test_set"] == "ephishllm paired"]
thr = {(r["source"], r["threshold"]): r for r in n["overlap_thresholds"]}
mv = n["matcher_validation_summary"][0]
sa = n["sa_in_kaggle"]
conf = next(c for c in casc if c["stage1"] == "TF-IDF + LogReg" and c["stage2"] == "Qwen-2.5-7B" and c["policy"] == "confirm")
lf = lambda t, s: loco[("logreg", t, s)]["f1"]
split_gap = sum(r["gap"] for r in ph.values()) / len(ph) * 100
paired_gap = sum(r["gap"] for r in pair) / max(1, len(pair)) * 100

doc = f"""# Final Update: speaker script

16 slides, about 10 minutes. Sinha slides 1 to 5, Saimon 6 to 8, Faria 9 to 16.
Press `N` in the deck for the timing notes. Every number here comes from
`results/final/`; if the slide and this script ever differ, trust the slide.

---

## Sinha

### 1. Title (15 sec)

EN: Good morning. We are Group 18. In the proposal we showed you an empty table
and said the question marks were the project. Today it is filled in, and a few
things in it surprised us.

BN: সবাইকে শুভেচ্ছা। আমরা Group 18। Proposal এ একটা খালি table দেখিয়ে বলেছিলাম,
প্রশ্নবোধক চিহ্নগুলোই আমাদের project। আজ সেটা পূরণ করা, আর কিছু ফলাফল আমাদের নিজেদেরই অবাক করেছে।

### 2. Where we started (45 sec)

EN: In July we reproduced the literature with a method older than deep learning
and got the same 97 to 99 percent. Then we trained on one corpus and tested on
another, and F1 fell from 0.99 to 0.30. Since the proposal we corrected three
things. We are not the first to test across corpora, two 2025 and 2026 papers
did that; ours is what they skip. We added a control, because removing
duplicates also removes data. And we now verify every duplicate pair exactly
instead of trusting an estimate.

BN: জুলাইতে আমরা deep learning এরও পুরনো একটা পদ্ধতি দিয়ে সেই ৯৭ থেকে ৯৯ percent
পেয়েছিলাম। তারপর এক corpus এ train করে অন্যটায় test করলাম, F1 ০.৯৯ থেকে ০.৩০ এ নামল।
Proposal এর পর তিনটা জিনিস ঠিক করেছি। আমরা প্রথম না, ২০২৫ ও ২০২৬ এর দুইটা paper আগেই
cross-corpus test করেছে; আমাদের কাজ ওরা যেটা বাদ দিয়েছে সেটা। আমরা একটা control যোগ
করেছি, কারণ duplicate সরালে data ও কমে যায়। আর প্রতিটা duplicate জোড়া এখন আন্দাজ নয়,
হিসাব করে যাচাই করা।

### 3. Objectives (30 sec)

EN: All six objectives from the proposal are done, and review added four more:
a label study, a base-rate analysis, two-stage detectors, and explanation
quality.

BN: Proposal এর ছয়টা objective ই শেষ, আর review এর পর আরো চারটা যোগ হয়েছে: label
study, base-rate বিশ্লেষণ, দুই ধাপের detector, আর explanation এর মান যাচাই।

### 4. Methodology (45 sec)

EN: Six steps. The one to look at is the control. Decontamination removes
training emails, so on its own a drop could just mean less data. We therefore
run a third setting that removes the same number of emails at random. If that
changes nothing, the cause is the duplicates.

BN: ছয়টা ধাপ। যেটা খেয়াল করবেন সেটা হলো control। Decontamination training email
সরিয়ে দেয়, তাই score কমলে সেটা শুধু কম data র কারণেও হতে পারত। তাই তৃতীয় একটা setting
এ আমরা সমান সংখ্যক email এলোমেলোভাবে সরাই। সেখানে কিছু না বদলালে বুঝতে হবে কারণটা
duplicate গুলোই।

### 5. Experimental details (45 sec)

EN: Nine sources, six of them take turns as the held-out corpus. Every model,
local, open or paid, is scored on the same fixed 300 emails per test set. Seed
42, one 8 GB laptop, every raw answer saved, total API spend {n['total_spend_usd']:.2f} dollars.

BN: নয়টা source, তার ছয়টা পালা করে held-out corpus হয়। প্রতিটা model, local হোক,
open হোক বা paid, প্রতি test set এ একই ৩০০টা email এ score পায়। Seed 42, একটা 8 GB
laptop, প্রতিটা raw উত্তর সংরক্ষিত, মোট API খরচ {n['total_spend_usd']:.2f} dollar।

---

## Saimon

### 6. Overlap (55 sec)

EN: How many SpamAssassin emails are inside the Kaggle set? Compared exactly,
the way most people would: {sa['exact_raw'][0]}. With whitespace removed: {sa['exact_norm'][0]:,}. With
near-duplicate matching: {sa['near'][0]:,}, which is {sa['near'][1]:.0f} percent of SpamAssassin.
{thr[('kaggle', 0.8)]['pct']:.0f} percent of Kaggle has a copy somewhere else, and at the stricter
threshold it is still {thr[('kaggle', 0.9)]['pct']:.0f} percent. Against brute force our matcher has
precision {mv['precision']:.2f} and recall {mv['recall']:.2f}.

BN: Kaggle set এর ভিতরে SpamAssassin এর কয়টা email আছে? হুবহু মিলালে {sa['exact_raw'][0]} টা।
Whitespace বাদ দিলে {sa['exact_norm'][0]:,}। Near-duplicate matching দিয়ে {sa['near'][0]:,}, মানে SpamAssassin এর
{sa['near'][1]:.0f} percent। Kaggle এর {thr[('kaggle', 0.8)]['pct']:.0f} percent এর copy অন্য কোথাও আছে, আর কড়া threshold এও
{thr[('kaggle', 0.9)]['pct']:.0f} percent। Brute force এর সাথে মিলিয়ে আমাদের matcher এর precision {mv['precision']:.2f}, recall {mv['recall']:.2f}।

### 7. Leakage and the control (60 sec)

EN: This is the most important slide. On SpamAssassin, training on the other
five corpora gives F1 {lf('spamassassin','loco_raw'):.3f}. Remove the same number of emails at random:
{lf('spamassassin','loco_random'):.3f}, no change. Remove the duplicates: {lf('spamassassin','loco_clean'):.3f}. Up to twelve points
disappear, and only when we remove the right emails. CEAS and TREC, which share
nothing with the others, do not move at all.

BN: এটাই সবচেয়ে গুরুত্বপূর্ণ slide। SpamAssassin এ বাকি পাঁচটা corpus এ train করলে F1
{lf('spamassassin','loco_raw'):.3f}। সমান সংখ্যক email এলোমেলোভাবে সরালে {lf('spamassassin','loco_random'):.3f}, কোনো পরিবর্তন নেই। Duplicate
গুলো সরালে {lf('spamassassin','loco_clean'):.3f}। বারো point পর্যন্ত উধাও, আর সেটা শুধু ঠিক email গুলো সরালেই।
CEAS আর TREC, যাদের সাথে কারো মিল নেই, একটুও নড়ে না।

### 8. What the benchmarks contain (45 sec)

EN: Then we asked what the positive class actually is. An LLM annotator, with a
second annotator on 300 emails, finds that only {min(r['phishing_pct'] for r in comp):.0f} to {max(r['phishing_pct'] for r in comp):.0f} percent of the
positive emails are phishing. The rest is ordinary bulk spam. So a paper
reporting phishing detection on these corpora is mostly reporting spam
detection.

BN: তারপর আমরা দেখলাম positive class আসলে কী। একটা LLM annotator, আর ৩০০ email এ
দ্বিতীয় একজন annotator দিয়ে দেখা গেল positive email গুলোর মাত্র {min(r['phishing_pct'] for r in comp):.0f} থেকে {max(r['phishing_pct'] for r in comp):.0f} percent
আসলে phishing। বাকিটা সাধারণ spam। মানে এই corpus গুলোতে "phishing detection" বললেও
আসলে বেশিরভাগ spam detection মাপা হচ্ছে।

---

## Faria

### 9. The main table (60 sec)

EN: Every detector on the same emails. Read three rows. Gemini-3.1-Flash-Lite,
a paid model, is best at {main['Gemini-3.1-Flash-Lite']['unseen_f1_mean']:.3f} with {100*main['Gemini-3.1-Flash-Lite']['false_alarm_rate']:.1f} percent false alarms.
Zero-shot Qwen-2.5-7B is the best open model at {main['Qwen-2.5-7B']['unseen_f1_mean']:.3f} for about three cents
per thousand emails. And look at the published BERT detector: {main['BERT-phishing (published)']['unseen_f1_mean']:.3f} on our
corpora, the highest number in the table, but {main['BERT-phishing (published)']['ai_phishing_f1']:.3f} on AI-written phishing. It
was trained on the corpora we test on.

BN: সব detector একই email এ। তিনটা row পড়ুন। Gemini-3.1-Flash-Lite, একটা paid model,
সবার উপরে {main['Gemini-3.1-Flash-Lite']['unseen_f1_mean']:.3f}, ভুল alarm {100*main['Gemini-3.1-Flash-Lite']['false_alarm_rate']:.1f} percent। Zero-shot Qwen-2.5-7B সেরা open model,
{main['Qwen-2.5-7B']['unseen_f1_mean']:.3f}, হাজার email এ প্রায় তিন cent। আর published BERT detector দেখুন: আমাদের
corpus এ {main['BERT-phishing (published)']['unseen_f1_mean']:.3f}, table এর সর্বোচ্চ, কিন্তু AI এর লেখা phishing এ {main['BERT-phishing (published)']['ai_phishing_f1']:.3f}। ওটা ঠিক
সেই corpus গুলোতেই train করা যেগুলোতে আমরা test করছি।

### 10. The token that looked like a shortcut (55 sec)

EN: We checked our own good result. The AI corpus writes links as the token
"double angle bracket link", in 94 of 150 phishing emails and in none of the
legitimate ones. Comparing emails that have it with emails that do not suggests
it is worth {split_gap:.0f} points of recall. But when we remove the token from the same
emails and ask again, the answers move by {paired_gap:.1f} points. The first test was
confounded: emails with links are simply easier than text-only attacks. The
result stands, and we publish the sanitised test sets.

BN: আমরা নিজেদের ভালো ফলাফলটাই যাচাই করেছি। AI corpus এ link গুলো একটা token দিয়ে লেখা,
১৫০টা phishing email এর ৯৪টায় আছে, আর legitimate কোনোটায় নেই। যেগুলোতে token আছে আর
যেগুলোতে নেই সেগুলো তুলনা করলে মনে হয় token টা {split_gap:.0f} point recall এর মূল্য রাখে। কিন্তু একই
email থেকে token সরিয়ে আবার জিজ্ঞেস করলে উত্তর বদলায় মাত্র {paired_gap:.1f} point। প্রথম test টা
বিভ্রান্তিকর ছিল: link ওয়ালা email এমনিতেই সহজ। ফলাফল টিকে গেছে, আর আমরা sanitised
test set প্রকাশ করেছি।

### 11. Operating points (55 sec)

EN: Our test sets are balanced, a mailbox is not. At five percent phishing the
ranking changes: Gemma, the best open model on AI phishing, would flag {base['Gemma-3-12B']['false_alerts_per_1000@0.05']:.0f}
good emails in every thousand. And a two-stage detector, TF-IDF first and the
LLM only on what it flags, gives F1 {conf['unseen_f1']:.3f} with {100*conf['false_alarm']:.1f} percent false alarms for
{conf['usd_per_1000']:.4f} dollars per thousand, which is cheaper and cleaner than either part alone.

BN: আমাদের test set ভারসাম্যপূর্ণ, কিন্তু আসল inbox না। পাঁচ percent phishing ধরলে ক্রম
বদলে যায়: Gemma, AI phishing এ সেরা open model, হাজারে {base['Gemma-3-12B']['false_alerts_per_1000@0.05']:.0f} টা ভালো email কে ভুল করে
ধরবে। আর দুই ধাপের detector, আগে TF-IDF, তারপর শুধু চিহ্নিত email গুলো LLM এ, F1 {conf['unseen_f1']:.3f},
ভুল alarm {100*conf['false_alarm']:.1f} percent, খরচ হাজারে {conf['usd_per_1000']:.4f} dollar, যা আলাদা আলাদা দুইটার চেয়েই ভালো।

### 12. Explanations (40 sec)

EN: When the verdict is right, the model's reason points at something really in
the email about nine times in ten. When the verdict is wrong, only about half
the reasons do. A wrong answer usually comes with an invented justification, so
showing an explanation to a user is only safe if the verdict is checked first.

BN: উত্তর ঠিক হলে model এর কারণটা দশবারে প্রায় নয়বার email এ সত্যিই থাকা কিছু দেখায়।
উত্তর ভুল হলে অর্ধেকের মতো। ভুল উত্তরের সাথে সাধারণত বানানো কারণ আসে, তাই ব্যবহারকারীকে
explanation দেখানো তখনই নিরাপদ যখন verdict আগে যাচাই করা হয়।

### 13. What it means (40 sec)

EN: Four things. Check overlap before claiming generalisation. Cheap detectors
are usable in the right order. Report false alarms and the base rate, not one
F1. And be suspicious of your own good numbers, including ours.

BN: চারটা কথা। Generalisation দাবি করার আগে overlap দেখুন। সস্তা detector ঠিক ক্রমে
সাজালে কাজে লাগে। একটা F1 না দিয়ে ভুল alarm আর base rate জানান। আর নিজের ভালো
ফলাফলকেও সন্দেহ করুন, আমাদেরটা সহ।

### 14. Limitations (35 sec)

EN: We are not the first to test across corpora. Our test sets are 300 emails,
so small differences are not meaningful. Our annotator is a model, not us. And
the LLMs may have seen the old corpora in pre-training, which is why the 2025
AI-written corpus matters most.

BN: আমরা প্রথম না যারা cross-corpus test করেছে। আমাদের test set ৩০০ email এর, তাই ছোট
পার্থক্যের মানে নেই। আমাদের annotator একটা model, আমরা নিজেরা না। আর LLM গুলো পুরনো
corpus আগেই দেখে থাকতে পারে, এজন্যই ২০২৫ এর AI corpus সবচেয়ে গুরুত্বপূর্ণ।

### 15. Next two weeks (30 sec)

EN: Hand-label 300 positives ourselves to replace the model annotator, add
threshold calibration, enlarge the test sets for the top three models, and
package the deduplication script so other groups can run it on their own data.

BN: নিজেরা ৩০০টা positive email হাতে label করব যাতে model annotator লাগে না, threshold
calibration যোগ করব, সেরা তিনটা model এর test set বড় করব, আর deduplication script টা
এমনভাবে গুছাবো যাতে অন্য group রা নিজেদের data তে চালাতে পারে।

### 16. Links and close (20 sec)

EN: Everything is public: code, every raw model answer, the paper, the research
log and a Colab notebook. {n['llm_calls']:,} model calls, {n['total_spend_usd']:.2f} dollars, one laptop. High
accuracy on one dataset is easy. Honest evaluation is the hard part. Thank you.

BN: সবকিছু public: code, প্রতিটা raw উত্তর, paper, research log আর একটা Colab notebook।
{n['llm_calls']:,} টা model call, {n['total_spend_usd']:.2f} dollar, একটা laptop। একটা dataset এ high accuracy পাওয়া সহজ।
কঠিন কাজটা হলো সৎ evaluation। ধন্যবাদ।

---

## The five questions most likely to come

1. *Could the drop be from less training data?* No. Removing the same number of
   emails at random changes the score by at most {abs(lf('spamassassin','loco_raw')-lf('spamassassin','loco_random'))*100:.1f} points; removing the
   duplicates changes it by {(lf('spamassassin','loco_raw')-lf('spamassassin','loco_clean'))*100:.0f}.
2. *How do you know the duplicates are real?* Every pair is verified with the
   exact similarity, and the matcher matches brute force on 400 hard cases
   (precision {mv['precision']:.2f}, recall {mv['recall']:.2f}).
3. *Which model should we use?* TF-IDF in front of zero-shot Qwen-2.5-7B, or a
   paid model if the budget allows: Gemini was better on every axis.
4. *Is Gemma not the best, it wins on AI phishing?* It flags {100*main['Gemma-3-12B']['false_alarm_rate']:.0f} percent of
   legitimate mail. It belongs in front of a human review queue.
5. *What did it cost?* {n['total_spend_usd']:.2f} dollars of API calls, on one 8 GB laptop.
"""
open(os.path.join(HERE, "speaker_script.md"), "w").write(doc)
print("speaker_script.md written,", len(doc.split()), "words")
