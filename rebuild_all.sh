#!/bin/bash
# Rebuilds every deliverable from the result files. Safe to run any time: it
# does not call any API and does not retrain anything.
set -e
cd "$(dirname "$0")"
PY=.venv/bin/python

echo "== analysis (tables, intervals, figures)"
$PY code/final/06_analysis.py > /dev/null
for s in 07_cascade 08_significance 09_placeholder 13_baserate; do
  echo "== $s"; $PY code/final/$s.py > /dev/null
done

echo "== paper"
$PY paper/make_tables.py > /dev/null
$PY paper/fill_numbers.py
(cd paper && tectonic main.tex 2>&1 | grep -E "Writing|error" || true)

echo "== slides"
$PY final-slides/collect_numbers.py > /dev/null
$PY final-slides/build_deck.py
$PY final-slides/build_script.py
$PY final-slides/build_practice_html.py

echo "== notebook"
(cd notebooks && ../$PY build_notebook.py)

echo "== team guide"
$PY guide/build_guide.py
$PY guide/build_guide_html.py

echo
echo "done. paper/main.pdf, final-slides/final_deck.html, TEAM_GUIDE.md updated."
echo "For the PowerPoint and PDF of the slides, render final_deck.html to"
echo "slide_01.png ... and run: $PY final-slides/build_pptx.py --images <dir>"
