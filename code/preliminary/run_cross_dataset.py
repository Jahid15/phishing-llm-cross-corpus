"""
Cross dataset generalization test. Trains TF-IDF + Logistic Regression on one
dataset and evaluates on the other two. The diagonal uses the normal 80/20
split so it is comparable with run_baselines.py.
Writes results/cross_dataset_results.csv
"""

import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "results", "preliminary")

DATASETS = ["kaggle", "spamassassin", "nazario_enron"]


def make_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(max_features=50000, ngram_range=(1, 2), min_df=2)),
        ("clf", LogisticRegression(max_iter=1000)),
    ])


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    data = {}
    for name in DATASETS:
        data[name] = pd.read_csv(os.path.join(DATA_DIR, name + ".csv"))

    rows = []
    for train_name in DATASETS:
        train_df = data[train_name]
        for test_name in DATASETS:
            if train_name == test_name:
                x_train, x_test, y_train, y_test = train_test_split(
                    train_df["text"], train_df["label"], test_size=0.2,
                    random_state=42, stratify=train_df["label"])
            else:
                x_train, y_train = train_df["text"], train_df["label"]
                x_test, y_test = data[test_name]["text"], data[test_name]["label"]

            pipe = make_pipeline()
            pipe.fit(x_train, y_train)
            pred = pipe.predict(x_test)
            acc = accuracy_score(y_test, pred)
            f1 = f1_score(y_test, pred, pos_label=1)
            rows.append({
                "train_on": train_name,
                "test_on": test_name,
                "accuracy": round(acc, 4),
                "f1": round(f1, 4),
            })
            print("train", train_name, "-> test", test_name,
                  "acc", round(acc, 4), "f1", round(f1, 4))

    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(RESULTS_DIR, "cross_dataset_results.csv"), index=False)
    print("saved results/cross_dataset_results.csv")


if __name__ == "__main__":
    main()
