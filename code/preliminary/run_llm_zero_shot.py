"""
Zero shot phishing classification with small open LLMs through OpenRouter.
Takes a balanced random sample from each dataset, asks each model to answer
phishing or legitimate, and tracks accuracy and token usage.

The API key is read from a .env file in the project root (OPENROUTER_API_KEY=...)
or from the environment. With the default models and 100 emails per dataset
the whole run costs only a few cents.

Writes results/llm_zero_shot_predictions.csv and results/llm_zero_shot_summary.csv
"""

import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests
from sklearn.metrics import accuracy_score, f1_score

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "preliminary")

DATASETS = ["kaggle", "spamassassin", "nazario_enron"]
SAMPLES_PER_DATASET = 100
MAX_CHARS = 1500
WORKERS = 6

# dollars per million tokens, taken from openrouter.ai/models, only used for the estimate
MODELS = {
    "meta-llama/llama-3.2-3b-instruct": (0.02, 0.04),
    "google/gemma-3-12b-it": (0.05, 0.10),
}

PROMPT = ("You are an email security assistant. Decide if the following email is a "
          "phishing email or a legitimate email. Answer with exactly one word: "
          "phishing or legitimate.\n\nEmail:\n{email}")


def load_api_key():
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1]
    return None


def ask_model(api_key, model, email_text):
    for attempt in range(3):
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": "Bearer " + api_key},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": PROMPT.format(email=email_text)}],
                    "temperature": 0,
                    "max_tokens": 8,
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            answer = data["choices"][0]["message"]["content"].strip().lower()
            usage = data.get("usage", {})
            return answer, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
        except Exception as e:
            print("retry", attempt + 1, e)
            time.sleep(3)
    return "", 0, 0


def main():
    api_key = load_api_key()
    if not api_key:
        print("No OPENROUTER_API_KEY found in the environment or .env, skipping.")
        sys.exit(1)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    all_rows = []
    summary_rows = []

    for model, (price_in, price_out) in MODELS.items():
        total_in, total_out, n_emails = 0, 0, 0
        for name in DATASETS:
            df = pd.read_csv(os.path.join(DATA_DIR, name + ".csv"))
            n = SAMPLES_PER_DATASET // 2
            sample = pd.concat([
                df[df["label"] == 1].sample(n=n, random_state=42),
                df[df["label"] == 0].sample(n=n, random_state=42),
            ]).reset_index(drop=True)

            texts = [t[:MAX_CHARS] for t in sample["text"]]
            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                answers = list(pool.map(lambda t: ask_model(api_key, model, t), texts))

            preds = []
            for (answer, tok_in, tok_out), true_label in zip(answers, sample["label"]):
                total_in += tok_in
                total_out += tok_out
                pred = 1 if "phish" in answer else 0
                preds.append(pred)
                all_rows.append({"model": model, "dataset": name,
                                 "true_label": true_label, "prediction": pred,
                                 "raw_answer": answer})
            n_emails += len(preds)

            acc = accuracy_score(sample["label"], preds)
            f1 = f1_score(sample["label"], preds, pos_label=1)
            summary_rows.append({"model": model, "dataset": name,
                                 "samples": len(sample),
                                 "accuracy": round(acc, 4), "f1": round(f1, 4)})
            print(model, name, "acc", round(acc, 4), "f1", round(f1, 4))

        cost = total_in / 1e6 * price_in + total_out / 1e6 * price_out
        for row in summary_rows:
            if row["model"] == model and "est_cost_usd_per_1000_emails" not in row:
                row["est_cost_usd_per_1000_emails"] = round(cost / n_emails * 1000, 4)
        print(model, "tokens in", total_in, "out", total_out,
              "estimated cost $", round(cost, 4))

    pd.DataFrame(all_rows).to_csv(
        os.path.join(RESULTS_DIR, "llm_zero_shot_predictions.csv"), index=False)
    pd.DataFrame(summary_rows).to_csv(
        os.path.join(RESULTS_DIR, "llm_zero_shot_summary.csv"), index=False)
    print("saved results/llm_zero_shot_predictions.csv and results/llm_zero_shot_summary.csv")


if __name__ == "__main__":
    main()
