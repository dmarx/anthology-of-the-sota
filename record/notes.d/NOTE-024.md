---
number: 24
status: Read
formerly:
- NOTE-tmpqa1ya
# inactive-ok: LIT-104 — Proposed — a watch-list paper, and this document is the reading that says what would take it off the list
paper: LIT-104
title: 'ReLoRA: High-Rank Training Through Low-Rank Updates'
version: 1
tags:
- training-optimization
date: '2026-09-09'
published: '2023-07-01'
summary: >-
  Restart LoRA repeatedly during pretraining — merge the adapter, reinitialise it, prune the optimizer state, re-warm the learning rate — so a sequence of low-rank updates sums to a high-rank one. The ablation is the finding: the full-rank warm start it also requires accounts for most of the measured gain, and the restart machinery adds 0.42 perplexity on top of it.
---

# NOTE-024: ReLoRA: High-Rank Training Through Low-Rank Updates

## Contribution

Applies parameter-efficient *fine-tuning* machinery to *pretraining*. The
observation is arithmetic: `rank(A+B) ≤ rank(A)+rank(B)`, and the inequality
is usually strict, so a sum of rank-`r` updates can have rank far above `r`.
LoRA as normally implemented cannot exploit this because the adapter is
merged once at the end. ReLoRA merges and reinitialises it repeatedly during
training, so

    ΔW = s·W_A¹W_B¹ + s·W_A²W_B² + … + s·W_A^N W_B^N

accumulates rank across restarts. Demonstrated on transformer language
models to 1.3B on C4.

## Key insight

The restart is not free, and most of the paper is about what breaks. Adam's
moments are the obstacle: with `β₁, β₂` at 0.9–0.999, the moments accumulated
for `W_A¹` steer the freshly reinitialised `W_A²` back into the same
subspace, which is exactly the thing the restart was supposed to escape. So a
restart needs three things at once — merge-and-reinit, a **partial optimizer
reset** (99% of the state pruned by magnitude), and a **jagged schedule** that
drops the learning rate to zero and re-warms over 50–100 steps. Drop the
schedule and the run **diverges**.

The second insight is the one the paper frames as intuition and the results
support: training is **locally** low-rank. Over a long trajectory the update
is high-rank (their Figure 4), but over a short window it is well
approximated by a low-rank one — which is precisely the window a restart
covers.

## Assumptions

- **Training is locally low-rank.** Stated as a speculation, motivated by
  Aghajanyan, Arora and the lottery-ticket line, and supported by their own
  singular-value analysis rather than proved.
- **A full-rank warm start is available.** From random initialisation ReLoRA
  needs one; their best 1.3B run warm-starts at 10K of 30K steps — **a third
  of the run is ordinary full-rank training.**
- Single epoch on at least compute-optimal data (Chinchilla), LLaMA-style
  architecture, bf16, models 60M–1.3B.

## Key results

- **1.3B, 23.1B tokens:** full-rank 16.83 ppl, ReLoRA **17.27**, LoRA+warm
  start 18.23, Control (a full-rank model with the same *trainable*
  parameter count) 21.73.
- **5.5 GB per-GPU RAM saved** at equal microbatch (27.8 → 22.3 GB), and a
  **9% wall-clock** improvement at 1.3B on 8×A100 (86 h vs 93.5 h) once the
  warm start is counted. The abstract's "9–40%" is the range across model
  sizes and hardware, not the 1.3B figure.
- Singular-value spectra confirm the mechanism: ReLoRA's update has far fewer
  near-zero singular values than LoRA's, resembling full-rank training.
- **Rank barely matters:** r=128 (19.16 ppl) vs r=512 (19.00) at hidden size
  2048.
- **Negative result, reported:** "Online ReLoRA" — merging every ~100 steps
  while resetting the optimizer every 2–5K — is *worse* at both 250M and
  1.3B. More restarts is not better.

- **Table 6, the ablation (130M), is the paper's most important table:**

  | restarts | opt. reset | jagged | warm start | ppl |
  |:--:|:--:|:--:|:--:|--:|
  | – | – | – | – | 34.17 |
  | ✓ | – | – | – | 34.25 |
  | ✓ | ✓ | – | – | **diverged** |
  | ✓ | – | ✓ | – | 34.29 |
  | ✓ | ✓ | ✓ | – | 29.77 |
  | – | – | – | ✓ | **25.46** |
  | ✓ | ✓ | ✓ | ✓ | **25.04** |
  | *regular training* | | | | 23.65 |

  The warm start alone gets 25.46. All of ReLoRA's machinery on top of it
  adds **0.42**. The same machinery *without* a warm start gets 29.77 — worse
  than the warm start on its own.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A sequence of low-rank updates accumulates into a high-rank one | strong | the arithmetic, plus the singular-value spectra |
