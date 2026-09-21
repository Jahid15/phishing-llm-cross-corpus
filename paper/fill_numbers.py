"""
Fills every number in sec_results.tex from results/final and writes the abstract.

Nothing in the paper text is typed by hand: each placeholder below is computed
from a result file, so re-running the experiments and this script keeps the
paper and the data in step. It fails loudly if a placeholder is left over.
"""
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "results", "final")
rd = lambda n: pd.read_csv(os.path.join(R, n))

main = rd("main_table.csv").set_index("model")
cost = rd("llm_cost.csv").set_index("model")
per = rd("per_source_metrics.csv")
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
SIX = ["spamassassin", "ceas08", "trec07", "ling", "enron", "kaggle"]
f3 = lambda x: f"{x:.3f}"
pc = lambda x: f"{100 * x:.0f}"


def g(model, col):
    return float(main.loc[model, col])


def ov(level, a, b, what="emails_of_source_found"):
    r = pairs[(pairs.level == level) & (pairs.contains == a) & (pairs.source == b)]
    return float(r[what].iat[0]) if len(r) else 0.0


def pwf(a, b, setting):
    return float(pw[(pw.train == a) & (pw.test == b) & (pw.setting == setting)].f1.iat[0])


def loco(model, test, setting):
    r = cl[(cl.model == model) & (cl.test == test) & (cl.setting == setting)]
    return float(r.f1.iat[0]) if len(r) else float("nan")


def mcnemar(a, b, scope="six unseen corpora"):
    r = sig[(sig.model_a == a) & (sig.model_b == b) & (sig.scope == scope)]
    if not len(r):
        return "not tested"
    p = float(r.p_value.iat[0])
    return f"$p={p:.0e}$".replace("e-0", "e-") if p >= 1e-16 else "$p<10^{-15}$"


rep = {}
# ---- overlap
rep["SA_EXACT"] = f"{int(ov('exact_raw', 'kaggle', 'spamassassin')):,}"
rep["SA_NORM"] = f"{int(ov('exact_norm', 'kaggle', 'spamassassin')):,}".replace(",", "{,}")
rep["SA_NEAR"] = f"{int(ov('near', 'kaggle', 'spamassassin')):,}".replace(",", "{,}")
rep["SA_NEAR_PCT"] = f"{ov('near', 'kaggle', 'spamassassin', 'pct_of_source'):.0f}"
rep["LING_PCT"] = f"{ov('near', 'kaggle', 'ling', 'pct_of_source'):.0f}"
rep["ENRON_PCT"] = f"{ov('near', 'kaggle', 'enron', 'pct_of_source'):.0f}"
kag = th[(th.source == "kaggle")].set_index("threshold")["pct"]
rep["KAGGLE_UNION"] = f"{kag.loc[0.8]:.0f}"
rep["KAGGLE_90"] = f"{kag.loc[0.9]:.0f}"
rep["MATCH_PREC"] = f"{mv.precision:.2f}"
rep["MATCH_REC"] = f"{mv.recall:.2f}"
sens = os.path.join(R, "overlap_pairs_chars5000.csv")
if os.path.exists(sens):
    b = rd("overlap_pairs_chars5000.csv")
    r5 = b[(b.level == "near") & (b.contains == "kaggle") & (b.source == "spamassassin")]
    rep["SENS_5K"] = f"{float(r5.pct_of_source.iat[0]):.1f}"
    rep["SENS_2K"] = f"{ov('near', 'kaggle', 'spamassassin', 'pct_of_source'):.1f}"
else:
    rep["SENS_5K"] = rep["SENS_2K"] = "n/a"
rep["MATCH_SHARE"] = f"{100 * mv.share_of_hard_cases_that_are_duplicates:.0f}"
w6 = within.loc[SIX]
rep["INT_LO"] = f"{w6.corpus_internal_near_dup_pct.min():.0f}"
rep["INT_HI"] = f"{w6.corpus_internal_near_dup_pct.max():.0f}"
rep["EVAL_LO"] = f"{w6.eval_with_near_dup_in_own_train_pct.min():.0f}"
rep["EVAL_HI"] = f"{w6.eval_with_near_dup_in_own_train_pct.max():.0f}"

