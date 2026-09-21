"""
Step 13. What the numbers look like at a realistic amount of phishing.

Our evaluation subsets are balanced, half phishing and half legitimate. A real
mailbox is not: most mail is legitimate. F1 and precision depend on that
balance, so a model that raises many false alarms looks much worse once the
balance is realistic, while recall and the false alarm rate do not change.

For a base rate p we keep the measured recall (TPR) and false alarm rate (FPR)
and recompute:
    precision(p) = p*TPR / (p*TPR + (1-p)*FPR)
    alerts per 1,000 emails = 1000 * (p*TPR + (1-p)*FPR)
    false alerts per 1,000  = 1000 * (1-p)*FPR

Writes results/final/base_rate.csv
"""

import os

import pandas as pd

from common import RESULTS_DIR, TRAIN_CORPORA
import progress

RATES = [0.5, 0.10, 0.05, 0.01]


def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location("an", os.path.join(os.path.dirname(__file__), "06_analysis.py"))
    an = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(an)
    preds, _ = an.load_preds()
    preds["name"] = preds["model"].map(an.pretty)
    keep = {"TF-IDF + LogReg": "loco_clean", "TF-IDF + NB": "loco_clean", "DistilBERT": "loco_clean"}

    rows = []
    for (name, setting), g in preds[preds.source.isin(TRAIN_CORPORA)].groupby(["name", "setting"]):
        if name in keep and setting != keep[name]:
            continue
        if name not in keep and not setting.startswith("llm_"):
            continue
        tpr = g[g.label == 1].pred.mean()
        fpr = g[g.label == 0].pred.mean()
        row = {"model": name, "setting": setting, "recall": round(tpr, 3), "false_alarm": round(fpr, 3)}
        for p in RATES:
            prec = p * tpr / (p * tpr + (1 - p) * fpr) if (p * tpr + (1 - p) * fpr) > 0 else 0.0
            f1 = 2 * prec * tpr / (prec + tpr) if (prec + tpr) > 0 else 0.0
            row[f"precision@{p:g}"] = round(prec, 3)
            row[f"f1@{p:g}"] = round(f1, 3)
            row[f"false_alerts_per_1000@{p:g}"] = round(1000 * (1 - p) * fpr, 1)
        rows.append(row)
    out = pd.DataFrame(rows).sort_values("f1@0.05", ascending=False)
    out.to_csv(os.path.join(RESULTS_DIR, "base_rate.csv"), index=False)
    cols = ["model", "recall", "false_alarm", "precision@0.5", "precision@0.05", "f1@0.05", "false_alerts_per_1000@0.05"]
    print(out[cols].to_string(index=False))
    progress.mark("13_baserate", "prevalence sensitivity computed")


if __name__ == "__main__":
    main()
