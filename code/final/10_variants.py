"""
Step 10. Sanitised copies of the English AI-written test set.

E-PhishGen writes phishing links as the placeholder "<<link>>" (and a few
similar ones). Only phishing emails contain them, so a detector could react to
the token rather than to the message. We build two copies of the same 300
evaluation emails:

  ephishllm_nolink : the placeholder is deleted
  ephishllm_url    : the placeholder is replaced by a plausible URL

Legitimate emails are untouched, they contain no placeholders. Comparing the
three versions tells us how much of the AI-phishing score was the token.

Writes data/final/eval_ephishllm_nolink.csv and eval_ephishllm_url.csv
"""

import os
import re

import pandas as pd

from common import DATA_DIR
import progress

PLACEHOLDER = re.compile(r"\s*<<[^>]{0,60}>>\s*")
FAKE_URL = " https://account-security-verify.example.com/login "


def main():
    ev = pd.read_csv(os.path.join(DATA_DIR, "eval_ephishllm.csv"), keep_default_na=False)
    for name, repl in [("ephishllm_nolink", " "), ("ephishllm_url", FAKE_URL)]:
        out = ev.copy()
        out["text"] = out.text.map(lambda t: re.sub(r"[ \t]+", " ", PLACEHOLDER.sub(repl, t)).strip())
        out.to_csv(os.path.join(DATA_DIR, f"eval_{name}.csv"), index=False)
        changed = (out.text != ev.text).sum()
        print(f"{name}: {changed} of {len(out)} emails changed "
              f"({(out.text != ev.text)[ev.label == 1].sum()} phishing, "
              f"{(out.text != ev.text)[ev.label == 0].sum()} legitimate)")
    progress.mark("10_variants", "sanitised AI-phishing sets built")


if __name__ == "__main__":
    main()
