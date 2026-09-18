# Script 3 — Nowshin Anjum Faria

**Slides 7, 8, 9, 10 · about 2 minutes 40 seconds**

Your job in one line: **turn the problems into a plan, and land the ending.** Sinha showed the field is stuck. Saimon showed why. You show the way out — and you close the talk, so the last thing the room hears is yours.

---

## The three sentences you must not miss

1. *"Is that number in any paper? No."* → about cost.
2. *"We do not generate phishing ourselves."* → the ethics line. A security teacher notices this.
3. *"High accuracy on one dataset is easy. Honest evaluation is the hard part."* → then stop talking.

---

# SLIDE 7 · Gaps 3 & 4 (40 sec) ⚡ show of hands

**On screen:** cost box, then the gemma result, then the blue box.

### English

> Thank you Saimon.
>
> We have two more gaps, and both are about something this field almost never talks about: **money.**
>
> We ran a small open model — llama-3.2-3b — through OpenRouter, and we measured the actual tokens. The cost came to **six-tenths of a cent per thousand emails.**
>
> Now, is that number in any paper? *(pause)* **No.** In fact Lin and his team, who worked on exactly these small models, write in their own limitations that they did **not** do a cost-benefit analysis. They left it as future work.
>
> *(raise your own hand while asking)*
>
> Quick show of hands — who thinks a **twelve billion** parameter model beats a **three billion** parameter model at this task?
>
> *(take the hands. smile.)*
>
> *(CLICK)*
>
> We tested gemma-3-12b. Four times bigger. Three times the price. Its precision fell to **0.58** — it flags almost every legitimate email as phishing. So bigger was not better. Bigger was **worse.**
>
> *(CLICK)*
>
> And here is what surprised us most. The small 3B model held **0.80 to 0.84 on all three corpora.** It never collapsed. Remember, the classical model fell from 0.99 to 0.30.
>
> So the small LLM is fifteen points worse inside a corpus — but far more stable outside it, for half a cent.
>
> Nobody puts accuracy, robustness and cost in the same table. But those three together are exactly what you need to decide what to actually deploy.

### বাংলা

> ধন্যবাদ সাইমন।
>
> আমাদের আরো দুইটা gap আছে, আর দুইটাই এমন একটা জিনিস নিয়ে যেটা নিয়ে এই field প্রায় কথাই বলে না: **টাকা।**
>
> আমরা একটা ছোট open model — llama-3.2-3b — OpenRouter দিয়ে চালিয়েছি, আর আসল token গুলো measure করেছি। খরচ দাঁড়ালো **হাজার email এ এক cent এরও অর্ধেক।**
>
> এখন, এই number টা কি কোনো paper এ আছে? *(pause)* **নাই।** বরং Lin আর তার team, যারা ঠিক এই ছোট model গুলো নিয়েই কাজ করেছে, তারা নিজেদের limitation এ লিখে গেছে যে তারা cost-benefit analysis **করেনি**। ওটা future work হিসেবে রেখে দিয়েছে।
>
> *(নিজের হাত তুলে জিজ্ঞেস করেন)*
>
> হাত তুলে বলেন তো — কে কে মনে করেন **বারো বিলিয়ন** parameter এর model এই কাজে **তিন বিলিয়ন** parameter এর model কে হারাবে?
>
> *(হাত গুলো দেখেন। হাসেন।)*
>
> *(CLICK)*
>
> আমরা gemma-3-12b test করেছি। চার গুণ বড়। তিন গুণ দাম। আর তার precision নেমে গেল **০.৫৮** এ — প্রায় প্রতিটা legitimate email কেই phishing বলে দেয়। মানে বড় হওয়াতে ভালো হয়নি। বড় হওয়াতে **খারাপ** হয়েছে।
>
> *(CLICK)*
>
> আর যেটা আমাদের সবচেয়ে অবাক করেছে — ছোট 3B model টা **তিনটা corpus এই ০.৮০ থেকে ০.৮৪** ধরে রেখেছে। একবারও ভেঙে পড়েনি। মনে করেন, classical model ০.৯৯ থেকে ০.৩০ এ নেমেছিল।
>
> তাহলে ছোট LLM টা নিজের corpus এ পনেরো point খারাপ — কিন্তু corpus এর বাইরে অনেক বেশি stable, আর খরচ আধা cent।
>
> Accuracy, robustness আর cost — এই তিনটা কেউ একসাথে এক table এ দেয় না। অথচ বাস্তবে কোনটা deploy করবেন, সেটা ঠিক করতে এই তিনটাই একসাথে লাগে।

