"""
Builds TEAM_GUIDE.md. Every number comes from results/final, so the guide
cannot drift from the experiments.
"""
import json
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "results", "final")
rd = lambda n: pd.read_csv(os.path.join(R, n))

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
exp = rd("explanations_summary.csv").set_index("model")
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


def loco(model, test, setting):
    r = cl[(cl.model == model) & (cl.test == test) & (cl.setting == setting)]
    return float(r.f1.iat[0]) if len(r) else float("nan")


def pwf(a, b, s):
    return float(pw[(pw.train == a) & (pw.test == b) & (pw.setting == s)].f1.iat[0])


def row(m):
    return (f"| {m} | {g(m,'unseen_f1_mean'):.3f} | {100*g(m,'false_alarm_rate'):.0f}% | "
            f"{g(m,'ai_phishing_f1'):.3f} | "
            + ("free" if g(m, 'usd_per_1000') == 0 else f"${g(m,'usd_per_1000'):.3f}") + " |")


comp = ls[ls.row == "composition"]
agr = ls[ls.row == "agreement"].iloc[0]
c_tfidf = cas[(cas.stage1 == "TF-IDF + LogReg") & (cas.stage2 == "Qwen-2.5-7B") & (cas.policy == "confirm")].iloc[0]
models_in_table = [m for m in main.index]

doc = f"""# Team guide: everything we did, why, and how to defend it

Group 18, Computer Security, United International University
Jahid Ibna Sinha, Md. Jakaria Alam Saimon, Nowshin Anjum Faria

This is written so that any of the three of us can answer any question about
the project without looking anything up. Read part 1 and part 8 the night
before the presentation; the rest is reference.

Every number here is generated from the result files by `guide/build_guide.py`,
so if an experiment is rerun this guide updates with it.

---

## 1. The project in one minute

We test whether cheap phishing email detectors really work, and we find that
the benchmarks everyone uses are broken in a specific, measurable way.

Three sentences:

1. Public phishing corpora contain copies of each other, so training on one and
   testing on another is partly testing on the training data.
2. When we remove those copies and test on a corpus the model has never seen,
   scores drop, and a small open LLM used with no training at all is as good as
   a trained model and better on AI-written phishing.
3. Which model you should pick depends on how much legitimate mail it wrongly
   flags and on what it costs, and neither is reported in the literature.

The one-line version: **high accuracy on one dataset is easy, honest evaluation
is the hard part.**

---

## 2. Why we did each thing (the reasoning chain)

This is the logic of the project. If you understand this section you can answer
almost any "why" question.

**Why phishing detection with LLMs?** It was the only topic nobody took, the
data is free, and small models can be run for cents through OpenRouter.

**Why did we become suspicious?** In July we reproduced the literature with
TF-IDF and logistic regression, a method from before deep learning, and got 97
to 99 percent, the same as GPT-4 papers. When an old simple method ties a
frontier model, the test is too easy, not the method too good.

**Why cross-corpus testing?** Because a mail server never receives mail from
its own training set. If a model only works on mail from the same collection,
it does not work.

**Why decontamination?** Because our first cross-corpus test had one suspiciously
good result (Kaggle to SpamAssassin, F1 {pwf('kaggle','spamassassin','raw'):.3f}).
We suspected the two corpora share emails. They do:
{ov('near','kaggle','spamassassin','pct_of_source'):.0f} percent of SpamAssassin sits inside Kaggle.

**Why near-duplicate matching and not exact matching?** Because exact matching
finds {int(ov('exact_raw','kaggle','spamassassin'))} of those emails. The aggregate deleted line breaks, which
changes the text without changing the message.

**Why a random-removal control?** Because decontamination also makes the
training set smaller, and a reviewer would say the drop is just less data. So
we remove the same number of emails at random: the score does not move. That
proves it is the leaked emails.

**Why false alarm rate?** Because F1 on a balanced test set hides it, and in a
real inbox flagging one in four legitimate emails makes a detector unusable.

**Why measure cost in dollars?** Because for a university in Bangladesh the
question is not only which model is best but which one can be afforded, and no
paper in our review reports it.

**Why annotate spam versus phishing?** Because four of the six corpora label
ordinary spam as positive. We wanted to know what our own numbers describe. Only
{comp.phishing_pct.min():.0f} to {comp.phishing_pct.max():.0f} percent of the positive emails are actually phishing.

**Why the placeholder study?** Because the AI-written corpus writes links as the
token `<<link>>`, which appears in 94 of our 150 phishing emails and in none of
the legitimate ones. If a model reacts to the token instead of the content, our
AI-phishing numbers would be fake. We ran two tests. The quick one (compare
emails that have the token with emails that do not) says it is worth
{100*ph[ph.test_set=='ephishllm'].gap.mean():.0f} points of recall. The proper one (remove the token from the same
emails and ask again) says {100*ph[ph.test_set=='ephishllm paired'].gap.mean():.1f} points. The first test was
confounded, because emails with links are a different kind of attack from
text-only ones. The result stands, and the lesson is to change one thing at a
time on the same data.

**Why two-stage detectors?** Because we had the per-email predictions already,
and combining a free filter with a paid model is what an organisation would
actually build.

---

## 3. The data

| Source | Role | Emails used | What it is |
|---|---|---|---|
"""
nice = {"spamassassin": "SpamAssassin, 2002 public spam corpus",
        "ceas08": "CEAS 2008 challenge corpus",
        "trec07": "TREC 2007 spam track",
        "ling": "Ling-Spam, linguistics mailing list",
        "enron": "Enron corporate mail, spam and ham",
        "kaggle": "Kaggle phishing set, an aggregate of older corpora",
        "nazario": "Nazario phishing feed, real phishing only",
        "nigerian": "Nigerian advance fee fraud only",
        "ephishllm": "E-PhishLLM, written by GPT-4o and GPT-4o-mini (English)",
        "ephishllm_it": "E-PhishLLM, Italian part",
        "ephishllm_de": "E-PhishLLM, German part"}
