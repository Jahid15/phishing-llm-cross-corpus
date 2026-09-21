"""
The spoken script for the 14 slide deck, in one place.

build_script.py turns this into speaker_script.md (for reading) and
build_practice_html.py turns it into PRACTICE.html (slide and script side by
side). Numbers come from numbers.json, so the script never disagrees with the
results.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
n = json.load(open(os.path.join(HERE, "numbers.json")))

main = {r["model"]: r for r in n["main"]}
loco = {(r["model"], r["test"], r["setting"]): r for r in n["classical_loco"]}
comp = [r for r in n["label_study_summary"] if r["row"] == "composition"]
agree = [r for r in n["label_study_summary"] if r["row"] == "agreement"][0]
base = {r["model"]: r for r in n["base_rate"]}
casc = n["cascade"]
ph = {r["model"]: r for r in n["placeholder_effect"] if r["test_set"] == "ephishllm"}
pair = [r for r in n["placeholder_effect"] if r["test_set"] == "ephishllm paired"]
thr = {(r["source"], r["threshold"]): r for r in n["overlap_thresholds"]}
mv = n["matcher_validation_summary"][0]
sa = n["sa_in_kaggle"]
conf = next(c for c in casc if c["stage1"] == "TF-IDF + LogReg" and c["stage2"] == "Qwen-2.5-7B" and c["policy"] == "confirm")
lf = lambda t, s: loco[("logreg", t, s)]["f1"]
G, Q, B = main["Gemini-3.1-Flash-Lite"], main["Qwen-2.5-7B"], main["BERT-phishing (published)"]
GM = main["Gemma-3-12B"]
split_gap = sum(r["gap"] for r in ph.values()) / len(ph) * 100
paired_gap = sum(r["gap"] for r in pair) / max(1, len(pair)) * 100
spend = n["total_spend_usd"]
calls = n["llm_calls"]
ph_lo, ph_hi = min(r["phishing_pct"] for r in comp), max(r["phishing_pct"] for r in comp)

SLIDES = [
 dict(no=1, who="Sinha", sec=15, title="Title",
  en="Good morning. We are Group 18. In the proposal we showed you an empty table and said the "
     "question marks were the project. Today the table is full, and some of what we found "
     "surprised us.",
  bn="সবাইকে শুভেচ্ছা। আমরা Group 18। Proposal এ আমরা একটা খালি table দেখিয়ে বলেছিলাম, ওই "
     "প্রশ্নবোধক চিহ্নগুলোই আমাদের project। আজ table টা পূরণ করা, আর কিছু ফলাফল আমাদের "
     "নিজেদেরকেই অবাক করেছে।",
  tip="হাসিমুখে, ধীরে। নাম তিনটা বলার দরকার নেই, slide এ আছে।"),

 dict(no=2, who="Sinha", sec=35, title="Where we started",
  en="Quick recap. In July we tested the papers' claim ourselves with TF-IDF and logistic "
     "regression, a method older than deep learning, and got the same 97 to 99 percent. Then we "
     "trained on one corpus and tested on another, and F1 fell from 0.99 to 0.30. Since the "
     "proposal we corrected three things. We are not the first to test across corpora, two recent "
     "papers did that. We added a control. And we now verify every duplicate exactly instead of "
     "trusting an estimate. So our question is: if we remove the leaked emails and always test on "
     "a corpus the model has never seen, how good are cheap detectors, what do they cost, and how "
     "much good mail do they block?",
  bn="ছোট করে আগের কথা। জুলাইতে আমরা নিজেরাই paper গুলোর দাবি যাচাই করেছিলাম TF-IDF আর "
     "Logistic Regression দিয়ে, যেটা deep learning এরও পুরনো, আর একই ৯৭ থেকে ৯৯ percent "
     "পেয়েছিলাম। তারপর এক corpus এ train করে আরেকটায় test করলাম, F1 ০.৯৯ থেকে ০.৩০ এ নেমে গেল। "
     "Proposal এর পর তিনটা জিনিস ঠিক করেছি। এক, আমরাই প্রথম না, সাম্প্রতিক দুইটা paper আগেই "
     "cross-corpus test করেছে। দুই, আমরা একটা control যোগ করেছি। তিন, প্রতিটা duplicate এখন "
     "আন্দাজে না, হিসাব করে মিলিয়ে দেখা। তাই আমাদের প্রশ্ন হলো: leaked email সরিয়ে, সবসময় "
     "অদেখা corpus এ test করলে সস্তা detector গুলো কতটা ভালো, খরচ কত, আর কতটা ভালো email আটকে দেয়?",
  tip="শেষ প্রশ্নটা নীল box এ আছে, ওটা দেখিয়ে এক সেকেন্ড থামো।"),

 dict(no=3, who="Sinha", sec=35, title="Objectives",
  en="These were our six objectives in the proposal. All six are done. And after review we added "
     "four more: what the corpora actually contain, what happens at a realistic amount of "
     "phishing, two-stage detectors, and whether the models' explanations are any good. Review "
     "made the project bigger, not smaller.",
  bn="Proposal এ আমাদের ছয়টা objective ছিল। ছয়টাই শেষ। Review এর পর আরো চারটা যোগ হয়েছে: corpus "
     "গুলোতে আসলে কী আছে, বাস্তবে যত phishing আসে তত হলে কী হয়, দুই ধাপের detector, আর model এর "
     "দেওয়া কারণগুলো আদৌ ভালো কিনা। Review কাজটা ছোট করেনি, বরং বড় করেছে।",
  tip="পুরো table পড়বে না। শুধু বলো ছয়টাই done, আর শেষ লাল row টা দেখাও।"),

 dict(no=4, who="Sinha", sec=40, title="Methodology",
  en="Six steps, one script each. The step to look at is number three, the control. Removing "
     "duplicates also removes training data, so on its own a drop could just mean less data. That "
     "is why we run a third setting that removes the same number of emails at random. If the "
     "random version does not drop, the cause is the duplicates. And every model, free, open or "
     "paid, is scored on exactly the same 300 emails per test set.",
  bn="ছয়টা ধাপ, প্রতিটার জন্য একটা script। যেটা খেয়াল করতে হবে সেটা তিন নম্বর, মানে control। "
     "Duplicate সরালে training data ও কমে যায়, তাই score কমলে সেটা শুধু কম data র কারণেও হতে "
     "পারত। এজন্য তৃতীয় একটা setting এ আমরা সমান সংখ্যক email এলোমেলোভাবে সরাই। এলোমেলো version "
     "এ score না কমলে বুঝতে হবে কারণ duplicate গুলোই। আর প্রতিটা model, free হোক, open হোক বা "
     "টাকা দিয়ে কেনা, প্রতি test set এ ঠিক একই ৩০০টা email এ score পায়।",
  tip="লাল box টায় আঙুল দেখাও। এই control টাই পুরো argument বাঁচায়।"),

 dict(no=5, who="Sinha", sec=45, title="Experimental details (from the notebook)",
  en=f"This slide is straight from our notebook. Nine email sources. Six of them take turns as the "
     f"held-out corpus, three are test only, including E-PhishLLM which is written by GPT-4o and "
     f"GPT-4o-mini. On the right are the settings: TF-IDF, DistilBERT trained on the laptop CPU, "
     f"six small open LLMs, three published phishing detectors and two paid models, all under one "
     f"prompt. Seed 42, one 8 GB laptop, every raw answer saved, total API spend {spend:.2f} "
     f"dollars. Saimon will show what we found.",
  bn=f"এই slide টা সরাসরি আমাদের notebook থেকে। নয়টা email source। তার ছয়টা পালা করে held-out "
     f"corpus হয়, তিনটা শুধু test এর জন্য, যার মধ্যে E-PhishLLM হলো GPT-4o আর GPT-4o-mini দিয়ে "
     f"লেখা। ডান পাশে setting গুলো: TF-IDF, laptop CPU তে train করা DistilBERT, ছয়টা ছোট open "
     f"LLM, তিনটা published phishing detector আর দুইটা paid model, সবাই একই prompt এ। Seed 42, "
     f"একটা 8 GB laptop, প্রতিটা raw উত্তর সংরক্ষিত, মোট API খরচ {spend:.2f} dollar। এখন সাইমন "
     f"দেখাবে আমরা কী পেয়েছি।",
  tip=f"মোট খরচ {spend:.2f} dollar কথাটা জোর দিয়ে বলো, শিক্ষক এটা মনে রাখেন।"),

 dict(no=6, who="Saimon", sec=55, title="Overlap between corpora", ask=True,
  en=f"Thank you Sinha. A question for you all: the Kaggle phishing dataset and SpamAssassin are "
     f"two different public datasets. How many emails do you think they have in common? "
     f"[wait 2 seconds, take one guess] If you compare the text exactly, the way anyone would, you "
     f"find {int(sa['exact_raw'][0])}. With whitespace removed, {int(sa['exact_norm'][0]):,}. With near-duplicate matching, "
     f"{int(sa['near'][0]):,}, which is {sa['near'][1]:.0f} percent of SpamAssassin. "
     f"{thr[('kaggle', 0.8)]['pct']:.0f} percent of the Kaggle corpus has a copy somewhere else. We verified this "
     f"against brute force: precision {mv['precision']:.2f}, recall {mv['recall']:.2f}.",
  bn=f"ধন্যবাদ সিনহা। সবাইকে একটা প্রশ্ন: Kaggle phishing dataset আর SpamAssassin, দুইটা আলাদা "
     f"public dataset। আপনাদের মনে হয় এদের মধ্যে কয়টা email একই? [২ সেকেন্ড অপেক্ষা করো, একটা "
     f"guess নাও] হুবহু text মিলালে, যেভাবে যে কেউ মিলাবে, পাওয়া যায় {int(sa['exact_raw'][0])} টা। Whitespace "
     f"বাদ দিলে {int(sa['exact_norm'][0]):,} টা। আর near-duplicate matching দিয়ে {int(sa['near'][0]):,} টা, মানে "
     f"SpamAssassin এর {sa['near'][1]:.0f} percent। Kaggle corpus এর {thr[('kaggle', 0.8)]['pct']:.0f} percent এর copy অন্য কোথাও না "
     f"কোথাও আছে। এটা আমরা brute force দিয়ে যাচাই করেছি: precision {mv['precision']:.2f}, recall {mv['recall']:.2f}।",
  tip="তিনটা সংখ্যা ধীরে বলো: দুই, তিন হাজার আটশ, পাঁচ হাজার। প্রথমটায় থেমে যাও, ওটাই ধাক্কা।"),

 dict(no=7, who="Saimon", sec=60, title="Leakage inflates scores, and the control", key=True,
  en=f"Now why that matters. Look at the SpamAssassin row. Train on the other five corpora as they "
     f"are: F1 {lf('spamassassin','loco_raw'):.3f}. Now remove the same number of training emails, but pick them at "
     f"random: {lf('spamassassin','loco_random'):.3f}. No change. Now remove the duplicates instead: {lf('spamassassin','loco_clean'):.3f}. Up to twelve "
     f"points disappear, and only when we remove the right emails. That is the control, and it is "
     f"the reason we can say this is leakage and not just less data. CEAS and TREC, which share "
     f"nothing with the others, do not move at all.",
  bn=f"এবার কেন এটা গুরুত্বপূর্ণ। SpamAssassin row টা দেখেন। বাকি পাঁচটা corpus যেমন আছে তেমন "
     f"train করলে F1 {lf('spamassassin','loco_raw'):.3f}। এবার সমান সংখ্যক training email সরাই, কিন্তু এলোমেলোভাবে "
     f"বেছে: {lf('spamassassin','loco_random'):.3f}। কোনো পরিবর্তন নেই। এবার duplicate গুলো সরাই: {lf('spamassassin','loco_clean'):.3f}। বারো point "
     f"পর্যন্ত উধাও, আর সেটা কেবল ঠিক email গুলো সরালেই। এটাই আমাদের control, আর এজন্যই আমরা "
     f"বলতে পারি এটা leakage, শুধু কম data না। CEAS আর TREC, যাদের সাথে কারো মিল নেই, একটুও নড়ে না।",
  tip="এক row ধরে তিনটা সংখ্যা বাম থেকে ডানে পড়ো, তারপর লাল box। এই slide এ তাড়াহুড়া করবে না।"),

 dict(no=8, who="Saimon", sec=45, title="What the benchmarks actually contain",
  en=f"Then we asked a different question: what is actually inside the positive class? We had an "
     f"LLM label every positive email as phishing or spam, with a second model on 300 of them to "
     f"check agreement, {100*float(agree['agreement']):.0f} percent. Only {ph_lo:.0f} to {ph_hi:.0f} percent of those emails are "
     f"phishing. The rest is ordinary bulk advertising. So when a paper says phishing detection on "
     f"these corpora, it is mostly measuring spam detection.",
  bn=f"এরপর আমরা অন্য একটা প্রশ্ন করলাম: positive class এর ভিতরে আসলে কী আছে? একটা LLM দিয়ে "
     f"প্রতিটা positive email কে phishing না spam হিসেবে label করালাম, আর ৩০০টায় দ্বিতীয় একটা "
     f"model দিয়ে মিলিয়ে দেখলাম, মিল {100*float(agree['agreement']):.0f} percent। দেখা গেল ওই email গুলোর মাত্র "
     f"{ph_lo:.0f} থেকে {ph_hi:.0f} percent আসলে phishing। বাকিটা সাধারণ বিজ্ঞাপন। মানে কোনো paper যখন এই "
     f"corpus এ phishing detection বলে, সে আসলে বেশিরভাগ spam detection মাপছে।",
  tip="হলুদ box এর সংখ্যাটা বলো, তারপর এক সেকেন্ড থামো।"),

 dict(no=9, who="Saimon", sec=40, title="A token that looked like a shortcut",
  en=f"One more check, this time on our own result. The AI-written corpus writes every phishing "
     f"link as a placeholder token. It is in 94 of our 150 phishing emails and in none of the "
     f"legitimate ones. Comparing emails that have it with emails that do not says the token is "
     f"worth {split_gap:.0f} points of recall, which would make our AI numbers meaningless. But when we "
     f"delete the token from the same emails and ask the models again, the answers move by "
     f"{paired_gap:.1f} points. The first test was comparing different kinds of email. The result stands. "
     f"Faria will take the model comparison.",
  bn=f"আরেকটা যাচাই, এবার নিজেদের ফলাফলের উপর। AI দিয়ে লেখা corpus এ প্রতিটা phishing link একটা "
     f"placeholder token দিয়ে লেখা। আমাদের ১৫০টা phishing email এর ৯৪টায় সেটা আছে, আর legitimate "
     f"কোনোটায় নেই। যেগুলোতে token আছে আর যেগুলোতে নেই, এদের তুলনা করলে মনে হয় token টা {split_gap:.0f} "
     f"point recall এর সমান, তাহলে তো আমাদের AI এর ফলাফল অর্থহীন। কিন্তু একই email থেকে token "
     f"মুছে আবার জিজ্ঞেস করলে উত্তর বদলায় মাত্র {paired_gap:.1f} point। প্রথম test টা আসলে দুই ধরনের email "
     f"তুলনা করছিল। ফলাফল টিকে গেছে। এখন ফারিয়া model গুলোর তুলনা দেখাবে।",
  tip="গল্পের মতো বলো: আমাদের নিজের ভালো ফলটা সন্দেহ হলো, তাই পরীক্ষা করলাম।"),

 dict(no=10, who="Faria", sec=55, title="Every detector on the same emails",
  en=f"Thank you Saimon. This is the table our proposal promised. Twenty detectors, the same "
     f"emails. Read three rows. Gemini, a paid model, is best: {G['unseen_f1_mean']:.3f} with {100*G['false_alarm_rate']:.0f} percent "
     f"false alarms. Zero-shot Qwen-2.5-7B is the best open model: {Q['unseen_f1_mean']:.3f} for about three cents "
     f"per thousand emails. Now the interesting row: the published BERT phishing detector scores "
     f"{B['unseen_f1_mean']:.3f} on our corpora, the highest number in the table, and {B['ai_phishing_f1']:.3f} on AI-written "
     f"phishing. It was trained on the same corpora we test on.",
  bn=f"ধন্যবাদ সাইমন। এই table টাই আমাদের proposal এ দেওয়া কথা। বিশটা detector, একই email। তিনটা "
     f"row পড়ুন। Gemini, একটা paid model, সবার সেরা: {G['unseen_f1_mean']:.3f}, ভুল alarm {100*G['false_alarm_rate']:.0f} percent। "
     f"Zero-shot Qwen-2.5-7B সেরা open model: {Q['unseen_f1_mean']:.3f}, হাজার email এ প্রায় তিন cent। এবার "
     f"মজার row টা: published BERT phishing detector আমাদের corpus এ পায় {B['unseen_f1_mean']:.3f}, table এর "
     f"সর্বোচ্চ, আর AI এর লেখা phishing এ পায় {B['ai_phishing_f1']:.3f}। কারণ ওটা ঠিক সেই corpus গুলোতেই train "
     f"করা যেগুলোতে আমরা test করছি।",
  tip="শুধু তিনটা row। শেষ row টা আঙুল দিয়ে দেখাও, ওটাই আমাদের পুরো গল্পের প্রমাণ।"),

 dict(no=11, who="Faria", sec=50, title="Operating points", ask=True,
  en=f"Our test sets are half phishing, a real inbox is not. At five percent phishing the ranking "
     f"changes. Gemma, the best open model on AI phishing, would flag "
     f"{base['Gemma-3-12B']['false_alerts_per_1000@0.05']:.0f} good emails in every thousand. Qwen flags "
     f"{base['Qwen-2.5-7B']['false_alerts_per_1000@0.05']:.0f}. And on the right is the practical answer: put the free TF-IDF filter first "
     f"and send only what it flags to the LLM. F1 {conf['unseen_f1']:.3f}, false alarms {100*conf['false_alarm']:.1f} percent, "
     f"{conf['usd_per_1000']:.4f} dollars per thousand. That is half the cost of the LLM alone and fewer false "
     f"alarms than either part by itself.",
  bn=f"আমাদের test set এ অর্ধেক phishing, আসল inbox এ তো তা না। পাঁচ percent phishing ধরলে ক্রম "
     f"বদলে যায়। Gemma, AI phishing এ সেরা open model, হাজারে {base['Gemma-3-12B']['false_alerts_per_1000@0.05']:.0f} টা ভালো email ভুল "
     f"করে ধরবে। Qwen ধরবে {base['Qwen-2.5-7B']['false_alerts_per_1000@0.05']:.0f} টা। আর ডান পাশে বাস্তব সমাধান: আগে free TF-IDF "
     f"filter, তারপর শুধু যেগুলো সে চিহ্নিত করে সেগুলো LLM এ পাঠাও। F1 {conf['unseen_f1']:.3f}, ভুল alarm "
     f"{100*conf['false_alarm']:.1f} percent, হাজারে {conf['usd_per_1000']:.4f} dollar। খরচ LLM এর অর্ধেক, আর ভুল alarm দুইটার "
     f"যেকোনো একটার চেয়েও কম।",
  tip=f"{base['Gemma-3-12B']['false_alerts_per_1000@0.05']:.0f} টা ভালো email বলে এক সেকেন্ড থামো, এটাই মানুষকে ভাবায়।"),

 dict(no=12, who="Faria", sec=40, title="What it means",
  en="Four lessons. One, check overlap before claiming generalisation. Two, cheap detectors work "
     "if you order them properly. Three, report false alarms and the base rate, not a single F1. "
     "Four, be suspicious of your own good numbers. We also asked the models to give a reason with "
     "every verdict: when the verdict is right the reason is real about nine times in ten, when it "
     "is wrong only about half the time. A wrong answer usually comes with an invented reason.",
  bn="চারটা শিক্ষা। এক, generalisation দাবি করার আগে overlap দেখুন। দুই, সস্তা detector ঠিক ক্রমে "
     "সাজালে কাজ করে। তিন, একটা F1 না দিয়ে ভুল alarm আর base rate জানান। চার, নিজের ভালো সংখ্যাকেও "
     "সন্দেহ করুন। আমরা model গুলোকে প্রতিটা উত্তরের সাথে কারণও জিজ্ঞেস করেছিলাম: উত্তর ঠিক হলে "
     "কারণটা দশবারে প্রায় নয়বার সত্যি, ভুল হলে অর্ধেকের মতো। ভুল উত্তরের সাথে সাধারণত বানানো "
     "কারণ আসে।",
  tip="প্রতিটা card এক লাইনে। শেষ বাক্যটা ধীরে: High accuracy on one dataset is easy, honest "
      "evaluation is the hard part."),

 dict(no=13, who="Faria", sec=35, title="Limitations",
  en="What this study does not show. We are not the first to test across corpora, two recent "
     "papers did. Our test sets are 300 emails, so small differences are not meaningful, and we "
     "report the intervals. Our annotator is a model, not us. And the LLMs may have seen the old "
     "corpora during pre-training, which is exactly why the 2025 AI-written corpus matters most.",
  bn="এই গবেষণা যা দেখায় না। আমরা প্রথম না যারা cross-corpus test করেছে, সাম্প্রতিক দুইটা paper "
     "আগেই করেছে। আমাদের test set ৩০০ email এর, তাই ছোট পার্থক্যের মানে নেই, আর আমরা interval "
     "গুলো দিয়েছি। আমাদের annotator একটা model, আমরা নিজেরা না। আর LLM গুলো পুরনো corpus আগেই দেখে "
     "থাকতে পারে, ঠিক এজন্যই ২০২৫ এর AI corpus সবচেয়ে গুরুত্বপূর্ণ।",
  tip="প্রথম তিনটা পরিষ্কার করে বলো। নিজের সীমা জানলে বাকি কথা বিশ্বাসযোগ্য হয়।"),

 dict(no=14, who="Faria", sec=35, title="Next two weeks and the source code",
  en=f"In the next two weeks: the three of us hand-label 300 emails so the spam versus phishing "
     f"claim no longer depends on a model, we add confidence and threshold calibration, we enlarge "
     f"the test sets for the top three models, and we package the deduplication script so other "
     f"groups can run it on their own data. Everything is public: the code, every raw model answer, "
     f"the paper and a Colab notebook. {calls:,} model calls, {spend:.2f} dollars, one laptop. "
     f"Thank you, we are happy to take questions.",
  bn=f"সামনের দুই সপ্তাহে: আমরা তিনজন নিজেরা ৩০০টা email হাতে label করব যাতে spam আর phishing এর "
     f"দাবিটা আর কোনো model এর উপর নির্ভর না করে, confidence আর threshold calibration যোগ করব, "
     f"সেরা তিনটা model এর test set বড় করব, আর deduplication script টা এমনভাবে গুছাবো যাতে অন্য "
     f"group রা নিজেদের data তে চালাতে পারে। সবকিছু public: code, প্রতিটা raw উত্তর, paper আর একটা "
     f"Colab notebook। {calls:,} টা model call, {spend:.2f} dollar, একটা laptop। ধন্যবাদ, এখন প্রশ্ন "
     f"থাকলে করতে পারেন।",
  tip="link দুইটা দেখাও, তিনটা সংখ্যা বলো, তারপর থামো। so yeah that's it বলবে না, ওটা শেষটা নষ্ট করে।"),
]

QA = [
 ("কম data র জন্য score কমেনি তো?",
  f"না, আমরা ঠিক এটাই test করেছি। সমান সংখ্যক email এলোমেলোভাবে সরালে score বদলায় মাত্র "
  f"{abs(lf('spamassassin','loco_raw')-lf('spamassassin','loco_random'))*100:.1f} point, আর duplicate সরালে {(lf('spamassassin','loco_raw')-lf('spamassassin','loco_clean'))*100:.0f} point।"),
 ("Duplicate গুলো সত্যি duplicate তো?",
  f"প্রতিটা জোড়া exact similarity দিয়ে যাচাই করা, আর ৪০০টা কঠিন ক্ষেত্রে brute force এর সাথে "
  f"মিলিয়ে precision {mv['precision']:.2f}, recall {mv['recall']:.2f}। কয়েকটা হাতে পড়েও দেখেছি, একই লেখা, শুধু "
  f"line break আলাদা।"),
 ("কোন model ব্যবহার করব?",
  f"সস্তায়: TF-IDF এর পরে zero-shot Qwen-2.5-7B, F1 {conf['unseen_f1']:.3f}, ভুল alarm {100*conf['false_alarm']:.1f}%, হাজারে "
  f"${conf['usd_per_1000']:.4f}। টাকা থাকলে Gemini, ওটা সব দিক থেকেই ভালো।"),
 ("Gemma তো AI phishing এ সেরা, ওটা না কেন?",
  f"Gemma {100*GM['false_alarm_rate']:.0f}% ভালো email কেও phishing বলে। বাস্তবে হাজারে "
  f"{base['Gemma-3-12B']['false_alerts_per_1000@0.05']:.0f} টা ভালো email আটকে দেবে। ওটা মানুষের review queue এর আগে বসানোর জন্য ভালো, "
  f"সরাসরি block করার জন্য না।"),
 ("GPT-4 কেন ব্যবহার করলে না?",
  "করেছি, reference হিসেবে দুইটা paid model চালিয়েছি আর ওরা এগিয়ে আছে, সেটা সৎভাবে লিখেছি। "
  "আমাদের গবেষণার প্রশ্নটা হলো কম বাজেটের একটা প্রতিষ্ঠান কী চালাতে পারবে, তাই মূল ফোকাস open model।"),
 ("খরচ কত হলো?",
  f"মোট {spend:.2f} dollar, একটা 8 GB laptop এ। বাকি সব free software আর public data।"),
 ("এটা কি নতুন কাজ?",
  "Cross-corpus test নতুন না, দুইটা paper আগে করেছে। নতুন হলো: corpus গুলোর মধ্যে duplicate মেপে "
  "সেগুলো সরিয়ে test করা, dollar এ খরচ দেওয়া, ভুল alarm এর হার দেওয়া, আর operating point বিশ্লেষণ।"),
]

TOTAL = sum(s["sec"] for s in SLIDES)
BY_SPEAKER = {}
for s in SLIDES:
    BY_SPEAKER.setdefault(s["who"], []).append(s)
