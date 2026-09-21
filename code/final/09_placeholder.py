"""
Step 9. Is the AI-phishing result driven by a give-away token?

E-PhishGen writes phishing links as the literal placeholder "<<link>>".
In our English evaluation subset 81 of the 150 phishing emails contain it and
none of the 150 legitimate ones do. A detector could simply be reacting to
that token instead of to the phishing content.

We split the phishing emails into the ones with a placeholder and the ones
without, and compare recall on the two halves for every model. If recall is
much lower without the placeholder, the token was doing the work.

This uses predictions we already have, so it costs nothing.
Writes results/final/placeholder_effect.csv
"""

import os
import re

import pandas as pd

from common import DATA_DIR, RESULTS_DIR
import progress

PLACEHOLDER = re.compile(r"<<[^>]{0,60}>>")


def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location("an", os.path.join(os.path.dirname(__file__), "06_analysis.py"))
    an = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(an)
    preds, _ = an.load_preds()
    preds["name"] = preds["model"].map(an.pretty)

    rows = []
    for src in ["ephishllm", "ephishllm_it", "ephishllm_de"]:
        ev = pd.read_csv(os.path.join(DATA_DIR, f"eval_{src}.csv"), keep_default_na=False)
        ev["has_ph"] = ev.text.str.contains(PLACEHOLDER)
        flag = dict(zip(ev.id, ev.has_ph))
        for (name, setting), g in preds[preds.source == src].groupby(["name", "setting"]):
            g = g.copy()
            g["has_ph"] = g.id.map(flag)
            pos = g[g.label == 1]
            if len(pos) == 0:
                continue
            with_ph, without = pos[pos.has_ph], pos[~pos.has_ph]
            if len(with_ph) == 0 or len(without) == 0:
                continue
            rows.append({
                "test_set": src, "model": name, "setting": setting,
                "n_with_placeholder": len(with_ph), "n_without": len(without),
                "recall_with_placeholder": round(with_ph.pred.mean(), 3),
                "recall_without": round(without.pred.mean(), 3),
                "gap": round(with_ph.pred.mean() - without.pred.mean(), 3),
                "false_alarm": round(g[g.label == 0].pred.mean(), 3)})
    # The split above compares different emails, so the gap could be the kind of
    # phishing rather than the token. The paired test below removes the token
    # from the SAME emails and compares the verdicts, which is the real test.
    paired = []
    ev = pd.read_csv(os.path.join(DATA_DIR, "eval_ephishllm.csv"), keep_default_na=False)
    has = dict(zip(ev.id, ev.text.str.contains(PLACEHOLDER)))
    for (name, setting), g in preds[preds.source.isin(["ephishllm", "ephishllm_nolink"])].groupby(["name", "setting"]):
        a = g[(g.source == "ephishllm") & (g.label == 1)].set_index("id")
        b = g[(g.source == "ephishllm_nolink") & (g.label == 1)].set_index("id")
        ids = [i for i in a.index.intersection(b.index) if has.get(i)]
        if len(ids) < 20:
            continue
        ra, rb = a.loc[ids, "pred"].mean(), b.loc[ids, "pred"].mean()
        flipped = int((a.loc[ids, "pred"].values > b.loc[ids, "pred"].values).sum())
        paired.append({"test_set": "ephishllm paired", "model": name, "setting": setting,
                       "n_with_placeholder": len(ids), "n_without": 0,
                       "recall_with_placeholder": round(ra, 3), "recall_without": round(rb, 3),
                       "gap": round(ra - rb, 3), "false_alarm": None,
                       "caught_only_with_token": flipped})
    rows += paired
    out = pd.DataFrame(rows).sort_values(["test_set", "gap"], ascending=[True, False])
    out.to_csv(os.path.join(RESULTS_DIR, "placeholder_effect.csv"), index=False)
    eng = out[out.test_set == "ephishllm"]
    pair = out[out.test_set == "ephishllm paired"]
    print(eng.to_string(index=False))
    print("\nsplit comparison, mean recall gap:", round(eng.gap.mean(), 3))
    if len(pair):
        print("\npaired comparison (same emails, token removed):")
        print(pair[["model", "n_with_placeholder", "recall_with_placeholder",
                    "recall_without", "gap", "caught_only_with_token"]].to_string(index=False))
        print("mean paired gap:", round(pair.gap.mean(), 3))
    progress.mark("09_placeholder",
                  f"split gap {round(eng.gap.mean(), 3)}, paired gap {round(pair.gap.mean(), 3) if len(pair) else 'n/a'}")


if __name__ == "__main__":
    main()
