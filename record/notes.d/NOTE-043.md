---
number: 43
status: Read
formerly:
- NOTE-tmpgnw5j
paper: LIT-076
title: 'DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling'
version: 2
history:
- version: 2
  date: '2026-09-10'
  note: >-
    The
tags:
- generative-modeling
date: '2026-09-09'
published: '2022-06-01'
summary: >-
  Notices that the diffusion ODE is semi-linear, solves its linear part analytically, and applies a numerical method only to the intractable neural-network integral. Training-free, 10–20 function evaluations, 4.70 FID at 10 NFE on CIFAR-10, and DDIM turns out to be exactly the first-order case.
---

# NOTE-043: DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling

## Contribution

Prior fast samplers treated the diffusion ODE as a black box and reached for
general-purpose solvers (Runge–Kutta and friends). This paper observes that the
ODE is **semi-linear** — it has a linear part that is known in closed form and
a nonlinear part that is the neural network — and that handing the whole thing
to a black box discards the closed-form half.

DPM-Solver computes the linear part **analytically** and, by a change of
variables to log-SNR `λ`, reduces the remainder to an **exponentially weighted
integral of the noise-prediction network**. First-, second- and third-order
approximations of that integral follow, with convergence-order guarantees.

## Key insight

Two, and the second is the more surprising.

**Approximate only what is intractable.** The paper's own summary of why it
works: "DPM-Solver keeps the known information as much as possible, and only
approximates the intractable integral of the neural network." A general solver
approximates the analytic part too, and pays for it in steps.

**The solution is invariant to the noise schedule.** Proposition 3.1 decouples
the exact solution of the diffusion ODE from the choice of `α_t` and `σ_t` —
given endpoints in `λ`, the solution does not depend on the schedule between
them. So the noise schedule, which the literature treated as a modelling
decision affecting sampling, does not affect the exact solution at all. It only
affects where the steps land.

## Assumptions

- **The noise-prediction network accepts continuous, non-integer times.** For
  discrete-time models this is a reparameterisation; the authors report it
  "can still work well" and hypothesise the smooth positional time embeddings
  are why. That is a hypothesis holding up the discrete-time half of the paper.
- The network is smooth enough in `λ` for a Taylor expansion — the only
  approximation made.
- Images; CIFAR-10 and others, 2022.

## Key results

- **4.70 FID at 10 NFE** and **2.87 FID at 20 NFE** on CIFAR-10.
- **4–16× speedup** over previous state-of-the-art *training-free* samplers.
- **Training-free**, and works on both continuous- and discrete-time
  pretrained models, under linear and cosine noise schedules.
- **DDIM is exactly DPM-Solver-1** (§4.1) — the first-order case. That
  retroactively explains DDIM's success and bounds it: it is the least accurate
  member of a family.
- Beats traditional Runge–Kutta methods (§4.2), which is the direct test of the
  "don't approximate the analytic part" argument.
- Two step-size schedules: uniform in `λ`, and an **adaptive** one that
  combines orders.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The diffusion ODE is semi-linear and its linear part is analytic | strong | derived |
| C2 | Approximating only the neural integral beats general solvers | strong | the RK comparison |
| C3 | The exact solution is invariant to the noise schedule between endpoints | strong | Proposition 3.1 |
| C4 | 10–20 NFE suffices, training-free | strong | measured |
| C5 | DDIM = DPM-Solver-1 | strong | shown |
| C6 | Discrete-time models tolerate continuous time inputs | **moderate — a stated hypothesis** | works empirically; the smooth-embedding explanation is guessed |

## Method

Change variables to `λ = log(α/σ)`. Solve the linear part in closed form. Taylor
expand the noise-prediction network in `λ` to order 1, 2 or 3. Choose steps
uniformly in `λ` or adaptively.

## Concepts

- **Semi-linearity, and solving what you can solve** — the transferable idea,
  and it is not about diffusion. Any ODE with a known linear part invites the
  same treatment.
- **Schedule invariance** — a modelling choice shown to be irrelevant to the
  quantity everyone thought it controlled.
- **Order as a dial** — the first/second/third-order family makes "how many
  steps" and "how accurate per step" separable.

## Connections

Sits with `LIT-067` and `LIT-093` as the third route to few-step sampling, and
is the one that requires **no training at all** — distillation needs a teacher
and a training run; consistency models need either; this needs a solver.

`LIT-038` is subsumed: DDIM is the first-order case. `LIT-075` (EDM) uses
**Heun's method, a second-order solver**, on a `ρ = 7` σ-grid, and reaches 35
NFE — arriving at the same conclusion (use a higher-order method) by a
different route, with the schedule chosen rather than shown irrelevant.

## Recommendations

- **R1** — When a system has an analytically solvable part, solve it and
  approximate only the rest. *Topic:* generative modelling, but the form is
  general. *Strength:* strong.
- **R2** — Prefer a dedicated higher-order solver to a general-purpose one.
  *Strength:* strong.
- **R3** — Before tuning a schedule, check whether the quantity it is supposed
  to control is actually invariant to it. *Strength:* strong, and C3 is a
  striking instance.
- **R4** — Reach for a training-free improvement before a training-based one;
  it costs a solver rather than a run. *Strength:* strong.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**

> **Overtaken by the [#121](https://github.com/dmarx/anthology-of-the-sota/issues/121) audit.** R1, R2 and R4 are now
> [SOTA-203](../practices.d/SOTA-203.md), for which this paper is the primary source. The rest of
> this reading stands as written.

The reading places `SOTA-188`'s source in context. `LIT-075`'s reading records
EDM's sampler as Heun's second-order method on a `ρ = 7` grid between
`σ_min = 0.002` and `σ_max = 80`, with the grid parameters tuned. **C3 here says
the exact solution does not depend on the schedule between endpoints** — so
EDM's `ρ` is choosing *where the approximation error lands*, not changing the
solution being approximated. That is a sharper way to read EDM's tuning than
EDM itself offers, and the record now has both papers in view.

C5 — DDIM is the first-order case — is also worth having recorded: the record's
diffusion notes treat DDIM as a technique, and it is a solver order.

The document's takeaways — "fast sampling for diffusion models", "ODE solver
optimization", "theoretical convergence guarantees", "practical
implementation" — say the paper is a fast ODE solver, four times, which is the
title.

## Limitations

- Images, 2022, FID only.
- C6 is explicitly a hypothesis and it underwrites the discrete-time results.
- Third-order convergence guarantees assume smoothness of a neural network in
  `λ`, which is assumed rather than characterised.
- The adaptive step-size algorithm is deferred to an appendix and not compared
  head-to-head with the handcrafted one in the main text.

## Open questions

- If the solution is schedule-invariant (C3), what exactly is a noise schedule
  *for* at training time? The paper answers the sampling half and leaves the
  training half untouched, and `LIT-036`'s simplified-objective weighting is
  the other half of the same question.
