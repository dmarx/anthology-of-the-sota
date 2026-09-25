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
  LIT-395 §7.4, which reports both edges of the sweet spot; LIT-119,
  which reaches for dropout in 2026 under exactly the condition the 2014 paper
  predicts; and LIT-668, which in 2019 removed dropout from a model that
  would not overfit and gained on every task. No survey of current pretraining
  recipes supports the stronger reading, and this note is here so that the
  `converged` above is not read as covering it.
title: 'Apply dropout where the model can memorize what it is shown, and not where it cannot'
version: 4
history:
- version: 2
  date: '2026-09-21'
  note: >-
    Bounds the negative half. The verdict is about dropout applied THROUGHOUT
    training; LIT-475 shows the same operator on a prefix of training
    lowering training loss in exactly the regime where the throughout version
    costs ViT-T six points of ImageNet accuracy. A reader taking "not where it
    cannot" as "never" would miss SOTA-285. The recommendation is
    unchanged and its evidence is strengthened -- that six-point drop is now
    the clearest measurement in the record of the cost this practice warns
    about.
- version: 3
  date: '2026-09-25'
  note: >-
    Converts this document's own admission into a reported result. v2 said that
    where the sweet-spot curve leaves large-scale pretraining "is an inference,
    not a reported result", and that the record had not confirmed why current
    recipes set dropout to zero. LIT-668 is one confirmation, from 2019:
    ALBERT-xxlarge does not overfit after 1M steps, so dropout was removed, and
    MLM accuracy and every downstream task improve — 90.4 to 90.7 average. The
    authors claim priority for it and bound their own claim. The recommendation
    is unchanged; what changes is that its right edge now has a language model
    behind it and not only a 2014 MNIST curve read forward.
- version: 4
  date: '2026-09-25'
  note: >-
    A second language model on the right edge, and this time one with a
    standard architecture. LIT-681 trains a BERT-base-shaped MLM for a single
    epoch, and turning dropout on costs 0.8 MNLI-m (80.95 against 81.79).
    That is one run. The recommendation is unchanged. The note that the
    record had only "one 2019 encoder with an unusual architecture" no
    longer holds.
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
- LIT-668
- LIT-681
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

<!-- inactive-ok-file: SOTA-285 — Proposed, and named as the boundary case
     this practice's condition does not cover. Its unsettled status is part of
     what is said about it: the evidence for the boundary is vision only -->

<!-- inactive-ok-file: THEORY-044 — Proposed, named once as the account of
     that boundary case and not relied on by anything here -->

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

**Where that leaves large-scale pretraining was an inference; it now has one
reported result behind it.** If a corpus is large enough that a model sees most
of it once and cannot memorize it, the right edge of §7.4 predicts little to
gain — against a cost the same paper measures at 2-3x training time.
[LIT-668](../literature.d/LIT-668.md) reports the prediction coming true and gives the reason in the same
terms: after 1M steps ALBERT-xxlarge "still do[es] not overfit to [its] training
data", so dropout was removed, and MLM accuracy rose along with every downstream
task — **90.4 to 90.7 on average**, with SQuAD 1.1, SQuAD 2.0, MNLI, SST-2 and
RACE all improving. The authors claim priority (*"to the best of our knowledge,
we are the first to show that dropout can hurt performance in large
Transformer-based models"*) and immediately bound it, noting that ALBERT's
shared-layer structure is "a special case of the transformer".

So the right edge holds on one language model, for the reason the 2014 curve
gives. And 0.3 points of average on one configuration is a confirmation, not a
large effect.

[LIT-681](../literature.d/LIT-681.md) is the second, with an ordinary architecture. It is a
BERT-base-shaped MLM trained for 24 hours on one GPU over a single epoch, where
"overfitting is not possible". Dropout is off in pretraining and back on at 0.1
for fine-tuning. The one row that turns it on in pretraining gives **80.95
MNLI-m against 81.79** (its Table 12, one pretraining run). The paper's reason
is a different one from the 2014 curve: dropout "effectively reduces the number
of gradient updates seen by each parameter" at nearly the same step cost. That
argument is not measured. The outcome is, and it falls where this practice
predicts. What is still not surveyed is *current* recipes. This record has
two encoders, not a statement about why the field sets dropout to zero today.

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

## The verdict is about the schedule, not only the regime

`LIT-475` is the strongest single confirmation of the negative half
above: standard dropout costs ViT-T **six** points of ImageNet-1K top-1 —
73.9 down to 67.9 — on a model far too small to memorize 1.2M images, which
is this practice's condition being paid in full.

The same paper shows that dropout applied only for the first stretch of
training and then switched off *lowers training loss* on the same models. So
what the condition rules out is dropout as a standing regularizer on a model
that is not overfitting. It does not rule out the operator appearing briefly
at the start, where it is doing something else entirely
([SOTA-285](SOTA-285.md), explained by
[THEORY-044](../theory.d/THEORY-044.md)).

The evidence for that boundary is vision only, which is why it is a pointer
here rather than a change to this practice's claim.
