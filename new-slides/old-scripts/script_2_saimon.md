# Script 2: Md. Jakaria Alam Saimon

**Slides 4, 5, 6 · about 2 minutes 20 seconds**
Your job: this is the **interactive part** of the talk and the part that contains our own original results. You have two audience moments. Use them.

---

## English version

### Slide 4: We reproduced it (35 sec)

Thank you Sinha.

We did not just believe those papers. We tested the story ourselves, on three public corpora. The Kaggle set, about seventeen and a half thousand emails. SpamAssassin, about six thousand. And Nazario phishing paired with Enron legitimate mail, about three thousand.

Now, what model did we use? Not GPT-4. Not RoBERTa. We used **TF-IDF with Logistic Regression**, the old classical method Sinha mentioned.

And look at the result. **97.9. 97.3. 99.2 percent.**

No LLM. No GPU. A technique older than deep learning. And it lands in exactly the same 97 to 99 percent band as GPT-4.

*(click)*

So phishing detection is solved… right?

### Slide 5: Gap 1, the collapse (50 sec) ⚡ INTERACTIVE

Let's actually check.

So we did something simple. We trained the model on **one** corpus, and then tested it on a **completely different** corpus. Because that is what happens in real life, real phishing emails do not come from your training set.

On its own corpus, this model scored F1 **0.992**. Almost perfect.

Now, can anyone guess what it became on the new corpus?

> **[PAUSE. Really wait. Take one or two guesses.**
> **If nobody speaks: "Just shout a number, higher or lower than 0.9?"]**

*(click)*

It became **zero point three zero four**.

From 0.99 to 0.30.

And here is the part that worries us most. What the model actually does is answer "legitimate" to almost every phishing email it has not seen before. So it misses most of the phishing, but the **accuracy** only drops to 0.69, which still looks acceptable on paper.

That means a paper reporting only accuracy would hide this completely. And not one paper in our review evaluates this way.

### Slide 6: Gap 2, the contamination (55 sec) ⚡ INTERACTIVE

It gets worse. And this is our newest result.

One transfer direction actually looked *great*. Kaggle to SpamAssassin, F1 0.97. Almost no drop.

Now, should we be happy about that? No. We were suspicious. Because the Kaggle set is not an original collection. It is an **aggregate**, built by merging older corpora together.

So we hashed every single email body and counted the duplicates.

*(click)*

**74.4 percent of SpamAssassin is sitting inside the Kaggle dataset.** Four thousand two hundred and eighty-two emails. The same messages, in both datasets.

*(click)*

And look at the other side. The one pair that shares **zero** emails: that is exactly the pair where performance collapsed to 0.35.

So the contamination explains the results almost perfectly. That "good transfer" was not generalisation. It was **memorisation**.

*(click)*

And now the part we are most proud of. When we ran a normal **exact**-duplicate check (the standard method, the one any careful researcher would run) it found only **48** duplicates. Only when we used **near**-duplicate matching did we find 4,282.

Why the difference? Because in one dataset the subject line was kept, and in the other it was stripped. One missing line, and 99 percent of the contamination becomes invisible.

*(click)*

So that good transfer was memorisation, not generalisation. And no paper in our review even checks whether the benchmarks they use overlap each other.

Faria will now show how we plan to fix all this.

---

## বাংলা version

### Slide 4: We reproduced it (35 sec)

ধন্যবাদ সিনহা।

আমরা শুধু ওই paper গুলো বিশ্বাস করে বসে থাকিনি। নিজেরাই গল্পটা test করেছি, তিনটা public corpus এর উপর। Kaggle set, প্রায় সাড়ে সতেরো হাজার email। SpamAssassin, প্রায় ছয় হাজার। আর Nazario phishing এর সাথে Enron এর legitimate mail, প্রায় তিন হাজার।

এখন, আমরা কোন model ব্যবহার করেছি? GPT-4 না। RoBERTa ও না। আমরা ব্যবহার করেছি **TF-IDF আর Logistic Regression**, সিনহা যেই পুরনো classical method এর কথা বলল।

আর result টা দেখেন। **97.9। 97.3। 99.2 percent।**

কোনো LLM নেই। GPU নেই। Deep learning এরও আগের একটা technique। আর সেটা GPT-4 এর মতোই ঠিক 97 থেকে 99 percent এর ঘরেই পড়েছে।

*(click)*

তাহলে তো phishing detection solved… তাই না?

### Slide 5: Gap 1, the collapse (50 sec) ⚡ INTERACTIVE

চলেন সত্যিই check করে দেখি।

