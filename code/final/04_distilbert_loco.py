"""
Step 4. Fine-tuned DistilBERT under the same leave-one-corpus-out protocol.
Both settings are run: with the training data as it is (loco_raw) and after
removing near duplicates of the test corpus (loco_clean), so the leakage
inflation is measured for a neural model too, not only for TF-IDF.

To fit an 8 GB laptop we train on a stratified sample of 1,000 emails per
training corpus (about 5,000 per fold), 1 epoch, 128 tokens, batch 16.
Runs on CPU by default in our runs (DEVICE=cpu). Apple MPS needed more memory than
an 8 GB laptop could give next to the other jobs.

Folds
  in_corpus  : 2,000 emails of T (never the evaluation emails), test on T
  loco_raw   : the five other corpora as they are, test on T
  loco_clean : the same five corpora minus near duplicates of T, test on T
  ALL        : all six corpora minus near duplicates of any extra test set,
               tested on nazario, nigerian and ephishllm
All tests use the shared evaluation subsets (300 or 150 emails).
"""

import gc
import os
import time

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

from common import (DATA_DIR, EXTRA_TESTS, RESULTS_DIR, SEED, TRAIN_CORPORA,
                    VARIANT_TESTS, load, load_eval)

MODEL = "distilbert-base-uncased"
PER_CORPUS = 1000
IN_CORPUS_N = 2000
MAX_LEN = 128
BATCH = 16
LR = 5e-5
DEVICE = os.environ.get("DEVICE") or ("mps" if torch.backends.mps.is_available() else "cpu")
PRED_DIR = os.path.join(RESULTS_DIR, "preds")
FOLD_DIR = os.path.join(RESULTS_DIR, "distilbert_folds")   # one file per fold, so a restart resumes
os.makedirs(FOLD_DIR, exist_ok=True)

torch.manual_seed(SEED)
np.random.seed(SEED)
tok = AutoTokenizer.from_pretrained(MODEL)


def sample(df, n):
    if len(df) <= n:
        return df
    frac = n / len(df)
    return pd.concat([g.sample(n=max(1, int(round(len(g) * frac))), random_state=SEED)
                      for _, g in df.groupby("label")])


def batches(texts, labels=None, shuffle=False):
    idx = list(range(len(texts)))
    loader = DataLoader(idx, batch_size=BATCH, shuffle=shuffle)
    for b in loader:
        enc = tok([texts[i][:4000] for i in b], truncation=True, max_length=MAX_LEN,
                  padding=True, return_tensors="pt")
        enc = {k: v.to(DEVICE) for k, v in enc.items()}
        if labels is not None:
            enc["labels"] = torch.tensor([labels[i] for i in b]).to(DEVICE)
        yield enc


def train(df):
    model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2).to(DEVICE)
    texts, labels = list(df.text), list(df.label.astype(int))
    steps = (len(texts) + BATCH - 1) // BATCH
    opt = torch.optim.AdamW(model.parameters(), lr=LR)
    sch = get_linear_schedule_with_warmup(opt, int(0.1 * steps), steps)
    model.train()
    for enc in batches(texts, labels, shuffle=True):
        loss = model(**enc).loss
        loss.backward()
        opt.step(); sch.step(); opt.zero_grad()
    return model


@torch.no_grad()
def predict(model, texts):
    model.eval()
    out = []
    for enc in batches(list(texts)):
        out += model(**enc).logits.argmax(-1).cpu().tolist()
    return out


def lean(df):
    # only what training needs, texts cut early to keep memory low on an 8 GB laptop
    return pd.DataFrame({"id": df.id, "text": df.text.str.slice(0, 4000), "label": df.label})


def free():
    gc.collect()
    if DEVICE == "mps":
        torch.mps.empty_cache()


def main():
    data = {c: lean(load(c)) for c in TRAIN_CORPORA}
    evals = {c: load_eval(c) for c in TRAIN_CORPORA + EXTRA_TESTS + VARIANT_TESTS}
    links = pd.read_csv(os.path.join(DATA_DIR, "near_dup_links.csv"))
    pred_rows, timing = [], []

    def fold_file(setting, test):
        return os.path.join(FOLD_DIR, f"{setting}__{test}.csv")

    def done(setting, test):
        return os.path.exists(fold_file(setting, test))

    def record(model, setting, test, train_size, train_sec):
        ev = evals[test]
        t0 = time.time()
        preds = predict(model, ev.text)
        sec = time.time() - t0
        timing.append({"setting": setting, "test": test, "train_size": train_size,
                       "train_sec": round(train_sec, 1),
                       "infer_sec_per_1000": round(sec / len(ev) * 1000, 2), "device": DEVICE})
        rows = [{"model": "distilbert", "setting": setting, "source": test,
                 "id": i, "label": l, "pred": int(p)} for i, l, p in zip(ev.id, ev.label, preds)]
        pd.DataFrame(rows).to_csv(fold_file(setting, test), index=False)
        pd.DataFrame([timing[-1]]).to_csv(fold_file(setting, test).replace(".csv", ".timing"), index=False)
        acc = np.mean(np.array(preds) == ev.label.values)
        print(setting, test, "acc", round(acc, 3), "train", train_size, "in", round(train_sec), "s", flush=True)

    for t in TRAIN_CORPORA:
        # in-corpus reference
        if not done("in_corpus", t):
            pool = data[t][~data[t].id.isin(evals[t].id)]
            tr = sample(pool, IN_CORPUS_N)
            t0 = time.time(); m = train(tr); record(m, "in_corpus", t, len(tr), time.time() - t0); m = None; free()

        # leave one corpus out, with and without the duplicates
        bad = set(links.loc[links.dup_in == t, "id"])
        for setting in ["loco_clean", "loco_raw"]:
            if done(setting, t):
                continue
            keep = (lambda df: df[~df.id.isin(bad)]) if setting == "loco_clean" else (lambda df: df)
            tr = pd.concat([sample(keep(data[c]), PER_CORPUS) for c in TRAIN_CORPORA if c != t])
            t0 = time.time(); m = train(tr); record(m, setting, t, len(tr), time.time() - t0); m = None; free()

    extra = EXTRA_TESTS + VARIANT_TESTS
    if not all(done("loco_clean", x) for x in extra):
        bad = set(links.loc[links.dup_in.isin(EXTRA_TESTS), "id"])
        tr = pd.concat([sample(data[c][~data[c].id.isin(bad)], PER_CORPUS) for c in TRAIN_CORPORA])
        t0 = time.time(); m = train(tr); sec = time.time() - t0
        for test in extra:
            record(m, "loco_clean", test, len(tr), sec)
        m = None; free()

    import glob
    pd.concat([pd.read_csv(f) for f in glob.glob(os.path.join(FOLD_DIR, "*.csv"))]).to_csv(
        os.path.join(PRED_DIR, "distilbert.csv"), index=False)
    pd.concat([pd.read_csv(f) for f in glob.glob(os.path.join(FOLD_DIR, "*.timing"))]).to_csv(
        os.path.join(RESULTS_DIR, "distilbert_timing.csv"), index=False)
    print("saved distilbert results")


if __name__ == "__main__":
    main()
