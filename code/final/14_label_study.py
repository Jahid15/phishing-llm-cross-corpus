"""
Step 14. Are we measuring phishing, or spam?

Four of our six corpora mark ordinary bulk spam as positive, while Nazario is
pure credential phishing. That is gap 4 from our proposal: the papers in this
field do not mean the same thing by "positive".

Here we ask an LLM annotator to sort every positive email in the evaluation
subsets into phishing or spam, with a second annotator on a subsample so we can
report agreement rather than trusting one model. Then we recompute detection
rates separately for the two kinds, using predictions we already have.

Writes results/final/label_study.csv          one row per annotated email
       results/final/label_study_summary.csv  composition and per-kind recall
"""

import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from common import RESULTS_DIR, TRAIN_CORPORA, load_eval
import progress

import importlib.util
_s = importlib.util.spec_from_file_location("llm", os.path.join(os.path.dirname(__file__), "05_llm_eval.py"))
llm = importlib.util.module_from_spec(_s)
_s.loader.exec_module(llm)

PRIMARY = "google/gemini-3.1-flash-lite"
SECOND = "openai/gpt-4o-mini"
SECOND_N = 300          # emails also annotated by the second model, for agreement
RAW = os.path.join(RESULTS_DIR, "label_study.csv")

PROMPT = ("You label unwanted emails for a security study. Read the email and choose one label.\n"
          "phishing: it tries to deceive the reader into giving credentials, money or access, "
          "or into opening a malicious link or attachment. Impersonation, fake invoices, "
          "account warnings, advance fee fraud and malware lures are phishing.\n"
          "spam: unsolicited bulk advertising or marketing with no attempt to deceive the "
          "reader into handing something over.\n"
          "Answer with exactly one word: phishing or spam.")


def annotate(model, rows, key):
    out = []
    def one(t):
        return llm.ask(key, model, [{"role": "system", "content": PROMPT}], t, max_tokens=5)
    with ThreadPoolExecutor(max_workers=6) as pool:
        res = list(pool.map(lambda r: one(r["text"]), rows))
    for r, a in zip(rows, res):
        ans = " ".join(str(a["answer"]).lower().split())
        kind = "phishing" if ans.startswith("ph") else ("spam" if ans.startswith("sp") else "unclear")
        out.append({"id": r["id"], "source": r["source"], "annotator": model,
                    "kind": kind, "answer": ans, "cost_usd": a["cost_usd"]})
    return out


def main():
    key = llm.api_key()
    done = pd.read_csv(RAW) if os.path.exists(RAW) else pd.DataFrame(columns=["id", "annotator"])
    rows = []
    for src in TRAIN_CORPORA:
        ev = load_eval(src)
        for _, e in ev[ev.label == 1].iterrows():
            rows.append({"id": e["id"], "source": src, "text": e["text"]})

    records = done.to_dict("records")
    for model, subset in [(PRIMARY, rows), (SECOND, rows[:SECOND_N])]:
        # rows whose annotation failed are tried again
        have = set(done[(done.annotator == model) & (done.kind != "unclear")]["id"]) if len(done) else set()
        todo = [r for r in subset if r["id"] not in have]
        if not todo:
            continue
        print(f"{model}: annotating {len(todo)} emails", flush=True)
        records += annotate(model, todo, key)
        pd.DataFrame(records).to_csv(RAW, index=False)
        llm.add_spend(sum(r["cost_usd"] for r in records if r["annotator"] == model))

    d = pd.DataFrame(records)
    prim = d[d.annotator == PRIMARY].set_index("id")
    sec = d[d.annotator == SECOND].set_index("id")
    both = prim.index.intersection(sec.index)
    agree = (prim.loc[both, "kind"] == sec.loc[both, "kind"]).mean()
    # Cohen's kappa
    a, b = prim.loc[both, "kind"], sec.loc[both, "kind"]
    cats = sorted(set(a) | set(b))
    pe = sum((a == c).mean() * (b == c).mean() for c in cats)
    kappa = (agree - pe) / (1 - pe) if pe < 1 else float("nan")
    print(f"\nannotator agreement on {len(both)} emails: {agree:.3f}, kappa {kappa:.3f}")

    # composition per corpus and detection rate per kind, from existing predictions
    spec = importlib.util.spec_from_file_location("an", os.path.join(os.path.dirname(__file__), "06_analysis.py"))
    an = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(an)
    preds, _ = an.load_preds()
    preds["name"] = preds["model"].map(an.pretty)
    kind = dict(zip(prim.index, prim.kind))

    summary = []
    for src in TRAIN_CORPORA:
        g = prim[prim.source == src]
        summary.append({"row": "composition", "source": src, "n_positives": len(g),
                        "phishing_pct": round(100 * (g.kind == "phishing").mean(), 1),
                        "spam_pct": round(100 * (g.kind == "spam").mean(), 1),
                        "unclear_pct": round(100 * (g.kind == "unclear").mean(), 1)})
    keep = {"TF-IDF + LogReg": "loco_clean", "TF-IDF + NB": "loco_clean", "DistilBERT": "loco_clean"}
    for (name, setting), g in preds[preds.source.isin(TRAIN_CORPORA) & (preds.label == 1)].groupby(["name", "setting"]):
        if name in keep and setting != keep[name]:
            continue
        if name not in keep and not setting.startswith("llm_"):
            continue
        g = g.copy()
        g["kind"] = g.id.map(kind)
        ph, sp = g[g.kind == "phishing"], g[g.kind == "spam"]
        if len(ph) < 20 or len(sp) < 20:
            continue
        summary.append({"row": "recall_by_kind", "model": name, "setting": setting,
                        "n_phishing": len(ph), "n_spam": len(sp),
                        "recall_phishing": round(ph.pred.mean(), 3),
                        "recall_spam": round(sp.pred.mean(), 3),
                        "gap": round(ph.pred.mean() - sp.pred.mean(), 3)})
    summary.append({"row": "agreement", "n": len(both), "agreement": round(agree, 3), "kappa": round(kappa, 3)})
    out = pd.DataFrame(summary)
    out.to_csv(os.path.join(RESULTS_DIR, "label_study_summary.csv"), index=False)
    print(out.to_string(index=False))
    progress.mark("14_label_study", f"agreement {agree:.2f}, kappa {kappa:.2f}")


if __name__ == "__main__":
    main()
