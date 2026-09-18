"""Writes the LaTeX tables of the paper from results/final, so the paper never drifts from the data."""
import os
import pandas as pd

R = os.path.join(os.path.dirname(__file__), "..", "results", "final")
OUT = os.path.dirname(os.path.abspath(__file__))


def w(name, s):
    open(os.path.join(OUT, name), "w").write(s)


# data table
st = pd.read_csv(os.path.join(R, "dataset_stats.csv"))
nice = {"spamassassin": "SpamAssassin", "ceas08": "CEAS-08", "trec07": "TREC-07", "ling": "Ling-Spam",
        "enron": "Enron", "kaggle": "Kaggle", "nazario": "Nazario", "nigerian": "Nigerian", "ephishllm": "E-PhishLLM (en)"}
rows = "\n".join(
    f"{nice[r.source]} & {'train/test' if r.role == 'train+test' else 'test'} & {r.emails_after_cleaning:,} & {r.emails_used:,} & {r.phishing_or_spam:,} & {r.eval_subset} \\\\"
    for r in st.itertuples())
w("tab_data.tex", r"""\begin{table}[t]
\caption{Email sources after cleaning. ``Used'' is after the 10k stratified cap. ``Eval'' is the fixed subset every model is scored on.}
\label{tab:data}
\centering\footnotesize
\setlength{\tabcolsep}{3.5pt}
\begin{tabular}{lrrrrr}
\toprule
Source & Role & Cleaned & Used & Positive & Eval \\
\midrule
""" + rows + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# overlap table: what share of each corpus sits inside Kaggle, per level
pairs = pd.read_csv(os.path.join(R, "overlap_pairs.csv"))
def get(level, a, b):
    r = pairs[(pairs.level == level) & (pairs.contains == a) & (pairs.source == b)]
    return (int(r.emails_of_source_found.iat[0]), r.pct_of_source.iat[0]) if len(r) else (0, 0.0)
lines = []
for a, b in [("kaggle", "spamassassin"), ("kaggle", "ling"), ("kaggle", "enron"), ("enron", "kaggle"),
             ("enron", "spamassassin"), ("trec07", "nigerian")]:
    def fmt(c, p):
        return f"{c:,} (" + ("$<$0.1" if 0 < p < 0.1 else f"{p:.1f}") + "\\%)"
    cells = " & ".join(fmt(*get(l, a, b)) for l in ["exact_raw", "exact_norm", "near"])
    lines.append(f"{nice[b]} in {nice[a]} & {cells} \\\\")
w("tab_overlap.tex", r"""\begin{table}[t]
\caption{Emails of one corpus found inside another, at three levels of matching: exact text, exact after removing all whitespace, and near duplicate. Percentages are of the first corpus.}
\label{tab:overlap}
\centering\footnotesize
\setlength{\tabcolsep}{1.6pt}
\begin{tabular}{lrrr}
\toprule
Pair & Exact & No space & Near dup. \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# inflation table
inf = pd.read_csv(os.path.join(R, "inflation.csv"))
lr = inf[inf.model == "TF-IDF + LogReg"].set_index("test")
nb = inf[inf.model == "TF-IDF + NB"].set_index("test")
rows = []
for t in ["spamassassin", "ling", "enron", "kaggle", "ceas08", "trec07"]:
    a, b = lr.loc[t], nb.loc[t]
    rows.append(f"{nice[t]} & {int(a.removed):,} & {a.in_corpus:.3f} & {a.loco_raw:.3f} & {a.loco_clean:.3f} & {round(a.inflation*100, 1) + 0.0:+.1f} & {round(b.inflation*100, 1) + 0.0:+.1f} \\\\")
w("tab_inflation.tex", r"""\begin{table}[t]
\caption{Leave-one-corpus-out F1 of TF-IDF + Logistic Regression on the full held-out corpus. ``Removed'' is the number of training emails with a near duplicate in the test corpus. $\Delta$ is raw minus clean, in F1 points, for LogReg and Naive Bayes.}
\label{tab:inflation}
\centering\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{lrrrrrr}
\toprule
Held out & Removed & In-corpus & Raw & Clean & $\Delta$ LR & $\Delta$ NB \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# pairwise leakage examples
pw = pd.read_csv(os.path.join(R, "classical_pairwise.csv"))
ex = []
for a, b in [("kaggle", "spamassassin"), ("kaggle", "enron"), ("kaggle", "ling"), ("spamassassin", "kaggle"), ("spamassassin", "enron")]:
    raw = pw[(pw.train == a) & (pw.test == b) & (pw.setting == "raw")].iloc[0]
    cl = pw[(pw.train == a) & (pw.test == b) & (pw.setting == "clean")].iloc[0]
    ex.append(f"{nice[a]} $\\rightarrow$ {nice[b]} & {int(raw.train_size - cl.train_size):,} & {raw.f1:.3f} & {cl.f1:.3f} \\\\")
w("tab_pairwise.tex", r"""\begin{table}[t]
\caption{Single-corpus transfer with TF-IDF + LogReg, before and after removing training emails that also appear in the test corpus.}
\label{tab:pairwise}
\centering\footnotesize
\begin{tabular}{lrrr}
\toprule
Train $\rightarrow$ test & Removed & Raw F1 & Clean F1 \\
\midrule
""" + "\n".join(ex) + r"""
\bottomrule
\end{tabular}
\end{table}
""")

# main table
m = pd.read_csv(os.path.join(R, "main_table.csv"))
rows = []
for r in m.itertuples():
    inc = f"{r.in_corpus_f1:.3f}" if isinstance(r.in_corpus_f1, float) and r.in_corpus_f1 == r.in_corpus_f1 else "--"
    cost = "local" if r.usd_per_1000 == 0 else f"{r.usd_per_1000:.3f}"
    rows.append(f"{r.model} & {inc} & {r.unseen_f1_mean:.3f} & {r.unseen_f1_ci.replace('-', '--')} & {r.unseen_f1_worst:.3f} & "
                f"{100*r.false_alarm_rate:.1f} & {r.ai_phishing_f1:.3f} & {r.nazario_recall:.3f} & {r.nigerian_recall:.3f} & {cost} \\\\")
w("tab_main.tex", r"""\begin{table*}[t]
\caption{Main results. All numbers are on the same fixed evaluation emails. Trained models use decontaminated leave-one-corpus-out data. ``Unseen'' is the mean F1 over the six held-out corpora with a 95\% bootstrap interval, ``Worst'' the lowest of the six. FA is the false alarm rate, the share of legitimate emails flagged as phishing, averaged over the six corpora. AI phishing is F1 on E-PhishLLM. Nazario and Nigerian contain only positives, so we report recall. Cost is the measured OpenRouter charge in USD per 1{,}000 emails.}
\label{tab:main}
\centering\footnotesize
\setlength{\tabcolsep}{4.5pt}
\begin{tabular}{lrrrrrrrrr}
\toprule
Model & In-corpus & Unseen & 95\% CI & Worst & FA (\%) & AI phishing & Nazario rec. & Nigerian rec. & USD/1k \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{table*}
""")
print("tables written")
