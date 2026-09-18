"""
Step 6. Put everything together.

Reads the predictions of every model on the shared evaluation subsets and
produces
  results/final/per_source_metrics.csv   every model x setting x test set
  results/final/main_table.csv           the "one honest table"
  results/final/inflation.csv            loco_raw vs loco_clean for classical models
  results/final/figures/*.png

95% confidence intervals come from 1,000 bootstrap resamples of the emails
inside each test set.
"""

import glob
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score

from common import EXTRA_TESTS, FIG_DIR, RESULTS_DIR, SEED, TRAIN_CORPORA

rng = np.random.default_rng(SEED)
B = 1000

SHORT = {
    "meta-llama/llama-3.2-1b-instruct": "Llama-3.2-1B",
    "meta-llama/llama-3.2-3b-instruct": "Llama-3.2-3B",
    "meta-llama/llama-3.1-8b-instruct": "Llama-3.1-8B",
    "qwen/qwen-2.5-7b-instruct": "Qwen-2.5-7B",
    "google/gemma-3-12b-it": "Gemma-3-12B",
    "microsoft/phi-4": "Phi-4-14B",
    "logreg": "TF-IDF + LogReg",
    "naive_bayes": "TF-IDF + NB",
    "distilbert": "DistilBERT",
}
PARAMS_B = {"Llama-3.2-1B": 1, "Llama-3.2-3B": 3, "Llama-3.1-8B": 8, "Qwen-2.5-7B": 7,
            "Gemma-3-12B": 12, "Phi-4-14B": 14}


def load_preds():
    frames = []
    for f in [os.path.join(RESULTS_DIR, "preds", "classical.csv"),
              os.path.join(RESULTS_DIR, "preds", "distilbert.csv")]:
        if os.path.exists(f):
            frames.append(pd.read_csv(f))
    llm_cost = {}
    for f in glob.glob(os.path.join(RESULTS_DIR, "llm_raw", "*.csv")):
        d = pd.read_csv(f)
        d["answer"] = d["answer"].fillna("")
        d["unparsed"] = (d["pred_raw"] == -1).astype(int)
        d["pred"] = d["pred_raw"].clip(lower=0)
        mode = d["mode"].iat[0]
        name = d["model"].iat[0]
        d["model"] = name + {"zero": "", "few": " (few-shot)", "long": " (relaxed)"}[mode]
        d["setting"] = "llm_" + mode
        llm_cost[d["model"].iat[0]] = {
            "usd_per_1000": d["cost_usd"].sum() / len(d) * 1000,
            "total_usd": d["cost_usd"].sum(), "calls": len(d),
            "unparsed_pct": 100 * d["unparsed"].mean(),
            "median_latency_s": d["latency_s"].median(),
            "tokens_in_mean": d["tokens_in"].mean()}
        frames.append(d[["model", "setting", "source", "id", "label", "pred", "unparsed"]])
    return pd.concat(frames, ignore_index=True), llm_cost


def metrics(y, p):
    return {"accuracy": accuracy_score(y, p),
            "precision": precision_score(y, p, zero_division=0),
            "recall": recall_score(y, p, zero_division=0),
            "f1": f1_score(y, p, zero_division=0)}


def boot_mean_f1(groups):
    """groups: list of (y, p) arrays, one per test set. CI of the mean F1."""
    vals = []
    for _ in range(B):
        fs = []
        for y, p in groups:
            i = rng.integers(0, len(y), len(y))
            fs.append(f1_score(y[i], p[i], zero_division=0))
        vals.append(np.mean(fs))
    return np.percentile(vals, [2.5, 97.5])


def pretty(m):
    base = m.replace(" (few-shot)", "").replace(" (relaxed)", "")
    suffix = " few-shot" if "few-shot" in m else (" relaxed" if "relaxed" in m else "")
    return SHORT.get(base, base) + suffix


