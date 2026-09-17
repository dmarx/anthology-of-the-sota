---
status: Active
title: 'If Influence Functions are the Answer, Then What is the Question?'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-17'
published: '2022-09-12'
arxiv: '2209.05364'
first_author: 'Bae'
keywords:
- 'influence-functions'
- 'data-attribution'
- 'leave-one-out'
- 'proximal-bregman'
implementations: []
summary: >-
  Bae et al. (2022), [ARXIV-2209.05364](https://arxiv.org/abs/2209.05364). Decomposes the gap between influence
  estimates and leave-one-out retraining into five terms, finds that three of
  them are not errors at all, and identifies what influence functions on
  neural networks do estimate: the proximal Bregman response function.
---

# LIT-tmpyirk2: If Influence Functions are the Answer, Then What is the Question?

Bae et al. (2022) — [ARXIV-2209.05364](https://arxiv.org/abs/2209.05364)

## Key takeaways

- **The known failure, decomposed rather than deplored.** Influence estimates
  match leave-one-out retraining for linear models and match it poorly for
  neural networks. The gap splits into five terms: the warm-start gap, the
  proximity gap, the non-convergence gap, linearization error, and solver
  error
- **Only two of the five are errors.** Linearization and solver error are at
  least an order of magnitude smaller for most neural networks. The first
  three are *gaps* rather than errors — they reflect that the estimate is
  answering a different question, not answering the same one badly
- **The different question is the PBRF.** The proximal Bregman response
  function is the effect of removing a data point *while keeping predictions
  close to those of the trained model*. Influence estimates track it closely
  across binary classification, regression, image reconstruction, image
  classification and language modelling
- **So the method is not fragile; it was mislabelled.** The conclusion
  explicitly rejects the prevailing "influence functions are fragile" reading:
  they give accurate answers to a different question, and the PBRF is a better
  gold standard for evaluating them than retraining is
- **And the uses survive.** The paper states that the PBRF supports the same
  purposes that motivated influence functions — finding influential or
  mislabelled examples, and carrying out data-poisoning attacks. That sentence
  is what keeps a practice standing after its explanation was replaced

<!-- inactive-ok-block: THEORY-tmp7738v — Rejected, and named as the account this paper
     corrects. Citing the successor here would say the wrong thing: what this paper acts on
     is the old account. -->
## Standing in the anthology

Read — [NOTE-tmpiq1um](../notes.d/NOTE-tmpiq1um.md). Sources [THEORY-tmpz2g03](../theory.d/THEORY-tmpz2g03.md), which corrects
[THEORY-tmp7738v](../theory.d/THEORY-tmp7738v.md).
