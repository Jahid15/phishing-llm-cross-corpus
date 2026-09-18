"""
Checks for duplicate emails between the three corpora. This backs up the
dataset leakage gap with a real number instead of a guess.
Emails are compared on the normalized body text (lowercased, whitespace removed)
so different formatting of the same email still matches.
Only uses the standard library so it runs on any python.
Writes results/dataset_overlap.csv
"""

import csv
import hashlib
import os
import sys

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "results", "preliminary")

csv.field_size_limit(sys.maxsize)


def read_column(filename, column, where=None):
    values = []
    with open(os.path.join(RAW_DIR, filename), newline="", encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f):
            if where and row.get(where[0]) != where[1]:
                continue
            v = row.get(column)
            if v:
                values.append(v)
    return values


def hashes(texts):
    out = set()
    for t in texts:
        t = "".join(t.lower().split())
        if len(t) > 20:
            out.add(hashlib.md5(t.encode()).hexdigest())
    return out


def main():
    sets = {
        "kaggle": hashes(read_column("Phishing_Email.csv", "Email Text")),
        "spamassassin": hashes(read_column("SpamAssasin.csv", "body")),
        "nazario_enron": hashes(read_column("Nazario.csv", "body")
                                + read_column("Enron.csv", "body", where=("label", "0"))),
    }

    rows = []
    names = list(sets)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            common = len(sets[a] & sets[b])
            pct = round(100 * common / min(len(sets[a]), len(sets[b])), 2)
            rows.append([a, b, len(sets[a]), len(sets[b]), common, pct])
            print(a, "vs", b, "shared:", common, "(", pct, "percent of smaller corpus )")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "dataset_overlap.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["corpus_a", "corpus_b", "unique_a", "unique_b",
                    "shared_emails", "pct_of_smaller"])
        w.writerows(rows)
    print("saved results/dataset_overlap.csv")


if __name__ == "__main__":
    main()
