---
number: 381
status: Active
formerly:
- SOTA-tmp3xeck
consensus: universal
consensus_note: >-
  Not doing it is what needs justifying, and the record can show the
  descendants rather than assert it: every contrastive document `#304` filed
  — `SOTA-360`, `SOTA-359`, `SOTA-363`, `SOTA-376` — scores against
  sampled negatives rather than normalising over a full candidate set, and
  CLIP (`LIT-588`) cites this line by name for its loss. What is *not*
  converged is the second half of the title: the guidance that `k` should
  fall as data grows is rarely restated and the vision line assumed the
  opposite. Read as of 2026-09.
title: 'Sample a handful of negatives instead of normalizing over the vocabulary, and let the count fall as the data grows'
version: 2
history:
- version: 2
  date: '2026-09-23'
  note: >-
    Re-sourced from LIT-609 to LIT-603, the same paper filed first; LIT-609
    is retired as its duplicate. The practice is unchanged.
tags:
- representation-and-encoding
- training-optimization
date: '2026-09-23'
source:
- LIT-603
introduced_by:
- LIT-603
implementations: []
---

# SOTA-381: Sample a handful of negatives instead of normalizing over the vocabulary, and let the count fall as the data grows

## Source

Mikolov et al. (2013), [LIT-603](../literature.d/LIT-603.md) — [ARXIV-1310.4546](https://arxiv.org/abs/1310.4546), §2.2.

## The claim

When the denominator of your objective ranges over a vocabulary too large to
enumerate, do not enumerate it. **Draw a few negatives from a noise
distribution and discriminate against those.**

And the part that gets dropped: **`k` is not a dial to turn up.** The paper's
own guidance is `k` in **5–20** for small datasets and **2–5** for large
ones — the number of negatives that helps *decreases* as the data grows.

## The honest framing of what the approximation is

Negative sampling descends from Noise-Contrastive Estimation, which
approximately maximises the log probability of the softmax. The paper
discards that property on purpose:

> we are only concerned with learning high-quality vector representations, so
> we are free to simplify NCE as long as the vector representations retain
> their quality

So negative sampling **is not an estimator of the softmax** and was never
claimed to be. It is a task chosen because its by-product is good. That
posture — the objective is a means, the representation is the end — is
inherited by every document in `#304`'s contrastive line, usually without the
sentence that licenses it. `THEORY-085` is the same shape arriving
independently: the InfoNCE bound is a certificate that saturates, and the
representation keeps improving past the point the certificate stops moving.

## The noise distribution is part of the method

The unigram distribution raised to the **3/4** power outperformed both the
plain unigram and the uniform "on every task we tried". No derivation is
offered and none has been supplied since; it is a measured constant that the
field carried forward. Worth knowing you are inheriting a tuned
hyperparameter rather than a principle.

## Conditions

- **The `k` guidance is for skip-gram word vectors** at 2013 scales, and
  nothing here tests it elsewhere. What generalises is the direction of the
  advice and the fact that somebody measured it.
- **The noise distribution matters as much as the count.** Negatives drawn
  from the wrong distribution make the discrimination trivial, which is
  [SOTA-361](SOTA-361.md)'s shortcut problem in another costume.
- **It gives up the likelihood.** If the downstream requirement is a
  calibrated probability over the vocabulary, this is the wrong objective and
  the paper would agree.
- **It is not the same experiment as the vision line**, and the record should
  not pretend otherwise. `SOTA-377` measures batch-size saturation for
  image-text contrastive pretraining; this measures `k` for skip-gram. They
  agree in direction and nobody has connected them.

## Known implementations

-

<!-- inactive-ok-file: LIT-609 — Superseded as a duplicate of LIT-603; named where the record says so -->
