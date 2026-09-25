---
status: Active
title: 'Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach'
version: 1
tags:
- model-architecture
- inference-optimization
- training-optimization
date: '2026-09-25'
published: '2025-02-07'
arxiv: '2502.05171'
first_author: 'Geiping'
keywords:
- 'depth-recurrence'
- 'looped-transformer'
- 'test-time-compute'
- 'latent-reasoning'
- 'truncated-backpropagation'
- 'adaptive-computation'
implementations:
- 'Huginn-0125 (huggingface.co/tomg-group-umd/huginn-0125)'
- 'github.com/seal-rg/recurrent-pretraining'
summary: >-
  Geiping et al. (NeurIPS 2025), [ARXIV-2502.05171](https://arxiv.org/abs/2502.05171). Huginn has a 2-layer
  prelude, a 4-layer core iterated `r` times with the input re-injected every
  iteration, and a 2-layer coda: 3.5B parameters trained on 800B tokens with
  `r` sampled per step (mean 32) and backpropagation through only the last 8
  iterations. Accuracy rises with test-time iterations and saturates per
  task. **Recurrence is shown to buy accuracy per parameter, not per FLOP.**
  The only controlled baseline has the same parameters and about 1/16 of the
  compute. "Equivalent to 50B parameters" is a FLOP count, not a comparison.
---

<!-- inactive-ok-file: SOTA-tmp5r387 SOTA-403 THEORY-103 — all Proposed; the practice this
     paper sources, a practice whose consensus note it amends, and an account
     it adds one uncontrolled data point to -->

# LIT-tmpdiu35: Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach

Geiping, McLeish, Jain, Kirchenbauer, Singh, Bartoldson, Kailkhura, Bhatele and Goldstein (2025) — [ARXIV-2502.05171](https://arxiv.org/abs/2502.05171)

## Key takeaways

**The architecture.** `e = P(x)`, `s₀ ~ N(0, σ²I)`, `sᵢ = R(e, sᵢ₋₁)`,
`p = C(s_r)`. The embedding is concatenated with the state at every
iteration, and the state starts from noise. The shape is `(2, 4, 2)` layers at
width 5280: "only 8 'real' layers, but when the recurrent block is iterated,
e.g. 32 times, it unfolds to an effective depth of 2+4r+2=132 layers".

**The training recipe.** Per step, `r ~ Poisson(e^τ) + 1` with `τ` log-normal
and mean 32. Backpropagation runs through the last `k = 8` iterations only.
One `r` is used per micro-batch across workers. The learning rate is constant
after warmup and "never cooled down". The run used 4,096 MI250X GPUs for
47,000 steps, on data "heavily skewed towards code and mathematical
reasoning" with instruction data mixed in.

**Test-time iterations help, and saturate by task** (zero-shot, same weights):

| r | ARC-E | HellaSwag | MMLU | SciQ | GSM8K CoT (flex.) |
| --- | --- | --- | --- | --- | --- |
| 4 | 49.07 | 43.46 | 23.39 | 80.00 | — |
| 8 | 65.11 | 58.54 | 25.29 | 92.10 | — |
| 16 | 69.49 | 64.67 | 31.25 | 93.90 | — |
| 32 | 69.91 | 65.21 | 31.38 | 93.50 | 42.08 |

"HellaSwag only needs 8 recurrences to achieve near peak performance while
other benchmarks make use of more compute." Few-shot context moves the
saturation point on ARC-C from about 8–12 iterations at zero-shot to about 32
at 25–50 shots.

**The one controlled comparison (Table 4, 180B tokens, same data).** It
compares the same architecture with one pass through the core against the
recurrent model at `r = 32`. SciQ 73.20 against 80.60, HellaSwag 37.34
against 48.80, GSM8K 2.20 against 10.24.

**Inference features, trained for nothing.** Per-token early exit on the KL
between successive states, a KV cache shared across iterations, and
warm-starting the state from the previous token. On MT-Bench their
differences from the baseline "are not stat. significant". That is no
measured loss, not a measured gain. Self-speculative decoding is described
with no numbers.

## Traps

- **Per parameter, not per FLOP.** The fixed-depth baseline has the same
  parameters and about 1/16 of the per-token compute. No standard transformer
  is trained at matched training or inference compute. "a computation load
  equivalent to 50 billion parameters" is a cost, not a comparison. On
  Table 1 the model sits near OLMo-7B (2023) and well below OLMo-2-7B.
- **The recipe is what the third run used.** Run 1 collapsed ("The
  correlation of hidden states … quickly goes to 1.0"). Run 2 "learned early
  to ignore the incoming state". Between runs the norm, adapter, embedding
  scale and learning rate all changed. Sandwich norm, `k = 8`, the Poisson
  sampling and locked-step sampling are untested at scale, and "at small
  scale, this works as well" comes with no numbers.
- **The peak learning rate is given twice**: 5×10⁻⁴ in §4.1 and 4×10⁻⁵ in
  §4.3. Cite it with the conflict.
- **"No CoT data needed"** does not hold as usually read. Instruction data is in
  the pretraining mix, and the GSM8K figures use 8-shot chain-of-thought with
  a chat template.

## Standing in the anthology

Filed from the reading-time triage of 2026-09-25. It is the record's first
depth-recurrent or looped model; `model-architecture` held nothing on it. It
sources one `Proposed` practice, `SOTA-tmp5r387`, with a `promote_when` that
asks for the missing FLOP-matched baseline.

**A same-author data point pulls the other way.** [LIT-tmpa75eq](LIT-tmpa75eq.md)
(Cramming, 2022/23), by the same first and last authors, compared
ALBERT-style recurrence against unshared layers at *equal wall-clock*. Shared
"(4-3)" reached 81.43 MNLI against 81.68 for 12 unshared layers: no gain.
That is the matched-compute comparison this paper lacks, run on a small
encoder under a different objective, and it found recurrence buys nothing
there. The two results do not conflict. Huginn's claim is per parameter.
Together they locate the open question.

- **[SOTA-403](../practices.d/SOTA-403.md)** said "nothing at current scale shares layers
  at all". Huginn shares its whole core block, feed-forward included, at 3.5B
  and 800B tokens. That sentence is amended. The recommendation is untouched,
  because Huginn neither splits attention from feed-forward nor compares at
  equal cost.
- **[THEORY-103](../theory.d/THEORY-103.md)** holds that Dehghani et al. report
  sharing as a gain and ALBERT as a loss, with no reconciliation. Huginn is a
  gain when the shared block is iterated *more*. Compute is the likely
  reconciling variable, and it is not tested here.
