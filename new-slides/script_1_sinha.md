# Script 1 — Jahid Ibna Sinha

**Slides 1, 2, 3 · about 2 minutes**

Your job in one line: **ask the question everybody is already thinking, then prove that the field has no answer for it.**

You do not present results. You build the trap. Saimon springs it.

---

## The three sentences you must not miss

1. *"LLM দিয়ে phishing detect করা তো পুরনো খবর — এতে আবার নতুন কী?"* → this is your hook, say it in the first 20 seconds.
2. *"Every number is between 97 and 99 percent."* → the boredom is the point.
3. *"Twenty-seven points gone."* → then stop talking.

---

# SLIDE 1 · Title (20 sec)

**On screen:** title, project name, three names, Group 18.

### English

> Good morning everyone. We are Group 18. I am Sinha, this is Saimon, and this is Faria.
>
> Our topic is **Phishing Email Detection Using Large Language Models**.
>
> *(small pause, half smile)*
>
> Now — before I start, let me say the question that is probably already in your head. *"LLMs detecting phishing? That is old news. The papers already report 99 percent. What is left to do?"*
>
> That was our question too. Our whole project is the answer to it.
>
> I will set up the problem. Saimon will show what happened when we tested it ourselves. Faria will show the plan.

### বাংলা

> সবাইকে শুভেচ্ছা। আমরা Group 18। আমি সিনহা, এ হলো সাইমন, আর ও ফারিয়া।
>
> আমাদের topic — **Phishing Email Detection Using Large Language Models**।
>
> *(ছোট pause, হালকা হাসি)*
>
> শুরু করার আগেই একটা কথা বলে নেই, যেটা এখনই আপনাদের মাথায় আসছে। *"LLM দিয়ে phishing detect করা — এটা তো পুরনো খবর। Paper গুলো তো already ৯৯ percent বলছে। এতে আবার নতুন কী?"*
>
> আমাদের প্রশ্নটাও ঠিক এইটাই ছিল। আর আমাদের পুরো project টাই এই প্রশ্নের উত্তর।
>
> আমি problem টা দাঁড় করাবো। তারপর সাইমন দেখাবে আমরা নিজেরা test করে কী পেলাম। শেষে ফারিয়া plan টা দেখাবে।

**Cue:** do NOT talk about how dangerous phishing is, or how many billions it costs. The teacher asked for technical content only. Skipping it also saves you 30 seconds.

---

# SLIDE 2 · The topic, technically (45 sec) ⚡ small interaction

**On screen:** Input → Model → Output diagram, then the three model families.

### English

> First, what is the problem technically?
>
> *(look at the audience)* Let me ask you — an email lands in your inbox. How do **you** decide it is phishing?
>
> *(1 second, take one answer or answer it yourself)*
>
> You read it. That is all. You do not open the attachment, you do not check the network traffic. You just read the words and something feels wrong.
>
> A machine does exactly the same thing. So technically this is **binary text classification**. Input: one raw email — subject line and body text. Output: one label — **phishing** or **legitimate**. No images, no attachments, no headers. Only text.
>
> Today three families of models do this job.
>
> **One — classical machine learning.** Turn the email into TF-IDF word counts, run Logistic Regression. This is older than deep learning. *Remember this one. It comes back in two minutes and it embarrasses everybody.*
>
> **Two — fine-tuned encoders.** BERT, RoBERTa, DistilBERT, trained on labelled emails.
>
> **Three — decoder LLMs.** The new direction. You prompt them zero-shot, or fine-tune cheaply with LoRA.
>
> And one practical point: every dataset in this field is **free and public**. That is the only reason a student group can do this project at all.

### বাংলা

> প্রথমে দেখি, technically problem টা আসলে কী।
>
> *(audience এর দিকে তাকান)* একটা প্রশ্ন করি — আপনার inbox এ একটা email আসলো। আপনি **কীভাবে** বুঝেন এটা phishing?
>
> *(এক সেকেন্ড থামেন, একটা উত্তর নিন বা নিজেই বলুন)*
>
> আপনি শুধু পড়েন। এটুকুই। Attachment খোলেন না, network traffic দেখেন না। শুধু লেখাটা পড়েন, আর মনে হয় কিছু একটা ঠিক নাই।
>
> মেশিনও ঠিক এই কাজটাই করে। তাই technically এটা একটা **binary text classification** problem। Input — একটা raw email, শুধু subject আর body text। Output — একটা label, **phishing** নাকি **legitimate**। কোনো image না, attachment না, header না। শুধু text।
>
> এখন এই কাজটা তিন ধরনের model করে।
>
> **এক — classical machine learning।** Email টাকে TF-IDF word count বানিয়ে Logistic Regression চালানো। Deep learning এরও আগের জিনিস। *এটা মনে রাখবেন। দুই মিনিট পর এটা আবার আসবে, আর সবাইকে লজ্জায় ফেলবে।*
>
> **দুই — fine-tuned encoder।** BERT, RoBERTa, DistilBERT — labelled email দিয়ে train করা।
>
> **তিন — decoder LLM।** এটাই নতুন direction। Zero-shot prompt করা যায়, অথবা LoRA দিয়ে সস্তায় fine-tune করা যায়।
>
> আর একটা practical কথা — এই field এর প্রতিটা dataset **free এবং public**। এই কারণেই একটা student group এর পক্ষে এই project টা করা সম্ভব।

