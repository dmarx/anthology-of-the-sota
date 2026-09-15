---
status: Read
paper: LIT-tmp4w505
title: 'Matching Accuracy, Different Geometry'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  ES and GRPO reach the same accuracy by travelling in nearly orthogonal
  directions two orders of magnitude apart in length, and land in the same
  basin with no loss barrier between them — because most of the ES
  displacement is a loss-invariant random walk whose squared norm grows as
  sigma^2 d T / N.
---

# NOTE-tmpmfvn0: Matching Accuracy, Different Geometry

## Contribution

Supplies the mechanism the ES line had been missing, and it is one mechanism
for four separate puzzles. Everyone had measured that ES moves enormously
further than GRPO; this says what the extra movement *is*, predicts how big it
should be from four quantities a practitioner controls, and shows that the
prediction's downstream consequences — orthogonality, flat curvature along the
update, and linear mode connectivity — all hold.

## Key insight

**The loss cannot see most of what ES does, and that is not a defect but a
consequence of where ES is.** Split the displacement into directions where the
loss changes and directions where it does not. On the second set nothing
constrains the walk, so it diffuses; gradient descent, by contrast, *freezes*
on flat directions because there is no gradient to follow. In a landscape with
many flat directions the diffusive part dominates, and the result is a run
that has travelled an enormous distance almost none of which is task progress.

Once that is stated, the strange facts stop being strange. The ES and GRPO
directions are nearly orthogonal because one of them is mostly noise in
dimensions the other never enters. The loss is flat along the ES displacement
because that is the definition of the dimensions it mostly occupies. And the
two solutions are linearly connected with no barrier because the off-manifold
offset between them is, by construction, loss-invariant.

## Assumptions

- **A landscape with many low-curvature directions**, which the paper takes as
  characteristic of LLM loss surfaces and which the whole argument needs.
- **Locality**: the decomposition is a local statement around the current
  parameters, exact only where flat directions are exactly flat.
- **Isotropic Gaussian perturbations** at scale `σ`, population `N`, over `T`
  steps.
- **Both arms hyperparameter-swept** — stated, with the sweeps in an appendix,
  and it is what makes the accuracy comparison worth reading.
- Single-task and sequential settings both use 200 training samples per task
  with 2,000 test samples (500 for Math), and 1,024 max generated tokens.

## Key results

- **The scaling.** Off-manifold squared displacement grows as `σ²dT/N`. The
  paper reports LLM parameters, particularly weight matrices, exhibiting
  precisely this random-walk behaviour with the theoretical scaling matching
  observation.
- **Single-task accuracy.** On Qwen3-4B-Instruct-2507, ES at 300 iterations
  gives the highest peak accuracy on all four tasks. Chemistry: ES(300) 76.5%,
  GRPO 74.9%, ES(100) 68.1%.
- **Sequential drift.** Across four sequential tasks the ES update norm grows
  **87.28 → 173.00**; GRPO's grows **1.00 → 1.84**. Ratios of 87–107×.
- **Continual competitiveness, conditioned.** ES "remains competitive
  sequentially when its iteration budget is controlled."
- **Linear mode connectivity.** Interpolating between the ES and GRPO
  solutions shows no significant loss barrier at intermediate points, across
  tasks.
- **Near-orthogonality.** The two methods' update directions are nearly
  orthogonal despite comparable task performance.
- **The random-direction probe.** Along each method's learned update
  direction, GRPO's behaves as sharply task-aligned and ES's behaves much like
  a *random* direction on held-out tasks — the measurement that converts the
  decomposition from an interpretation into a finding.
- **Propositions.** The formal statement of the contrast: on flat directions
  gradient descent freezes at initialization while ES diffuses with variance
  set by the scaling above.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | ES displacement decomposes into on- and off-manifold components, the second loss-invariant | strong | derived, and the four downstream predictions all hold |
| C2 | Off-manifold squared norm grows as `σ²dT/N` | moderate | predicted and reported to match observation; the population-size dependence is the least directly varied of the four |
| C3 | ES and GRPO update directions are nearly orthogonal | strong | measured |
| C4 | The two solutions are linearly connected with no loss barrier | strong | interpolation across four tasks |
| C5 | The ES direction resembles a random direction on held-out tasks | strong | direct probe, and the most load-bearing measurement for C1 |
| C6 | ES matches or exceeds GRPO in single-task accuracy at 4B | moderate | four tasks, one model, both arms swept |
| C7 | ES stays competitive in continual learning with a controlled iteration budget | moderate | the sequential experiment, one ordering of four tasks |
| C8 | The off-manifold walk is harmless | not claimed | loss-invariant is not capability-invariant — see [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) |

