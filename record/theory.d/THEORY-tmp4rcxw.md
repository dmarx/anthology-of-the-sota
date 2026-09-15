---
status: Proposed
promote_when: >-
  The curvature-active dimension measured rather than inferred — a Hessian or
  Gauss-Newton spectrum of an actual fine-tuning landscape, showing the stiff
  count flat across model sizes — or the accessibility result reproduced on a
  model family other than Qwen2.5 by a group with no author in common with
  LIT-211. What would not satisfy this: another demonstration that small
  populations work, which is the fact this account exists to explain.
title: 'Fine-tuning landscapes are low-dimensional in curvature, and improving directions are degenerate rather than unique'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
source:
- LIT-tmpfjaya
explains:
- SOTA-154
- SOTA-tmpdcmgg
summary: >-
  Liang et al. (2026), [LIT-tmpfjaya](../literature.d/LIT-tmpfjaya.md) — a small set of stiff directions carries
  the improvement in a fine-tuning landscape and their number does not grow
  with the model. Because improvement depends only on a perturbation's
  projection onto that subspace, many ambient perturbations share a useful
  component, so a fixed population of about thirty keeps working as dimension
  grows. The same heterogeneity gives rise-then-decay: stiff modes saturate
  while variance keeps accumulating in the flat bulk.
---

# THEORY-tmp4rcxw: Fine-tuning landscapes are low-dimensional in curvature, and improving directions are degenerate rather than unique

## Source

Liang et al. (2026), [LIT-tmpfjaya](../literature.d/LIT-tmpfjaya.md).

## What was actually shown

The claim has two halves and they are worth separating, because one is
measured and the other is argued.

**Degeneracy, and the argument for it.** Let a `k`-dimensional
curvature-active subspace govern improvement. For an isotropic perturbation,
only its projection onto that subspace matters, so the set of ambient
perturbations sharing any given useful projection is an affine subspace of
dimension `d − k`. Whether random search succeeds is then the probability mass
of the improvement-supporting set under the sampling distribution — a quantity
living in `k` dimensions, not `d`. **The ambient dimension drops out.** The
paper's contrast is needle-in-a-haystack against a degenerate "wheel of
fortune": in the first, improvement is one direction of vanishing measure and
fixed-population search must fail as `d` grows; in the second it is a
low-dimensional subspace with many ambient preimages, and extreme-value
selection over a small population succeeds.

**Accessibility, and the measurement.** The prediction is that population
requirements should not grow with model size. Best-of-`N` improvement on
GSM8K, ARC-C and WinoGrande across Qwen2.5-Instruct from 0.5B to 7B rises
quickly and flattens beyond `N ≈ 30–40`, **with no systematic rightward shift
as the model grows**. At fixed `N = 30` there is a range of small `σ` for
which headroom-normalized improvement stays positive across the whole range.

**What could have come out the other way.** This is the useful shape of
negative result: a curse of dimensionality has a direct empirical signature —
the knee of the best-of-`N` curve moving right as `d` grows — and it is absent
over an order of magnitude of scale. The paper also forecloses the obvious
artifact, showing the flattening is intrinsic diminishing returns of expected
extrema rather than exhaustion of a finite candidate pool.

**And the same geometry predicts a second, unrelated-looking thing.** In a
local quadratic model the curvature spectrum sets a relaxation rate per mode:
stiff directions converge fast, flat ones slowly and accumulate noise.
So under fixed stochasticity the reward rises while stiff modes pay out, peaks
when they are exhausted, and decays as variance keeps filling the flat bulk —
"rushing downhill before the valley floods". A two-block toy spectrum
reproduces the trajectory analytically, larger populations raise the terminal
plateau, and the same rise-then-decay appears in GRPO runs. That a geometric
claim made to explain sample efficiency also predicts a training-curve shape
in a *different optimizer* is the strongest thing here.

## What this explains, and how much

<!-- inactive-ok-block: SOTA-154 is Active; named as the practice this
     account underwrites -->
<!-- inactive-ok-block: THEORY-006 — Proposed, and named as the account this
     one gives a different answer from -->
**It is why [SOTA-154](../practices.d/SOTA-154.md) is possible at all**, and it is a different answer from
[THEORY-006](THEORY-006.md)'s. That account says pretraining leaves the neighbourhood dense
with task-improving perturbations, and the density grows with scale. This says
the set of directions that matter is small and does not grow, so a fixed
population keeps hitting it however large the model gets.

<!-- inactive-ok-block: SOTA-tmpdcmgg — Proposed, filed in this same change,
     and named as the practice this account's interventions section informs -->
**And it separates two stopping questions [SOTA-tmpdcmgg](../practices.d/SOTA-tmpdcmgg.md) had run
together.** Rise-then-decay is degradation of the *target* reward under fixed
hyperparameters, with a real peak worth stopping at. That is not the same as
the prior-task drift the forgetting literature measures, which recovers. One
argues for early stopping and the other against it, and they are about
different curves.

## What this does not say

**It does not measure the curvature it is named for.** The "bulk plus
outliers" spectrum is imported from the overparameterized-network literature
and drawn schematically; no Hessian of an actual fine-tuning landscape is
computed. Everything measured here is a downstream consequence. That is why
the promotion condition asks for the spectrum.

**It does not establish that spectral heterogeneity is what transformers
have.** The two-block toy model shows heterogeneity is *sufficient* to produce
rise-then-decay. Sufficiency is not identification, and the paper does not
claim it is.

**It is not independent of the work it explains.** Three of its seven authors
— Liang, Miikkulainen and Qiu — are authors on [LIT-211](../literature.d/LIT-211.md), the paper whose
result it accounts for. The measurements are ones anyone could repeat; nobody
outside that line has.

<!-- inactive-ok-block: THEORY-006 — Proposed, and this paragraph is the record of the disagreement between the two -->
**And it does not settle the scale disagreement with [THEORY-006](THEORY-006.md).** That
account reports the fraction of improving perturbations rising from 0% at 0.5B
to 64% at 32B at a fixed `σ`; this reports accessibility flat from 0.5B to 7B
with `σ` chosen per model. Fixed-`σ` density and best-`σ` accessibility are
different quantities and the two results are not directly comparable. The
honest position is that the record holds two measurements of related things
that point different ways about scale, and that the experiment separating them
— one `σ` protocol, both metrics, across scales — has not been run.

**Neither account is a rival to the other on the main question.** [LIT-233](../literature.d/LIT-233.md)
reads the thicket as a broad pretrained basin intersected with a
low-dimensional, degenerate set of task directions, citing this paper for the
second half. Read that way the two are one picture, and the disagreement above
is about the scale dependence of a measurement, not about the geometry.
