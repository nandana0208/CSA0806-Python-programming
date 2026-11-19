# Task A5 – Design an AI Application for Citizen Complaints

## A5.1 Sentiment and summary
A lexicon scorer assigns positive scores to words such as `good`, `clean`, `improved`, and negative scores to `bad`, `smoke`, `unsafe`, and `polluted`. A preceding negation word (`not`, `never`, `no`) reverses the next sentiment word's contribution, so “not good” becomes negative. This is a lightweight rule-based baseline and does not understand all context, sarcasm or complex grammar.

An extractive summariser tokenises complaint sentences, counts frequent non-stopwords and selects the sentence(s) containing the highest-scoring important words. It reuses original sentences rather than generating new text.

## A5.2 Basic chatbot
The chatbot detects station names, date words and the pollutant name in a question, then queries SQLite. Example: “What is the PM2.5 in Adyar today?” maps to a parameterised SQL query for Adyar and the requested date. It should respond that data is unavailable if no matching observation exists.

Limitations: fixed keywords, limited spelling variation, ambiguous dates, no conversational memory, no deep language understanding and no ability to answer outside the database.

A trained Naive Bayes model requires labelled training examples and model storage. Prediction can be fast after training but has model-loading and memory costs; a pre-trained language model needs substantially more memory and compute. A trained model may improve generalisation over a word list when good representative training data exists, but accuracy is not guaranteed and must be evaluated on held-out complaints. A lexicon method is small and transparent, with per-complaint work roughly O(w) for w tokens.
