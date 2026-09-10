---
number: 62
status: Read
formerly:
- NOTE-tmpr6rju
paper: LIT-017
title: 'An Empirical Model of Large-Batch Training'
version: 1
tags:
- training-optimization
date: '2026-09-09'
summary: >-
  Defines the gradient noise scale — the ratio of the gradient's variance to its squared norm — and shows it predicts, to an order of magnitude, the batch size past which data parallelism stops buying speed. Also the source of "critical batch size" as a measurable quantity, and of the hyperbola relating steps taken to examples processed.
---

# NOTE-062: An Empirical Model of Large-Batch Training

## Contribution

Answers a question the field was answering by trial and error: **how large a
batch is worth using, before running the experiment.** The paper defines a
statistic — the **gradient noise scale** — computable during ordinary training,
and shows across eight tasks in three learning paradigms that it predicts the
largest useful batch size to within an order of magnitude.

It is also where **critical batch size** stops being a vibe and becomes a
defined quantity with a measurement procedure.

## Key insight

Batch size is a signal-to-noise question, and nothing else. A minibatch
gradient is an unbiased estimate of the true gradient whose covariance scales
as `Σ/B`. Expanding the loss to second order in a step of size `ε` along that
noisy gradient and minimising over `ε` gives

    ε_opt(B) = ε_max / (1 + B_noise/B)
    ΔL_opt(B) = ΔL_max / (1 + B_noise/B)

with

    B_noise = tr(HΣ) / (Gᵀ H G)                     (2.8)

So the *whole* dependence of per-step progress on batch size is the single
factor `1/(1 + B_noise/B)`. Below `B_noise` doubling the batch nearly doubles
progress; above it, doubling buys almost nothing. **At `B = B_noise` exactly,
training speed is 50% of the maximum** — the noise scale is the knee, not the
ceiling.

The Hessian makes 2.8 expensive, so the paper offers the estimator it actually
uses:

    B_simple = tr(Σ) / |G|²                          (2.9)

— the summed per-component gradient variance over the squared gradient norm,
which needs no Hessian and, they report, differs from `B_noise` by a small
constant factor in practice. Appendix A.1 gives a way to measure it with
negligible overhead inside data-parallel training, which is what makes the
result usable rather than merely true.

## Assumptions

- **A second-order expansion of the loss around the current point.** The
  derivation is local; the paper is candid that it involves "many unfounded
  assumptions" and rests its case on the empirical fit instead.
- **`B_simple ≈ B_noise` up to a constant** — exact only if the Hessian is a
  multiple of the identity, and defended as approximately true under training
  schemes that improve conditioning.
- **Batches are i.i.d. samples**, or `B ≪ dataset`. Notably the noise scale is
  **independent of dataset size**, which is what lets it transfer across
  domains.
- Derived for SGD; applied without modification to momentum, Adam and RMSProp,
  and found to still work.

## Key results

- **The knee is at the noise scale**, verified on MNIST, SVHN, CIFAR-10,
  ImageNet, Billion Word, Atari, OpenAI's Dota agent, and an SVHN VAE — eight
  tasks spanning supervised learning, RL and generative modelling.
- **The steps/examples tradeoff is a hyperbola:**

      (S/S_min − 1)·(E/E_min − 1) = 1               (2.11)

  where `S` is optimisation steps and `E` examples processed to reach a fixed
  loss. This is a Pareto frontier between wall-clock and total compute, and it
  is the shape of the curve, not just its scale, that the theory predicts.
- **Critical batch size is defined off that fit:** `B_crit = E_min / S_min`.
- **The noise scale grows over a run** as the loss falls — so the batch size
  that was right at the start is too small later, which is the argument for
  ramping it.
- **Model size affects the noise scale only through performance.** A bigger
  model has a larger noise scale because it reaches a better loss, not because
  it is bigger. That is a genuinely non-obvious claim and the paper isolates it.
