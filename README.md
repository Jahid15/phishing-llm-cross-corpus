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

Phishing detectors in the literature report 97 to 99 percent accuracy, almost
always measured inside a single corpus. We asked what they are worth on mail
from a corpus they have never seen, after removing the emails that the public
corpora share with each other. Most of the popular Kaggle phishing set turns
out to have a near duplicate in another public corpus, which an exact-match
check almost completely misses, and removing those copies drops a "good"
cross-corpus F1 from 0.966 to 0.666. Removing the same number of training
emails at random instead changes nothing, so the cause is leakage and not the
smaller training set. We also find that only 15 to 25 percent of the positive
emails in these corpora are phishing rather than bulk spam, and that the
AI-written corpus used as a shift test carries a give-away token worth about 18
points of recall. On honest, decontaminated data we compare classical models, a
fine-tuned DistilBERT, six small open LLMs, three published phishing detectors
and two commercial models on identical emails, with false alarm rates and the
measured dollar cost, and we report what happens at a realistic amount of
phishing and what cheap two-stage detectors achieve.

## Where to look

| What | Where |
|---|---|
| The paper (IEEE, two columns) | [`paper/main.pdf`](paper/main.pdf) |
| The whole story, step by step | [`RESEARCH_LOG.md`](RESEARCH_LOG.md) |
| Notebook with every table and figure | [`notebooks/phishing_llm_cross_corpus.ipynb`](notebooks/phishing_llm_cross_corpus.ipynb) |
| Final presentation | [`final-slides/final_deck.html`](final-slides/final_deck.html), [`final-slides/final_deck.pptx`](final-slides/final_deck.pptx), [`final-slides/group-18.pdf`](final-slides/group-18.pdf) |
| Rehearsal view, slide and script side by side | [`final-slides/PRACTICE.html`](final-slides/PRACTICE.html) |
| Speaker script, English and Bangla | [`final-slides/speaker_script.md`](final-slides/speaker_script.md) |
| The whole study explained in Bangla | [`GUIDE.html`](GUIDE.html) |
| Final code | [`code/final/`](code/final/) |
| Final results (CSV + figures) | [`results/final/`](results/final/) |
| Guide for the team, with a question bank | [`TEAM_GUIDE.md`](TEAM_GUIDE.md) |
| What is done and what is left | [`PLAN.md`](PLAN.md), `python code/final/run_all.py --status` |
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
python 07_cascade.py           # two-stage detectors, from saved predictions
python 08_significance.py      # McNemar tests
python 09_placeholder.py       # the give-away token in the AI-written corpus
python 13_baserate.py          # precision at a realistic amount of phishing
python 14_label_study.py       # spam versus phishing annotation (needs the key)
python 15_explanations.py      # explanation quality (needs the key)
python 16_validate_matcher.py  # brute-force validation of the matcher
DEVICE=mps python 12_offtheshelf.py --models bert,modernbert,phishsense
```

`python code/final/run_all.py` runs the long steps in order and skips whatever
is already finished, so it can be stopped and restarted.

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
