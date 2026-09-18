// Builds final_deck.pptx from numbers.json and the result figures.
// Run: NODE_PATH=<dir with pptxgenjs> node build_pptx.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const n = JSON.parse(fs.readFileSync(path.join(__dirname, "numbers.json")));
const FIG = path.join(__dirname, "..", "results", "final", "figures");
const REPO = "https://github.com/Jahid15/phishing-llm-cross-corpus";
const COLAB = "https://colab.research.google.com/github/Jahid15/phishing-llm-cross-corpus/blob/main/notebooks/phishing_llm_cross_corpus.ipynb";

const C = { bg: "0F1420", card: "1B2335", text: "F5F7FA", muted: "94A3B8", accent: "FF6B4A",
            good: "4ADE80", blue: "60A5FA", amber: "FBBF24", line: "2A3448" };
const F = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "Phishing Email Detection Using LLMs: Final Update";

const f3 = x => (typeof x === "number" ? x.toFixed(3) : String(x));
const sa = n.sa_in_kaggle;
const main = n.main;
const best = main.find(r => r.model === "Qwen-2.5-7B");
const qfs = main.find(r => r.model === "Qwen-2.5-7B few-shot");
const lr = main.find(r => r.model === "TF-IDF + LogReg");
const infl = Object.fromEntries(n.inflation_logreg.map(r => [r.test, r]));
const spent = n.llm_total_usd + n.discarded_usd;

function base(kicker, speaker, title) {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  s.addText(kicker.toUpperCase(), { x: 0.6, y: 0.35, w: 9, h: 0.3, fontFace: F, fontSize: 12, bold: true,
    color: C.accent, charSpacing: 2, margin: 0, isTextBox: true });
  if (speaker) s.addText(speaker, { x: 10.7, y: 0.35, w: 2, h: 0.3, fontFace: F, fontSize: 12, color: C.muted,
    align: "right", margin: 0, isTextBox: true });
  s.addText(title, { x: 0.6, y: 0.7, w: 12.1, h: 0.8, fontFace: F, fontSize: 32, bold: true, color: C.text,
    margin: 0, isTextBox: true });
  return s;
}
function card(s, x, y, w, h, border) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08,
    fill: { color: C.card }, line: { color: border || C.card, width: border ? 1.5 : 0 } });
}
function cardText(s, x, y, w, h, head, body, color, border) {
  card(s, x, y, w, h, border);
  s.addText([
    { text: head, options: { bold: true, color: color || C.text, fontSize: 15, breakLine: true } },
    { text: body, options: { color: C.muted, fontSize: 12 } }],
    { x: x + 0.15, y: y + 0.1, w: w - 0.3, h: h - 0.2, fontFace: F, valign: "top", margin: 0, isTextBox: true, paraSpaceAfter: 4 });
}
function pageNum(s, k) {
  s.addText(String(k), { x: 12.2, y: 7.0, w: 0.5, h: 0.3, fontFace: F, fontSize: 11, color: C.muted, align: "right", margin: 0, isTextBox: true });
}
function img(s, file, x, y, w, h) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 } });
  s.addImage({ path: path.join(FIG, file), x: x + 0.1, y: y + 0.1, w: w - 0.2, h: h - 0.2, sizing: { type: "contain", w: w - 0.2, h: h - 0.2 } });
}
const hdr = t => ({ text: t, options: { bold: true, color: C.blue, fill: { color: C.bg } } });
const cell = (t, o = {}) => ({ text: String(t), options: Object.assign({ color: C.text }, o) });

