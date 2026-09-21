# Completion plan (round 2, 20 September 2026)

Budget: 5 USD total for the project. Spent so far 0.52. Cap for this round: 3.00.
Every step writes its own output files and is skipped if those files exist, so the
work can be stopped and resumed. `python code/final/run_all.py --status` shows where we are.

| # | Step | Why | Output | Cost |
|---|---|---|---|---|
| A | Consistent in-corpus protocol | in-corpus F1 must be measured the same way for every model family (on the shared evaluation subset, trained without those emails) | results/final/classical_loco.csv (setting in_corpus_eval) | free |
| B | Italian and German E-PhishLLM test sets | our English-only limitation becomes a measured result | data/final/eval_ephishllm_it.csv, _de.csv | free |
| C | Rerun overlap with the new sets | keep one coherent decontamination pass | results/final/overlap_* | free |
| D | Rerun classical LOCO | new in-corpus protocol + new test sets | results/final/classical_loco.csv | free |
| E | DistilBERT: raw vs clean on the two most contaminated folds, and the new test sets | show leakage inflation for a neural model, not only TF-IDF | results/final/distilbert_folds/ | free |
| F | Frontier reference model | answers "how far are cheap models from a 2026 frontier model" | results/final/llm_raw/*frontier* | ~0.60 |
| G | Few-shot source ablation (old corpora vs AI-written vs mixed examples) | causal test of our anchoring claim: are old examples the reason few-shot hurts on AI phishing? | results/final/llm_raw/*few_ai*, *few_mix* | ~0.45 |
| H | Multilingual runs (it, de) for the best small models and the frontier model | measured, not assumed | results/final/llm_raw/* | ~0.25 |
| I | Spam versus phishing relabelling of positives by an LLM annotator, with agreement check | closes gap 4 (labels conflated) | results/final/label_study.csv | ~0.35 |
| J | Explanation quality on a sample | proposal objective 5 | results/final/explanations.csv | ~0.30 |
| K | Cascade and ensemble analysis from saved predictions | practical operating points, no new API calls | results/final/cascade.csv | free |
| L | Significance tests (McNemar) between the key model pairs | claims backed by statistics | results/final/significance.csv | free |
| M | Rebuild paper, slides, notebook, guides | deliverables | paper/main.pdf, final-slides/, TEAM_GUIDE.md | free |

Total estimated API cost: about 1.95 USD, hard cap enforced in code at 3.00 for this round.


---

## Status: complete (21 September 2026)

Every step above is done, and review added more. Total API spend 1.58 USD of
the 5 USD budget. `python code/final/run_all.py --status` lists the finished
steps with timestamps.

Added after the three reviews (literature, methodology, models):

| Step | Output |
|---|---|
| Random-removal control for the leakage claim | `results/final/classical_loco.csv`, setting `loco_random` |
| Exact Jaccard verification and a brute-force validation of the matcher | `results/final/matcher_validation_summary.csv` |
| Duplication inside each corpus, and Jaccard and shingle-length sensitivity | `results/final/within_corpus_dup.csv`, `overlap_thresholds.csv`, `*_chars5000.csv` |
| Paired bootstrap and leave-one-corpus-out jackknife, McNemar tests | `main_table.csv`, `paired_differences.csv`, `significance.csv` |
| Spam versus phishing annotation with two annotators | `label_study_summary.csv` |
| Published detectors, including Phishsense through an ungated mirror | `preds/offtheshelf.csv` |
| Frontier reference models | `llm_raw/*gemini*`, `*gpt-4o-mini*` |
| Few-shot example source ablation (legacy, AI-written, mixed) | `llm_raw/*few_ai*`, `*few_mix*` |
| Sanitised and multilingual AI-phishing sets, with a paired token test | `placeholder_effect.csv`, `eval_ephishllm_{nolink,url,it,de}.csv` |
| Base-rate analysis and two-stage detectors | `base_rate.csv`, `cascade.csv` |
| Explanation quality with an LLM judge and a hand-read sample | `explanations_summary.csv`, `explanations_sample.md` |
| Threshold fairness check for the published detector | `threshold_check.csv` |

Rebuild every deliverable from the result files with `./rebuild_all.sh`.