**Cue:** the show of hands works because most people will raise their hand for the bigger model. When you reveal that it is worse, that is a small, satisfying surprise. Do not skip it.

---

# SLIDE 8 · Objectives (40 sec)

**On screen:** six numbered objectives.

### English

> So here is what we will actually build. Six objectives — I will read the titles, not the whole slide.
>
> **One, a decontaminated benchmark.** Six independent public corpora, and we publish the near-duplicate matrix as a result in itself.
>
> **Two, leave-one-corpus-out.** We train on five corpora, and always test on the sixth — one the model has never seen.
>
> **Three, one protocol for every model family.** Classical, DistilBERT, small open LLMs, and Phishsense-1B as an external reference.
>
> **Four, cost measured in dollars.** *(slow down here)* We log every token and convert it to US dollars per thousand emails. Measured — not described with adjectives.
>
> **Five, AI-written phishing.** *(slow down here too)* We test every detector on E-PhishLLM, a public corpus of LLM-generated phishing — the attack that is actually growing right now.
>
> And **six, one honest table** — accuracy, robustness and cost together, with confidence intervals.
>
> All six run on our own laptops. The whole thing costs under two dollars of our five dollar budget.

### বাংলা

> তাহলে আমরা আসলে কী বানাবো। ছয়টা objective — আমি শুধু শিরোনামগুলো পড়ব, পুরো slide না।
>
> **এক, একটা decontaminated benchmark।** ছয়টা স্বাধীন public corpus, আর near-duplicate matrix টা নিজেই একটা result হিসেবে publish করব।
>
> **দুই, leave-one-corpus-out।** পাঁচটা corpus এ train করে সবসময় ছয় নম্বরটায় test করব — যেটা model কখনো দেখেনি।
>
> **তিন, সব model family এর জন্য একই protocol।** Classical, DistilBERT, ছোট open LLM, আর external reference হিসেবে Phishsense-1B।
>
> **চার, খরচ dollar এ measure করা।** *(এখানে ধীরে)* প্রতিটা token log করে হাজার email প্রতি US dollar এ রূপান্তর করব। মাপা হবে — বিশেষণ দিয়ে বর্ণনা না।
>
> **পাঁচ, AI দিয়ে লেখা phishing।** *(এখানেও ধীরে)* প্রতিটা detector কে E-PhishLLM এ test করব — LLM দিয়ে বানানো phishing এর একটা public corpus। এই attack টাই এখন আসলে বাড়ছে।
>
> আর **ছয়, একটা সৎ table** — accuracy, robustness আর cost একসাথে, confidence interval সহ।
>
> ছয়টাই আমাদের নিজেদের laptop এ চলবে। পুরো কাজটার খরচ আমাদের পাঁচ dollar budget এর মধ্যে দুই dollar এরও কম।

**Cue:** do **not** read all six in full sentences — you will run out of time. Titles only, plus one extra line on four and five. Those two are the new ones.

---

# SLIDE 9 · Proposed method (50 sec)

**On screen:** six-stage pipeline, left to right.

### English

> And this is how the pipeline works, left to right. Six stages.
>
> **Stage one — collect.** Six free public corpora from Zenodo.
>
> **Stage two — decontaminate.** *(point at it)* This is the stage nobody else has. MinHash and LSH near-duplicate matching, and we remove every email that appears in more than one corpus. Saimon just showed you why: without this stage, your result is memorisation, not detection.
>
> **Stage three — split.** Train on five corpora, test on the sixth.
>
> **Stage four — run the models.** Classical, DistilBERT locally on CPU, and the small open LLMs — all under one identical prompt and one identical protocol, so the comparison is fair.
>
> **Stage five — the shift test.** Every detector gets run on E-PhishLLM: AI-written phishing that no model has ever seen.
>
> And one ethical point here, which matters. We do **not** generate phishing emails ourselves. We use a published, peer-reviewed corpus instead. It is cheaper, it is citable, other people can reproduce it — and we create no new attack content.
>
> **Stage six — report.** Accuracy, robustness, and cost per thousand emails.

### বাংলা

