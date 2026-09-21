"""
Step 8. Are the differences between models real, or could they be chance?

We use McNemar's exact test on the paired predictions. Both models judged the
same emails, so for every pair we count the emails where exactly one of them
is right, and test whether that split is even. Small p means the difference is
unlikely to be chance.

Tests are run on the pooled six held-out corpora (1,800 emails) and separately
on the AI-written set (300 emails).

Writes results/final/significance.csv
"""

import os

import pandas as pd
from scipy.stats import binomtest

from common import RESULTS_DIR, TRAIN_CORPORA
import progress

PAIRS = [
    ("Qwen-2.5-7B", "TF-IDF + LogReg"),
    ("Qwen-2.5-7B", "DistilBERT"),
    ("Qwen-2.5-7B", "Gemma-3-12B"),
    ("Qwen-2.5-7B", "Llama-3.1-8B"),
    ("Qwen-2.5-7B few-shot", "Qwen-2.5-7B"),
    ("Qwen-2.5-7B few-shot AI", "Qwen-2.5-7B few-shot"),
    ("Llama-3.2-3B few-shot AI", "Llama-3.2-3B few-shot"),
    ("TF-IDF + LogReg", "DistilBERT"),
    ("Gemma-3-12B", "TF-IDF + LogReg"),
]


PRIMARY = {"TF-IDF + LogReg": "loco_clean", "TF-IDF + NB": "loco_clean", "DistilBERT": "loco_clean"}


def preds_table():
    import importlib.util
    spec = importlib.util.spec_from_file_location("an", os.path.join(os.path.dirname(__file__), "06_analysis.py"))
    an = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(an)
    p, _ = an.load_preds()
    p["name"] = p["model"].map(an.pretty)
    # one row per model and email: trained models are compared in their honest
    # leave-one-corpus-out setting, LLMs in the setting that defines them
    keep = []
    for name, g in p.groupby("name"):
        want = PRIMARY.get(name)
        keep.append(g[g.setting == want] if want else g[g.setting.str.startswith("llm_")])
    return pd.concat(keep, ignore_index=True).drop_duplicates(subset=["name", "source", "id"])


def mcnemar(a_ok, b_ok):
    n01 = int(((~a_ok) & b_ok).sum())   # only b right
    n10 = int((a_ok & (~b_ok)).sum())   # only a right
    n = n01 + n10
    if n == 0:
        return n10, n01, 1.0
    return n10, n01, binomtest(n10, n, 0.5).pvalue


def main():
    p = preds_table()
    rows = []
    for a, b in PAIRS:
        for scope, sets in [("six unseen corpora", TRAIN_CORPORA), ("AI-written (E-PhishLLM)", ["ephishllm"])]:
            da = p[(p.name == a) & (p.source.isin(sets))].set_index(["source", "id"]).sort_index()
            db = p[(p.name == b) & (p.source.isin(sets))].set_index(["source", "id"]).sort_index()
            ids = da.index.intersection(db.index)
            if len(ids) < 50:
                continue
            da, db = da.loc[ids], db.loc[ids]
            a_ok = (da.pred == da.label).values
            b_ok = (db.pred == db.label).values
            n10, n01, pv = mcnemar(a_ok, b_ok)
            rows.append({"model_a": a, "model_b": b, "scope": scope, "n": len(ids),
                         "a_correct_only": n10, "b_correct_only": n01,
                         "acc_a": round(a_ok.mean(), 4), "acc_b": round(b_ok.mean(), 4),
                         "p_value": f"{pv:.2e}", "significant_at_0.05": pv < 0.05})
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(RESULTS_DIR, "significance.csv"), index=False)
    print(out.to_string(index=False))
    progress.mark("08_significance", f"{len(out)} tests")


if __name__ == "__main__":
    main()
