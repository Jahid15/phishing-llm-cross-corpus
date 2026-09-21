"""Builds phishing_llm_cross_corpus.ipynb from the cells below. Run, then execute with nbconvert."""
import nbformat as nbf

REPO = "https://github.com/Jahid15/phishing-llm-cross-corpus"
nb = nbf.v4.new_notebook()
C = []
md = lambda s: C.append(nbf.v4.new_markdown_cell(s.strip()))
code = lambda s: C.append(nbf.v4.new_code_cell(s.strip()))

md(f"""
# Phishing Email Detection with Small Open LLMs: a Cross-Corpus, Leakage-Aware, Cost-Aware Benchmark

Group 18, Computer Security, United International University
Jahid Ibna Sinha, Md. Jakaria Alam Saimon, Nowshin Anjum Faria

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Jahid15/phishing-llm-cross-corpus/blob/main/notebooks/phishing_llm_cross_corpus.ipynb)

Source code: {REPO}

This notebook walks through the whole experiment. Every table and figure is read
from `results/final/`, which the scripts in `code/final/` produce. By default the
notebook only loads the saved results, so it runs in seconds. Set
`RUN_EXPERIMENTS = True` to run everything again from the raw data.

| Step | Script | What it does |
|---|---|---|
| 1 | `01_prepare_data.py` | download and clean 9 email sources |
| 2 | `02_overlap.py` | find emails shared between corpora (exact and near duplicate) |
| 3 | `03_classical_loco.py` | TF-IDF models, leave-one-corpus-out, raw vs decontaminated |
| 4 | `04_distilbert_loco.py` | fine-tuned DistilBERT, same protocol |
| 5 | `05_llm_eval.py` | six small open LLMs through OpenRouter, measured cost |
| 6 | `06_analysis.py` | final table, confidence intervals, figures |
| 7 | `07_cascade.py` | two-stage detectors built from saved predictions |
| 8 | `08_significance.py` | McNemar tests between model pairs |
| 9 | `09_placeholder.py` | the give-away token in the AI-written corpus |
| 12 | `12_offtheshelf.py` | published phishing detectors, including Phishsense |
| 13 | `13_baserate.py` | precision at a realistic amount of phishing |
| 14 | `14_label_study.py` | spam versus phishing annotation |
| 15 | `15_explanations.py` | explanation quality |
| 16 | `16_validate_matcher.py` | brute-force validation of the matcher |
""")

code("""
import os, sys
IN_COLAB = "google.colab" in sys.modules
if IN_COLAB and not os.path.exists("phishing-llm-cross-corpus"):
    !git clone -q https://github.com/Jahid15/phishing-llm-cross-corpus
    %cd phishing-llm-cross-corpus
    !pip -q install datasketch
elif os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")

RUN_EXPERIMENTS = False   # True = rerun all steps (about 1 to 2 hours, LLM step needs OPENROUTER_API_KEY)

import pandas as pd
from IPython.display import Image, display
pd.set_option("display.width", 200)
R = "results/final/"
""")

md("""
## Step 1. Data

Six corpora that contain both phishing/spam and legitimate mail are used for
training and testing. Three more sets are only ever used for testing:
Nazario (real phishing), Nigerian fraud, and E-PhishLLM (emails written by
GPT-4o-mini, English part). Large corpora are capped at 10,000 emails with a
stratified sample (seed 42). Each set also has a fixed evaluation subset of 300
emails (150 for the one-class sets) that every model is scored on.
""")
code("""
if RUN_EXPERIMENTS:
    !python code/final/01_prepare_data.py
pd.read_csv(R + "dataset_stats.csv")
""")

md("""
## Step 2. How much do the corpora overlap?

Three checks, from strict to loose. `exact_raw` compares the text exactly as a
model reads it. `exact_norm` lowercases and removes all whitespace (our
preliminary method). `near` uses MinHash over 9-character shingles of the
letters and digits only, with Jaccard similarity of at least 0.8.
""")
code("""
if RUN_EXPERIMENTS:
    !python code/final/02_overlap.py
pairs = pd.read_csv(R + "overlap_pairs.csv")
view = pairs[pairs.contains == "kaggle"].pivot_table(index="source", columns="level",
        values="emails_of_source_found", fill_value=0)
view["size"] = pairs[pairs.contains == "kaggle"].groupby("source").source_size.first()
print("Emails of each corpus that also appear inside the Kaggle aggregate:")
view
""")
code("""display(Image(R + "figures/overlap_heatmap.png", width=520))""")