// 1 title
{
  const s = pres.addSlide(); s.background = { color: C.bg };
  s.addText("COMPUTER SECURITY · FINAL UPDATE · PROJECT FORUM", { x: 0.8, y: 1.6, w: 11, h: 0.4, fontFace: F, fontSize: 14, bold: true, color: C.accent, charSpacing: 2, margin: 0, isTextBox: true });
  s.addText("Phishing Email Detection Using Large Language Models", { x: 0.8, y: 2.1, w: 11.5, h: 1.6, fontFace: F, fontSize: 44, bold: true, color: C.text, margin: 0, isTextBox: true, valign: "top" });
  s.addText("A leakage-aware, cross-corpus and cost-aware benchmark of small open LLMs", { x: 0.8, y: 3.75, w: 11.5, h: 0.5, fontFace: F, fontSize: 20, color: C.blue, margin: 0, isTextBox: true });
  s.addText("Jahid Ibna Sinha (011221376)\nMd. Jakaria Alam Saimon (011221002)\nNowshin Anjum Faria (011221372)", { x: 0.8, y: 5.0, w: 6, h: 1.2, fontFace: F, fontSize: 14, color: C.muted, margin: 0, isTextBox: true, valign: "top" });
  s.addText([{ text: "United International University", options: { bold: true, color: C.text, breakLine: true } }, { text: "Group 18", options: { color: C.muted } }],
    { x: 7.5, y: 5.4, w: 5, h: 0.8, fontFace: F, fontSize: 14, align: "right", margin: 0, isTextBox: true });
  s.addNotes("15 sec. Names and title. Say: in the proposal we promised a table that did not exist. Today we show it filled in.");
}

// 2 journey
{
  const s = base("Where we started", "Sinha", "From a suspicion to a measured result");
  const tl = [["15 JUL", "Literature review", "5 papers, all 97 to 99%. Every one tests inside one dataset. None reports cost."],
              ["21 JUL", "Preliminary run", "Train on one corpus, test on another: F1 0.99 fell to 0.30."],
              ["11 AUG", "Overlap check", "Kaggle already contains two thirds of SpamAssassin."],
              ["5 SEP", "Proposal talk", "Six objectives, one table to fill."],
              ["18 SEP", "Final experiments", `9 sources, 9 models, ${n.total_emails_clean.toLocaleString("en-US")} emails checked for overlap.`]];
  tl.forEach((t, i) => {
    const x = 0.6 + i * 2.45;
    card(s, x, 1.7, 2.3, 1.75, i === 4 ? C.accent : null);
    s.addText([{ text: t[0], options: { color: C.amber, bold: true, fontSize: 11, breakLine: true } },
               { text: t[1], options: { color: C.text, bold: true, fontSize: 15, breakLine: true } },
               { text: t[2], options: { color: C.muted, fontSize: 11.5 } }],
      { x: x + 0.15, y: 1.8, w: 2.0, h: 1.55, fontFace: F, valign: "top", margin: 0, isTextBox: true, paraSpaceAfter: 3 });
  });
  s.addText("What changed since the proposal", { x: 0.6, y: 3.7, w: 8, h: 0.4, fontFace: F, fontSize: 16, bold: true, color: C.text, margin: 0, isTextBox: true });
  const ch = [["Prior work found", "E-PhishGen (AISec 2025) already tested classical models across corpora. Our claim is now leakage removal plus cost, and we cite them."],
              ["Nazario is test-only", "Enron became a full corpus, so pairing Nazario with Enron mail would leak. Nazario now measures phishing recall only."],
              ["Numbers rebuilt", "The 74.4% / 4,282 / 48 on our proposal slides came from an unsaved run. Every number today comes from code in the repo."]];
  ch.forEach((c, i) => cardText(s, 0.6 + i * 4.08, 4.2, 3.93, 1.45, c[0], c[1], C.amber));
  card(s, 0.6, 5.95, 12.13, 0.9, C.blue);
  s.addText([{ text: "Question: ", options: { bold: true } }, { text: "if we remove leaked emails and always test on a corpus the model has never seen, how good are cheap detectors, and what do they cost?" }],
    { x: 0.8, y: 6.0, w: 11.8, h: 0.8, fontFace: F, fontSize: 16, color: C.text, margin: 0, isTextBox: true, valign: "middle" });
  pageNum(s, 2);
  s.addNotes("45 sec. Walk the timeline in one breath. Then the three changes, be open about the old numbers. Land on the question in the blue box.");
}

