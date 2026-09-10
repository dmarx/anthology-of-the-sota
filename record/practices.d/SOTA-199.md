---
number: 199
status: Active
formerly:
- SOTA-tmptrepp
consensus: converged
consensus_note: >-
  The same instrument as the KL-to-reference term every RLHF pipeline runs,
  arrived at independently in supervised fine-tuning. What is not converged is
  anyone stating it as one idea.
title: "Regularize a narrow fine-tune against the pre-fine-tuning model's own samples"
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-10'
published: '2022-08-01'
source:
- LIT-079
implementations:
- DreamBooth
---

# SOTA-199: Regularize a narrow fine-tune against the pre-fine-tuning model's own samples

## Source

Ruiz et al. (2022), [LIT-079](../literature.d/LIT-079.md) — DreamBooth, which names the failure and supplies
the cheapest possible fix for it.

## The failure

Fine-tuning on a few examples of one thing destroys the model's ability to
produce the general class it belongs to. DreamBooth calls this **language
drift**, alongside a collapse in output diversity: bind a token to five photos
of one dog and the model forgets how to draw dogs.

This is the ordinary cost of a narrow update, and it is usually paid or worked
around with early stopping.

## The fix

**Supervise the model with its own generated samples.** Before fine-tuning,
sample the frozen model on the general class — "a [class noun]" — and include
those samples in the fine-tuning objective as a class-specific
prior-preservation loss.

No external dataset, no held-out set, no separate teacher. **The model before
you touched it is the regularizer**, and it is available for free because you
have it.

## The general form

This is the same instrument as the KL-to-reference penalty in the record's
post-training neighbourhood — keep the updated policy close to the one you
started from — arrived at independently, in supervised fine-tuning, for the same
reason. The record carries that idea as an RL mechanism and nowhere as a general
statement about fine-tuning.

Stated generally: **when a narrow update risks destroying a general capability,
distil the capability out of the pre-update checkpoint and put it in the
objective.** The pre-update model is a complete specification of the behaviour
you are trying not to lose, and sampling from it is cheaper than finding data
that describes it.

## Conditions

Images, 2022, 3–5 reference examples. The prior being preserved has to exist —
the class noun must name something the model already produces well, or there is
nothing to sample.

The loss term has a weight and `LIT-079` does not sweep it, which is odd for the
component doing the work.

DreamBooth also reports a pipeline-level finding that generalises past its
domain: the super-resolution stages **must be fine-tuned too** or they
hallucinate detail they have not seen for the new subject. The thing to
regularize is the whole pipeline, not the component you were thinking about.

## Known implementations

- DreamBooth's class-specific prior preservation loss
