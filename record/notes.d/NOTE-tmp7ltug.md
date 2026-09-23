---
status: Read
paper: LIT-tmpa9msy
title: 'Automatic Evaluation of Topic Coherence'
version: 1
date: '2026-09-23'
summary: >-
  Average pairwise PMI of a topic's top words, estimated on Wikipedia,
  correlates with human coherence ratings about as well as the paper's
  measure of annotator agreement. Knowledge-base and search-engine measures
  are less reliable. Read in full.
---

# NOTE-tmp7ltug: Automatic Evaluation of Topic Coherence

## Contribution

An automatic proxy for human judgments of topic coherence, cheap enough to
run on every topic of every model, and a comparison of the resources such a
proxy could be built on.

## Key insight

**A coherent topic is a set of words that people use together.** How often
the words co-occur in a large, broad reference corpus measures that
directly, and more reliably than a hand-built ontology or search-engine hit
counts.

## Key results

- PMI over Wikipedia (10-word window): ρ = 0.78 and 0.77 (news), 0.74 and
  0.77 (books), median and mean
- Inter-annotator agreement: 0.79 and 0.73 (news), 0.82 and 0.78 (books)
- Google title matches: 0.80 on news, 0.51 on books. Google log hits: 0.46
  and −0.19
- WordNet measures range from −0.31 to 0.66, and their rankings disagree
  between corpora

## Limitations

- **The agreement ceiling is not like-for-like.** One annotator against the
  mean of eight, versus the method against the mean of all nine
- **Corpora chosen for varied topic quality**, which raises rank
  correlations
- **LDA topics only, at one number of topics per corpus.** Whether PMI
  tracks human judgment for other models is untested here
- **A rating task, not Chang et al.'s intrusion task.** The two operationalize
  "interpretable" differently, and this paper does not compare them
- **No comparison with likelihood**, so it does not bear on Chang et al.'s
  likelihood finding directly