// 3 objectives
{
  const s = base("Objectives", "Sinha", "Six objectives from the proposal");
  const rows = [[hdr("#"), hdr("Objective"), hdr("What we delivered"), hdr("Status")],
    ["1", "Decontaminated benchmark", "9 sources, overlap measured at 3 levels, near duplicates removed", "Done"],
    ["2", "Leave-one-corpus-out", "6 folds, each run with raw and cleaned training data", "Done"],
    ["3", "One protocol, all families", "2 classical, DistilBERT, 6 small LLMs, 2 few-shot. Phishsense-1B not run", "Mostly"],
    ["4", "Cost in dollars", `Real cost of every one of ${n.llm_calls.toLocaleString("en-US")} LLM calls, from OpenRouter`, "Done"],
    ["5", "AI-written phishing", "E-PhishLLM (GPT-4o-mini emails) as a held-out shift test", "Done"],
    ["6", "One honest table", "F1 on unseen corpora with 95% bootstrap intervals, next to cost", "Done"]]
    .map((r, i) => i === 0 ? r : r.map((t, j) => cell(t, j === 3 ? { bold: true, color: t === "Done" ? C.good : C.amber } : {})));
  s.addTable(rows, { x: 0.6, y: 1.7, w: 12.1, colW: [0.5, 3.0, 7.2, 1.4], fontFace: F, fontSize: 14,
    border: { type: "solid", color: C.line, pt: 0.75 }, fill: { color: C.bg }, rowH: 0.55, valign: "middle" });
  s.addText("Phishsense-1B needs a HuggingFace access token. It is the first item for the next two weeks.", { x: 0.6, y: 6.4, w: 12, h: 0.4, fontFace: F, fontSize: 13, color: C.muted, margin: 0, isTextBox: true });
  pageNum(s, 3);
  s.addNotes("30 sec. Do not read every row. Say: five of six fully done, one mostly, and say why Phishsense is missing.");
}

// 4 methodology
{
  const s = base("Methodology", "Sinha", "Six steps, one script each, all on a laptop");
  const st = [["1 Collect", "9 public sources, subject + body, 10k cap per corpus", C.blue],
              ["2 Overlap", "exact, normalized, MinHash near duplicate", C.accent],
              ["3 Decontaminate", "train on 5 corpora, drop copies of the 6th", C.accent],
              ["4 Models", "TF-IDF, DistilBERT, 6 small LLMs", C.muted],
              ["5 Shift test", "E-PhishLLM, Nazario, Nigerian", C.amber],
              ["6 Report", "F1 + 95% CI + USD per 1,000", C.good]];
  st.forEach((t, i) => {
    const x = 0.6 + i * 2.05;
    cardText(s, x, 1.8, 1.8, 1.7, t[0], t[1], t[2], t[2]);
    if (i < 5) s.addText("→", { x: x + 1.8, y: 2.4, w: 0.25, h: 0.4, fontFace: F, fontSize: 18, color: C.muted, align: "center", margin: 0, isTextBox: true });
  });
  cardText(s, 0.6, 4.0, 5.95, 2.2, "Leave-one-corpus-out",
    "For each corpus T, train on the other five and test on all of T. Run twice: raw training data, and with every near duplicate of T removed. The gap is the inflation caused by leaked emails.", C.text);
  cardText(s, 6.78, 4.0, 5.95, 2.2, "Same emails for everyone",
    "A fixed 300-email subset per test set. Every model, local or paid, is scored on exactly those emails, so the numbers are comparable.", C.text);
  pageNum(s, 4);
  s.addNotes("45 sec. Point at steps 2 and 3, those are ours. Explain raw vs clean in one sentence. Then hand over to Saimon.");
}

