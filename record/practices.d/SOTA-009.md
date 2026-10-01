---
number: 9
status: 'Active'
title: 'warmup to a large early lr, anneal throughout training to small final lr'
version: 2
history:
- version: 2
  date: '2026-09-18'
  note: >-
    Adds `model-stability`. The schedule exists to get through early training without divergence, which is what the line it sits in is about (ADR-049).
tags:
- training-optimization
- model-stability
date: '2026-08-24'
source:
- LIT-010
introduced_by:
- LIT-010
summary: >-
  Smith et al. (2017), [LIT-010](../literature.d/LIT-010.md) — [ARXIV-1708.07120](https://arxiv.org/abs/1708.07120).
compared_against:
- SOTA-100
---

# SOTA-009: warmup to a large early lr, anneal throughout training to small final lr

## Source

Smith et al. (2017), [LIT-010](../literature.d/LIT-010.md) — [ARXIV-1708.07120](https://arxiv.org/abs/1708.07120).

## The shape, and what each part is doing

Ramp to a peak, then decay to a small final value. The ramp is [SOTA-008](SOTA-008.md)'s
argument; the decay is the part this practice adds, and its justification is
different: late in training the gradient's useful component is small relative
to its noise, so a large step mostly moves the parameters around a basin
rather than into it. Shrinking the rate turns the run from exploring to
settling.

The shape as one recommendation comes from LIT-010. Smith and Topin's "1cycle"
policy is a single cycle of rising then falling rate, shorter than the run.
After it the rate falls "several orders of magnitude less than the initial
learning rate" for the remaining iterations. On CIFAR-10 with a 56-layer
ResNet, their super-convergence run reached 92.4% test accuracy in 10,000
iterations, where piecewise-constant training peaked at 91.2% after about
80,000. Warmup alone is not theirs: the paper credits it to He et al. (2016)
and Goyal et al. (2017), and treats it as a discretised version of a cyclical
learning rate.

SOTA-100 also puts a ramp at the start of training, and for a different
reason: Post-LN transformers have large gradients near the output at
initialisation. Its source, LIT-114, trained Post-LN baselines with a linear
warmup followed by decay (inverse square root in its main experiments), which
is this practice's shape. On IWSLT14 De-En the result was sensitive to the
ramp's length: with
T_warmup = 500, Adam reached only 31.16 and 2.77 BLEU at peak rates of 5e-4
and 1e-3. Under Pre-LN the same paper drops warmup. So SOTA-100's
justification for the ramp lapses with the architecture, while this
practice's justification for it does not.

## What has moved, and it is most of this

<!-- inactive-ok-block: SOTA-039 — Superseded, named as the default this practice describes and as what replaced it -->
The record's own line has largely left this shape. [SOTA-039](SOTA-039.md) — a single cosine
cycle, the default this practice describes — is Superseded by [SOTA-140](SOTA-140.md)'s
warmup-stable-decay, and the reason is a property the cosine shape lacks:
cosine has to know the total token budget in advance, because the schedule's
endpoint is baked into its curve. Stable-then-decay leaves the budget open,
so a run can be extended without invalidating the schedule it has been
following.

<!-- inactive-ok-block: SOTA-141, SOTA-156 — Proposed, cited as how far past this shape the record's line has gone -->
[SOTA-141](SOTA-141.md) goes further and decays linearly to exactly zero, and [SOTA-156](SOTA-156.md) argues
the schedule can be dispensed with entirely by averaging iterates.

So this practice is best read as the frame those variations are stated
against — "warm up, then anneal" is still the shape, and every specific answer
about *how* has moved past it. Kept Active because the frame holds; a reader
choosing a schedule today should be reading [SOTA-140](SOTA-140.md) rather than this.
