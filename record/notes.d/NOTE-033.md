---
number: 33
status: Read
formerly:
- NOTE-tmpamwk9
paper: LIT-065
title: 'Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B'
version: 1
tags:
- distributed-optimization
date: '2026-09-09'
published: '2022-01-01'
summary: >-
  The 3D-parallelism report — 8-way tensor, 35-way pipeline, data parallel over 560 DGX A100 nodes — and an unusually complete training recipe, including a batch-size ramp from 32 to 1920 and β₂ lowered to 0.95 to suppress loss spikes. Also the corpus's cleanest artefact of pre-Chinchilla misallocation: 530B parameters trained on 270B tokens.
---

# NOTE-033: Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B

## Contribution

Two things, and the second is why the paper is still worth reading.

The stated contribution is **3D parallelism**: combining tensor-slicing
(Megatron, `LIT-022`), pipeline parallelism and data parallelism so each
operates in the regime where it is effective.

The unstated one is **a complete published training recipe at 530B** —
learning rate, warmup, initialisation, Adam betas, clipping, decay, and a
batch-size ramp — at a level of detail frontier reports stopped providing
almost immediately afterwards.

## Key insight

**Data parallelism runs out because batch size runs out.** The paper says it
directly: the batch size a model can be trained with has an upper bound, so at
4000 GPUs pure data parallelism "would only allow for a batch size of 1 per
GPU". That ceiling is not a systems limit — it is the *statistical* limit
`LIT-017` calls the critical batch size. The reason 3D parallelism exists is
that the gradient noise scale is finite, a connection neither paper makes.

Once data parallelism is capped, the remaining devices must be used by
splitting the model, and the split follows the interconnect: tensor-slicing is
bandwidth-hungry so it stays inside a node, pipelining is latency-tolerant so
it crosses them.

## Assumptions

- **An interconnect hierarchy**: NVLink/NVSwitch within a node, 200 Gbps HDR
  InfiniBand between, three-level fat tree with 850 switches, all-NVMe parallel
  filesystem. The parallelism split is derived from this and does not transfer
  to a flatter network.
- bfloat16 mixed precision throughout.
- A finite critical batch size — assumed, not measured here.

## Key results

- **530B parameters**: 105 layers, hidden 20480, 128 heads, sequence 2048.
  **8-way tensor × 35-way pipeline**, data-parallel over the rest, on 560 DGX
  A100 nodes (Selene), 1.4 exaFLOP/s peak 16-bit.
- **Per-GPU throughput falls as the cluster grows.** Batch size 1920 on 280 /
  350 / 420 nodes gives iteration times 60.1 / 50.2 / 44.4 s — **126 / 121 /
  113 teraFLOP/s per GPU** against a 312 peak. Reported plainly, which is rare.
- **The recipe in full:** LR 5.0e-5; **1B tokens of linear warmup**; cosine
  decay to 10% over 340B tokens; **batch size ramped 32 → 1920 in increments of
  32 over the first 12B tokens**; Adam β₁ = 0.9, **β₂ = 0.95**, ε = 1e-8;
  gradient-norm clip 1.0; weight decay 0.1; init `N(0, σ²)` with
  **σ ≈ √(1/(3H))**, `H` the hidden size.
- **Three stability findings, stated as findings:**
  - **β₂ was reduced from its standard 0.99 specifically "to reduce spikes in
    the training loss."**
  - **Higher-variance initialisation fails to converge**, corroborating prior
    work they cite.
  - Higher learning rate increases instability — and the LR was *projected*
    from a plot of learning rate against model size rather than swept.
- **Trained on 270B tokens** from a 339B-token corpus: about **0.5 tokens per
  parameter.**
- Loss trajectory: 3.15 at 1B tokens → 2.31 at the end of the batch ramp (12B)
  → 1.85 at 270B.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | No single parallelism strategy reaches this scale | strong | argued from the batch ceiling and memory, and demonstrated |
| C2 | Per-GPU efficiency degrades as the cluster grows at fixed batch | strong | three measured points |
| C3 | Lowering β₂ suppresses loss spikes | moderate | an operational finding, not ablated |
| C4 | Initialisation variance above ~√(1/3H) fails to converge at this scale | moderate | reported, corroborated by cited work |
| C5 | The batch size should be ramped | moderate | done, and it works; no control |

## Method

8-way tensor parallel within a node, 35-way pipeline across nodes, data
parallel over the remainder. Ramp the batch size over the first 12B tokens.
Warm up over 1B tokens, cosine to 10%. Project the learning rate from model
size rather than sweeping it.

## Concepts

- **The batch-size ceiling as the reason for model parallelism** — the
  connective insight, and the one the record can use.
- **Parallelism matched to interconnect tier.**
- **β₂ as a stability dial** — a lever the record does not currently name.

## Connections

Composes `LIT-022`'s tensor parallelism with ZeRO-style data parallelism and
pipelining; `LIT-102` is the later work on making the data-parallel leg
cheaper; `SOTA-017`/`SOTA-018` cover the pipeline leg's bubble.

**`LIT-017` is the missing link.** The critical batch size is why the
data-parallel leg caps out, and the 32→1920 ramp is exactly what `LIT-017`
predicts when it finds the noise scale rising as the loss falls. Two papers,
one mechanism, no citation between them.

Against `LIT-040` and Chinchilla: **0.5 tokens per parameter** versus
Chinchilla's ~20 makes this the corpus's clearest artefact of the sub-linear
data-scaling era — a 530B model trained on fewer tokens than a 7B model gets
today. `LIT-040`, read in the same batch, is where that allocation was derived.

## Recommendations

- **R1** — Choose the parallelism split from the interconnect hierarchy, not
  from preference. *Topic:* distributed optimization. *Strength:* strong.
- **R2** — Ramp the batch size rather than fixing it. *Strength:* moderate
  here, strong read with `LIT-017`, which supplies the reason.
- **R3** — Reach for β₂ before the learning rate when the loss spikes.
  *Topic:* model stability. *Strength:* moderate — one operational report.
- **R4** — Expect per-GPU throughput to fall as the cluster grows at fixed
  batch size, and report it. *Topic:* analysis and evaluation. *Strength:*
  strong.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**

Two things are worth carrying anyway. **R3** — lowering Adam's β₂ to suppress
loss spikes — is a stability lever the record names nowhere, reported here as
an operational finding at 530B. It is not ablated, which is why no practice is
filed, but the stability neighbourhood (`SOTA-035` clipping, `SOTA-052`
initialisation) has a gap where it should sit.

The **`LIT-017` connection** is the more valuable one. The record carries
pipeline and tensor parallelism as systems techniques with systems
justifications; the actual cause of the whole arrangement is a statistical
property of the gradient.

The document's takeaways — "large scale training techniques", "system
optimization strategies", "distributed training improvements", "memory
management methods" — are four ways of saying "this is a systems paper", about
a report that publishes an exact recipe.

## Limitations

- 2022, A100-era; the throughput numbers are hardware-specific.
- C3, C4 and C5 are operational reports without ablations. This is a training
  log, not a controlled study.
- Benchmark results are superseded.
- The model is a monument to an allocation the field abandoned, which makes
  the recipe more useful than the model.

## Open questions

- How far does R3 go? β₂ = 0.95 is now common at scale and this is one of the
  earliest places it is given a *reason*. What it trades against is not
  examined here or, as far as this record knows, anywhere.
- What would this model have been at 20 tokens per parameter? The report is
  the counterfactual's control condition, and nobody ran the other arm.
