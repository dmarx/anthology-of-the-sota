---
status: Active
title: 'The plateau before factual recall is the formation of the attention circuit that recall needs'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-tmpbtdlg
explains:
- SOTA-tmp8nitg
summary: >-
  Zucchet et al. (2025), [LIT-tmpbtdlg](../literature.d/LIT-tmpbtdlg.md) — during the plateau between generic
  statistics and entity-specific knowledge, the attention circuit that
  selects an attribute value is being built, and until it exists the error at
  the attribute token does not reach the name tokens. Shown by patching a
  reference model's attention patterns in, which removes the plateau
  entirely.
---

# THEORY-tmp8a4gm: The plateau before factual recall is the formation of the attention circuit that recall needs
<!-- inactive-ok-file: SOTA-tmp8nitg — Proposed, and filed in this same contribution as the practice this explains; also named in `explains:` -->

## Source

Zucchet et al. (2025), [LIT-tmpbtdlg](../literature.d/LIT-tmpbtdlg.md) — [ARXIV-2503.21676](https://arxiv.org/abs/2503.21676).

## What was actually shown

Training on a factual-recall task passes through three phases: a short one
learning generic attribute-value statistics, a long plateau sitting at
exactly the loss an ideal model with no entity-specific knowledge would
reach, and then the acquisition of entity-attribute associations. The
plateau's length grows almost linearly with the number of entities.

The claim is that the plateau *is* the extraction circuit being built. Three
pieces of evidence, and the first is an intervention:

- **Attention patching removes the plateau.** Take a reference model's
  attention patterns from some point in its training and substitute them into
  a second model throughout that model's training. Patterns from later in the
  plateau work progressively better, and post-plateau patterns make the
  plateau disappear.
- **Patterns from very early training are worse than the untrained ones** —
  the model is then attending to attribute-type tokens to predict the generic
  distribution, which is the wrong place for recall, and this slows learning.
- **Attention to name tokens rises through the plateau**, measured at exactly
  the position that tests recall.

The mechanism: factual recall runs through a known circuit in which a late
attention operation selects the value matching the attribute type. Without
it, the prediction error at the attribute token is spread across irrelevant
positions instead of flowing back to the name tokens — so the key-value store
in the MLPs gets no usable signal, and the loss sits still.

The near-linear scaling of plateau length with population also supports a
statistical reading over a pure saddle-point one: the model must see an
entity several times to discover that attribute values are entity-specific.

## The picture it installs

**A flat loss can be a prerequisite under construction, and the flatness is
causal.** The model is not failing to make progress during the plateau; it is
making the only progress available, on a component whose value does not show
up in the loss until it is finished — and which the rest of the model needs
before *its* gradients mean anything.

That reframes what a plateau is evidence of. The instinct is to treat it as a
sign the run is stuck, the learning rate is wrong, or the data is bad. Here
it is a sign that a shared piece of machinery is being built, and the useful
question becomes what would build it faster.

## What this does not say

**It does not say all plateaus are circuits.** This is one plateau in one
task, and the patching method that established it has not been run anywhere
else. The paper's own cited neighbours — repetition helping arithmetic
training, low task diversity shortening plateaus on synthetic Markov mixtures
— are suggestive and are not the same measurement.

**It does not transfer the numbers.** Plateau length scaling with population
size is measured where population size is exactly known, which is what a
synthetic setting buys and a natural corpus does not have.

**It does not make the schedule free.** The practice it explains
([SOTA-tmp8nitg](../practices.d/SOTA-tmp8nitg.md)) follows from the mechanism, and the mechanism says nothing
about the out-of-distribution cost of training on a concentrated
distribution — which the neighbouring literature says exists.

**It does not identify the circuit uniquely.** The patching shows *some*
attention structure is the bottleneck and the attention-to-name measurement
shows it has the right signature, which together are strong. It is not the
same as having ablated the specific extraction circuit and watched recall
fail.

## Why `Active`

Because the central claim is established by intervention rather than
correlation. Patching the attention patterns in makes the plateau go away;
that is a causal test, and it came out the way the account predicts. Two
further signatures agree with it.

The limits are limits of scope — one task, one synthetic setting, one
plateau — rather than doubts about whether the account holds where it was
measured. What would make it more valuable is not more confidence but more
reach: the patching method is portable, and running it on a plateau nobody
has explained would say whether this is a general shape or a local fact.
