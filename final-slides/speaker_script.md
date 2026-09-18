# Final Update: Speaker Script

About 8 minutes. Sinha: slides 1 to 4. Saimon: slides 5 to 7. Faria: slides 8 to 12.
Numbers on the slides come straight from `results/final/`. If a number here
and a number on the slide ever differ, trust the slide.

Press `N` in the HTML deck to see the timing notes for each slide.

---

## Sinha

### Slide 1. Title (15 sec)

EN: Good morning. We are Group 18. In our proposal we showed you an empty
table and said the question marks were the project. Today we show it filled in.

BN: সবাইকে শুভেচ্ছা। আমরা Group 18। Proposal এ আমরা একটা খালি table দেখিয়েছিলাম,
বলেছিলাম প্রশ্নবোধক চিহ্নগুলোই আমাদের project। আজ সেই table টা পূরণ করে দেখাবো।

### Slide 2. Where we started (45 sec)

EN: Quick recap. In July every paper we read said 97 to 99 percent, but all of
them tested inside one dataset. When we trained on one corpus and tested on
another, F1 fell from 0.99 to 0.30. In August we found that Kaggle already
contains most of SpamAssassin.

Three things changed since the proposal, and we want to be open about them.
First, a 2025 paper, E-PhishGen, already tested across datasets, so our claim
is now leakage and cost. Second, Nazario is now a test-only set. Third, the
numbers 74.4 percent, 4,282 and 48 on our proposal slides came from a run we
never saved. Every number today comes from code in our repository.

So our question is simple. If we remove leaked emails and always test on a
corpus the model has never seen, how good are cheap detectors, and what do
they cost?

BN: ছোট করে বলি। জুলাইতে সব paper ৯৭ থেকে ৯৯ percent বলছিল, কিন্তু সবাই একটা
dataset এর ভিতরেই test করেছে। আমরা এক corpus এ train করে অন্যটায় test করলে F1
০.৯৯ থেকে ০.৩০ এ নেমে গেল। আগস্টে দেখলাম Kaggle এর ভিতরেই SpamAssassin এর বেশিরভাগ
email আছে।

Proposal এর পর তিনটা জিনিস বদলেছে, সেটা খোলাখুলি বলছি। এক, ২০২৫ এর E-PhishGen paper
আগেই dataset এর বাইরে test করেছে, তাই আমাদের claim এখন leakage আর cost। দুই, Nazario
এখন শুধু test set। তিন, proposal slide এর ৭৪.৪ percent, ৪,২৮২ আর ৪৮ এই সংখ্যাগুলো
এমন একটা run থেকে এসেছিল যেটা আমরা save করিনি। আজকের প্রতিটা সংখ্যা repository এর code থেকে আসা।

তাই প্রশ্নটা সহজ। leaked email সরিয়ে দিয়ে, সবসময় অদেখা corpus এ test করলে, সস্তা
detector গুলো কতটা ভালো, আর খরচ কত?

### Slide 3. Objectives (30 sec)

EN: We set six objectives. Five are fully done. The third is mostly done: we
ran every model family we promised except Phishsense-1B, because it needs a
HuggingFace access token. That is our first task for the next two weeks.

BN: আমাদের ছয়টা objective ছিল। পাঁচটা পুরো শেষ। তিন নম্বরটা প্রায় শেষ: Phishsense-1B
ছাড়া সব model চালিয়েছি, কারণ ওটার জন্য HuggingFace token লাগে। এটাই সামনের দুই
সপ্তাহের প্রথম কাজ।

### Slide 4. Methodology (45 sec)

EN: Six steps, one script each, all on one laptop. Steps two and three are
ours. We measure how many emails the corpora share, then for every corpus we
train on the other five and test on it. We do that twice: once with the
training data as it is, and once after removing every training email that has
a copy in the test corpus. The difference between the two is how much leaked
emails inflate the score. And every model, local or paid, is scored on exactly
the same emails. Saimon will show the details.

BN: ছয়টা ধাপ, প্রতিটার জন্য একটা script, সব একটা laptop এ। দুই আর তিন নম্বর ধাপ
আমাদের নিজের। প্রথমে দেখি corpus গুলো কতগুলো email share করে, তারপর প্রতিটা corpus
এর জন্য বাকি পাঁচটায় train করে ওটায় test করি। দুইবার করি: একবার data যেমন আছে, আরেকবার
test corpus এ কপি আছে এমন সব training email সরিয়ে। দুইটার পার্থক্যই হলো leaked email
score কতটা বাড়িয়ে দেয়। আর প্রতিটা model, local হোক বা paid, ঠিক একই email এ score
পায়। বিস্তারিত সাইমন দেখাবে।