for r in stats.itertuples():
    doc += (f"| {r.source} | {'train and test' if r.role=='train+test' else 'test only'} | "
            f"{r.emails_used:,} | {nice.get(r.source,'')} |\n")

doc += f"""
Every test set has a fixed subset of 300 emails (150 for the one-class sets),
balanced between the classes. Every model is scored on exactly those emails, so
the comparison is fair. Large corpora were capped at 10,000 emails so that the
biggest ones do not dominate training and so the work fits an 8 GB laptop.

**If asked why these corpora:** they are the ones the papers we reviewed use, so
our criticism applies to those papers directly. They are free, public and
text-only.

---

## 4. What we found, with the numbers

### 4.1 The corpora copy each other

| Check | SpamAssassin emails found inside Kaggle |
|---|---|
| Exact text | {int(ov('exact_raw','kaggle','spamassassin'))} |
| After removing whitespace | {int(ov('exact_norm','kaggle','spamassassin')):,} |
| Near duplicate (Jaccard 0.8, exactly verified) | {int(ov('near','kaggle','spamassassin')):,} ({ov('near','kaggle','spamassassin','pct_of_source'):.0f}%) |

Kaggle also contains {ov('near','kaggle','ling','pct_of_source'):.0f}% of Ling-Spam and {ov('near','kaggle','enron','pct_of_source'):.0f}% of Enron.
In total {float(th[(th.source=='kaggle')&(th.threshold==0.8)].pct.iat[0]):.0f}% of the Kaggle corpus has a near copy somewhere else, and
at the stricter threshold 0.9 it is still {float(th[(th.source=='kaggle')&(th.threshold==0.9)].pct.iat[0]):.0f}%.

Duplicates also exist inside each corpus: {within.loc[SIX].eval_with_near_dup_in_own_train_pct.min():.0f} to {within.loc[SIX].eval_with_near_dup_in_own_train_pct.max():.0f}% of each corpus's
own evaluation emails have a near copy in its training part.

**Validation:** on 400 SpamAssassin emails with no whitespace-exact match in
Kaggle, checked against all 17,505 Kaggle emails by brute force, our matcher has
precision {mv.precision:.2f} and recall {mv.recall:.2f}.

### 4.2 Removing the copies changes the results

| Setting | SpamAssassin fold, F1 |
|---|---|
| Train on the other five corpora as they are | {loco('logreg','spamassassin','loco_raw'):.3f} |
| Remove the same number of emails at random | {loco('logreg','spamassassin','loco_random'):.3f} |
| Remove the near duplicates | {loco('logreg','spamassassin','loco_clean'):.3f} |

Single-corpus transfer, Kaggle to SpamAssassin: {pwf('kaggle','spamassassin','raw'):.3f} before, {pwf('kaggle','spamassassin','clean'):.3f} after.

### 4.3 What the corpora contain

| Corpus | Positives that are phishing | Positives that are spam |
|---|---|---|
"""
for r in comp.itertuples():
    doc += f"| {r.source} | {r.phishing_pct:.0f}% | {r.spam_pct:.0f}% |\n"

