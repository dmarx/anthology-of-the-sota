---
number: 86
status: Proposed
formerly:
- THEORY-tmp7dspe
promote_when: >-
  An ablation that separates the two things LDA adds over a one-topic
  mixture: several topics per document, and a Dirichlet prior on the
  proportions. For example, a mixture of unigrams with matched Bayesian
  smoothing against LDA at equal numbers of topics, with held-out
  likelihood and a human judgment of topic quality, on corpora larger than
  the source's two. The source compares whole models, so the multi-topic
  claim and the prior are confounded.
title: 'A text document is better modelled as a mixture of several topics, each a distribution over words, than as a draw from a single topic'
version: 1
tags:
- signal-structure
- generative-modeling
date: '2026-09-23'
source:
- LIT-592
summary: >-
  Blei, Ng and Jordan (2003), [LIT-592](../literature.d/LIT-592.md) — exchangeability of a document's
  words implies, by de Finetti, a mixture over a latent parameter. LDA takes
  that parameter to be a per-document distribution over topics. It has lower
  held-out perplexity than a mixture of unigrams, which forces one topic per
  document, on AP newswire and C. elegans abstracts, at every number of
  topics. The multi-topic structure and LDA's Dirichlet smoothing are not
  separated, and perplexity is the only measure.
---

# THEORY-086: A text document is better modelled as a mixture of several topics, each a distribution over words, than as a draw from a single topic

## Source

Blei, Ng and Jordan (2003), [LIT-592](../literature.d/LIT-592.md). Read as [NOTE-322](../notes.d/NOTE-322.md).

## The account

A document is not about one thing. A newswire article about a foundation's
grants to an opera and a school draws its words from arts, money and
education at once (the paper's Figure 8). Modelled as a single topic, it
must be forced into one cluster, and any word that cluster rarely saw makes
its probability collapse. Modelled as a mixture, each word can come from
whichever topic suits it, and the document's topic proportions are a
compact description of what it is about.

## What it explains

- Why the mixture of unigrams overfits as topics are added (Table 1). Finer
  single-topic clusters leave more words unseen in each, and held-out
  perplexity explodes
- Why topic proportions work as a low-dimensional document representation.
  They matched full word features for classification with 0.4% of the
  dimensions

## Where it is weak

- **Confounded with the prior.** LDA differs from the mixture of unigrams in
  two ways, several topics per document and a Dirichlet prior. The paper
  does smooth the baseline, but it does not isolate the first
- **Perplexity only**, on two small corpora, and for bag-of-words models
- **A modelling claim about text, not a measurement of it.** The
  exchangeability it starts from is, in the authors' words, a simplifying
  assumption chosen for efficiency