// 5 experimental details
{
  const s = base("Experimental core details (from the notebook)", "Saimon", "What exactly we ran");
  const ds = Object.fromEntries(n.datasets.map(d => [d.source, d]));
  const order = ["spamassassin", "ceas08", "trec07", "ling", "enron", "kaggle", "nazario", "nigerian", "ephishllm"];
  const rows = [[hdr("Source"), hdr("Role"), hdr("Cleaned"), hdr("Used"), hdr("Eval")]]
    .concat(order.map(k => [cell(k), cell(ds[k].role), cell(ds[k].emails_after_cleaning.toLocaleString("en-US")),
                            cell(ds[k].emails_used.toLocaleString("en-US")), cell(ds[k].eval_subset)]));
  s.addTable(rows, { x: 0.6, y: 1.7, w: 6.4, colW: [1.7, 1.3, 1.3, 1.2, 0.9], fontFace: F, fontSize: 12.5,
    border: { type: "solid", color: C.line, pt: 0.75 }, fill: { color: C.bg }, rowH: 0.42, valign: "middle" });
  const boxes = [["Classical", `TF-IDF 1-2 grams, 50k features, LogReg / Naive Bayes, CPU ${n.logreg_cpu_sec_per_1000} s per 1,000 emails`, C.blue],
                 ["DistilBERT", "1 epoch, 128 tokens, batch 16, lr 5e-5, 1,000 emails per corpus, laptop CPU", C.good],
                 ["6 LLMs via OpenRouter", "Llama 1B/3B/8B, Qwen 7B, Gemma 12B, Phi-4 14B. Temperature 0, 5 output tokens, 1,500 chars. Few-shot: 4 examples from other corpora", C.accent],
                 ["Reproducible", `Seed 42 everywhere. 8 GB MacBook. Total API spend $${spent.toFixed(2)}`, C.amber]];
  boxes.forEach((b, i) => cardText(s, 7.3, 1.7 + i * 1.27, 5.43, 1.12, b[0], b[1], b[2]));
  pageNum(s, 5);
  s.addNotes("50 sec. This is the notebook slide. Mention: all numbers on later slides are produced by these scripts, the notebook re-creates every table.");
}

// 6 overlap
{
  const s = base("Result 1 · Overlap between corpora", "Saimon", "The standard check finds almost none of it");
  s.addText("SpamAssassin emails that also sit inside the Kaggle set", { x: 0.6, y: 1.65, w: 6, h: 0.3, fontFace: F, fontSize: 13, color: C.muted, margin: 0, isTextBox: true });
  [["EXACT TEXT", sa.exact_raw, C.muted], ["NO WHITESPACE", sa.exact_norm, C.amber], ["NEAR DUPLICATE", sa.near, C.accent]].forEach((b, i) => {
    const x = 0.6 + i * 2.1;
    card(s, x, 2.05, 1.95, 1.6, b[2]);
    s.addText([{ text: b[0], options: { fontSize: 10.5, bold: true, color: b[2], breakLine: true } },
               { text: b[1][0].toLocaleString("en-US"), options: { fontSize: 34, bold: true, color: i ? b[2] : C.text, breakLine: true } },
               { text: b[1][1] + "%", options: { fontSize: 12, color: C.muted } }],
      { x: x + 0.15, y: 2.12, w: 1.7, h: 1.45, fontFace: F, margin: 0, isTextBox: true, valign: "top" });
  });
  card(s, 0.6, 3.9, 6.15, 1.0);
  s.addText([{ text: "Kaggle also holds " }, { text: `${Math.round(n.ling_in_kaggle_near[1])}%`, options: { bold: true, color: C.accent } },
             { text: " of Ling and " }, { text: `${Math.round(n.enron_in_kaggle_near[1])}%`, options: { bold: true, color: C.accent } },
             { text: " of Enron. More than half of Kaggle is Enron." }],
    { x: 0.8, y: 3.95, w: 5.8, h: 0.9, fontFace: F, fontSize: 16, color: C.text, margin: 0, isTextBox: true, valign: "middle" });
  s.addText("Why exact matching fails: Kaggle deletes line breaks and glues words (\"cream?Isn't\"). We checked 400 of them by brute force: the matches are real.",
    { x: 0.6, y: 5.1, w: 6.1, h: 0.7, fontFace: F, fontSize: 12.5, color: C.muted, margin: 0, isTextBox: true, valign: "top" });
  img(s, "overlap_heatmap.png", 7.05, 1.65, 5.68, 4.95);
  pageNum(s, 6);
  s.addNotes("55 sec. Say the three numbers slowly: two, three thousand eight hundred, five thousand. The exact check is what most people would run and it finds two.");
}

