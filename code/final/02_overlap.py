"""
Step 2. How many emails do the corpora share with each other?

We check three levels, from strict to loose:
  exact_raw   md5 of the text exactly as the model reads it (subject + body)
  exact_norm  md5 of the body after lowercasing and removing ALL whitespace
              (this is what our preliminary check_overlap.py did)
  near        MinHash with locality sensitive hashing proposes candidate pairs
              from 9-character shingles of the body reduced to lowercase
              letters and digits; every candidate is then checked with the
              EXACT Jaccard similarity of the two shingle sets, and pairs at
              0.8 or above count as the same email. The MinHash estimate has a
              standard error of about 0.035 with 128 permutations, which is too
              loose for a headline number, so it is used only to shortlist.

Why characters and not words: the Kaggle aggregate often deletes line
breaks, which glues two words together ("cream?Isn't"). Word shingles
break on that, character shingles over letters and digits do not.

Runs on the full cleaned corpora, not the 10k samples.
Outputs
  results/final/overlap_matrix_<level>.csv   row corpus contains X% of column corpus
  results/final/overlap_pairs.csv            counts per pair and level
  results/final/overlap_thresholds.csv       how the counts change at Jaccard 0.7, 0.8, 0.9
  results/final/within_corpus_dup.csv        near duplicates INSIDE one corpus, including
                                             how many evaluation emails have a near copy in
                                             the training part of their own corpus
  results/final/overlap_timing.csv           wall clock of each stage
  data/final/near_dup_links.csv              id -> other sources it has a near duplicate in
                                             (used later to decontaminate training data)

Options: --max-chars and --threshold with --tag write sensitivity copies
instead of the main files.
"""

import argparse
import hashlib
import os
import re
import time
from collections import defaultdict

import numpy as np
import pandas as pd
from datasketch import MinHash, MinHashLSH

from common import ALL_SOURCES, DATA_DIR, RESULTS_DIR, strip_subject_prefix

NUM_PERM = 128
THRESHOLD = 0.8
SHINGLE = 9
MAX_CHARS = 2000
LSH_THRESHOLD = 0.65   # shortlist generously, then check exactly


def md5(s):
    return hashlib.md5(s.encode("utf-8", "ignore")).hexdigest()


def alnum(text):
    return re.sub(r"[^a-z0-9]", "", str(text).lower())


def shingles(chars):
    chars = chars[:MAX_CHARS]
    if len(chars) < SHINGLE:
        return [chars.encode()]
    return list({chars[i:i + SHINGLE].encode() for i in range(len(chars) - SHINGLE + 1)})


def jaccard(a, b):
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter) if (a or b) else 0.0


