# Research Log: Phishing Email Detection with Small Open LLMs

Group 18, Computer Security, United International University
Jahid Ibna Sinha (011221376), Md. Jakaria Alam Saimon (011221002), Nowshin Anjum Faria (011221372)

This is the story of the project from the first day, written so any of us can
pick it up without asking the others. Each step says what we did, why we did
it, what we found, and what we decided because of it. Dates are when the files
were made.

---

## Step 1. Picking the topic (early July 2026)

The teacher shared the list of topics other groups had already taken: prompt
injection, RAG poisoning, agentic AI security, an MCP survey, malware
detection, npm/PyPI supply chain, cloud misconfiguration, GNSS spoofing and a
few more. Nobody had phishing.

We picked "Phishing Email Detection Using Large Language Models" for three
reasons.

1. No overlap with any other group.
2. All the datasets are free public text files. They run on a normal laptop.
3. The LLM part can go through OpenRouter, where small open models cost a
   fraction of a cent per email. We set ourselves a budget of 5 dollars.

## Step 2. Literature review (15 July 2026)

Files: `literature_review.*`, `Group_18_literature_review.pdf`

We read five papers from 2023 to 2026, in the order the teacher asked
(abstract, the second last paragraph of the introduction, dataset, method,
limitations).

| Paper | What they did | Headline |
|---|---|---|
| Heiding et al. 2024 | GPT-4 wrote phishing, 112 people tested | AI phishing works on humans |
| Koide et al. 2024 (ChatSpamDetector) | GPT-4 with a chain of thought prompt | 99.70% accuracy |
| Uddin et al. 2024 | Fine-tuned RoBERTa + explanations | 98.45% |
| Lin et al. 2025 | 3B models + LoRA + a paid GPT-4o-mini teacher | small models get close to big ones |
| Kuikel et al. 2025 | Faithfulness of explanations | accuracy and faithfulness do not move together |

What we noticed: every paper trains and tests inside one dataset, and none of
them says what it costs to run. That became our starting question.

## Step 3. Preliminary experiments (21 July 2026)

Files: `code/preliminary/`, `results/preliminary/`, `research_gaps.md`

We wanted to test the "99 percent" story ourselves before writing a proposal.
Four small scripts:

- `get_data.py` downloaded Kaggle (17,505 emails), SpamAssassin (5,809), and
  Nazario phishing paired with Enron legitimate mail (3,128).
- `run_baselines.py` trained TF-IDF + Logistic Regression and Naive Bayes with
  an 80/20 split. We got 97.9, 97.3 and 99.2 percent accuracy. A method older
  than deep learning matched GPT-4.
- `run_cross_dataset.py` trained on one corpus and tested on another. The
  Nazario+Enron model fell from F1 0.992 to 0.304 on Kaggle. It called almost
  every unseen phishing email legitimate, yet accuracy stayed at 0.69, so an
  accuracy-only report would hide it.
- `run_llm_zero_shot.py` asked llama-3.2-3b and gemma-3-12b about 100 emails
  per corpus. The 3B model stayed at 0.80 to 0.84 on every corpus. The 12B
  model was worse: precision 0.58, it called almost everything phishing.
  The whole run cost under one cent.

One result looked too good: Kaggle to SpamAssassin kept F1 at 0.97. We wrote
down a suspicion that Kaggle, which is an aggregate, already contains
SpamAssassin emails.

We turned all of this into five gaps: single-dataset evaluation, leakage
between datasets, no AI-written phishing in public corpora, spam and phishing
labels mixed up, and no paper reporting accuracy, robustness and cost together.

## Step 4. Proposal (25 July 2026)

Files: `project_proposal.*`

Title: "Cost Aware Benchmarking of Small Open LLMs for Cross Corpus Phishing
Email Detection". Five objectives: a deduplicated cross-corpus benchmark,
leave-one-corpus-out testing, cheap improvements only, a test on AI-written
phishing, and one table with accuracy, robustness and cost.

## Step 5. Checking the leakage suspicion (11 August 2026)

File: `code/preliminary/check_overlap.py`, `results/preliminary/dataset_overlap.csv`

