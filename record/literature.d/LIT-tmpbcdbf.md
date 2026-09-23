---
status: Active
title: 'Distributed Representations of Words and Phrases and their Compositionality'
version: 1
tags:
- representation-and-encoding
- training-optimization
- signal-structure
date: '2026-09-23'
published: '2013-10-01'
arxiv: '1310.4546'
first_author: 'Mikolov'
keywords:
- 'negative-sampling'
- 'noise-contrastive-estimation'
- 'subsampling'
- 'skip-gram'
- 'phrase-vectors'
extends:
- LIT-tmpkfqzo
summary: >-
  Mikolov et al. (2013), [ARXIV-1310.4546](https://arxiv.org/abs/1310.4546). Where negative sampling comes
  from — and it is NCE with the consistency deliberately dropped, kept only
  because the vectors stay good. Also: the number of negatives that helps
  *falls* as the dataset grows, which is the opposite of what the vision
  contrastive line later assumed.
---

# LIT-tmpbcdbf: Distributed Representations of Words and Phrases and their Compositionality

Mikolov et al. (2013) — [ARXIV-1310.4546](https://arxiv.org/abs/1310.4546)

## Key takeaways

- **Negative sampling is defined here, and it is defined as a deliberate
  degradation.** It descends from Noise-Contrastive Estimation (Gutmann &
  Hyvärinen), which "can be shown to approximately maximize the log
  probability of the softmax". The paper then says the quiet part: *"we are
  only concerned with learning high-quality vector representations, so we are
  free to simplify NCE as long as the vector representations retain their
  quality."* **NEG is not an estimator of anything; it is a task that
  produces good vectors.** The record's contrastive documents inherit that
  posture without usually inheriting the sentence.
- **The number of negatives falls as the dataset grows.** `k` in the range
  **5–20** is useful for small datasets; for large ones "`k` can be as small
  as **2–5**". Stated plainly, unremarkably, in 2013.
- **The noise distribution is tuned and the tuning is reported.** The unigram
  raised to the **3/4** power beat both the plain unigram and the uniform
  distribution "on every task we tried" — an exponent with no derivation
  behind it, carried forward by everyone since.
- **Subsampling frequent words does two things at once.** It gives
  "significant speedup" *and* improves "accuracy of the representations of
  less frequent words". A throughput change that improves quality is rare
  enough to be worth its own document — [SOTA-tmpoaohk](../practices.d/SOTA-tmpoaohk.md).
- **Phrases as units.** Idiomatic phrases are not compositions of their
  words, so the paper finds phrases in text and learns vectors for them
  directly, "millions of phrases". The `what counts as a unit` question,
  asked and answered empirically.

## Standing in the anthology

Unit G of `#304`. It sources [SOTA-tmp3xeck](../practices.d/SOTA-tmp3xeck.md) (sample negatives; let the count
fall with data) and [SOTA-tmpoaohk](../practices.d/SOTA-tmpoaohk.md) (subsample frequent tokens).

**The `k` finding is the reason this unit was worth doing at all.** The
record now holds three arguments that the negative count is not a quality
dial — `THEORY-085`'s `log N` ceiling on the InfoNCE certificate, `LIT-591`'s
finding that batch-size gaps close with longer training, and `SOTA-tmptiobf`'s
measured saturation at 32k. This is a fourth, from a different literature,
**ten years earlier**, and pointing further: not merely that more negatives
stop helping, but that **fewer are needed as data grows**.

Four arguments, four literatures, none downstream of the others. Whether the
word-embedding case is really the same phenomenon is not settled here — the
objectives differ and nobody has connected them — but the record should at
least stop treating "more negatives is better" as something the field
believed uniformly. It did not; the text side said otherwise, first.
