"""Writes speaker_script.md from script_data.py."""
import os
import script_data as d

HERE = os.path.dirname(os.path.abspath(__file__))
rows = "".join(
    f"| {who} | {ss[0]['no']} to {ss[-1]['no']} | "
    f"{sum(s['sec'] for s in ss)//60}:{sum(s['sec'] for s in ss)%60:02d} |\n"
    for who, ss in d.BY_SPEAKER.items())

doc = f"""# Presentation script, {len(d.SLIDES)} slides, about {d.TOTAL//60} minutes {d.TOTAL%60} seconds

| Who | Slides | Time |
|---|---|---|
{rows}
প্রতিটা slide এ তিনটা জিনিস: **কী বলবে (English)**, **কী বলবে (বাংলা)**, আর **কীভাবে বলবে**.
দুইটা ভাষার যেকোনো একটা বলো, মিশিয়ে বললেও সমস্যা নেই. সব সংখ্যা `results/final/` থেকে আসা.

Practice করার সহজ উপায়: `final-slides/PRACTICE.html` খোলো, সেখানে slide আর script পাশাপাশি
দেখা যায়, timer সহ. আসল presentation অবশ্যই `final_deck.html` বা `final_deck.pptx` থেকেই হবে.
"""

for who, ss in d.BY_SPEAKER.items():
    t = sum(s["sec"] for s in ss)
    doc += f"\n---\n\n# {who.upper()} · slides {ss[0]['no']} to {ss[-1]['no']} · {t//60}:{t%60:02d}\n"
    for s in ss:
        mark = "  ⚡ এখানে audience কে প্রশ্ন করো" if s.get("ask") else ("  ⭐ সবচেয়ে গুরুত্বপূর্ণ slide" if s.get("key") else "")
        doc += (f"\n## Slide {s['no']} · {s['title']} ({s['sec']} sec){mark}\n\n"
                f"**EN:** {s['en']}\n\n**BN:** {s['bn']}\n\n**কীভাবে:** {s['tip']}\n")

doc += "\n---\n\n# যে প্রশ্নগুলো আসবেই\n\n"
for q, a in d.QA:
    doc += f"**{q}**\n{a}\n\n"

open(os.path.join(HERE, "speaker_script.md"), "w").write(doc)
print("speaker_script.md written,", len(doc.split()), "words")
