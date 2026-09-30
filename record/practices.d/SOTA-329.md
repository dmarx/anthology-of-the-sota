---
number: 329
status: Proposed
formerly:
- SOTA-tmpx0l6h
promote_when: >-
  A group other than the ReFT authors runs LoReFT and LoRA under one tuning
  protocol, tuned on development sets with the same search budget for each,
  on short-output tasks, and LoReFT still matches or beats LoRA at its
  parameter count. Another table of baseline numbers copied from earlier
  papers does not count, however large the margin.
title: 'For short-output tasks, adapt a frozen model with a low-rank intervention on a few positions of the residual stream, not a weight adapter; do not use it for long chain-of-thought'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-22'
source:
- LIT-549
introduced_by:
- LIT-549
compared_against:
- SOTA-184
consensus: unreplicated
consensus_note: >-
  One group, and its comparisons are against baseline numbers reported in
  other papers, not re-run. The record holds no independent head-to-head
  in either direction. LoRA (SOTA-184) remains the universal default, and
  nothing here is a reason to change that for reasoning or long-form
  generation.
implementations:
- pyreft
summary: >-
  Wu, Arora et al. (2024), [LIT-549](../literature.d/LIT-549.md) — LoReFT sets an r-dimensional
  subspace of the hidden state at a few prompt positions to a learned
  linear function of that state, with the model frozen. At 0.03% of
  parameters against LoRA's 0.8%, it leads on commonsense QA (LLaMA-7B 80.2
  against 74.7) and is level on GLUE. It loses on arithmetic chain of
  thought (GSM8K 26.0 against 37.5). All baseline numbers are copied from
  other papers.
---

# SOTA-329: For short-output tasks, adapt a frozen model with a low-rank intervention on a few positions of the residual stream, not a weight adapter; do not use it for long chain-of-thought

## Source

Wu, Arora et al. (2024), [LIT-549](../literature.d/LIT-549.md) — ReFT. Read as [NOTE-290](../notes.d/NOTE-290.md).

## The practice

**Where the output is a label or a short answer, and trainable parameters
or per-task storage are what you are short of, train LoReFT instead of a
weight adapter.**

- **The intervention:** at chosen layers, replace the hidden state `h` at
  the first `p` and last `s` prompt positions with
  `h + Rᵀ(Wh + b − Rh)`, where `R` has `r` orthonormal rows. Only `R`, `W`
  and `b` train. DiReFT (`h + W₂ᵀ(W₁h + b)`, no orthogonality) is cheaper
  to train and slightly worse
- **Starting settings, from the authors (Appendix D.2):** intervene on
  several positions, since one is always worse. Start with all layers and
  prune. Start with a rank below 32, such as 4, because higher rank is not
  reliably better. Tie the prefix and suffix weights. The GLUE runs used
  rank 1
- **What it buys:** 0.03% of the model's parameters against LoRA's
  0.7–0.8%, per-task weights under 1MB, and an inference cost fixed by the
  number of edited positions, not the prompt length

**Do not use it where the model has to generate a long chain of thought.**
On arithmetic with chain of thought it is behind LoRA at both sizes tested,
by 11.5 points on GSM8K at 7B. The authors' explanation is that an edit made
only on prompt positions is diluted as the generation grows. If that is
right, the gap is structural and more tuning would not close it.

## What was measured

| suite | model | LoReFT | LoRA | notes |
|---|---|--:|--:|---|
| commonsense (8) | LLaMA-7B | 80.2 | 74.7 | DoRA 78.1; HellaSwag 93.1 against 78.1 |
| commonsense (8) | Llama-3 8B | 86.6 | 80.8 | DoRA 85.2 |
| arithmetic CoT (4) | LLaMA-7B | 42.6 | 46.9 | GSM8K 26.0 against 37.5 |
| arithmetic CoT (4) | LLaMA-13B | 49.6 | 51.1 | |
| AlpacaEval v1 | Llama-2 7B | 85.60 | 81.48 | GPT-4 judge; full FT 80.93 |
| GLUE (8) | RoBERTa-large | 88.2 | 88.1 | full FT 88.6 |

## Conditions

- **The baselines are not re-run.** Every LoRA, DoRA and adapter number is
  copied from Hu et al. 2023, Liu et al. 2024 or Wu et al. 2024. ReFT was
  tuned on development sets, and the authors say much PEFT work tuned on test
  sets. That would favour the baselines, but different tuning protocols make
  the table a cross-paper comparison, not a controlled one
- **One task carries much of the commonsense margin.** HellaSwag alone
  moves 15 points at 7B. Several of the other seven tasks are within a
  point or two of DoRA
- **LLaMA-family decoders to 13B, and RoBERTa**
- **More hyperparameters than LoRA:** which positions, which layers and
  whether to tie them, in addition to rank

## Known implementations

- `pyreft` (Stanford NLP)
