# Script 3: Nowshin Anjum Faria

**Slides 7, 8, 9, 10 · about 2 minutes 40 seconds**
Your job: turn the problems Saimon exposed into a concrete plan, and close the talk. You have one optional audience moment on slide 7.

---

## English version

### Slide 7: Gaps 3 and 4 (40 sec)

Thank you Saimon.

So we have two more gaps, and both are about something the field almost never talks about: **cost**.

We ran a small open model, llama-3.2-3b, through OpenRouter. We measured the actual tokens. The cost came to **six-tenths of a cent per thousand emails**.

Now, is that number in any paper? No. In fact, Lin and his team, who worked on exactly these small models, write in their own limitations that they did **not** do a cost-benefit analysis. They left it as future work.

*(optional, ask before clicking)* Quick show of hands, who thinks a **twelve billion** parameter model beats a **three billion** parameter model at this task?

*(click)*

We tested gemma-3-12b. Four times bigger. Three times the price. And its precision fell to **0.58**, it flags almost every legitimate email as phishing. So it is worse, not better.

*(click)*

And here is what surprised us most. The small 3B model held **0.80 to 0.84 on all three corpora**. It never collapsed. Remember, the classical model fell from 0.99 to 0.30. The small LLM is fifteen points worse inside a corpus, but far more stable across corpora, and it costs half a cent.

Nobody puts accuracy, robustness and cost in the same table. But that is exactly what you need to decide what to actually deploy.

### Slide 8: Objectives (40 sec)

So here is what we will build. Six objectives.

**One: a decontaminated benchmark.** Six independent public corpora, and we publish the near-duplicate matrix as a result in itself.

**Two: leave-one-corpus-out.** We train on five corpora and always test on the sixth, which the model has never seen.

**Three: one protocol for every model family.** Classical, DistilBERT, small open LLMs, and Phishsense-1B as an external reference.

**Four: cost measured in dollars.** We log every token and convert it to US dollars per thousand emails. Measured, not described.

**Five: AI-written phishing.** We test every detector on E-PhishLLM, a public corpus of LLM-generated phishing.

And **six: one honest table** with accuracy, robustness and cost together, with confidence intervals.

All six run on our own laptops. The whole thing costs under two dollars of our five dollar budget.

### Slide 9: Proposed method (50 sec)

And this is how the pipeline works, left to right. Six stages.

**Stage one, collect.** Six free public corpora from Zenodo.

**Stage two, decontaminate.** This is the stage nobody else has. We use MinHash and LSH near-duplicate matching, and remove every email that appears in more than one corpus. Saimon showed you why: without this stage, your results are memorisation.

**Stage three, split.** Train on five corpora, test on the sixth.

**Stage four, run the models.** Classical, DistilBERT locally on CPU, and the small open LLMs, all under one identical prompt and protocol.

**Stage five, the shift test.** We run every detector on E-PhishLLM, AI-written phishing that no model has ever seen.

And one ethical point here, which matters. We do **not** generate phishing emails ourselves. We use a published, peer-reviewed corpus instead. It is cheaper, it is citable, other people can reproduce it, and we create no new attack content.

**Stage six, report.** Accuracy, robustness, and cost per thousand emails.

### Slide 10: Expected outcome and close (30 sec)

And this is what we deliver. This table.

Some cells we already have from our preliminary work. Most are question marks, and those question marks *are* the project.

Filled in properly. Deduplicated. On corpora that each model has never seen. With the cost of every row in the last column. And the code published so anyone can re-run it.

As far as we can find, this table does not exist in any paper.

*(click)*

We will finish with the one sentence that describes everything we found:

**High accuracy on one dataset is easy. Honest evaluation is the hard part.**

Thank you. We are happy to take questions.

---

## বাংলা version

### Slide 7: Gaps 3 and 4 (40 sec)

ধন্যবাদ জাকারিয়া।

আমাদের আরো দুইটা gap আছে, আর দুইটাই এমন একটা জিনিস নিয়ে যেটা নিয়ে এই field প্রায় কথাই বলে না: **খরচ**।

আমরা একটা ছোট open model, llama-3.2-3b, OpenRouter দিয়ে চালিয়েছি। আসল token গুলো measure করেছি। খরচ দাঁড়ালো **হাজার email এ আধা cent এরও কম**।

এখন, এই number টা কি কোনো paper এ আছে? না। বরং Lin আর তার team, যারা ঠিক এই ছোট model গুলো নিয়েই কাজ করেছে, তারা নিজেদের limitation এ লিখেছে যে তারা cost-benefit analysis **করেনি**। ওটা future work হিসেবে রেখে দিয়েছে।

*(ইচ্ছা করলে, click করার আগে)* হাত তুলে বলেন তো, কে কে মনে করেন **বারো বিলিয়ন** parameter এর model এই কাজে **তিন বিলিয়ন** parameter এর model কে হারাবে?

*(click)*

আমরা gemma-3-12b test করেছি। চার গুণ বড়। তিন গুণ দাম। আর তার precision নেমে গেল **0.58** এ: প্রায় প্রতিটা legitimate email কেই phishing বলে দেয়। মানে এটা ভালো না, বরং খারাপ।

*(click)*

আর যেটা আমাদের সবচেয়ে অবাক করেছে। ছোট 3B model টা **তিনটা corpus এই 0.80 থেকে 0.84** ধরে রেখেছে। একবারও ভেঙে পড়েনি। মনে করেন, classical model 0.99 থেকে 0.30 এ নেমেছিল। ছোট LLM টা নিজের corpus এ পনেরো point খারাপ, কিন্তু corpus এর বাইরে অনেক বেশি stable, আর খরচ আধা cent।

