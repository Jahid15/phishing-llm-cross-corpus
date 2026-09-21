"""
Step 7. Two-stage detectors, built from predictions we already have.

No new API calls: we reuse the saved per-email predictions on the shared
evaluation subsets, so we can ask what happens if two cheap detectors are
combined, and what that would cost.

Two policies:
  confirm : stage 2 only sees the emails stage 1 flagged. Final verdict is
            "phishing" when both say so. Fewer false alarms.
            cost = cost1 + cost2 * (share of mail stage 1 flags)
  rescue  : stage 2 only sees the emails stage 1 cleared. Final verdict is
            "phishing" when either says so. Higher recall.
            cost = cost1 + cost2 * (share of mail stage 1 clears)

Writes results/final/cascade.csv
"""

import glob
import os

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score

from common import RESULTS_DIR, TRAIN_CORPORA
import progress

PAIRS = [("Gemma-3-12B", "Qwen-2.5-7B"), ("Llama-3.1-8B", "Qwen-2.5-7B"),
         ("TF-IDF + LogReg", "Qwen-2.5-7B"), ("TF-IDF + LogReg", "Gemma-3-12B"),
         ("Qwen-2.5-7B", "Gemma-3-12B")]
SETS = TRAIN_CORPORA + ["ephishllm"]


def load_preds():
    frames = [pd.read_csv(f) for f in
              [os.path.join(RESULTS_DIR, "preds", "classical.csv"),
               os.path.join(RESULTS_DIR, "preds", "distilbert.csv")] if os.path.exists(f)]
    import importlib.util
    spec = importlib.util.spec_from_file_location("an", os.path.join(os.path.dirname(__file__), "06_analysis.py"))
    an = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(an)
    llm, cost = an.load_preds()
    llm["name"] = llm["model"].map(an.pretty)
    keep = llm[llm.setting.isin(["llm_zero"])][["name", "setting", "source", "id", "label", "pred"]]
    cl = pd.concat(frames, ignore_index=True)
    cl = cl[cl.setting == "loco_clean"]
    cl["name"] = cl["model"].map(an.SHORT)
    cl = cl[["name", "setting", "source", "id", "label", "pred"]]
    costs = {an.pretty(k): v["usd_per_1000"] for k, v in cost.items()}
    return pd.concat([keep, cl], ignore_index=True), costs


def metrics(y, p):
    return {"f1": f1_score(y, p, zero_division=0), "precision": precision_score(y, p, zero_division=0),
            "recall": recall_score(y, p, zero_division=0),
            "false_alarm": ((p == 1) & (y == 0)).sum() / max(1, (y == 0).sum())}


def main():
    preds, costs = load_preds()
    rows = []
    for a, b in PAIRS:
        for policy in ["confirm", "rescue"]:
            per_set = []
            for src in SETS:
                pa = preds[(preds.name == a) & (preds.source == src)].set_index("id")
                pb = preds[(preds.name == b) & (preds.source == src)].set_index("id")
                ids = pa.index.intersection(pb.index)
                if len(ids) == 0:
                    continue
                y = pa.loc[ids, "label"].values
                p1, p2 = pa.loc[ids, "pred"].values, pb.loc[ids, "pred"].values
                if policy == "confirm":
                    final = ((p1 == 1) & (p2 == 1)).astype(int)
                    share_to_stage2 = (p1 == 1).mean()
                else:
                    final = ((p1 == 1) | (p2 == 1)).astype(int)
                    share_to_stage2 = (p1 == 0).mean()
                m = metrics(y, final)
                m.update({"set": src, "share_to_stage2": share_to_stage2})
                per_set.append(m)
            if not per_set:
                continue
            d = pd.DataFrame(per_set).set_index("set")
            unseen = d.loc[[s for s in TRAIN_CORPORA if s in d.index]]
            cost = costs.get(a, 0.0) + costs.get(b, 0.0) * float(unseen.share_to_stage2.mean())
            rows.append({"stage1": a, "stage2": b, "policy": policy,
                         "unseen_f1": round(unseen.f1.mean(), 3),
                         "unseen_recall": round(unseen.recall.mean(), 3),
                         "false_alarm": round(unseen.false_alarm.mean(), 3),
                         "ai_phishing_f1": round(float(d.loc["ephishllm", "f1"]), 3) if "ephishllm" in d.index else np.nan,
                         "ai_phishing_recall": round(float(d.loc["ephishllm", "recall"]), 3) if "ephishllm" in d.index else np.nan,
                         "share_to_stage2": round(float(unseen.share_to_stage2.mean()), 3),
                         "usd_per_1000": round(cost, 4)})
    out = pd.DataFrame(rows).sort_values(["policy", "unseen_f1"], ascending=[True, False])
    out.to_csv(os.path.join(RESULTS_DIR, "cascade.csv"), index=False)
    print(out.to_string(index=False))
    progress.mark("07_cascade", f"{len(out)} combinations")


if __name__ == "__main__":
    main()
