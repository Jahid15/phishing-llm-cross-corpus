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

B = 1000
_BOOT_IDX = {}


def boot_index(n):
    """The same resample positions for every model, so model comparisons are paired."""
    if n not in _BOOT_IDX:
        _BOOT_IDX[n] = np.random.default_rng(SEED).integers(0, n, size=(B, n))
    return _BOOT_IDX[n]

SHORT = {
    "meta-llama/llama-3.2-1b-instruct": "Llama-3.2-1B",
    "meta-llama/llama-3.2-3b-instruct": "Llama-3.2-3B",
    "meta-llama/llama-3.1-8b-instruct": "Llama-3.1-8B",
    "qwen/qwen-2.5-7b-instruct": "Qwen-2.5-7B",
    "google/gemma-3-12b-it": "Gemma-3-12B",
    "microsoft/phi-4": "Phi-4-14B",
    "google/gemini-3.1-flash-lite": "Gemini-3.1-Flash-Lite",
    "openai/gpt-4o-mini": "GPT-4o-mini",
    "bert": "BERT-phishing (published)",
    "modernbert": "ModernBERT-phishing (published)",
    "phishsense": "Phishsense-1B (published)",
    "logreg": "TF-IDF + LogReg",
    "naive_bayes": "TF-IDF + NB",
    "distilbert": "DistilBERT",
}
FRONTIER = {"Gemini-3.1-Flash-Lite", "GPT-4o-mini"}
PUBLISHED = {"BERT-phishing (published)", "ModernBERT-phishing (published)", "Phishsense-1B (published)"}
PARAMS_B = {"Llama-3.2-1B": 1, "Llama-3.2-3B": 3, "Llama-3.1-8B": 8, "Qwen-2.5-7B": 7,
            "Gemma-3-12B": 12, "Phi-4-14B": 14}


def load_preds():
    frames = []
    for f in [os.path.join(RESULTS_DIR, "preds", "classical.csv"),
              os.path.join(RESULTS_DIR, "preds", "distilbert.csv"),
              os.path.join(RESULTS_DIR, "preds", "offtheshelf.csv")]:
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
        suffix = {"zero": "", "few": " (few-shot)", "few_ai": " (few-shot AI)",
                  "few_mix": " (few-shot mixed)", "long": " (relaxed)"}[mode]
        d["model"] = name + suffix
        d["setting"] = "llm_" + mode
        six = d[d.source.isin(TRAIN_CORPORA)]
        llm_cost[d["model"].iat[0]] = {
            # measured on the same six corpora the F1 column uses
            "usd_per_1000": (six["cost_usd"].sum() / len(six) * 1000) if len(six) else
                            (d["cost_usd"].sum() / len(d) * 1000),
            "usd_per_1000_all_sets": d["cost_usd"].sum() / len(d) * 1000,
            "total_usd": d["cost_usd"].sum(), "calls": len(d),
            "unparsed_pct": 100 * d["unparsed"].mean(),
            "api_failed": int((d["tokens_in"] == 0).sum()),
            "median_latency_s": d["latency_s"].median(),
            "tokens_in_mean": d["tokens_in"].mean()}
        frames.append(d[["model", "setting", "source", "id", "label", "pred", "unparsed"]])
    return pd.concat(frames, ignore_index=True), llm_cost


def metrics(y, p):
    return {"accuracy": accuracy_score(y, p),
            "precision": precision_score(y, p, zero_division=0),
            "recall": recall_score(y, p, zero_division=0),
            "f1": f1_score(y, p, zero_division=0)}


def boot_samples(groups):
    """Bootstrap distribution of the mean F1 over the held-out corpora.

    The resample positions come from boot_index, so two models are always
    compared on the same resampled emails and the difference between them can
    be given its own interval.
    """
    vals = np.zeros(B)
    for b in range(B):
        fs = []
        for y, p in groups:
            i = boot_index(len(y))[b]
            fs.append(f1_score(y[i], p[i], zero_division=0))
        vals[b] = np.mean(fs)
    return vals


def boot_mean_f1(groups):
    v = boot_samples(groups)
    return np.percentile(v, [2.5, 97.5])