আমরা খুব simple একটা কাজ করলাম। **একটা** corpus এ model train করলাম, আর test করলাম **সম্পূর্ণ আলাদা** একটা corpus এ। কারণ বাস্তবে তো এটাই হয়, আসল phishing email আপনার training set থেকে আসে না।

নিজের corpus এ এই model এর F1 ছিল **0.992**। প্রায় perfect।

এখন, কেউ কি guess করতে পারবেন নতুন corpus এ এটা কত হলো?

> **[থামেন। সত্যিই অপেক্ষা করেন। এক দুইটা guess নেন।**
> **কেউ না বললে: "একটা number বলেন: 0.9 এর বেশি না কম?"]**

*(click)*

হয়েছে **zero point three zero four**।

0.99 থেকে 0.30।

আর যেই অংশটা আমাদের সবচেয়ে বেশি ভাবাচ্ছে সেটা হলো, model টা আসলে যা করে তা হলো, আগে দেখেনি এমন প্রায় প্রতিটা phishing email কে "legitimate" বলে দেয়। মানে বেশিরভাগ phishing miss করে, কিন্তু **accuracy** নামে মাত্র 0.69 এ, যেটা কাগজে কলমে এখনো গ্রহণযোগ্য দেখায়।

মানে কোনো paper যদি শুধু accuracy report করে, এই সমস্যাটা পুরোপুরি ঢাকা পড়ে যাবে। আর আমাদের review করা একটা paper ও এইভাবে evaluate করে না।

### Slide 6: Gap 2, the contamination (55 sec) ⚡ INTERACTIVE

ব্যাপারটা আরো খারাপ। আর এইটা আমাদের একদম নতুন result।

একটা transfer direction দেখতে কিন্তু **দারুণ** ছিল। Kaggle থেকে SpamAssassin, F1 0.97। প্রায় কোনো drop নেই।

এখন, এটাতে কি আমাদের খুশি হওয়া উচিত? না। আমাদের সন্দেহ হলো। কারণ Kaggle set কোনো original collection না। এটা একটা **aggregate**, পুরনো কয়েকটা corpus মিলিয়ে বানানো।

তাই আমরা প্রতিটা email body hash করে duplicate গুনলাম।

*(click)*

**SpamAssassin এর 74.4 percent Kaggle dataset এর ভিতরেই বসে আছে।** চার হাজার দুইশ বিরাশিটা email। একই message, দুই dataset এই।

*(click)*

আর অন্য দিকটা দেখেন। যেই এক জোড়ার মধ্যে **শূন্যটা** email common: ঠিক সেখানেই performance ভেঙে 0.35 এ নেমেছে।

মানে contamination দিয়েই result গুলো প্রায় পুরোপুরি ব্যাখ্যা হয়ে যায়। ওই "ভালো transfer" টা generalization ছিল না। ওটা ছিল **memorization**।

*(click)*

আর এখন যেই অংশটা নিয়ে আমরা সবচেয়ে গর্বিত। আমরা যখন সাধারণ **exact** duplicate check চালালাম (standard method, যেকোনো যত্নশীল researcher যেটা চালাবে) সেটা পেল মাত্র **48** টা duplicate। শুধু যখন **near**-duplicate matching ব্যবহার করলাম, তখন পেলাম 4,282 টা।

পার্থক্যটা কেন? কারণ এক dataset এ subject line রাখা ছিল, আর অন্যটায় ফেলে দেওয়া হয়েছে। একটা মাত্র line missing, আর 99 percent contamination অদৃশ্য হয়ে গেল।

*(click)*

তো ওই ভালো transfer টা ছিল memorization, generalization না। আর আমাদের review করা কোনো paper ই check করে না যে তারা যেই benchmark গুলো ব্যবহার করছে সেগুলো একে অপরের সাথে overlap করে কি না।

আমরা কীভাবে এসব ঠিক করতে চাই, ফারিয়া এখন সেটা দেখাবে।

---

## Delivery tips

- **Slide 5 is the moment of the whole presentation.** Do not rush past the question. Genuinely stop and wait, even four seconds of silence feels long to you but works on the audience. If nobody answers, force a quick binary: "higher or lower than 0.9?"
- Say "**zero point three zero four**" slowly, one word at a time. Do not say "point three oh four."
- On slide 6 you can add a show of hands before the reveal: raise your own hand while asking, people copy you.
- The **48 versus 4,282** point is the genuinely new contribution. Slow down there. That is the sentence the teacher will remember.
- Do not apologise for the small dataset sizes. State the numbers confidently.
- Hand over by name: "Faria will now show how we plan to fix all this."
