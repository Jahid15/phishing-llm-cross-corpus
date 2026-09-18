"""
Step 2. How many emails do the corpora share with each other?

We check three levels, from strict to loose:
  exact_raw   md5 of the text exactly as the model reads it (subject + body)
  exact_norm  md5 of the body after lowercasing and removing ALL whitespace
              (this is what our preliminary check_overlap.py did)
  near        MinHash on 9-character shingles of the body reduced to lowercase
              letters and digits only, pairs with estimated Jaccard
              similarity >= 0.8 count as the same email

Why characters and not words: the Kaggle aggregate often deletes line
breaks, which glues two words together ("cream?Isn't"). Word shingles
break on that, character shingles over letters and digits do not.

Runs on the full cleaned corpora, not the 10k samples.
Outputs
  results/final/overlap_matrix_<level>.csv   row corpus contains X% of column corpus
  results/final/overlap_pairs.csv            counts per pair and level
  data/final/near_dup_links.csv              id -> other sources it has a near duplicate in
                                             (used later to decontaminate training data)
"""

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


def md5(s):
    return hashlib.md5(s.encode("utf-8", "ignore")).hexdigest()


def alnum(text):
    return re.sub(r"[^a-z0-9]", "", str(text).lower())


def shingles(chars):
    chars = chars[:MAX_CHARS]
    if len(chars) < SHINGLE:
        return [chars.encode()]
    return list({chars[i:i + SHINGLE].encode() for i in range(len(chars) - SHINGLE + 1)})


def main():
    t0 = time.time()
    frames = []
    for s in ALL_SOURCES:
        df = pd.read_csv(os.path.join(DATA_DIR, "full_" + s + ".csv"), keep_default_na=False)
        df["source"] = s
        frames.append(df[["id", "source", "text", "body"]])
    data = pd.concat(frames, ignore_index=True)
    body = data["body"].map(strip_subject_prefix)
    data["h_raw"] = data["text"].map(md5)
    data["h_norm"] = body.map(lambda b: md5("".join(b.lower().split())))
    data["alnum"] = body.map(alnum)
    print("loaded", len(data), "emails in", round(time.time() - t0), "s")

    # MinHash signatures in bulk
    sh = [shingles(n) for n in data["alnum"]]
    mhs = MinHash.bulk(sh, num_perm=NUM_PERM)
    print("minhash done", round(time.time() - t0), "s")

    lsh = MinHashLSH(threshold=THRESHOLD, num_perm=NUM_PERM)
    for i, m in enumerate(mhs):
        lsh.insert(i, m, check_duplication=False)
    print("lsh built", round(time.time() - t0), "s")

    sources = data["source"].values
    near_links = defaultdict(set)   # row index -> set of other sources
    for i, m in enumerate(mhs):
        for j in lsh.query(m):
            if sources[j] != sources[i] and sources[j] not in near_links[i]:
                if mhs[i].jaccard(mhs[j]) >= THRESHOLD:
                    near_links[i].add(sources[j])
    print("near duplicate search done", round(time.time() - t0), "s")

    # links for exact levels
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
        # M[a][b] = percent of emails in b that also appear in a
        mat = pd.DataFrame(0.0, index=ALL_SOURCES, columns=ALL_SOURCES)
        cnt = defaultdict(int)
        for i, others in links.items():
            for a in others:
                cnt[(a, sources[i])] += 1
        for (a, b), c in cnt.items():
            mat.loc[a, b] = round(100 * c / sizes[b], 2)
        mat.to_csv(os.path.join(RESULTS_DIR, f"overlap_matrix_{level}.csv"))
        for (a, b), c in cnt.items():
            pair_rows.append({"level": level, "contains": a, "source": b,
                              "emails_of_source_found": c, "source_size": int(sizes[b]),
                              "pct_of_source": round(100 * c / sizes[b], 2)})
        total = sum(1 for v in links.values() if v)
        print(level, "emails with a copy in another corpus:", total)

    pd.DataFrame(pair_rows).sort_values(["level", "emails_of_source_found"], ascending=[True, False]) \
        .to_csv(os.path.join(RESULTS_DIR, "overlap_pairs.csv"), index=False)

    # map the near links to the ids of the 10k samples used in the experiments
    text_to_links = {}
    for i, others in near_links.items():
        if others:
            text_to_links[(sources[i], data["h_raw"].iat[i])] = others
    rows = []
    for s in ALL_SOURCES:
        used = pd.read_csv(os.path.join(DATA_DIR, s + ".csv"), keep_default_na=False)
        for uid, text in zip(used["id"], used["text"]):
            others = text_to_links.get((s, md5(text)))
            if others:
                for o in sorted(others):
                    rows.append({"id": uid, "source": s, "dup_in": o})
    pd.DataFrame(rows, columns=["id", "source", "dup_in"]).to_csv(
        os.path.join(DATA_DIR, "near_dup_links.csv"), index=False)
    print("saved overlap results, total time", round(time.time() - t0), "s")


if __name__ == "__main__":
    main()
