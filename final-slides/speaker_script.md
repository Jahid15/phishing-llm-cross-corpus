# Presentation script, 14 slides, about 9 minutes 45 seconds

| Who | Slides | Time |
|---|---|---|
| Sinha | 1 to 5 | 2:50 |
| Saimon | 6 to 9 | 3:20 |
| Faria | 10 to 14 | 3:35 |

প্রতিটা slide এ তিনটা জিনিস: **কী বলবে (English)**, **কী বলবে (বাংলা)**, আর **কীভাবে বলবে**.
দুইটা ভাষার যেকোনো একটা বলো, মিশিয়ে বললেও সমস্যা নেই. সব সংখ্যা `results/final/` থেকে আসা.

Practice করার সহজ উপায়: `final-slides/PRACTICE.html` খোলো, সেখানে slide আর script পাশাপাশি
দেখা যায়, timer সহ. আসল presentation অবশ্যই `final_deck.html` বা `final_deck.pptx` থেকেই হবে.

---

# SINHA · slides 1 to 5 · 2:50

## Slide 1 · Title (15 sec)

**EN:** Good morning. We are Group 18. In the proposal we showed you an empty table and said the question marks were the project. Today the table is full, and some of what we found surprised us.

**BN:** সবাইকে শুভেচ্ছা। আমরা Group 18। Proposal এ আমরা একটা খালি table দেখিয়ে বলেছিলাম, ওই প্রশ্নবোধক চিহ্নগুলোই আমাদের project। আজ table টা পূরণ করা, আর কিছু ফলাফল আমাদের নিজেদেরকেই অবাক করেছে।

**কীভাবে:** হাসিমুখে, ধীরে। নাম তিনটা বলার দরকার নেই, slide এ আছে।

## Slide 2 · Where we started (35 sec)

**EN:** Quick recap. In July we tested the papers' claim ourselves with TF-IDF and logistic regression, a method older than deep learning, and got the same 97 to 99 percent. Then we trained on one corpus and tested on another, and F1 fell from 0.99 to 0.30. Since the proposal we corrected three things. We are not the first to test across corpora, two recent papers did that. We added a control. And we now verify every duplicate exactly instead of trusting an estimate. So our question is: if we remove the leaked emails and always test on a corpus the model has never seen, how good are cheap detectors, what do they cost, and how much good mail do they block?

**BN:** ছোট করে আগের কথা। জুলাইতে আমরা নিজেরাই paper গুলোর দাবি যাচাই করেছিলাম TF-IDF আর Logistic Regression দিয়ে, যেটা deep learning এরও পুরনো, আর একই ৯৭ থেকে ৯৯ percent পেয়েছিলাম। তারপর এক corpus এ train করে আরেকটায় test করলাম, F1 ০.৯৯ থেকে ০.৩০ এ নেমে গেল। Proposal এর পর তিনটা জিনিস ঠিক করেছি। এক, আমরাই প্রথম না, সাম্প্রতিক দুইটা paper আগেই cross-corpus test করেছে। দুই, আমরা একটা control যোগ করেছি। তিন, প্রতিটা duplicate এখন আন্দাজে না, হিসাব করে মিলিয়ে দেখা। তাই আমাদের প্রশ্ন হলো: leaked email সরিয়ে, সবসময় অদেখা corpus এ test করলে সস্তা detector গুলো কতটা ভালো, খরচ কত, আর কতটা ভালো email আটকে দেয়?

**কীভাবে:** শেষ প্রশ্নটা নীল box এ আছে, ওটা দেখিয়ে এক সেকেন্ড থামো।

## Slide 3 · Objectives (35 sec)

**EN:** These were our six objectives in the proposal. All six are done. And after review we added four more: what the corpora actually contain, what happens at a realistic amount of phishing, two-stage detectors, and whether the models' explanations are any good. Review made the project bigger, not smaller.

**BN:** Proposal এ আমাদের ছয়টা objective ছিল। ছয়টাই শেষ। Review এর পর আরো চারটা যোগ হয়েছে: corpus গুলোতে আসলে কী আছে, বাস্তবে যত phishing আসে তত হলে কী হয়, দুই ধাপের detector, আর model এর দেওয়া কারণগুলো আদৌ ভালো কিনা। Review কাজটা ছোট করেনি, বরং বড় করেছে।

**কীভাবে:** পুরো table পড়বে না। শুধু বলো ছয়টাই done, আর শেষ লাল row টা দেখাও।

