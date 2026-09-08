---
status: Proposed
promote_when: >-
  A pretraining report that says it set its domain proportions by fitting a
  functional form rather than by ablation or judgement, or an independent
  group fitting a mixing law and reporting the predicted-versus-actual error
  at a scale it did not fit on. What would not move it: another report saying
  its proportions came from "ablation studies on smaller models", which is
  the expensive version of this and is already what the field does.
consensus: unreplicated
consensus_note: >-
  One group, one functional form. Nobody has disputed it and nobody has
  reproduced it; the frontier reports in this record either say their
  proportions came from small-scale ablations or say nothing at all.
title: 'Set the pretraining data proportions by fitting a mixing law on small runs, not by argument'
version: 1
tags:
- data-pipeline
date: '2026-09-08'
published: '2024-03-01'
source:
- LIT-201
implementations: []
summary: >-
  Ye et al. (2024), [LIT-201](../literature.d/LIT-201.md) — model performance is quantitatively predictable
  as a function of the mixture proportions, so fitting the law on a sample of
  mixtures reads off performance on mixtures never trained. Nested with the
  existing scaling laws, small runs predict a large model. Matched the default
  mixture trained for 48% more steps.
---

# SOTA-tmpoacn9: Set the pretraining data proportions by fitting a mixing law on small runs, not by argument

## Source

Ye et al. (2024), [LIT-201](../literature.d/LIT-201.md) — [ARXIV-2403.16952](https://arxiv.org/abs/2403.16952).

Pretraining corpora are mixtures of domains, the proportions matter a great
deal, and they are set by heuristics and qualitative argument — not because
anyone prefers that, but because the alternative appeared to require training
a model per candidate mixture.

The finding is that it does not. Performance is quantitatively predictable as
a function of the proportions, in a fittable functional form. Fit it on a
sample of mixtures and you can read off performance on mixtures you never
trained.

**The nesting is what makes it affordable.** Compose the mixing law with the
existing scaling laws over training steps and model size, and small-scale
runs predict a large model on a large token budget under arbitrary mixtures.
The search stops needing runs at the target scale, which is the whole cost
argument.

## What it bought

Optimising the mixture for a 1B model over 100B RedPajama tokens reached
performance comparable to the default mixture trained for **48% more steps**.
Extended to continual training, the law predicts the critical proportion at
which catastrophic forgetting is avoided.

## The same move the record already makes elsewhere

[SOTA-142](SOTA-142.md) sets the peak learning rate by a fitted power law instead of a
sweep, and [LIT-145](../literature.d/LIT-145.md) fits scaling laws from one run's checkpoints instead of a
run per duration. This is that move applied to the data mixture — converting
a judgement call into a fitted prediction — and it is filed so the three are
legible as the same idea.

## Conditions, and why this is Proposed

One group, one functional form, no reproduction and no dispute. More to the
point: **no frontier report in this record says it used a mixing law.** They
report "domain-specific sampling rates determined by ablation studies on
smaller models" (Kimi K3) or say nothing. That is the *shape* of this method
without the functional form, so the honest reading is that the field is doing
the expensive version and has not adopted the cheap one — which is a reason
to hold the practice provisionally, not a reason to leave it unfiled.

## Known implementations

- None reported. The nearest thing in the record is small-model ablation,
  which is the search this replaces rather than an instance of it.
