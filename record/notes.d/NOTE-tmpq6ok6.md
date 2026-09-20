---
status: Read
paper: LIT-tmpdoa3b
title: 'Hidden Breakthroughs in Language Model Training'
version: 1
date: '2026-09-20'
summary: >-
  A smooth loss curve is what many differently-timed abrupt transitions look
  like when averaged. POLCA decomposes loss change per example and along a
  curvature-derived low-rank basis; on synthetic arithmetic it recovers the
  carrying skill, which clustering the exact loss curves does not.
---

# NOTE-tmpq6ok6: Hidden Breakthroughs in Language Model Training

## Contribution

Turns "the loss curve is mostly smooth" from an observation about training
into an observation about the metric. The argument is that conceptual
breakthroughs are frequent rather than rare, and the aggregate loss conceals
them by construction — the more transitions there are, differently timed, the
smoother their sum. The paper supplies a decomposition that undoes both
collapses the scalar performs, per example and per direction, and validates
it with a negative control: a concept its method recovers and clustering on
the raw loss curves does not.

## Key insight

**Smoothness is evidence about the averaging, not about the training.** The
figure that carries the paper is a sum of sigmoids: each basis direction has
a sharp inflection, at a different time, and the sum is smooth. Under that
reading, the field's practice of studying the few visible discontinuities as
special is backwards — those are the transitions that happened to be
synchronised enough to survive averaging, and the interesting population is
the one that did not. The corollary for anyone watching a run: a flat stretch
and a smooth descent are the same kind of non-evidence, and neither licenses
the conclusion that nothing structural is happening.

## Assumptions

- **A low-rank training subspace exists** and captures most of the movement.
  The basis construction depends on it.
- **Synchronised loss change implies a shared skill.** The clustering step
  assumes examples whose losses move together at the same time depend on the
  same breakthrough. Plausible and not verified independently of the
  clustering.
- **One skill corresponds to one basis direction.** Stated as an assumption
  for the attribution argument.
- **Small scale by design.** 9M-parameter, 3-layer transformer, chosen to
  make per-example POLCA at fine intervals feasible. 1250 validation points,
  POLCA every 20 iterations, 50 basis vectors.
- Top Hessian eigenvectors reflect local oscillation rather than long-term
  movement, so directions not lowering loss over the run are discarded — an
  assumption inherited from the EOS literature and consistent with
  [LIT-tmp20sa6](../literature.d/LIT-tmp20sa6.md).

## Key results

- **POLCA recovers a concept the aggregate cannot.** On synthetic arithmetic,
  clustering exact loss trajectories recovers digit positions; clustering
  POLCA curves recovers digit positions **and** carrying. Maximum carry
  fraction under exact-loss clustering is 0.514 — chance.
- **Two decompositions are necessary, not one.** Per-example disaggregation
  alone fails when an example depends on several breakthroughs or when
  distinct concepts arrive together and merge; the directional decomposition
  separates those.
- **The basis is built from curvature**: iteratively project the loss Hessian
  onto the nullspace of the basis so far and append top eigenvectors, via
  Hessian-vector products rather than forming the Hessian.
- **POLCA modifies Loss Change Allocation twice**: an arbitrary orthonormal
  basis rather than axis-aligned units, and per-example rather than
  dataset-level attribution.
- Results extend from the synthetic task to natural language, where the
  clusters are reported as interpretable.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Conceptual breakthroughs occur frequently and are hidden by the aggregate loss | moderate | the sum-of-sigmoids argument plus recovery of hidden transitions in two settings; "frequently" is not quantified |
| C2 | POLCA recovers concepts that loss-curve clustering does not | strong | the arithmetic negative control, with the baseline at chance |
| C3 | Per-example and per-direction decomposition are both needed | moderate | argued from the polygenic case and demonstrated on the synthetic task |
| C4 | The recovered clusters correspond to interpretable capabilities | moderate | clear on synthetic arithmetic where ground truth exists; interpretive on natural language |

## Method

Construct a low-rank basis of the training subspace: at each checkpoint,
project the loss Hessian onto the nullspace of the basis built so far, take
the top eigenvectors by Hessian-vector products, and append. Discard
directions that do not lower loss over the run, on the grounds that the very
top eigenvectors track oscillation rather than progress.

