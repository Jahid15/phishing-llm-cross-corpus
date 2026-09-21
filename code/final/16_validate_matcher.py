"""
Step 16. Does the near-duplicate matcher tell the truth?

The overlap numbers are a headline result, so the matcher needs its own check.
We take a random sample of SpamAssassin emails that have NO whitespace-exact
match in Kaggle (the easy cases are excluded on purpose), compare each one
against every Kaggle email by brute force, and compare that ground truth with
what the MinHash and LSH pipeline decided for the same emails.

Reports precision and recall of the pipeline against brute force.
Writes results/final/matcher_validation.csv and a few example pairs.
"""

import os
import random
import re

import pandas as pd

from common import DATA_DIR, RESULTS_DIR, SEED, strip_subject_prefix
import progress

N_SAMPLE = 400
SHINGLE = 9
MAX_CHARS = 2000
THRESHOLD = 0.8


def alnum(t):
    return re.sub(r"[^a-z0-9]", "", str(t).lower())


def shingles(chars):
    chars = chars[:MAX_CHARS]
    if len(chars) < SHINGLE:
        return {chars}
    return {chars[i:i + SHINGLE] for i in range(len(chars) - SHINGLE + 1)}


def jac(a, b):
    i = len(a & b)
    return i / (len(a) + len(b) - i) if (a or b) else 0.0


def main():
    sa = pd.read_csv(os.path.join(DATA_DIR, "full_spamassassin.csv"), keep_default_na=False)
    kg = pd.read_csv(os.path.join(DATA_DIR, "full_kaggle.csv"), keep_default_na=False)
    nows = lambda t: "".join(str(t).lower().split())
    kaggle_norm = {nows(strip_subject_prefix(b)) for b in kg.body}

    hard = sa[~sa.body.map(lambda b: nows(strip_subject_prefix(b)) in kaggle_norm)]
    sample = hard.sample(n=min(N_SAMPLE, len(hard)), random_state=SEED)
    print(f"{len(hard)} SpamAssassin emails have no whitespace-exact match in Kaggle; "
          f"checking {len(sample)} of them against all {len(kg)} Kaggle emails", flush=True)

    kg_sets = [shingles(alnum(strip_subject_prefix(b))) for b in kg.body]
    links = pd.read_csv(os.path.join(DATA_DIR, "near_dup_links.csv"))
    used = pd.read_csv(os.path.join(DATA_DIR, "spamassassin.csv"), keep_default_na=False)
    flagged_text = set(used.loc[used.id.isin(links.loc[links.dup_in == "kaggle", "id"]), "text"])

    rows, examples = [], []
    for _, e in sample.iterrows():
        s = shingles(alnum(strip_subject_prefix(e.body)))
        best, best_j = -1, 0.0
        for j, ks in enumerate(kg_sets):
            v = jac(s, ks)
            if v > best_j:
                best_j, best = v, j
        truth = best_j >= THRESHOLD
        pipeline = e.text in flagged_text
        rows.append({"id": e.id, "best_jaccard": round(best_j, 3),
                     "brute_force_duplicate": truth, "pipeline_said_duplicate": pipeline})
        if truth and len(examples) < 5:
            examples.append((round(best_j, 3), e.body[:200], kg.body.iat[best][:200]))

    d = pd.DataFrame(rows)
    both = d.brute_force_duplicate & d.pipeline_said_duplicate
    tp, fp = int(both.sum()), int((~d.brute_force_duplicate & d.pipeline_said_duplicate).sum())
    fn = int((d.brute_force_duplicate & ~d.pipeline_said_duplicate).sum())
    prec = tp / max(1, tp + fp)
    rec = tp / max(1, tp + fn)
    d.to_csv(os.path.join(RESULTS_DIR, "matcher_validation.csv"), index=False)
    summary = {"sampled": len(d), "brute_force_duplicates": int(d.brute_force_duplicate.sum()),
               "pipeline_duplicates": int(d.pipeline_said_duplicate.sum()),
               "precision": round(prec, 3), "recall": round(rec, 3),
               "share_of_hard_cases_that_are_duplicates": round(float(d.brute_force_duplicate.mean()), 3)}
    pd.DataFrame([summary]).to_csv(os.path.join(RESULTS_DIR, "matcher_validation_summary.csv"), index=False)
    print(summary)
    with open(os.path.join(RESULTS_DIR, "matcher_examples.md"), "w") as f:
        f.write("# Matched pairs found by brute force\n\n")
        for v, a, b in examples:
            f.write(f"## Jaccard {v}\n\nSpamAssassin: {a!r}\n\nKaggle: {b!r}\n\n---\n\n")
    progress.mark("16_validate_matcher", f"precision {prec:.2f}, recall {rec:.2f}")


if __name__ == "__main__":
    main()
