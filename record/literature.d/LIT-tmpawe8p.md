---
status: Active
title: 'Bootstrap your own latent: A new approach to self-supervised Learning'
version: 1
tags:
- representation-and-encoding
- model-stability
- vision-and-graphics
date: '2026-09-23'
published: '2020-06-01'
arxiv: '2006.07733'
first_author: 'Grill'
keywords:
- 'self-supervised-learning'
- 'representation-collapse'
- 'momentum-target-network'
- 'predictor'
- 'joint-embedding'
extended_by:
- LIT-tmp3roys
summary: >-
  Grill et al. (2020), [ARXIV-2006.07733](https://arxiv.org/abs/2006.07733). Learns a representation with no
  negatives at all: an online network predicts a slow EMA copy of itself
  under a different augmentation. 74.3% ImageNet linear. Why it does not
  collapse is a hypothesis in the paper, not a result, and [LIT-tmp3roys](LIT-tmp3roys.md)
  disputes which part is doing the work.
---

# LIT-tmpawe8p: Bootstrap your own latent: A new approach to self-supervised Learning

Grill et al. (2020) — [ARXIV-2006.07733](https://arxiv.org/abs/2006.07733)

## Key takeaways

- **No negatives, and the loss admits the trivial answer.** Two networks:
  an **online** one (encoder → projector → **predictor**) and a **target**
  one (encoder → projector, no predictor) whose weights are an exponential
  moving average of the online network's. The online network predicts
  `sg(target projection)` of a different augmented view; the loss is
  symmetrised by swapping which view goes where. Outputting a constant
  minimises this loss and the paper says so outright.
- **The argument for why it does not is structural, and it is a
  hypothesis.** The target's updates are *not* `∇_ξ` of the loss, so the
  authors "hypothesize that there is no loss `L_{θ,ξ}` such that BYOL's
  dynamics is a gradient descent on `L` jointly over `θ, ξ`" — explicitly
  likened to GANs. There is therefore no reason a priori for the parameters
  to reach that minimum.
- **The mechanism sketch, under an assumption that is not met.** With an
  *optimal* predictor `q*`, the online update follows in expectation
  `∇_θ E[Σ_i Var(z'_{ξ,i} | z_θ)]` — the expected conditional variance. Since
  `Var(X|Y,Z) ≤ Var(X|Y)`, discarding information from the online projection
  cannot lower it, and `Var(z'|z_θ) ≤ Var(z'|c)` for constant `c`, so the
  collapsed equilibrium is *unstable*. The authors' own gloss on the target
  network follows: its job may be to keep the predictor near-optimal, since
  a hard copy would propagate variability fine but "sudden changes in the
  target network might break the assumption of an optimal predictor".
- **The ablation is what the field remembered: remove either the predictor
  or the target network and it collapses.** Removing the predictor turns
  BYOL into an unsupervised Mean Teacher, and that collapses.
- **The ablation the field forgot is more interesting.** The target network
  *can* be removed without collapse if the predictor is kept near-optimal —
  by solving it in closed form on each batch (52.5% top-1) or merely by
  raising the predictor's learning rate (66.5%). Raising both the projector's
  and the predictor's learning rates instead gives ≈25%. So it is not
  asymmetry in general but the predictor's *relative* optimality that is
  load-bearing.
- **Numbers.** 74.3% ImageNet top-1 under linear evaluation with ResNet-50,
  79.6% with a larger ResNet. Augmentations are SimCLR's ([LIT-591](LIT-591.md)) plus
  solarization. Removing weight decay makes both BYOL and SimCLR diverge —
  a detail worth keeping, since it means the regulariser is part of the
  method rather than a default.

## Standing in the anthology

Unit C of `#304`, the cluster where the record's `representation collapse`
documents finally get their sources. Sources [SOTA-tmp1kmsu](../practices.d/SOTA-tmp1kmsu.md) with
[LIT-tmp3roys](LIT-tmp3roys.md).

The status is `Active` because the *method* works and is the ancestor of the
EMA-teacher family the record already holds through `LIT-216`. The
<!-- inactive-ok: THEORY-tmpf89jm — Deferred by design: the question is open and this cluster is where the record says so. Citing it is the point, not an oversight. -->
*explanation* is a separate question, and it is contested: [THEORY-tmpf89jm](../theory.d/THEORY-tmpf89jm.md)
files the dispute, in which `LIT-tmp3roys` removes the momentum encoder BYOL
says is essential and reports **67.7%** at 100 epochs, against the **0.3%**
BYOL reports for the same removal.
