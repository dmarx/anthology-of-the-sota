---
number: 15
status: Active
formerly:
- THEORY-tmp3pg79
title: 'Dropout regularizes by imposing a data-dependent penalty, not an isotropic one'
version: 1
tags:
- model-stability
date: '2026-09-17'
source:
- LIT-392
- LIT-393
- LIT-391
explains:
- SOTA-238
summary: >-
  Wager et al. (2013), [LIT-392](../literature.d/LIT-392.md) — for generalized linear models dropout is
  first-order equivalent to L2 applied after scaling the features by an
  estimate of the inverse diagonal Fisher information, so the penalty depends
  on the data and not only on the weights. Three derivations from three
  directions agree on that shape — inverse-curvature scaling here,
  variance-scaled weight decay in [LIT-393](../literature.d/LIT-393.md), ridge with a
  standard-deviation-scaled Gamma in [LIT-391](../literature.d/LIT-391.md) — and none of them covers a
  deep network.
---

# THEORY-015: Dropout regularizes by imposing a data-dependent penalty, not an isotropic one

## Source

Wager et al. (2013), [LIT-392](../literature.d/LIT-392.md), with
the same conclusion reached independently in Baldi and Sadowski (2013),
[LIT-393](../literature.d/LIT-393.md) §5, and in Srivastava et al.
(2014), [LIT-391](../literature.d/LIT-391.md) §9.1.

## What was actually shown

**The claim is about the metric, not the presence of a penalty.** For
generalized linear models, the dropout regularizer is first-order equivalent
to an **L2 regularizer applied after scaling the features by an estimate of
the inverse diagonal Fisher information matrix**. Weight decay penalizes
`‖w‖²`; this penalizes `‖w‖²` measured in a metric the data determines. That
is the content — "dropout is a regularizer" is not a finding, and "dropout is
like weight decay" is the reading this result contradicts.

**Three derivations, three model classes, one shape.**

- *Inverse curvature* — [LIT-392](../literature.d/LIT-392.md), GLMs:
  L2 under an inverse-Fisher scaling.
- *Input magnitude and noise variance* —
  [LIT-393](../literature.d/LIT-393.md) §5.1, a single linear unit
  under squared error: the expected dropout gradient is **exactly** the
  gradient of `E_ENS + ½ Σ wᵢ² Iᵢ² Var(δᵢ)`, a weight-decay term scaled by the
  input magnitudes and the dropout variance, maximal at `p = 0.5`. §5.2
  extends it approximately to a sigmoidal unit under relative entropy.
- *Input standard deviation* —
  [LIT-391](../literature.d/LIT-391.md) §9.1, linear regression:
  marginalizing the noise gives ridge with a `Γ` that scales each weight's
  cost by the standard deviation of its input dimension — "if a particular
  data dimension varies a lot, the regularizer tries to squeeze its weight
  more." Absorbing `p` into `w` makes the regularization constant `(1−p)/p`
  explicit, so decreasing retention increases regularization.

That three derivations with different assumptions land on a data-scaled
penalty is the reason the record believes the shape rather than any one
constant in it.

**The account makes a prediction and it comes out.** Because the regularizer
depends on the feature distribution and not on the labels, *unlabeled* data
can be used to estimate a better one.
[LIT-392](../literature.d/LIT-392.md) builds exactly that
semi-supervised variant and it consistently improves on dropout training in
document classification, including on IMDB. An interpretation that only
renames a procedure cannot be tested; this one was, in the direction it
predicted.

## What this does not say

**None of it covers a deep network.** The results are for generalized linear
models, a single linear unit, a single sigmoidal unit, and linear regression.
[LIT-391](../literature.d/LIT-391.md) §9.2 is explicit that no
closed-form marginalized model is available for logistic regression or deep
nets, and that the Gaussian assumptions such approximations rest on "become
successively weaker as more layers are added". Dropout is used almost
entirely in the setting none of these derivations reaches.

**It does not license replacing dropout with its marginalized regularizer.**
That is what the equivalence would suggest and what the papers decline to
claim past the model classes above.
[LIT-391](../literature.d/LIT-391.md) raises it as the way to get
dropout's benefit without its 2-3x training cost and reports that for anything
more complicated than linear regression "it is not obvious how to" obtain the
regularizer.

**The two accounts of dropout are not independent.**
[THEORY-016](THEORY-016.md) and this one are derived in the same
paper, and the sigmoidal case here *uses* the `NWGM` result there via a Taylor
expansion. Citing them as converging evidence would be double-counting; what
they are is one formalism answering two different questions.

**It is not why dropout is used.** This says what dropout does to the
objective. Whether doing that is worth 2-3x the training time, and in which
data regime, is a practice question — [SOTA-238](../practices.d/SOTA-238.md) — and the
answer there is conditional in a way this document has nothing to say about.