// 7 inflation, native chart
{
  const s = base("Result 2 · Leakage inflates scores", "Saimon", "Remove the copies and the good transfer disappears");
  card(s, 0.6, 1.7, 5.3, 1.55, C.accent);
  s.addText([{ text: "KAGGLE → SPAMASSASSIN, TF-IDF + LOGREG", options: { fontSize: 10.5, bold: true, color: C.accent, breakLine: true } },
             { text: `${n.kaggle_to_sa.raw.toFixed(3)}  →  `, options: { fontSize: 32, bold: true, color: C.text } },
             { text: n.kaggle_to_sa.clean.toFixed(3), options: { fontSize: 32, bold: true, color: C.accent, breakLine: true } },
             { text: "F1 with leaked emails, then after removing them", options: { fontSize: 12, color: C.muted } }],
    { x: 0.8, y: 1.78, w: 5.0, h: 1.4, fontFace: F, margin: 0, isTextBox: true, valign: "top" });
  const T = ["spamassassin", "ling", "enron", "kaggle", "ceas08", "trec07"];
  const rows = [[hdr("Held-out"), hdr("Raw"), hdr("Clean"), hdr("Drop"), hdr("Removed")]].concat(
    T.map(t => [cell(t), cell(infl[t].loco_raw.toFixed(3)), cell(infl[t].loco_clean.toFixed(3)),
                cell((infl[t].inflation * 100).toFixed(1), { bold: true, color: infl[t].inflation > 0.01 ? C.accent : C.muted }),
                cell(Math.round(infl[t].removed).toLocaleString("en-US"))]));
  s.addTable(rows, { x: 0.6, y: 3.45, w: 5.3, colW: [1.5, 0.9, 0.9, 0.8, 1.2], fontFace: F, fontSize: 12.5,
    border: { type: "solid", color: C.line, pt: 0.75 }, fill: { color: C.bg }, rowH: 0.36, valign: "middle" });
  s.addText("CEAS and TREC share almost nothing with the rest, and their scores do not move. That is the control.",
    { x: 0.6, y: 6.15, w: 5.3, h: 0.6, fontFace: F, fontSize: 12, color: C.muted, margin: 0, isTextBox: true });
  s.addChart(pres.charts.BAR, [
      { name: "In-corpus (80/20)", labels: T, values: T.map(t => infl[t].in_corpus) },
      { name: "Unseen, raw", labels: T, values: T.map(t => infl[t].loco_raw) },
      { name: "Unseen, decontaminated", labels: T, values: T.map(t => infl[t].loco_clean) }],
    { x: 6.2, y: 1.7, w: 6.53, h: 5.0, barDir: "col", barGrouping: "clustered",
      chartColors: ["60A5FA", "FBBF24", "FF6B4A"], showTitle: true, title: "TF-IDF + LogReg, F1", titleColor: C.text, titleFontSize: 14,
      showLegend: true, legendPos: "b", legendColor: C.text, legendFontSize: 11,
      valAxisMinVal: 0, valAxisMaxVal: 1, valAxisLabelColor: C.muted, catAxisLabelColor: C.text, catAxisLabelFontSize: 11,
      valGridLine: { color: C.line, size: 0.5 }, catGridLine: { style: "none" }, valAxisLabelFormatCode: "0.0",
      plotArea: { fill: { color: C.bg } } });
  pageNum(s, 7);
  s.addNotes("55 sec. Kaggle to SpamAssassin was the suspicious 0.97 from July. Now it is measured. Point at CEAS and TREC: no overlap, no change. Hand over to Faria.");
}