We hashed every email body after lowercasing and removing all whitespace.
Kaggle and SpamAssassin shared 3,838 emails, which is 66 percent of
SpamAssassin. So the "good transfer" was the model recognising emails it had
already seen. The suspicion became a fact.

## Step 6. Proposal presentation (15 August and 5 September 2026)

Files: `slides/` (first version), `new-slides/` (the version we presented)

Ten slides in three parts. Sinha set up the problem (the task, the state of
the art, and the one paper whose model fell from 97.5 to 70 percent on a new
dataset). Saimon showed our own results (the collapse and the leakage). Faria
showed the plan (six objectives, a six stage pipeline and the empty results
table).

A note we must be honest about: the September deck said "74.4 percent,
4,282 near duplicates, and only 48 exact duplicates". Those numbers came from
a quick near-duplicate run that we never saved in the repository. The saved
script gave 66 percent and 3,838. In the final work (Step 8) we rebuilt the
near-duplicate check properly and the paper only uses numbers that the code
in this repository produces.

## Step 7. Planning the final experiments (18 September 2026)

Before writing any code we checked two things.

First, the E-PhishLLM corpus we promised is real and public
(github.com/pajola/e-phishGen, 16,616 emails, written by GPT-4o-mini). But the
same paper, E-PhishGen (AISec 2025), already tested classical models across
eight legacy corpora. So we could not honestly claim "nobody tests across
datasets". We changed our claim to what is still new: measuring and removing
near-duplicate leakage between corpora before testing, including the Kaggle
aggregate that most LLM papers use, and reporting measured cost next to
accuracy. The paper cites E-PhishGen as the closest work.

Second, the budget. The team agreed on a hard cap of 2 dollars of OpenRouter
credit. The LLM script records the real cost of every call and stops itself
before 1.90.

Decisions we made while planning, and why:

| Decision | Why |
|---|---|
| Six training corpora: SpamAssassin, CEAS-08, TREC-07, Ling, Enron, Kaggle | they all contain both classes, so each can be a held-out test corpus |
| Nazario and Nigerian become test-only | they only contain phishing or fraud. In the preliminary work we paired Nazario with Enron ham, but Enron is now its own corpus, so that pairing would leak into it |
| E-PhishLLM English part only | our models and prompt are English |
| Cap every corpus at 10,000 emails (stratified, seed 42) | TREC, CEAS and Enron are much bigger and would dominate training. It also keeps runs on an 8 GB laptop |
| A fixed 300-email evaluation subset per test set | every model, including the paid LLMs, is scored on exactly the same emails |
| Label 1 = phishing or spam | that is how most corpora are labelled. The LLM prompt says "phishing, scam or spam" so it matches. Recall on Nazario and Nigerian is reported on its own |
| Phishsense-1B left out | its HuggingFace page needs a login token. Listed as a limitation and a two-week task |

## Step 8. Measuring the overlap properly

Script: `code/final/02_overlap.py`

We compared all nine sources at three levels: exact text, exact after removing
all whitespace (our August method), and near duplicate with MinHash.

The first near-duplicate version used 5-word shingles and found fewer copies
than the simple whitespace check, which made no sense. We looked at a matched
pair and saw why: the Kaggle aggregate often deletes line breaks, which glues
two words together ("cream?Isn't"). Word shingles break on that. We switched
to 9-character shingles over letters and digits only.

To make sure the matcher was not inventing matches, we took 400 random
SpamAssassin emails with no whitespace-exact match in Kaggle and searched
Kaggle by brute force. 59 percent had a true copy (Jaccard of at least 0.8),
the same rate MinHash reported. We read several by hand. They were the same
messages with different line breaks or a cut first word.

What we found (SpamAssassin emails that also sit inside Kaggle):

| Check | Found | Share of SpamAssassin |
|---|---|---|
| Exact text, as a model reads it | 2 | 0.03% |
| Whitespace removed (August method) | 3,850 | 66.3% |
| Near duplicate (final) | 5,009 | 86.3% |

Kaggle also holds 90 percent of Ling and 35 percent of Enron. More than half of
Kaggle is Enron. The Kaggle "dataset" is mostly older corpora stitched together.
This replaces the unsaved numbers in the September slides (74.4 percent,
4,282 and 48).

## Step 9. Classical models, leave-one-corpus-out

Script: `code/final/03_classical_loco.py`

