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
- 'word2vec'
- 'negative-sampling'
- 'subsampling'
- 'phrases'
- 'additive-compositionality'
implementations:
- word2vec
extends:
- LIT-tmp9cbir
summary: >-
  Mikolov, Sutskever, Chen, Corrado and Dean (NIPS 2013), [ARXIV-1310.4546](https://arxiv.org/abs/1310.4546).
  Makes skip-gram fast and better. Negative sampling replaces the softmax
  with logistic regression against k noise words drawn from the unigram
  distribution raised to the 3/4 power. Frequent words are subsampled, with
  discard probability 1 − √(t/f) at t ≈ 10⁻⁵, which runs 2–10× faster and
  helps rare words. High-PMI bigrams become single tokens. Vector sums
  compose meanings, for example Russian + river ≈ Volga River.
compared_against:
- LIT-tmp1v5mg
---

# LIT-tmp55q30: Distributed Representations of Words and Phrases and their Compositionality

Mikolov, Sutskever, Chen, Corrado and Dean, Google (NIPS 2013) —
[ARXIV-1310.4546](https://arxiv.org/abs/1310.4546)

## Key takeaways

- **Negative sampling** (§2.2): for each observed pair, distinguish the true
  context word from k samples drawn from a noise distribution, using
  logistic regression. k = 5–20 for small data and 2–5 for large. Unlike NCE
  it needs only samples, not their probabilities
- **The noise distribution:** U(w)^{3/4}/Z "outperformed significantly the
  unigram and the uniform distributions … on every task we tried". No
  numbers are given
- **Subsampling frequent words** (§2.3, Table 1): discard each occurrence
  with probability 1 − √(t/f(w)), t ≈ 10⁻⁵. The rationale is that "the" is
  near every word and teaches little. Word analogies, 300d skip-gram:
  - NEG-5: 38 → 14 minutes, 59 → 60%
  - NEG-15: 97 → 36 minutes, 61 → 61%
  - HS-Huffman: 41 → 21 minutes, 47 → 55%
- **Phrases** (§4, Table 3): bigrams scored by (count(ab) − δ) /
  (count(a)·count(b)) above a threshold become single tokens, in 2–4 passes.
  On a new phrase-analogy set, subsampling helps a lot: NEG-15 goes 27 → 42%
  and HS goes 19 → 47%. The best model reaches 72% with 33B words
- **Additive compositionality** (§5, Table 5): the nearest tokens to
  vec(Russian) + vec(river) include Volga River. The authors' explanation is
  that vectors are log-linear in context probabilities, so a sum behaves
  like a product of context distributions, an AND

## Standing in the anthology

Filed on request with its predecessor ([LIT-tmp9cbir](LIT-tmp9cbir.md)) and with GloVe
([LIT-tmp1v5mg](LIT-tmp1v5mg.md)), which uses this paper's skip-gram and CBOW with negative
sampling as its baseline. It sources [SOTA-tmpt56rt](../practices.d/SOTA-tmpt56rt.md) (subsampling) and
[SOTA-tmpuwmrz](../practices.d/SOTA-tmpuwmrz.md) (the 3/4-power noise distribution), and is a source for
[THEORY-tmp472k3](../theory.d/THEORY-tmp472k3.md).

**`signal-structure`, because two of its methods rest on what text is
like.** Subsampling rests on the heavy head of the word-frequency
distribution. Phrase detection treats non-compositional multi-word units,
such as "Air Canada", as words. That is the property [LIT-410](LIT-410.md) and [LIT-409](LIT-409.md)
are about.

**The 3/4 exponent carries no evidence in the paper.** It is asserted to be
significantly better, with no table. It became a fixture of embedding and
retrieval code anyway.

Read — [NOTE-tmpd9zqq](../notes.d/NOTE-tmpd9zqq.md).

<!-- inactive-ok-file: SOTA-tmpuwmrz, THEORY-tmp472k3 — Proposed, filed in this same contribution from this paper -->