---

## Saimon

### Slide 5. Experimental details (50 sec)

EN: This slide is straight from our notebook. Nine sources. Six have both
classes and take turns as the held-out corpus. Three are test only: Nazario,
real phishing; Nigerian fraud; and E-PhishLLM, phishing written by GPT-4o-mini.
Big corpora are capped at 10,000 emails, and every test set has a fixed
300-email subset. On the right are the model settings. Everything uses seed
42, runs on an 8 GB MacBook, and the total API bill was under one dollar.

BN: এই slide টা সরাসরি আমাদের notebook থেকে। নয়টা source। ছয়টায় দুই ধরনের email
আছে, এগুলো পালা করে held-out corpus হয়। তিনটা শুধু test: Nazario আসল phishing,
Nigerian fraud, আর E-PhishLLM যেটা GPT-4o-mini দিয়ে লেখা phishing। বড় corpus গুলো
১০,০০০ email এ সীমিত, আর প্রতিটা test set এ একটা নির্দিষ্ট ৩০০ email এর subset।
ডানে model এর setting। সব জায়গায় seed 42, একটা 8 GB MacBook, আর মোট API খরচ এক
dollar এর কম।

### Slide 6. Overlap (55 sec)

EN: How many SpamAssassin emails are inside the Kaggle set? If you compare the
text exactly, the way most people would, you find two. Two. If you remove
whitespace, three thousand eight hundred. With near-duplicate matching, five
thousand and nine. That is 86 percent of SpamAssassin.

Kaggle also holds 90 percent of Ling and 35 percent of Enron. Exact matching
misses it because Kaggle deleted line breaks and glued words together. We
checked 400 of these emails by brute force to make sure the matches are real.

BN: Kaggle set এর ভিতরে SpamAssassin এর কয়টা email আছে? বেশিরভাগ মানুষ যেভাবে
করবে, text হুবহু মিলালে পাওয়া যায় দুইটা। মাত্র দুইটা। whitespace সরালে তিন হাজার
আটশো। near-duplicate matching দিয়ে পাঁচ হাজার নয়টা। মানে SpamAssassin এর ৮৬ percent।

Kaggle এর ভিতরে Ling এর ৯০ percent আর Enron এর ৩৫ percent ও আছে। হুবহু মিলানো
এটা ধরতে পারে না কারণ Kaggle line break মুছে শব্দ জোড়া লাগিয়ে দিয়েছে। আমরা ৪০০টা
email brute force দিয়ে যাচাই করেছি, match গুলো আসল।

### Slide 7. Leakage inflates scores (55 sec)

EN: Remember the Kaggle to SpamAssassin transfer from July, F1 0.97? Remove
the copies and it falls to 0.67. It was memorisation.

In the leave-one-corpus-out test, cleaning costs 10 to 11 points on
SpamAssassin and Ling, and about 5 on Enron and Kaggle. Now look at CEAS and
TREC. They share almost nothing with the others, and their scores do not move
at all. That is our control: the drop appears exactly where the overlap is.
Faria will now show all the models.

BN: জুলাইয়ের Kaggle থেকে SpamAssassin এর F1 ০.৯৭ মনে আছে? কপিগুলো সরালে সেটা
নেমে যায় ০.৬৭ এ। ওটা মুখস্থ করা ছিল।

leave-one-corpus-out test এ পরিষ্কার করলে SpamAssassin আর Ling এ ১০ থেকে ১১ point
কমে, Enron আর Kaggle এ প্রায় ৫। এবার CEAS আর TREC দেখেন। এরা বাকিদের সাথে প্রায়
কিছুই share করে না, আর এদের score একটুও নড়ে না। এটাই আমাদের control: যেখানে
overlap আছে, ঠিক সেখানেই score পড়ে। এখন ফারিয়া সব model দেখাবে।

---

## Faria

### Slide 8. The main table (60 sec)

EN: This is the table from our proposal, filled in. Every model on the same
held-out emails. The highlighted row is zero-shot Qwen-2.5-7B, our
recommendation. Look at three things: the unseen-corpus F1, the AI phishing
column, and the cost column. TF-IDF is still strong on old mail but weak on
AI-written phishing. The smallest Llama is simply too weak.

