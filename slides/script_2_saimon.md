# Script for Saimon (slides 4 to 6, about 2 min)

Covers: our preliminary experiments and the identified gaps. This is the interactive part.

## English version

(Slide 4)
Thank you Jahid. So we did not just trust these papers, we tested the story ourselves on three corpora, the Kaggle set with about seventeen and a half thousand emails, SpamAssassin with about six thousand, and Nazario phishing paired with Enron ham, about three thousand. A very simple model, TF-IDF with Logistic Regression, and look, 97.9, 97.3 and 99.2 percent accuracy. Same range as the papers. So phishing detection is solved, right?

(Slide 5)
Well, let's check. We trained on one corpus and tested on a different one. On its own corpus the model had F1 0.992. Anyone want to guess what it became on the other corpus? (pause, take one or two guesses from the audience) ... It became 0.304. From 0.99 to 0.30. The model basically says legitimate to every phishing email it has not seen before, so accuracy still looks okay while it misses most of the phishing. And no paper in our review evaluates this way.

(Slide 6)
It gets worse, and here is our newest result. One transfer direction looked great, Kaggle to SpamAssassin, F1 0.97. Suspicious. So we hashed every email body and counted duplicates. 3,838 emails, that is 66 percent of SpamAssassin, sit inside the Kaggle dataset. That great transfer was memorization, not generalization. Also, the corpora are old, there is zero AI generated phishing in any benchmark, and labels are inconsistent, spam and phishing get mixed. Last one, quick show of hands, who thinks a 12B model beats a 3B model at this? (pause) Actually the small llama held a stable 0.80 to 0.84 on every corpus, for half a cent per thousand emails, while the bigger gemma flagged almost everything as phishing, precision 0.58. Nobody reports these three things together, accuracy, robustness and cost. Nowshin will show how we plan to fix that.

## Bangla version

(Slide 4)
ধন্যবাদ জাহিদ। আমরা শুধু paper গুলোকে বিশ্বাস করে বসে থাকিনি, নিজেরাই গল্পটা test করেছি তিনটা corpus এর উপর। Kaggle set, প্রায় সাড়ে সতেরো হাজার email, SpamAssassin প্রায় ছয় হাজার, আর Nazario phishing এর সাথে Enron ham, প্রায় তিন হাজার। খুবই simple একটা model, TF-IDF আর Logistic Regression, আর দেখেন, 97.9, 97.3 আর 99.2 percent accuracy। Paper গুলোর মতোই। তাহলে তো phishing detection solved, তাই না?

(Slide 5)
আচ্ছা, check করে দেখি। আমরা এক corpus এ train করে অন্য corpus এ test করলাম। নিজের corpus এ model এর F1 ছিল 0.992। কেউ কি guess করবেন অন্য corpus এ এটা কত হলো? (একটু থামেন, audience থেকে এক দুইটা guess নেন) ... হয়েছে 0.304। 0.99 থেকে 0.30। Model টা আসলে নতুন phishing দেখলেই বলে দেয় legitimate, তাই accuracy দেখতে ঠিকঠাক লাগে কিন্তু বেশিরভাগ phishing miss হয়ে যায়। আর আমাদের review করা কোনো paper এইভাবে evaluate করে না।

(Slide 6)
ব্যাপারটা আরো খারাপ, আর এইটা আমাদের একদম নতুন result। একটা transfer direction দেখতে দারুণ ছিল, Kaggle থেকে SpamAssassin, F1 0.97। সন্দেহজনক। তাই আমরা প্রতিটা email এর body hash করে duplicate গুনলাম। 3,838 টা email, মানে SpamAssassin এর 66 percent, Kaggle dataset এর ভিতরেই বসে আছে। ওই ভালো transfer টা আসলে generalization ছিল না, ছিল memorization। এছাড়া corpus গুলো পুরনো, কোনো benchmark এ AI generated phishing নেই, আর label ও inconsistent, spam আর phishing মিশে গেছে। শেষেরটা, হাত তুলে বলেন তো, কে কে মনে করেন 12B model এই কাজে 3B model কে হারাবে? (থামেন) আসলে ছোট llama প্রতিটা corpus এ stable 0.80 থেকে 0.84 ধরে রেখেছে, হাজার email এ খরচ মাত্র আধা cent, আর বড় gemma প্রায় সব email কেই phishing বলে দিয়েছে, precision 0.58। এই তিনটা জিনিস, accuracy, robustness আর cost, কেউ একসাথে report করে না। আমরা কীভাবে এটা fix করতে চাই, সেটা নওশিন দেখাবে।

## Delivery tips
- Slide 5 is your moment. Actually pause and let one or two people guess before revealing 0.304. If nobody speaks, say "lower or higher than 0.9?" to force a quick answer.
- Say "zero point three zero four" slowly.
- On slide 6, raise your own hand when asking the show of hands question, people follow.
