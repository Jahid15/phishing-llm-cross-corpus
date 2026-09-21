"""
Step 1. Build nine clean email sources with the same columns:
    id, subject, body, text, label
text = subject + newline + body. It is what every model reads.
label 1 = phishing or spam (unwanted), 0 = legitimate.

Sources
  training corpora (both classes): spamassassin, ceas08, trec07, ling, enron, kaggle
  extra test sets: nazario (phishing only), nigerian (fraud only),
                   ephishllm (LLM written, English), and the Italian and German
                   parts of the same corpus (ephishllm_it, ephishllm_de)

Raw files come from Zenodo record 8339691, the Kaggle phishing email set
(HuggingFace mirror) and github.com/pajola/e-phishGen.
"""

import csv
import json
import os
import sys
import urllib.request

import pandas as pd

from common import (CAP_PER_CORPUS, DATA_DIR, EVAL_PER_SET, RAW_DIR, SEED,
                    TRAIN_CORPORA, EXTRA_TESTS)

csv.field_size_limit(sys.maxsize)

ZENODO = "https://zenodo.org/records/8339691/files/{}?download=1"
FILES = {
    "SpamAssasin.csv": ZENODO.format("SpamAssasin.csv"),
    "CEAS_08.csv": ZENODO.format("CEAS_08.csv"),
    "TREC_07.csv": ZENODO.format("TREC_07.csv"),
    "Ling.csv": ZENODO.format("Ling.csv"),
    "Enron.csv": ZENODO.format("Enron.csv"),
    "Nazario.csv": ZENODO.format("Nazario.csv"),
    "Nigerian_Fraud.csv": ZENODO.format("Nigerian_Fraud.csv"),
    "Phishing_Email.csv": "https://huggingface.co/datasets/zefang-liu/phishing-email-dataset/resolve/main/Phishing_Email.csv",
    "ephishLLM.json": "https://raw.githubusercontent.com/pajola/e-phishGen/main/ephishLLM.json",
}


def download_all():
    os.makedirs(RAW_DIR, exist_ok=True)
    for name, url in FILES.items():
        path = os.path.join(RAW_DIR, name)
        if os.path.exists(path) and os.path.getsize(path) > 100000:
            continue
        print("downloading", name)
        urllib.request.urlretrieve(url, path)


def zenodo(filename):
    df = pd.read_csv(os.path.join(RAW_DIR, filename), engine="python")
    return pd.DataFrame({"subject": df["subject"].fillna(""),
                         "body": df["body"].fillna(""),
                         "label": df["label"].astype(int)})


def kaggle():
    df = pd.read_csv(os.path.join(RAW_DIR, "Phishing_Email.csv"))
    return pd.DataFrame({"subject": "",
                         "body": df["Email Text"].fillna(""),
                         "label": (df["Email Type"] == "Phishing Email").astype(int)})


def ephishllm(lang="en"):
    rows = json.load(open(os.path.join(RAW_DIR, "ephishLLM.json")))
    df = pd.DataFrame(rows)
    df = df[df["Language"] == lang]
    return pd.DataFrame({"subject": df["Subject"].fillna(""),
                         "body": df["Body"].fillna(""),
                         "label": df["type"].astype(int)})


BUILDERS = {
    "spamassassin": lambda: zenodo("SpamAssasin.csv"),
    "ceas08": lambda: zenodo("CEAS_08.csv"),
    "trec07": lambda: zenodo("TREC_07.csv"),
    "ling": lambda: zenodo("Ling.csv"),
    "enron": lambda: zenodo("Enron.csv"),
    "kaggle": kaggle,
    "nazario": lambda: zenodo("Nazario.csv"),
    "nigerian": lambda: zenodo("Nigerian_Fraud.csv"),
    "ephishllm": ephishllm,
    "ephishllm_it": lambda: ephishllm("it"),
    "ephishllm_de": lambda: ephishllm("de"),
}


def clean(df):
    df = df.copy()
    df["subject"] = df["subject"].astype(str).str.strip()
    df["body"] = df["body"].astype(str).str.strip()
    df["text"] = (df["subject"] + "\n" + df["body"]).str.strip()
    df = df[df["body"].str.len() > 20]
    # duplicates inside one corpus are removed here, between corpora later
    df = df.drop_duplicates(subset=["text"])
    return df


def stratified_cap(df, cap):
    if len(df) <= cap:
        return df
    frac = cap / len(df)
    parts = [g.sample(n=int(round(len(g) * frac)), random_state=SEED)
             for _, g in df.groupby("label")]
    return pd.concat(parts)


def main():
    download_all()
    stats = []
    for name, build in BUILDERS.items():
        full = clean(build()).reset_index(drop=True)
        n_full = len(full)
        # full cleaned corpus is kept too, the overlap study uses it
        full.insert(0, "id", [f"{name}:full{i}" for i in range(len(full))])
        full[["id", "subject", "body", "text", "label"]].to_csv(
            os.path.join(DATA_DIR, "full_" + name + ".csv"), index=False)
        full = full.drop(columns="id")
        df = stratified_cap(full, CAP_PER_CORPUS).reset_index(drop=True)
        df.insert(0, "id", [f"{name}:{i}" for i in range(len(df))])
        df[["id", "subject", "body", "text", "label"]].to_csv(
            os.path.join(DATA_DIR, name + ".csv"), index=False)

        # fixed evaluation subset, balanced when both classes exist
        if df["label"].nunique() == 2:
            half = EVAL_PER_SET // 2
            ev = pd.concat([df[df.label == 1].sample(n=min(half, (df.label == 1).sum()), random_state=SEED),
                            df[df.label == 0].sample(n=min(half, (df.label == 0).sum()), random_state=SEED)])
        else:
            ev = df.sample(n=min(EVAL_PER_SET // 2, len(df)), random_state=SEED)
        ev[["id", "text", "label"]].to_csv(os.path.join(DATA_DIR, "eval_" + name + ".csv"), index=False)

        role = "train+test" if name in TRAIN_CORPORA else "test only"
        stats.append({"source": name, "role": role, "emails_after_cleaning": n_full,
                      "emails_used": len(df), "phishing_or_spam": int(df.label.sum()),
                      "legitimate": int((df.label == 0).sum()), "eval_subset": len(ev)})
        print(stats[-1])

    from common import RESULTS_DIR
    pd.DataFrame(stats).to_csv(os.path.join(RESULTS_DIR, "dataset_stats.csv"), index=False)
    print("saved results/final/dataset_stats.csv")


if __name__ == "__main__":
    main()
