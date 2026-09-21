"""
Runs the heavy steps in order and remembers what is finished.

  python run_all.py            run everything that is not done yet
  python run_all.py --status   show what is done
  python run_all.py --only 03  run one step

Each step is skipped when its own output already exists, so stopping and
restarting this script is safe.
"""

import argparse
import os
import subprocess
import sys
import time

import progress

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

STEPS = [
    ("02_overlap", ["02_overlap.py"]),
    ("03_classical", ["03_classical_loco.py"]),
    ("04_distilbert", ["04_distilbert_loco.py"]),
    # the published detectors are run separately because they use the GPU while
    # the fine-tuning above uses the CPU:
    #   DEVICE=mps python 12_offtheshelf.py --models bert,modernbert --sources ...
    #   DEVICE=mps python 12_offtheshelf.py --models phishsense --sources ...
    ("06_analysis", ["06_analysis.py"]),
]


def run(step, cmd):
    print(f"\n=== {step} ===", flush=True)
    t0 = time.time()
    env = dict(os.environ, DEVICE=os.environ.get("DEVICE", "cpu"))
    r = subprocess.run([PY, "-u"] + [os.path.join(HERE, cmd[0])] + cmd[1:], cwd=HERE, env=env)
    if r.returncode != 0:
        print(f"{step} failed with code {r.returncode}, stopping so it can be resumed")
        sys.exit(r.returncode)
    progress.mark(step, f"{round((time.time() - t0) / 60, 1)} min")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.status:
        progress.status()
        return
    for step, cmd in STEPS:
        if a.only and not step.startswith(a.only):
            continue
        if progress.done(step) and not a.force:
            print(f"skip {step}, already done")
            continue
        run(step, cmd)


if __name__ == "__main__":
    main()
