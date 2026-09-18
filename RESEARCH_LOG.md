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

