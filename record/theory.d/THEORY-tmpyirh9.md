---
status: Proposed
promote_when: >-
  The benign state confirmed by a second group, or at a scale where
  instability is expensive: a training run held in the sparse-but-not-low-rank
  attention regime, with entropy reported near zero and the run completing, at
  a billion parameters or above. Alternatively, SEC used prospectively — a
  run flagged as heading for a crash by spectral energy concentration before
  the loss moves. What would NOT meet it: another method that stabilizes
  training by bounding singular values. Every remedy in this cluster does
  that, and it is compatible with either account.
title: 'What crashes a transformer is spectral energy concentrating in the query-key product, not low attention entropy as such'
version: 1
tags:
- model-stability
- attention-techniques
date: '2026-09-22'
source:
- LIT-tmp8a9ww
explains:
- SOTA-tmpyf7w7
corrects:
- THEORY-tmp4mah6
summary: >-
  Qi et al. (2025), [LIT-tmp8a9ww](../literature.d/LIT-tmp8a9ww.md) — an attention map that is
  sparse but **not** low-rank has near-zero entropy and trains fine; one that
  is sparse **and** low-rank crashes. So entropy is the symptom. The cause
  offered is spectral energy concentration of `W_q^T W_k`, which in crashed
  runs collapses into fewer than 10 directions. `Proposed`: it is one group's
  counterexample to another group's account, at 300M and below.
---
<!-- inactive-ok-file: THEORY-tmp4mah6 — Proposed, and the account this one
     corrects. The `corrects` relation is the citation. -->

<!-- inactive-ok-file: SOTA-tmpyf7w7 — Proposed, filed in this same
     contribution and named in the `explains` table. -->

# THEORY-tmpyirh9: What crashes a transformer is spectral energy concentrating in the query-key product, not low attention entropy as such

## Source

Qi, He, Ye, Li, Zi, Dai, Zou and Xiao (2025),
[LIT-tmp8a9ww](../literature.d/LIT-tmp8a9ww.md) — read as [NOTE-tmpo1rg6](../notes.d/NOTE-tmpo1rg6.md).
Theorem 1, with the mode distinction in §3.3 and the discussion in the
appendix.

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-tmpyf7w7](../practices.d/SOTA-tmpyf7w7.md) | cap the step by `τ·σ₁(W_{t−1})/σ₁(∇W_t)` | Weyl's inequality makes that ratio the exact handle on how fast `σ₁` can grow, and it is the growth that concentrates the energy |

## The account

When attention collapses, the map goes sparse. The claim is that sparsity
alone is not the problem:

| mode | attention map | outcome |
|---|---|---|
| **benign** | sparse, not low-rank — close to an identity | trains fine |
| **malignant** | sparse and simultaneously low-rank | crashes |

Both have near-zero entropy. The paper puts the consequence bluntly: the
benign state "is a counterexample of entropy collapse … According to the
definition of entropy collapse, state B should lead to model crash; however,
our experiments show that the model remains stable in this state."

**The proposed cause is upstream of the attention map.** Theorem 1: if `X` is
low-rank and `W = W_q^T W_k` is low-rank with a few dominant singular values
— greater than `C₀√d_q` for `C₀ ≫ 1` — then the map is sparse and low-rank
with high probability. So the measurable quantity is `SEC(d_q, s)`, the share
of `W_q^T W_k`'s spectral energy held by its top `s` directions. In crashed
runs it concentrates into **fewer than 10 directions**; in healthy runs it
stays spread.

**It also rejects the other incumbent explanation.** Rank collapse of the
*activations* is argued to be the wrong locus, on the grounds that the cause
lives in the weight matrix and the activations only carry it forward.

## What it corrects, and how much of it survives

[THEORY-tmp4mah6](THEORY-tmp4mah6.md) says low attention entropy is what breaks
training, and proves a tight bound making low entropy inevitable once the
spectral norm is large. **The bound is untouched.** What is replaced is the
step from low entropy to instability: on this account there is a low-entropy
state that is harmless, so entropy cannot be the criterion.

Most of what the earlier account predicts still happens, which is what
`corrects` means here — the reasoning changes and the phenomena mostly do not.
Both accounts point at the same lever, since bounding `σ₁` growth suppresses
concentration and low entropy together. That is also why no experiment so far
distinguishes them.

## Why `Proposed`

**It is one group's counterexample and nobody has answered it.** The whole
correction rests on this group observing stable runs in the benign state. The
paper it contradicts has not replied, and no third party has looked.

**The scales are small.** 50M to 307M, on ViT, Swin and GPT-2-small. The
instability being explained is famous at 8B and above
([SOTA-192](../practices.d/SOTA-192.md) records it appearing around there), and whether the
benign state stays benign at that scale is exactly what is not known.

**Theorem 1 gives sufficiency, not necessity.** Low-rank `X` and concentrated
`W` produce a sparse low-rank map with high probability. Nothing rules out a
crash arriving by another route, so "SEC is *the* cause" is stronger than
what is proved.

**SEC is shown retrospectively.** The curves compare runs already known to
have crashed against runs already known to have succeeded. Used as a
prospective warning it would be worth more than the optimizer the paper
derives, and that use is not demonstrated.

## What it does not say

**It does not say bounding attention logits is unnecessary.**
[SOTA-192](../practices.d/SOTA-192.md) and [SOTA-131](../practices.d/SOTA-131.md) remain the remedies with the
most evidence behind them; this changes what they should be understood to
prevent, not whether to use them.

**It does not say entropy is useless as a diagnostic.** It says entropy alone
does not discriminate, and that a reader watching a live run should check
whether the map is also losing rank.

**It does not address the input factor.** Theorem 1 requires `X` low-rank as
well, and the remedy acts only on the weights. What makes `X` low-rank, and
whether it could be prevented there instead, is not examined here or in the
account this corrects.
