---
number: 232
status: 'Proposed'
formerly:
- SOTA-tmp5nzpk
title: 'Convert an autoregressive model into a diffusion model by continual pretraining rather than training one from scratch'
version: 1
tags:
- generative-modeling
promote_when: >-
  A second group converting an open-weight AR model of 7B or above and
  reporting parity with the original on standard benchmarks, or any
  production system serving a converted model for infilling. What would not
  move it: a better diffusion LM trained from scratch, which strengthens the
  other branch; or a conversion demonstrated only below 1B, where the
  compute argument for converting rather than training is weakest.
consensus: unreplicated
consensus_note: >-
  One group, one method, models released. Nothing in this record contests it
  and nothing replicates it. The competing route — training as diffusion from
  the start — is held at [SOTA-157](SOTA-157.md) and is also `Proposed`, so the record
  currently records the choice without recommending either side of it.
date: '2026-09-17'
source:
- LIT-381
introduced_by:
- LIT-381
implementations:
- LIT-381
summary: >-
  Gong et al. (2024), [LIT-381](../literature.d/LIT-381.md) — [ARXIV-2410.17891](https://arxiv.org/abs/2410.17891). Continual pretraining on
  under 200B tokens turns an existing autoregressive model into a diffusion
  language model — GPT2 and LLaMA across 127M-7B — competitive with the AR
  original. The reason to want one is infilling without prompt re-ordering,
  not perplexity.
---

# SOTA-232: Convert an autoregressive model into a diffusion model by continual pretraining rather than training one from scratch

<!-- inactive-ok-file: SOTA-157 — Proposed, and this practice's counterpart; naming it is how the record holds the choice -->

## Source

Gong et al. (2024), [LIT-381](../literature.d/LIT-381.md) — [ARXIV-2410.17891](https://arxiv.org/abs/2410.17891).

## The claim

Diffusion language models are hard to train from scratch at scale;
autoregressive checkpoints are abundant. Continual pretraining under 200B
tokens, on a stated correspondence between the AR and diffusion objectives,
converts one into the other — demonstrated on GPT2 and LLaMA from 127M to 7B,
released as DiffuGPT and DiffuLLaMA.

The converted models beat earlier diffusion LMs and are competitive with the
AR models they came from.

## Why do it at all

Parity is not a reason. If the converted model only matched the original,
converting would be a cost with no return.

The return is **infilling without prompt re-ordering**. An AR model can be
made to fill a gap by rearranging the prompt so the suffix comes first, and
that workaround is paid at every call and constrains how the context can be
built. A diffusion model does not need it. In-context learning and
instruction following survive the conversion, so the capability is added
rather than traded for.

## The other branch

[SOTA-157](SOTA-157.md) is the same decision from the other end — train as a masked
diffusion model from the start, from [LIT-217](../literature.d/LIT-217.md). Both are `Proposed`, which
is the honest state: the record holds the choice and recommends neither side.

What separates them is when the decision is made and what it costs to change.
Training as diffusion commits the whole pretraining budget in advance;
converting is under 200B tokens spent against a checkpoint that already
exists, which makes it the cheaper way to be wrong.

## Conditions

`Proposed`, and the reason is supply rather than doubt about the measurement:
one group, one method, no production system in this record serving a
converted model. The released weights make it checkable, which is the main
thing raising it above a paper claim.

The 200B-token figure is a ceiling from these experiments, not a law, and the
largest conversion shown is 7B. Nothing here says what conversion costs at
frontier scale, and the compute argument for converting rather than training
is strongest exactly where it has not been demonstrated.