**Cue:** the line *"remember this one, it comes back"* is a setup. Say it like you are hiding something. You are.

---

# SLIDE 3 · State of the art (50 sec) ⚡ your money slide

**On screen:** table of 6 works, then a red box appears on click.

### English

> So, 2022 to 2026. What did the researchers actually achieve?
>
> *(now read fast, flat, almost bored — this tone IS the argument)*
>
> Koide, GPT-4 with chain-of-thought — ninety-nine point seven.
> Uddin, fine-tuned RoBERTa — ninety-eight point four.
> Alhuzali, fourteen models across ten datasets — ninety-nine point zero.
> Lin, small three-billion models with LoRA — zero point nine six.
> MultiPhishGuard, five LLM agents cooperating — ninety-seven point nine.
>
> *(stop. change tone completely. slow.)*
>
> Now look at what just happened. Different models. Different years. Completely different techniques. **Every single number is between 97 and 99 percent.**
>
> When every method gives you the same score, that does not mean every method is perfect. It means **the test has stopped telling you anything.**
>
> *(one full second of silence — then CLICK)*
>
> And here is why. **Every one of those numbers is measured on one dataset at a time.**
>
> Now the last row. Phishsense-1B — an open model, built specifically for phishing. On its own dataset: 97.5 percent. Then someone tested it on a **different** real-world dataset.
>
> Seventy percent.
>
> **Twenty-seven points. Gone.**
>
> *(stop. do not explain it. hand over.)*
>
> That one row was our clue. Saimon will now show you what we found when we followed it.

### বাংলা

> তাহলে দেখি, ২০২২ থেকে ২০২৬ — researcher রা আসলে কী পেয়েছে?
>
> *(এখন দ্রুত, flat, প্রায় বিরক্তিকর ভঙ্গিতে পড়ুন — এই বিরক্তিটাই আসল যুক্তি)*
>
> Koide, GPT-4 আর chain-of-thought prompt — নিরানব্বই দশমিক সাত।
> Uddin, fine-tuned RoBERTa — আটানব্বই দশমিক চার।
> Alhuzali, দশটা dataset এ চৌদ্দটা model — নিরানব্বই দশমিক শূন্য।
> Lin, তিন বিলিয়ন parameter এর ছোট model with LoRA — শূন্য দশমিক ছিয়ানব্বই।
> MultiPhishGuard, পাঁচটা LLM agent একসাথে — সাতানব্বই দশমিক নয়।
>
> *(থামেন। গলার স্বর সম্পূর্ণ বদলান। ধীরে।)*
>
> এবার খেয়াল করেন কী হলো। আলাদা model। আলাদা বছর। সম্পূর্ণ আলাদা technique। কিন্তু **প্রতিটা number ৯৭ থেকে ৯৯ percent এর মধ্যে।**
>
> যখন সব method একই score দেয়, তখন এর মানে এই না যে সব method perfect। এর মানে হলো — **test টা আর আমাদের কিছুই বলছে না।**
>
> *(পুরো এক সেকেন্ড নীরবতা — তারপর CLICK)*
>
> আর কারণটা এই। **উপরের প্রতিটা number একবারে একটামাত্র dataset এ মাপা।**
>
> এবার শেষ row টা। Phishsense-1B — একটা open model, বিশেষভাবে phishing এর জন্যই বানানো। নিজের dataset এ ৯৭.৫ percent। তারপর কেউ একজন এটাকে **অন্য** একটা real-world dataset এ test করলো।
>
> সত্তর percent।
>
> **সাতাশ point। উধাও।**
>
> *(থামেন। ব্যাখ্যা করবেন না। hand over করেন।)*
>
> ওই একটা row-ই ছিল আমাদের clue। সাইমন এখন দেখাবে, এই clue follow করে আমরা কী পেলাম।

---

## Delivery notes for you specifically

- **Tone map:** Slide 1 friendly → Slide 2 explaining → Slide 3 fast and bored → then suddenly slow and serious. That change of speed is what makes people look up.
- **Do not read the table row by row like a list.** Say the numbers almost carelessly. If the audience gets slightly bored for five seconds, you have won.
- **Pause before the click.** One full second feels like ten to you and like nothing to them. Count it in your head.
- Say *"twenty-seven points gone"* and then **close your mouth.** Do not add "so as you can see". That kills it.
- Hand over by name, every time: *"Saimon will now show you…"*

## If you are running out of time (30-second emergency version of slide 3)

> "Every paper from 2022 to 2026 reports 97 to 99 percent. Different models, same score — that means the test is broken, not that the models are perfect. And the reason is on this slide: every number is measured on one dataset at a time. The one model that was tested on a second dataset dropped 27 points. Saimon, take it."

## Questions likely to come to YOU

- *"Why is binary classification enough? Real email has links and headers."* → Correct, and that is a limitation we state. We use text only because every public corpus is text only, and because it makes all models comparable under one protocol.
- *"Aren't these papers using different datasets already?"* → They use different datasets, but each one **trains and tests inside the same dataset**. Nobody trains on one and tests on another. That is the difference.
- *"Is 97-99% not just because the task is easy?"* → That is exactly our hypothesis, and slides 4 to 6 test it.