For each held-out corpus we trained on the other five twice: once as they are
(raw) and once after removing training emails that have a near duplicate in
the test corpus (clean).

- Kaggle to SpamAssassin, the "good transfer" from July: F1 0.966 raw,
  0.666 clean. It really was leakage.
- In leave-one-corpus-out, cleaning cost Logistic Regression 10 points on
  SpamAssassin, 11.5 on Ling, 5 on Enron and 5 on Kaggle. CEAS and TREC, which
  share almost nothing with the others, did not move at all. That is what we
  would expect if leakage, and not something else, causes the gap.
- Classical models reach only 0.64 to 0.68 F1 on AI-written phishing.

A practical lesson: running DistilBERT at the same time as this job pushed the
8 GB laptop into heavy swapping, so we stopped it and ran the jobs one after
another.

## Step 10. Small LLMs through OpenRouter

Script: `code/final/05_llm_eval.py`

Six models zero-shot on 2,400 emails each, and few-shot (four examples from
the other corpora) for Llama-3.2-3B and Qwen-2.5-7B.

Two problems came up.

1. Gemma-3-12B has a single provider on OpenRouter and it kept answering
   "429 Too Many Requests". Failed calls are saved with zero tokens, and the
   script retries only those on the next run. We ran Gemma on its own with
   two parallel requests so it would stop being throttled.
2. Phi-4 ignored "answer with one word" in 37 percent of emails. It starts
   with "As a large language model..." or "Based on the content..." and the
   5-token limit cuts it off before any verdict. We tried a relaxed mode with
   80 tokens and a parser that reads the verdict out of the text. We dropped
   it after reading the answers: Phi-4 often writes a generic checklist with
   no verdict at all, and the parser read words like "malicious" in that
   advice as a verdict. The paper reports the strict run and explains the
   failure. The discarded answers (cost 0.01 dollars) are kept in
   `results/final/llm_raw_discarded/`.

3. Few-shot gave the most surprising result. Four examples from the other
   corpora raised Qwen-2.5-7B on old corpora (0.928 to 0.937 mean F1) but
   dropped it on AI-written phishing (0.819 to 0.598). Llama-3.2-3B did the
   same. Our reading: examples from 2002 to 2008 corpora teach the model that
   phishing looks like old spam, so polished GPT-written phishing looks
   "normal". Because of this we recommend zero-shot Qwen, not the few-shot
   version that tops the unseen-corpus column.

## Step 11. DistilBERT on an 8 GB laptop

Script: `code/final/04_distilbert_loco.py`

This took three attempts, and the lessons are worth keeping.

1. First run, Apple GPU (MPS), 256 tokens. It shared memory with the classical
   job and the laptop started swapping. One cross-corpus fold took 17 minutes
   instead of about 8. The script also loaded full copies of all six corpora
   and never released GPU memory between folds, so the process grew to 6 GB.
2. We rewrote it to load only the columns it needs, free memory after each
   fold, and save each fold to its own file so a restart resumes where it
   stopped. We also tried capping the GPU memory, which then ran out at 3 GB.
3. We timed one training step on both devices at 128 tokens: 0.85 s on the CPU
   and 0.70 s on the GPU. The CPU is almost as fast and uses memory
   predictably, so the final run uses the CPU (`DEVICE=cpu`) and 128 tokens.
   The subject line and the first hundred or so words carry most phishing
   cues, and the paper states the 128 token limit.

## Step 12. The final numbers (18 September 2026, evening)

Script: `code/final/06_analysis.py`, output `results/final/main_table.csv`

Gemma-3-12B finished last. Its rate-limited calls were retried one at a
time until only 1 of 19,200 LLM calls was left without an answer (counted
as "unparsed").

When all rows were in, Gemma looked like the winner on AI-written phishing
(F1 0.955). Before calling it the best model we checked precision per corpus
and found it flags 57 percent of the legitimate Enron mail. So we added a
false alarm column (share of legitimate mail flagged) to the analysis. It
changed how we describe the results:

| Model | Unseen-corpus F1 | False alarms | AI phishing F1 | USD per 1,000 |
|---|---|---|---|---|
| Qwen-2.5-7B, zero-shot | 0.928 | 3% | 0.819 | 0.031 |
| Gemma-3-12B | 0.882 | 25% | 0.955 | 0.016 |
| TF-IDF + LogReg | 0.901 | 9% | 0.640 | free |
| DistilBERT | 0.891 | 6% | 0.493 | free |