## Slide 4 · Methodology (40 sec)

**EN:** Six steps, one script each. The step to look at is number three, the control. Removing duplicates also removes training data, so on its own a drop could just mean less data. That is why we run a third setting that removes the same number of emails at random. If the random version does not drop, the cause is the duplicates. And every model, free, open or paid, is scored on exactly the same 300 emails per test set.

**BN:** ছয়টা ধাপ, প্রতিটার জন্য একটা script। যেটা খেয়াল করতে হবে সেটা তিন নম্বর, মানে control। Duplicate সরালে training data ও কমে যায়, তাই score কমলে সেটা শুধু কম data র কারণেও হতে পারত। এজন্য তৃতীয় একটা setting এ আমরা সমান সংখ্যক email এলোমেলোভাবে সরাই। এলোমেলো version এ score না কমলে বুঝতে হবে কারণ duplicate গুলোই। আর প্রতিটা model, free হোক, open হোক বা টাকা দিয়ে কেনা, প্রতি test set এ ঠিক একই ৩০০টা email এ score পায়।

**কীভাবে:** লাল box টায় আঙুল দেখাও। এই control টাই পুরো argument বাঁচায়।

## Slide 5 · Experimental details (from the notebook) (45 sec)

**EN:** This slide is straight from our notebook. Nine email sources. Six of them take turns as the held-out corpus, three are test only, including E-PhishLLM which is written by GPT-4o and GPT-4o-mini. On the right are the settings: TF-IDF, DistilBERT trained on the laptop CPU, six small open LLMs, three published phishing detectors and two paid models, all under one prompt. Seed 42, one 8 GB laptop, every raw answer saved, total API spend 1.58 dollars. Saimon will show what we found.

**BN:** এই slide টা সরাসরি আমাদের notebook থেকে। নয়টা email source। তার ছয়টা পালা করে held-out corpus হয়, তিনটা শুধু test এর জন্য, যার মধ্যে E-PhishLLM হলো GPT-4o আর GPT-4o-mini দিয়ে লেখা। ডান পাশে setting গুলো: TF-IDF, laptop CPU তে train করা DistilBERT, ছয়টা ছোট open LLM, তিনটা published phishing detector আর দুইটা paid model, সবাই একই prompt এ। Seed 42, একটা 8 GB laptop, প্রতিটা raw উত্তর সংরক্ষিত, মোট API খরচ 1.58 dollar। এখন সাইমন দেখাবে আমরা কী পেয়েছি।

**কীভাবে:** মোট খরচ 1.58 dollar কথাটা জোর দিয়ে বলো, শিক্ষক এটা মনে রাখেন।

---

# SAIMON · slides 6 to 9 · 3:20

## Slide 6 · Overlap between corpora (55 sec)  ⚡ এখানে audience কে প্রশ্ন করো

**EN:** Thank you Sinha. A question for you all: the Kaggle phishing dataset and SpamAssassin are two different public datasets. How many emails do you think they have in common? [wait 2 seconds, take one guess] If you compare the text exactly, the way anyone would, you find 2. With whitespace removed, 3,850. With near-duplicate matching, 5,032, which is 87 percent of SpamAssassin. 93 percent of the Kaggle corpus has a copy somewhere else. We verified this against brute force: precision 1.00, recall 1.00.

**BN:** ধন্যবাদ সিনহা। সবাইকে একটা প্রশ্ন: Kaggle phishing dataset আর SpamAssassin, দুইটা আলাদা public dataset। আপনাদের মনে হয় এদের মধ্যে কয়টা email একই? [২ সেকেন্ড অপেক্ষা করো, একটা guess নাও] হুবহু text মিলালে, যেভাবে যে কেউ মিলাবে, পাওয়া যায় 2 টা। Whitespace বাদ দিলে 3,850 টা। আর near-duplicate matching দিয়ে 5,032 টা, মানে SpamAssassin এর 87 percent। Kaggle corpus এর 93 percent এর copy অন্য কোথাও না কোথাও আছে। এটা আমরা brute force দিয়ে যাচাই করেছি: precision 1.00, recall 1.00।

**কীভাবে:** তিনটা সংখ্যা ধীরে বলো: দুই, তিন হাজার আটশ, পাঁচ হাজার। প্রথমটায় থেমে যাও, ওটাই ধাক্কা।