// 8 main table
{
  const s = base("Result 3 · The table from the proposal, filled in", "Faria", "Unseen corpora, AI phishing and cost in one place");
  const rows = [[hdr("Model"), hdr("Unseen-corpus F1 (95% CI)"), hdr("Worst corpus"), hdr("AI phishing F1"), hdr("Nazario recall"), hdr("$ / 1,000")]]
    .concat(main.map(r => {
      const o = r === best ? { color: C.accent, bold: true } : {};
      return [cell(r.model, o), cell(`${f3(r.unseen_f1_mean)} (${r.unseen_f1_ci})`, o), cell(f3(r.unseen_f1_worst), o),
              cell(f3(r.ai_phishing_f1), o), cell(f3(r.nazario_recall), o), cell(r.usd_per_1000 === 0 ? "local" : "$" + r.usd_per_1000.toFixed(3), o)];
    }));
  s.addTable(rows, { x: 0.6, y: 1.7, w: 12.1, colW: [2.9, 2.8, 1.5, 1.7, 1.7, 1.5], fontFace: F, fontSize: 12.5,
    border: { type: "solid", color: C.line, pt: 0.75 }, fill: { color: C.bg }, rowH: 0.37, valign: "middle", align: "center" });
  s.addText("All scores on the same held-out emails. Trained models use decontaminated data. LLMs never saw any of our data.",
    { x: 0.6, y: 6.6, w: 12, h: 0.35, fontFace: F, fontSize: 12, color: C.muted, margin: 0, isTextBox: true });
  pageNum(s, 8);
  s.addNotes("60 sec. Read only the top row, the TF-IDF row and the worst LLM. Point at the cost column.");
}

// 9 takeaways
{
  const s = base("Result 4 · What it means", "Faria", "Cheap detectors can be robust, if you pick carefully");
  const tk = [[`1. Best balance: ${best.model} zero-shot`, `${f3(best.unseen_f1_mean)} F1 on unseen corpora, ${f3(best.ai_phishing_f1)} on AI phishing, $${best.usd_per_1000.toFixed(3)} per 1,000 emails.`, C.good],
              [`2. Few-shot helps old mail, hurts AI phishing`, `Qwen: unseen ${f3(best.unseen_f1_mean)} to ${f3(qfs.unseen_f1_mean)}, but AI phishing ${f3(best.ai_phishing_f1)} to ${f3(qfs.ai_phishing_f1)}. Old examples anchor the model to old spam.`, C.accent],
              [`3. TF-IDF is a strong, free baseline`, `${f3(lr.unseen_f1_mean)} on unseen corpora, but only ${f3(lr.ai_phishing_f1)} on AI-written phishing.`, C.blue],
              [`4. Size is not quality`, `Phi-4 (14B) ignored the one-word format in a third of emails and scored below 3B and 8B models.`, C.amber]];
  tk.forEach((t, i) => cardText(s, 0.6, 1.65 + i * 1.25, 5.9, 1.12, t[0], t[1], t[2], t[2]));
  img(s, "f1_vs_cost.png", 6.75, 1.65, 5.98, 4.85);
  pageNum(s, 9);
  s.addNotes("60 sec. Four takeaways, one sentence each. Spend the most time on number 2, it is the surprise: examples from old corpora make the model worse on new attacks.");
}

// 10 limitations
{
  const s = base("Limitations", "Faria", "What this study does not show");
  const L = [["Labels are mixed", "Four corpora count ordinary spam as positive. We keep the published labels and report phishing-only recall separately."],
             ["Small evaluation sets", "300 emails per test set keeps the cost low. The 95% intervals are about ±0.02 to ±0.03."],
             ["LLM training data is unknown", "Old public corpora may be in the LLMs' pre-training data. E-PhishLLM is newer, but we cannot rule it out."],
             ["Text only, English only", "No headers, URLs or attachments. The Italian and German part of E-PhishLLM is unused."],
             ["Light DistilBERT training", "1,000 emails per corpus and one epoch, to fit an 8 GB laptop."],
             ["One prompt, one run", "No prompt search. Providers can change a model behind the same name."]];
  L.forEach((l, i) => cardText(s, 0.6 + (i % 2) * 6.13, 1.7 + Math.floor(i / 2) * 1.65, 6.0, 1.5, l[0], l[1], C.text));
  pageNum(s, 10);
  s.addNotes("40 sec. Say the first three clearly. The teacher will ask about LLM pre-training contamination, so name it before they do.");
}

