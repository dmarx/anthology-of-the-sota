---
number: 203
status: Read
formerly:
- NOTE-tmpgwkkj
paper: LIT-453
title: 'Central Flows'
version: 1
date: '2026-09-20'
summary: >-
  Models the time-averaged trajectory of an oscillating optimizer as a
  differential equation that predicts the real path numerically. Reading it:
  at the edge of stability sharpness sets the step size, not the learning
  rate; and adaptive optimizers steer away from curvature so they can step
  further later, which ablating makes them slower.
---

<!-- inactive-ok-file: THEORY-024 — Proposed since the Kaon control (LIT-tmp6umwv); named as the adjacent account this reading is not, which stands either way -->
# NOTE-203: Central Flows
<!-- inactive-ok-file: SOTA-255 — Proposed, and named as one of the two explicit curvature-affecting knobs this reading says has no joint account with the implicit one -->
<!-- inactive-ok-file: SOTA-261 — Proposed, and named in the same sentence and for the same reason -->

## Contribution

Makes the edge-of-stability regime analysable by giving up on the
oscillations. Instead of modelling the jagged path an optimizer actually
takes, it models the smoothed one — and shows that a differential equation
for the time-average predicts the real long-run trajectory of generic
networks to high numerical accuracy, which is a much stronger result than a
qualitative account of the same regime. Interpreting the flow then answers
two questions that had no answer: in what precise sense an adaptive optimizer
adapts to the landscape, and why adapting is not sufficient — the optimizer
also *shapes* the landscape it is adapting to, and that shaping is where its
advantage comes from.

## Key insight

**The learning rate is not a step size; it is a curvature penalty.** At the
edge of stability the oscillations drive the effective step to the largest
stable value at the current weights, which is a function of current sharpness
— so the learning rate hyperparameter cannot be setting how far you move,
because sharpness already is. What it does instead is modulate the strength
of an implicit sharpness penalty, which steers the trajectory toward flatter
regions where the stable step is larger. A bigger learning rate speeds
training by an indirect route: not a bigger step now, a flatter region later.
That inverts the usual mental model and it explains the otherwise odd
observation that higher learning rates optimise *slower* at first and faster
over the run.

## Assumptions

- **Deterministic, full-batch training.** Everything here. The stochastic
  case is not covered and the record's practices are all stochastic.
- **Edge of stability.** The analysis is of the oscillatory regime; the
  claims about step size and the role of the learning rate are claims about
  what happens there, not at initialisation or in a stable phase.
- **Heuristic time-averaging.** The flows are derived by arguments the
  authors explicitly call heuristic and name making them rigorous as future
  work. The justification is empirical: the flows predict the trajectories.
- **Third-order Taylor expansion required.** The mechanism is invisible to
  the second-order expansions optimization theory usually uses.
- Predictions are at the abstraction level of the **loss landscape**, which
  the authors flag as the framework's own limitation: it says the learning
  rate modulates a sharpness penalty, and not how that penalty affects
  learning, or which layers are implicated.

## Key results

- **Central flows predict real trajectories** of generic networks with high
  numerical accuracy over long horizons. *Holds when:* full-batch, the
  settings tested (CNNs and transformers on standard tasks).
- **Effective step size at EOS is set by current sharpness** — driven to the
  largest stable value at the current weights — for Scalar RMSProp.
- **The hyperparameters do not set the step size.** Their only role in the
  time-averaged trajectory is to modulate the implicit sharpness penalty; the
  learning rate increases it monotonically, and the EMA parameter interpolates
  between normalised gradient descent and plain gradient descent.
- **Acceleration via regularization.** Ablating the implicit curvature
  regularization while keeping the same step-size adaptation makes the
  optimizer **navigate into sharper regions, take smaller steps, and optimise
  slower**. The ablation is the evidence — the mechanism is shown to be
  load-bearing, not merely present.
- **Higher learning rates optimise slower initially and faster in the long
  run**, which is the signature the mechanism predicts and is measured
  directly.
- **First-order oscillatory methods implicitly acquire second-order
  information**, at no additional gradient queries, giving RMSProp an implicit
  preconditioner.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The time-averaged trajectory of an oscillating optimizer is captured by a differential equation that predicts the real path | strong | numerical agreement over long horizons across several settings |
| C2 | At EOS the effective step size is set by sharpness, not by the learning rate | strong | derived from the flow and consistent with the measured trajectories |
| C3 | Adaptive optimizers implicitly regularise curvature, and this is essential to their efficacy | strong | the ablation: same adaptation, no curvature shaping, measurably slower |
| C4 | Oscillatory first-order methods implicitly pick up second-order information | moderate | follows from the flow's structure; offered as a partial explanation of a standing puzzle |
| C5 | A third-order Taylor expansion is necessary to see any of this | moderate | argued, and consistent with the prior result it builds on |

