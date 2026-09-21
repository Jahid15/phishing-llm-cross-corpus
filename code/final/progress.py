"""
Tiny progress tracker so a long run can be stopped and resumed.
Each step records when it finished and what it produced.
"""

import json
import os
import time

from common import RESULTS_DIR

FILE = os.path.join(RESULTS_DIR, "progress.json")


def _load():
    if os.path.exists(FILE):
        return json.load(open(FILE))
    return {}


def done(step):
    return step in _load()


def mark(step, note=""):
    d = _load()
    d[step] = {"finished": time.strftime("%Y-%m-%d %H:%M:%S"), "note": note}
    json.dump(d, open(FILE, "w"), indent=1, sort_keys=True)
    print(f"[progress] {step} done. {note}")


def status():
    d = _load()
    for k in sorted(d):
        print(f"{k:28s} {d[k]['finished']}  {d[k]['note']}")
    return d


if __name__ == "__main__":
    status()
