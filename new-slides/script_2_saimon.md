# Script 2 — Md. Jakaria Alam Saimon

**Slides 4, 5, 6 · about 2 minutes 20 seconds**

Your job in one line: **you are the twist.** Sinha said "the papers all say 99 percent." You show it falls apart. These three slides carry our only original results, and both audience moments are yours.

---

## ⚠️ NUMBERS NOTE — read this before the talk

The slide shows **74.4% / 4,282 near-duplicates / 48 exact duplicates**.
The submitted results file (`results/dataset_overlap.csv`) says **66.4% / 3,838 shared**.

Say whichever number is actually backed by code we can show. **The team must say one number, not two.** If the MinHash run is not saved and reproducible before the talk, use the safe line below:

> Safe version: *"Two thirds of SpamAssassin — 3,838 emails — sit inside the Kaggle set."*

Everything else in this script stays the same.

---

## The three sentences you must not miss

1. *"So phishing detection is solved… right?"* → then pause.
2. *"Zero. Point. Three. Zero. Four."* → said slowly, one word at a time.
3. *"Forty-eight versus four thousand."* → this is our best original finding.

---

# SLIDE 4 · We tested it ourselves (35 sec)

**On screen:** three corpora, three accuracy numbers, then a question appears on click.

### English

> Thank you Sinha.
>
> Now, we did not just believe those papers. We tested the story ourselves, on three public corpora. Kaggle — about seventeen and a half thousand emails. SpamAssassin — about six thousand. And Nazario phishing paired with Enron legitimate mail — about three thousand.
>
> And which model did we use? *(pause)* Not GPT-4. Not RoBERTa. We used **TF-IDF with Logistic Regression** — the old classical method Sinha told you to remember.
>
> Look at the result. **97.9. 97.3. 99.2 percent.**
>
> No LLM. No GPU. No training budget. A technique older than deep learning — and it lands in exactly the same 97 to 99 band as GPT-4.
>
> *(CLICK)*
>
> So phishing detection is solved… right?
>
> *(let the question sit. do NOT answer it. move to next slide.)*

### বাংলা

> ধন্যবাদ সিনহা।
>
> আমরা কিন্তু ওই paper গুলো শুধু বিশ্বাস করে বসে থাকিনি। গল্পটা নিজেরাই test করেছি, তিনটা public corpus এর উপর। Kaggle — প্রায় সাড়ে সতেরো হাজার email। SpamAssassin — প্রায় ছয় হাজার। আর Nazario phishing এর সাথে Enron এর legitimate mail — প্রায় তিন হাজার।
>
> আর আমরা কোন model ব্যবহার করলাম? *(pause)* GPT-4 না। RoBERTa ও না। আমরা ব্যবহার করলাম **TF-IDF আর Logistic Regression** — সিনহা যেই পুরনো classical method টা মনে রাখতে বলেছিল।
>
> Result টা দেখেন। **৯৭.৯। ৯৭.৩। ৯৯.২ percent।**
>
> কোনো LLM নাই। GPU নাই। Training budget নাই। Deep learning এরও আগের একটা technique — আর সেটা ঠিক GPT-4 এর মতোই ৯৭ থেকে ৯৯ এর ঘরে পড়লো।
>
> *(CLICK)*
>
> তাহলে তো phishing detection solved… তাই না?
>
> *(প্রশ্নটা ঝুলিয়ে রাখেন। উত্তর দিবেন না। পরের slide এ যান।)*

**Cue:** say *"no LLM, no GPU"* with a little pride. This slide is quietly funny — a 20-year-old method tying GPT-4. Let people enjoy it, because you are about to take it away.

---

# SLIDE 5 · Gap 1 · The collapse (50 sec) ⚡⚡ THE MOMENT OF THE TALK

**On screen:** 0.992 on the left. Right side is blank until you click.

### English