- Qwen zero-shot is our recommendation: robust, few false alarms, cheap.
- Gemma catches the most AI phishing but flags a quarter of normal mail. It
  fits a "send to review" role, not automatic blocking. Our July preliminary
  run had already seen Gemma calling almost everything phishing.
- DistilBERT has the best in-corpus F1 of any model (0.975) and the weakest
  AI-phishing F1 of the trained models. The usual way of measuring would have
  picked it.
- In the Kaggle fold only 4,075 of 5,000 DistilBERT training emails survived
  decontamination, another sign of how much Kaggle copies the others.

Total API spend: 0.52 dollars of the 2 dollar cap.

## Step 13. Writing it up

- Paper: `paper/main.pdf`, IEEE two-column, 6 pages. Tables are generated
  from the result CSVs (`paper/make_tables.py`) and every number in the text
  is filled in by `paper/fill_numbers.py`, so the paper cannot drift from the
  data. Build with `tectonic main.tex`.
- Final slides: `final-slides/final_deck.html` (present in a browser, press N
  for notes) and `final-slides/final_deck.pptx`. Both are generated from
  `final-slides/numbers.json`. Speaker script in English and Bangla:
  `final-slides/speaker_script.md`.
- Notebook: `notebooks/phishing_llm_cross_corpus.ipynb`, opens in Colab,
  loads every result in seconds or reruns all six steps.

## Step 14. Publishing

Repository: https://github.com/Jahid15/phishing-llm-cross-corpus (public).
The `.env` file with the OpenRouter key and the `data/` folder are in
`.gitignore`, and we scanned every committed file for the key before each
push.

## What is left (next two weeks)

1. Phishsense-1B: get a HuggingFace token and run it on the same 2,400 emails.
2. Relabel a sample into phishing versus spam and rerun, to close the label gap.
3. 1,000 emails per test set for the top three models (under 0.50 dollars).
4. The Italian and German part of E-PhishLLM, and a stronger DistilBERT run.

## How to pick this up

Read this log, then `README.md` for commands. Every result in the paper and
slides can be rebuilt with `python code/final/06_analysis.py`, then
`paper/make_tables.py`, `paper/fill_numbers.py`, `final-slides/collect_numbers.py`,
`final-slides/build_deck.py` and `node final-slides/build_pptx.js`, without
calling any API again.

---

# Round 2: completing the study (20 to 21 September 2026)

After the first version was published we went back over the work with three
questions: what does the 2025 and 2026 literature already do, what is wrong
with our own method, and what is still missing from the proposal. We used three
independent reviewers (separate agents with no knowledge of each other's
findings) for the literature, the methodology and the available models and
corpora, then worked through what they found.

## Step 17. What the literature already does, and what is left for us

Two papers turned out to do a large part of what we had claimed as new.
E-PhishGen (AISec 2025) already evaluates classical models, DistilBERT and
several LLMs with a leave-one-dataset-out protocol over eight corpora. Bhuiyan
and Bhuiyan (Big Data and Cognitive Computing, 2026) already study cross-corpus
fragility and artifact learning over six corpora.

We narrowed the claim rather than defending a wrong one. What neither of them
does, and what we keep: measuring the near-duplicate overlap between the
corpora and removing it before testing, a control that shows the drop is not
just a smaller training set, the cost in dollars, the false alarm rate on
legitimate mail, and the operating-point analysis. The related work section now
cites both papers prominently and says exactly this.

## Step 18. What was wrong with our own method

The methodology review found five things that mattered. All are now fixed.

1. In-corpus F1 was measured differently for different model families (an 80/20
   split at natural class balance for the classical models, the balanced
   evaluation subset for DistilBERT), and we had compared them anyway. Both are
   now measured the same way, on the shared evaluation subset, and the old
   80/20 number is kept separately for the leakage table.
2. The leakage claim was confounded with training-set size, because
   decontamination also removes data. We added a control that removes the same
   number of training emails at random. It changes the score by at most 0.004
   while decontamination changes it by 0.057 on average, so the cause is which
   emails are removed, not how many. This is now the strongest single piece of
   evidence in the paper.