def main():
    global MAX_CHARS
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-chars", type=int, default=2000)
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    ap.add_argument("--tag", default="", help="suffix for sensitivity runs")
    args = ap.parse_args()
    MAX_CHARS = args.max_chars
    tag = ("_" + args.tag) if args.tag else ""
    timing = {}

    t0 = time.time()
    frames = []
    for s_ in ALL_SOURCES:
        df = pd.read_csv(os.path.join(DATA_DIR, "full_" + s_ + ".csv"), keep_default_na=False)
        df["source"] = s_
        frames.append(df[["id", "source", "text", "body"]])
    data = pd.concat(frames, ignore_index=True)
    body = data["body"].map(strip_subject_prefix)
    data["h_raw"] = data["text"].map(md5)
    data["h_norm"] = body.map(lambda b: md5("".join(b.lower().split())))
    data["alnum"] = body.map(alnum)
    timing["load"] = round(time.time() - t0, 1)
    print("loaded", len(data), "emails in", timing["load"], "s", flush=True)

    # signatures are built one email at a time: holding every shingle set in
    # memory at once needs far more RAM than a laptop has
    from datasketch import LeanMinHash
    mhs = []
    for n in data["alnum"]:
        m = MinHash(num_perm=NUM_PERM)
        m.update_batch(shingles(n))
        mhs.append(LeanMinHash(m))
    timing["minhash"] = round(time.time() - t0, 1)
    print("minhash done", timing["minhash"], "s", flush=True)

    lsh = MinHashLSH(threshold=LSH_THRESHOLD, num_perm=NUM_PERM)
    for i, m in enumerate(mhs):
        lsh.insert(i, m, check_duplication=False)
    timing["lsh"] = round(time.time() - t0, 1)
    print("lsh built", timing["lsh"], "s", flush=True)

    sources = data["source"].values
    alnum_col = data["alnum"].values
    _cache = {}

    def shingle_set(i):
        """Shingles for one email, recomputed on demand with a small cache."""
        v = _cache.get(i)
        if v is None:
            if len(_cache) > 20000:
                _cache.clear()
            v = _cache[i] = set(shingles(alnum_col[i]))
        return v

    near_links = defaultdict(set)        # row -> other sources holding a near copy
    within = defaultdict(set)            # row -> rows in the same source
    pair_j = []                          # exact similarities, for the threshold study
    for i, m in enumerate(mhs):
        for j in lsh.query(m):
            if j <= i:
                continue
            jac = jaccard(shingle_set(i), shingle_set(j))
            if jac < 0.7:
                continue
            pair_j.append((i, j, jac))
            if jac >= args.threshold:
                if sources[i] != sources[j]:
                    near_links[i].add(sources[j])
                    near_links[j].add(sources[i])
                else:
                    within[i].add(j)
                    within[j].add(i)
    timing["pairs"] = round(time.time() - t0, 1)
    print("exact check of", len(pair_j), "candidate pairs done", timing["pairs"], "s", flush=True)

    # how the cross-corpus counts move with the threshold
    rows = []
    for th in [0.7, 0.8, 0.9]:
        cnt = defaultdict(set)
        for i, j, jac in pair_j:
            if jac >= th and sources[i] != sources[j]:
                cnt[sources[i]].add(i)
                cnt[sources[j]].add(j)
        sizes = data.groupby("source").size()
        for s_ in ALL_SOURCES:
            rows.append({"threshold": th, "source": s_, "emails_with_copy_elsewhere": len(cnt[s_]),
                         "corpus_size": int(sizes[s_]),
                         "pct": round(100 * len(cnt[s_]) / int(sizes[s_]), 2)})
    pd.DataFrame(rows).to_csv(os.path.join(RESULTS_DIR, f"overlap_thresholds{tag}.csv"), index=False)

    def exact_links(col):
        links = defaultdict(set)
        groups = data.groupby(col)["source"].apply(set)
        multi = groups[groups.map(len) > 1]
        lookup = data[col].values
        for i, h in enumerate(lookup):
            if h in multi.index:
                links[i] = multi[h] - {sources[i]}
        return links

    levels = {"exact_raw": exact_links("h_raw"), "exact_norm": exact_links("h_norm"), "near": near_links}
    sizes = data.groupby("source").size()
    pair_rows = []
    for level, links in levels.items():
        mat = pd.DataFrame(0.0, index=ALL_SOURCES, columns=ALL_SOURCES)
        cnt = defaultdict(int)
        for i, others in links.items():
            for a in others:
                cnt[(a, sources[i])] += 1
        for (a, b), c in cnt.items():
            mat.loc[a, b] = round(100 * c / sizes[b], 2)
        mat.to_csv(os.path.join(RESULTS_DIR, f"overlap_matrix_{level}{tag}.csv"))
        for (a, b), c in cnt.items():
            pair_rows.append({"level": level, "contains": a, "source": b,
                              "emails_of_source_found": c, "source_size": int(sizes[b]),
                              "pct_of_source": round(100 * c / sizes[b], 2)})
        print(level, "emails with a copy in another corpus:", sum(1 for v in links.values() if v), flush=True)

    pd.DataFrame(pair_rows).sort_values(["level", "emails_of_source_found"], ascending=[True, False]) \
        .to_csv(os.path.join(RESULTS_DIR, f"overlap_pairs{tag}.csv"), index=False)

    # duplicates inside one corpus: how much of each evaluation subset has a
    # near copy in the part of its own corpus a model would train on
    ids = data["id"].values
    within_rows = []
    for s_ in ALL_SOURCES:
        idx = [i for i in range(len(data)) if sources[i] == s_]
        internal = sum(1 for i in idx if within[i]) / max(1, len(idx))
        used = pd.read_csv(os.path.join(DATA_DIR, s_ + ".csv"), keep_default_na=False)
        ev = pd.read_csv(os.path.join(DATA_DIR, "eval_" + s_ + ".csv"), keep_default_na=False)
        text_to_row = {(sources[i], data["h_raw"].iat[i]): i for i in idx}
        ev_rows = {text_to_row.get((s_, md5(t))) for t in ev.text}
        train_rows = {text_to_row.get((s_, md5(t))) for t in used.text} - ev_rows
        hit = sum(1 for r in ev_rows if r is not None and (within[r] & train_rows))
        within_rows.append({"source": s_, "corpus_internal_near_dup_pct": round(100 * internal, 2),
                            "eval_emails": len(ev),
                            "eval_with_near_dup_in_own_train_pct": round(100 * hit / max(1, len(ev)), 2)})
        print("within", within_rows[-1], flush=True)
    pd.DataFrame(within_rows).to_csv(os.path.join(RESULTS_DIR, f"within_corpus_dup{tag}.csv"), index=False)

    # links for decontamination, mapped onto the capped samples actually used
    text_to_links = {}
    for i, others in near_links.items():
        if others:
            text_to_links[(sources[i], data["h_raw"].iat[i])] = others
    rows = []
    for s_ in ALL_SOURCES:
        used = pd.read_csv(os.path.join(DATA_DIR, s_ + ".csv"), keep_default_na=False)
        for uid, text in zip(used["id"], used["text"]):
            others = text_to_links.get((s_, md5(text)))
            if others:
                for o in sorted(others):
                    rows.append({"id": uid, "source": s_, "dup_in": o})
    if not tag:
        pd.DataFrame(rows, columns=["id", "source", "dup_in"]).to_csv(
            os.path.join(DATA_DIR, "near_dup_links.csv"), index=False)
    timing["total"] = round(time.time() - t0, 1)
    pd.DataFrame([timing]).to_csv(os.path.join(RESULTS_DIR, f"overlap_timing{tag}.csv"), index=False)
    print("saved overlap results, total time", timing["total"], "s")


if __name__ == "__main__":
    main()