> Let's actually check.
>
> We did something very simple. We trained the model on **one** corpus — and tested it on a **completely different** corpus. Because that is what real life is. Real phishing emails do not come from your training set.
>
> On its own corpus this model scored F1 **zero point nine nine two**. Almost perfect.
>
> *(step forward, look at them)*
>
> Now — can anyone guess what it became on the new corpus?
>
> > **[STOP. Actually wait. Take one or two guesses.**
> > **If nobody speaks, force a binary: "Just shout — higher or lower than 0.9?"]**
>
> *(CLICK)*
>
> **Zero. Point. Three. Zero. Four.**
>
> From 0.99 to 0.30. Same model. Same code. Different emails.
>
> And here is the part that worries us most. What the model actually does is answer **"legitimate"** to almost every phishing email it has never seen. So it misses most of the phishing — but the **accuracy** only falls to 0.69, which still looks perfectly acceptable in a table.
>
> So a paper that reports accuracy only would hide this completely. And not one paper in our review evaluates this way.

### বাংলা

> চলেন সত্যিই check করে দেখি।
>
> আমরা খুব simple একটা কাজ করলাম। **একটা** corpus এ model train করলাম — আর test করলাম **সম্পূর্ণ আলাদা** একটা corpus এ। কারণ বাস্তবে তো এটাই হয়। আসল phishing email আপনার training set থেকে আসে না।
>
> নিজের corpus এ এই model এর F1 ছিল **শূন্য দশমিক নয় নয় দুই**। প্রায় perfect।
>
> *(এক পা সামনে আসেন, তাকান)*
>
> এখন — কেউ কি guess করতে পারবেন, নতুন corpus এ এটা কত হলো?
>
> > **[থামেন। সত্যি সত্যি অপেক্ষা করেন। এক-দুইটা guess নেন।**
> > **কেউ না বললে জোর করে binary করেন: "একটা কথা বলেন — ০.৯ এর বেশি না কম?"]**
>
> *(CLICK)*
>
> **শূন্য দশমিক তিন শূন্য চার।**
>
> ০.৯৯ থেকে ০.৩০। একই model। একই code। শুধু email গুলো আলাদা।
>
> আর যেই অংশটা আমাদের সবচেয়ে বেশি ভাবায় — model টা আসলে যা করে তা হলো, আগে দেখেনি এমন প্রায় প্রতিটা phishing email কে **"legitimate"** বলে দেয়। মানে বেশিরভাগ phishing miss করে — কিন্তু **accuracy** নামে মাত্র ০.৬৯ এ, যেটা table এ দেখতে এখনো একদম গ্রহণযোগ্য।
>
> মানে কোনো paper যদি শুধু accuracy report করে, এই পুরো সমস্যাটা ঢাকা পড়ে যাবে। আর আমাদের review করা একটা paper ও এইভাবে evaluate করে না।

**Cue:** four seconds of silence feels endless to you and normal to them. Do not rescue the silence. If you rush this slide, the presentation loses its best moment.

---

# SLIDE 6 · Gap 2 · The contamination (55 sec) ⚡ our strongest result

**On screen:** four things reveal one at a time. Click deliberately.

### English

> It gets worse. And this is our newest result.
>
> One transfer direction actually looked **great**. Kaggle to SpamAssassin — F1 0.97. Almost no drop at all.
>
> Now, should we be happy about that? *(shake your head)* We were suspicious. Because the Kaggle set is not an original collection — it is an **aggregate**, built by merging older corpora together.
>
> So we hashed every single email body and counted the duplicates.
>
> *(CLICK)*
>
> **Seventy-four percent of SpamAssassin is sitting inside the Kaggle dataset.** Four thousand two hundred and eighty-two emails. The same messages, in both datasets. The model was not generalising — it was recognising emails it had already been trained on.
>
> *(CLICK)*
>
> And now look at the other side. The one pair of corpora that shares **zero** emails? That is exactly the pair where performance collapsed to 0.35.
>
> So the contamination explains our results almost perfectly. That "good transfer" was not generalisation. It was **memorisation.**
>
> *(CLICK)*
>
> And here is the part we are most proud of. When we ran a normal **exact**-duplicate check — the standard method, what any careful researcher would run — it found **forty-eight** duplicates. Only when we used **near**-duplicate matching did we find four thousand two hundred and eighty-two.
>
> Forty-eight versus four thousand.
>
> Why? Because in one dataset the subject line was kept, and in the other it was stripped. **One missing line, and 99 percent of the contamination becomes invisible.**
>
> So anyone deduplicating the normal way would look at these corpora and call them clean. And no paper in our review even checks whether the benchmarks they use overlap each other.
>
> Faria will now show how we plan to fix all of this.

