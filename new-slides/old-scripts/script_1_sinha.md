# Script 1: Jahid Ibna Sinha

**Slides 1, 2, 3 · about 1 minute 55 seconds**
Your job: open the talk, explain the problem technically, and set the trap that Saimon springs on slide 5.

---

## English version

### Slide 1: Title (20 sec)

Good morning everyone. We are Group 18. I am Sinha, and with me are Saimon and Faria.

Our topic is **Phishing Email Detection Using Large Language Models**. The full title of our project is *Cost-Aware Benchmarking of Small Open LLMs for Cross-Corpus Phishing Email Detection*.

I will explain the technical problem and what other researchers have done. Then Saimon will show what we found when we tested it ourselves. Then Faria will show our plan.

### Slide 2: The topic, technically (45 sec)

Let me start with the technical picture.

At its core this is a **binary text classification** problem. The input is one raw email, just the subject line and the body text. The output is one label: **phishing**, or **legitimate**. That is all. No images, no attachments, no network traffic. Only text.

Today, three families of models do this job.

The **first** is classical machine learning. You turn the email into TF-IDF word features and run Logistic Regression or Naive Bayes. This is old technology, but remember it. It comes back later.

The **second** is fine-tuned encoders. Models like BERT, RoBERTa and DistilBERT, trained on labelled email data.

The **third** is decoder LLMs. This is the new direction. You can prompt them zero-shot or few-shot, or fine-tune them cheaply with LoRA.

And one practical point. All the datasets used in this field (SpamAssassin, CEAS, Nazario, Enron, Nigerian Fraud, Ling, TREC) are **free and public**. That is why this project fits our student budget.

### Slide 3: State of the art (50 sec)

Now, what have researchers achieved from 2022 to 2026?

Koide and his team prompted GPT-4 with a chain-of-thought prompt. **99.7 percent** accuracy.

Uddin and his team fine-tuned RoBERTa and added explainability. **98.45 percent**.

Alhuzali's team tested fourteen models across ten datasets. **99.08 percent**.

Lin's team took small three-billion parameter models and fine-tuned them, going from 0.59 up to 0.96.

MultiPhishGuard used five cooperating LLM agents. **97.89 percent**.

Now look carefully. Every single number is between 97 and 99 percent. Different models, different years, different techniques, same answer. When every method gives the same score, the test has stopped telling us anything useful.

*(click)*

And here is the reason. **Every one of those numbers is measured on one dataset at a time.**

Look at the last row. Phishsense-1B is an open model built specially for phishing. On its own dataset: 97.5 percent. The moment someone tested it on a *different* real-world dataset, it fell to **70 percent**. Twenty-seven points gone.

That one row is the clue. Saimon will now show you what happened when we followed it.

---

## বাংলা version

### Slide 1: Title (20 sec)

সবাইকে শুভেচ্ছা। আমরা Group 18. আমি সিনহা, আর আমার সাথে আছে জাকারিয়া এবং ফারিয়া।

আমাদের topic হলো **Phishing Email Detection Using Large Language Models**। আমাদের project এর পুরো নাম *Cost-Aware Benchmarking of Small Open LLMs for Cross-Corpus Phishing Email Detection*।

আমি technical problem টা আর অন্য researcher রা কী করেছে সেটা বলব। তারপর জাকারিয়া দেখাবে আমরা নিজেরা test করে কী পেয়েছি। শেষে ফারিয়া আমাদের plan দেখাবে।

### Slide 2: The topic, technically (45 sec)

প্রথমে technical ছবিটা বলি।

মূলত এটা একটা **binary text classification** problem। Input হলো একটা raw email, শুধু subject line আর body text। Output হলো একটা label: **phishing**, নাকি **legitimate**। এটুকুই। কোনো image না, attachment না, network traffic না। শুধু text।

এখন তিন ধরনের model এই কাজটা করে।

**প্রথম** হলো classical machine learning। Email কে TF-IDF word feature বানিয়ে Logistic Regression বা Naive Bayes চালানো হয়। পুরনো technology, কিন্তু এটা মনে রাখবেন, পরে আবার আসবে।

**দ্বিতীয়** হলো fine-tuned encoder। BERT, RoBERTa, DistilBERT, labelled email data দিয়ে train করা।

**তৃতীয়** হলো decoder LLM। এটাই নতুন direction। Zero-shot বা few-shot prompt করা যায়, অথবা LoRA দিয়ে সস্তায় fine-tune করা যায়।

আর একটা practical কথা। এই field এ যত dataset ব্যবহার হয় (SpamAssassin, CEAS, Nazario, Enron, Nigerian Fraud, Ling, TREC) সবগুলোই **free এবং public**। এই কারণেই আমাদের student budget এ project টা সম্ভব।

### Slide 3: State of the art (50 sec)

এখন দেখি, 2022 থেকে 2026 পর্যন্ত researcher রা কী পেয়েছে।

Koide আর তার team GPT-4 কে chain-of-thought prompt দিয়েছে। **99.7 percent** accuracy।

Uddin আর তার team RoBERTa fine-tune করেছে, সাথে explainability যোগ করেছে। **98.45 percent**।

Alhuzali এর team দশটা dataset এ চৌদ্দটা model test করেছে। **99.08 percent**।

Lin এর team ছোট তিন বিলিয়ন parameter এর model fine-tune করে 0.59 থেকে 0.96 এ নিয়ে গেছে।

MultiPhishGuard পাঁচটা LLM agent একসাথে ব্যবহার করেছে। **97.89 percent**।

এবার ভালো করে খেয়াল করেন। প্রতিটা number 97 থেকে 99 percent এর মধ্যে। আলাদা model, আলাদা বছর, আলাদা technique, কিন্তু answer একই। যখন সব method একই score দেয়, তখন বুঝতে হবে test টা আর কিছু বলছে না।

*(click)*

আর কারণটা এই। **উপরের প্রতিটা number একবারে একটা dataset এ measure করা।**

শেষ row টা দেখেন। Phishsense-1B একটা open model, বিশেষভাবে phishing এর জন্য বানানো। নিজের dataset এ 97.5 percent। যেই মুহূর্তে কেউ অন্য একটা real-world dataset এ test করলো, নেমে গেল **70 percent** এ। সাতাশ point উধাও।

ওই একটা row ই clue। জাকারিয়া এখন দেখাবে আমরা এই clue follow করে কী পেলাম।

---

## Delivery tips

- **Slide 3 is your slide.** Do not read the table row by row like a list. Say the numbers fast, almost boringly. The boredom is the point. Then slow right down for "every number is between 97 and 99."
- Pause for one full second before you click to reveal the red box.
- Say "**twenty-seven points gone**" and stop. Let it sit before you hand over.
- Do not talk about motivation, why phishing is dangerous, or statistics about attacks. The teacher asked for technical content only. Skipping it also saves you 30 seconds.
- Hand over by name: "Saimon will now show you what happened when we followed it."
