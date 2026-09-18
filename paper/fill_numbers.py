"""Fills the numbers in sec_results.tex and writes abstract.tex, all from results/final."""
import json
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "results", "final")
m = pd.read_csv(os.path.join(R, "main_table.csv")).set_index("model")
cost = pd.read_csv(os.path.join(R, "llm_cost.csv")).set_index("model")
num = json.load(open(os.path.join(HERE, "..", "final-slides", "numbers.json")))

def g(model, col):
    return float(m.loc[model, col])

f = lambda x: f"{x:.3f}"
zero = cost[~cost.index.str.contains("few-shot")]
rep = {
    "QWEN_UNSEEN": f(g("Qwen-2.5-7B", "unseen_f1_mean")),
    "QWENFS_UNSEEN": f(g("Qwen-2.5-7B few-shot", "unseen_f1_mean")),
    "LR_UNSEEN": f(g("TF-IDF + LogReg", "unseen_f1_mean")),
    "L3_UNSEEN": f(g("Llama-3.2-3B", "unseen_f1_mean")),
    "L3FS_UNSEEN": f(g("Llama-3.2-3B few-shot", "unseen_f1_mean")),
    "PHI_UNSEEN": f(g("Phi-4-14B", "unseen_f1_mean")),
    "L1_UNSEEN": f(g("Llama-3.2-1B", "unseen_f1_mean")),
    "L1_WORST": f(g("Llama-3.2-1B", "unseen_f1_worst")),
    "LR_AI": f(g("TF-IDF + LogReg", "ai_phishing_f1")),
    "NB_AI": f(g("TF-IDF + NB", "ai_phishing_f1")),
    "QWEN_AI": f(g("Qwen-2.5-7B", "ai_phishing_f1")),
    "QWENFS_AI": f(g("Qwen-2.5-7B few-shot", "ai_phishing_f1")),
    "L3_AI": f(g("Llama-3.2-3B", "ai_phishing_f1")),
    "L3FS_AI": f(g("Llama-3.2-3B few-shot", "ai_phishing_f1")),
    "L8_AI": f(g("Llama-3.1-8B", "ai_phishing_f1")),
    "LLM_MIN_COST": f"{zero.usd_per_1000.min():.3f}",
    "LLM_MAX_COST": f"{zero.usd_per_1000.max():.3f}",
    "QWEN_COST": f"{cost.loc['Qwen-2.5-7B', 'usd_per_1000']:.3f}",
    "QWEN_100K": f"{cost.loc['Qwen-2.5-7B', 'usd_per_1000'] * 100:.2f}",
    "TOTAL_CALLS": f"{num['llm_calls'] + 300:,}".replace(",", "{,}"),
    "TOTAL_USD": f"{num['llm_total_usd'] + num['discarded_usd']:.2f}",
    "DB_TRAIN": f"{num.get('distilbert_train_min_per_fold', 0):.0f}",
    "DB_INFER": f"{num.get('distilbert_infer_sec_per_1000', 0):.0f}",
}
tim = pd.read_csv(os.path.join(R, "distilbert_timing.csv"))
pc = pd.read_csv(os.path.join(R, "per_source_metrics.csv"))
def rec(model, src):
    return float(pc[(pc.model == model) & (pc.test == src)].recall.iat[0])
