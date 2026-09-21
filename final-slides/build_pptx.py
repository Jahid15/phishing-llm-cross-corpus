"""
Builds final_deck.pptx and group-18.pdf source images from final_deck.html.

The HTML deck is the master copy. Rendering it to slides keeps the PowerPoint
identical to what is presented, and the speaker notes are carried across from
the note text in the HTML.

Usage:
  1. render the slides to PNG (any headless browser, see README in this folder)
     the images must be named slide_01.png ... in --images
  2. python build_pptx.py --images /path/to/pngs
"""
import argparse
import glob
import os
import re

from pptx import Presentation
from pptx.util import Inches

HERE = os.path.dirname(os.path.abspath(__file__))


def notes_from_html():
    html = open(os.path.join(HERE, "final_deck.html")).read()
    raw = re.findall(r'<div class="note">(.*?)</div>', html, re.S)
    clean = []
    for r in raw:
        t = re.sub(r"<[^>]+>", "", r)
        clean.append(" ".join(t.split()))
    return clean


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "final_deck.pptx"))
    a = ap.parse_args()

    images = sorted(glob.glob(os.path.join(a.images, "slide_*.png")))
    if not images:
        raise SystemExit(f"no slide_*.png found in {a.images}")
    notes = notes_from_html()

    pres = Presentation()
    pres.slide_width, pres.slide_height = Inches(13.333), Inches(7.5)
    blank = pres.slide_layouts[6]
    for i, path in enumerate(images):
        s = pres.slides.add_slide(blank)
        s.shapes.add_picture(path, 0, 0, width=pres.slide_width, height=pres.slide_height)
        if i < len(notes) and notes[i]:
            s.notes_slide.notes_text_frame.text = notes[i]
    pres.save(a.out)
    print(f"{a.out} written, {len(images)} slides, {sum(1 for x in notes if x)} with notes")


if __name__ == "__main__":
    main()
