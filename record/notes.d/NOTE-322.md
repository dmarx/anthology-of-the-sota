---
number: 322
status: Read
formerly:
- NOTE-tmp5yu4p
paper: LIT-592
title: 'Latent Dirichlet Allocation'
version: 1
date: '2026-09-23'
summary: >-
  The bag-of-words assumption, read through de Finetti, implies a
  document-level mixture. LDA is that mixture with Dirichlet topic
  proportions. It generalizes better than one-topic-per-document and
  per-document-parameter models by held-out perplexity. Main text read in
  full; the variational derivations in the appendices skimmed.
---

# NOTE-322: Latent Dirichlet Allocation

## Contribution

A fully generative model of a text corpus in which each document mixes
several topics, derived from the exchangeability that bag-of-words methods
already assume, with tractable variational inference.

## Key insight

**Take the bag-of-words assumption seriously and it hands you the model.**
Exchangeable words are conditionally i.i.d. given something, and making that
something a per-document distribution over topics lets a document be about
several things at once. Making it random, not a parameter, lets the model
score documents it has not seen.

## Key results

- Lowest held-out perplexity at every number of topics on C. elegans
  abstracts and AP newswire (Figure 9)
- Uncorrected baselines overfit badly: mixture of unigrams 4.19 × 10¹⁰⁶ and
  pLSI 5.04 × 10⁶ perplexity at 50 topics on AP (Table 1)
- 50 topic proportions match or beat 15,818 word features for SVM
  classification on two Reuters tasks (Figure 10)
- Best predictive perplexity for held-out movies on EachMovie (Figure 11)

## Limitations

- **The pLSI comparison uses folding-in**, which by the authors' account
  gives pLSI an unfair advantage. LDA still wins, so the direction holds
- **The classification features were fit on all documents,** test documents
  included (without labels). The authors say the result "need[s] further
  substantiation"
- **Perplexity is the only measure of topic quality.** Whether low perplexity
  means topics a person would recognize is not tested here, and the record
  holds no later work on it
- **Bag of words by design.** The paper states it is not doing language
  modeling, and word order is discarded
- **Two small corpora**, with results shown only as plots
