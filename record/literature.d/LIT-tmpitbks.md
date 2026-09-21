---
status: Active
title: 'Parallel Scaling Law for Language Models'
version: 1
tags:
- inference-optimization
- model-architecture
- training-optimization
- analysis-and-evaluation
date: '2026-09-21'
published: '2025-05-01'
arxiv: '2505.10475'
first_author: 'Chen'
keywords:
- 'scaling-law'
- 'parallel-computation'
- 'classifier-free-guidance'
- 'prefix-tuning'
- 'inference-efficiency'
implementations: []
summary: >-
  Chen et al. (2025), [ARXIV-2505.10475](https://arxiv.org/abs/2505.10475). Run the *same* weights over `P`
  learnably-prefixed copies of the input and aggregate the outputs: the loss
  falls as if the parameter count had risen by `O(log P)`. Fitted across
  0.5B–4.4B and `P = 1…8` on two corpora. At batch size 1, matching a
  parameter-scaled model costs **22× less added memory and 6× less added
  latency** — and **P× the training FLOPs**, which is the real price.
---

<!-- inactive-ok-file: SOTA-257 — Proposed, named in a list of the things this
     record already holds that spend parallel computation, precisely to say
     how this paper differs from each; a contrast does not rest on the
     contrasted document being settled -->

# LIT-tmpitbks: Parallel Scaling Law for Language Models

Chen et al. (2025) — [ARXIV-2505.10475](https://arxiv.org/abs/2505.10475)

## Key takeaways

- **The question it asks is a good one.** Classifier-free guidance runs two
  forward passes, one on a deliberately degraded input, and beats one pass.
  The degraded stream carries *less* information than the clean one, so why
  can a single pass not learn what two passes do? The paper's answer is that
  the second pass is not supplying information, it is supplying
  **computation** — and then generalizes: replace the hand-designed "bad"
  input with `P` learnable ones and the fixed contrastive rule with a learned
  aggregator.
- **The mechanism is deliberately boring.** `P` learned prefixes (prefix
  tuning, equivalently `P` distinct KV-caches) and a small MLP producing
  dynamic aggregation weights. About **0.2% extra parameters per stream**, no
  change to the backbone, no change to the data or the objective.
- **And the paper says the mechanism barely matters.** Pivot experiments over
  alternative input transformations (including LoRA-style factorizations) and
  aggregation rules "minimally affect model performance; the significant
  factor is the number of computations". This is the claim that makes it a
  statement about computation rather than about a trick.
- **`P` streams ≈ `O(log P)` more parameters.** Fitted from 0.5B–4.4B
  non-embedding parameters at `P = 1…8` on 42B tokens, on Stack-V2-Python and
  the Pile separately, with a high reported goodness of fit. The fitted
  coefficient is **0.39 on Stack-V2** and **0.33 on the Pile** — code and
  reasoning benefit more than general text.
- **Confirmed downstream, and asymmetrically.** A 1.6B model at `P = 8`
  matches the **4.4B** baseline on coding (39.1 vs 39.2) but only the **2.8B**
  baseline on general tasks (55.7 vs 55.2). The gap between those two is the
  paper's most interesting result.
- **Cost measured in memory and latency rather than FLOPs**, on the argument
  that decoding is memory-bound and FLOPs mis-ranks it — flash attention
  spends more FLOPs for less latency. At batch size 1, a 1.6B model scaled to
  `P = 8` uses **22× less added memory and 6× less added latency** than the
  parameter scaling that matches it. The advantage survives to batch size 8
  and is explicitly framed as an **edge-deployment** result.
- **Training costs roughly `P`× the FLOPs**, which the paper addresses rather
  than hides: 1T tokens of ordinary pretraining, then **20B tokens (2%)** with
  the streams switched on. The loss spikes when the random prefixes appear and
  recovers within **0.0002T tokens**.
- **It retrofits.** Continual pretraining of Qwen-2.5-3B works; so does
  freezing the backbone entirely and training only the prefixes and
  aggregator, which makes `P` a **deployment-time dial** on one set of
  weights.
- 67 checkpoints and the code released.

## Standing in the anthology

The record holds several things that spend extra computation at inference —
[SOTA-280](../practices.d/SOTA-280.md) samples several reasoning paths and votes,
[SOTA-227](../practices.d/SOTA-227.md) drafts and verifies, [SOTA-257](../practices.d/SOTA-257.md) ensembles
independently seeded models and distils them. This is a different animal from
all three: the streams **share every backbone weight**, the transformation and
the aggregation are **learned**, and — the part none of the others has — the
parallelism is present **during training**, which is why the paper can fit a
scaling law to it rather than a benchmark curve.

The comparison with beam search in the appendix is the authors' own argument
for that distinction, and the related-work section is unusually candid about
the lineage: Monte Carlo dropout, BatchEnsemble and LoRA ensembles all share
parameters across components, and what is new here is asking what `P` does to
*model capacity* rather than to variance.
