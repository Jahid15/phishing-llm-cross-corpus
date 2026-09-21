"""
Writes every LaTeX table of the paper from results/final, so the paper can be
rebuilt from the data and cannot drift from it.
"""
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "results", "final")
NICE = {"spamassassin": "SpamAssassin", "ceas08": "CEAS-08", "trec07": "TREC-07", "ling": "Ling-Spam",
        "enron": "Enron", "kaggle": "Kaggle", "nazario": "Nazario", "nigerian": "Nigerian",
        "ephishllm": "E-PhishLLM (en)", "ephishllm_it": "E-PhishLLM (it)", "ephishllm_de": "E-PhishLLM (de)",
        "ephishllm_nolink": "E-PhishLLM, token removed", "ephishllm_url": "E-PhishLLM, token replaced"}
SIX = ["spamassassin", "ceas08", "trec07", "ling", "enron", "kaggle"]


def w(name, s):
    open(os.path.join(HERE, name), "w").write(s)


def table(caption, label, colspec, header, rows, wide=False, size="footnotesize", sep="3pt"):
    env = "table*" if wide else "table"
    return (f"\\begin{{{env}}}[t]\n\\caption{{{caption}}}\n\\label{{{label}}}\n"
            f"\\centering\\{size}\n\\setlength{{\\tabcolsep}}{{{sep}}}\n"
            f"\\begin{{tabular}}{{{colspec}}}\n\\toprule\n{header} \\\\\n\\midrule\n"
            + "\n".join(rows) + f"\n\\bottomrule\n\\end{{tabular}}\n\\end{{{env}}}\n")


# ---------------------------------------------------------------- data
st = pd.read_csv(os.path.join(R, "dataset_stats.csv"))
rows = [f"{NICE[r.source]} & {'train/test' if r.role == 'train+test' else 'test'} & {r.emails_after_cleaning:,} & "
        f"{r.emails_used:,} & {r.phishing_or_spam:,} & {r.eval_subset} \\\\" for r in st.itertuples()]
w("tab_data.tex", table("Email sources after cleaning. ``Used'' is after the 10k stratified cap. ``Eval'' is the fixed "
                        "subset every model is scored on.", "tab:data", "lrrrrr",
                        "Source & Role & Cleaned & Used & Positive & Eval", rows))

# ---------------------------------------------------------- overlap
pairs = pd.read_csv(os.path.join(R, "overlap_pairs.csv"))
within = pd.read_csv(os.path.join(R, "within_corpus_dup.csv")).set_index("source")


def get(level, a, b):
    r = pairs[(pairs.level == level) & (pairs.contains == a) & (pairs.source == b)]
    return (int(r.emails_of_source_found.iat[0]), float(r.pct_of_source.iat[0])) if len(r) else (0, 0.0)


def fmt(c, p):
    return f"{c:,} (" + ("$<$0.1" if 0 < p < 0.1 else f"{p:.1f}") + "\\%)"


lines = [f"{NICE[b]} in {NICE[a]} & " + " & ".join(fmt(*get(l, a, b)) for l in ["exact_raw", "exact_norm", "near"]) + " \\\\"
         for a, b in [("kaggle", "spamassassin"), ("kaggle", "ling"), ("kaggle", "enron"), ("enron", "kaggle"),
                      ("enron", "spamassassin"), ("trec07", "nigerian")]]
w("tab_overlap.tex", table("Emails of one corpus found inside another, at three levels of matching: exact text, exact "
                           "after removing all whitespace, and near duplicate (exact Jaccard at least 0.8). "
                           "Percentages are of the first corpus.", "tab:overlap", "lrrr",
                           "Pair & Exact & No space & Near dup.", lines, sep="2pt"))

th = pd.read_csv(os.path.join(R, "overlap_thresholds.csv"))
piv = th.pivot_table(index="source", columns="threshold", values="pct")
rows = [f"{NICE[s]} & {within.loc[s, 'corpus_internal_near_dup_pct']:.1f} & "
        f"{within.loc[s, 'eval_with_near_dup_in_own_train_pct']:.1f} & "
        + " & ".join(f"{piv.loc[s, t]:.1f}" for t in [0.7, 0.8, 0.9]) + " \\\\"
        for s in SIX + ["nazario", "nigerian", "ephishllm"]]
w("tab_within.tex", table("Duplication inside and between corpora, in percent. ``Internal'' is the share of a corpus "
                          "with a near copy elsewhere in the same corpus. ``Eval in train'' is the share of that "
                          "corpus's evaluation emails with a near copy in the part of the corpus a model trains on. "
                          "The last three columns are the share with a near copy in a different corpus, at three "
                          "Jaccard thresholds.", "tab:within", "lrrrrr",
                          "Corpus & Internal & Eval in train & $\\geq$0.7 & $\\geq$0.8 & $\\geq$0.9", rows))

