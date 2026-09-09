---
status: Read
paper: LIT-088
title: 'Scaling Vision Transformers to 22 Billion Parameters'
version: 1
tags:
- model-stability
date: '2026-09-09'
summary: >-
  Three architectural changes carry ViT from 4B to 22B — parallel attention/MLP blocks, QK normalization, and removed biases. QK-norm is the load-bearing one: training diverged around 8B from attention logits growing until the softmax was almost one-hot with near-zero entropy, and LayerNorm on the queries and keys before the dot product fixed it.
---

# NOTE-tmpoxmj0: Scaling Vision Transformers to 22 Billion Parameters

## Contribution

A scale report whose value is three named, separately motivated changes and
one clean diagnosis. The largest dense ViT before this was 4B; the paper's
claim is that "small, but critical changes to the original architecture" buy
both hardware utilisation and training stability at 22B.

- **Parallel layers.** Attention and MLP applied to the same normalised input
  and summed, rather than sequentially:
  `y = x + MLP(LN(x)) + Attention(LN(x))`.
- **QK normalization.** LayerNorm applied to queries and keys before the
  dot product.
- **Omitted biases**, on the QKV projections and in the LayerNorms.

## Key insight

The instability has a specific, named mechanism, and it is the most useful
thing in the paper. Training **diverged after a few thousand steps at around
8B parameters**, caused by

> extremely large values in attention logits, which lead to (almost one-hot)
> attention weights with near-zero entropy.

That is a complete causal story — logit growth → saturated softmax → no
gradient → divergence — and the fix follows from it directly: normalise the
queries and keys so the dot product cannot grow without bound.

    softmax[ (1/√d) · LN(XW_Q)(LN(XW_K))ᵀ ]

Figure 1 shows the 8B model diverging without it and not with it.

The second insight is about the parallel-layer change, and it is a *systems*
one: applying attention and MLP in parallel lets the QKV projections fuse with
the MLP's first linear into one matmul, and the attention out-projection fuse
with the MLP's second. PaLM reports this speeding its largest model's training
by **15% without degradation**.

## Assumptions

- Vision encoder, image and video, patch embeddings, multi-head attention
  pooling in the head. **Not decoder-only, not a language model.**
- The instability at 8B is assumed representative of what happens above it —
  reasonable, and the fix is applied to 22B without re-deriving.
- TPU-era accelerators; the utilisation numbers are hardware-specific.

## Key results

- **QK-norm prevents divergence** at 8B, demonstrated directly (Figure 1,
  Appendix B).
- **Removing biases from QKV projections and LayerNorms improved accelerator
  utilisation by 3% with no quality degradation** — following PaLM.
- **But biases are *kept* on the MLP dense layers**, explicitly departing from
  PaLM, because the authors "observed improved quality and no speed
  reduction". Bias removal is not uniform, and this is the paper's own
  counterexample to its own change.
- The LayerNorms are applied **without bias and centering**, citing Zhang &
  Sennrich — i.e. **RMSNorm**.
- **54.9% model FLOPs utilisation**, described as very efficient hardware use.
- **89.5% on ImageNet**; linear probing of ViT-22B can approach or exceed full
  fine-tuning of smaller models at high resolution — often cheaper.
- Improves the accuracy/calibration tradeoff, with and without temperature
  scaling.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Attention-logit growth to a near-one-hot softmax causes divergence at ~8B | strong | diagnosed and shown |
| C2 | QK normalization prevents it | strong | Figure 1, direct comparison |
| C3 | Parallel attention/MLP enables matmul fusion worth ~15% | moderate | the 15% is PaLM's number, cited not re-measured |
| C4 | Dropping QKV and LayerNorm biases costs nothing and buys 3% utilisation | strong | measured |
| C5 | MLP biases are worth keeping | moderate | observed, contradicting PaLM, no ablation shown |
| C6 | Linear probing a larger model can beat fine-tuning a smaller one | moderate | measured on their transfer suite |

## Method

