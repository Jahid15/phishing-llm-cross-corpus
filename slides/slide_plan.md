# Slide Plan: Term Paper Presentation

Topic: Phishing Email Detection Using Large Language Models
Total time: 5 to 6 minutes, 9 slides, 3 speakers.

Covers exactly what the teacher asked: topic introduction (technical only, no motivation), state of the art, identified gaps, objectives, proposed method.

Speaker order: Jahid (slides 1-3), Saimon (slides 4-6), Faria (slides 7-9).

Note: the deck slides/phishing_llm_deck.pptx is already built. Slides 1-3 were updated to match this plan (presenter order, easy topic story, the catch column). Slides 4-9 are unchanged.

Design notes for whoever makes the slides: keep slides very light, one idea per slide, big numbers, almost no full sentences. Dark background with one accent color works well. All the numbers below are real, from our results folder, do not change them. You can paste each slide block into ChatGPT or Canva AI as-is and ask for a slide design.

---

## Slide 1. Title (Jahid, 20 sec)

Content:
- Title: Phishing Email Detection Using Large Language Models
- Subtitle: Cost Aware Benchmarking of Small Open LLMs Across Corpora
- Course: Computer Security, United International University
- Team in presenting order: Jahid Ibna Sinha (011221376), Md. Jakaria Alam Saimon (011221002), Nowshin Anjum Faria (011221372)

Visual: just clean text, maybe a small envelope/fish-hook icon.

## Slide 2. How do we catch a phishing email? (Jahid, 55 sec) INTERACTIVE

Content:
- Opening hook (spoken): show of hands, who got a lottery or fake bank email
- Task diagram stays on top: raw email -> classifier -> phishing / legitimate, caption "binary text classification, one email in, one label out"
- Four generation cards, the evolution of detection:
  - 01 Rules and Blocklists: block known bad senders and links, fails when wording changes
  - 02 Classical ML: TF-IDF with Logistic Regression, learns spammy word patterns
  - 03 Deep Models: fine tuned BERT and RoBERTa, read words in context
  - 04 LLMs Today: prompted like a human reader, judges and explains, no training needed
- Twist row at the bottom, this is also why we chose the topic:
  - The same LLMs now write phishing emails, attacks got cheap
  - LLMs can also detect phishing, and that is what we study

Visual: keep the email -> model -> labels diagram, 4 numbered cards in a row, 2 wide chips at the bottom.

## Slide 3. State of the art, and the catch (Jahid, 50 sec)

Content, table with 4 columns: paper, approach, result, the catch:
- Koide et al. 2024: GPT-4 + chain of thought, 99.70 percent. Catch: closed paid model, one dataset, no cost given
- Heiding et al. 2024: LLMs as judges, sometimes beat humans. Catch: only 20 emails per category, no public dataset
- Uddin et al. 2024: fine tuned RoBERTa + LIME, 98.45 percent. Catch: single Kaggle dataset, English only
- Lin et al. 2025: 3B LLMs + LoRA, near big model. Catch: needs a paid teacher model, two datasets
- Kuikel et al. 2025: accuracy vs faithfulness, they do not correlate. Catch: one dataset pair, few models tested
- Bottom line on slide: "Every paper tests on one dataset at a time. Our plan: combine multiple corpora and test across them."

Visual: 6 row 4 column table, the catch column is the point, bottom line in accent color.

## Slide 4. What we tested (Saimon, 35 sec)

Content:
- Our preliminary experiments: 3 public corpora, cleaned to text + label
  - kaggle: 17,505 emails, spamassassin: 5,809, nazario+enron: 3,128
- TF-IDF + Logistic Regression, in-dataset accuracy: 97.9 / 97.3 / 99.2 percent
- Same range the papers report. Looks like a solved problem
- (say verbally: but is it?)

Visual: 3 dataset cards with sizes, a green tick and "97-99%" big.

## Slide 5. Gap 1, the collapse (Saimon, 45 sec) INTERACTIVE

Content:
- Question on slide first (build/animation): "Train on corpus A, test on corpus B. F1 was 0.992. What does it become?"
- Then reveal: 0.992 -> 0.304
- Small matrix of train/test F1: diagonal 0.95-0.99, worst off-diagonal 0.304 and 0.354
- The model just says "legitimate" to unseen phishing

Visual: 3x3 heatmap style matrix, diagonal green, worst cells red. Reveal the red cells on click.

## Slide 6. Gaps 2 to 5, with one fresh number (Saimon, 45 sec)

Content:
- Gap 2: dataset leakage. We hashed every email body: 3,838 shared emails between Kaggle and SpamAssassin = 66.4 percent of SpamAssassin. The "good transfer" (F1 0.972) was memorization
- Gap 3: corpora are from early 2000s to 2024, zero AI generated phishing in any benchmark
- Gap 4: spam vs phishing labels conflated between corpora
- Gap 5: zero shot llama-3.2-3b: stable 0.80-0.84 everywhere, half a cent per 1000 emails; bigger gemma-3-12b worse (precision 0.58, flags everything). Nobody reports accuracy + robustness + cost together

Visual: 4 compact rows with icons; make "66.4%" and "0.5 cent / 1000 emails" big.

## Slide 7. Objectives (Faria, 40 sec)

Content, 5 short lines:
1. Deduplicated cross corpus benchmark from free public datasets
2. Leave one corpus out evaluation, classical + small open LLMs
3. Cheap improvements only: prompts, few shot, local DistilBERT (no paid teacher model)
4. Small LLM-generated phishing test set (evaluation only)
5. One table: accuracy + robustness + cost per 1000 emails, plus explanation check

Visual: numbered list, keep each line under 8 words on the slide.

## Slide 8. Proposed method (Faria, 45 sec)

Content, pipeline left to right:
- Stage 1: collect 3 corpora -> normalize -> deduplicate across corpora (we already found the 66 percent leak)
- Stage 2: leave one corpus out loop: train/prompt on two corpora, always test on the held out one
- Stage 3: models compared under same protocol: TF-IDF LogReg, DistilBERT (local CPU), llama-3.2-3b zero shot and few shot via OpenRouter
- Stage 4: extra test set of LLM written phishing, measure degradation
- Stage 5: report accuracy, F1, robustness drop, cost per 1000 emails in one table

Visual: horizontal 5-box pipeline diagram with arrows. This is the main visual of the deck, make it clean.

## Slide 9. Expected outcome and close (Faria, 30 sec)

Content:
- Deliverable: reproducible benchmark (code public), one honest comparison table
- Everything runs on a laptop, total LLM budget under 5 dollars (spent so far: under 1 cent)
- Closing line: "high accuracy on one dataset is easy, honest evaluation is the hard part"
- Thank you + questions

Visual: minimal, the closing line big in the center.

---

Timing check: 20+55+50+35+45+45+40+45+30 = 365 sec = 6 min 5 sec. Slightly over, so keep the interactive pauses short and it lands around 6 minutes.

Interactive moments (already in the scripts):
- Slide 2: show of hands, who received a lottery or fake bank email
- Slide 5: ask the audience to guess the F1 drop before revealing
- Slide 6: quick show of hands, "who thinks the 12B model beats the 3B?" before revealing gemma result