pct = lambda x: f"{100 * x:.0f}"
rep.update({
    "QWEN_FA_WORST": pct(g("Qwen-2.5-7B", "false_alarm_worst")),
    "QWEN_FA": pct(g("Qwen-2.5-7B", "false_alarm_rate")),
    "GEMMA_FA_WORST": pct(g("Gemma-3-12B", "false_alarm_worst")),
    "GEMMA_FA": pct(g("Gemma-3-12B", "false_alarm_rate")),
    "GEMMA_AI": f(g("Gemma-3-12B", "ai_phishing_f1")),
    "GEMMA_NAZ": pct(g("Gemma-3-12B", "nazario_recall")) + "\\%",
    "GEMMA_COST": f"{cost.loc['Gemma-3-12B', 'usd_per_1000']:.3f}",
    "L8_FA": pct(g("Llama-3.1-8B", "false_alarm_rate")),
    "L1_FA": pct(g("Llama-3.2-1B", "false_alarm_rate")),
    "QWEN_AI_REC": f"{rec('Qwen-2.5-7B', 'ephishllm'):.2f}",
})
rep["DB_KAGGLE_N"] = f"{int(tim[(tim.setting == 'loco_clean') & (tim.test == 'kaggle')].train_size.iat[0]):,}".replace(",", "{,}")
rep["DB_INC"] = f(g("DistilBERT", "in_corpus_f1"))
rep["DB_AI"] = f(g("DistilBERT", "ai_phishing_f1"))
if "DistilBERT" in m.index:
    rep["DISTILBERT_SENTENCE"] = (f"the fine-tuned DistilBERT ({f(g('DistilBERT', 'unseen_f1_mean'))}), although")
    rep["DISTILBERT_AI"] = f" and {f(g('DistilBERT', 'ai_phishing_f1'))} (DistilBERT)"
else:
    rep["DISTILBERT_SENTENCE"] = "although"
    rep["DISTILBERT_AI"] = ""
if "Gemma-3-12B" in m.index:
    rep["GEMMA_SENTENCE"] = (f"Gemma-3-12B reaches {f(g('Gemma-3-12B', 'unseen_f1_mean'))} on unseen corpora "
                             f"and {f(g('Gemma-3-12B', 'ai_phishing_f1'))} on AI phishing, "
                             f"at {cost.loc['Gemma-3-12B', 'usd_per_1000']:.3f} dollars per 1{{,}}000 emails.")
else:
    rep["GEMMA_SENTENCE"] = ""

s = open(os.path.join(HERE, "sec_results.tex")).read()
for k in sorted(rep, key=len, reverse=True):
    s = s.replace(k, rep[k])
left = [w for w in s.split() if w.isupper() and "_" in w]
assert not left, left
open(os.path.join(HERE, "sec_results_filled.tex"), "w").write(s)

sa = num["sa_in_kaggle"]
abstract = f"""Published phishing email detectors, from GPT-4 prompts to fine-tuned
transformers, report 97 to 99\\% accuracy. Almost all of these numbers come from
training and testing inside one dataset. We ask how good cheap detectors are
when the test mail comes from a corpus the model has never seen, and when
emails shared between corpora are removed first. Comparing nine public email
sources, we find that the widely used Kaggle phishing set contains
{sa['near'][1]:.0f}\\% of SpamAssassin, {num['ling_in_kaggle_near'][1]:.0f}\\% of Ling-Spam and
{num['enron_in_kaggle_near'][1]:.0f}\\% of Enron as near duplicates, while an exact-match check
finds only {sa['exact_raw'][0]} of the SpamAssassin copies. Removing the copies lowers the
F1 of a TF-IDF model transferred from Kaggle to SpamAssassin from
{num['kaggle_to_sa']['raw']:.3f} to {num['kaggle_to_sa']['clean']:.3f}, and lowers
leave-one-corpus-out F1 by up to 11.5 points. We then compare classical models,
DistilBERT and six small open LLMs (1B to 14B parameters) on the same held-out
emails, including AI-written phishing, next to the measured API cost.
Zero-shot Qwen-2.5-7B gives the best balance, with a mean F1 of
{rep['QWEN_UNSEEN']} on unseen corpora, {rep['QWEN_FA']}\\% false alarms and {rep['QWEN_AI']} F1 on
AI-written phishing, for {float(rep['QWEN_COST'])*100:.0f} US cents per 1{{,}}000 emails.
Gemma-3-12B catches more AI-written phishing (F1 {rep['GEMMA_AI']}) but flags
{rep['GEMMA_FA']}\\% of legitimate mail. The fine-tuned DistilBERT has the best
in-corpus score of all models and the weakest AI-phishing score of the trained
ones, and few-shot examples taken from old corpora raise scores on old mail
but lower them on AI-written phishing. The
whole study ran on one laptop for {rep['TOTAL_USD']} US dollars of API fees."""
open(os.path.join(HERE, "abstract.tex"), "w").write(abstract)
print("filled", len(rep), "numbers")