def corpus_jackknife(f1s):
    """Leave one corpus out of the average, to show how much one corpus moves it.

    The bootstrap above treats the six corpora as fixed and only resamples
    emails inside them. The spread that matters for "a corpus we have never
    seen" is the spread between corpora, which is what this reports.
    """
    f1s = np.asarray(f1s)
    means = [np.mean(np.delete(f1s, k)) for k in range(len(f1s))]
    return float(np.min(means)), float(np.max(means))


def pretty(m):
    base = m
    for tag in [" (few-shot AI)", " (few-shot mixed)", " (few-shot)", " (relaxed)"]:
        base = base.replace(tag, "")
    suffix = ("" if base == m else
              {" (few-shot)": " few-shot", " (few-shot AI)": " few-shot AI",
               " (few-shot mixed)": " few-shot mixed", " (relaxed)": " relaxed"}[m[len(base):]])
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
    boot_by_model = {}
    settings = {"TF-IDF + LogReg": "loco_clean", "TF-IDF + NB": "loco_clean",
                "DistilBERT": "loco_clean"}
    for n in PUBLISHED:
        settings[n] = "pretrained"
    for name in preds["name"].unique():
        if name in settings:
            setting = settings[name]
        elif "few-shot AI" in name:
            setting = "llm_few_ai"
        elif "few-shot mixed" in name:
            setting = "llm_few_mix"
        elif "few-shot" in name:
            setting = "llm_few"
        elif "relaxed" in name:
            setting = "llm_long"
        else:
            setting = "llm_zero"
        g = preds[(preds.name == name) & (preds.setting == setting)]
        unseen = [(s.label.values, s.pred.values) for _, s in g[g.source.isin(TRAIN_CORPORA)].groupby("source")]
        if len(unseen) < len(TRAIN_CORPORA):
            continue
        f1s = [f1_score(y, p, zero_division=0) for y, p in unseen]
        # false alarm rate: share of legitimate emails flagged, mean over the six unseen corpora
        fprs = [((p == 1) & (y == 0)).sum() / max(1, (y == 0).sum()) for y, p in unseen]
        lo, hi = boot_mean_f1(unseen)
        jk_lo, jk_hi = corpus_jackknife(f1s)
        boot_by_model[name] = boot_samples(unseen)
        # in-corpus is measured the same way for every trained model: train on the
        # corpus minus the evaluation subset, test on that subset
        rows_inc = per[(per.model == name) & (per.setting == "in_corpus")]
        inc = rows_inc["f1"].mean() if len(rows_inc) else np.nan  # an LLM has no training corpus
        def m_on(src, key):
            s = g[g.source == src]
            return metrics(s.label, s.pred)[key] if len(s) else np.nan
        full = next((k for k in llm_cost if pretty(k) == name), None)
        cost = llm_cost[full]["usd_per_1000"] if full else 0.0
        main_rows.append({
            "model": name,
            "type": ("frontier LLM" if name.split(" few")[0] in FRONTIER else
                     "published detector" if name in PUBLISHED else
                     "small LLM" if full else
                     "fine-tuned encoder" if name == "DistilBERT" else "classical"),
            "in_corpus_f1": round(inc, 3) if not np.isnan(inc) else "",
            "unseen_f1_mean": round(np.mean(f1s), 3),
            "unseen_f1_ci": f"{lo:.3f}-{hi:.3f}",
            "unseen_f1_jackknife": f"{jk_lo:.3f}-{jk_hi:.3f}",
            "unseen_f1_worst": round(min(f1s), 3),
            "false_alarm_rate": round(float(np.mean(fprs)), 3),
            "false_alarm_worst": round(float(np.max(fprs)), 3),
            "ai_phishing_f1": round(m_on("ephishllm", "f1"), 3),
            "nazario_recall": round(m_on("nazario", "recall"), 3),
            "nigerian_recall": round(m_on("nigerian", "recall"), 3),
            "usd_per_1000": round(cost, 4),
            "unparsed_pct": round(llm_cost[full]["unparsed_pct"], 1) if full else 0.0,
        })
    main = pd.DataFrame(main_rows).sort_values("unseen_f1_mean", ascending=False)
    main.to_csv(os.path.join(RESULTS_DIR, "main_table.csv"), index=False)
    print(main.to_string(index=False))

    # paired bootstrap intervals for the differences the paper talks about
    pairs = [("Qwen-2.5-7B", "TF-IDF + LogReg"), ("Qwen-2.5-7B", "DistilBERT"),
             ("Qwen-2.5-7B few-shot", "Qwen-2.5-7B"), ("Gemma-3-12B", "Qwen-2.5-7B"),
             ("Gemini-3.1-Flash-Lite", "Qwen-2.5-7B")]
    diff_rows = []
    for a, b in pairs:
        if a in boot_by_model and b in boot_by_model:
            d = boot_by_model[a] - boot_by_model[b]
            lo_d, hi_d = np.percentile(d, [2.5, 97.5])
            diff_rows.append({"model_a": a, "model_b": b, "mean_difference": round(float(d.mean()), 4),
                              "ci_low": round(float(lo_d), 4), "ci_high": round(float(hi_d), 4),
                              "excludes_zero": bool(lo_d > 0 or hi_d < 0)})
    pd.DataFrame(diff_rows).to_csv(os.path.join(RESULTS_DIR, "paired_differences.csv"), index=False)
    if diff_rows:
        print(pd.DataFrame(diff_rows).to_string(index=False))

    pd.DataFrame([{"model": pretty(k), **{a: round(b, 5) for a, b in v.items()}}
                  for k, v in llm_cost.items()]).to_csv(os.path.join(RESULTS_DIR, "llm_cost.csv"), index=False)

    # inflation caused by leaked emails (classical, full test corpora)
    inf = cl[cl.setting.isin(["loco_raw", "loco_clean"])].pivot_table(
        index=["model", "test"], columns="setting", values="f1").reset_index()
    rem = cl[cl.setting == "loco_clean"][["model", "test", "removed"]]
    inf = inf.merge(rem, on=["model", "test"])
    inf["inflation"] = (inf["loco_raw"] - inf["loco_clean"]).round(4)
    inc = cl[cl.setting == "in_corpus_split"][["model", "test", "f1"]].rename(columns={"f1": "in_corpus"})
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
    # hand-placed label offsets (points) so crowded labels do not overlap
    offs = {"TF-IDF + LogReg": (6, 6), "TF-IDF + NB": (6, -2), "DistilBERT": (6, -10),
            "Gemma-3-12B": (-8, 8), "Llama-3.1-8B": (-62, -4), "Qwen-2.5-7B": (-50, 4),
            "Qwen-2.5-7B few-shot": (-40, 6), "Llama-3.2-3B few-shot": (5, -2), "Llama-3.2-3B": (5, -6)}
    for _, r in main.iterrows():
        x = max(r.usd_per_1000, 0.001)
        c = {"small LLM": "#d62728", "frontier LLM": "#9467bd", "classical": "#1f77b4",
             "fine-tuned encoder": "#2ca02c", "published detector": "#ff7f0e"}.get(r.type, "#777777")
        ax.scatter(x, r.unseen_f1_mean, color=c, s=22, zorder=3)
        ax.annotate(r.model, (x, r.unseen_f1_mean), fontsize=6, xytext=offs.get(r.model, (4, 2)),
                    textcoords="offset points")
    ax.set_xlim(0.0006, 0.15)
    ax.set_ylim(top=0.965)
    ax.set_xscale("log"); ax.set_xlabel("API cost, USD per 1,000 emails (local models drawn at 0.001)")
    ax.set_ylabel("mean F1 on unseen corpora"); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(FIG_DIR, "f1_vs_cost.png")); plt.close(fig)

    # 3. per corpus F1 heatmap of the main models
    order = list(main.model)
    cols = TRAIN_CORPORA + ["ephishllm"]
    mat = []
    for name in order:
        setting_rows = per[(per.model == name) & (per.setting.isin(["loco_clean", "llm_zero", "llm_few", "llm_few_ai", "llm_few_mix", "llm_long"]))]
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
