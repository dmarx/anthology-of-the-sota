---
number: 182
status: Active
formerly:
- SOTA-tmp5bfj6
title: 'Compute the normalization statistic without centering (RMSNorm)'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Records an outside re-run. Narang et al. (LIT-tmpnc3oh) reproduce the loss
    gain over LayerNorm in a T5 codebase, and it is added as a corroborating
    source. They measure a speedup of about 2–5%, not LIT-023's 7–64%, and
    the downstream gain does not hold once relative position biases are
    swapped for learned positions. The recommendation and consensus are
    unchanged. What changes is what the record says the speed saving is.
tags:
- model-stability
consensus: universal
date: '2026-09-08'
source:
- LIT-023
- LIT-tmpnc3oh
introduced_by:
- LIT-023
implementations:
- llama2
summary: >-
  Zhang and Sennrich (2019), [LIT-023](../literature.d/LIT-023.md) — [ARXIV-1910.07467](https://arxiv.org/abs/1910.07467). Drop the mean
  subtraction from layer normalization and rescale by the root mean square
  alone.
compared_against:
- SOTA-191
---

# SOTA-182: Compute the normalization statistic without centering (RMSNorm)

## Source

Zhang and Sennrich (2019), [LIT-023](../literature.d/LIT-023.md) — [ARXIV-1910.07467](https://arxiv.org/abs/1910.07467).

## What it drops

Layer normalization does two things to a vector: re-centers it on its mean
and re-scales it by its standard deviation. RMSNorm keeps only the second,
dividing by the root mean square and learning a gain. The paper's claim is
that the re-scaling is what buys the stability and the re-centering is
close to free to drop — the same convergence, 7–64% less time per step in
the settings it measures.

## What an outside re-run found

Narang et al. (LIT-tmpnc3oh) swapped LayerNorm for RMSNorm in a 223M T5
encoder-decoder with every other hyperparameter fixed. RMSNorm was one of the
few changes among about fifty that beat the baseline. Early loss was **2.167 ± 0.008 against 2.182 ±
0.005** over five seeds, final loss 1.821 against 1.838, and it won on all
four task families.

Two things came out smaller than the source claims:

- **The speed saving is a few percent, not tens.** They measured 3.68
  against 3.50 steps per second, about 5%. With learned positions it was 3.99
  against 3.90, about 2%. LIT-023's 7–64% was measured per model in its own
  implementations. In a TPU codebase where normalization is a small share of
  the step, expect the low end or below.
- **The downstream gain is not robust to the position scheme.** With learned
  absolute positions instead of relative biases, RMSNorm still lowers
  pre-training loss (2.209 against 2.245) but trails the baseline on SuperGLUE
  and WebQuestions.

Neither weakens the recommendation, whose claim is that centering is close
to free to drop. Both bound the reason usually given for it.

## Independent of placement

This is independent of where the normalization sits. Centering and placement are
separate choices, and this practice is about the statistic; [SOTA-032](SOTA-032.md) is
about the position. Nothing stops a Post-LN model from using RMSNorm, and
GPT-2 is Pre-LN with full LayerNorm.

## Why `universal`

In the record's modern half a
model using centered LayerNorm is the one that would need to explain
itself.

## Known implementations

- llama2, and effectively every open-weight decoder since
