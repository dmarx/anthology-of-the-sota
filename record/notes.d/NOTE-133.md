---
number: 133
status: Read
formerly:
- NOTE-tmpmcac1
paper: LIT-361
title: 'Local SGD Converges Fast and Communicates Little'
version: 1
date: '2026-09-15'
summary: >-
  Workers can run SGD independently for H steps before averaging, and as long
  as H = O(sqrt(T/(Kb))), this infrequent synchronization incurs no asymptotic
  cost in convergence rate—communication can be slashed without sacrificing
  linear speedup.
---
# NOTE-133: Local SGD Converges Fast and Communicates Little

## Contribution

Provides the first rigorous convergence proof showing that local SGD
achieves linear speedup in the number of workers K on strongly convex
objectives, matching mini-batch SGD in gradient evaluations while reducing
communication rounds by up to O(T^{1/2}).

## Key insight

Workers can run SGD independently for H steps before averaging, and as long
as H = O(sqrt(T/(Kb))), this infrequent synchronization incurs no asymptotic
cost in convergence rate—communication can be slashed without sacrificing
linear speedup.

## Assumptions

- Objective is strongly convex and L-smooth (Lipschitz-continuous
  gradients).
- Stochastic gradients are unbiased with bounded variance: E[||g - grad
  f||^2] <= sigma^2.
- Gradient norms are bounded: ||grad f|| <= G everywhere.
- Workers have access to i.i.d. stochastic gradients from the same
  distribution.
- Synchronization interval satisfies H = O(sqrt(T/(Kb))) for linear speedup
  to hold.

## Key results

- **Theorem 1 (Synchronous Local SGD).** After T steps with K workers and
  synchronization interval H = O(sqrt(T/(Kb))), local SGD converges at rate
  O(1/(KTb)), matching mini-batch SGD.
  *Holds when:* Strongly convex, L-smooth objectives; bounded gradients; H =
  O(sqrt(T/(Kb))).
- **Communication Reduction Corollary.** Communication rounds can be reduced
  by a factor of up to O(sqrt(T)) relative to mini-batch SGD with no
  asymptotic loss in convergence rate.
  *Holds when:* Same conditions as Theorem 1; requires T large enough for
  the bound to be tight.
- **Theorem 2 (Asynchronous Local SGD).** Asynchronous local SGD achieves
  the same O(1/(KTb)) rate when the combined constraint H + tau =
  O(sqrt(T/K)) is satisfied, where tau is the maximum delay.
  *Holds when:* Strongly convex, L-smooth objectives; asynchronous delay tau
  bounded uniformly.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Local SGD converges at rate O(1/(KTb)) on strongly convex, smooth functions when H = O(sqrt(T/(Kb))), matching mini-batch SGD. | strong | Formal proof via perturbed iterate analysis bounding both variance reduction (factor K) and worker drift (function of H). |
| C2 | The number of communication rounds can be reduced by up to O(T^{1/2}) compared to mini-batch SGD without degrading the convergence rate. | strong | Derived directly from the constraint H = O(sqrt(T)) in the convergence theorem. |
| C3 | Asynchronous local SGD achieves the same asymptotic rate as synchronous local SGD when (H + delay) = O(sqrt(T/K)). | moderate | Extended proof in appendix; asynchronous version analyzed with analogous perturbed iterate lemma. |

## Method

**Local SGD (synchronized and asynchronous).**

K workers each maintain a local model and run H steps of SGD independently
using their own stochastic gradients. Every H steps all workers average
their parameters via AllReduce and reset to the common average. Convergence
is proven by tracking a virtual sequence equal to the average of all local
iterates and bounding the deviation of local iterates from this virtual
sequence. A quadratically weighted iterate average is returned as the final
solution.

- Periodic synchronization with AllReduce every H steps
- Perturbed iterate analysis: virtual (averaged) sequence nearly behaves as
  mini-batch SGD
- Drift bound: local iterates stay within O(H * eta * G) of the virtual
  average
- Quadratically weighted iterate averaging for optimal convergence rate
- Asynchronous extension allowing per-worker communication schedules

## Concepts

- **Local SGD** — Distributed SGD variant where workers run gradient steps
  independently for H iterations between global parameter averaging rounds.
- **Communication gap H** — The number of local SGD steps each worker
  performs between successive synchronization rounds; controls the
  communication-computation trade-off.
- **Perturbed iterate analysis** — Proof technique that tracks a virtual
  sequence (average of worker iterates) and bounds how far individual worker
  iterates stray from it.
- **Linear speedup** — The convergence rate improves proportionally with the
  number of workers K, so K workers converge K times faster than a single
  worker.

## Connections

**Builds on.**

- Optimal Distributed Online Prediction Using Mini-Batches (Dekel et al.,
  2012) — Mini-batch SGD baseline that local SGD is shown to match in total
  gradient evaluations.
- Communication-Efficient Learning of Deep Networks from Decentralized Data
  (McMahan et al., 2017) — FedAvg introduced the local SGD idea for
  federated learning; this paper provides the first convergence proof.

**Related.**

- Don't Use Large Mini-Batches, Use Local SGD ([LIT-362](../literature.d/LIT-362.md)) — Empirically
  extends local SGD to deep learning, introducing post-local SGD based on
  this theoretical foundation.
- SlowMo: Improving Communication-Efficient Distributed SGD with Slow
  Momentum ([LIT-373](../literature.d/LIT-373.md)) — Builds on local SGD as a base algorithm, adding
  a slow momentum outer loop.
- DiLoCo: Distributed Low-Communication Training of Language Models
  ([LIT-212](../literature.d/LIT-212.md)) — DiLoCo applies local SGD ideas at LLM scale, citing this paper
  as the theoretical basis for infrequent synchronization.

## Recommendations

- **R1** — Set the synchronization interval H = O(sqrt(T/(Kb))) to maintain
  linear speedup while maximizing communication savings.
  *Topic:* communication frequency · *Strength:* strong · *When:* Strongly
  convex, smooth objectives; T large enough that variance term dominates.
- **R2** — Use adaptive (increasing) communication intervals when the total
  number of training steps T is not known in advance.
  *Topic:* adaptive scheduling · *Strength:* moderate · *When:* When training
  duration is uncertain; respects the H = O(sqrt(T)) constraint for any
  realized T.
- **R3** — Prefer asynchronous local SGD in heterogeneous clusters,
  exploiting load balancing so faster workers advance multiple sequences.
  *Topic:* heterogeneous systems · *Strength:* moderate · *When:* Workers have
  different speeds; asynchronous delay tau must satisfy H + tau =
  O(sqrt(T/K)).

## Bearing on the record

`H = O(sqrt(T/(Kb)))` is the synchronization interval that keeps linear
speedup, and it is the number the record's local-update practice does not
name. A practice on communication frequency would rest here.

## Limitations

- Convergence proof restricted to strongly convex objectives; non-convex
  guarantees were not established in this paper.
- Bounded gradient assumption (||gradient|| <= G) may not hold in practice
  for deep neural networks.
- Analysis becomes loose for extreme settings (one-shot averaging H=T); one-
  shot SGD is not covered.
- Asymptotic bounds may be too conservative to predict optimal H for short
  training runs or large clusters.

## Open questions

- Can the convergence analysis be tightened in terms of bias and variance to
  better predict optimal H for practical finite-T regimes?
- How does local SGD behave on non-convex objectives with data heterogeneity
  across workers?
- What is the information-theoretic lower bound on communication for
  parallel SGD, and does local SGD achieve it?