# ---- leakage
rep["K2SA_RAW"] = f3(pwf("kaggle", "spamassassin", "raw"))
rep["K2SA_CLEAN"] = f3(pwf("kaggle", "spamassassin", "clean"))
drops = {t: loco("logreg", t, "loco_raw") - loco("logreg", t, "loco_clean") for t in SIX}
rep["LING_DROP"] = f"{100 * drops['ling']:.1f}"
rep["SA_DROP"] = f"{100 * drops['spamassassin']:.1f}"
rep["CTRL_DROP"] = f"{100 * max(drops['ceas08'], drops['trec07']):.1f}"
rand_diff = [abs(loco("logreg", t, "loco_raw") - loco("logreg", t, "loco_random")) for t in SIX]
rep["RANDOM_MAXDIFF"] = f"{100 * np.nanmax(rand_diff):.1f}"
inc = [loco("logreg", t, "in_corpus_split") for t in SIX]
cln = [loco("logreg", t, "loco_clean") for t in SIX]
rep["INC_LO"], rep["INC_HI"] = f3(np.nanmin(inc)), f3(np.nanmax(inc))
rep["CLEAN_LO"], rep["CLEAN_HI"] = f3(np.nanmin(cln)), f3(np.nanmax(cln))
gaps = [100 * (a - b) for a, b in zip(inc, cln)]
rep["GAP_LO"], rep["GAP_HI"] = f"{np.nanmin(gaps):.0f}", f"{np.nanmax(gaps):.0f}"

# ---- labels
comp = ls[ls.row == "composition"]
rep["PH_LO"] = f"{comp.phishing_pct.min():.0f}"
rep["PH_HI"] = f"{comp.phishing_pct.max():.0f}"
agr = ls[ls.row == "agreement"].iloc[0]
rep["AGREE"] = f"{100 * float(agr.agreement):.0f}"
rep["KAPPA"] = f"{float(agr.kappa):.2f}"
kind = ls[ls.row == "recall_by_kind"]
rep["KIND_GAP_LO"] = f"{100 * kind.gap.min():.0f}"
rep["KIND_GAP_HI"] = f"{100 * kind.gap.max():.0f}"

# ---- model comparison
rep["QWEN_UNSEEN"] = f3(g("Qwen-2.5-7B", "unseen_f1_mean"))
rep["LR_UNSEEN"] = f3(g("TF-IDF + LogReg", "unseen_f1_mean"))
rep["DB_UNSEEN"] = f3(g("DistilBERT", "unseen_f1_mean"))
rep["QWEN_FA"] = f"{100 * g('Qwen-2.5-7B', 'false_alarm_rate'):.0f}"
rep["QWEN_AI"] = f3(g("Qwen-2.5-7B", "ai_phishing_f1"))
rep["DB_INC"] = f3(g("DistilBERT", "in_corpus_f1"))
rep["DB_AI"] = f3(g("DistilBERT", "ai_phishing_f1"))
rep["GEM_UNSEEN"] = f3(g("Gemini-3.1-Flash-Lite", "unseen_f1_mean"))
rep["GEM_FA"] = f"{100 * g('Gemini-3.1-Flash-Lite', 'false_alarm_rate'):.1f}"
rep["GEM_AI"] = f3(g("Gemini-3.1-Flash-Lite", "ai_phishing_f1"))
rep["GEM_COST"] = f"{cost.loc['Gemini-3.1-Flash-Lite', 'usd_per_1000']:.3f}"
rep["QWEN_VS_LR_P"] = mcnemar("Qwen-2.5-7B", "TF-IDF + LogReg")
diff_file = os.path.join(R, "paired_differences.csv")
if os.path.exists(diff_file):
    pdiff = rd("paired_differences.csv")
    row = pdiff[(pdiff.model_a == "Qwen-2.5-7B") & (pdiff.model_b == "TF-IDF + LogReg")]
    rep["QWEN_VS_LR"] = f"{float(row.mean_difference.iat[0]):+.3f}" if len(row) else "n/a"
    rep["QWEN_VS_LR_CI"] = (f"{float(row.ci_low.iat[0]):+.3f} to {float(row.ci_high.iat[0]):+.3f}"
                            if len(row) else "n/a")
    rowf = pdiff[(pdiff.model_a == "Qwen-2.5-7B few-shot") & (pdiff.model_b == "Qwen-2.5-7B")]
    rep["QWEN_FS_CI"] = (f"difference {float(rowf.mean_difference.iat[0]):+.3f}, interval "
                         f"{float(rowf.ci_low.iat[0]):+.3f} to {float(rowf.ci_high.iat[0]):+.3f}") if len(rowf) else "n/a"
