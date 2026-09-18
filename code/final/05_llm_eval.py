"""
Step 5. Small open LLMs through OpenRouter, zero-shot and few-shot.

Every model reads the same fixed evaluation subsets (data/final/eval_*.csv),
so the LLM numbers are directly comparable with the classical and DistilBERT
numbers computed on the same emails.

An LLM never trains on our corpora, so every test set is unseen for it.
Few-shot examples for a test corpus are always taken from the OTHER training
corpora, the same leave-one-corpus-out rule the trained models follow.

The dollar cost is the real cost OpenRouter reports for each call
(usage.cost), not an estimate from the price list. A hard budget stops the
run before it goes over.

Usage
  python 05_llm_eval.py --mode zero --models all
  python 05_llm_eval.py --mode few  --models meta-llama/llama-3.2-3b-instruct
  python 05_llm_eval.py --mode long --models microsoft/phi-4

Mode "long" is the zero-shot prompt with room for 80 output tokens. Some models
(Phi-4) ignore the one-word instruction and start explaining, so with 5 tokens
the verdict is cut off. In long mode we read the verdict out of the explanation.
We tried it on Phi-4 and dropped it: the model often writes a generic checklist
("indicators of a malicious email...") with no verdict, so keyword parsing
reads advice as a verdict. The paper reports the strict run only. The
discarded answers are kept in results/final/llm_raw_discarded/.
"""

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from common import ALL_SOURCES, RESULTS_DIR, ROOT, SEED, TRAIN_CORPORA, load, load_eval

MODELS = [
    "meta-llama/llama-3.2-1b-instruct",
    "meta-llama/llama-3.2-3b-instruct",
    "meta-llama/llama-3.1-8b-instruct",
    "qwen/qwen-2.5-7b-instruct",
    "google/gemma-3-12b-it",
    "microsoft/phi-4",
]
MAX_CHARS = 1500
WORKERS = 8
BUDGET_USD = 1.90
RAW_DIR = os.path.join(RESULTS_DIR, "llm_raw")
SPEND_FILE = os.path.join(RESULTS_DIR, "llm_spend.json")

INSTRUCTION = ("You are an email security assistant. Decide if the email below is "
               "malicious or unwanted (phishing, scam or spam) or legitimate. "
               "Answer with exactly one word: phishing or legitimate.")

lock = threading.Lock()


def api_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    env = os.path.join(ROOT, ".env")
    if os.path.exists(env):
        for line in open(env):
            if line.strip().startswith("OPENROUTER_API_KEY="):
                return line.strip().split("=", 1)[1]
    sys.exit("OPENROUTER_API_KEY not found")


def spent():
    if os.path.exists(SPEND_FILE):
        return json.load(open(SPEND_FILE))["total_usd"]
    return 0.0


def add_spend(usd):
    with lock:
        total = spent() + usd
        json.dump({"total_usd": total}, open(SPEND_FILE, "w"))
        return total


def few_shot_messages(test_source):
    """2 phishing + 2 legitimate short emails from corpora other than the test one."""
    pool = [c for c in TRAIN_CORPORA if c != test_source]
    examples = []
    for i, label in enumerate([1, 0, 1, 0]):
        df = load(pool[i % len(pool)])
        df = df[(df.label == label) & (df.text.str.len().between(150, 600))]
        examples.append((df.sample(n=1, random_state=SEED + i).text.iat[0], label))
    msgs = [{"role": "system", "content": INSTRUCTION}]
    for text, label in examples:
        msgs.append({"role": "user", "content": "Email:\n" + text[:MAX_CHARS]})
        msgs.append({"role": "assistant", "content": "phishing" if label else "legitimate"})
    return msgs


def ask(key, model, prefix, text, max_tokens=5):
    msgs = prefix + [{"role": "user", "content": "Email:\n" + text[:MAX_CHARS]}]
    for attempt in range(4):
        try:
            t = time.time()
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                              headers={"Authorization": "Bearer " + key},
                              json={"model": model, "messages": msgs, "temperature": 0,
                                    "max_tokens": max_tokens, "usage": {"include": True}},
                              timeout=90)
            r.raise_for_status()
            d = r.json()
            u = d.get("usage", {})
            return {"answer": (d["choices"][0]["message"]["content"] or "").strip().lower(),
                    "tokens_in": u.get("prompt_tokens", 0), "tokens_out": u.get("completion_tokens", 0),
                    "cost_usd": float(u.get("cost", 0) or 0), "latency_s": round(time.time() - t, 3)}
        except Exception as e:
            print("  retry", attempt + 1, model, str(e)[:80])
            time.sleep(4 * (attempt + 1))
    return {"answer": "", "tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0, "latency_s": 0.0}


def parse(answer):
    if "phish" in answer or "spam" in answer or "malicious" in answer:
        return 1
    if "legit" in answer:
        return 0
    return -1   # unparsed, counted as legitimate later and reported separately


VERDICT = re.compile(r"\b(phishing|legitimate|spam|scam|malicious|fraudulent|not phishing)\b")


def parse_long(answer):
    """Last verdict word in the answer, ignoring the question being repeated back."""
    a = re.sub(r"(phishing|malicious[^.]*?)\s+or\s+legitimate|legitimate\s+or\s+(phishing|malicious)", " ", answer)
    hits = VERDICT.findall(a)
    if not hits:
        return -1
    return 0 if hits[-1] in ("legitimate", "not phishing") else 1


def run(model, mode, key, workers=WORKERS):
    os.makedirs(RAW_DIR, exist_ok=True)
    out = os.path.join(RAW_DIR, f"{model.replace('/', '__')}__{mode}.csv")
    done = pd.read_csv(out) if os.path.exists(out) else pd.DataFrame(columns=["id", "tokens_in"])
    # a call that failed after all retries has zero tokens, it is tried again
    done = done[done["tokens_in"] > 0]
    done_ids = set(done["id"])
    rows = done.to_dict("records")

    for source in ALL_SOURCES:
        ev = load_eval(source)
        todo = ev[~ev["id"].isin(done_ids)]
        if todo.empty:
            continue
        if spent() > BUDGET_USD:
            print("budget reached, stopping"); break
        prefix = few_shot_messages(source) if mode == "few" else [{"role": "system", "content": INSTRUCTION}]
        max_tokens = 80 if mode == "long" else 5
        with ThreadPoolExecutor(max_workers=workers) as pool:
            res = list(pool.map(lambda t: ask(key, model, prefix, t, max_tokens), todo["text"]))
        for (_, e), r in zip(todo.iterrows(), res):
            r.update({"id": e["id"], "source": source, "label": e["label"],
                      "model": model, "mode": mode,
                      "pred_raw": parse_long(r["answer"]) if mode == "long" else parse(r["answer"])})
            rows.append(r)
        total = add_spend(sum(r["cost_usd"] for r in res))
        pd.DataFrame(rows).to_csv(out, index=False)
        print(f"{model} {mode} {source}: {len(todo)} emails, total spend ${total:.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["zero", "few", "long"], default="zero")
    ap.add_argument("--models", default="all")
    ap.add_argument("--workers", type=int, default=WORKERS)
    a = ap.parse_args()
    models = MODELS if a.models == "all" else a.models.split(",")
    key = api_key()
    for m in models:
        run(m, a.mode, key, a.workers)
    print("done. total spend $%.4f" % spent())


if __name__ == "__main__":
    main()