Compute POLCA — loss change attributed to movement, projected onto each basis
vector, per individual example rather than over the dataset. Sum over time to
get a projected loss trajectory per example per direction.

Cluster those trajectories (HDBSCAN) to find groups of examples whose losses
move together along the same direction at the same time, and compare against
clustering the exact per-example loss curves.

## Concepts

- **POLCA** — Projection Oriented Loss Change Allocation: loss change
  attributed to movement along an arbitrary basis vector, per example.
- **Hidden breakthrough** — an abrupt transition in a subset of data or a
  single direction, invisible in the aggregate because other transitions are
  differently timed.
- **Polygenic scaling effects** — examples that require several skills and so
  show transitions at several scales. Named from prior work; the directional
  decomposition exists to handle them.
- **Projected loss** — cumulative POLCA along one basis vector for one
  example; the object that gets clustered.

## Connections

Extends Loss Change Allocation, generalising its basis and its granularity.

Sits in the phase-transition literature — induction heads, grammar
acquisition, hierarchical generalisation — and reframes it: those are the
transitions visible in the aggregate, and the claim here is that they are a
biased sample of a larger population.

Supports Nanda et al.'s speculation that "phase transitions are everywhere",
and gives it a measurement rather than leaving it as a reading of anecdotes.

Complements [LIT-tmp20sa6](../literature.d/LIT-tmp20sa6.md) from the other end: that paper says the
trajectory you plot is a time-average of oscillation, this says the scalar you
plot is an average over data and directions. Both are about what the curve
threw away.

## Recommendations

- **R1** — Do not read a smooth loss curve as evidence that training is
  proceeding smoothly; it is consistent with many abrupt transitions.
  *Topic:* evaluation. *Status:* experimental. *Strength:* moderate.
  *Applies when:* always, as a caution; the decomposition is the expensive
  part, the caution is free.
- **R2** — When you need to know what a run is doing, decompose the loss per
  example and along directions, not just per example. *Topic:* measurement.
  *Status:* experimental. *Strength:* moderate. *Applies when:* checkpoints
  and Hessian-vector products are affordable, which at small scale they are.
- **R3** — Do not treat visible discontinuities as the population of
  breakthroughs; they are the synchronised ones. *Topic:* interpretability.
  *Status:* experimental. *Strength:* moderate. *Applies when:* studying
  learning dynamics from loss curves.

## Bearing on the record

- **Should produce a practice** for R1 and R3 together. The record has
  nothing that says how to find out what a training run is doing, and "watch
  the loss" is the default this contradicts.
- **Generalises [THEORY-028](../theory.d/THEORY-028.md)**, filed two days ago, which says one specific
  plateau is a circuit being built. That was one transition made visible by
  an intervention; this says the population is large and supplies a way to
  see it without one.
- **With [LIT-tmp20sa6](../literature.d/LIT-tmp20sa6.md) and [LIT-tmp82k5k](../literature.d/LIT-tmp82k5k.md) it completes a three-part
  account** of how the aggregate loss curve is lossy — time-averaged
  oscillation, summed transitions, and motion after apparent convergence.
  That synthesis is worth a theory document because no single paper states
  it.
- **Does not bear on any training recommendation.** Nothing here says to
  train differently; it says to measure differently, which is why the
  practice belongs under `analysis-and-evaluation`.

## Limitations

- 9M parameters. The paper is explicit that the size was chosen for
  feasibility, and POLCA's cost is why.
- "Breakthroughs occur frequently" is the headline and is the least
  quantified claim — how many, at what scale, in a real pretraining run, is
  not measured.
- The clustering assumption (synchronised loss change implies shared skill)
  is validated where ground truth exists and is interpretive elsewhere.
- The one-skill-one-direction assumption is a strong idealisation of a
  high-dimensional trajectory.
- Cost: checkpoints, Hessian-vector products at each, per-example forward
  passes at every interval. Nothing here suggests it scales to a frontier run
  as instrumentation.

## Open questions

- How many hidden transitions are there in a real pretraining run? The method
  is what would answer it and the cost is what prevents it.
- Do the directions POLCA finds correspond to anything mechanistic —
  circuits, as in [THEORY-028](../theory.d/THEORY-028.md) — or only to statistical clusters?
- Could a cheaper proxy find the same transitions? Per-example loss variance
  across a batch costs nothing and was not tried.
