---
number: 8
status: 'Active'
title: 'linear warmup of LR stabilizes early training with large batch size.'
version: 3
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Source corrected (#114). Warmup is Goyal et al. (LIT-007); LIT-009
    (LARS) cites it as prior work and argues that recipe is not general
    enough and may diverge. LIT-009 stays in the list as the paper that
    found its limit. The recommendation is unchanged.
- version: 3
  date: '2026-09-10'
  note: >-
    Corrected `published:`, which is derived from the primary source and
    had gone stale: LIT-009's date survived the re-source to LIT-007.
    Found by the #119 backfill. The recommendation and the source list
    are unchanged.
tags:
- training-optimization
date: '2026-08-24'
published: '2017-06-01'
source:
# Warmup is Goyal et al. (LIT-007), which introduced it as the fix for
# divergence under linear LR scaling. LIT-009 (LARS) cites it as prior work
# and argues the recipe is "not general enough"; it stays in the list as the
# paper that found the limit.
- LIT-007
- LIT-009
summary: >-
  You et al. (2017), [LIT-009](../literature.d/LIT-009.md) — [ARXIV-1708.03888](https://arxiv.org/abs/1708.03888).
compared_against:
- SOTA-100
---

# SOTA-008: linear warmup of LR stabilizes early training with large batch size.

## Source

You et al. (2017), [LIT-009](../literature.d/LIT-009.md) — [ARXIV-1708.03888](https://arxiv.org/abs/1708.03888).


## Whose recipe this is

Warmup is **Goyal et al.** ([LIT-007](../literature.d/LIT-007.md)). Linear scaling of the learning rate
with batch size makes early optimization harder and networks "may diverge
especially during the initial phase"; their fix is to start at a small safe
rate and raise it to the target over the first steps. With that, they trained
ResNet-50 at batch 8K.

This practice cited **LARS** ([LIT-009](../literature.d/LIT-009.md)) until [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114). LARS describes warmup as
prior work — "Linear scaling of LR with a warm-up is the *state-of-the-art*
recipe for large batch training" — and then argues against its sufficiency:

> We argue that the current recipe for large batch training (linear learning
> rate scaling with warm-up) **is not general enough and training may
> diverge.**

Its own contribution is **Layer-wise Adaptive Rate Scaling**, which got
AlexNet to batch 8K and ResNet-50 to **batch 32K** without accuracy loss —
past where warmup alone held.

So the record had the practice sourced to the paper that found its limit. Both
notes are now named: `LIT-007` first, as where warmup comes from, and
`LIT-009` beside it, because a reader should know the recipe has a ceiling and
who established it.

## What warmup is for at large batch

A large batch gives a low-variance gradient estimate, which is what makes a
large learning rate usable — but only once the parameters are somewhere the
estimate means something. At initialisation the loss surface is far from any
minimum and the early steps are large in a direction chosen mostly by the
initialisation, so the same rate that is stable later diverges immediately.

Ramping the rate linearly from near zero over the first steps buys the time
for the parameters to reach a region where the large rate is survivable. It is
the compensation that makes the large-batch regime work at all, which is why
it arrived with large-batch training rather than before it.

## Three reasons warmup persists, only one of which is this

Worth separating, because the record holds them in different places and they
scale differently:

- **Initialisation gradients**, which is [SOTA-100](SOTA-100.md)'s mechanism and depended on
  post-norm; pre-norm ([SOTA-032](SOTA-032.md)) largely removed it.
- **Adam's second moment**, which is estimated from a handful of samples in the
  first steps and is unreliable until the average fills — this one is about the
  optimizer, not the architecture, and does not scale with model size.
- **Reaching a schedule's peak**, which is bookkeeping: a schedule with a peak
  needs a ramp to it, and [SOTA-009](SOTA-009.md) is that schedule.

A practice that says "warmup stabilises early training" is true and does not
say which of the three it means. All three are real; only the second still
binds for a pre-norm model trained with Adam, which is every model in this
record.