3. Near duplicates inside a corpus were never measured. They are now: 9 to 19
   percent of each corpus's own evaluation emails have a near copy in the part
   of the corpus a model trains on, which makes ordinary in-corpus scores
   optimistic before any cross-corpus question is asked.
4. The bootstrap intervals were not paired across models and used a shared
   random generator, so they were not reproducible and could not support
   comparisons. They are now paired on identical resample positions, we report
   the interval of the difference for the comparisons we make, and we added a
   leave-one-corpus-out jackknife, which is the honest interval for "a corpus
   we have never seen".
5. Near-duplicate decisions used the MinHash estimate, which has a standard
   error of about 0.035 at our threshold. Every candidate pair is now verified
   with the exact Jaccard similarity, and the matcher itself is validated
   against brute force in a committed script (precision 1.00, recall 1.00 on
   400 hard cases). The numbers went up slightly rather than down.

## Step 19. A parsing bug that would have produced a fake result

The first frontier run (Gemini-3.1-Flash-Lite) came back with 2,399 of 2,400
answers unparsed. The model had answered "ph" or "leg": the provider cuts the
reply to one token, and our parser looked for the whole words. Left alone, the
model would have appeared to call every email legitimate.

Because we save the raw text of every answer, the fix cost nothing: we improved
the parser to accept a prefix (and to read negations such as "not phishing"
correctly) and re-read the stored answers with `11_reparse.py`. 2,399
predictions were corrected and no other model's results changed. Saving raw
answers is the practice that made this recoverable.

## Step 20. New experiments

| What | Why | Result |
|---|---|---|
| Frontier reference (Gemini-3.1-Flash-Lite, GPT-4o-mini) | how far are cheap models from a current paid model | Gemini is ahead of every open model on every axis we measure |
| Published phishing detectors (BERT, ModernBERT, Phishsense-1B through an ungated mirror) | their model cards name the corpora we test on, so contamination should be visible in released artefacts | see the results table |
| Few-shot source ablation (old corpora, AI-written, mixed) | test our claim that the examples, not few-shot itself, cause the drop on AI mail | swapping in AI-written examples recovers most of the AI-phishing score |
| Italian and German E-PhishLLM | our English-only limitation becomes a measurement | scores drop, an English prompt does not transfer for free |
| Placeholder study and sanitised copies | the corpus writes links as `<<link>>`, only in phishing mail | worth about 18 points of recall on average; Gemma is almost unaffected |
| Spam versus phishing annotation with two annotators | gap 4 from the proposal | only 15 to 25 percent of the positives are phishing |
| Base-rate analysis | balanced test sets are not a mailbox | at 5 percent phishing the ranking changes and false alarms dominate |
| Two-stage detectors from saved predictions | what an organisation would actually build | TF-IDF in front of an LLM halves the cost and lowers false alarms |
| Explanation quality with an LLM judge | objective 5 of the proposal | reasons are grounded about 9 times in 10 when the verdict is right, about half the time when it is wrong |
| McNemar tests | are the differences real | Qwen beats the classical models and DistilBERT; few-shot gains on old corpora are not significant, its AI-phishing loss is |

## Step 21. Things we tried and dropped

- Phi-4 with a larger output budget was first discarded because a quick reading
  suggested the model refuses. The methodology review showed the discarded file
  contradicted that, so it was rerun properly and is reported.
- The first rewrite of the overlap script held every email's shingle set in
  memory at once, which would have needed roughly 20 GB. It now builds
  signatures one email at a time and recomputes only candidate pairs.
- Running DistilBERT on the Apple GPU: it needed more than 3 GB of GPU memory
  and competed with the other jobs, so the final runs use the CPU at 128 tokens.

## Step 22. Bugs found while finishing, and what they teach

Four bugs surfaced in the last stretch. All are fixed, and all are the kind
that would have produced a wrong number in a paper rather than a crash.

1. **The Gemini parser.** Covered in step 19: 2,399 valid answers were being
   read as "legitimate" because the provider truncated the reply to one token.
   Saving raw answers made it free to fix.
