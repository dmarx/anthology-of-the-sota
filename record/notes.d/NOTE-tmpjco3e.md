---
status: Read
paper: LIT-tmpdkrfi
title: 'SiT: Scalable Interpolant Transformers'
version: 1
date: '2026-09-20'
summary: >-
  Walks one variable at a time from DiT to SiT with the architecture,
  parameter count and GFLOPs held fixed: discrete to continuous time,
  score to velocity prediction, variance-preserving to linear interpolant,
  ODE to a tuned SDE sampler. Velocity and the linear interpolant carry most
  of the gain, and the sampler's diffusion coefficient turns out to be
  choosable after training.
---

# NOTE-tmpjco3e: SiT: Scalable Interpolant Transformers

## Contribution

Separates four decisions that the diffusion literature had bundled into
"which model" and measures each on its own. The interpolant framework lets
the path connecting data and noise be specified independently of the
objective, the time discretization and the sampler; holding DiT's backbone,
parameter count and GFLOPs exactly fixed, the paper varies each in turn and
reports what it buys. The result is both a ranked attribution — velocity
prediction and a straight-line interpolant carry most of the improvement —
and a structural observation that the stochastic sampler's diffusion
coefficient was never downstream of training and can be tuned for free.

## Key insight

**The forward process and the sampler were tied together by convention, not
by necessity.** In score-based diffusion the diffusion coefficient used at
sampling time is inherited from the forward SDE that generated the training
distribution, and the literature presents this as intrinsic. It is not: the
coefficient affects neither the velocity field nor the score, only how the
reverse SDE is integrated. So it is a sampler hyperparameter, choosable after
the model is trained, and tuning it tightens the KL divergence between model
and target without touching a weight. More generally, the paper's method —
change one ingredient, keep the FLOPs identical — is what turns a family of
"models" into a design space with attributable parts.

## Assumptions

- **Class-conditional ImageNet at 256×256 and 512×512.** Everything measured
  is here; no text conditioning, no other data.
- **DiT's architecture held exactly fixed** — same structure, same parameter
  count, same GFLOPs, same hyperparameters. That is what licenses the
  attribution and also bounds it: these are statements about transport
  choices at a fixed backbone.
- The transition study fixes training at 400K steps on SiT-B, and limits
  sampler function evaluations to match DiT's sampling budget. Heun for the
  ODE, Euler-Maruyama for the SDE.
- **Only one of score and velocity is estimated**; the other is expressed
  from it through an identity that holds for the interpolants considered.
- Endpoint distributions of equal variance, for the GVP interpolant's
  constant-variance property.

## Key results

- **Continuous time over discrete**: marginal gain. Its value is structural —
  it decouples the sampling discretization from the training discretization,
  which is what makes free choice of the diffusion coefficient usable.
- **Velocity prediction over score prediction**: significant gain, with a
  weighted score model intermediate.
- **Linear or GVP interpolant over variance-preserving**: significant gain.
  *Mechanism offered:* transport cost — the path length falls — and the VP
  interpolant's singularity at one endpoint disappears.
- **Tuned diffusion coefficient on a stochastic sampler**: further gain, with
  no retraining.
- **SiT-XL reaches FID-50K of 2.06 at 256×256 and 2.62 at 512×512**, and
  beats DiT uniformly across model sizes and throughout training, converging
  faster at every size.
- Continuous-time training allows trading function evaluations against FID
  after the fact.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Velocity prediction beats score prediction at fixed architecture and budget | strong | the transition ablation, one variable changed |
| C2 | A linear or GVP interpolant beats the variance-preserving one | strong | same ablation, with the singularity argument as mechanism |
| C3 | The sampler's diffusion coefficient can be chosen after training and tuning it helps | strong | follows from the coefficient not entering the velocity or score; demonstrated without retraining |
| C4 | The interpolant's advantage comes from reduced transport cost | weak | path length is measured and observed to fall; no intervention isolates it |
| C5 | Continuous-time training is worth taking for its own sake | weak | the direct gain is marginal; the case is that it enables C3 |

## Method

Define a stochastic interpolant connecting the data and Gaussian
distributions, of which the variance-preserving diffusion path, the
generalized-VP path and the straight line are instances. Train a network to
estimate the velocity field of the corresponding probability-flow ODE; derive
the score from it.

Then transition: start from a DiT configuration (discrete time, score
prediction, VP interpolant, its standard sampler) and change one element at a
time until reaching SiT (continuous time, velocity prediction, linear
interpolant, tuned SDE sampler), reporting FID-50K at each step with training
steps, architecture, parameter count and sampling budget held constant.