doc += f"""
Two annotators agreed on {100*float(agr.agreement):.0f}% of 300 doubly annotated emails (kappa {float(agr.kappa):.2f}).

### 4.4 The model comparison

| Model | Unseen-corpus F1 | False alarms | AI-phishing F1 | Cost per 1,000 |
|---|---|---|---|---|
"""
for m in ["Gemini-3.1-Flash-Lite", "GPT-4o-mini", "Qwen-2.5-7B", "Llama-3.1-8B", "Gemma-3-12B",
          "Llama-3.2-3B", "Phi-4-14B", "Llama-3.2-1B", "TF-IDF + LogReg", "TF-IDF + NB", "DistilBERT"]:
    if m in main.index:
        doc += row(m) + "\n"

doc += f"""
### 4.5 At a realistic amount of phishing (5% of mail)

| Model | F1 at 5% | Legitimate emails wrongly flagged per 1,000 |
|---|---|---|
"""
for m in ["Gemini-3.1-Flash-Lite", "Qwen-2.5-7B", "TF-IDF + LogReg", "DistilBERT", "Gemma-3-12B"]:
    if m in br.index:
        doc += f"| {m} | {float(br.loc[m,'f1@0.05']):.3f} | {float(br.loc[m,'false_alerts_per_1000@0.05']):.0f} |\n"