def main():
    preds, llm_cost = load_preds()
    preds["name"] = preds["model"].map(pretty)

    # per source metrics
    rows = []
    for (name, setting, src), g in preds.groupby(["name", "setting", "source"]):
        rows.append({"model": name, "setting": setting, "test": src, "n": len(g),
                     **{k: round(v, 4) for k, v in metrics(g.label, g.pred).items()}})
    per = pd.DataFrame(rows)
    per.to_csv(os.path.join(RESULTS_DIR, "per_source_metrics.csv"), index=False)

    # classical in-corpus numbers come from the 80/20 split in 03
    cl = pd.read_csv(os.path.join(RESULTS_DIR, "classical_loco.csv"))
    cl["model"] = cl["model"].map(SHORT)

    # the main table
    main_rows = []
    settings = {"TF-IDF + LogReg": "loco_clean", "TF-IDF + NB": "loco_clean",
                "DistilBERT": "loco_clean"}
    for name in preds["name"].unique():
        setting = settings.get(name, "llm_few" if "few-shot" in name else
                               ("llm_long" if "relaxed" in name else "llm_zero"))
        g = preds[(preds.name == name) & (preds.setting == setting)]
        unseen = [(s.label.values, s.pred.values) for _, s in g[g.source.isin(TRAIN_CORPORA)].groupby("source")]
        if len(unseen) < len(TRAIN_CORPORA):
            continue
        f1s = [f1_score(y, p, zero_division=0) for y, p in unseen]
        lo, hi = boot_mean_f1(unseen)
        if name in ("TF-IDF + LogReg", "TF-IDF + NB"):
            inc = cl[(cl.model == name) & (cl.setting == "in_corpus")]["f1"].mean()
        elif name == "DistilBERT":
            inc = per[(per.model == name) & (per.setting == "in_corpus")]["f1"].mean()
        else:
            inc = np.nan  # an LLM has no training corpus
        def m_on(src, key):
            s = g[g.source == src]
            return metrics(s.label, s.pred)[key] if len(s) else np.nan
        full = next((k for k in llm_cost if pretty(k) == name), None)
        cost = llm_cost[full]["usd_per_1000"] if full else 0.0
        main_rows.append({
            "model": name,
            "type": "LLM" if full else ("fine-tuned encoder" if name == "DistilBERT" else "classical"),
            "in_corpus_f1": round(inc, 3) if not np.isnan(inc) else "",
            "unseen_f1_mean": round(np.mean(f1s), 3),
            "unseen_f1_ci": f"{lo:.3f}-{hi:.3f}",
            "unseen_f1_worst": round(min(f1s), 3),
            "ai_phishing_f1": round(m_on("ephishllm", "f1"), 3),
            "nazario_recall": round(m_on("nazario", "recall"), 3),
            "nigerian_recall": round(m_on("nigerian", "recall"), 3),
            "usd_per_1000": round(cost, 4),
            "unparsed_pct": round(llm_cost[full]["unparsed_pct"], 1) if full else 0.0,
        })
    main = pd.DataFrame(main_rows).sort_values("unseen_f1_mean", ascending=False)
    main.to_csv(os.path.join(RESULTS_DIR, "main_table.csv"), index=False)
    print(main.to_string(index=False))

    pd.DataFrame([{"model": pretty(k), **{a: round(b, 5) for a, b in v.items()}}
                  for k, v in llm_cost.items()]).to_csv(os.path.join(RESULTS_DIR, "llm_cost.csv"), index=False)

    # inflation caused by leaked emails (classical, full test corpora)
    inf = cl[cl.setting.isin(["loco_raw", "loco_clean"])].pivot_table(
        index=["model", "test"], columns="setting", values="f1").reset_index()
    rem = cl[cl.setting == "loco_clean"][["model", "test", "removed"]]
    inf = inf.merge(rem, on=["model", "test"])
    inf["inflation"] = (inf["loco_raw"] - inf["loco_clean"]).round(4)
    inc = cl[cl.setting == "in_corpus"][["model", "test", "f1"]].rename(columns={"f1": "in_corpus"})
    inf = inf.merge(inc, on=["model", "test"], how="left")
    inf.to_csv(os.path.join(RESULTS_DIR, "inflation.csv"), index=False)
    print(inf.to_string(index=False))

    figures(per, main)


