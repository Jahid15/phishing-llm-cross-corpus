"""
Step 17. Is the published detector's failure just a threshold?

We score released models with their default decision rule (the higher of the
two class scores). The ModernBERT card recommends a threshold of 0.37 instead,
which would flag more mail. If that alone fixed the AI-phishing failure, our
reading would be wrong, so we measure it.

Writes results/final/threshold_check.csv
"""

import os

import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from common import RESULTS_DIR, load_eval
import progress

MODEL = "mikaelnurminen/modernbert-large-phishing"
SETS = ["spamassassin", "nazario", "ephishllm", "ephishllm_nolink", "ephishllm_it"]
THRESHOLDS = [0.5, 0.37, 0.2]
DEVICE = os.environ.get("DEVICE", "cpu")


@torch.no_grad()
def main():
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL, attn_implementation="eager").to(DEVICE).eval()
    pos = 1
    rows = []
    for src in SETS:
        ev = load_eval(src)
        probs = []
        for i in range(0, len(ev), 8):
            chunk = [t[:6000] for t in ev.text.iloc[i:i + 8]]
            enc = tok(chunk, truncation=True, max_length=512, padding=True, return_tensors="pt")
            enc = {k: v.to(DEVICE) for k, v in enc.items()}
            probs += model(**enc).logits.softmax(-1)[:, pos].cpu().tolist()
        p = pd.Series(probs)
        y = ev.label.values
        for t in THRESHOLDS:
            pred = (p >= t).astype(int).values
            tp = int(((pred == 1) & (y == 1)).sum())
            fp = int(((pred == 1) & (y == 0)).sum())
            fn = int(((pred == 0) & (y == 1)).sum())
            rec = tp / max(1, tp + fn)
            prec = tp / max(1, tp + fp)
            rows.append({"test_set": src, "threshold": t, "recall": round(rec, 3),
                         "precision": round(prec, 3),
                         "f1": round(2 * prec * rec / max(1e-9, prec + rec), 3),
                         "false_alarm": round(fp / max(1, int((y == 0).sum())), 3),
                         "mean_phishing_prob": round(float(p.mean()), 3)})
        print(rows[-3:], flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(RESULTS_DIR, "threshold_check.csv"), index=False)
    print(out.to_string(index=False))
    progress.mark("17_threshold_check", "ModernBERT at three thresholds")


if __name__ == "__main__":
    main()
