# Research Gaps Identified from Preliminary Experiments

Topic: Phishing Email Detection Using Large Language Models

Team: Md. Jakaria Alam Saimon (011221002), Jahid Ibna Sinha (011221376), Nowshin Anjum Faria (011221372)

United International University, Course: Computer Security

Following the direction from our literature review, we ran preliminary experiments on three public corpora: the Kaggle Phishing Email dataset (17,505 emails), SpamAssassin (5,809), and Nazario phishing paired with Enron ham (3,128). We trained TF-IDF with Logistic Regression and Naive Bayes on each corpus, tested every model on the other two corpora, and also ran two small open LLMs (llama-3.2-3b and gemma-3-12b through OpenRouter) zero-shot on 100 sampled emails per corpus. The code and result files are submitted along with this document. From the results we identify the following gaps.

Gap 1. Single dataset evaluation hides a large generalization gap. Inside their own corpus our simple baselines reach 97 to 99 percent accuracy, the same range the reviewed papers report with much heavier models. But the model trained on Nazario plus Enron drops from F1 0.992 to 0.304 on the Kaggle corpus and 0.354 on SpamAssassin. It keeps predicting legitimate for unseen phishing, so accuracy looks fine while the phishing class is missed. The reviewed papers evaluate on a single corpus, so their numbers likely overstate real world performance. A standard cross-corpus benchmark for phishing email detection does not exist yet.

Gap 2. Aggregated datasets leak between benchmarks. The direction from Kaggle to SpamAssassin barely dropped (F1 0.972), which is suspicious rather than impressive. The Kaggle set aggregates several older collections, so it very likely shares emails with SpamAssassin. None of the reviewed papers check for such overlap, which makes cross-dataset claims unreliable and calls for a deduplicated benchmark.

Gap 3. The public corpora are old and contain no AI-generated phishing. Enron and SpamAssassin are from the early 2000s and the Nazario feed is mostly 2015 to 2024. Heiding et al. showed that GPT-4 written phishing works well on humans, yet no public benchmark contains LLM-generated phishing emails, so we cannot measure how detectors handle the attacks that are actually growing.

Gap 4. Spam and phishing labels are conflated. SpamAssassin labels ordinary junk mail as positive while the Nazario set contains only credential phishing. Uddin et al. deliberately excluded spam for this reason. Since every paper defines the positive class differently, results across papers are not comparable.

Gap 5. The accuracy, robustness and cost trade-off is never quantified. Our zero-shot llama-3.2-3b stayed stable at 0.80 to 0.84 accuracy on all three corpora with no training data, while the classical models collapsed outside their own corpus. So the LLM is 15 points worse in-domain but far more robust, at about half a cent per thousand emails. The bigger gemma-3-12b was worse (precision 0.58 on two corpora, it flags almost everything as phishing), so scale does not fix calibration. Koide et al. report 99.7 percent with GPT-4 but no cost, and Kuikel et al. show accuracy and explanation faithfulness do not move together. No paper puts these three axes in one table, which is what a deployment decision needs and what we plan to study next, together with cheap fine-tuning of the small LLM.