md("""
## Step 3. Classical models, leave-one-corpus-out

For each held-out corpus the model is trained on the other five. `loco_raw`
trains on them as they are. `loco_clean` first drops every training email that
has a near duplicate in the test corpus. The difference is score inflation
caused by leaked emails.
""")
code("""
if RUN_EXPERIMENTS:
    !python code/final/03_classical_loco.py
inf = pd.read_csv(R + "inflation.csv")
inf[["model", "test", "in_corpus", "loco_raw", "loco_clean", "inflation", "removed"]]
""")
code("""display(Image(R + "figures/incorpus_vs_unseen.png", width=520))""")

md("""
## Step 4. DistilBERT

Fine-tuned locally on the laptop CPU, 1,000 emails per training corpus,
one epoch, 128 tokens. Only the decontaminated setting is run.
""")
code("""
if RUN_EXPERIMENTS:
    !python code/final/04_distilbert_loco.py
pd.read_csv(R + "distilbert_timing.csv")
""")

md("""
## Step 5. Small open LLMs

Zero-shot for six models and few-shot (four examples from the other corpora)
for two. Temperature 0, five output tokens, emails cut to 1,500 characters. The
cost is what OpenRouter charged for each call.
""")
code("""
if RUN_EXPERIMENTS:
    !python code/final/05_llm_eval.py --mode zero --models all
pd.read_csv(R + "llm_cost.csv")
""")

md("""
## Step 6. The final table

`unseen_f1_mean` is the mean F1 over the six held-out corpora, with a 95%
bootstrap interval. `unseen_f1_worst` is the lowest of the six.
`ai_phishing_f1` is on E-PhishLLM. The two recall columns are detection rates
on real phishing (Nazario) and fraud (Nigerian). Cost is USD per 1,000 emails
(zero for local models).
""")
code("""
if RUN_EXPERIMENTS:
    !python code/final/06_analysis.py
pd.read_csv(R + "main_table.csv")
""")
code("""
display(Image(R + "figures/per_corpus_f1.png", width=560))
display(Image(R + "figures/f1_vs_cost.png", width=560))
""")
md("""
## Step 7. Is it the duplicates, or just less data?

Decontamination also shrinks the training set. The `loco_random` setting removes
the same number of training emails at random instead, so the two effects can be
told apart.
""")
code("""
cl = pd.read_csv(R + "classical_loco.csv")
lr = cl[cl.model == "logreg"]
six = ["spamassassin", "ceas08", "trec07", "ling", "enron", "kaggle"]
lr.pivot_table(index="test", columns="setting", values="f1").loc[six][
    ["in_corpus_split", "loco_raw", "loco_random", "loco_clean"]].round(3)
""")

md("""
## Step 8. What the corpora actually contain

An LLM annotator sorted every positive evaluation email into phishing or spam,
with a second annotator on 300 of them for agreement.
""")
code("""
ls = pd.read_csv(R + "label_study_summary.csv")
display(ls[ls.row == "composition"][["source", "n_positives", "phishing_pct", "spam_pct"]])
display(ls[ls.row == "agreement"][["n", "agreement", "kappa"]])
""")

md("""
## Step 9. AI-written phishing and the give-away token

E-PhishGen writes phishing links as the literal token `<<link>>`, which appears
only in phishing emails. Recall is compared on phishing emails with and without
it, and the test set is rebuilt with the token removed and replaced.
""")
code("""
pd.read_csv(R + "placeholder_effect.csv").query("test_set == 'ephishllm'")[
    ["model", "recall_with_placeholder", "recall_without", "gap"]]
""")

md("""
## Step 10. Operating points

Balanced test sets are not mailboxes. Precision is recomputed at a 5% phishing
rate, and two-stage detectors are built from predictions we already have.
""")
code("""
display(pd.read_csv(R + "base_rate.csv")[
    ["model", "recall", "false_alarm", "precision@0.05", "f1@0.05", "false_alerts_per_1000@0.05"]].head(8))
display(pd.read_csv(R + "cascade.csv").head(6))
""")

md("""
## Step 11. Are the differences real?

McNemar tests on the paired predictions, and the paired bootstrap difference
for the comparisons the paper makes.
""")
code("""
display(pd.read_csv(R + "significance.csv").head(8))
import os
if os.path.exists(R + "paired_differences.csv"):
    display(pd.read_csv(R + "paired_differences.csv"))
""")

md("""
## What to take away

See `paper/main.pdf` for the discussion, `TEAM_GUIDE.md` for a full explanation
of every decision, and `RESEARCH_LOG.md` for the story of how the project
developed, including the mistakes.
""")

nb["cells"] = C
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, "phishing_llm_cross_corpus.ipynb")
print("notebook written")