| C2 | Restarts require an optimizer reset *and* a jagged schedule or they fail | strong | ablated; the pair without the schedule diverges |
| C3 | ReLoRA approaches full-rank quality at 1.3B | moderate | 17.27 vs 16.83 — close, and still a gap that does not visibly close |
| C4 | ReLoRA's own mechanism is what delivers the result | **weak — contradicted by Table 6** | the warm start carries 25.46 of the 25.04 |
| C5 | Efficiency improves with model size | moderate | asserted from 60M–1.3B; 9% wall-clock at the top end |
| C6 | Training is locally low-rank | moderate | explicitly a speculation, with supporting spectra |

## Method

Train full-rank for a warm start (5K–10K steps). Replace attention and FFN
linears with LoRA at r=128, freezing the base weights; keep embeddings and
norms full-rank. Every `q` steps merge `W ← W + s·W_A W_B`, reinitialise
`W_A` (Kaiming) and `W_B` (zeros), prune 99% of the Adam state by magnitude,
drop the LR to zero and re-warm over 50–100 steps.

## Concepts

- **Locally low-rank training** — the load-bearing idea, and the one that
  outlives the method.
- **Restart as a rank operation** — treating merge-and-reinit as a way to
  *buy rank*, rather than as a checkpointing detail.
- **Trainable-parameter-matched control** — their Control baseline is a
  full-rank model with as many trainable parameters as ReLoRA has, which is
  the comparison that makes the result meaningful. Worth stealing.

## Connections

Downstream of LoRA and the lottery-ticket literature; a sibling of the
optimizer-memory line the record carries elsewhere. Its methodological
neighbour is `LIT-156`, which argues that challengers to a well-tuned
baseline routinely look better than they are — Table 6 here is a case where
the paper's own ablation makes that argument for it.

## Recommendations

- **R1** — If restarting an adapter mid-training, reset the optimizer state
  *and* re-warm the learning rate; either alone fails, and the pair without
  the re-warm diverges. *Topic:* training optimization. *Strength:* strong.
  The most reliable thing in the paper.
- **R2** — Match a parameter-efficient method against a full-rank model with
  the same *trainable* parameter count, not only against the full model.
  *Topic:* analysis and evaluation. *Strength:* strong.
- **R3** — Consider ReLoRA for memory-constrained pretraining. *Strength:*
  **weak.** Table 6 says most of the benefit is the warm start, and the
  wall-clock gain at 1.3B is 9%.

## Bearing on the record

**No practice is sourced to this paper, and this reading does not create one**
— R3 is too weak to file and R1 is too narrow to matter outside this method.

<!-- inactive-ok-block: LIT-104 — Proposed, and this paragraph is about that document's own defects -->
The reading does correct `LIT-104`, whose takeaways were wrong about what the
paper is:

| takeaway | verdict |
|---|---|
| "Rank-based layer stacking" | **not the method.** There is no stacking of layers anywhere. ReLoRA restarts an adapter on a fixed architecture |
| "Training optimization" | fair |
| "Memory efficiency" | fair — 5.5 GB/GPU |
| "Architecture design" | **wrong category.** This is a training procedure; the architecture is stock LLaMA-style and unchanged |

The document was also tagged `model-architecture` on the strength of those
bullets. Retagged `training-optimization`, which is what it is.

## Limitations

- 1.3B is the ceiling, and the gap to full-rank training (0.44 ppl) does not
  visibly close with scale.
- The headline result depends on a warm start that is a third of the run, so
  "parameter-efficient pretraining" is doing a third of its pretraining the
  ordinary way.
- The 9–40% speedup range in the abstract is much wider than the 9% measured
  at the largest scale.
- GLUE numbers are, as the authors say, far from state of the art because
  the models saw ~20× less data than BERT or T5 — so the downstream evidence
  is weak in both directions.

## Open questions

- Is there any regime where the restart machinery, and not the warm start,
  is what pays? Table 6 asks this question and the paper does not answer it.
- Why does *more* restarting hurt? The Online ReLoRA negative result cuts
  against the rank argument that motivates the method, and is reported
  without an explanation.
