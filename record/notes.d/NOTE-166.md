---
number: 166
status: Read
formerly:
- NOTE-tmpk5fba
paper: LIT-381
title: 'Scaling Diffusion Language Models via Adaptation from Autoregressive Models'
version: 1
date: '2026-09-17'
summary: >-
  Continual pretraining on under 200B tokens converts GPT2 and LLaMA at
  127M-7B into diffusion language models competitive with their AR
  counterparts. The argument is economic before it is technical — diffusion
  LMs are hard to train at scale and AR checkpoints are abundant — and the
  capability that pays for it is infilling without prompt re-ordering.
---

# NOTE-166: Scaling Diffusion Language Models via Adaptation from Autoregressive Models

<!-- inactive-ok-file: SOTA-157 — Proposed, the other branch of this decision; deliberate throughout -->

Read from [LIT-381](../literature.d/LIT-381.md) — [ARXIV-2410.17891](https://arxiv.org/abs/2410.17891).

## The argument, which is about supply

Diffusion language models have been studied at smaller scale than
autoregressive ones, they lack fair comparison on language modeling
benchmarks, and training them from scratch at scale is hard. Meanwhile
open-weight AR models are everywhere.

So the question is not "which paradigm is better" but "given a very large
stock of AR checkpoints, how do you get a diffusion model". The answer is
continual pretraining, under 200B tokens, exploiting a stated connection
between the AR and the diffusion objectives — which is what makes it a
conversion rather than a fresh run with a warm start.

Range: GPT2 and LLaMA, 127M through 7B, released as DiffuGPT and DiffuLLaMA.

## What it buys

Competitive with the AR counterparts on language modeling, reasoning and
commonsense, and better than earlier diffusion LMs. But parity is not the
reason to do this — if the converted model merely matched the original, the
conversion would be a cost with no return.

The return is **filling in the middle without prompt re-ordering**. An AR
model can be coaxed into infilling by rearranging the prompt so the suffix
precedes the gap, and that is a workaround with a cost at every call. A
diffusion model does not need it. That is the capability the paradigm change
is for, and it is why the practice is about *what you gain* rather than about
perplexity.

## What the record already had on the other side

[SOTA-157](../practices.d/SOTA-157.md) — train as a masked diffusion model rather than autoregressively,
from [LIT-217](../literature.d/LIT-217.md) (LLaDA). That is the same decision approached from the
opposite end, and the two belong beside each other: one says choose the
paradigm before you spend the compute, the other says you can change your
mind afterwards for under 200B tokens.

## The shape I keep meeting

This is the third time in one pass that a gap in this record turned out to be
the same shape: **build it that way from scratch, or adapt an artifact you
already have.**

- Quantization — [SOTA-185](../practices.d/SOTA-185.md) and [SOTA-163](../practices.d/SOTA-163.md) compress a finished model,
  against a ternary line that trains in the target format from the start.
- Adaptation — [SOTA-123](../practices.d/SOTA-123.md) pretrains a tiny model from scratch on the target
  distribution instead of fine-tuning one.
- Generative paradigm — [SOTA-157](../practices.d/SOTA-157.md) trains as diffusion; this converts.

No document in the record names that shape, which is exactly what [DP-007](../principles.d/DP-007.md)
predicts of a pattern everybody uses and nobody introduced. Filing it is a
candidate for `THEORY`, not for a practice, because it says what is true about
a family of decisions rather than what to do in any one of them. Left unfiled
here deliberately — noticing a pattern three times is not yet evidence, and
the right move is to record the observation and see whether a fourth arrives.