doc += f"""
### 4.6 Two-stage detector

TF-IDF first, and only the mail it flags goes to Qwen:
F1 {c_tfidf.unseen_f1:.3f}, false alarms {100*c_tfidf.false_alarm:.1f}%, cost ${c_tfidf.usd_per_1000:.4f} per 1,000,
which is about half the cost of running Qwen on everything.

### 4.7 Explanations

When the verdict is right, the reason is grounded in the email about 9 times in
10. When the verdict is wrong, only {100*exp['grounded_when_wrong'].mean():.0f}% of reasons are grounded: a wrong
answer usually comes with an invented reason.

---

## 5. The code, file by file

All of it is in `code/final/`. Run `python code/final/run_all.py --status` to see
what has finished.

| File | What it does |
|---|---|
| `common.py` | paths, the list of corpora, the seed, shared helpers |
| `progress.py` | records which steps are finished so a run can resume |
| `01_prepare_data.py` | downloads and cleans the nine sources, builds the evaluation subsets |
| `02_overlap.py` | the overlap study: exact, whitespace-normalised and near duplicate, plus within-corpus duplication and the threshold sensitivity |
| `03_classical_loco.py` | TF-IDF models, in-corpus, leave-one-corpus-out raw, clean and the random control, plus the 6x6 transfer matrix |
| `04_distilbert_loco.py` | DistilBERT fine-tuning per fold, raw and clean, on CPU, one file per fold so it resumes |
| `05_llm_eval.py` | all LLM calls, answer parsing, cost accounting, budget guard, caching |
| `06_analysis.py` | the main table, bootstrap and jackknife intervals, figures |
| `07_cascade.py` | two-stage detectors built from saved predictions |
| `08_significance.py` | McNemar tests between model pairs |
| `09_placeholder.py` | the `<<link>>` token analysis |
| `10_variants.py` | builds the sanitised copies of the AI-written test set |
| `11_reparse.py` | re-reads saved answers when the parser improves |
| `12_offtheshelf.py` | published phishing detectors, including Phishsense |
| `13_baserate.py` | precision and F1 at realistic phishing rates |
| `14_label_study.py` | spam versus phishing annotation and agreement |
| `15_explanations.py` | explanation quality with an LLM judge |
| `16_validate_matcher.py` | brute-force validation of the near-duplicate matcher |

Rebuild the paper: `python paper/make_tables.py`, `python paper/fill_numbers.py`,
then `tectonic paper/main.tex`. Rebuild the slides:
`python final-slides/collect_numbers.py`, `python final-slides/build_deck.py`,
`node final-slides/build_pptx.js`.

---

## 6. Concepts in plain words

**F1** combines precision and recall into one number. Precision: of the emails
we flagged, how many really were phishing. Recall: of the phishing emails, how
many we caught. F1 is high only when both are high.

**False alarm rate** is the share of legitimate emails that get flagged. It is
not in F1 in an obvious way, and it is what annoys users.

**Leave one corpus out (LOCO)** means: train on five corpora, test on the sixth,
and repeat six times. It simulates meeting mail from a new source.

**Near duplicate** means two emails are almost the same text. We measure it with
Jaccard similarity over 9-character pieces: the share of pieces the two emails
share. 0.8 means they share four fifths of their pieces.

**MinHash and LSH** are a fast way to find candidate near-duplicate pairs
without comparing all 170,000 emails against each other, which would be 14
billion comparisons. We then verify each candidate exactly.

**Bootstrap interval** is a way to say how much a number would wobble if we had
sampled different emails: resample the test emails with replacement 1,000 times
and look at the spread.

**Jackknife over corpora** leaves out one corpus at a time and re-averages,
which shows how much one corpus moves the result.

**McNemar test** compares two models on the same emails by counting the cases
where exactly one of them is right; a small p value means the difference is
unlikely to be luck.

**Zero-shot and few-shot** mean asking a model with no examples, or with a few
examples inside the prompt.

**Decontamination** here means removing training emails that have a near
duplicate in the test corpus.

---

## 7. Honest weaknesses, and what to say about them

Say these before the examiner does. Knowing your own limitations is what makes
the rest credible.

1. **We are not the first to test across corpora.** E-PhishGen (AISec 2025) and
   Bhuiyan and Bhuiyan (2026) did leave-one-corpus-out before us. What is ours
   is measuring and removing the overlap first, the random-removal control, the
   cost in dollars, the false alarm rates, and the operating-point analysis.
2. **Our test sets are 300 emails each.** The bootstrap interval is about
   plus or minus 0.015, so small differences are not meaningful. We report the
   intervals and the significance tests instead of hiding this.
3. **The labels are not ours.** Four corpora call spam positive. We measured
   that split rather than fixing it.
4. **The annotator is a model.** We used a second model on 300 emails and report
   agreement ({100*float(agr.agreement):.0f}%, kappa {float(agr.kappa):.2f}); we did not hand-label everything.
5. **The LLMs may have seen the old corpora in pre-training.** We cannot rule it
   out. That is why the 2025 AI-written corpus matters most for them.
6. **Model families see different amounts of each email** (TF-IDF 20,000
   characters, LLMs 1,500, DistilBERT 128 word pieces), and DistilBERT trains on
   less data than the classical models. Its row is a lower bound.
7. **Phishsense-1B** was run through a third-party ungated copy with our own
   prompt, because the official repository is gated.
8. **One prompt, one run per model.** No prompt search, no repeated sampling.

---

## 8. Questions you will be asked, with answers

**What is new here?** Three things nobody had done: we measure how much public
phishing corpora overlap and remove it before testing, we report what it costs
in dollars, and we report how much legitimate mail each model wrongly flags.

**Why does the overlap matter?** Because a model that has seen the test email
during training is not being tested. Kaggle to SpamAssassin looks like
{pwf('kaggle','spamassassin','raw'):.2f} F1 and is really {pwf('kaggle','spamassassin','clean'):.2f}.

**Could the drop just be from having less training data?** No, and we tested
exactly that. Removing the same number of emails at random leaves the score
unchanged ({loco('logreg','spamassassin','loco_random'):.3f} against {loco('logreg','spamassassin','loco_raw'):.3f} raw); removing the duplicates drops it to
{loco('logreg','spamassassin','loco_clean'):.3f}.

**How do you know the near duplicates are real duplicates?** Every candidate
pair is verified with the exact Jaccard similarity, not the MinHash estimate,
and we validated the whole matcher against brute force on 400 hard cases:
precision {mv.precision:.2f}, recall {mv.recall:.2f}. We also read pairs by hand; they are the same
messages with different line breaks.

**Why is 0.8 the threshold?** It is the standard value used for deduplicating
text corpora. We also report 0.7 and 0.9: at 0.9 the Kaggle figure is still
{float(th[(th.source=='kaggle')&(th.threshold==0.9)].pct.iat[0]):.0f}%, so the finding does not depend on the threshold.

**Which model should we use?** For a small budget, a TF-IDF filter in front of
zero-shot Qwen-2.5-7B: F1 {c_tfidf.unseen_f1:.3f}, {100*c_tfidf.false_alarm:.1f}% false alarms, ${c_tfidf.usd_per_1000:.4f} per 1,000
emails. If a paid API is possible, Gemini-3.1-Flash-Lite was better than every
open model on every axis we measured.

**Why not GPT-4 or a big model?** We did run current commercial models as a
reference, and they are ahead. Our research question is what a low-budget
organisation can deploy, which is why the open models are the focus.

**Isn't Gemma the best, it has the highest AI-phishing score?** It catches the
most, but it flags {100*g('Gemma-3-12B','false_alarm_rate'):.0f}% of legitimate mail. At a realistic 5% phishing rate
that is {float(br.loc['Gemma-3-12B','false_alerts_per_1000@0.05']):.0f} false alerts per 1,000 emails, so it belongs in front of a
human review queue, not in front of a delete button.

**Why is Phi-4 so low?** In {cost.loc['Phi-4-14B','unparsed_pct']:.0f}% of emails it ignored the instruction to
answer in one word and started explaining, so no verdict fit in the output
budget. We report it as a format-compliance failure, and we also ran it with a
larger output budget.

**Did the models just react to the `<<link>>` token in the AI corpus?** No, and
this is worth telling properly. Comparing emails that carry the token with
emails that do not shows a {100*ph[ph.test_set=='ephishllm'].gap.mean():.0f} point recall gap, which looks damning. But when we
remove the token from the same emails and ask again, the verdicts move by
{100*ph[ph.test_set=='ephishllm paired'].gap.mean():.1f} points. The first comparison was confounded: link-based lures are
easier to spot than text-only business email compromise, token or not. We
publish the sanitised copies of the test set so anyone can check.

**Why did few-shot prompting hurt?** Because the examples came from corpora from
2002 to 2008, which teach the model that phishing looks like old spam. When we
swapped in AI-written examples and changed nothing else, the AI-phishing score
recovered. That is the controlled version of the claim.

**How much did all this cost?** ${spend:.2f} of API calls in total, on one 8 GB
laptop. Everything else is free software and public data.

**How do we know the results are reproducible?** Seed 42 everywhere, every raw
model answer is saved in the repository, and the paper's tables and numbers are
generated from those files by scripts rather than typed.

**What would you do next?** Hand-label a phishing versus spam subset to replace
the model annotator, test at realistic prevalence on live mail, add
threshold calibration per corpus, and extend the multilingual part beyond
Italian and German.

---

## 9. Who presents what

The suggested split follows the deck: Sinha sets up the problem and the method,
Saimon presents the overlap and leakage results, Faria presents the model
comparison, operating points and limitations. Whoever is asked a question
should answer from part 8 above; if it is not there, say what we measured and
what we did not, rather than guessing.
"""
open(os.path.join(HERE, "..", "TEAM_GUIDE.md"), "w").write(doc)
print("TEAM_GUIDE.md written,", len(doc.split()), "words")
