---
status: Proposed
promote_when: >-
  A study by others, on topics from more than one model family (for example
  neural topic models as well as LDA), showing that average-PMI coherence
  over a large external corpus still ranks topics and models the way people
  do. It should compare against a single annotator's agreement with the
  rest, not a group mean. The source scored LDA topics only.
title: 'Score topic coherence automatically as the average pointwise mutual information of a topic''s top-word pairs, estimated on a large external reference corpus'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-tmpa9msy
introduced_by:
- LIT-tmpa9msy
consensus: unassessed
consensus_note: >-
  PMI-style coherence, in this and later variants, became the default
  automatic score for topic models. Adoption is not evidence (DP-005), and
  whether it holds beyond the LDA topics it was validated on has not been
  assessed here.
implementations: []
summary: >-
  Newman et al. (2010), [LIT-tmpa9msy](../literature.d/LIT-tmpa9msy.md) — when you cannot put every topic in
  front of people ([SOTA-368](SOTA-368.md)), approximate their judgment. Take the topic's
  top ten words and, for each of the 45 pairs, compute PMI from
  co-occurrence in 10-word windows over a large general corpus such as
  Wikipedia. Average the 45 scores. On 237 LDA topics this correlated with
  nine people's ratings at ρ ≈ 0.77, far better than WordNet measures.
---

# SOTA-tmpe36so: Score topic coherence automatically as the average pointwise mutual information of a topic's top-word pairs, estimated on a large external reference corpus

## Source

Newman et al. (2010), [LIT-tmpa9msy](../literature.d/LIT-tmpa9msy.md). Read as [NOTE-tmp7ltug](../notes.d/NOTE-tmp7ltug.md).

## The practice

- **Use an external corpus, not the training corpus.** The point is to ask
  whether people use these words together, so count co-occurrence somewhere
  broad and independent of the model's data. Wikipedia worked on both news
  and books topics
- **Score pairs in a sliding window.** PMI(wᵢ, wⱼ) = log p(wᵢ, wⱼ) /
  p(wᵢ)p(wⱼ), with co-occurrence in a 10-word window, averaged over the 45
  pairs of the top ten words
- **Prefer it to knowledge-base and search-engine scores.** WordNet measures
  were erratic, and Google collapsed on the books corpus
- **Treat it as a proxy for the human task ([SOTA-368](SOTA-368.md)), not a replacement.**
  Validate it against people on your own models before relying on it to
  choose between them

## Conditions

- **Validated on LDA topics only**
- **The agreement ceiling in the source is not like-for-like**, so "as good
  as a human annotator" overstates it. What is shown is a strong correlation
  with the group mean
