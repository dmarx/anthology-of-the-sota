---
status: Active
title: 'Drop Dropout on Single-Epoch Language Model Pretraining'
version: 1
tags:
- model-stability
date: '2026-09-18'
published: '2025-05-01'
arxiv: '2505.24788'
first_author: 'Liu'
keywords:
- 'dropout'
- 'pretraining'
- 'single-epoch'
- 'early-dropout'
- 'model-editing'
implementations: []
summary: >-
  Liu et al. (2025), [ARXIV-2505.24788](https://arxiv.org/abs/2505.24788), Findings of ACL 2025. The experiment
  SOTA-240 said nobody had run. Pretraining BERT and Pythia 160M/1.4B for a
  single epoch at varying dropout rates: **every capability measure is worse
  with dropout than without** — LM loss, BLiMP, SQuAD F1, MNLI — and the rate
  correlates with the size of the harm. "Early dropout" degrades too. Models
  trained without it are also more editable under MEND. So the right edge of
  Srivastava's sweet spot is not merely diminishing returns in this regime; it
  is a cost.
---

# LIT-tmpn2vpg: Drop Dropout on Single-Epoch Language Model Pretraining

Liu et al., Stanford (2025) — [ARXIV-2505.24788](https://arxiv.org/abs/2505.24788), Findings of ACL 2025

## Key takeaways

- **The gap it fills, in its own words.** Dropout has quietly disappeared from
  large-model pretraining on the reasoning that a single epoch cannot overfit,
  and "no thorough empirical investigation has been done on the role of
  dropout in LM pretraining." This is that investigation.

- **The result is one-directional.** Across every capability evaluated, models
  pretrained *with* dropout did worse than models pretrained without it: mean
  language-modelling loss, BLiMP (morpho-syntax), SQuAD F1 (question
  answering), and marginally MNLI (inference). **And the dropout rate
  correlates with the size of the effect** — more dropout, more harm.

- **Both architectures, three models.** Masked (BERT) and autoregressive
  (Pythia 160M and 1.4B), single-epoch, several seeds, at varying rates.

- **"Early dropout" does not rescue it.** Applying dropout for an initial
  portion of training and then disabling it — proposed elsewhere as a
  stabilization technique — also degrades performance relative to no dropout
  at all.

- **A second axis nobody had looked at: editability.** Models trained without
  dropout are statistically more successful under gradient-based editing
  (MEND), and indistinguishable under representation-based editing (ReFT).
  The authors' hypothesis is that dropout "non-discriminately limits
  co-adaptation in input features, leading to less localized representations
  of knowledge, resulting in multiple independent copies of facts stored" —
  which makes a gradient-based edit have to find all the copies. ReFT is
  unaffected because it edits orthogonal subspaces.

- **Stated limitations, and they are the right ones.** The paper makes **no
  theoretical claim** and says so, noting that the expected value of dropout
  converges to the identity (citing Baldi and Sadowski) and that the
  first-order-regularizer lens (citing Wager et al.) would be the fruitful way
  in. Overfitting emerges with parameter count and 1.4B is the ceiling here,
  so the scaling argument is inference from the trend rather than measurement.

## Standing in the anthology

**It closes the question [SOTA-240](../practices.d/SOTA-240.md) was filed
with.** That practice said, in its own body, that reading Srivastava et al.
§7.4's right edge forward to large-scale pretraining was "the anthology
reading a 2014 curve forward rather than a claim anyone has checked at scale",
and asked for someone to check it. Someone did, and the answer is stronger
than the practice's own framing: in the single-epoch regime dropout is not
merely unnecessary, it is **harmful**, monotonically in the rate.

The practice now sources it and the hedge is gone.

**And it lands exactly on the two theory documents already here.** Its
limitations section names [LIT-393](LIT-393.md) and [LIT-396](LIT-396.md) —
Baldi and Sadowski, Wager et al. — as the accounts a theoretical treatment
would have to go through, which are [THEORY-016](../theory.d/THEORY-016.md)
and [THEORY-015](../theory.d/THEORY-015.md). The record holds both, and holds
no such treatment, which makes this a named open question rather than a
vague one.
