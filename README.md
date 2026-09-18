# Phishing Email Detection with Small Open LLMs

A leakage-aware, cross-corpus and cost-aware benchmark.
Term project, Computer Security, United International University (Group 18).

| ID | Name |
|---|---|
| 011221376 | Jahid Ibna Sinha |
| 011221002 | Md. Jakaria Alam Saimon |
| 011221372 | Nowshin Anjum Faria |

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Jahid15/phishing-llm-cross-corpus/blob/main/notebooks/phishing_llm_cross_corpus.ipynb)

## In one paragraph

Phishing detectors in the literature report 97 to 99 percent accuracy, but
almost always train and test inside one dataset. We tested cheap detectors on
corpora they had never seen, after removing emails that appear in more than
one corpus. The popular Kaggle phishing set turned out to contain 86 percent of
SpamAssassin, 90 percent of Ling-Spam and 35 percent of Enron as near
duplicates, which an exact-match check almost completely misses. Removing
those copies drops a "good" cross-corpus F1 from 0.966 to 0.666. On honest
test data a small open LLM (Qwen-2.5-7B, zero-shot) is the best balance: 0.928
F1 on unseen corpora, 3 percent false alarms and 0.819 F1 on AI-written
phishing, at about 3 US cents per 1,000 emails. Gemma-3-12B catches more
AI-written phishing (0.955) but flags a quarter of legitimate mail, and the
fine-tuned DistilBERT, best of all inside one corpus, is the weakest trained
model on AI-written phishing.

## Where to look

| What | Where |
|---|---|
| The paper (IEEE, two columns) | [`paper/main.pdf`](paper/main.pdf) |
| The whole story, step by step | [`RESEARCH_LOG.md`](RESEARCH_LOG.md) |
| Notebook with every table and figure | [`notebooks/phishing_llm_cross_corpus.ipynb`](notebooks/phishing_llm_cross_corpus.ipynb) |
| Final presentation | [`final-slides/final_deck.html`](final-slides/final_deck.html), [`final-slides/final_deck.pptx`](final-slides/final_deck.pptx) |
| Final code | [`code/final/`](code/final/) |
| Final results (CSV + figures) | [`results/final/`](results/final/) |
| Earlier submissions | literature review, proposal, research gaps (root folder), preliminary code in [`code/preliminary/`](code/preliminary/) |
| Proposal presentation | [`new-slides/`](new-slides/) |

## Run it

Python 3.9 or newer.

```bash
python -m venv .venv && source .venv/bin/activate
pip install pandas scikit-learn requests datasketch scipy matplotlib torch transformers
cd code/final
python 01_prepare_data.py      # downloads 9 sources into data/ (about 450 MB)
python 02_overlap.py           # exact and near-duplicate overlap, about 5 minutes
python 03_classical_loco.py    # TF-IDF models, leave-one-corpus-out, about 45 minutes
python 04_distilbert_loco.py   # DistilBERT on CPU (set DEVICE=mps for Apple GPU), about 45 minutes
python 05_llm_eval.py --mode zero --models all   # needs OPENROUTER_API_KEY
python 05_llm_eval.py --mode few --models meta-llama/llama-3.2-3b-instruct,qwen/qwen-2.5-7b-instruct
python 06_analysis.py          # tables, confidence intervals, figures
```

For the LLM step, put `OPENROUTER_API_KEY=...` in a `.env` file in the project
root or in the environment. The key and the `data/` folder are never
committed. Every LLM answer we got is saved in `results/final/llm_raw/`, so
the analysis can be rerun without spending anything.

Seed 42 everywhere. Total API spend for the whole project was 0.52 US dollars
(19,500 calls, including a discarded trial).

## Repository layout

```
code/preliminary/   July scripts (3 corpora, first cross-corpus and LLM test)
code/final/         six-step final pipeline (01 to 06)
results/preliminary/
results/final/      CSVs, raw LLM answers, figures, logs
notebooks/          Colab notebook
paper/              LaTeX source and PDF, tables are generated from results
final-slides/       final deck (HTML + PPTX), generated from results
new-slides/         proposal deck and speaker scripts
slides/             first proposal deck draft
```