def figures(per, main):
    plt.rcParams.update({"font.size": 9, "figure.dpi": 200})

    # 1. near duplicate overlap heatmap
    ov = pd.read_csv(os.path.join(RESULTS_DIR, "overlap_matrix_near.csv"), index_col=0)
    ov = ov.loc[TRAIN_CORPORA + EXTRA_TESTS, TRAIN_CORPORA + EXTRA_TESTS]
    fig, ax = plt.subplots(figsize=(4.6, 3.8))
    im = ax.imshow(ov.values, cmap="Reds", vmin=0, vmax=100)
    ax.set_xticks(range(len(ov))); ax.set_xticklabels(ov.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(ov))); ax.set_yticklabels(ov.index)
    for i in range(len(ov)):
        for j in range(len(ov)):
            v = ov.values[i, j]
            if v >= 0.5:
                ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=7,
                        color="white" if v > 50 else "black")
    ax.set_xlabel("corpus B"); ax.set_ylabel("corpus A")
    ax.set_title("% of B with a near duplicate in A")
    fig.colorbar(im, fraction=0.046, pad=0.04)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "overlap_heatmap.png")); plt.close(fig)

    # 2. unseen corpus F1 vs cost
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    for _, r in main.iterrows():
        x = max(r.usd_per_1000, 0.001)
        c = "#d62728" if r.type == "LLM" else ("#1f77b4" if r.type == "classical" else "#2ca02c")
        ax.scatter(x, r.unseen_f1_mean, color=c, s=22, zorder=3)
        ax.annotate(r.model, (x, r.unseen_f1_mean), fontsize=6, xytext=(3, 2), textcoords="offset points")
    ax.set_xscale("log"); ax.set_xlabel("API cost, USD per 1,000 emails (local models drawn at 0.001)")
    ax.set_ylabel("mean F1 on unseen corpora"); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "f1_vs_cost.png")); plt.close(fig)

    # 3. per corpus F1 heatmap of the main models
    order = list(main.model)
    cols = TRAIN_CORPORA + ["ephishllm"]
    mat = []
    for name in order:
        setting_rows = per[(per.model == name) & (per.setting.isin(["loco_clean", "llm_zero", "llm_few", "llm_long"]))]
        mat.append([setting_rows[setting_rows.test == c]["f1"].mean() for c in cols])
    mat = np.array(mat)
    fig, ax = plt.subplots(figsize=(4.8, 0.28 * len(order) + 1.0))
    im = ax.imshow(mat, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=45, ha="right")
    ax.set_yticks(range(len(order))); ax.set_yticklabels(order)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", fontsize=6)
    ax.set_title("F1 on each held-out test set")
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "per_corpus_f1.png")); plt.close(fig)

    # 4. in-corpus vs unseen for trained models
    inf = pd.read_csv(os.path.join(RESULTS_DIR, "inflation.csv"))
    lr = inf[inf.model == "TF-IDF + LogReg"].set_index("test").loc[TRAIN_CORPORA]
    x = np.arange(len(lr)); w = 0.27
    fig, ax = plt.subplots(figsize=(4.8, 2.6))
    ax.bar(x - w, lr.in_corpus, w, label="in-corpus (80/20)", color="#9ecae1")
    ax.bar(x, lr.loco_raw, w, label="unseen, raw training", color="#fc9272")
    ax.bar(x + w, lr.loco_clean, w, label="unseen, decontaminated", color="#de2d26")
    ax.set_xticks(x); ax.set_xticklabels(lr.index, rotation=30, ha="right")
    ax.set_ylabel("F1"); ax.set_ylim(0, 1.05); ax.legend(fontsize=6, loc="lower left")
    ax.set_title("TF-IDF + LogReg")
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "incorpus_vs_unseen.png")); plt.close(fig)
    print("figures saved")


if __name__ == "__main__":
    main()
