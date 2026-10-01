---
status: Active
title: 'Shortformer: Better Language Modeling Using Shorter Inputs'
version: 1
tags:
- training-optimization
- attention-techniques
date: '2026-10-01'
published: '2020-12-31'
arxiv: '2012.15832'
first_author: 'Press'
keywords:
- 'staged-training'
- 'subsequence-length'
- 'position-infused-attention'
- 'language-modeling'
- 'wikitext-103'
implementations: []
summary: >-
  Press, Smith and Lewis (2020), [ARXIV-2012.15832](https://arxiv.org/abs/2012.15832). Training a
  transformer language model on short subsequences first and then at the full
  length is faster *and* better than training at the full length throughout:
  on WikiText-103 (247M parameters, final length 3,072), 128 tokens for the
  first 50 epochs gives 17.52 dev perplexity against the baseline's 18.65.
  The paper credits the two-stage routine to BERT, which used it only for
  speed. Also introduces position-infused attention.
---

# LIT-tmpkql17: Shortformer: Better Language Modeling Using Shorter Inputs

Press, Smith and Lewis (2020) — [ARXIV-2012.15832](https://arxiv.org/abs/2012.15832)

## Key takeaways

- **Staged training (§4):** train on short subsequences, then switch to the
  target length, changing nothing else — batch size grows to keep tokens per
  batch fixed, and the optimizer state is not reset. The paper says the
  routine "was previously applied to speed up the training of BERT", and
  that its contribution is showing it also improves perplexity.
- **It is faster and better, not a trade.** On WikiText-103 with the
  Baevski & Auli model (247M parameters, final length 3,072, 205 epochs),
  starting at 128 tokens until epoch 50 gives 17.52 dev perplexity against
  18.65 for the baseline, finishing in 87% of its training time; until epoch
  100, 17.62 in 74% of the time. Test perplexity with sliding-window
  evaluation is 17.56 against 18.70.
- **Robust to the split:** every initial length of 1,024 or less that switches
  by epoch 125 beats the baseline by a large margin (Table 2). Shortening the
  second stage below 3,072 hurt, and up to six stages did no better than two.
- **Position-infused attention (§5):** add absolute position embeddings to
  queries and keys rather than to word embeddings, so cached representations
  from earlier subsequences can be attended to cheaply. Combined with staged
  training, a 1.65x training speedup.

## Standing in the anthology

Filed as the controlled test behind staged context extension, which the
record otherwise held only as a schedule frontier-scale reports run and do
not ablate. Its scale is the limit: one 247M model, sinusoidal positions, and
a final length of 3,072, three orders of magnitude short of the
million-token schedules that cite the practice today.
