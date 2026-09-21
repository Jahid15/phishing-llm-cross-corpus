# Team guide: everything we did, why, and how to defend it

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
good result (Kaggle to SpamAssassin, F1 0.966).
We suspected the two corpora share emails. They do:
87 percent of SpamAssassin sits inside Kaggle.

**Why near-duplicate matching and not exact matching?** Because exact matching
finds 2 of those emails. The aggregate deleted line breaks, which
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
15 to 25 percent of the positive emails are actually phishing.

**Why the placeholder study?** Because the AI-written corpus writes links as the
token `<<link>>`, which appears in 94 of our 150 phishing emails and in none of
the legitimate ones. If a model reacts to the token instead of the content, our
AI-phishing numbers would be fake. We ran two tests. The quick one (compare
emails that have the token with emails that do not) says it is worth
16 points of recall. The proper one (remove the token from the same
emails and ask again) says 0.9 points. The first test was
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
| spamassassin | train and test | 5,803 | SpamAssassin, 2002 public spam corpus |
| ceas08 | train and test | 10,000 | CEAS 2008 challenge corpus |
| trec07 | train and test | 10,000 | TREC 2007 spam track |
| ling | train and test | 2,858 | Ling-Spam, linguistics mailing list |
| enron | train and test | 10,000 | Enron corporate mail, spam and ham |
| kaggle | train and test | 10,000 | Kaggle phishing set, an aggregate of older corpora |
| nazario | test only | 1,554 | Nazario phishing feed, real phishing only |
| nigerian | test only | 3,316 | Nigerian advance fee fraud only |
| ephishllm | test only | 10,000 | E-PhishLLM, written by GPT-4o and GPT-4o-mini (English) |
| ephishllm_it | test only | 2,701 | E-PhishLLM, Italian part |
| ephishllm_de | test only | 2,349 | E-PhishLLM, German part |

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
| Exact text | 2 |
| After removing whitespace | 3,850 |
| Near duplicate (Jaccard 0.8, exactly verified) | 5,032 (87%) |

Kaggle also contains 91% of Ling-Spam and 36% of Enron.
In total 93% of the Kaggle corpus has a near copy somewhere else, and
at the stricter threshold 0.9 it is still 86%.

Duplicates also exist inside each corpus: 9 to 19% of each corpus's
own evaluation emails have a near copy in its training part.

**Validation:** on 400 SpamAssassin emails with no whitespace-exact match in
Kaggle, checked against all 17,505 Kaggle emails by brute force, our matcher has
precision 1.00 and recall 1.00.

### 4.2 Removing the copies changes the results

| Setting | SpamAssassin fold, F1 |
|---|---|
| Train on the other five corpora as they are | 0.947 |
| Remove the same number of emails at random | 0.947 |
| Remove the near duplicates | 0.840 |

Single-corpus transfer, Kaggle to SpamAssassin: 0.966 before, 0.672 after.

### 4.3 What the corpora contain

| Corpus | Positives that are phishing | Positives that are spam |
|---|---|---|
| spamassassin | 19% | 81% |
| ceas08 | 15% | 85% |
| trec07 | 25% | 75% |
| ling | 19% | 79% |
| enron | 21% | 79% |
| kaggle | 25% | 75% |

Two annotators agreed on 86% of 300 doubly annotated emails (kappa 0.35).

### 4.4 The model comparison

| Model | Unseen-corpus F1 | False alarms | AI-phishing F1 | Cost per 1,000 |
|---|---|---|---|---|
| Gemini-3.1-Flash-Lite | 0.960 | 2% | 0.950 | $0.080 |
| GPT-4o-mini | 0.950 | 4% | 0.917 | $0.046 |
| Qwen-2.5-7B | 0.928 | 3% | 0.819 | $0.033 |
| Llama-3.1-8B | 0.881 | 21% | 0.817 | $0.012 |
| Gemma-3-12B | 0.882 | 25% | 0.955 | $0.017 |
| Llama-3.2-3B | 0.850 | 5% | 0.507 | $0.017 |
| Phi-4-14B | 0.727 | 28% | 0.759 | $0.022 |
| Llama-3.2-1B | 0.623 | 60% | 0.474 | $0.009 |
| TF-IDF + LogReg | 0.899 | 10% | 0.640 | free |
| TF-IDF + NB | 0.894 | 7% | 0.631 | free |
| DistilBERT | 0.891 | 6% | 0.540 | free |

