# Script for Jahid (slides 1 to 3, about 2 min)

Covers: title, topic introduction in plain words, state of the art with the catch of each paper.

## English version

(Slide 1)
Assalamu alaikum everyone. I am Jahid, and this is our team, Saimon and Nowshin. Our term paper topic is Phishing Email Detection Using Large Language Models. I will introduce the topic and what researchers have done so far, Saimon will show our own experiments, and Nowshin will present our objectives and method.

(Slide 2)
So, we all have heard about phishing emails, right? Quick show of hands, who has ever received an email saying you won a lottery, or your bank account will be closed today? (pause, look around) Almost everyone. So phishing is nothing new. But have you ever wondered how a computer decides which email is phishing and which one is safe? For the machine it is a simple question with two answers. An email goes in, and one label comes out, phishing or legitimate. What changed over time is who answers that question. First generation, the old way, rules and blocklists. Block the known bad senders and bad links. It fails the moment the attacker changes the words. Second generation, classical machine learning. It learns spammy word patterns from data. Third generation, deep models like BERT, they actually read every word in its context. And today, the fourth generation, large language models. You just prompt them, they read the email like a human and even explain why it is suspicious. But here is the twist. The same LLMs can also write phishing emails now. So attacking became cheap, and defending got a new tool, both at the same time. That is exactly why we chose this topic.

(Slide 3)
Now, what did researchers already do with this idea? These five papers, 2023 to 2026, are the state of the art. GPT-4 with a good prompt reached 99.7 percent accuracy. Fine tuned RoBERTa reached 98.45. Small 3B models got close to the big ones. Very impressive numbers, right? But look at the last column, every paper has a catch. Closed paid models, no cost reported, tiny test sets, English only, paid teacher models. And one problem is common in all of them, every single paper tests on one dataset at a time. Our plan is different, we combine multiple datasets and test across them. And when we actually tried that, something interesting happened. Saimon will show you.

## Bangla version

(Slide 1)
আসসালামু আলাইকুম সবাইকে। আমি জাহিদ, আর এই আমাদের team, সাইমন আর নওশিন। আমাদের term paper এর টপিক হলো Phishing Email Detection Using Large Language Models। আমি টপিকটা introduce করবো আর এখন পর্যন্ত researcher রা কী করেছে সেটা বলবো, সাইমন আমাদের নিজেদের experiment দেখাবে, আর নওশিন আমাদের objectives আর method present করবে।

(Slide 2)
আচ্ছা, phishing email এর কথা তো আমরা সবাই শুনেছি, তাই না? একটু হাত তুলে বলেন তো, কে কে কখনো এমন email পেয়েছেন যে আপনি lottery জিতেছেন, বা আজকেই আপনার bank account বন্ধ হয়ে যাবে? (একটু থামেন, চারপাশে তাকান) প্রায় সবাই। তো phishing নতুন কিছু না। কিন্তু কখনো ভেবে দেখেছেন, একটা computer কীভাবে ঠিক করে কোন email টা phishing আর কোনটা safe? Machine এর জন্য এটা দুইটা উত্তরের একটা প্রশ্ন। একটা email ঢুকবে, একটা label বের হবে, phishing অথবা legitimate। সময়ের সাথে যেটা বদলেছে সেটা হলো এই প্রশ্নের উত্তরটা কে দেয়। প্রথম generation, পুরনো পদ্ধতি, rules আর blocklist। চেনা খারাপ sender আর link গুলো block করে দাও। Attacker শব্দগুলো একটু বদলালেই এটা fail করে। দ্বিতীয় generation, classical machine learning, data থেকে spammy শব্দের pattern শেখে। তৃতীয় generation, deep model যেমন BERT, এরা আসলে প্রতিটা শব্দ তার context এ পড়ে। আর আজকে, চতুর্থ generation, large language model। শুধু prompt করলেই হয়, ওরা মানুষের মতো email টা পড়ে, এমনকি explain ও করে কেন এটা suspicious। কিন্তু এখানে একটা twist আছে। এই একই LLM এখন phishing email লিখতেও পারে। মানে attack করা হয়ে গেছে সস্তা, আবার defense ও পেয়ে গেছে নতুন একটা অস্ত্র, দুটো একসাথে। ঠিক এই কারণেই আমরা এই টপিকটা বেছে নিয়েছি।

(Slide 3)
এখন, এই idea নিয়ে researcher রা কী কী করেছে? এই পাঁচটা paper, 2023 থেকে 2026, এটাই state of the art। GPT-4 ভালো prompt দিয়ে 99.7 percent accuracy পেয়েছে। Fine tuned RoBERTa পেয়েছে 98.45। ছোট 3B model গুলোও বড়দের কাছাকাছি চলে গেছে। Number গুলো impressive, তাই না? কিন্তু শেষ column টা দেখেন, প্রতিটা paper এর একটা করে catch আছে। Closed paid model, cost report করা হয়নি, ছোট্ট test set, শুধু English, paid teacher model। আর একটা সমস্যা সবগুলোতেই common, প্রত্যেকটা paper test করে একটা মাত্র dataset এর উপর। আমাদের plan টা আলাদা, আমরা একাধিক dataset combine করবো আর এক dataset এ train করে অন্যটায় test করবো। আর যখন আমরা আসলেই সেটা করে দেখলাম, interesting একটা জিনিস ঘটলো। সেটা সাইমন আপনাদের দেখাবে।

## Delivery tips
- The show of hands on slide 2 is your icebreaker, actually wait 2 or 3 seconds and raise your own hand first.
- On slide 2 walk through the four cards left to right with your hand, one line each, do not read the card text word by word.
- On slide 3, do not read all five rows. Say the two or three big numbers, then jump to the catch column, that is the point of the slide.
- End with a cliffhanger tone: "something interesting happened, Saimon will show you."
