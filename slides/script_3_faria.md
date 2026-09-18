# Script for Nowshin, 3rd presenter (slides 7 to 9, about 1 min 45 sec)

Covers: objectives, proposed method, expected outcome and closing.

## English version

(Slide 7)
Thanks Saimon. So the gaps are clear, now our objectives, five of them, all very concrete. One, build a deduplicated cross corpus benchmark from these free public datasets, so the 66 percent leak Jahid showed can never inflate a result again. Two, evaluate everything with a leave one corpus out protocol, the model is always tested on a corpus it has never seen. Three, improve the small LLM using only cheap methods, better prompts, few shot examples, and a small DistilBERT trained locally, no expensive teacher model. Four, create a small test set of LLM written phishing, for evaluation only, because no benchmark has any. And five, put accuracy, robustness and cost per thousand emails into one single table.

(Slide 8)
Our method is one pipeline. First we collect and normalize the three corpora and deduplicate across them. Second, the leave one corpus out loop, train or prompt on two corpora, always test on the held out one. Third, four detectors go through the exact same protocol, TF-IDF Logistic Regression, DistilBERT on a normal laptop CPU, and llama-3.2-3b zero shot and few shot through OpenRouter. Fourth, every detector also faces our AI written phishing set, and we measure how much it degrades. Finally everything lands in that one honest table.

(Slide 9)
What you get at the end is a reproducible benchmark, code and scripts included, that runs fully on a laptop, and the total LLM budget stays under five dollars, till now we spent less than one cent. If you remember one line from us, remember this one, high accuracy on one dataset is easy, honest evaluation is the hard part. Thank you, we are happy to take questions.

## Bangla version

(Slide 7)
ধন্যবাদ সাইমন। Gap গুলো তো পরিষ্কার, এখন আমাদের objectives, পাঁচটা, সবগুলোই খুব concrete। এক, এই free public dataset গুলো থেকে একটা deduplicated cross corpus benchmark বানানো, যাতে জাহিদ যে 66 percent leak দেখালো, সেটা আর কখনো কোনো result কে ফুলিয়ে দেখাতে না পারে। দুই, সবকিছু leave one corpus out protocol দিয়ে evaluate করা, মানে model সবসময় এমন একটা corpus এ test হবে যেটা সে কখনো দেখেনি। তিন, small LLM কে improve করা শুধু সস্তা method দিয়ে, ভালো prompt, few shot example, আর একটা ছোট DistilBERT যেটা নিজেদের laptop এই train হবে, কোনো দামি teacher model না। চার, LLM দিয়ে লেখা phishing এর একটা ছোট test set বানানো, শুধু evaluation এর জন্য, কারণ কোনো benchmark এ এটা নেই। আর পাঁচ, accuracy, robustness আর প্রতি হাজার email এর cost, এই তিনটাকে একটা মাত্র table এ আনা।

(Slide 8)
আমাদের method টা একটা pipeline। প্রথমে তিনটা corpus collect আর normalize করে corpus গুলোর মধ্যে deduplicate করবো। দ্বিতীয়ত, leave one corpus out loop, দুইটা corpus এ train বা prompt করবো, test সবসময় বাদ রাখা corpus টায়। তৃতীয়ত, চারটা detector একদম একই protocol এর ভিতর দিয়ে যাবে, TF-IDF Logistic Regression, DistilBERT সাধারণ laptop এর CPU তে, আর llama-3.2-3b zero shot এবং few shot, OpenRouter দিয়ে। চতুর্থত, প্রতিটা detector কে আমাদের AI লেখা phishing set ও face করতে হবে, আর আমরা মাপবো performance কতটা নামে। শেষে সবকিছু গিয়ে জমা হবে ওই একটা honest table এ।

(Slide 9)
শেষে আপনারা যা পাবেন তা হলো একটা reproducible benchmark, code আর script সহ, যেটা পুরোটাই একটা laptop এ চলে, আর পুরো LLM budget পাঁচ dollar এর নিচে, এখন পর্যন্ত আমাদের খরচ এক cent এরও কম। আমাদের কাছ থেকে যদি একটা লাইন মনে রাখেন, তাহলে এটাই রাখবেন, এক dataset এ high accuracy পাওয়া সহজ, honest evaluation টাই আসল কঠিন কাজ। ধন্যবাদ, এখন প্রশ্ন নিতে পারি।

## Delivery tips
- Slide 7 has five objectives, use your fingers to count them off, it keeps the audience with you.
- Slide 8, walk along the pipeline on the slide with your hand, left to right.
- The closing line on slide 9 works best if you pause one second before it and say it slowly.
- Likely teacher questions to be ready for: why leave one corpus out (because it simulates unseen real world email), why small models (cost and hardware realism), is the AI phishing set safe (evaluation only, never sent to anyone, stays offline).
