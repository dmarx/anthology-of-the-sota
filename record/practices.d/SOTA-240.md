---
number: 240
status: Active
formerly:
- SOTA-tmpdicl5
consensus: converged
consensus_note: >-
  Dropout itself is not in dispute: it is in every framework, and not
  implementing it is what would need justifying. What this record has assessed
  is narrower than that — the *conditional*, that the decision turns on
  whether the model can memorize what it is shown. The grounds are
  LIT-395 §7.4, which reports both edges of the sweet spot, and LIT-119,
  which reaches for dropout in 2026 under exactly the condition the 2014 paper
  predicts. No survey of current pretraining recipes supports the stronger
  reading, and this note is here so that the `converged` above is not read as
  covering it.
title: 'Apply dropout where the model can memorize what it is shown, and not where it cannot'
version: 1
tags:
- model-stability
date: '2026-09-17'
# LIT-175 is deliberately NOT here. It produced evidence that multi-epoch
# training on a fixed corpus overfits severely — the CONDITION this practice
# turns on — but it tested objective augmentation, not dropout. ADR-017 sends
# problem-setting work to the prose rather than the field, and the Source
# section names it there.
source:
- LIT-395
- LIT-119
introduced_by:
- LIT-394
implementations:
- 'Falcon-H1-Tiny (0.1 after the linear projections, for a repeated FIM corpus)'
summary: >-
  Srivastava et al. (2014), [LIT-395](../literature.d/LIT-395.md) — dropout has a "sweet spot" in
  dataset size and reports both of its edges: no gain at all on data small
  enough to memorize through the noise, and a declining gain once the data is
  large enough that overfitting is not the problem. It costs 2-3x training
  time and it is not a drop-in — the paper's own recipe pairs it with n/p
  units, 10-100x the learning rate, momentum 0.95-0.99 and a max-norm
  constraint. Introduced by Hinton et al. (2012), [LIT-394](../literature.d/LIT-394.md).
explained_by:
- THEORY-015
- THEORY-016
---

# SOTA-240: Apply dropout where the model can memorize what it is shown, and not where it cannot

## Source

Srivastava et al. (2014), [LIT-395](../literature.d/LIT-395.md) —
JMLR 15:1929-1958. Introduced by Hinton et al. (2012),
[LIT-394](../literature.d/LIT-394.md) —
[ARXIV-1207.0580](https://arxiv.org/abs/1207.0580).

The condition is in the first sentence of the 2012 paper and has been part of
the claim ever since: *a large network trained on a small training set*.
Dropout is a treatment for a model with enough capacity to memorize what it
is being shown. It is not a default to carry into a setting where that is not
true, and it has never been presented as one.

## The sweet spot, and why both edges matter

[LIT-395](../literature.d/LIT-395.md) §7.4 varies MNIST training
set size — 100, 500, 1K, 5K, 10K, 50K — against one fixed architecture with
`p = 0.5` hidden and `0.8` input. **At 100 and 500 examples dropout gives no
improvement at all**: the model can overfit through the noise. The gain then
rises with data size "up to a point and then declines", because past that
point overfitting is no longer what limits the model. The paper's own words
for what it found: a sweet spot at "some amount of data that is large enough
to not be memorized in spite of the noise but not so large that overfitting
is not a problem anyways."

Both edges are the useful part. A practice derived only from the left one
would say *more data, more dropout*; a practice derived only from the right
one would say the opposite. What the curve actually supports is a ratio
claim, which is why this practice is stated as one.

**Where that leaves large-scale pretraining is an inference, not a reported
result.** If a corpus is large enough that a model sees most of it once and
cannot memorize it, the right edge of §7.4 predicts little to gain — against
a cost the same paper measures at 2-3x training time. The record has not
surveyed current pretraining recipes to confirm that this is why they set
dropout to zero, and until it has, that sentence is the anthology reading a
2014 curve forward rather than a claim anybody has checked at scale.

**The converse case is live and recent.**
[LIT-119](../literature.d/LIT-119.md) reports dropout 0.1 after the linear
projections recovering HumanEval-FIM "under the heavy repetition of a small
FIM corpus" — a 2026 model report reaching for a 2012 technique under the
condition the 2014 paper predicts it works in.
[LIT-175](../literature.d/LIT-175.md) is the same regime seen whole:
multi-epoch training on a fixed corpus overfits severely, and the objective
augmentations it proposes — token-level noise among them — are dropout's
question asked again about the data rather than the units.

## It is not a drop-in, and the paper says so

Appendix A of [LIT-395](../literature.d/LIT-395.md) is a coupled
recipe, and adding `p = 0.5` to an otherwise unchanged configuration is not
what it reports:

- **At least `n/p` units** where `n` was optimal without dropout. Only `pn`
  are present in expectation, so the layer has to be widened to compensate.
- **10-100x the learning rate** that was optimal without it, because dropout
  noise makes gradients cancel. **Momentum 0.95-0.99** rather than the usual
  0.9.
- **Max-norm, `c` typically 3-4** — needed *because* of the high learning rate
  and momentum above, to stop the weights growing. The paper reports
  dropout + max-norm as better than either alone (1.05 vs 1.35 and 1.25 on its
  comparison).
- **`p` of 0.5-0.8 for hidden units, 0.8 for real-valued inputs.** Smaller `p`
  needs bigger `n`, which slows training and can underfit; larger `p` may not
  regularize enough.

The cost is **2-3x training time** for the same architecture, and the paper
attributes it to the noise rather than to the masking arithmetic: each case
trains a different random architecture, so the gradients are not gradients of
the network that will be used.

**Gaussian multiplicative noise is the cheaper variant on one axis.**
Multiplying activations by `N(1, σ²)` with `σ² = (1−p)/p` matches Bernoulli
dropout's first two moments, requires no test-time weight scaling at all, and
is reported as as good or slightly better (MNIST 0.95 vs 1.08; CIFAR-10 12.5
vs 12.6).

## Known implementations

- Falcon-H1-Tiny — dropout 0.1 after the linear projections, for a repeated
  FIM corpus ([LIT-119](../literature.d/LIT-119.md)).