## Slide 7 · Leakage inflates scores, and the control (60 sec)  ⭐ সবচেয়ে গুরুত্বপূর্ণ slide

**EN:** Now why that matters. Look at the SpamAssassin row. Train on the other five corpora as they are: F1 0.947. Now remove the same number of training emails, but pick them at random: 0.947. No change. Now remove the duplicates instead: 0.840. Up to twelve points disappear, and only when we remove the right emails. That is the control, and it is the reason we can say this is leakage and not just less data. CEAS and TREC, which share nothing with the others, do not move at all.

**BN:** এবার কেন এটা গুরুত্বপূর্ণ। SpamAssassin row টা দেখেন। বাকি পাঁচটা corpus যেমন আছে তেমন train করলে F1 0.947। এবার সমান সংখ্যক training email সরাই, কিন্তু এলোমেলোভাবে বেছে: 0.947। কোনো পরিবর্তন নেই। এবার duplicate গুলো সরাই: 0.840। বারো point পর্যন্ত উধাও, আর সেটা কেবল ঠিক email গুলো সরালেই। এটাই আমাদের control, আর এজন্যই আমরা বলতে পারি এটা leakage, শুধু কম data না। CEAS আর TREC, যাদের সাথে কারো মিল নেই, একটুও নড়ে না।

**কীভাবে:** এক row ধরে তিনটা সংখ্যা বাম থেকে ডানে পড়ো, তারপর লাল box। এই slide এ তাড়াহুড়া করবে না।

## Slide 8 · What the benchmarks actually contain (45 sec)

**EN:** Then we asked a different question: what is actually inside the positive class? We had an LLM label every positive email as phishing or spam, with a second model on 300 of them to check agreement, 86 percent. Only 15 to 25 percent of those emails are phishing. The rest is ordinary bulk advertising. So when a paper says phishing detection on these corpora, it is mostly measuring spam detection.

**BN:** এরপর আমরা অন্য একটা প্রশ্ন করলাম: positive class এর ভিতরে আসলে কী আছে? একটা LLM দিয়ে প্রতিটা positive email কে phishing না spam হিসেবে label করালাম, আর ৩০০টায় দ্বিতীয় একটা model দিয়ে মিলিয়ে দেখলাম, মিল 86 percent। দেখা গেল ওই email গুলোর মাত্র 15 থেকে 25 percent আসলে phishing। বাকিটা সাধারণ বিজ্ঞাপন। মানে কোনো paper যখন এই corpus এ phishing detection বলে, সে আসলে বেশিরভাগ spam detection মাপছে।

**কীভাবে:** হলুদ box এর সংখ্যাটা বলো, তারপর এক সেকেন্ড থামো।

## Slide 9 · A token that looked like a shortcut (40 sec)

**EN:** One more check, this time on our own result. The AI-written corpus writes every phishing link as a placeholder token. It is in 94 of our 150 phishing emails and in none of the legitimate ones. Comparing emails that have it with emails that do not says the token is worth 16 points of recall, which would make our AI numbers meaningless. But when we delete the token from the same emails and ask the models again, the answers move by 0.9 points. The first test was comparing different kinds of email. The result stands. Faria will take the model comparison.

**BN:** আরেকটা যাচাই, এবার নিজেদের ফলাফলের উপর। AI দিয়ে লেখা corpus এ প্রতিটা phishing link একটা placeholder token দিয়ে লেখা। আমাদের ১৫০টা phishing email এর ৯৪টায় সেটা আছে, আর legitimate কোনোটায় নেই। যেগুলোতে token আছে আর যেগুলোতে নেই, এদের তুলনা করলে মনে হয় token টা 16 point recall এর সমান, তাহলে তো আমাদের AI এর ফলাফল অর্থহীন। কিন্তু একই email থেকে token মুছে আবার জিজ্ঞেস করলে উত্তর বদলায় মাত্র 0.9 point। প্রথম test টা আসলে দুই ধরনের email তুলনা করছিল। ফলাফল টিকে গেছে। এখন ফারিয়া model গুলোর তুলনা দেখাবে।

**কীভাবে:** গল্পের মতো বলো: আমাদের নিজের ভালো ফলটা সন্দেহ হলো, তাই পরীক্ষা করলাম।

---

# FARIA · slides 10 to 14 · 3:35

## Slide 10 · Every detector on the same emails (55 sec)

