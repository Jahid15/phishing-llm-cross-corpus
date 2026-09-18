"""
Downloads the email datasets and builds cleaned csv files with two columns: text, label.
Label 1 means phishing, 0 means legitimate.
Datasets: Kaggle Phishing Email dataset (via HuggingFace mirror), SpamAssassin,
and Nazario phishing + Enron ham (both from the Zenodo curated collection, record 8339691).
"""

import os
import urllib.request

import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")

FILES = {
    "Phishing_Email.csv": "https://huggingface.co/datasets/zefang-liu/phishing-email-dataset/resolve/main/Phishing_Email.csv",
    "SpamAssasin.csv": "https://zenodo.org/records/8339691/files/SpamAssasin.csv?download=1",
    "Nazario.csv": "https://zenodo.org/records/8339691/files/Nazario.csv?download=1",
    "Enron.csv": "https://zenodo.org/records/8339691/files/Enron.csv?download=1",
}


def download_all():
    os.makedirs(RAW_DIR, exist_ok=True)
    for name, url in FILES.items():
        path = os.path.join(RAW_DIR, name)
        if os.path.exists(path) and os.path.getsize(path) > 100000:
            print("already have", name)
            continue
        print("downloading", name)
        urllib.request.urlretrieve(url, path)


def clean(df):
    df = df.dropna(subset=["text"]).copy()
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"].str.len() > 20]
    df = df.drop_duplicates(subset=["text"])
    return df[["text", "label"]]


def build_kaggle():
    df = pd.read_csv(os.path.join(RAW_DIR, "Phishing_Email.csv"))
    df["text"] = df["Email Text"]
    df["label"] = (df["Email Type"] == "Phishing Email").astype(int)
    return clean(df)


def build_spamassassin():
    df = pd.read_csv(os.path.join(RAW_DIR, "SpamAssasin.csv"))
    df["text"] = df["subject"].fillna("") + "\n" + df["body"].fillna("")
    return clean(df)


def build_nazario_enron():
    naz = pd.read_csv(os.path.join(RAW_DIR, "Nazario.csv"))
    naz["text"] = naz["subject"].fillna("") + "\n" + naz["body"].fillna("")
    naz = clean(naz)

    enron = pd.read_csv(os.path.join(RAW_DIR, "Enron.csv"))
    enron = enron[enron["label"] == 0]
    enron["text"] = enron["subject"].fillna("") + "\n" + enron["body"].fillna("")
    enron = clean(enron)
    # sample the same number of ham emails as phishing to keep the set balanced
    enron = enron.sample(n=len(naz), random_state=42)

    return pd.concat([naz, enron], ignore_index=True)


def main():
    download_all()
    os.makedirs(OUT_DIR, exist_ok=True)
    builders = {
        "kaggle.csv": build_kaggle,
        "spamassassin.csv": build_spamassassin,
        "nazario_enron.csv": build_nazario_enron,
    }
    for name, fn in builders.items():
        df = fn()
        df.to_csv(os.path.join(OUT_DIR, name), index=False)
        print(name, "->", len(df), "emails, phishing:", int(df["label"].sum()))


if __name__ == "__main__":
    main()
