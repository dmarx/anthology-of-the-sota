---
status: Active
title: 'Reading Tea Leaves: How Humans Interpret Topic Models'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-23'
published: '2009-12-01'
# NIPS 2009. No arXiv version and no DOI, so the source is the proceedings
# page (ADR-009).
url: 'https://papers.nips.cc/paper_files/paper/2009/hash/f92586a25bb3145facd64ab20fd554ff-Abstract.html'
first_author: 'Chang'
keywords:
- 'topic-models'
- 'interpretability'
- 'human-evaluation'
- 'word-intrusion'
- 'topic-intrusion'
- 'held-out-likelihood'
implementations: []
compared_against:
- LIT-592
summary: >-
  Chang, Boyd-Graber, Gerrish, Wang and Blei (NIPS 2009). Two Mechanical Turk
  tasks measure whether a topic model's latent space means anything to
  people. In word intrusion, subjects find the odd word out among a topic's
  top five. In topic intrusion, they find the topic that does not belong to
  a document. On pLSI, LDA and CTM at 50, 100 and 150 topics over NYT and
  Wikipedia, CTM has the best held-out likelihood and the worst human scores.
  LDA is usually best. The paper concludes that likelihood does not track
  interpretability, and it reads the trend as a negative correlation.
---

# LIT-tmpmiyeb: Reading Tea Leaves: How Humans Interpret Topic Models

Chang, Boyd-Graber, Gerrish, Wang and Blei, Princeton, Maryland and Facebook
(NIPS 2009) — <https://papers.nips.cc/paper_files/paper/2009/hash/f92586a25bb3145facd64ab20fd554ff-Abstract.html>

## Key takeaways

- **The gap it names** (§1–2): topic models are presented and used as if
  their topics were meaningful, for browsing, corpus exploration and model
  checking. But they are evaluated by held-out likelihood or external tasks,
  and nobody had measured the meaning
- **Word intrusion** (§3.1): show the five most probable words of a topic
  plus an intruder, a word improbable in this topic but probable in another.
  Model precision is the fraction of subjects who pick the planted intruder
- **Topic intrusion** (§3.2): show a document's title and first sentences,
  its three most probable topics, and one improbable topic. Topic log odds
  compares the model's probability for the planted intruder with its
  probability for the one subjects picked
- **Setup** (§4.1–4.3): 8,447 NYT articles and 10,000 Wikipedia articles,
  with proper nouns removed so subjects did not need encyclopedic knowledge.
  pLSI, LDA and CTM at K = 50, 100 and 150, with 20% held out. Each task was
  done by 8 Mechanical Turk workers
- **Likelihood** (Table 1): CTM is generally best, then LDA, then pLSI. The
  gaps are small, for example NYT at 50 topics: LDA −7.3214, CTM −7.3335,
  pLSI −7.3384
- **Humans** (Figures 3 and 6): on word intrusion LDA usually does best and
  CTM worst, and pLSI degrades as K grows. On topic intrusion, LDA and pLSI
  beat CTM. Topic log odds are nearly flat across K for LDA and pLSI
- **Where people and model disagree** (Figure 4): agreement is highest on
  documents about one unambiguous concept ("Lindy Hop") and lowest on
  documents that span disparate areas ("Book")

## Standing in the anthology

Filed on request, after Latent Dirichlet Allocation ([LIT-592](LIT-592.md)). It is
`compared_against` that paper, whose model it evaluates, and it sources
[SOTA-tmpa7058](../practices.d/SOTA-tmpa7058.md). It also answers the gap [NOTE-322](../notes.d/NOTE-322.md) recorded: whether low
perplexity means topics a person would recognize.

**The claim that travels is stronger than the evidence.** The discussion says
likelihood-based metrics "are, indeed, negatively correlated" with the human
measures. What the figures show is 18 fitted models with downward regression
lines, driven mostly by one model: CTM has the best likelihood and the worst
interpretability. Within LDA and pLSI, topic log odds barely move across K,
and no correlation coefficient is reported for the likelihood relationship.
What is well supported is the weaker claim: likelihood does not track
interpretability, and CTM is a clean counterexample.

Read — [NOTE-tmppi0z8](../notes.d/NOTE-tmppi0z8.md).
