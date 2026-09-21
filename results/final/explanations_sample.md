# Explanations to read by hand

Twelve cases, half of them wrong verdicts.

## enron · qwen-2.5-7b-instruct · true label phishing · said legitimate (wrong)

reason: it appears to be a standard email delivery failure notification.

judge: grounded=1.0, supports=1.0

email: delivery failure : ? ? ? ? t 620 ao 24679 coa 81 e 6517 c 4 ( t 620 ao 24679 coa 81 e 6517 c 4 @ marinfonet . com ) ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ?
your message
subject : re : your text
was not delivered to :
t 620 ao 24679 coa 81 e 6517 c 4 @ marinfonet . com
because :
 $ b % f !

---

## ephishllm · qwen-2.5-7b-instruct · true label phishing · said legitimate (wrong)

reason: the email appears to be from a ceo requesting assistance with a financial matter, which is a common and legitimate request.

judge: grounded=0.0, supports=0.0

email: Immediate Assistance Required with Financial Matters
Jessica,

I need your immediate assistance in processing a financial matter crucial to our operations. Kindly prioritize this and let me know the relevant details at your earliest convenience.

The funds need to be transferred under strict confidentiality, and your prompt action will ensure the success of this operation.

Thank you for your atte

---

## ephishllm · qwen-2.5-7b-instruct · true label phishing · said legitimate (wrong)

reason: the email requests a legitimate work-related action and uses a professional tone.

judge: grounded=0.0, supports=0.0

email: Access Required: Project Database Credentials Needed
Hi Charlotte,

I hope this email finds you well. We are currently consolidating the telemetry data for our next project briefing, and I need your access credentials to the shared database to integrate the latest developments. Please send over your login details at your earliest convenience, so we can keep the project on schedule.

Thanks in adva

---

## ling · qwen-2.5-7b-instruct · true label phishing · said legitimate (wrong)

reason: the email appears to be a promotional travel offer and does not contain typical phishing or scam elements.

judge: grounded=1.0, supports=0.0

email: b a r g a i n a i r f a r e s your 1 - stop travel supplier air , hotels , cars , trains , tours , packages * * * call 1-888 - 5-bargain or 202-898 - 7887 for reservations * * * * * * receive a $ 10 discount by referrering to this email * * * roundtrip international airfares : athens frnkfrt london madrid milan munich nice paris rome vienna atlanta $ 819 $ 750 $ 410 $ 745 $ 778 $ 700 $ 730 $ 699 $

---

## ceas08 · qwen-2.5-7b-instruct · true label phishing · said legitimate (wrong)

reason: the email appears to be a legitimate cnn newsletter with links to video content.

judge: grounded=1.0, supports=1.0

email: CNN.com Daily Top 10
>+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+= >THE DAILY TOP 10 >from CNN.com >Top videos and stories as of: Aug  1, 2008  3:58 PM EDT >+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+= TOP 10 VIDEOS 1. PARIS HILTON TAKES ON MCCAIN http://www.cnn.com/video/partners/email/index.html?url=/video/politics/2008/08/06/wynter.paris.hilton.ad.cnn Paris Hilto

---

## ephishllm · qwen-2.5-7b-instruct · true label phishing · said legitimate (wrong)

reason: the email appears to be from a project manager and contains a relevant message about project documentation.

judge: grounded=1.0, supports=1.0

email: Latest Update on Project Documentation
Hey Liam,

I hope your day is going well! I know you're busy with the data visualization project, but I thought you’d like to check out this document related to your team’s current work. It contains some recent adjustments that could be pertinent.

Here's the link you need:

<<link>>

Let me know if you have any questions or need further clarification. Lookin

---

## enron · qwen-2.5-7b-instruct · true label phishing · said phishing (correct)

reason: the email contains suspicious links and is promoting a male enhancement product with misleading testimonials.

judge: grounded=1.0, supports=1.0

email: stronger , more powerful climaxes
male enhancement is achieving your goals of becoming a better man
90 % of males were interested in improving their sexual stamina ,
performance , and the size of their manhood . are you one of the 90 % ?
i ' m 67 years old . i was very wary of putting my details on the internet ,
but i am very pleased that it worked out for me . your product arrived only 2
days af

---

## ephishllm · qwen-2.5-7b-instruct · true label legitimate · said legitimate (correct)

reason: the email appears to be a routine project update from a team leader to a colleague.

judge: grounded=1.0, supports=1.0

email: Progress Update: Refurbishment Project Phases Completed
Hi Hazel,

I hope you're doing well. I'm writing to give you an update on the progress of the aircraft refurbishment project.

We've successfully completed the first two phases of the project ahead of schedule, which includes the deconstruction and inspection of internal components. The team did an excellent job managing the complexities invo

---

## spamassassin · qwen-2.5-7b-instruct · true label legitimate · said legitimate (correct)

reason: the email appears to be a news update from 2002 and does not contain any suspicious elements.

judge: grounded=1.0, supports=1.0

email: Tibetans see hint of detente with China
URL: http://www.newsisfree.com/click/-2,8418827,215/
Date: 2002-10-01T04:33:57+01:00

*World latest:* Dalai Lama's envoy hails first contact in 20 years.

---

## kaggle · qwen-2.5-7b-instruct · true label phishing · said phishing (correct)

reason: the email contains a suspicious link and attempts to诱骗受害者进行金融操作。

judge: grounded=1.0, supports=1.0

email: urgent news would you reflnance if you knew you ' d save thousands ? we can get you lnterest as low as 2 . 16 % . fill out our small form below and we ' ll show you how . get the house and / or car you always wanted , it takes less than a minute of your time http : / / www . ez - rate . info / qute / ido 501 . php john was enjoying sleeping near the tree .

---

## spamassassin · qwen-2.5-7b-instruct · true label phishing · said phishing (correct)

reason: the email contains multiple "click here" links without clear text, which is a common tactic in phishing attempts.

judge: grounded=1.0, supports=1.0

email: Chicago office base - without the office space? smbqt
**Your Fully Staffed office in Chicago is ready when you are.**

| Live telephone answering with call screen/announce/patch.  
Prestige address, phone, fax, e-mail, executive offices.  
Operational to serve your customers today.  
  
Chicago - Office, Inc. is the fast, easy and professional  
way to establish your fully flexible office base in 

---

## ephishllm · qwen-2.5-7b-instruct · true label phishing · said phishing (correct)

reason: the email contains a suspicious download link and unsolicited offer, which is a common tactic for phishing.

judge: grounded=1.0, supports=1.0

email: Unlock the Full Potential of Your Work with Free Project Tools!
Hello Logan,

Are you looking to enhance your digital content development skills? We have an exciting offer just for you! Download our "Project Tools.zip," which includes cutting-edge software tailored for renewable energy content creation, all at no cost!

By integrating these tools into your workflow, you can:
- Improve efficiency i

---