### 4.5 At a realistic amount of phishing (5% of mail)

| Model | F1 at 5% | Legitimate emails wrongly flagged per 1,000 |
|---|---|---|
| Gemini-3.1-Flash-Lite | 0.833 | 16 |
| Qwen-2.5-7B | 0.725 | 28 |
| TF-IDF + LogReg | 0.484 | 91 |
| DistilBERT | 0.560 | 60 |
| Gemma-3-12B | 0.289 | 239 |

### 4.6 Two-stage detector

TF-IDF first, and only the mail it flags goes to Qwen:
F1 0.911, false alarms 1.1%, cost $0.0161 per 1,000,
which is about half the cost of running Qwen on everything.

### 4.7 Explanations

When the verdict is right, the reason is grounded in the email about 9 times in
10. When the verdict is wrong, only 53% of reasons are grounded: a wrong
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
   agreement (86%, kappa 0.35); we did not hand-label everything.
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
0.97 F1 and is really 0.67.

**Could the drop just be from having less training data?** No, and we tested
exactly that. Removing the same number of emails at random leaves the score
unchanged (0.947 against 0.947 raw); removing the duplicates drops it to
0.840.

**How do you know the near duplicates are real duplicates?** Every candidate
pair is verified with the exact Jaccard similarity, not the MinHash estimate,
and we validated the whole matcher against brute force on 400 hard cases:
precision 1.00, recall 1.00. We also read pairs by hand; they are the same
messages with different line breaks.

**Why is 0.8 the threshold?** It is the standard value used for deduplicating
text corpora. We also report 0.7 and 0.9: at 0.9 the Kaggle figure is still
86%, so the finding does not depend on the threshold.

**Which model should we use?** For a small budget, a TF-IDF filter in front of
zero-shot Qwen-2.5-7B: F1 0.911, 1.1% false alarms, $0.0161 per 1,000
emails. If a paid API is possible, Gemini-3.1-Flash-Lite was better than every
open model on every axis we measured.

**Why not GPT-4 or a big model?** We did run current commercial models as a
reference, and they are ahead. Our research question is what a low-budget
organisation can deploy, which is why the open models are the focus.

**Isn't Gemma the best, it has the highest AI-phishing score?** It catches the
most, but it flags 25% of legitimate mail. At a realistic 5% phishing rate
that is 239 false alerts per 1,000 emails, so it belongs in front of a
human review queue, not in front of a delete button.

**Why is Phi-4 so low?** In 37% of emails it ignored the instruction to
answer in one word and started explaining, so no verdict fit in the output
budget. We report it as a format-compliance failure, and we also ran it with a
larger output budget.

**Did the models just react to the `<<link>>` token in the AI corpus?** No, and
this is worth telling properly. Comparing emails that carry the token with
emails that do not shows a 16 point recall gap, which looks damning. But when we
remove the token from the same emails and ask again, the verdicts move by
0.9 points. The first comparison was confounded: link-based lures are
easier to spot than text-only business email compromise, token or not. We
publish the sanitised copies of the test set so anyone can check.

**Why did few-shot prompting hurt?** Because the examples came from corpora from
2002 to 2008, which teach the model that phishing looks like old spam. When we
swapped in AI-written examples and changed nothing else, the AI-phishing score
recovered. That is the controlled version of the claim.

**How much did all this cost?** $1.58 of API calls in total, on one 8 GB
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