### বাংলা

> ব্যাপারটা আরো খারাপ। আর এইটা আমাদের একদম নতুন result।
>
> একটা transfer direction কিন্তু দেখতে **দারুণ** ছিল। Kaggle থেকে SpamAssassin — F1 ০.৯৭। প্রায় কোনো drop নাই।
>
> এখন, এতে কি আমাদের খুশি হওয়া উচিত? *(মাথা নাড়েন)* আমাদের সন্দেহ হলো। কারণ Kaggle set কোনো original collection না — এটা একটা **aggregate**, পুরনো কয়েকটা corpus মিলিয়ে বানানো।
>
> তাই আমরা প্রতিটা email body hash করে duplicate গুনলাম।
>
> *(CLICK)*
>
> **SpamAssassin এর চুয়াত্তর percent Kaggle dataset এর ভিতরেই বসে আছে।** চার হাজার দুইশ বিরাশিটা email। একই message, দুই dataset এই। Model টা generalise করছিল না — সে আসলে আগে train এ দেখা email গুলোই চিনে ফেলছিল।
>
> *(CLICK)*
>
> এবার অন্য দিকটা দেখেন। যেই এক জোড়া corpus এর মধ্যে **শূন্যটা** email common — ঠিক সেখানেই performance ভেঙে ০.৩৫ এ নেমেছে।
>
> মানে contamination দিয়েই আমাদের result গুলো প্রায় পুরোপুরি ব্যাখ্যা হয়ে যায়। ওই "ভালো transfer" টা generalization ছিল না। ওটা ছিল **memorization।**
>
> *(CLICK)*
>
> আর এখন যেই অংশটা নিয়ে আমরা সবচেয়ে গর্বিত। আমরা যখন সাধারণ **exact** duplicate check চালালাম — standard method, যেকোনো যত্নশীল researcher যেটা চালাবে — সেটা পেল মাত্র **আটচল্লিশটা** duplicate। শুধু যখন **near**-duplicate matching ব্যবহার করলাম, তখন পেলাম চার হাজার দুইশ বিরাশি।
>
> আটচল্লিশ বনাম চার হাজার।
>
> কেন? কারণ এক dataset এ subject line রাখা ছিল, আর অন্যটায় ফেলে দেওয়া হয়েছে। **একটা মাত্র line missing, আর ৯৯ percent contamination অদৃশ্য।**
>
> মানে কেউ যদি স্বাভাবিক নিয়মে deduplicate করে, সে এই corpus গুলোকে পরিষ্কার বলেই ধরে নিবে। আর আমাদের review করা কোনো paper ই check করে না, তারা যেই benchmark গুলো ব্যবহার করছে সেগুলো একে অপরের সাথে overlap করে কি না।
>
> আমরা এসব কীভাবে ঠিক করতে চাই, ফারিয়া এখন সেটা দেখাবে।

---

## Delivery notes for you specifically

- **Slide 5 is the peak of the whole presentation.** Everything before it is setup, everything after it is response. Give it room.
- Say the numbers like words, not like decimals: *"zero point three zero four"*, never *"point three oh four."*
- On slide 6, **raise your own hand while asking** for a show of hands — people copy the speaker automatically.
- The **48 versus 4,282** line is the single sentence the teacher will remember. Slow down, and say the two numbers next to each other.
- Do not apologise for small dataset sizes or "it's only preliminary." State the numbers confidently. They are real.
- Hand over by name: *"Faria will now show how we plan to fix all of this."*

## Questions likely to come to YOU

- *"Maybe the drop is just because the two corpora have different definitions of phishing?"* → Partly yes, and that is our Gap 4 — spam versus phishing labels are conflated across corpora. It is a second reason the current benchmarks are not comparable, not a reason the collapse is fine.
- *"Is 0.30 F1 not just a bad model?"* → Same model, same code, 0.99 on its own corpus. The only thing that changed is the emails. That is the definition of a generalisation failure.
- *"How exactly did you detect near-duplicates?"* → Normalised the body text (lowercase, whitespace removed), hashed it, and matched. The full project moves to MinHash + LSH so it scales to six corpora.
