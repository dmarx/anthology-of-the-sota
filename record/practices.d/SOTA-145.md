---
number: 145
status: Active
formerly:
- SOTA-tmp8u4ld
consensus: converged
consensus_note: >-
  Every reasoning recipe in this record runs it — R1 (LIT-164), Olmo 3's RLVR
  stages (LIT-130), Falcon-H1-Tiny at 0.6B (LIT-119) — and the three papers
  that attack GRPO's objective (LIT-167, LIT-168, LIT-180) all keep the group
  baseline while changing something else. The dissent is about the objective's
  details, not about dropping the critic.
title: 'Estimate the RL baseline from a group of samples for the same prompt instead of training a critic'
version: 4
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to LIT-167 as well. The body enumerates four works that run or
    rework GRPO and observes that all four keep the group baseline; three
    were in the field and the fourth was not, so the count the practice
    argues from could not be checked against it. The recommendation is
    unchanged.
- version: 3
  date: '2026-09-07'
  note: >-
    "What this does not say" gained a third limit: the practice does not say
    policy-gradient RL is the right family. Evolution strategies at scale is
    a rival paradigm, now a Proposed practice of its own and recorded in
    `compared_against:`. The recommendation is unchanged.
- version: 4
  date: '2026-10-03'
  note: >-
    Flow-GRPO (LIT-tmpdktqx) added as a source: the first evidence in the
    record from outside language, GRPO's group baseline run unchanged on a
    flow-matching image model. It carries a condition on group size (24
    stable; 12 and 6 collapsed). The recommendation and consensus are
    unchanged.
tags:
- adaptation-and-tuning
date: '2026-09-07'
source:
# The practice's case is that four works which run or rework GRPO all keep
# the group baseline. Three were named here; LIT-167 — Dr. GRPO, which
# removes a length bias and keeps the baseline — was the fourth (ADR-017).
- LIT-127
- LIT-119
- LIT-167
- LIT-168
- LIT-180
- LIT-tmpdktqx
introduced_by:
- LIT-127
implementations: []
summary: >-
  Shao et al. (2024), [LIT-127](../literature.d/LIT-127.md) — Group Relative Policy Optimization: PPO with
  the value model dropped and the baseline taken from the scores of several
  outputs sampled for the same prompt, which removes a model-sized chunk of
  the RL memory footprint and is what every later reasoning recipe in this
  record actually runs.
corrected_by:
- SOTA-146
compared_against:
- SOTA-154
- SOTA-212
---

# SOTA-145: Estimate the RL baseline from a group of samples for the same prompt instead of training a critic

PPO needs a value model to tell it whether an outcome was better than
expected. At LLM scale that critic is a second network of comparable size,
trained alongside the policy, and it is the largest avoidable cost in the RL
stage.

GRPO ([LIT-127](../literature.d/LIT-127.md)) removes it. Sample a group of
outputs for the same prompt, score them, and use the group's own statistics as
the baseline: an output is good relative to its siblings rather than relative
to a learned prediction. The critic disappears and the advantage estimate
becomes a within-group comparison.

## Why this is the settled part

The record holds four papers that run or rework GRPO, and **all four keep the
group baseline**:

- [LIT-119](../literature.d/LIT-119.md) runs it on a 0.6B reasoning model and reports it sensitive above
  all to the learning rate — a tuning finding, not an objection to the method.
- [LIT-167](../literature.d/LIT-167.md) identifies a length bias in the objective and publishes Dr. GRPO
  to remove it. The group baseline stays.
- [LIT-168](../literature.d/LIT-168.md) decouples the clipping range and adds dynamic sampling. The group
  baseline stays.
- [LIT-180](../literature.d/LIT-180.md) moves the importance ratio from token to sequence level. The
  group baseline stays.

Three independent groups examined this objective closely enough to publish a
correction to it, and none of them proposed bringing the critic back. That is
what `converged` is recording here: not that nobody has looked, but that
people looked hard and changed something else.

## Outside language, and how big the group has to be

Flow-GRPO ([LIT-tmpdktqx](../literature.d/LIT-tmpdktqx.md)) runs the group baseline on an image generator.
GRPO's group-normalized advantage, clipped ratio and KL penalty are used
unchanged on SD3.5-M with LoRA, after the flow model's sampler is turned
into a same-marginal SDE so that each step is a Gaussian policy. There is
still no critic. GenEval rises from 0.63 to 0.95 and OCR accuracy from 0.59
to 0.92, on rewards it is also trained on.

It adds a condition the language papers did not state: **the group has to
be large enough for the baseline to hold.** At 24 samples per prompt
training was stable; at 12 and at 6 it collapsed on PickScore (its Fig. 5).
One run per setting, on one task.

## What this does not say

<!-- inactive-ok-block: SOTA-146 — Proposed, and naming it as Proposed is
     the whole point of the sentence -->

It does not say run GRPO as published. That is
[SOTA-146](SOTA-146.md), and it is `Proposed` for a reason: the
same three papers that kept the group baseline each found a different defect
in the rest of the objective, and no two of them fixed the same one.

It also does not say *when* to run RL. [SOTA-129](SOTA-129.md) is the
<!-- inactive-ok: SOTA-130 — Proposed, named as the variation this is orthogonal to -->
three-stage recipe and [SOTA-130](SOTA-130.md) the variation that skips the SFT
stage; both name RLVR as a stage and neither names an algorithm. This is the
algorithm, and it is orthogonal to that argument — the group baseline is what
you run either way.


And it does not say policy-gradient RL is the right *family*. Evolution
strategies ([SOTA-154](SOTA-154.md), `Proposed`) reach the same goal without
backpropagation and report a larger average improvement than either PPO or
GRPO on the one task they share — on a single fixed hyperparameter set,
against RL tuned per experiment. That is not a counterexample to the argument
above, which is about what works that *run or rework GRPO* keep; it is
evidence about whether to be in that family at all, at 8B and below and on
two tasks. The practice stands, and the assumption underneath it is now a
named rival with a promotion condition rather than an assumption.

<!-- inactive-ok-block: SOTA-212 — Proposed, named as the rival compared directly against this practice -->
The second rival ran its comparison against this practice directly. RandOpt
([SOTA-212](SOTA-212.md)) scores thousands of random weight perturbations in one parallel
pass and majority-votes the best 50, and its paper matched it on training
FLOPs against GRPO at 200 iterations across seven tasks at 0.5B–8B: it won
most cells, 85.0% against GRPO's 68.5% on Countdown with OLMo3-7B-Instruct and
87.1% against 83.2% on GSM8K with Qwen2.5-3B-Instruct. But GRPO answered with
one sample against a 50-way ensemble, and the paper says so; the comparison is
about whether to leave the family, not about whether to keep the group
baseline inside it.
