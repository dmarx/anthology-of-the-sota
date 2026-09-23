---
number: 208
status: Read
formerly:
- NOTE-tmpnr9by
paper: LIT-456
title: 'Muon is Not That Special'
version: 1
date: '2026-09-20'
summary: >-
  An optimizer that replaces the gradient's singular values with chaotic
  noise matches Muon on NanoGPT. Reading it: the LMO account of spectral
  optimizers fails its own control, and what the control leaves standing is
  that Muon's optimal step size is constant where Euclidean descent's is not.
---

<!-- inactive-ok-file: THEORY-024 THEORY-033 — THEORY-024 is Proposed as of this contribution and is what this reading demotes; THEORY-033 is Proposed and filed here from it -->
# NOTE-208: Muon is Not That Special

## Contribution

The success of Muon has been explained almost universally through linear
minimization oracles: Muon works because it takes the exact steepest-descent
step under the spectral norm. This paper builds the controls that account
never had. It sweeps the whole Schatten family, extrapolates past where any
norm exists, and then destroys the geometry entirely by substituting random
singular values — and performance survives. What is true afterwards that was
not before: precise adherence to a target geometry is not what makes spectral
optimizers work, and there is a candidate for what does.

## Key insight

The LMO framework is a description of Muon, not an explanation of it. The
thing the framework quietly supplies, and the thing that turns out to matter,
is that the resulting update has a *stable scale*: under exact line search in
a random-feature model, plain gradient descent beats spectral descent, but
only with an oscillating step-size schedule that cannot be implemented. The
spectral update's optimal step size is constant. Muon's advantage is that its
best learning rate is a number you can find once and keep.

## Assumptions

- **Single-layer matrix domain** for the LMO analysis in §2.1: a
  differentiable loss on matrices, strictly positive singular values.
- **`L`-Lipschitz gradients with respect to the chosen norm**, bounded below,
  plus sufficient-descent and boundedness conditions on the spectral mapping,
  for the convergence theorems (2.3, 2.5, D.1).
- **Mean-zero Gaussian post-activations** in the random-feature model, in the
  proportional asymptotic limit. The authors flag that this excludes ReLU.
- **Scale.** NanoGPT / GPT-2-style language models, WikiText-2 at 118M
  tokens, three seeds. One modality, one architecture family. This record's
  Muon practices are evidenced at 90M to 1.6T parameters and trillions of
  tokens; nothing here was run in that regime.

## Key results

- **Theorem 2.1** — a preconditioned spectral descent update is a
  steepest-descent update for some unitarily invariant norm *only if* the
  spectral mapping preserves the order of the singular values. *Holds when:*
  fixed function and point, single matrix layer. This is what places
  `TruncatedSGD`, `Kaon` and `Freon` at `p < 1` outside the LMO framework.
- **Theorem 2.3** — preconditioned spectral descent converges at
  `min ‖∇f‖ → 0` under sufficient-descent and boundedness conditions, with no
  LMO anywhere in the argument. *Holds when:* the two constants satisfy the
  divergence condition.
- **Theorem 2.5** — random spectral descent, i.e. `Kaon`, retains an
  `O(1/√K)`-type rate almost surely. *Holds when:* the random singular values
  are drawn i.i.d. on a bounded positive interval, independent of history.
- **Theorem 2.7 / E.5** — the QDWH-based rational iteration for `(G G^T)^{-p/2} G`
  is optimal in its class, with doubly exponential convergence. *Holds when:*
  the spectrum is bounded away from zero by `l`.
- **Empirical, Figure 4 (WikiText-2, 118M tokens)** — `TruncatedSGD` improves
  on SGD but does not reach Muon; `Kaon` matches Muon; `Freon` at the optimal
  exponent matches Muon, and that exponent lies strictly in `p < 1`.
- **Propositions 3.1–3.3 and Figure 5 (random features)** — under exact line
  search the ranking reverses in favour of GD, but optimal GD's step size
  oscillates violently while spectral descent's is constant.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The best-performing update in the Schatten family on GPT-2 is not steepest descent for any unitarily invariant norm | strong | Theorem 2.1 plus the measured optimal exponents in `p < 1` (Figures 6, I.7) |