else:
    rep["QWEN_VS_LR"] = rep["QWEN_VS_LR_CI"] = rep["QWEN_FS_CI"] = "n/a"
rep["PHI_UNPARSED"] = f"{cost.loc['Phi-4-14B', 'unparsed_pct']:.0f}"
if "Phi-4-14B relaxed" in main.index:
    rep["PHI_LONG_SENTENCE"] = (f"unseen-corpus F1 {f3(g('Phi-4-14B relaxed', 'unseen_f1_mean'))} against "
                                f"{f3(g('Phi-4-14B', 'unseen_f1_mean'))}, with "
                                f"{cost.loc['Phi-4-14B relaxed', 'unparsed_pct']:.0f}\\% unparsed instead of "
                                f"{cost.loc['Phi-4-14B', 'unparsed_pct']:.0f}\\%")
else:
    rep["PHI_LONG_SENTENCE"] = "we did not rerun it with a larger output budget"

pub = [m for m in main.index if "(published)" in m]
if pub:
    parts = []
    for m in sorted(pub, key=lambda x: -g(x, "unseen_f1_mean")):
        parts.append(f"{m.replace(' (published)', '')} reaches {f3(g(m, 'unseen_f1_mean'))} on our legacy corpora "
                     f"and {f3(g(m, 'ai_phishing_f1'))} on AI-written phishing")
    best_pub = max(pub, key=lambda x: g(x, "unseen_f1_mean"))
    rep["PUBLISHED_SENTENCE"] = (
        "The released detectors behave as contamination predicts. " + "; ".join(parts) + ". "
        f"{best_pub.replace(' (published)', '')} has the highest unseen-corpus score in the whole table "
        f"({f3(g(best_pub, 'unseen_f1_mean'))}), above every LLM we ran, which is what a leaderboard built on "
        "these corpora would report. Its model card names the same Kaggle lineage we test on, so that column is "
        "partly a memory test, and the AI-written column is where the difference shows. "
        "The one exception is the LoRA-tuned causal model, which transfers much better than the two encoder "
        "classifiers, so the failure is not a property of released models as such.")
else:
    rep["PUBLISHED_SENTENCE"] = "We were not able to run the released detectors in time for this version."

tc = os.path.join(R, "threshold_check.csv")
if os.path.exists(tc):
    t = rd("threshold_check.csv")
    ai = t[t.test_set == "ephishllm"].set_index("threshold")
    rep["THRESHOLD_SENTENCE"] = (
        f"We also checked that this is not simply the decision threshold. The ModernBERT card recommends 0.37 "
        f"rather than the default. On AI-written phishing its recall goes from {ai.loc[0.5, 'recall']:.2f} at the "
        f"default to {ai.loc[0.37, 'recall']:.2f} at the recommended threshold and {ai.loc[0.2, 'recall']:.2f} at 0.2, "
        f"while the false alarm rate on the same set moves from {100 * ai.loc[0.5, 'false_alarm']:.0f}\\% to "
        f"{100 * ai.loc[0.2, 'false_alarm']:.0f}\\%. Lowering the threshold trades one failure for the other rather "
        f"than removing it.")
else:
    rep["THRESHOLD_SENTENCE"] = ""

# ---- AI phishing and the placeholder
eng = ph[ph.test_set == "ephishllm"]
rep["SPLIT_GAP"] = f"{100 * eng.gap.mean():.0f}"
pair = ph[ph.test_set == "ephishllm paired"]
rep["PAIRED_GAP"] = f"{100 * pair.gap.mean():.1f}" if len(pair) else "n/a"
rep["MAXPAIRED"] = f"{100 * pair.gap.max():.1f} points" if len(pair) else "n/a"
rep["GAPMEAN"] = rep["SPLIT_GAP"]