> আর pipeline টা এইভাবে কাজ করে, বাম থেকে ডানে। ছয়টা stage।
>
> **Stage এক — collect।** Zenodo থেকে ছয়টা free public corpus।
>
> **Stage দুই — decontaminate।** *(আঙুল দিয়ে দেখান)* এই stage টা আর কারো নাই। MinHash আর LSH দিয়ে near-duplicate matching, আর একাধিক corpus এ থাকা প্রতিটা email বাদ দেওয়া। সাইমন এইমাত্র দেখালো কেন — এই stage ছাড়া আপনার result টা detection না, memorization।
>
> **Stage তিন — split।** পাঁচটা corpus এ train, ছয় নম্বরটায় test।
>
> **Stage চার — model চালানো।** Classical, DistilBERT locally CPU তে, আর ছোট open LLM গুলো — সব একই prompt আর একই protocol এ, যাতে তুলনাটা fair হয়।
>
> **Stage পাঁচ — shift test।** প্রতিটা detector কে E-PhishLLM এ চালাবো: AI এর লেখা phishing, যেটা কোনো model কখনো দেখেনি।
>
> আর এখানে একটা ethical কথা, যেটা গুরুত্বপূর্ণ। আমরা নিজেরা phishing email **বানাবো না**। বদলে একটা published, peer-reviewed corpus ব্যবহার করব। এতে খরচ কম, cite করা যায়, অন্যরা reproduce করতে পারবে — আর আমরা নতুন কোনো attack content তৈরি করছি না।
>
> **Stage ছয় — report।** Accuracy, robustness, আর হাজার email প্রতি খরচ।

**Cue:** walk the pipeline left to right **once**. Do not jump around. Spend most of your time on stage 2 and stage 5 — those are the two stages nobody else does.

---

# SLIDE 10 · Expected outcome and close (30 sec)

**On screen:** the results table, mostly question marks. Then the closing line.

### English

> And this is what we deliver. This one table.
>
> A few cells we already have from our preliminary work. Most of them are question marks — *(point at them)* — and those question marks **are** the project.
>
> Filled in properly. Deduplicated. On corpora that each model has never seen. With the real cost of every row in the last column. And the code published, so anyone can re-run it.
>
> As far as we can find, this table does not exist in any paper.
>
> *(CLICK)*
>
> *(slow down, look up, one sentence)*
>
> **High accuracy on one dataset is easy. Honest evaluation is the hard part.**
>
> Thank you. We are happy to take questions.

### বাংলা

> আর আমরা এইটা deliver করব। এই একটা table।
>
> কয়েকটা ঘর আমাদের preliminary কাজ থেকেই আছে। বেশিরভাগই প্রশ্নবোধক চিহ্ন — *(দেখান)* — আর ওই প্রশ্নবোধক চিহ্নগুলোই **আসলে** আমাদের project।
>
> ঠিকভাবে পূরণ করা। Deduplicated। এমন corpus এ, যেটা প্রতিটা model কখনো দেখেনি। শেষ column এ প্রতিটা row এর আসল খরচ সহ। আর code publish করা, যাতে যে কেউ আবার চালাতে পারে।
>
> আমরা যতদূর খুঁজে পেয়েছি, এই table টা কোনো paper এ নাই।
>
> *(CLICK)*
>
> *(ধীরে, মুখ তুলে, একটা বাক্য)*
>
> **একটা dataset এ high accuracy পাওয়া সহজ। কঠিন কাজটা হলো সৎ evaluation।**
>
> ধন্যবাদ। এখন প্রশ্ন থাকলে করতে পারেন।

---

## Delivery notes for you specifically

- Deliver the last line slowly, then **stop talking.** Do not add *"so yeah, that's it"* — it kills the ending. Silence, then applause.
- Point at the question marks with your hand when you say *"those question marks are the project."* Physical gestures make a static table feel alive.
- The ethics sentence on slide 9 is free marks in a Computer Security course. Say it clearly, do not rush past it.
- You close the talk, so stand still and face the room for the final sentence. No looking at the screen.

## Questions likely to come to YOU

- *"Why not use GPT-4?"* → Cost, and it is closed — we cannot control or reproduce version changes. Our research question is specifically about what a low-budget organisation can actually deploy.
- *"Isn't 0.80 accuracy too low to be useful?"* → In-corpus, yes, it is lower. But it is stable across corpora, where the classical model collapses to 0.30. Which one you want depends on whether your real email looks like your training data — and it usually does not.
- *"How do you know the LLM did not see these datasets during training?"* → We do not, fully. That is a stated limitation, and it is exactly why we added the E-PhishLLM shift test, which was generated after most training cutoffs.
- *"Is five dollars really enough?"* → Our full preliminary run cost under one cent. The planned experiments cost under two dollars. Everything else runs on CPU on our own laptops.
