"""
Step 15. Are the reasons the models give any good?

Objective 5 of our proposal. Accuracy says whether a verdict is right; it says
nothing about whether the stated reason is real. Kuikel et al. found that the
most accurate model is not the one with the most faithful explanations, so we
check ours.

We sample 100 emails, ask two small models for a verdict plus one sentence of
reasoning, and then have a stronger model judge each reason on two questions:
  grounded  : does the reason point at something that is actually in the email?
  supports  : does the reason support the verdict the model gave?
We also write a small file of examples for the team to read by hand, because a
judge model checking another model is not the last word.

Writes results/final/explanations.csv, explanations_summary.csv
       results/final/explanations_sample.md   (for human reading)
"""

import os
import random
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from common import RESULTS_DIR, SEED, TRAIN_CORPORA, load_eval
import progress

import importlib.util
_s = importlib.util.spec_from_file_location("llm", os.path.join(os.path.dirname(__file__), "05_llm_eval.py"))
llm = importlib.util.module_from_spec(_s)
_s.loader.exec_module(llm)

MODELS = ["qwen/qwen-2.5-7b-instruct", "google/gemma-3-12b-it"]
JUDGE = "google/gemini-3.1-flash-lite"
PER_CORPUS = 10          # 5 phishing, 5 legitimate
AI_N = 40
RAW = os.path.join(RESULTS_DIR, "explanations.csv")

ASK = ("You are an email security assistant. Decide if the email below is malicious or "
       "unwanted (phishing, scam or spam) or legitimate. Answer in this format:\n"
       "verdict: <phishing or legitimate>\nreason: <one short sentence>")

JUDGE_PROMPT = (
    "You are checking the quality of a reason given by an email classifier.\n"
    "Answer with exactly two words separated by a space.\n"
    "First word: grounded if the reason points at something that really appears in the email, "
    "ungrounded if it invents details or is generic boilerplate.\n"
    "Second word: supports if the reason supports the stated verdict, contradicts otherwise.")


def sample_emails():
    rows = []
    rnd = random.Random(SEED)
    for src in TRAIN_CORPORA:
        ev = load_eval(src)
        for label in [1, 0]:
            pool = ev[ev.label == label]
            for _, e in pool.sample(n=PER_CORPUS // 2, random_state=SEED).iterrows():
                rows.append({"id": e["id"], "source": src, "label": label, "text": e["text"]})
    ev = load_eval("ephishllm")
    for label in [1, 0]:
        for _, e in ev[ev.label == label].sample(n=AI_N // 2, random_state=SEED).iterrows():
            rows.append({"id": e["id"], "source": "ephishllm", "label": label, "text": e["text"]})
    rnd.shuffle(rows)
    return rows


def parse_reply(text):
    verdict, reason = "", ""
    for line in str(text).splitlines():
        low = line.lower().strip()
        if low.startswith("verdict:"):
            verdict = low.split(":", 1)[1].strip()
        elif low.startswith("reason:"):
            reason = line.split(":", 1)[1].strip()
    if not verdict:
        verdict = " ".join(str(text).lower().split())[:20]
    return verdict, reason


def main():
    key = llm.api_key()
    rows = sample_emails()
    done = pd.read_csv(RAW) if os.path.exists(RAW) else pd.DataFrame(columns=["id", "model"])
    records = done.to_dict("records")

    for model in MODELS:
        have = set(done[done.model == model]["id"]) if len(done) else set()
        todo = [r for r in rows if r["id"] not in have]
        if not todo:
            continue
        print(f"{model}: {len(todo)} emails", flush=True)
        with ThreadPoolExecutor(max_workers=6) as pool:
            res = list(pool.map(lambda r: llm.ask(key, model,
                                                  [{"role": "system", "content": ASK}],
                                                  r["text"], max_tokens=70), todo))
        for r, a in zip(todo, res):
            v, reason = parse_reply(a["answer"])
            records.append({"id": r["id"], "source": r["source"], "label": r["label"],
                            "model": model, "verdict": v, "reason": reason,
                            "pred": max(llm.parse(v), 0), "cost_usd": a["cost_usd"]})
        pd.DataFrame(records).to_csv(RAW, index=False)
        llm.add_spend(sum(x["cost_usd"] for x in records if x["model"] == model))

    d = pd.DataFrame(records)
    text_of = {r["id"]: r["text"] for r in rows}
    for col in ("grounded", "supports"):
        if col not in d.columns:
            d[col] = pd.NA
    need = d[d["grounded"].isna()]
    if len(need):
        print(f"judging {len(need)} explanations", flush=True)
        def judge(r):
            msg = (f"EMAIL:\n{text_of.get(r['id'], '')[:1200]}\n\n"
                   f"VERDICT: {r['verdict']}\nREASON: {r['reason']}")
            return llm.ask(key, JUDGE, [{"role": "system", "content": JUDGE_PROMPT}], msg, max_tokens=12)
        with ThreadPoolExecutor(max_workers=6) as pool:
            res = list(pool.map(judge, need.to_dict("records")))
        grounded, supports, raw, cost = [], [], [], 0.0
        for a in res:
            ans = " ".join(str(a["answer"]).lower().split())
            raw.append(ans)
            grounded.append("ungrounded" not in ans and "grounded" in ans)
            supports.append("support" in ans and "contradict" not in ans)
            cost += a["cost_usd"]
        d.loc[need.index, "grounded"] = [float(x) for x in grounded]
        d.loc[need.index, "supports"] = [float(x) for x in supports]
        d.loc[need.index, "judge_answer"] = raw
        d.to_csv(RAW, index=False)
        llm.add_spend(cost)

    for col in ("grounded", "supports"):
        d[col] = pd.to_numeric(d[col], errors="coerce")
    d["correct"] = (d.pred == d.label)
    d["has_reason"] = d.reason.fillna("").str.len() > 10
    summary = d.groupby("model").agg(n=("id", "size"), accuracy=("correct", "mean"),
                                     gave_reason=("has_reason", "mean"),
                                     grounded=("grounded", "mean"),
                                     supports_verdict=("supports", "mean")).round(3).reset_index()
    wrong = d[~d.correct].groupby("model")["grounded"].mean().round(3)
    summary["grounded_when_wrong"] = summary.model.map(wrong)
    summary.to_csv(os.path.join(RESULTS_DIR, "explanations_summary.csv"), index=False)
    print(summary.to_string(index=False))

    with open(os.path.join(RESULTS_DIR, "explanations_sample.md"), "w") as f:
        f.write("# Explanations to read by hand\n\nTwelve cases, half of them wrong verdicts.\n\n")
        pick = pd.concat([d[~d.correct].head(6), d[d.correct].head(6)])
        for _, r in pick.iterrows():
            f.write(f"## {r['source']} · {r['model'].split('/')[-1]} · "
                    f"true label {'phishing' if r['label'] else 'legitimate'} · "
                    f"said {r['verdict']} ({'correct' if r['correct'] else 'wrong'})\n\n"
                    f"reason: {r['reason']}\n\njudge: grounded={r.get('grounded')}, supports={r.get('supports')}\n\n"
                    f"email: {str(text_of.get(r['id'], ''))[:400]}\n\n---\n\n")
    progress.mark("15_explanations", f"{len(d)} explanations judged")


if __name__ == "__main__":
    main()