BN: এটা আমাদের proposal এর table, এখন পূরণ করা। সব model একই অদেখা email এ। হাইলাইট
করা row টা zero-shot Qwen-2.5-7B, এটাই আমাদের সুপারিশ। তিনটা জিনিস দেখেন: অদেখা
corpus এ F1, AI phishing এর কলাম, আর খরচের কলাম। TF-IDF পুরনো email এ এখনো ভালো, কিন্তু
AI দিয়ে লেখা phishing এ দুর্বল। সবচেয়ে ছোট Llama এই কাজের জন্য যথেষ্ট না।

### Slide 9. What it means (60 sec)

EN: Four takeaways. One, zero-shot Qwen gives the best balance for about three
cents per thousand emails. Two, and this surprised us: few-shot examples from
old corpora make the model better on old mail but much worse on AI phishing,
because they teach it that phishing looks like old spam. Three, TF-IDF is a
free and strong baseline, but not for modern phishing. Four, bigger is not
better: Phi-4 ignored our one-word format in a third of emails.

BN: চারটা কথা। এক, zero-shot Qwen হাজার email এ প্রায় তিন cent এ সবচেয়ে ভালো ভারসাম্য
দেয়। দুই, এটা আমাদের অবাক করেছে: পুরনো corpus থেকে few-shot উদাহরণ দিলে model পুরনো
email এ ভালো করে কিন্তু AI phishing এ অনেক খারাপ করে, কারণ উদাহরণগুলো শেখায় যে
phishing দেখতে পুরনো spam এর মতো। তিন, TF-IDF বিনা খরচে শক্ত baseline, কিন্তু আধুনিক
phishing এর জন্য না। চার, বড় মানেই ভালো না: Phi-4 এক তৃতীয়াংশ email এ আমাদের এক শব্দের
উত্তরের নিয়ম মানেনি।

### Slide 10. Limitations (40 sec)

EN: Some honest limits. Four corpora count spam as positive, not only
phishing. Our test sets are 300 emails, so differences under about 0.02 do not
mean much. And the LLMs may have seen the old corpora during pre-training. That
is exactly why the newer E-PhishLLM test matters most for them.

BN: কিছু সীমাবদ্ধতা খোলাখুলি বলি। চারটা corpus শুধু phishing না, spam কেও positive
ধরে। আমাদের test set ৩০০ email এর, তাই ০.০২ এর কম পার্থক্যের তেমন মানে নেই। আর LLM
গুলো pre-training এ পুরনো corpus দেখে থাকতে পারে। এই কারণেই নতুন E-PhishLLM test টা
ওদের জন্য সবচেয়ে গুরুত্বপূর্ণ।

### Slide 11. Next two weeks (30 sec)

EN: Four small steps: run Phishsense-1B, relabel spam versus phishing on a
sample, bigger test sets for the top three models, and the Italian and German
part of E-PhishLLM. Each one reuses scripts we already have.

BN: চারটা ছোট কাজ: Phishsense-1B চালানো, একটা sample এ spam আর phishing আলাদা করে
label করা, সেরা তিনটা model এর জন্য বড় test set, আর E-PhishLLM এর ইতালিয়ান ও জার্মান
অংশ। প্রতিটাতেই আমাদের আগের script কাজে লাগবে।

### Slide 12. Source code and close (20 sec)

EN: Everything is public: the code, the results, the paper, and a Colab
notebook that rebuilds every table. We will end with the same sentence as last
time, because now we can prove it. High accuracy on one dataset is easy.
Honest evaluation is the hard part. Thank you.

BN: সবকিছু public: code, result, paper, আর একটা Colab notebook যেটা প্রতিটা table
আবার বানায়। শেষ করবো আগের বারের বাক্যটা দিয়েই, কারণ এবার আমরা এটা প্রমাণ করতে পারি।
একটা dataset এ high accuracy পাওয়া সহজ। কঠিন কাজটা হলো সৎ evaluation। ধন্যবাদ।

---

## Likely questions

- *Why not GPT-4?* Cost, and it is closed. Our question is what a small budget can deploy.
- *How do you know the near duplicates are real?* We searched 400 of them by brute force and read many by hand. Same messages, different line breaks.
- *Did the LLMs see these corpora in training?* Maybe for the old ones. E-PhishLLM is from 2025, which is why we weight it most.
- *Why did few-shot hurt on AI phishing?* The examples come from 2002 to 2008 corpora, so they anchor the model to old spam style.
- *How much did it cost?* Under one US dollar for the whole study, measured per call.