**EN:** Thank you Saimon. This is the table our proposal promised. Twenty detectors, the same emails. Read three rows. Gemini, a paid model, is best: 0.960 with 2 percent false alarms. Zero-shot Qwen-2.5-7B is the best open model: 0.928 for about three cents per thousand emails. Now the interesting row: the published BERT phishing detector scores 0.962 on our corpora, the highest number in the table, and 0.470 on AI-written phishing. It was trained on the same corpora we test on.

**BN:** ধন্যবাদ সাইমন। এই table টাই আমাদের proposal এ দেওয়া কথা। বিশটা detector, একই email। তিনটা row পড়ুন। Gemini, একটা paid model, সবার সেরা: 0.960, ভুল alarm 2 percent। Zero-shot Qwen-2.5-7B সেরা open model: 0.928, হাজার email এ প্রায় তিন cent। এবার মজার row টা: published BERT phishing detector আমাদের corpus এ পায় 0.962, table এর সর্বোচ্চ, আর AI এর লেখা phishing এ পায় 0.470। কারণ ওটা ঠিক সেই corpus গুলোতেই train করা যেগুলোতে আমরা test করছি।

**কীভাবে:** শুধু তিনটা row। শেষ row টা আঙুল দিয়ে দেখাও, ওটাই আমাদের পুরো গল্পের প্রমাণ।

## Slide 11 · Operating points (50 sec)  ⚡ এখানে audience কে প্রশ্ন করো

**EN:** Our test sets are half phishing, a real inbox is not. At five percent phishing the ranking changes. Gemma, the best open model on AI phishing, would flag 239 good emails in every thousand. Qwen flags 28. And on the right is the practical answer: put the free TF-IDF filter first and send only what it flags to the LLM. F1 0.911, false alarms 1.1 percent, 0.0161 dollars per thousand. That is half the cost of the LLM alone and fewer false alarms than either part by itself.

**BN:** আমাদের test set এ অর্ধেক phishing, আসল inbox এ তো তা না। পাঁচ percent phishing ধরলে ক্রম বদলে যায়। Gemma, AI phishing এ সেরা open model, হাজারে 239 টা ভালো email ভুল করে ধরবে। Qwen ধরবে 28 টা। আর ডান পাশে বাস্তব সমাধান: আগে free TF-IDF filter, তারপর শুধু যেগুলো সে চিহ্নিত করে সেগুলো LLM এ পাঠাও। F1 0.911, ভুল alarm 1.1 percent, হাজারে 0.0161 dollar। খরচ LLM এর অর্ধেক, আর ভুল alarm দুইটার যেকোনো একটার চেয়েও কম।

**কীভাবে:** 239 টা ভালো email বলে এক সেকেন্ড থামো, এটাই মানুষকে ভাবায়।

## Slide 12 · What it means (40 sec)

**EN:** Four lessons. One, check overlap before claiming generalisation. Two, cheap detectors work if you order them properly. Three, report false alarms and the base rate, not a single F1. Four, be suspicious of your own good numbers. We also asked the models to give a reason with every verdict: when the verdict is right the reason is real about nine times in ten, when it is wrong only about half the time. A wrong answer usually comes with an invented reason.

**BN:** চারটা শিক্ষা। এক, generalisation দাবি করার আগে overlap দেখুন। দুই, সস্তা detector ঠিক ক্রমে সাজালে কাজ করে। তিন, একটা F1 না দিয়ে ভুল alarm আর base rate জানান। চার, নিজের ভালো সংখ্যাকেও সন্দেহ করুন। আমরা model গুলোকে প্রতিটা উত্তরের সাথে কারণও জিজ্ঞেস করেছিলাম: উত্তর ঠিক হলে কারণটা দশবারে প্রায় নয়বার সত্যি, ভুল হলে অর্ধেকের মতো। ভুল উত্তরের সাথে সাধারণত বানানো কারণ আসে।

**কীভাবে:** প্রতিটা card এক লাইনে। শেষ বাক্যটা ধীরে: High accuracy on one dataset is easy, honest evaluation is the hard part.

## Slide 13 · Limitations (35 sec)

**EN:** What this study does not show. We are not the first to test across corpora, two recent papers did. Our test sets are 300 emails, so small differences are not meaningful, and we report the intervals. Our annotator is a model, not us. And the LLMs may have seen the old corpora during pre-training, which is exactly why the 2025 AI-written corpus matters most.