## Method

Write the optimizer's update, observe that in the EOS regime it oscillates
about a smooth path, and derive a differential equation for the time-average
by treating the oscillations through their covariance rather than their
detail. Do this for gradient descent, Scalar RMSProp and RMSProp.

Validate by integrating the flow and comparing against the real optimizer's
trajectory over long horizons — loss, sharpness and effective step size — on
several architectures and datasets.

Interpret by reading terms off the flow: which quantity sets the step, which
hyperparameter enters where, and what the implicit penalty is. Test the
interpretation by **ablating the penalty term from the flow** and integrating
the ablated flow, which isolates curvature-shaping from step-size adaptation.

## Concepts

- **Edge of stability (EOS)** — the regime in which sharpness rises to the
  stability threshold and the optimizer oscillates about its path rather than
  descending smoothly.
- **Central flow** — a differential equation modelling the time-averaged
  trajectory. Distinct from gradient flow, which takes a different path.
- **Effective step size** — the distance actually moved, as against the
  learning rate hyperparameter. The paper keeps the two words separate
  throughout, which is most of the point.
- **Acceleration via regularization** — implicitly penalising curvature so as
  to reach regions where larger steps are stable.
- **Stationary flow** — the variant used for RMSProp, where the
  preconditioner is treated as equilibrated.

## Connections

Builds directly on the edge-of-stability literature and on the result that a
third-order expansion is needed to see oscillation-triggered curvature
reduction. Extends that from gradient descent to adaptive optimizers, where
the same expansion reveals a different mechanism.

Explains experiments in two prior papers that the authors name as otherwise
unaccounted for.

Adjacent to the modular-duality account the record holds at [THEORY-024](../theory.d/THEORY-024.md):
both are addressing why the second-order story keeps almost working. That one
says orthogonalising the update is dualising it and muP and Shampoo are
partial approximations of one map; this says first-order methods already
extract second-order information by oscillating. Neither cites the other.

## Recommendations

- **R1** — Read a learning rate as a curvature penalty rather than a step
  length when training at the edge of stability. *Topic:* optimization.
  *Status:* experimental. *Strength:* moderate. *Applies when:* full-batch,
  EOS; the stochastic translation is unestablished.
- **R2** — Expect a higher learning rate to be slower early and faster late,
  and do not tune it on early loss. *Topic:* hyperparameter tuning. *Status:*
  experimental. *Strength:* moderate. *Applies when:* as above.
- **R3** — When designing an adaptive optimizer, design the curvature-shaping
  deliberately; adapting to curvature without shaping it is measurably worse.
  *Topic:* optimizer design. *Status:* experimental. *Strength:* moderate.
  *Applies when:* building an optimizer rather than choosing one.

## Bearing on the record

- **Should produce a theory** for C2, C3 and C4 together — they are one
  account with three limbs, and it explains why the record's default
  optimizer recommendation ([SOTA-001](../practices.d/SOTA-001.md)) is right for a reason nobody had
  stated.
- **Reframes every learning-rate practice the record holds** without
  contradicting any of them. [SOTA-009](../practices.d/SOTA-009.md)'s warmup-then-anneal, and the
  warmup-stable-decay line, are advice about a quantity whose prose
  description — how far the optimizer moves — is not what the quantity does at
  EOS. The practices stand; their explanations were never written.
- **No practice should be filed from R1 or R2 yet.** Both are about full-batch
  training and every recipe the record holds is stochastic. Filing them would
  assert a transfer nobody has made.
- **Third piece of the loss-curve account**, with [LIT-455](../literature.d/LIT-455.md) and
  [LIT-454](../literature.d/LIT-454.md): the plotted trajectory is a time-average of something
  that is not smooth.

## Limitations

- **Full-batch.** The gap between this and any real training run is the whole
  stochastic gradient, and the paper does not bridge it.
- Time-averaging is justified heuristically and validated empirically; the
  conditions under which it is rigorous are named as open.
- Predictions live at the level of the loss landscape and do not translate to
  architecture or data without further work the paper does not do.
- The detailed interpretive results are for RMSProp variants; Adam is treated
  as first-order in the same family but is not the main object.
- Sharpness, the quantity everything turns on, is expensive to measure in
  practice, so the account is more useful for reasoning than for monitoring.

## Open questions

- Does the picture survive stochastic gradients? That is the question
  standing between this and any practice.
- Can an optimizer be designed with the implicit preconditioner made
  explicit? The authors name it as exciting future work, and it is the direct
  test of C4.
- How does the implicit sharpness penalty interact with the explicit
  regularisation the record already recommends — weight decay at
  [SOTA-255](../practices.d/SOTA-255.md) and [SOTA-261](../practices.d/SOTA-261.md)? Two curvature-affecting knobs, no joint account.
