---
number: 202
status: Read
formerly:
- NOTE-tmpa0ky3
paper: LIT-454
title: 'The Limiting Dynamics of SGD'
version: 1
date: '2026-09-20'
summary: >-
  Long after the loss converges the weights keep travelling, distance growing
  as a power law with a non-trivial exponent. Derives SGD at finite learning
  rate and batch size as an underdamped Langevin equation and shows the
  driver is a modified loss plus probability currents, with the motion
  incoherent oscillation in the Hessian's top eigensubspace rather than
  diffusion.
---

# NOTE-202: The Limiting Dynamics of SGD
<!-- inactive-ok-file: ADR-034 — Proposed, and cited for the rule this reading leans on about what a Rejected theory does and does not retire -->
<!-- inactive-ok-file: THEORY-013 — Rejected, and named three times on purpose: the shared SDE machinery makes guilt-by-association the available mistake, and saying so is what these passages are for -->

## Contribution

Explains a phenomenon that had been observed and left as a curiosity:
networks keep moving through parameter space long after performance stops
changing, and they move anomalously — distance travelled grows as a power law
in steps with an exponent that is not the Brownian one. The account
identifies what is doing the driving, and it is not the objective anyone
wrote down. Deriving SGD at finite learning rate and batch size as a
second-order Langevin equation and pushing it through the Fokker-Planck
equation yields a *modified* loss, which implicitly regularises velocity, and
probability currents, which produce oscillation in phase space. Projected
into the Hessian's top eigensubspace the motion is incoherent oscillation
rather than random walk, and that incoherence is where the anomalous exponent
comes from.

## Key insight

**Where SGD ends up is not a stationary point of the loss you minimised.**
The stationary distribution depends on the interaction between the
gradient-noise covariance and the Hessian, and the object it is stationary
for is a modified loss. That reframes the end of training: the flat tail of a
loss curve is not the optimizer having stopped, it is the optimizer having
reached a regime where its motion no longer changes the number being plotted.
The velocity regularisation in the modified loss is the part with the most
reach — it says the limiting behaviour is shaped by how fast the weights are
moving, not only by where they are, which is invisible in any first-order
picture.

## Assumptions

- **Finite learning rate and batch size**, which is what makes the
  continuous-time model underdamped rather than the usual overdamped
  approximation. Momentum then enters as a physical parameter rather than an
  addition.
- **The gradient noise has structure**, and its covariance's relationship to
  the Hessian is what the results turn on. A white-noise assumption would
  give a different and wrong answer.
- **The analysis is of the limiting regime** — after performance has
  converged. It says nothing about the descent.
- The closed-form results are for **linear regression**, where the dynamics
  are Ornstein-Uhlenbeck; the neural-network results are empirical agreement
  with expressions derived under approximations.
- The projection argument uses the **top eigensubspace of the Hessian**,
  taken as where the interesting motion lives.

## Key results

- **Anomalous diffusion**: distance travelled grows as a power law in updates
  with a non-trivial exponent, long after convergence. *Holds when:* measured
  empirically across the settings tested.
- **A modified loss plus probability currents** drive the limiting dynamics,
  derived via Fokker-Planck. The modified loss implicitly regularises
  velocity; the currents cause phase-space oscillation.
- **The motion is not random.** In the Hessian's top eigensubspace it is
  incoherent oscillation, which is what produces the anomalous exponent
  rather than a Brownian one.
- **Linear case in closed form**: an Ornstein-Uhlenbeck process whose moments
  are a sum of damped harmonic oscillators in the eigenbasis of the data.
- **Quantitative hyperparameter predictions**: expressions for how learning
  rate, batch size and momentum influence limiting instantaneous speed and
  the anomalous diffusion exponent, reported as matching empirics exactly.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Networks continue to travel anomalously long after convergence | strong | direct measurement, and consistent with prior observations |
| C2 | The driver is a modified loss with velocity regularisation plus probability currents | moderate | derived under a continuous-time approximation; the derivation is the evidence |
| C3 | The limiting motion is incoherent oscillation in the Hessian's top subspace, not diffusion | moderate | shown by projection; an interpretation of the measured trajectory |
| C4 | Learning rate, batch size and momentum have derivable effects on limiting speed and exponent | strong | closed-form expressions reported to match empirics exactly |
| C5 | The stationary distribution reflects noise-covariance/Hessian interaction rather than the original loss | moderate | derived, and consistent with prior work reaching a similar conclusion |

## Method

Derive a continuous-time model of SGD that keeps finite learning rate and
batch size, arriving at an underdamped Langevin equation in which momentum is
a parameter of the physics. Apply the Fokker-Planck equation to get the
stationary distribution, and read off the modified loss and the probability
currents.

