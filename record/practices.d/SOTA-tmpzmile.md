---
status: Proposed
promote_when: >-
  The low-step crossover measured by a group unconnected to this one, at a
  scale where a latency budget would actually be set, against a masked
  diffusion baseline distilled just as hard. A further likelihood result on
  uniform-state diffusion is not it: masked diffusion is ahead there and this
  practice does not contest it.
consensus: unreplicated
consensus_note: >-
  One paper, one lab — and the same lab authored MDLM, the strongest baseline
  it is measured against. Discrete diffusion for language is an active area
  with several independent groups, but nobody outside this one has reported
  the few-step crossover, which is the claim.
title: 'When the sampling budget is small, prefer uniform-state discrete diffusion with consistency distillation — masked diffusion cannot revise what it has already emitted'
version: 1
tags:
- generative-modeling
- inference-optimization
- model-architecture
date: '2026-09-21'
source:
- LIT-tmpvrm26
introduced_by:
- LIT-tmpvrm26
implementations: []
explained_by:
- THEORY-tmprosv3
---

<!-- inactive-ok-file: SOTA-157 — Proposed, and named to say this document does
     NOT contest it: masked diffusion is ahead on likelihood in the source's own
     tables, and the claim here is about a regime that practice does not cover -->

<!-- inactive-ok-file: SOTA-254 — Proposed, and named in the same sentence and for
     the same reason as SOTA-157 -->

# SOTA-tmpzmile: When the sampling budget is small, prefer uniform-state discrete diffusion with consistency distillation — masked diffusion cannot revise what it has already emitted

## Source

Sahoo, Deschenaux, Gokaslan, Wang, Chiu and Kuleshov (2025),
[LIT-tmpvrm26](../literature.d/LIT-tmpvrm26.md) — read as [NOTE-tmp290m1](../notes.d/NOTE-tmp290m1.md). LM1B and
OpenWebText at GPT-2 scale.

## The claim, and the regime it is about

The record already recommends masked diffusion for language modelling
([SOTA-157](SOTA-157.md), [SOTA-254](SOTA-254.md)). **This does not contest that.** On
likelihood, masked diffusion is ahead in the source's own tables — MDLM wins
6 of 7 zero-shot datasets and both training corpora.

What it adds is a crossover. Below roughly **32 function evaluations**,
distilled uniform-state diffusion generates better text than distilled masked
diffusion; above it, masked diffusion wins. So the choice depends on the step
budget, and the record previously had no way to say that because it held only
one of the two families.

## Why the ordering flips

Masked diffusion unmasks many tokens independently and **cannot revise a token
once it has been emitted**. At a small step count that means committing to
choices made with little context and living with them, which shows up as
incoherence.

Uniform-state diffusion is self-correcting — a later denoising step can
overwrite an earlier one. At a large step budget that flexibility buys little
and costs likelihood; at a small one it is the whole difference.

This is a structural property of the two processes, not a tuning artefact,
which is the reason to expect the crossover to survive where a tuned number
would not.

## What it takes to get there

**Distillation is not optional.** The 8- and 16-step results are *after*
Discrete Consistency Distillation — five rounds, starting at a discretization
step of 2 and doubling. The undistilled model needs 1024 steps.

**Use the denoising model, not an EMA copy, as the distillation teacher.**
This goes against standard practice in consistency models and the source
ablates it: the non-EMA teacher gives the better distilled model.

**The Greedy-Tail sampler buys the last factor of two** — 16 steps to 8 —
with slightly better generative perplexity and lower entropy. Each distillation
round improves both quality and diversity under Greedy-Tail, which is not true
of ancestral sampling.

**And train with the Gaussian-guided curriculum** ([THEORY-tmprosv3](../theory.d/THEORY-tmprosv3.md)),
which is what makes the base model good enough to distil from. It roughly
halves training time to a given perplexity against the previous uniform-state
model.

## Conditions

**Measure generative perplexity in float64, and report entropy beside it.**
Masked diffusion models can show misleading Gen PPL with low diversity under
low-precision sampling — a known artefact the source cites and guards against
by running every sampling experiment in double precision. It also reports
entropy: MDLM distilled with SDTT matches an autoregressive model's Gen PPL at
5.4 entropy against 5.6, a diversity loss the perplexity number alone hides.
A comparison run without both of these is not evidence about this practice.

**Scale.** LM1B and OpenWebText, GPT-2-sized models. A latency budget that
makes few-step generation worth choosing is set at serving scale, and there is
no evidence there.

**One lab, which also wrote the baseline.** MDLM is from the same group. That
makes the comparison likely to be competently run and not independent.

**The crossover point is one number from one setup.** "About 32 function
evaluations" is where the curves cross in this paper's figure, against this
paper's distilled MDLM. Nothing says where it sits for a different model, a
different distillation budget, or a different sampler.

**Likelihood is not the thing being recommended.** Duo beats an autoregressive
transformer on 3 of 7 zero-shot datasets and loses the other four by wide
margins — 82.05 against 89.35 on PTB, 25.75 against 33.57 on Wikitext. That
number belongs to the paper, not to this recommendation.
