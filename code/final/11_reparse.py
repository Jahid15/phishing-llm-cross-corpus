"""
Step 11. Re-read every saved model answer with the current parser.

We keep the raw text of every answer, so when the parser improves we can redo
the reading without paying for the calls again. This is what happened with
Gemini: the provider cut its reply to a single token ("ph" / "leg"), which the
first parser did not recognise, so 2,399 of 2,400 valid answers were being
recorded as "legitimate".

Prints what changed per file and rewrites the pred_raw column.
"""

import glob
import os

import pandas as pd

from common import RESULTS_DIR
import progress

import importlib.util
spec = importlib.util.spec_from_file_location("llm", os.path.join(os.path.dirname(__file__), "05_llm_eval.py"))
llm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(llm)


def reparse_offtheshelf():
    """The published causal model answers TRUE or FALSE, which the first parser
    did not know about. Its answers are saved, so they can be re-read."""
    import importlib.util as iu
    sp = iu.spec_from_file_location("ots", os.path.join(os.path.dirname(__file__), "12_offtheshelf.py"))
    ots = iu.module_from_spec(sp)
    sp.loader.exec_module(ots)
    out = []
    for f in sorted(glob.glob(os.path.join(RESULTS_DIR, "preds", "offtheshelf", "*.csv"))):
        d = pd.read_csv(f)
        if "answer" not in d.columns:
            continue
        new = d["answer"].fillna("").map(lambda a: ots.causal_parse(a, llm))
        changed = int((new != d["pred"]).sum())
        if changed:
            d["pred"] = new
            d.to_csv(f, index=False)
        out.append({"file": os.path.basename(f), "changed": changed})
        print(out[-1])
    files = glob.glob(os.path.join(RESULTS_DIR, "preds", "offtheshelf", "*.csv"))
    if files:
        pd.concat([pd.read_csv(x) for x in files], ignore_index=True).to_csv(
            os.path.join(RESULTS_DIR, "preds", "offtheshelf.csv"), index=False)
    return out


def main():
    rows = []
    for f in sorted(glob.glob(os.path.join(RESULTS_DIR, "llm_raw", "*.csv"))):
        d = pd.read_csv(f)
        d["answer"] = d["answer"].fillna("")
        mode = d["mode"].iat[0]
        new = d["answer"].map(llm.parse_long if mode == "long" else llm.parse)
        changed = int((new != d["pred_raw"]).sum())
        rows.append({"file": os.path.basename(f), "n": len(d), "changed": changed,
                     "unparsed_before": int((d.pred_raw == -1).sum()),
                     "unparsed_after": int((new == -1).sum())})
        if changed:
            d["pred_raw"] = new
            d.to_csv(f, index=False)
        print(rows[-1])
    rows += reparse_offtheshelf()
    pd.DataFrame(rows).to_csv(os.path.join(RESULTS_DIR, "reparse_report.csv"), index=False)
    progress.mark("11_reparse", f"{sum(r['changed'] for r in rows)} predictions corrected")


if __name__ == "__main__":
    main()