Take ViT. Apply attention and MLP in parallel off one LayerNorm, fusing the
projection matmuls. LayerNorm the queries and keys before the dot product. Drop
biases from QKV and the norms; keep them on the MLP dense layers. Use RMSNorm.

## Concepts

- **Attention entropy collapse** — the failure mode, named with its mechanism.
  The most portable thing here and not vision-specific at all.
- **Normalising the inputs to a dot product to bound its output** — the same
  instrument `SOTA-050`'s `1/√d_k` reaches for, applied where the scale factor
  is not enough.
- **Fusion-motivated architecture** — the parallel block exists because of what
  it lets a compiler do, not because of what it represents.

## Connections

**This is the gap worth naming.** The record carries `SOTA-131` — QK-Clip,
rescale query and key weights when attention logits exceed a threshold, from
the Muon line — and its own body says QK-normalisation "is the other" route to
the same invariant, citing DeepSeek-V4 running Muon with QK-norm and no clip.
But the record has **no document that reads a paper establishing QK-norm**.
ViT-22B is one of the earliest at scale, with the mechanism diagnosed and an
isolated before/after.

`SOTA-050` is the ancestor: scale by `1/√d_k` so logits do not grow with
dimension. QK-norm is what you do when that is no longer sufficient because
the *weights* have grown, not the dimension.

<!-- inactive-ok-block: SOTA-191 — Proposed, and this paragraph is about that status specifically -->
On normalization: ViT-22B removes **bias and centering** while keeping the
gain — which is RMSNorm, `SOTA-182`, and is the **opposite half** from the one
`SOTA-191` says is expendable. It therefore corroborates `SOTA-191`'s
`contested_by` rather than the practice, and does **not** satisfy its
`promote_when`, which asks for a decoder-only language model with the *gain*
removed.

## Recommendations

- **R1** — When training diverges at scale, check attention-logit magnitude and
  softmax entropy before anything else. *Topic:* model stability. *Strength:*
  strong — a named mechanism with a cheap diagnostic.
- **R2** — Normalise queries and keys before the dot product. *Strength:*
  strong; now standard, and this is an early clean demonstration.
- **R3** — Apply attention and MLP in parallel to enable matmul fusion.
  *Topic:* systems optimization. *Strength:* moderate; the 15% is inherited
  from PaLM.
- **R4** — Do not remove biases uniformly. *Strength:* moderate, and it is the
  paper's own qualification of R4-adjacent advice everyone else states flatly.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice** — but
it identifies a real hole. `SOTA-131` (QK-Clip) is `Active` and describes
QK-norm as the alternative route to the same invariant; nothing in the record
reads a source for that alternative. This note is now that reading, and a
practice for QK-norm is a candidate for a session scoped to the registry.

<!-- inactive-ok-block: SOTA-191 — Proposed, and this paragraph is about that status specifically -->
The reading also **tightens `SOTA-191` rather than promoting it.** A 22B model
dropping LayerNorm bias and centering while keeping the gain is one more
instance of the field taking the RMSNorm half — which is exactly what
`SOTA-191`'s `consensus_note` already says, now with a second data point at
scale.

Retagged from `model-architecture` to `model-stability`: the paper's own
framing is that the changes are for "efficiency and training stability at
scale", and the stability diagnosis is what survives.

The document's takeaways — "vision model scaling", "training optimization",
"architecture adaptations", "performance analysis" — name no change, no
mechanism and no number.

## Limitations

- Vision encoder. Every result here has to cross a modality boundary to reach
  the record's usual subject, and C1's mechanism is the part that plausibly
  does.
- C3's 15% is PaLM's measurement, not this paper's.
- C5 is an observation without an ablation, and it contradicts the source it
  otherwise follows.
- Utilisation figures are TPU-specific.

## Open questions

- Where exactly does QK-norm stop being needed, and does it interact with
  `SOTA-131`'s clip? The record now has both routes to the invariant and no
  comparison.
- Why do MLP biases earn their place when QKV biases do not? Two groups
  disagree and neither shows the experiment.
