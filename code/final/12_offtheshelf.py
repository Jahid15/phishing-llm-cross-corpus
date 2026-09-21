"""
Step 12. Published phishing detectors, used as they are shipped.

These are models other people trained and released for phishing detection. We
run them on our evaluation subsets without any fine-tuning.

Why this matters for the paper: every one of these was trained on the Kaggle
lineage that we test on (their model cards name the Kaggle phishing email set,
SpamAssassin, Enron, CEAS or Ling). So their scores on our legacy corpora are
partly a memory test, while E-PhishLLM is mail none of them can have seen. The
gap between the two is contamination made visible in released artefacts, not
just in our own training runs.

Models
  ealvaradob/bert-finetuned-phishing              BERT-large, binary head
  mikaelnurminen/modernbert-large-phishing        ModernBERT-large, binary head
  wolfCuanhamaRWS/Llama-Phishsense-merged-1B      ungated merge of Phishsense-1B,
                                                  a causal model, prompted with the
                                                  same instruction as our other LLMs
                                                  (its official template sits in a
                                                  gated repository we cannot read)

Resumable: one file per model and test set under results/final/preds/offtheshelf/.
Usage: python 12_offtheshelf.py --models bert,modernbert,phishsense --sources a,b
"""

import argparse
import glob
import os
import time

import pandas as pd
import torch

from common import EVAL_SETS, RESULTS_DIR, load_eval
import progress

OUT_DIR = os.path.join(RESULTS_DIR, "preds", "offtheshelf")
os.makedirs(OUT_DIR, exist_ok=True)
DEVICE = os.environ.get("DEVICE", "cpu")
MAX_LEN = 512
BATCH = 8

MODELS = {
    "bert": {"id": "ealvaradob/bert-finetuned-phishing", "kind": "cls"},
    "modernbert": {"id": "mikaelnurminen/modernbert-large-phishing", "kind": "cls", "eager": True},
    "phishsense": {"id": "wolfCuanhamaRWS/Llama-Phishsense-merged-1B", "kind": "causal"},
}
def causal_parse(ans, llm):
    """Phishsense answers TRUE or FALSE, as its documentation describes.
    Other causal models answer with a word, so both forms are accepted."""
    a = " ".join(str(ans).lower().split())
    if a.startswith("true"):
        return 1
    if a.startswith("false"):
        return 0
    return max(llm.parse(a), 0)


INSTRUCTION = ("You are an email security assistant. Decide if the email below is "
               "malicious or unwanted (phishing, scam or spam) or legitimate. "
               "Answer with exactly one word: phishing or legitimate.")


def positive_index(model):
    """Which output index means phishing, read from the model's own labels."""
    id2label = {int(k): str(v).lower() for k, v in (model.config.id2label or {}).items()}
    for i, lab in id2label.items():
        if "phish" in lab or "spam" in lab or lab in ("malicious", "1", "label_1"):
            return i
    return 1


@torch.no_grad()
def run_classifier(name, spec, sources):
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(spec["id"])
    kw = {"attn_implementation": "eager"} if spec.get("eager") else {}
    model = AutoModelForSequenceClassification.from_pretrained(spec["id"], **kw).to(DEVICE).eval()
    pos = positive_index(model)
    print(f"{name}: labels {model.config.id2label}, phishing index {pos}", flush=True)
    for src in sources:
        out_file = os.path.join(OUT_DIR, f"{name}__{src}.csv")
        if os.path.exists(out_file):
            continue
        ev = load_eval(src)
        preds, t0 = [], time.time()
        for i in range(0, len(ev), BATCH):
            chunk = [t[:6000] for t in ev.text.iloc[i:i + BATCH]]
            enc = tok(chunk, truncation=True, max_length=MAX_LEN, padding=True, return_tensors="pt")
            enc = {k: v.to(DEVICE) for k, v in enc.items()}
            preds += (model(**enc).logits.argmax(-1) == pos).int().cpu().tolist()
        sec = (time.time() - t0) / len(ev) * 1000
        pd.DataFrame({"model": name, "setting": "pretrained", "source": src,
                      "id": ev.id, "label": ev.label, "pred": preds,
                      "cpu_sec_per_1000": round(sec, 1)}).to_csv(out_file, index=False)
        acc = (pd.Series(preds).values == ev.label.values).mean()
        print(f"{name} {src}: acc {acc:.3f} ({sec:.0f} s per 1000)", flush=True)


@torch.no_grad()
def run_causal(name, spec, sources):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import importlib.util
    s = importlib.util.spec_from_file_location("llm", os.path.join(os.path.dirname(__file__), "05_llm_eval.py"))
    llm = importlib.util.module_from_spec(s)
    s.loader.exec_module(llm)

    tok = AutoTokenizer.from_pretrained(spec["id"])
    # half precision: a 1B model in float32 needs about 5 GB, which does not fit
    # next to the other jobs on an 8 GB laptop
    dtype = torch.float16 if DEVICE == "mps" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(spec["id"], dtype=dtype).to(DEVICE).eval()
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    for src in sources:
        out_file = os.path.join(OUT_DIR, f"{name}__{src}.csv")
        if os.path.exists(out_file):
            continue
        ev = load_eval(src)
        preds, answers, t0 = [], [], time.time()
        for text in ev.text:
            msgs = [{"role": "system", "content": INSTRUCTION},
                    {"role": "user", "content": "Email:\n" + text[:1500]}]
            try:
                prompt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            except Exception:
                prompt = INSTRUCTION + "\n\nEmail:\n" + text[:1500] + "\nAnswer:"
            enc = tok(prompt, return_tensors="pt", truncation=True, max_length=2048).to(DEVICE)
            gen = model.generate(**enc, max_new_tokens=5, do_sample=False,
                                 pad_token_id=tok.pad_token_id)
            ans = tok.decode(gen[0][enc["input_ids"].shape[1]:], skip_special_tokens=True).strip().lower()
            answers.append(ans)
            preds.append(causal_parse(ans, llm))
        sec = (time.time() - t0) / len(ev) * 1000
        pd.DataFrame({"model": name, "setting": "pretrained", "source": src,
                      "id": ev.id, "label": ev.label, "pred": preds, "answer": answers,
                      "cpu_sec_per_1000": round(sec, 1)}).to_csv(out_file, index=False)
        acc = (pd.Series(preds).values == ev.label.values).mean()
        print(f"{name} {src}: acc {acc:.3f} ({sec:.0f} s per 1000)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="bert,modernbert,phishsense")
    ap.add_argument("--sources", default="")
    a = ap.parse_args()
    sources = a.sources.split(",") if a.sources else EVAL_SETS
    for name in a.models.split(","):
        spec = MODELS[name]
        (run_causal if spec["kind"] == "causal" else run_classifier)(name, spec, sources)
    files = glob.glob(os.path.join(OUT_DIR, "*.csv"))
    pd.concat([pd.read_csv(f) for f in files], ignore_index=True).to_csv(
        os.path.join(RESULTS_DIR, "preds", "offtheshelf.csv"), index=False)
    progress.mark("12_offtheshelf", f"{len(files)} model/test-set files")


if __name__ == "__main__":
    main()
