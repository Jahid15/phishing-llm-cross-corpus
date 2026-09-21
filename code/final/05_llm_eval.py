"""
Step 5. Small open LLMs through OpenRouter, zero-shot and few-shot.

Every model reads the same fixed evaluation subsets (data/final/eval_*.csv),
so the LLM numbers are directly comparable with the classical and DistilBERT
numbers computed on the same emails.

An LLM never trains on our corpora, so every test set is unseen for it.
Few-shot examples for a test corpus are always taken from the OTHER sources,
the same leave-one-corpus-out rule the trained models follow.

Few-shot example pools (mode names):
  few      four examples from the other legacy corpora (2002 to 2008 style mail)
  few_ai   four examples of AI-written mail from E-PhishLLM, never the emails
           used for evaluation
  few_mix  two legacy and two AI-written examples
This is how we test whether the examples themselves, and not few-shot
prompting as such, are what changes behaviour on AI-written phishing.

The dollar cost is the real cost OpenRouter reports for each call
(usage.cost), not an estimate from the price list. A hard budget stops the
run before it goes over.

Usage
  python 05_llm_eval.py --mode zero --models all
  python 05_llm_eval.py --mode few  --models meta-llama/llama-3.2-3b-instruct
  python 05_llm_eval.py --mode few_ai --models qwen/qwen-2.5-7b-instruct
  python 05_llm_eval.py --mode zero --models google/gemini-3.1-flash-lite --sources ephishllm_it,ephishllm_de
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

from common import EVAL_SETS, RESULTS_DIR, ROOT, SEED, TRAIN_CORPORA, load, load_eval

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
BUDGET_USD = 3.00     # total project spend allowed, checked before each test set
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


def _pick(source, label, seed, exclude_ids=()):
    df = load(source)
    df = df[(df.label == label) & (df.text.str.len().between(150, 600)) & (~df.id.isin(exclude_ids))]
    return df.sample(n=1, random_state=seed).text.iat[0]


def few_shot_messages(test_source, kind="few"):
    """Four short examples, two positive and two negative, never from the test set."""
    legacy = [c for c in TRAIN_CORPORA if c != test_source]
    ai_source = "ephishllm"
    ai_exclude = set(load_eval("ephishllm").id) | set(load_eval("ephishllm_it").id) | set(load_eval("ephishllm_de").id)
    examples = []
    for i, label in enumerate([1, 0, 1, 0]):
        if kind == "few" or (kind == "few_mix" and i < 2):
            examples.append((_pick(legacy[i % len(legacy)], label, SEED + i), label))
        else:
            examples.append((_pick(ai_source, label, SEED + i, ai_exclude), label))
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
            if "choices" not in d:
                # some providers answer 200 with an error body, for example when
                # they are rate limited; treat it as a retryable failure
                raise RuntimeError(str(d.get("error", d))[:120])
            u = d.get("usage", {})
            return {"answer": (d["choices"][0]["message"]["content"] or "").strip().lower(),
                    "tokens_in": u.get("prompt_tokens", 0), "tokens_out": u.get("completion_tokens", 0),
                    "cost_usd": float(u.get("cost", 0) or 0), "latency_s": round(time.time() - t, 3)}
        except Exception as e:
            print("  retry", attempt + 1, model, str(e)[:80])
            time.sleep(4 * (attempt + 1))
    return {"answer": "", "tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0, "latency_s": 0.0}


def parse(answer):
    """Read a one-word verdict.

    Two things this has to survive. Some models answer with a negation
    ("not phishing"), so the negative cases are checked first. Some providers
    cut the answer to a single token, so Gemini replies "ph" or "leg" rather
    than the whole word; a prefix is enough to know what it meant.
    """
    a = " ".join(str(answer).lower().split())
    if not a:
        return -1
    if a.startswith("not ") or "not phishing" in a or "not spam" in a or "not malicious" in a:
        return 0
    if a.startswith("leg") or "legit" in a or "benign" in a or "safe" in a:
        return 0
    if a.startswith("ph") or "phish" in a or a.startswith("spam") or "malicious" in a or a.startswith("mal"):
        return 1
    return -1   # no verdict given, counted as legitimate later and reported separately


VERDICT = re.compile(r"\b(phishing|legitimate|spam|scam|malicious|fraudulent|not phishing)\b")


def parse_long(answer):
    """Last verdict word in the answer, ignoring the question being repeated back."""
    a = re.sub(r"(phishing|malicious[^.]*?)\s+or\s+legitimate|legitimate\s+or\s+(phishing|malicious)", " ", answer)
    hits = VERDICT.findall(a)
    if not hits:
        return -1
    return 0 if hits[-1] in ("legitimate", "not phishing") else 1


def run(model, mode, key, workers=WORKERS, sources=None):
    os.makedirs(RAW_DIR, exist_ok=True)
    out = os.path.join(RAW_DIR, f"{model.replace('/', '__')}__{mode}.csv")
    done = pd.read_csv(out) if os.path.exists(out) else pd.DataFrame(columns=["id", "source", "tokens_in"])
    # a call that failed after all retries has zero tokens, it is tried again
    done = done[done["tokens_in"] > 0]
    # keyed by (test set, id): the sanitised copies of a test set reuse the ids
    # of the original, so an id on its own is not unique
    done_keys = set(zip(done["source"], done["id"])) if len(done) else set()
    rows = done.to_dict("records")

    for source in (sources or EVAL_SETS):
        ev = load_eval(source)
        todo = ev[[(source, i) not in done_keys for i in ev["id"]]]
        if todo.empty:
            continue
        if spent() > BUDGET_USD:
            print("budget reached, stopping"); break
        prefix = ([{"role": "system", "content": INSTRUCTION}] if mode in ("zero", "long")
                  else few_shot_messages(source, mode))
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
    ap.add_argument("--mode", choices=["zero", "few", "few_ai", "few_mix", "long"], default="zero")
    ap.add_argument("--models", default="all")
    ap.add_argument("--workers", type=int, default=WORKERS)
    ap.add_argument("--sources", default="", help="comma separated test sets, default all")
    a = ap.parse_args()
    models = MODELS if a.models == "all" else a.models.split(",")
    key = api_key()
    for m in models:
        run(m, a.mode, key, a.workers, a.sources.split(",") if a.sources else None)
    print("done. total spend $%.4f" % spent())


if __name__ == "__main__":
    main()