- RL tasks have far larger noise scales — environment stochasticity plus
  credit-assignment variance — which is why Dota tolerates batches of millions
  and ImageNet does not.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Per-step progress depends on batch size only through `1/(1+B_noise/B)` | moderate | derived under a local quadratic model the authors flag as unfounded |
| C2 | The noise scale predicts the largest useful batch size to an order of magnitude | strong | 8 tasks, 3 paradigms |
| C3 | `(S/S_min−1)(E/E_min−1)=1` describes real training runs | strong | fit across tasks, and the shape is predicted not fitted |
| C4 | The noise scale rises through training | strong | measured |
| C5 | Model size matters only via the loss it reaches | moderate | isolated empirically; the mechanism is argued |
| C6 | Dynamically ramping the batch along the noise scale saves compute | moderate | analysed in Appendix D, demonstrated rather than deployed at scale |

## Method

Measure `B_simple = tr(Σ)/|G|²` from the gradients you already compute in a
data-parallel step (the per-worker gradients give the variance for free). Fit
full training runs to Equation 2.11 to get `E_min`, `S_min` and hence `B_crit`.
Compare the two.

## Concepts

- **Gradient noise scale** — the quantity, and the reason batch-size limits
  differ by domain rather than by folklore.
- **Critical batch size** — defined here as `E_min/S_min`, from a fit to the
  time/compute frontier.
- **The time/compute Pareto frontier** — that "train faster" and "train
  cheaper" are one dial with a known shape, not two goals.

## Connections

Directly upstream of the scaling-law literature, which inherits `B_crit`
wholesale — `LIT-028` uses it to allocate batch size, and the compute-optimal
line downstream of that depends on it. Also the theoretical companion to the
large-batch recipes: `LIT-007`'s linear scaling with warmup is what you do
*below* the noise scale, and LARS is what people reached for on hitting it.

## Recommendations

- **R1** — Measure the noise scale rather than sweeping batch sizes. *Topic:*
  training optimization. *Strength:* strong. *Applies when:* choosing data
  parallelism in a new domain — which is exactly where sweeps are most
  expensive.
- **R2** — Expect the useful batch size to **grow during a run**, and consider
  ramping it. *Strength:* moderate.
- **R3** — Read "we can use a bigger batch because the model is bigger" as a
  claim about the loss reached, not the parameter count. *Strength:* moderate.
- **R4** — State batch-size results as a point on the steps/examples frontier,
  not as a speedup. *Topic:* analysis and evaluation. *Strength:* strong.

## Bearing on the record

**Nothing is sourced to this paper**, which is the surprising part — the
anthology carries the downstream consequences of the noise scale without
carrying its origin. `B_crit` appears in the scaling-law practices as an
inherited quantity, and this is where it is defined and given a measurement.

No practice is filed from this reading: R1 is a real candidate and belongs to
a session that can check what the record already says about batch-size
selection, not to a note-repair pass. Flagged here so it is not lost.

The four takeaways this document carried were **directionally right and
contentless** — "introduces gradient noise scale", "predicts optimal batch
size", "critical batch size analysis". True, and they leave a reader unable to
compute anything. That is a different defect from the wrong-paper cases
`#114` found, and it is the more common one in this population.

## Limitations

- Order-of-magnitude prediction, which the paper says plainly. It tells you
  whether 10³ or 10⁵ is the right ballpark, not whether 8K beats 16K.
- The derivation is local and second-order; its justification is the fit.
- 2018 scales. The largest language experiment is Billion Word.
- C6 (adaptive batch sizing) is analysed more than it is demonstrated.

## Open questions

- Does the noise scale still predict the knee for a modern LLM at 10⁴–10⁵
  batch sizes and trillions of tokens? Every practice downstream assumes so.
- The preconditioned version — dividing gradient components by Adam's
  accumulated second moment — is tried and reported as "mixed results", which
  is unsatisfying given that everything is trained with Adam now.
