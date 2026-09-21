---
status: Read
paper: LIT-tmpzi9vi
title: 'mHC-lite: the experiment that was one measurement from settling the Birkhoff dispute'
version: 1
date: '2026-09-21'
summary: >-
  Read from the #180 worklist. It makes the doubly-stochastic constraint
  exact, which is precisely the condition under which [LIT-151](../literature.d/LIT-151.md)'s objection
  should bite hardest — and it reports no stream statistic, so the dispute
  stands. The approximation it replaces is real and measured: column sums of
  the layer-wise product off by up to **220%** at 24 layers.
---

<!-- inactive-ok-file: SOTA-136 SOTA-169 — both Proposed, and both named
     as the practices this paper lands in rather than relied on as settled.
     SOTA-136 is the branch it repairs and whose promotion condition it does
     NOT meet, which this document says in as many words; SOTA-169 is the
     trunk, named to record that its promote_when's exclusion does not apply
     here and that it stays put regardless. -->

# NOTE-tmpa0q97: mHC-lite: the experiment that was one measurement from settling the Birkhoff dispute

## Contribution

mHC constrains the residual mixing matrix to be doubly stochastic by running
20 Sinkhorn-Knopp iterations. This observes that 20 iterations do not get
there, and replaces the approximation with a construction that is exact:
by Birkhoff-von Neumann, every doubly stochastic matrix is a convex
combination of permutation matrices, so parameterize the convex weights with
a softmax and the result is doubly stochastic by construction. Native matrix
operations only — no fused CUDA kernel.

## Key results

**The approximation gap is real, and measured in training rather than
constructed.** The worked example uses a near-degenerate input
(`α = 10⁻¹³`), where 20 SK iterations leave column sums of **1.92, 0.59,
0.59**. On its own that would be an adversarial case. It is not: Figure 4
measures the distribution of the relative range `log(1/ν)` over actual SK
inputs during training and finds **≈ 27.9%** of them at `1/ν ≥ 10¹³`.

**And it accumulates with depth, which is measured too.** A single mHC
residual matrix's column sum can be off by up to **100%**; the column sums of
the layer-wise product `∏_l H^res_l` are off by up to **220%** in a
**24-layer** network.

**A methodological choice worth crediting.** Statistics are computed
per-token over 64 sequences of length 1024 from the trained model, explicitly
because "averaging across tokens can hide potential instability". That is the
same discipline `SOTA-307` argues for in a different setting.

**The empirical claim.** mHC-lite matches or exceeds mHC in performance, keeps
training throughput with a naive PyTorch implementation, and yields a smaller
mean gradient norm with reduced fluctuations than mHC (Figure 2, L model,
FineWeb-Edu). Both mHC and mHC-lite sit far below HC on gradient norm.

**The scale.** nanoGPT at three sizes — S (6 layers, ~45M), M (12 layers,
~0.12B), L (24 layers, ~0.36B) — with `n = 4` streams, on OpenWebText and
FineWeb-Edu, for **10,000 steps ≈ 1.3B tokens in total**, stated as a
computational constraint.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | 20 SK iterations leave a substantial gap to double stochasticity | **strong** | 27.9% of real SK inputs at `1/ν ≥ 10¹³`; per-matrix deviation to 100% |
| C2 | The gap accumulates through depth | strong at the depth tested | 220% on the layer-wise product at 24 layers |
| C3 | Exact construction removes the residual instability | moderate | gradient-norm dynamics, one model size, one dataset |
| C4 | mHC-lite matches or exceeds mHC | **weak as stated** | 0.36B parameters and 1.3B tokens, against a technique shipped at 1.6T |

## Limitations

**The scale is very small for a stability claim.** 1.3B tokens total and
0.36B parameters at most. The thing being repaired ships in a 1.6T-parameter
production model ([LIT-139](../literature.d/LIT-139.md)). Instability that appears or vanishes at
nanoGPT scale is weak evidence about what happens three orders of magnitude
up, and the paper is candid that compute is why.

**No seeds.** Gradient-norm trajectories are smoothed with a 200-step moving
average and the shaded band is the within-window standard deviation — which
is variation across steps, not across runs. Nothing here distinguishes "mHC
is less stable" from "this run of mHC was less stable".

**The depth argument is extrapolated past its own evidence.** 220% at 24
layers is measured; the inference to scale is "implying the risks of
instability when models further scale up", supported by noting that a recent
model builds a 1,000-layer network — with classical identity residuals, not
hyper-connections. The extrapolation is reasonable and it is not a
measurement.

**It does not measure what the dispute is about.** Searching the paper for
homogenization, diversity, distinctness or collapse returns nothing. Its
whole account of stability is gradient norms and constraint violation.

## Bearing on the record

**[SOTA-136](../practices.d/SOTA-136.md)'s promotion condition is still unmet, for the third time.**
That condition asks for "a measurement of stream homogenization with depth
under the doubly-stochastic constraint that finds it does not happen, or a
production report at depth whose streams stay distinct". [LIT-139](../literature.d/LIT-139.md) was
the production report and measured no stream statistic; [LIT-152](../literature.d/LIT-152.md) was an
independent evaluation that did not test the constraint; this is a repair of
the constraint's implementation that also measures no stream statistic. Three
documents, none of them the one experiment.

**And this one is the sharpest miss of the three, which is worth stating
precisely.** [LIT-151](../literature.d/LIT-151.md)'s objection is that the doubly-stochastic set is
bounded above but not below, so mixing can only contract and must therefore
erode what distinguishes the streams. Under mHC that argument has an escape
hatch: the projection is *approximate*, so the matrices are not actually in
the set, and whatever distinctness survives might be surviving through the
gap. mHC-lite closes the hatch — the matrices are exactly doubly stochastic
by construction. So it is the cleanest available test of the objection, and
the objection predicts it should homogenize *more*. Instead it performs as
well or better, with no stream statistic reported either way.

That is not evidence against [LIT-151](../literature.d/LIT-151.md), because the outcome it predicts
was never measured. It is a missed opportunity, and naming it is the useful
thing this record can do: the experiment that would settle a two-year dispute
is one histogram away, on a model the authors already trained, with code
already public.

**It does refine the recommendation inside the branch**, which is why
[SOTA-136](../practices.d/SOTA-136.md) goes to v3: if you adopt the doubly-stochastic constraint,
construct it rather than approximate it. That instruction is cheap, exact,
and removes a dependency on custom kernels.

**The trunk does not move.** [SOTA-169](../practices.d/SOTA-169.md) asks for a second laboratory
*shipping* a widened constrained stream in a released model, or a study
isolating width at matched parameters. This is a second laboratory and it
ships nothing, and it isolates the constraint rather than the width.

## Open questions

- **Does exact double stochasticity homogenize the streams?** One histogram
  of pairwise stream similarity by depth, on the L model, run twice — mHC
  against mHC-lite. Public code, trained models, and it settles what
  [LIT-139](../literature.d/LIT-139.md) and [LIT-152](../literature.d/LIT-152.md) left open.
- **Does the gap matter at production scale?** 220% at 24 layers is
  suggestive and 1.3B tokens is not where the instability mHC was built for
  appears.
- **Is the convex-combination parameterization as expressive?** `n = 4`
  streams means 24 permutation matrices; the softmax over them is a different
  parameterization of the same polytope, and whether optimization reaches the
  same points is not addressed.
