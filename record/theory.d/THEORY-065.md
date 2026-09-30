---
number: 65
status: Proposed
formerly:
- THEORY-tmpcz8go
promote_when: >-
  The clustering measured in a trained transformer's actual forward pass:
  token representations tracked layer by layer in a model this record holds,
  with the number of clusters and the limiting geometry reported against the
  spectrum of each head's value matrix — including the heads whose `V`
  violates the leading-eigenvalue condition, since those are the control. That
  needs no training and it is the whole gap. What would NOT meet it: an
  extension of the theorems to multi-head or feed-forward architectures, or
  further numerics on random `(Q, K, V)`. Those widen the idealization, and
  what is missing is not a wider idealization but one measurement outside it.
title: 'Self-attention drives tokens into a few clusters, and the spectrum of the value matrix decides the geometry they land in'
version: 1
tags:
- attention-techniques
- model-architecture
- analysis-and-evaluation
date: '2026-09-22'
source:
- LIT-528
summary: >-
  Geshkovski, Letrouit, Polyanskiy and Rigollet (2023), [LIT-528](../literature.d/LIT-528.md) —
  with weights held fixed, self-attention is an interacting particle system
  and its tokens cluster. Which clusters is not arbitrary: `V = I` sends them
  to the vertices of a convex polytope, a simple positive leading eigenvalue
  to at most three parallel hyperplanes, `V = −I` to a single point at the
  origin. In one dimension the attention matrix provably becomes low-rank and
  Boolean — the structure Linformer and LoRA assume and impose.
---

# THEORY-065: Self-attention drives tokens into a few clusters, and the spectrum of the value matrix decides the geometry they land in

## Source

Geshkovski, Letrouit, Polyanskiy and Rigollet (2023),
[LIT-528](../literature.d/LIT-528.md) — read as [NOTE-272](../notes.d/NOTE-272.md).
NeurIPS 2023.

## The account

Treat tokens as particles and layers as time. With `(Q, K, V)` fixed, the
transformer is the interacting particle system

    ẋᵢ = Σⱼ Pᵢⱼ(t) V xⱼ(t),   P = rowsoftmax⟨Qxᵢ, Kxⱼ⟩

and the question is where the particles end up. **They cluster**, and the
geometry of the limit is a function of one thing: the spectrum of `V`.

| `V` | limit |
|---|---|
| `I_d` | the vertices of a convex polytope — generically far fewer than `n` |
| leading eigenvalue real, positive, simple | at most **three** parallel hyperplanes, perpendicular to the leading eigenvector |
| paranormal | a polytope in the leading eigenspace, a subspace in the rest |
| `−I_d` | one cluster, at the origin |

**Why the value matrix and not the others.** The assumptions on `V` are
rigid and the assumptions on `Q, K` are not — numerically the clustering
pattern survives violating `Qᵀ K ≻ 0`, and no regime survives the leading
eigenvalue of `V` being negative or complex. `Q` and `K` warp which tokens
attract which; `V` decides what kind of object they are attracted to.

**The low-rank corollary is the part that touches practice.** At `d = 1` with
`V > 0` and `QK > 0`, the attention matrix converges doubly exponentially to a
Boolean matrix of rank 1 or 2: a handful of tokens capture the attention of
almost all the others — leaders. That the attention matrix is nearly low-rank
is the empirical premise behind Linformer's factorization and behind LoRA, and
the paper's own remark is the sharp one: in both, *the low-rank structure is
imposed rather than extracted from `P` itself*. Here it is derived.

**And it corrects a coarser picture.** Dong et al. showed pure attention
without skip connections collapses everything into one tight cluster. With the
residual connection present, the structure is not collapse but a
classification — which is why "rank collapse" as an unqualified statement is
wrong about the architecture people actually train.

## Why `Proposed`

**One group, and no forward pass of a trained model is measured.** The bridge
to practice is real but narrow: the paper checks its hypotheses on
ALBERT-xlarge-v2's learned weights and finds heads 5 and 14 satisfy them, with
`⟨Qφ₁, Kφ₁⟩` = 1.3060 and 0.6719 — while saying that not all sixteen heads do.
That is a check on the weights, not on where the tokens go.

**The genericity is quantified and it is not large.** The leading-eigenvalue
condition holds for about **14%** of real Ginibre matrices at `d = 128`, a
fraction the authors say vanishes as `d → ∞`, slowly. It is automatic when
every entry of `V` is positive, which trained matrices need not be.

**The low-rank theorem is one-dimensional, and its own remark says the obvious
extension is false.** At `d = 2` there is a two-token configuration forming a
single cluster whose attention matrix converges to the identity — rank 2. So
rank of the limit is not cluster count in general, and the authors conjecture
the result holds for almost all initial conditions rather than all.

## What it does not say

**It does not say the idealization is a defect.** Weights are time-independent
— which is ALBERT's actual architecture, not only an analytic convenience —
the dynamics are continuous, and the analysis runs on tokens rescaled by
`e^{−tV}` in place of layer normalization. All three are conditions, and the
discrete-time analogue is written out with the proofs stated to carry through.
Clustering is also reported to arrive within a few layers, so the `t → ∞`
statement is not describing a regime no network reaches. This record holds
[THEORY-009](THEORY-009.md) — a mean-field infinite-width limit — at `Active`; an
idealization is filed with its conditions, not refused.

**It does not cover multi-head or feed-forward transformers.** Both are open
problems in the source with numerics attached, and numerics attached to an
open problem is what `Proposed` is for.

**It does not say clusters are good.** The classification is descriptive.
Whether the leaders it predicts are the informative tokens is asserted by
analogy with the original attention-visualization figures and is not measured
here.

**It does not explain neural collapse**, which it names as a resemblance:
class representations forming a simplex in late layers. The record holds no
document on that either, and the two are related by appearance rather than by
any argument given.
