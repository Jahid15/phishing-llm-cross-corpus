"""Collects every number the slides quote from results/final into numbers.json."""
import json
import os

import pandas as pd

R = os.path.join(os.path.dirname(__file__), "..", "results", "final")
n = {}

stats = pd.read_csv(os.path.join(R, "dataset_stats.csv"))
n["datasets"] = stats.to_dict("records")
n["total_emails_used"] = int(stats.emails_used.sum())
n["total_emails_clean"] = int(stats.emails_after_cleaning.sum())

pairs = pd.read_csv(os.path.join(R, "overlap_pairs.csv"))
def found(level, a, b):
    r = pairs[(pairs.level == level) & (pairs.contains == a) & (pairs.source == b)]
    return (int(r.emails_of_source_found.iat[0]), float(r.pct_of_source.iat[0])) if len(r) else (0, 0.0)
n["sa_in_kaggle"] = {lvl: found(lvl, "kaggle", "spamassassin") for lvl in ["exact_raw", "exact_norm", "near"]}
n["ling_in_kaggle_near"] = found("near", "kaggle", "ling")
n["enron_in_kaggle_near"] = found("near", "kaggle", "enron")
n["kaggle_in_enron_near"] = found("near", "enron", "kaggle")

pw = pd.read_csv(os.path.join(R, "classical_pairwise.csv"))
def pwf(a, b, s):
    return float(pw[(pw.train == a) & (pw.test == b) & (pw.setting == s)].f1.iat[0])
n["kaggle_to_sa"] = {"raw": pwf("kaggle", "spamassassin", "raw"), "clean": pwf("kaggle", "spamassassin", "clean")}
n["kaggle_to_enron"] = {"raw": pwf("kaggle", "enron", "raw"), "clean": pwf("kaggle", "enron", "clean")}
n["kaggle_to_ling"] = {"raw": pwf("kaggle", "ling", "raw"), "clean": pwf("kaggle", "ling", "clean")}

inf = pd.read_csv(os.path.join(R, "inflation.csv"))
n["inflation_logreg"] = inf[inf.model == "TF-IDF + LogReg"].round(3).astype(object).where(inf.notna(), None).to_dict("records")

main = pd.read_csv(os.path.join(R, "main_table.csv"))
n["main"] = main.fillna("").to_dict("records")

cost = pd.read_csv(os.path.join(R, "llm_cost.csv"))
n["llm_cost"] = cost.to_dict("records")
n["llm_total_usd"] = round(float(cost.total_usd.sum()), 4)
n["llm_calls"] = int(cost.calls.sum())
disc = os.path.join(R, "llm_raw_discarded")
n["discarded_usd"] = round(sum(pd.read_csv(os.path.join(disc, f)).cost_usd.sum() for f in os.listdir(disc)), 4) if os.path.isdir(disc) else 0.0

db = os.path.join(R, "distilbert_timing.csv")
if os.path.exists(db):
    t = pd.read_csv(db)
    n["distilbert_train_min_per_fold"] = round(float(t[t.setting == "loco_clean"].train_sec.mean()) / 60, 1)
    n["distilbert_infer_sec_per_1000"] = round(float(t.infer_sec_per_1000.mean()), 1)

cl = pd.read_csv(os.path.join(R, "classical_loco.csv"))
n["logreg_cpu_sec_per_1000"] = round(float(cl[(cl.model == "logreg") & (cl.setting == "loco_clean")].cpu_sec_per_1000.mean()), 2)

json.dump(n, open(os.path.join(os.path.dirname(__file__), "numbers.json"), "w"), indent=1, default=float, allow_nan=False)
print(json.dumps({k: v for k, v in n.items() if k not in ("datasets", "main", "inflation_logreg", "llm_cost")}, indent=1, default=float))