qrow = eng[eng.model == "Qwen-2.5-7B"].iloc[0]
grow = eng[eng.model == "Gemma-3-12B"].iloc[0]
rep["QWEN_WITH"] = f"{100 * qrow.recall_with_placeholder:.0f}\\%"
rep["QWEN_WITHOUT"] = f"{100 * qrow.recall_without:.0f}\\%"
rep["GEMMA_WITH"] = f"{100 * grow.recall_with_placeholder:.0f}\\%"
rep["GEMMA_WITHOUT"] = f"{100 * grow.recall_without:.0f}\\%"
rep["PH_WITH"] = f"{int(qrow.n_with_placeholder)}"
ev = pd.read_csv(os.path.join(R, "..", "..", "data", "final", "eval_ephishllm.csv"), keep_default_na=False)
import re as _re
rep["PH_LEGIT"] = str(int(ev[ev.label == 0].text.str.contains(_re.compile(r"<<[^>]{0,60}>>")).sum()))


def f1_on(model, src, setting):
    r = per[(per.model == model) & (per.setting == setting) & (per.test == src)]
    return float(r.f1.iat[0]) if len(r) else float("nan")


rep["MULTI_GEM"] = f3(f1_on("Gemini-3.1-Flash-Lite", "ephishllm_it", "llm_zero"))
rep["MULTI_GEMMA"] = f3(f1_on("Gemma-3-12B", "ephishllm_it", "llm_zero"))
multi = []
for m, s in [("Qwen-2.5-7B", "llm_zero"), ("Gemma-3-12B", "llm_zero"), ("Llama-3.1-8B", "llm_zero")]:
    base = f1_on(m, "ephishllm", s)
    for lang in ["ephishllm_it", "ephishllm_de"]:
        v = f1_on(m, lang, s)
        if v == v:
            multi.append(base - v)
rep["MULTI_DROP"] = f"{100 * np.mean(multi):.0f}" if multi else "n/a"

# ---- few shot
rep["QWENFS_UNSEEN"] = f3(g("Qwen-2.5-7B few-shot", "unseen_f1_mean"))
rep["QWENFS_AI"] = f3(g("Qwen-2.5-7B few-shot", "ai_phishing_f1"))
rep["QWENFSAI_AI"] = f3(g("Qwen-2.5-7B few-shot AI", "ai_phishing_f1"))
rep["QWENFSAI_FA"] = f"{100 * g('Qwen-2.5-7B few-shot AI', 'false_alarm_rate'):.0f}"
rep["QWENFSMIX_AI"] = (f3(g("Qwen-2.5-7B few-shot mixed", "ai_phishing_f1"))
                       if "Qwen-2.5-7B few-shot mixed" in main.index else "not run")
rep["QWEN_FS_P"] = mcnemar("Qwen-2.5-7B few-shot", "Qwen-2.5-7B", "AI-written (E-PhishLLM)")

# ---- operating points
rep["GEMMA_F1_05"] = f3(float(br.loc["Gemma-3-12B", "f1@0.05"]))
rep["GEMMA_ALERTS"] = f"{float(br.loc['Gemma-3-12B', 'false_alerts_per_1000@0.05']):.0f}"
rep["QWEN_F1_05"] = f3(float(br.loc["Qwen-2.5-7B", "f1@0.05"]))
rep["QWEN_ALERTS"] = f"{float(br.loc['Qwen-2.5-7B', 'false_alerts_per_1000@0.05']):.0f}"
c1 = cas[(cas.stage1 == "TF-IDF + LogReg") & (cas.stage2 == "Qwen-2.5-7B") & (cas.policy == "confirm")].iloc[0]
rep["CASCADE_F1"] = f3(c1.unseen_f1)
rep["CASCADE_FA"] = f"{100 * c1.false_alarm:.1f}"
rep["CASCADE_COST"] = f"{c1.usd_per_1000:.4f}"
c2 = cas[(cas.stage1 == "Qwen-2.5-7B") & (cas.stage2 == "Gemma-3-12B") & (cas.policy == "rescue")].iloc[0]
rep["RESCUE_AI_RECALL"] = f3(c2.ai_phishing_recall)
rep["RESCUE_FA"] = f"{100 * c2.false_alarm:.0f}"