## Method

Train Qwen3-4B-Instruct-2507 with ES and with GRPO on four tasks — Countdown,
Math, SciKnowEval-Chemistry, BoolQ — in a single-task setting and then
sequentially, with hyperparameter sweeps for both. Measure update norms per
checkpoint, interpolate between the two methods' solutions to test for a loss
barrier, and probe the landscape along each method's update direction on
held-out tasks against a random-direction control. Then derive the
on/off-manifold decomposition and check its predicted scaling against the
measured weight changes.

## Concepts

- **On-manifold / off-manifold** — directions in which the loss does and does
  not change. The whole paper is the consequence of ES being unconstrained on
  the second set.
- **Linear mode connectivity** — two solutions joined by a straight path along
  which the loss does not rise.
- **Off-manifold drift** — the loss-invariant random-walk component, `σ²dT/N`
  in squared norm.

## Connections

It cites the prior suggestion that ES retains low KL divergence to the base
model and might therefore suit continual learning, and explicitly names the
catastrophic-forgetting result on smaller models (Qwen2.5-1.5B and
Llama-3.2-1B) as the other side. Its decomposition is the answer to both.
Lineage is on the LIT.

## Recommendations

<!-- inactive-ok-block: SOTA-tmpdcmgg — Proposed, filed from this reading in this same change -->
- **R1** — Control the iteration budget; drift is linear in steps and the
  paper's own continual result is conditioned on it. *Topic:* post-training.
  *Strength:* strong. Filed as [SOTA-tmpdcmgg](../practices.d/SOTA-tmpdcmgg.md).
- **R2** — Prefer a larger population to more steps at fixed accuracy: `N`
  divides drift, `T` multiplies it. *Strength:* moderate — derived from the
  scaling, not separately demonstrated.
- **R3** — Do not read a large ES update norm as evidence of a large
  functional change, and do not read a small one as safety. *Topic:*
  evaluation. *Strength:* strong, and it retires a whole class of argument in
  this line.
- **R4** — Do not read "low KL to base" as capability preservation either. The
  off-manifold walk is invisible to the training objective by construction.

## Bearing on the record

<!-- inactive-ok-block: SOTA-tmpdcmgg — Proposed, filed from this reading
     in this same change; naming it is the point -->
Filed as [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md), and it is the source of [THEORY-tmpt76ks](../theory.d/THEORY-tmpt76ks.md) and the
primary source of [SOTA-tmpdcmgg](../practices.d/SOTA-tmpdcmgg.md).

**It settles a three-way argument the record was holding without a
referee.** [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) read the drift as the cause of forgetting,
[LIT-230](../literature.d/LIT-230.md) read it as functionally sparse and harmless, [LIT-231](../literature.d/LIT-231.md) read it as
proof the search finds nothing. All three are describing a loss-invariant
random walk. Whether it hurts depends on what else you measure and for how
long, which is a question none of the three was actually asking.

<!-- inactive-ok-block: SOTA-154 is Active; named as the practice this paper
     is a fourth independent measurement of -->
**On [SOTA-154](../practices.d/SOTA-154.md)** it is a fourth independent group reporting ES at or ahead
of GRPO, at 4B, with both arms swept — and it lands above the scale where
every negative in this line sits.

## Limitations

Stated: the decomposition is local. From this reading: one model and four
tasks for a theory offered as general; the `N` dependence is the part of the
scaling least directly varied, which is why [THEORY-tmpt76ks](../theory.d/THEORY-tmpt76ks.md)'s promotion
condition asks for it specifically; and "no loss barrier" is a property of the
particular solution pairs tested.

## Open questions

- **Does raising `N` actually cut drift at fixed accuracy?** The practice this
  supports turns that knob and the paper does not.
- **How does the accounting degrade as flat directions become merely
  low-curvature?** The clean split is exact only at exactly zero curvature.
- **Is linear mode connectivity between ES and GRPO solutions general?** If
  so it is a strong statement about post-training reaching one basin
  regardless of optimizer, and worth far more than it is claimed for here.