**BN:** এই গবেষণা যা দেখায় না। আমরা প্রথম না যারা cross-corpus test করেছে, সাম্প্রতিক দুইটা paper আগেই করেছে। আমাদের test set ৩০০ email এর, তাই ছোট পার্থক্যের মানে নেই, আর আমরা interval গুলো দিয়েছি। আমাদের annotator একটা model, আমরা নিজেরা না। আর LLM গুলো পুরনো corpus আগেই দেখে থাকতে পারে, ঠিক এজন্যই ২০২৫ এর AI corpus সবচেয়ে গুরুত্বপূর্ণ।

**কীভাবে:** প্রথম তিনটা পরিষ্কার করে বলো। নিজের সীমা জানলে বাকি কথা বিশ্বাসযোগ্য হয়।

## Slide 14 · Next two weeks and the source code (35 sec)

**EN:** In the next two weeks: the three of us hand-label 300 emails so the spam versus phishing claim no longer depends on a model, we add confidence and threshold calibration, we enlarge the test sets for the top three models, and we package the deduplication script so other groups can run it on their own data. Everything is public: the code, every raw model answer, the paper and a Colab notebook. 40,498 model calls, 1.58 dollars, one laptop. Thank you, we are happy to take questions.

**BN:** সামনের দুই সপ্তাহে: আমরা তিনজন নিজেরা ৩০০টা email হাতে label করব যাতে spam আর phishing এর দাবিটা আর কোনো model এর উপর নির্ভর না করে, confidence আর threshold calibration যোগ করব, সেরা তিনটা model এর test set বড় করব, আর deduplication script টা এমনভাবে গুছাবো যাতে অন্য group রা নিজেদের data তে চালাতে পারে। সবকিছু public: code, প্রতিটা raw উত্তর, paper আর একটা Colab notebook। 40,498 টা model call, 1.58 dollar, একটা laptop। ধন্যবাদ, এখন প্রশ্ন থাকলে করতে পারেন।

**কীভাবে:** link দুইটা দেখাও, তিনটা সংখ্যা বলো, তারপর থামো। so yeah that's it বলবে না, ওটা শেষটা নষ্ট করে।

---

# যে প্রশ্নগুলো আসবেই

**কম data র জন্য score কমেনি তো?**
না, আমরা ঠিক এটাই test করেছি। সমান সংখ্যক email এলোমেলোভাবে সরালে score বদলায় মাত্র 0.0 point, আর duplicate সরালে 11 point।

**Duplicate গুলো সত্যি duplicate তো?**
প্রতিটা জোড়া exact similarity দিয়ে যাচাই করা, আর ৪০০টা কঠিন ক্ষেত্রে brute force এর সাথে মিলিয়ে precision 1.00, recall 1.00। কয়েকটা হাতে পড়েও দেখেছি, একই লেখা, শুধু line break আলাদা।

**কোন model ব্যবহার করব?**
সস্তায়: TF-IDF এর পরে zero-shot Qwen-2.5-7B, F1 0.911, ভুল alarm 1.1%, হাজারে $0.0161। টাকা থাকলে Gemini, ওটা সব দিক থেকেই ভালো।

**Gemma তো AI phishing এ সেরা, ওটা না কেন?**
Gemma 25% ভালো email কেও phishing বলে। বাস্তবে হাজারে 239 টা ভালো email আটকে দেবে। ওটা মানুষের review queue এর আগে বসানোর জন্য ভালো, সরাসরি block করার জন্য না।

**GPT-4 কেন ব্যবহার করলে না?**
করেছি, reference হিসেবে দুইটা paid model চালিয়েছি আর ওরা এগিয়ে আছে, সেটা সৎভাবে লিখেছি। আমাদের গবেষণার প্রশ্নটা হলো কম বাজেটের একটা প্রতিষ্ঠান কী চালাতে পারবে, তাই মূল ফোকাস open model।

**খরচ কত হলো?**
মোট 1.58 dollar, একটা 8 GB laptop এ। বাকি সব free software আর public data।

**এটা কি নতুন কাজ?**
Cross-corpus test নতুন না, দুইটা paper আগে করেছে। নতুন হলো: corpus গুলোর মধ্যে duplicate মেপে সেগুলো সরিয়ে test করা, dollar এ খরচ দেওয়া, ভুল alarm এর হার দেওয়া, আর operating point বিশ্লেষণ।