2. **A published model that speaks a different language.** Phishsense-1B
   answers TRUE or FALSE, as its documentation says, not "phishing" or
   "legitimate". Our parser scored all of its answers as negative, which made
   it look like a model that never flags anything (exactly 0.500 accuracy on a
   balanced set). Once the parser accepted TRUE and FALSE its scores became
   0.96 on SpamAssassin and 0.84 on AI-written phishing. A score of exactly
   0.500 on a balanced set is always worth investigating.
3. **A resume key that was not unique.** Our sanitised copies of the
   AI-written test set reuse the ids of the original emails, and the LLM cache
   was keyed on the id alone, so those sets were skipped as "already done" and
   silently produced no rows. The key is now the pair (test set, id).
4. **A crash that idled the machine for hours.** A variable introduced during
   the rewrite of the DistilBERT script was defined in one branch and used in
   another, so the last fold failed at two in the morning and the queue behind
   it did nothing until we looked. The lesson for the next long run: have the
   runner print a heartbeat, and check on a long job rather than assuming it is
   still working.

## Step 23. Fairness checks on the published detectors

Two of the three released detectors score near the top of our table on the
legacy corpora and fail on AI-written phishing (F1 0.47 and 0.15). Before
reporting that we checked two alternative explanations.

- *Is it the decision threshold?* The ModernBERT card recommends 0.37 rather
  than the default. We reran it at 0.5, 0.37 and 0.2. Recall on AI-written
  phishing goes from 0.09 to 0.11 to 0.22 while the false alarm rate on the
  same set goes from 8 to 33 percent. Lowering the threshold moves the failure,
  it does not remove it.
- *Is it a property of released models in general?* No. Phishsense-1B, which is
  a LoRA-tuned causal model rather than an encoder classifier, reaches 0.84 on
  the same AI-written set. We say so in the paper.

## Step 24. Final numbers

Everything in the paper, the slides and the team guide is generated from
`results/final/` by scripts, so the three documents cannot disagree. The
headline results after all the corrections:

- Near duplicates: 87 percent of SpamAssassin, 91 percent of Ling-Spam and 36
  percent of Enron sit inside the Kaggle set; an exact check finds 2 of the
  SpamAssassin copies. Stable at Jaccard 0.9 and at 5,000 characters, and the
  matcher matches brute force exactly on 400 hard cases.
- Leakage: removing the duplicates costs up to 12 F1 points in
  leave-one-corpus-out; removing the same number of emails at random costs at
  most 0.4 points.
- Labels: 15 to 25 percent of the positive emails are phishing, the rest spam.
- Models: Gemini-3.1-Flash-Lite 0.959 unseen F1 at 1.7 percent false alarms,
  zero-shot Qwen-2.5-7B 0.928 at 3.0 percent for about 3 cents per 1,000
  emails, TF-IDF 0.899 at 9.6 percent for nothing.
- Published detectors: BERT-phishing tops the unseen-corpus column at 0.962 and
  scores 0.470 on AI-written phishing; ModernBERT 0.892 and 0.149;
  Phishsense-1B 0.947 and 0.839.
- Operating points: at a 5 percent phishing rate the ranking changes, and a
  TF-IDF filter in front of Qwen gives F1 0.911 at 1.1 percent false alarms for
  0.016 dollars per 1,000 emails.
- Total API spend for the whole project: under 2 dollars.

## Step 25. A finding we had to withdraw

Earlier in this round we reported that the `<<link>>` placeholder in the
AI-written corpus was worth about 18 points of recall, and we put it in the
slides as a caution about synthetic benchmarks. When the sanitised copies of
the test set were finally evaluated by all the models, the picture changed.

- Split comparison (emails that carry the token against emails that do not):
  a gap of about 16 points.
- Paired comparison (the same emails, with the token removed): a gap of
  0.9 points, and at most 2 points for any single model.

The first comparison is confounded. Emails that contain a link placeholder are
link-based lures; the ones without are business email compromise and similar
text-only attacks, which are harder for every detector. So the token is not
what the models were reacting to, and our AI-phishing numbers stand.

We kept both results in the paper. The quick test pointed the wrong way, and a
reader who ran only that test would have drawn the opposite conclusion. The
rule we take from it: when you suspect a shortcut, change that one thing on the
same data rather than comparing two groups that differ in other ways.