Accuracy, robustness আর cost, এই তিনটা কেউ একসাথে এক table এ দেয় না। অথচ বাস্তবে কোনটা deploy করবেন সেটা ঠিক করতে এই তিনটাই লাগে।

### Slide 8: Objectives (40 sec)

তাহলে আমরা কী বানাবো। ছয়টা objective।

**এক: একটা decontaminated benchmark।** ছয়টা স্বাধীন public corpus, আর near-duplicate matrix টা নিজেই একটা result হিসেবে publish করব।

**দুই: leave-one-corpus-out।** পাঁচটা corpus এ train করে সবসময় ছয় নম্বরটায় test করব, যেটা model কখনো দেখেনি।

**তিন: সব model family এর জন্য একই protocol।** Classical, DistilBERT, ছোট open LLM, আর reference হিসেবে Phishsense-1B।

**চার: খরচ dollar এ measure করা।** প্রতিটা token log করে হাজার email প্রতি US dollar এ রূপান্তর করব। মাপা হবে, শুধু বর্ণনা না।

**পাঁচ: AI দিয়ে লেখা phishing।** প্রতিটা detector কে E-PhishLLM এ test করব, যেটা LLM দিয়ে বানানো phishing এর একটা public corpus।

আর **ছয়: একটা সৎ table**, যেখানে accuracy, robustness আর cost একসাথে থাকবে, confidence interval সহ।

ছয়টাই আমাদের নিজেদের laptop এ চলবে। পুরো কাজটার খরচ আমাদের পাঁচ dollar budget এর মধ্যে দুই dollar এরও কম।

### Slide 9: Proposed method (50 sec)

আর pipeline টা এইভাবে কাজ করে, বাম থেকে ডানে। ছয়টা stage।

**Stage এক, collect।** Zenodo থেকে ছয়টা free public corpus।

**Stage দুই, decontaminate।** এই stage টা আর কারো নেই। আমরা MinHash আর LSH near-duplicate matching ব্যবহার করে একাধিক corpus এ থাকা প্রতিটা email বাদ দেব। জাকারিয়া দেখিয়েছে কেন: এই stage ছাড়া আপনার result টা memorization।

**Stage তিন, split।** পাঁচটা corpus এ train, ছয় নম্বরটায় test।

**Stage চার, model চালানো।** Classical, DistilBERT locally CPU তে, আর ছোট open LLM গুলো, সব একই prompt আর একই protocol এ।

**Stage পাঁচ, shift test।** প্রতিটা detector কে E-PhishLLM এ চালাবো, AI এর লেখা phishing যেটা কোনো model কখনো দেখেনি।

আর এখানে একটা ethical কথা, যেটা গুরুত্বপূর্ণ। আমরা নিজেরা phishing email **বানাবো না**। বদলে একটা published, peer-reviewed corpus ব্যবহার করব। এতে খরচ কম, cite করা যায়, অন্যরা reproduce করতে পারবে, আর আমরা নতুন কোনো attack content তৈরি করছি না।

**Stage ছয়, report।** Accuracy, robustness, আর হাজার email প্রতি খরচ।

### Slide 10: Expected outcome and close (30 sec)

আর আমরা এইটা deliver করব। এই table টা।

কিছু ঘর আমাদের preliminary কাজ থেকেই আছে। বেশিরভাগই প্রশ্নবোধক চিহ্ন, আর ওই প্রশ্নবোধক চিহ্নগুলোই আসলে আমাদের project।

ঠিকভাবে পূরণ করা। Deduplicated। এমন corpus এ যেটা প্রতিটা model কখনো দেখেনি। শেষ column এ প্রতিটা row এর খরচ সহ। আর code publish করা, যাতে যে কেউ আবার চালাতে পারে।

আমরা যতদূর খুঁজে পেয়েছি, এই table টা কোনো paper এ নেই।

*(click)*

শেষ করব একটা বাক্য দিয়ে, যেটা আমাদের পুরো কাজটাকে বর্ণনা করে:

**একটা dataset এ high accuracy পাওয়া সহজ। কঠিন কাজটা হলো সৎ evaluation।**

ধন্যবাদ। এখন প্রশ্ন থাকলে করতে পারেন।

---

## Delivery tips

- **Slide 9 is your main visual.** Walk it left to right once, do not jump around. Spend most of your time on stage 2 and stage 5, those are the two stages nobody else has.
- The ethics sentence on slide 9 ("we do not generate phishing ourselves") is worth saying clearly. It is the kind of thing a Computer Security teacher notices and rewards.
- On slide 8, do **not** read all six objectives word for word, you will run out of time. Read the bold titles, and add one extra sentence only on four and five.
- On slide 10, point at the question marks when you say "those question marks are the project."
- Deliver the final line slowly, then **stop talking**. Do not add "so yeah, that's it" afterwards, it kills the ending.
- Be ready for the most likely questions:
  - *"Why not use GPT-4?"* → Cost, and it is closed, we cannot control or reproduce version changes. Our research question is specifically about what a low-budget organisation can deploy.
  - *"Isn't 0.80 accuracy too low to be useful?"* → In-corpus, yes it is lower. But it is stable across corpora where the classical model collapses to 0.30. Which one you want depends on whether your real email looks like your training set, and it usually does not.
  - *"How do you know the LLM did not see these datasets in training?"* → We do not, fully. That is a stated limitation, and it is exactly why we added the E-PhishLLM shift test, which was generated after most training cutoffs.
