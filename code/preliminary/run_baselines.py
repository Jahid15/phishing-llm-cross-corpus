"""
Trains classical baselines (TF-IDF + Logistic Regression, TF-IDF + Naive Bayes)
on each dataset separately with an 80/20 split.
Writes results/baseline_results.csv
"""

import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "results", "preliminary")

DATASETS = ["kaggle.csv", "spamassassin.csv", "nazario_enron.csv"]


def make_pipeline(model):
    return Pipeline([
        ("tfidf", TfidfVectorizer(max_features=50000, ngram_range=(1, 2), min_df=2)),
        ("clf", model),
    ])


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rows = []
    for name in DATASETS:
        df = pd.read_csv(os.path.join(DATA_DIR, name))
        x_train, x_test, y_train, y_test = train_test_split(
            df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"])

        models = {
            "logreg": LogisticRegression(max_iter=1000),
            "naive_bayes": MultinomialNB(),
        }
        for model_name, model in models.items():
            pipe = make_pipeline(model)
            pipe.fit(x_train, y_train)
            pred = pipe.predict(x_test)
            acc = accuracy_score(y_test, pred)
            prec, rec, f1, _ = precision_recall_fscore_support(
                y_test, pred, average="binary", pos_label=1)
            rows.append({
                "dataset": name.replace(".csv", ""),
                "model": model_name,
                "train_size": len(x_train),
                "test_size": len(x_test),
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1": round(f1, 4),
            })
            print(name, model_name, "acc", round(acc, 4), "f1", round(f1, 4))

    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(RESULTS_DIR, "baseline_results.csv"), index=False)
    print("saved results/baseline_results.csv")


if __name__ == "__main__":
    main()
