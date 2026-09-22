---
status: Proposed
promote_when: >-
  A tight lower bound on the residual with skip connections present — the open
  challenge the source itself poses. What is proved today is that SOME
  parameterization preserves the residual, because one path skips every layer;
  what everyone quotes the paper for is that skip connections prevent collapse
  in transformers people train, and the gap between those is the whole of the
  status. A measurement would also serve: the convergence condition
  `4γβ < √d_qk` evaluated on a trained checkpoint this record holds, which
  needs no training. What would NOT meet it: another architecture ablated the
  same way. The residual-norm curve for SAN, SAN+MLP, SAN+skip and the full
  transformer is the observation, and the record already holds it.
title: 'Pure self-attention collapses every token onto one, and skip connections prevent it by keeping short paths alive'
version: 1
tags:
- attention-techniques
- model-architecture
- model-stability
date: '2026-09-22'
source:
- LIT-tmpcv53l
summary: >-
  Dong, Cordonnier and Loukas (2021), [LIT-tmpcv53l](../literature.d/LIT-tmpcv53l.md) — decompose a
  self-attention network into paths, one head per layer, and the residual after
  removing the best rank-1 approximation shrinks at a **cubic** rate: doubly
  exponential in depth. Skip connections create short paths — including one
  that skips everything — and that is what stops it. MLPs slow it in
  proportion to their Lipschitz constant. **Layer normalization cannot help at
  all**, because it is a right multiplication.
---
<!-- inactive-ok-file: SOTA-010 — Superseded, named only as the code whose
     claim moved to THEORY-011 when it was retired as a practice; the sentence
     citing it is about that move, not about taking its advice. -->

<!-- inactive-ok-file: THEORY-064 — Proposed, named under "what it does not
     say" to record a tension neither source frames as one. The use requires
     it to be unsettled. -->

# THEORY-tmp91yaa: Pure self-attention collapses every token onto one, and skip connections prevent it by keeping short paths alive

## Source

Dong, Cordonnier and Loukas (2021), [LIT-tmpcv53l](../literature.d/LIT-tmpcv53l.md) — read as
[NOTE-tmpsokgi](../notes.d/NOTE-tmpsokgi.md). ICML 2021.

## The account

**The decomposition first, because everything follows from it.** A depth-`L`,
`H`-head self-attention network's output is a sum over *paths*, each path a
choice of one head per layer, each term a single-head deep network. Turn skip
connections on and a path may also choose to skip a layer, so the number of
paths of length `l` becomes `C(L,l)·H^l`. The path set fills with short paths,
and one path skips every layer.

**Pure attention collapses, fast.** Write `res(X) = X − 1xᵀ`, the part of the
representation that is not the same for every token. For a pure self-attention
network,

    ‖res(SAN(X))‖ ≤ (4γβ/√d_qk)^((3^L−1)/2) · ‖res(X)‖^(3^L)

— a **cubic** rate, doubly exponential in depth, whenever `4γβ < √d_qk`. Every
token becomes the same token. The rate is cubic rather than linear because an
attention matrix formed from a low-rank input mixes tokens faster, so each
layer's collapse accelerates the next one's: a cascade. The authors' scale:
falling three orders of magnitude takes a linear rate about a dozen steps and a
cubic rate two or three.

**Skip connections are what stands in the way.** The length-zero path carries
the input through untouched, so there are infinitely many parameterizations
with `‖res(X_L)‖ ≥ ‖res(X)‖` — holding as `L → ∞` and for `β` arbitrarily
small. Read through the decomposition, a deep transformer is closer to an
**ensemble of shallow single-head networks** than to a deep one, because the
long paths have had their residual destroyed and the short ones have not.

**MLPs slow it, and the slowing has a price the source names.** The bound gains
the MLP's Lipschitz constant λ. More powerful MLPs, slower collapse — a
tug-of-war. And larger Lipschitz constants make the model less robust and more
sensitive to input perturbations, and raise gradient variance.

**Layer normalization cannot help, and the argument is two lines.**
`LN(SA(X))` rewrites as `Σ_h P_h X W̃_h + 1b̃ᵀ` with `W̃_h = W_h D_LN^{-1}`.
Layer normalization is therefore a right multiplication plus a rank-1 shift,
and right multiplication cannot increase rank.

## Why `Proposed`

**The claim everyone quotes is the one that is not proved.** What is proved is
that pure attention collapses, and that *some* parameterization with skip
connections preserves the residual. What the paper is cited for is that skip
connections prevent rank collapse in transformers people train. The authors are
candid: the upper bound they can derive with skip connections is "vacuously
large", the lower bound they give is elementary, and **a tight lower bound is
posed as an open challenge to the community**. That challenge is the
`promote_when`.

**The convergence condition is never evaluated.** `4γβ < √d_qk` bounds
quantities — `β ≥ ‖W_QK‖₁‖W_V‖₁,∞` and a γ depending on attention entries —
that no trained model is checked against here.

**The object of the theorem is not an architecture anyone trains.** §3 exists
to say so, and the record has an instance of the title travelling further than
the theorem.

## What it does not say

**It does not say transformers suffer rank collapse.** It says the component
that would cause it is present and the components that prevent it are also
present. The measured curves on BERT, ALBERT and XLNet show the full
architecture flat and the ablations collapsing.

**It is not the same phenomenon as weight matrices going low rank during
training**, which several documents in this record also call rank collapse.
That one is about weights over training time and this is about token
representations through depth in a single forward pass; this one is prevented
by residual connections and nothing claims the other is. The conflation is the
field's rather than this record's —
[LIT-350](../literature.d/LIT-350.md) uses the term the other way in its own words — and
[NOTE-tmpsokgi](../notes.d/NOTE-tmpsokgi.md) carries the table separating them.

**It is not the only account of why skip connections matter.**
[THEORY-011](THEORY-011.md) holds that they smooth the loss landscape, which is where
[SOTA-010](../practices.d/SOTA-010.md) went when it was retired as a practice. Different
mechanism, same component, and this paper claims its effect was previously
unknown. No relation is declared between the two because neither refines the
other.

**It does not survive [LIT-521](../literature.d/LIT-521.md)'s objection unchallenged.** That
paper argues rank collapse of activations is the wrong locus for a training
crash — the cause sits in the weight matrix, and activations only carry it
forward. Both sides are in the record and nobody has adjudicated them.

**And the MLP remedy pulls against [THEORY-064](THEORY-064.md).** That account holds
transformers' robustness is made of their bias toward low-sensitivity
functions. This one says the component counteracting collapse does it by
raising a Lipschitz constant, which increases sensitivity to input
perturbations. Three years apart, no citation either way, and neither frames it
as a trade.