# ------------------------------------------------------- inflation
inf = pd.read_csv(os.path.join(R, "classical_loco.csv"))
lr = inf[inf.model == "logreg"]
piv = lr.pivot_table(index="test", columns="setting", values="f1")
rem = lr[lr.setting == "loco_clean"].set_index("test")["removed"]
rows = []
for t in SIX:
    r = piv.loc[t]
    rows.append(f"{NICE[t]} & {int(rem[t]):,} & {r.get('in_corpus_split', float('nan')):.3f} & {r['loco_raw']:.3f} & "
                f"{r.get('loco_random', float('nan')):.3f} & {r['loco_clean']:.3f} & "
                f"{(r['loco_raw'] - r['loco_clean']) * 100:+.1f} \\\\")
w("tab_inflation.tex", table("Leave-one-corpus-out F1 of TF-IDF with logistic regression. ``Removed'' is the number of "
                             "training emails that have a near duplicate in the held-out corpus. ``Random'' is the "
                             "control that removes the same number of training emails at random. $\\Delta$ is raw minus "
                             "clean, in F1 points.", "tab:inflation", "lrrrrrr",
                             "Held out & Removed & In-corp. & Raw & Random & Clean & $\\Delta$", rows, sep="2pt"))

pw = pd.read_csv(os.path.join(R, "classical_pairwise.csv"))
ex = []
for a, b in [("kaggle", "spamassassin"), ("kaggle", "enron"), ("kaggle", "ling"), ("spamassassin", "kaggle"),
             ("spamassassin", "enron"), ("ceas08", "trec07")]:
    raw = pw[(pw.train == a) & (pw.test == b) & (pw.setting == "raw")].iloc[0]
    cl = pw[(pw.train == a) & (pw.test == b) & (pw.setting == "clean")].iloc[0]
    ex.append(f"{NICE[a]} $\\rightarrow$ {NICE[b]} & {int(raw.train_size - cl.train_size):,} & {raw.f1:.3f} & {cl.f1:.3f} \\\\")
w("tab_pairwise.tex", table("Single-corpus transfer with TF-IDF and logistic regression, before and after removing "
                            "training emails that also appear in the test corpus. The last row is a pair that shares "
                            "almost nothing.", "tab:pairwise", "lrrr",
                            "Train $\\rightarrow$ test & Removed & Raw F1 & Clean F1", ex))

# ------------------------------------------------------------ main
m = pd.read_csv(os.path.join(R, "main_table.csv"))
order = {"classical": 0, "fine-tuned encoder": 1, "published detector": 2, "small LLM": 3, "frontier LLM": 4}
m["o"] = m.type.map(order).fillna(9)
m = m.sort_values(["o", "unseen_f1_mean"], ascending=[True, False])
rows, last = [], None
for r in m.itertuples():
    if last is not None and r.type != last:
        rows.append("\\midrule")
    last = r.type
    inc = f"{r.in_corpus_f1:.3f}" if isinstance(r.in_corpus_f1, float) and r.in_corpus_f1 == r.in_corpus_f1 else "--"
    cost = "local" if r.usd_per_1000 == 0 else f"{r.usd_per_1000:.3f}"
    jk = getattr(r, "unseen_f1_jackknife", "")
    jk = str(jk).replace("-", "--") if isinstance(jk, str) and jk else "--"
    num = lambda v: "--" if v != v else f"{v:.3f}"
    rows.append(f"{r.model} & {inc} & {r.unseen_f1_mean:.3f} & {r.unseen_f1_ci.replace('-', '--')} & "
                f"{jk} & {100 * r.false_alarm_rate:.1f} & "
                f"{num(r.ai_phishing_f1)} & {num(r.nazario_recall)} & {cost} \\\\")
w("tab_main.tex", table("Main results, all on the same evaluation emails. Trained models use decontaminated "
                        "leave-one-corpus-out data. ``Unseen'' is the mean F1 over the six held-out corpora, with a "
                        "paired bootstrap interval over emails and a leave-one-corpus-out jackknife range over corpora. "
                        "FA is the share of legitimate emails flagged. AI phishing is F1 on E-PhishLLM. Nazario "
                        "contains only phishing, so we report recall. Cost is the measured charge in USD per 1{,}000 "
                        "emails on the six corpora.", "tab:main", "lrrrrrrrr",
                        "Model & In-corpus & Unseen & Bootstrap & Jackknife & FA (\\%) & AI phish & Nazario & USD/1k",
                        rows, wide=True, sep="3.5pt"))