Finally, with the model frozen, sweep the diffusion coefficient of the
reverse SDE — a quantity conventionally copied from the forward process —
and report the improvement it buys.

## Concepts

- **Stochastic interpolant** — a specified path connecting two distributions,
  of which diffusion's forward process is one case. The framework's point is
  that the path is a free choice.
- **Linear interpolant** — the straight line between data and noise; the
  rectified-flow path.
- **GVP (generalized variance-preserving)** — an interpolant holding variance
  constant across time for endpoint distributions of equal variance.
- **Velocity field** — the drift of the probability-flow ODE. Estimated
  directly here, with the score expressed from it.
- **Diffusion coefficient** — the noise amplitude of the reverse-time SDE.
  Conventionally tied to the forward process; here, a free sampler
  hyperparameter.
- **Transport cost / path length** — the distance the interpolant moves mass,
  offered as the reason straighter paths train better.

## Connections

Built on DiT ([LIT-tmpfnkux](../literature.d/LIT-tmpfnkux.md)), whose backbone it holds fixed — the comparison
is unreadable without knowing that the architecture is identical.

Sits in the stochastic-interpolant and flow-matching literature, which
generalizes score-based diffusion by decoupling the path from the process,
and provides the first systematic empirical case for the straight-line path
at transformer scale.

Forward to [LIT-tmps0tea](../literature.d/LIT-tmps0tea.md), which names this paper as the prior evidence for
rectified flow and states its limitation precisely: the advantages had been
shown at small and medium scale, and only for class-conditional models.

## Recommendations

- **R1** — Predict the velocity rather than the score. *Topic:* objective.
  *Status:* experimental. *Strength:* strong. *Applies when:* transformer
  diffusion or flow models; the identity converting between them makes this
  cheap to adopt.
- **R2** — Use a straight-line or GVP interpolant rather than the
  variance-preserving diffusion path. *Topic:* forward process. *Status:*
  experimental. *Strength:* strong. *Applies when:* as above.
- **R3** — Tune the stochastic sampler's diffusion coefficient after training;
  it is not determined by the forward process. *Topic:* sampling. *Status:*
  experimental. *Strength:* strong. *Applies when:* a continuous-time model
  and a stochastic sampler.
- **R4** — Train in continuous time so that the sampling discretization is a
  separate decision from the training one. *Topic:* training. *Status:*
  experimental. *Strength:* moderate. *Applies when:* the sampler will be
  tuned after training, which R3 says it should be.

## Bearing on the record

- **Should produce practices** for R2 (jointly with [LIT-tmps0tea](../literature.d/LIT-tmps0tea.md), which
  supplies the scale) and for R3, which the record has nothing resembling.
- **R1 nearly duplicates [SOTA-195](../practices.d/SOTA-195.md)** — predict `v` rather than the noise at low
  signal-to-noise — and is better read as independent support for it than as
  a new practice. The two arrive at velocity from different arguments:
  [SOTA-195](../practices.d/SOTA-195.md) from numerical failure of epsilon-prediction near zero SNR,
  this from a clean ablation at fixed compute.
- **Every sampler practice the record holds assumes the sampler is downstream
  of training** — [SOTA-203](../practices.d/SOTA-203.md) on higher-order solvers, [SOTA-207](../practices.d/SOTA-207.md) on choosing
  the deterministic one. R3 says one parameter never was, which is a free
  tuning pass the record has not recorded.
- **Supplies the controlled half of the rectified-flow case.** [LIT-tmps0tea](../literature.d/LIT-tmps0tea.md)
  has the scale and a 61-way sweep; this has one variable changed at a time.
  A practice drawn from either alone would be weaker than one drawn from both.

## Limitations

- One dataset, one conditioning mode, two resolutions. The paper it feeds
  into says so explicitly when justifying its own existence.
- FID is the only quality metric, and FID's known insensitivities are not
  discussed.
- The transport-cost explanation is an observation about path length
  accompanying the result, not an isolated cause. A shorter path and a better
  FID co-occur; nothing here makes one produce the other.
- The gain attributed to continuous time is marginal on its own, so the
  four-step transition's headline improvement is carried by two of the four
  steps.
- Sampling cost is matched by function evaluations, which is the right
  comparison for the ablation and not the same as wall-clock or as a fair
  comparison against samplers with different per-step costs.

## Open questions

- Is straightness the cause, or is transport cost a proxy for something else?
  An interpolant matched in path length but not straight would separate them.
- How much of the diffusion-coefficient gain survives at few function
  evaluations, where the practical interest is?
- Does the ranking hold under text conditioning and at scale? [LIT-tmps0tea](../literature.d/LIT-tmps0tea.md)
  answers the interpolant part and not the rest.