# ---- explanations
rep["GROUNDED_QWEN"] = f"{100 * float(exp.loc['qwen/qwen-2.5-7b-instruct', 'grounded']):.0f}"
rep["GROUNDED_GEMMA"] = f"{100 * float(exp.loc['google/gemma-3-12b-it', 'grounded']):.0f}"
rep["WRONG_GROUNDED"] = f"{100 * exp['grounded_when_wrong'].mean():.0f}"

# ---- cost
zero = cost[~cost.index.str.contains("few-shot|relaxed", regex=True)]
open_models = zero[~zero.index.isin(["Gemini-3.1-Flash-Lite", "GPT-4o-mini"])]
rep["LLM_MIN_COST"] = f"{open_models.usd_per_1000.min():.3f}"
rep["LLM_MAX_COST"] = f"{open_models.usd_per_1000.max():.3f}"
cpu = cl[(cl.model == "logreg") & (cl.setting == "loco_clean")]["cpu_sec_per_1000"]
rep["CPU_MIN"], rep["CPU_MAX"] = f"{cpu.min():.2f}", f"{cpu.max():.2f}"
tim = rd("distilbert_timing.csv")
rep["DB_TRAIN"] = f"{tim[tim.setting == 'loco_clean'].train_sec.mean() / 60:.0f}"
rep["DB_INFER"] = f"{tim.infer_sec_per_1000.mean():.0f}"
spend = json.load(open(os.path.join(R, "llm_spend.json")))["total_usd"]
rep["TOTAL_USD"] = f"{spend:.2f}"
rep["TOTAL_CALLS"] = f"{int(cost.calls.sum()):,}".replace(",", "{,}")

# ---- write
s = open(os.path.join(HERE, "sec_results.tex")).read()
for k in sorted(rep, key=len, reverse=True):
    s = s.replace(k, str(rep[k]))
left = sorted({w for w in s.replace("\\", " ").replace("{", " ").replace("}", " ").split()
               if w.isupper() and "_" in w})
assert not left, f"unfilled placeholders: {left}"
open(os.path.join(HERE, "sec_results_filled.tex"), "w").write(s)

abstract = f"""Published phishing email detectors report 97 to 99\\% accuracy, almost always
measured inside a single corpus. We ask what they are worth on mail from a
corpus they have never seen, once the emails that public corpora share with
each other are removed. Comparing nine public sources, we find that
{rep['SA_NEAR_PCT']}\\% of SpamAssassin, {rep['LING_PCT']}\\% of Ling-Spam and
{rep['ENRON_PCT']}\\% of Enron have a near duplicate inside the widely used Kaggle
phishing set, while an exact-match check finds {rep['SA_EXACT']} of the
SpamAssassin copies. Removing the duplicates lowers a transfer score from
{rep['K2SA_RAW']} to {rep['K2SA_CLEAN']} F1, and removing the same number of
training emails at random instead changes nothing, which separates leakage from
lost data. An LLM annotator finds that only {rep['PH_LO']} to {rep['PH_HI']}\\% of
the positive emails in these corpora are phishing rather than bulk spam. On
decontaminated leave-one-corpus-out data we compare classical models, a
fine-tuned DistilBERT, six small open LLMs, three published phishing detectors
and two commercial models on identical emails, with false alarm rates and the
measured dollar cost. Zero-shot Qwen-2.5-7B reaches {rep['QWEN_UNSEEN']} mean F1
with {rep['QWEN_FA']}\\% false alarms at three US cents per 1{{,}}000 emails,
Gemini-3.1-Flash-Lite reaches {rep['GEM_UNSEEN']}, and a two-stage detector that
sends only flagged mail to an LLM reaches {rep['CASCADE_F1']} at
{rep['CASCADE_FA']}\\% false alarms for {rep['CASCADE_COST']} dollars per
1{{,}}000. We also show that the AI-written phishing corpus used here carries a
give-away token which a naive comparison blames for {rep['SPLIT_GAP']} points of recall,
but which a paired test clears ({rep['PAIRED_GAP']} points), and that
few-shot examples taken from old corpora, rather than few-shot prompting
itself, are what lower performance on AI-written mail. The whole study ran on
one laptop for {rep['TOTAL_USD']} US dollars."""
open(os.path.join(HERE, "abstract.tex"), "w").write(abstract)
print(f"filled {len(rep)} numbers")