// 11 next two weeks
{
  const s = base("Scope of improvements within 2 weeks", "Faria", "What we can finish before the final paper");
  const W = [["DAYS 1 TO 3", "Phishsense-1B", "Get a HuggingFace token, run it locally on the same 2,700 emails. It is the model that fell from 97.5% to 70%.", C.blue],
             ["DAYS 4 TO 6", "Phishing-only labels", "Relabel spam vs phishing on a sample and rerun, to close the label gap.", C.accent],
             ["DAYS 7 TO 9", "Bigger test sets", "1,000 emails per set for the top 3 models. Under $0.50 more.", C.amber],
             ["DAYS 10 TO 14", "Multilingual + write-up", "Italian and German E-PhishLLM, stronger DistilBERT, final paper.", C.good]];
  W.forEach((w, i) => {
    const x = 0.6 + i * 3.06;
    card(s, x, 1.8, 2.9, 3.4, w[3]);
    s.addText([{ text: w[0], options: { fontSize: 11, bold: true, color: C.amber, breakLine: true } },
               { text: w[1], options: { fontSize: 17, bold: true, color: C.text, breakLine: true } },
               { text: w[2], options: { fontSize: 13, color: C.muted } }],
      { x: x + 0.18, y: 1.95, w: 2.55, h: 3.1, fontFace: F, margin: 0, isTextBox: true, valign: "top", paraSpaceAfter: 6 });
  });
  s.addText("Each item reuses the existing scripts. The budget left is well over one dollar.", { x: 0.6, y: 5.6, w: 12, h: 0.4, fontFace: F, fontSize: 13, color: C.muted, margin: 0, isTextBox: true });
  pageNum(s, 11);
  s.addNotes("30 sec. Four blocks, left to right. Stress that each one is small because the pipeline already exists.");
}

// 12 links
{
  const s = base("Source code", "Faria", "Everything is public and re-runnable");
  card(s, 0.6, 1.8, 5.95, 1.9, C.blue);
  s.addText([{ text: "GITHUB", options: { fontSize: 11, bold: true, color: C.blue, breakLine: true } },
             { text: REPO.replace("https://", ""), options: { fontSize: 17, color: C.text, hyperlink: { url: REPO }, breakLine: true } },
             { text: "code, results, paper, research log", options: { fontSize: 12, color: C.muted } }],
    { x: 0.8, y: 1.95, w: 5.6, h: 1.6, fontFace: F, margin: 0, isTextBox: true, valign: "top", paraSpaceAfter: 6 });
  card(s, 6.78, 1.8, 5.95, 1.9, C.accent);
  s.addText([{ text: "COLAB NOTEBOOK", options: { fontSize: 11, bold: true, color: C.accent, breakLine: true } },
             { text: "notebooks/phishing_llm_cross_corpus.ipynb", options: { fontSize: 16, color: C.text, hyperlink: { url: COLAB }, breakLine: true } },
             { text: "loads every result in seconds, or re-runs all six steps", options: { fontSize: 12, color: C.muted } }],
    { x: 6.98, y: 1.95, w: 5.6, h: 1.6, fontFace: F, margin: 0, isTextBox: true, valign: "top", paraSpaceAfter: 6 });
  card(s, 0.6, 4.3, 12.13, 1.2);
  s.addText([{ text: "High accuracy on one dataset is easy. ", options: { color: C.text } }, { text: "Honest evaluation is the hard part.", options: { color: C.accent } }],
    { x: 0.8, y: 4.35, w: 11.8, h: 1.1, fontFace: F, fontSize: 24, bold: true, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText("Thank you. Questions?", { x: 0.6, y: 6.0, w: 12.1, h: 0.4, fontFace: F, fontSize: 14, color: C.muted, align: "center", margin: 0, isTextBox: true });
  pageNum(s, 12);
  s.addNotes("20 sec. Read the links, then the closing line slowly, then stop.");
}

pres.writeFile({ fileName: path.join(__dirname, "final_deck.pptx") }).then(f => console.log("written", f));