Solve the linear-regression case exactly as an Ornstein-Uhlenbeck process and
express its moments as damped harmonic oscillators in the data eigenbasis.

Measure distance travelled against update count for real networks past
convergence, fit the exponent, project the trajectory into the Hessian's top
eigensubspace to characterise the motion, and compare the derived
hyperparameter dependences against measurement.

## Concepts

- **Anomalous diffusion** — distance growing as a power law in steps with an
  exponent differing from Brownian motion's.
- **Modified loss** — the objective the limiting stationary distribution is
  actually stationary for, differing from the training loss and including a
  velocity regularisation.
- **Probability currents** — the non-equilibrium component of the stationary
  distribution; what makes the motion oscillatory rather than a random walk.
- **Underdamped Langevin** — the second-order continuous-time model that
  follows from keeping finite learning rate and batch size, as against the
  usual overdamped first-order one.

## Connections

Sits alongside earlier work identifying that the stationary distribution
reflects a modified objective depending on the noise-covariance/Hessian
relationship; the contribution here is explicit expressions where that work
argued existence.

The closest thing the record holds is [THEORY-013](../theory.d/THEORY-013.md) — same SDE machinery,
and `Rejected`. It claimed the noise scale `g = eps*N/B` selects minima that
generalise, and Shallue et al. ([LIT-058](../literature.d/LIT-058.md)) swept 35 workloads and found the
effect vanishes once metaparameters are retuned.

That rejection does not touch this paper. It was a claim about test accuracy;
this one makes none. The shared machinery is a reason to read them together
and not a reason to treat either as evidence about the other.

With [LIT-453](../literature.d/LIT-453.md) and [LIT-455](../literature.d/LIT-455.md) it forms the third part of a picture
about what the loss curve hides — here, that a flat tail is not a stopped
optimizer.

## Recommendations

- **R1** — Do not infer from a flat loss that training has stopped changing
  the weights. *Topic:* evaluation. *Status:* experimental. *Strength:*
  moderate. *Applies when:* reasoning about the end of a run — checkpoint
  selection, averaging windows, when to stop.
- **R2** — If limiting speed or diffusion matters to a decision, it is
  derivable from learning rate, batch size and momentum rather than needing
  measurement. *Topic:* optimization. *Status:* experimental. *Strength:*
  weak. *Applies when:* the expressions transfer, which is shown for the
  settings tested.

## Bearing on the record

- **Third leg of the loss-curve account**, with the other two papers in this
  contribution. That is where its value in this record is.
- **Should not produce a practice on its own.** R1 is real but is carried by
  the joint practice; R2 names quantities — limiting speed, diffusion
  exponent — that no decision in this record currently depends on. Filing a
  practice from it would assert a relevance nobody has established.
- **Must not be read as reviving [THEORY-013](../theory.d/THEORY-013.md).** Same SDE framing, and that
  account is `Rejected` on a generalisation claim this paper does not make.
  [ADR-034](../decisions.d/ADR-034.md) is the rule: `Rejected` on a theory means the reason is wrong, not
  that everything built with the same tools is. The note says so explicitly
  because the association is the available mistake.
- **Bears on weight averaging.** If the limiting motion is incoherent
  oscillation in the top Hessian subspace, then averaging weights over that
  window is averaging over the oscillation — which is a mechanism for why
  weight averaging works that the record does not hold, and which this paper
  does not claim. Worth flagging as a connection rather than filing as one.

## Limitations

- Published 2021 at small scale by current standards; nothing here is a
  frontier-scale measurement.
- The continuous-time model is an approximation, and everything downstream of
  it inherits that. The closed forms are for linear regression.
- The limiting regime only. Nothing about the descent, which is where the
  record's practices operate.
- "Matches empirics exactly" is the paper's phrasing for its hyperparameter
  predictions in the settings tested; it is not a claim about transfer.
- The quantities are expensive or awkward to measure — Hessian eigensubspaces,
  diffusion exponents over long tails — which is part of why the results have
  not propagated into practice.

## Open questions

- Does the modified loss survive the objection that retired [THEORY-013](../theory.d/THEORY-013.md)?
  Shallue et al. retuned metaparameters and the generalisation effect
  vanished. Nobody has asked whether the limiting speed and diffusion exponent
  survive the same retuning, and that is the experiment this paper's
  hyperparameter predictions invite.
- Does the incoherent-oscillation picture explain weight averaging? The
  connection is immediate and unmade.
- Does any of it survive to modern scales and to Adam? Both untested here.