# ---------------------------------------------------------- labels
ls = pd.read_csv(os.path.join(R, "label_study_summary.csv"))
comp = ls[ls.row == "composition"]
rows = [f"{NICE[r.source]} & {int(r.n_positives)} & {r.phishing_pct:.1f} & {r.spam_pct:.1f} \\\\" for r in comp.itertuples()]
kind = ls[ls.row == "recall_by_kind"].sort_values("gap", ascending=False).head(6)
w("tab_labels.tex", table("What the positive class contains, according to an LLM annotator (second annotator on 300 "
                          "emails, agreement 86\\%). Percentages of the positive evaluation emails.",
                          "tab:labels", "lrrr", "Corpus & Positives & Phishing (\\%) & Spam (\\%)", rows))

# ------------------------------------------- AI phishing and the token
ph = pd.read_csv(os.path.join(R, "placeholder_effect.csv"))
per = pd.read_csv(os.path.join(R, "per_source_metrics.csv"))
prim = {"TF-IDF + LogReg": "loco_clean", "DistilBERT": "loco_clean", "Qwen-2.5-7B": "llm_zero",
        "Gemma-3-12B": "llm_zero", "Llama-3.1-8B": "llm_zero", "Gemini-3.1-Flash-Lite": "llm_zero"}


def f1_on(model, src):
    s = prim.get(model, "llm_zero")
    row = per[(per.model == model) & (per.setting == s) & (per.test == src)]
    return float(row.f1.iat[0]) if len(row) else float("nan")


rows = []
for model in prim:
    g = ph[(ph.model == model) & (ph.test_set == "ephishllm")]
    gap = f"{float(g.gap.iat[0]):+.2f}" if len(g) else "--"
    vals = [f1_on(model, s) for s in ["ephishllm", "ephishllm_nolink", "ephishllm_url", "ephishllm_it", "ephishllm_de"]]
    rows.append(f"{model} & " + " & ".join("--" if v != v else f"{v:.3f}" for v in vals) + f" & {gap} \\\\")
w("tab_aiphish.tex", table("AI-written phishing. The first column is the corpus as published. The next two are the "
                           "same 300 emails with the give-away placeholder token removed or replaced by a plausible "
                           "URL. Then the Italian and German parts. The last column is the recall gap on the English "
                           "set between phishing emails that contain the token and those that do not.",
                           "tab:aiphish", "lrrrrrr",
                           "Model & As published & Token removed & Token replaced & Italian & German & Token gap",
                           rows, wide=True))

# -------------------------------------------------------- base rate
br = pd.read_csv(os.path.join(R, "base_rate.csv"))
br = br[br.model.isin(["Gemini-3.1-Flash-Lite", "Qwen-2.5-7B", "TF-IDF + LogReg", "DistilBERT",
                       "Gemma-3-12B", "Llama-3.1-8B", "Phi-4-14B"])]
rows = [f"{r.model} & {r.recall:.3f} & {100 * r.false_alarm:.1f} & {r['precision@0.5']:.3f} & "
        f"{r['precision@0.05']:.3f} & {r['f1@0.05']:.3f} & {r['false_alerts_per_1000@0.05']:.0f} \\\\"
        for _, r in br.iterrows()]
w("tab_baserate.tex", table("The same models at a realistic amount of phishing. Recall and false alarm rate are "
                            "measured; precision and F1 are recomputed for a mailbox where 5\\% of mail is phishing. "
                            "The last column is how many legitimate emails out of 1{,}000 would be flagged.",
                            "tab:baserate", "lrrrrrr",
                            "Model & Recall & FA (\\%) & Prec. at 50\\% & Prec. at 5\\% & F1 at 5\\% & Bad alerts/1k",
                            rows, wide=True, sep="4pt"))

# ---------------------------------------------------------- cascade
cas = pd.read_csv(os.path.join(R, "cascade.csv"))
rows = []
for _, r in cas.sort_values("usd_per_1000").iterrows():
    rows.append(f"{r.stage1} $\\rightarrow$ {r.stage2} & {r.policy} & {r.unseen_f1:.3f} & "
                f"{100 * r.false_alarm:.1f} & {r.ai_phishing_f1:.3f} & {100 * r.share_to_stage2:.0f} & "
                f"{r.usd_per_1000:.4f} \\\\")
w("tab_cascade.tex", table("Two-stage detectors built from models we already measured, with no new calls. "
                           "``confirm'' sends only the mail stage 1 flagged to stage 2 and needs both to agree; "
                           "``rescue'' sends only the mail stage 1 cleared and accepts either verdict. ``To stage 2'' "
                           "is the share of mail that reaches the second model, which is what makes the cost lower "
                           "than running that model on everything.", "tab:cascade", "llrrrrr",
                           "Pipeline & Policy & Unseen F1 & FA (\\%) & AI phish & To stage 2 (\\%) & USD/1k",
                           rows, wide=True))
print("tables written")
