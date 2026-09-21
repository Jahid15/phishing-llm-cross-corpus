"""
Shared paths and helpers for the final experiments.
Every script in this folder imports from here so that paths, seeds and
text cleaning are the same everywhere.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DIR = os.path.join(ROOT, "data", "raw")
DATA_DIR = os.path.join(ROOT, "data", "final")
RESULTS_DIR = os.path.join(ROOT, "results", "final")
FIG_DIR = os.path.join(ROOT, "results", "final", "figures")

SEED = 42

# six corpora that have both classes, used for leave-one-corpus-out
TRAIN_CORPORA = ["spamassassin", "ceas08", "trec07", "ling", "enron", "kaggle"]
# extra test sets, never used for training
EXTRA_TESTS = ["nazario", "nigerian", "ephishllm", "ephishllm_it", "ephishllm_de"]
# sanitised copies of the English AI-written set, built by 10_variants.py.
# They are evaluation sets only: they are never part of the overlap study,
# because by construction they are copies of ephishllm.
VARIANT_TESTS = ["ephishllm_nolink", "ephishllm_url"]

ALL_SOURCES = TRAIN_CORPORA + EXTRA_TESTS
EVAL_SETS = ALL_SOURCES + VARIANT_TESTS

# emails per corpus kept for the experiments (stratified sample, after cleaning)
CAP_PER_CORPUS = 10000
# emails per test set in the common evaluation subset (all models see the same emails)
EVAL_PER_SET = 300

for d in (DATA_DIR, RESULTS_DIR, FIG_DIR):
    os.makedirs(d, exist_ok=True)


def normalize(text):
    """Lowercase and collapse all whitespace. Used for hashing and shingling."""
    return " ".join(str(text).lower().split())


def strip_subject_prefix(text):
    """Some corpora glue 'Subject: ...' in front of the body. Remove that first line."""
    return re.sub(r"^\s*subject:[^\n]*\n", "", str(text), flags=re.IGNORECASE)


def load(name):
    import pandas as pd
    return pd.read_csv(os.path.join(DATA_DIR, name + ".csv"), keep_default_na=False)


def load_eval(name):
    import pandas as pd
    return pd.read_csv(os.path.join(DATA_DIR, "eval_" + name + ".csv"), keep_default_na=False)
