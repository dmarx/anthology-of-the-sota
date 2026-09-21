---
number: 40
status: Active
formerly:
- THEORY-tmpacv6c
title: A metric that composes or thresholds per-token error turns a smooth capability curve into a sharp one, with nothing happening in the model
version: 1
tags:
- analysis-and-evaluation
- training-optimization
source:
- LIT-471
explains:
- SOTA-200
summary: >-
  Schaeffer et al. (2023), [LIT-471](../literature.d/LIT-471.md) — if per-token accuracy rises
  smoothly with scale, a metric demanding all `L` tokens goes as `p^L` and is
  flat-then-sharp by construction; a thresholded metric does the same by a
  step. Demonstrated by rescoring fixed outputs, and by manufacturing
  emergence in vision models that had never shown it.
---

# THEORY-040: A metric that composes or thresholds per-token error turns a smooth capability curve into a sharp one, with nothing happening in the model

## Source

Schaeffer, Miranda and Koyejo (2023), [LIT-471](../literature.d/LIT-471.md) — read as
[NOTE-220](../notes.d/NOTE-220.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-200](../practices.d/SOTA-200.md) | check whether an emergent capability is a metric artefact | the artefact has a closed form, so the check has an arithmetic target and a cheap positive test |

## The account

Assume the thing scaling laws assert: per-token cross entropy falls smoothly
with scale, so the probability `p` of emitting the correct token rises
smoothly toward 1. Now ask what a *score* does to that curve.

A metric that requires an `L`-token target to match exactly composes `p` with
itself `L` times. Under independence the score is `p^L` — and `p^L` plotted
against log-scale is near-zero for a long stretch and then turns up sharply,
because compounding a number below 1 is brutal until that number is close to
1. Nothing about the model is discontinuous. The exponent is.

A metric that thresholds does the same by a different route. Multiple Choice
Grade scores 1 when the correct option holds the highest probability mass and
0 otherwise; it is a step function applied to a continuous quantity, and a
step function crossed smoothly still reports a jump.

So "emergence" under such a metric is a statement about the composition of
the scoring function with the capability curve, not about the capability
curve. The test that follows is exact: **change the scoring function and hold
the outputs fixed.** If the sharpness was in the metric, a linear metric
(Token Edit Distance) or a proper scoring rule (Brier Score) on the identical
outputs returns a smooth curve.

A second, smaller term sits underneath. Composing `p` down to a small number
means the small models' true score is small but nonzero, and a test set too
coarse to resolve it reports zero. Zero looks like inability; it is often
resolution. Adding test data alone moved every InstructGPT/GPT-3 model above
chance without changing anything else.

## What was actually shown

The mechanism was demonstrated three ways, and the third is the one that
settles it. Rescoring GPT-3's fixed arithmetic outputs with Token Edit
Distance removed the emergence. Rescoring LaMDA under Brier Score removed it
on the tasks where Multiple Choice Grade showed it. And then the mechanism
was run **forwards**: shallow autoencoders on CIFAR-100 and Omniglot
transformers, neither of which had ever been reported as emergent, were given
a thresholded or all-or-nothing metric and produced sharp, unpredictable-looking
curves on demand.

Manufacturing the phenomenon is stronger evidence for the mechanism than
dissolving it, because dissolving one instance leaves open whether the
instance was special. Manufacturing it shows the metric is sufficient.

Corroborating the reach: >92% of hand-annotated BIG-Bench emergent abilities
sit under Multiple Choice Grade or Exact String Match — one discontinuous,
one nonlinear, which is exactly the pair this account predicts.

## What this does not say

**It does not say emergence is impossible.** The source says so in as many
words. A capability curve could genuinely be piecewise — Caballero et al.'s
broken scaling laws say so, and Michaud et al. give conditions — and this
account does not rule that out. It says a sharp plot is not evidence of one.

**It does not put a number on how much observed emergence is artefactual.**
The >92% counts which metrics the claims sit under, not how many claims
survive rescoring; most of them cannot be rescored, because the outputs were
never released.

**It does not cover intermediate-step emergence.** [LIT-470](../literature.d/LIT-470.md) §5.1
objected that the *quality of intermediate reasoning steps* also jumps, which
is not a property of how the final answer is scored. That objection is
untouched by this account and remains the strongest thing standing against it.

**The closed form assumes token independence**, which is false. It is an
illustration of the shape, not a fit — the account survives without it
because the qualitative claim is only that composing a probability `L` times
is convex in the wrong direction.

## Its relation to the other account

[THEORY-039](THEORY-039.md) explains the same practice from a different place. There, the
distortion is in what the *task asks of the model* — auxiliary demands the
weaker model pays more of, so scale paying down a demand looks like scale
unlocking a capacity. Here the distortion is downstream of the model
entirely: the outputs are fixed and the scoring function is the whole story.

Two independent mechanisms reaching the same advice is why
[SOTA-200](../practices.d/SOTA-200.md) is a check worth running rather than a special case.
