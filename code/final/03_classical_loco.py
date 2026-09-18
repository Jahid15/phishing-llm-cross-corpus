"""
Step 3. Classical models (TF-IDF + Logistic Regression, TF-IDF + Naive Bayes)
under leave-one-corpus-out (LOCO), with and without decontamination.

For every held-out corpus T:
  in-corpus  : 80/20 split inside T (what most papers report)
  loco_raw   : train on the other five corpora as they are, test on all of T
  loco_clean : same, but first drop every training email that has a
               near duplicate in T (links from 02_overlap.py)
The gap between loco_raw and loco_clean is the score inflation caused by
leaked emails.

The extra test sets (nazario, nigerian, ephishllm) are scored with a model
trained on all six corpora, again raw and clean.

We also run the one-corpus-to-one-corpus matrix (6 x 6) like the
preliminary experiment, raw and clean.

Predictions on the shared evaluation subsets are saved for the final table.
"""

import os
import time

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from common import DATA_DIR, EXTRA_TESTS, RESULTS_DIR, SEED, TRAIN_CORPORA, load, load_eval

MAX_CHARS = 20000
PRED_DIR = os.path.join(RESULTS_DIR, "preds")
os.makedirs(PRED_DIR, exist_ok=True)


def make(model_name):
    clf = LogisticRegression(max_iter=1000) if model_name == "logreg" else MultinomialNB()
    return Pipeline([("tfidf", TfidfVectorizer(max_features=50000, ngram_range=(1, 2), min_df=2)),
                     ("clf", clf)])


def scores(y, p):
    pr, rc, f1, _ = precision_recall_fscore_support(y, p, average="binary", pos_label=1, zero_division=0)
    return {"accuracy": round(accuracy_score(y, p), 4), "precision": round(pr, 4),
            "recall": round(rc, 4), "f1": round(f1, 4)}


def clip(s):
    return s.str.slice(0, MAX_CHARS)


def main():
    data = {c: load(c) for c in TRAIN_CORPORA + EXTRA_TESTS}
    evals = {c: load_eval(c) for c in TRAIN_CORPORA + EXTRA_TESTS}
    links = pd.read_csv(os.path.join(DATA_DIR, "near_dup_links.csv"))

    def dirty_ids(test_source):
        return set(links.loc[links.dup_in == test_source, "id"])

    rows, pred_rows = [], []

    for model_name in ["logreg", "naive_bayes"]:
        # in-corpus reference
        for t in TRAIN_CORPORA:
            df = data[t]
            xtr, xte, ytr, yte = train_test_split(clip(df.text), df.label, test_size=0.2,
                                                  random_state=SEED, stratify=df.label)
            m = make(model_name).fit(xtr, ytr)
            rows.append({"model": model_name, "setting": "in_corpus", "test": t,
                         "train_size": len(xtr), "removed": 0, **scores(yte, m.predict(xte))})

        # leave one corpus out, raw and clean, plus extra test sets
        for t in TRAIN_CORPORA + ["ALL"]:
            train_sources = [c for c in TRAIN_CORPORA if c != t]
            train = pd.concat([data[c] for c in train_sources], ignore_index=True)
            tests = [t] if t != "ALL" else EXTRA_TESTS
            for setting in ["loco_raw", "loco_clean"]:
                for test in tests:
                    tr = train
                    removed = 0
                    if setting == "loco_clean":
                        bad = dirty_ids(test)
                        tr = train[~train.id.isin(bad)]
                        removed = len(train) - len(tr)
                    m = make(model_name).fit(clip(tr.text), tr.label)
                    te = data[test]
                    t0 = time.time()
                    pred = m.predict(clip(te.text))
                    sec_per_1k = (time.time() - t0) / len(te) * 1000
                    rows.append({"model": model_name, "setting": setting, "test": test,
                                 "train_size": len(tr), "removed": removed,
                                 "cpu_sec_per_1000": round(sec_per_1k, 3), **scores(te.label, pred)})
                    ev = evals[test]
                    for i, l, p in zip(ev.id, ev.label, m.predict(clip(ev.text))):
                        pred_rows.append({"model": model_name, "setting": setting, "source": test,
                                          "id": i, "label": l, "pred": int(p)})
                    print(model_name, setting, test, rows[-1]["f1"], "removed", removed)

    pd.DataFrame(rows).to_csv(os.path.join(RESULTS_DIR, "classical_loco.csv"), index=False)
    pd.DataFrame(pred_rows).to_csv(os.path.join(PRED_DIR, "classical.csv"), index=False)

    # 6 x 6 pairwise matrix with logistic regression, raw and clean
    pair = []
    for a in TRAIN_CORPORA:
        for b in TRAIN_CORPORA:
            if a == b:
                continue
            for setting in ["raw", "clean"]:
                tr = data[a]
                if setting == "clean":
                    tr = tr[~tr.id.isin(dirty_ids(b))]
                m = make("logreg").fit(clip(tr.text), tr.label)
                s = scores(data[b].label, m.predict(clip(data[b].text)))
                pair.append({"train": a, "test": b, "setting": setting,
                             "train_size": len(tr), **s})
        print("pairwise done for", a)
    pd.DataFrame(pair).to_csv(os.path.join(RESULTS_DIR, "classical_pairwise.csv"), index=False)
    print("saved classical results")


if __name__ == "__main__":
    main()