| C2 | Precise target spectra are largely irrelevant to performance | moderate | `Kaon` matching Muon at NanoGPT scale, three seeds, one architecture |
| C3 | Suppressing large singular values is necessary but not sufficient | moderate | `TruncatedSGD` improves on SGD and falls short of Muon, Figure 4(a) |
| C4 | Muon's advantage is step-size optimality rather than geometry | moderate | exact in the random-feature model only; the authors call the framework diagnostic, not predictive |
| C5 | Optimization is governed by batch gradient alignment and directional descent potential | moderate | exact local Taylor expansion, but rigorous analysis confined to the RF setting |
| C6 | The optimal exponent cannot be tracked online | strong | a stated negative result: their adaptive-exponent attempts failed because the optimum fluctuates too wildly across batches |

## Method

Three optimizers, each a relaxation of the last. `TruncatedSGD` zeroes the
top few percent of singular values. `Freon` applies `U diag(σ^(1-q)) V^T` with
a mean-Schatten normalization that keeps the maximum step size independent of
the exponent, computed by an optimal QDWH rational iteration. `Kaon` replaces
the singular values with iterates of a chaotic third-order logistic
recurrence lifted to matrices, so that no SVD and no target norm is involved.

## Concepts

- **Preconditioned spectral descent** — an update `U f(σ) V^T` for an
  arbitrary vector-valued mapping `f`, which is a strictly larger family than
  steepest descent under a unitarily invariant norm.
- **Batch gradient alignment `A`** — how much of the update direction agrees
  with the stochastic gradient.
- **Directional descent potential `C`** — the second-order term along the
  update direction; unknowable a priori, since the Taylor midpoint is.
- **Mean Schatten norm** — `‖·‖_p / r^{1/p}`, the rescaling that makes the
  maximum step size comparable across exponents.

## Connections

Extends the local-expansion framework of the reference the paper labels 11
with a variable step size, non-LMO updates and stochasticity. It sits against
the duality line — Bernstein and Newhouse, [LIT-438](../literature.d/LIT-438.md) — and against the
LMO analyses of Kovalev and of Pethick et al. It cites Islamov et al. (2026),
"Non-Euclidean gradient descent operates at the edge of stability", which
joins this to [LIT-461](../literature.d/LIT-461.md); the record does not hold that paper.
Jiang et al.'s concurrent spectral clipping targets the same large singular
values as `TruncatedSGD`.

## Bearing on the record

- **It is the outside test [THEORY-024](../theory.d/THEORY-024.md) said it lacked.** That document's
  closing paragraph: all three of its sources share authors, and it is
  `Active` "not because anyone outside has confirmed the frame". The first
  outside group to test the frame finds its explanatory core does not hold.
  `THEORY-024` goes to `Proposed` on this reading.
- **It does not touch [SOTA-121](../practices.d/SOTA-121.md) or [SOTA-165](../practices.d/SOTA-165.md).** Muon still
  works; matrix preconditioning still wins the fair comparison. What is
  contested is the account, which is exactly the separation [ADR-031](../decisions.d/ADR-031.md)
  built the `THEORY` scheme for and [ADR-034](../decisions.d/ADR-034.md) restated.
- **It produces [THEORY-033](../theory.d/THEORY-033.md)**, on step-size realizability as the
  surviving account.
- **It produces no practice.** The actionable residue — retune the learning
  rate per optimizer rather than transferring it — is already
  [SOTA-165](../practices.d/SOTA-165.md)'s, from [LIT-156](../literature.d/LIT-156.md), at four scales rather than one.
  Filing it again from weaker evidence would add a citation and no claim.
- **`Kaon` is not a recommendation and must not be read as one.** The authors
  call it a pedagogical construction. It is a control, and [DP-006](../principles.d/DP-006.md)'s
  distinction applies: the record holds it because of what it rules out.

## Limitations

The authors list five, and the first two are the ones that bound the contest.

- **Scope**: one architecture modality (GPT-2), plus a random feature model.
  No vision, no other loss landscape, no frontier scale.
- **Assumptions**: the exact asymptotics require mean-zero activations, which
  excludes ReLU.
- **No predictive power**: `A` and `C` are stochastic and evaluable only
  post hoc, so the framework diagnoses rather than prescribes.
- **The adaptive-exponent idea failed**: tracking the optimal `q` step by step
  degrades long-run dynamics even with optimal step sizes.
- **`Freon`'s implementation is a demonstration**, and the authors doubt the
  engineering is worth it given how similar everything performs.

## Open questions

- Does `Kaon` still match Muon at 1B parameters and above? The whole force of
  the contest turns on whether the null result survives scale, and the
  practices it argues with are evidenced there and this is not.
- Do alignment and descent potential behave the same way outside the
  random-feature model and outside language?
- If the optimal exponent cannot be tracked online, is there a schedule for
  it? The paper's negative result is about greedy tracking specifically.
