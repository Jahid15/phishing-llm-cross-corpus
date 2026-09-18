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
## What to take away

See `paper/paper.pdf` for the discussion and `RESEARCH_LOG.md` for the full
story of how the project developed.
""")

nb["cells"] = C
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, "phishing_llm_cross_corpus.ipynb")
print("notebook written")
