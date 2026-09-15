---
number: 156
status: Read
formerly:
- NOTE-tmpywc4x
paper: LIT-344
title: 'Byzantine-Tolerant Machine Learning'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
summary: >-
  Averaging is catastrophically fragile: a single Byzantine worker can steer
  the aggregate to any arbitrary vector. The fix is to replace aggregation
  with selection — choose the gradient vector that is most "centrally located"
  among its nearest correct neighbors, using the n-f-2 nearest neighbors to
  ensure the majority of those neighbors are correct workers.
---
# NOTE-156: Byzantine-Tolerant Machine Learning

## Contribution

The paper proves that no linear combination of worker gradient estimates
(including averaging) can tolerate even a single Byzantine worker in
distributed SGD. It then introduces Krum, the first gradient aggregation
rule proven to be Byzantine-resilient in arbitrary dimension d with
polynomial time complexity O(n²·(d + log n)). Krum selects the worker vector
with the smallest sum of squared distances to its n-f-2 nearest neighbors,
provably converging under the condition 2f+2 < n. An m-Krum extension
averages the top-m selected vectors to make better use of correct workers.

## Key insight

Averaging is catastrophically fragile: a single Byzantine worker can steer
the aggregate to any arbitrary vector. The fix is to replace aggregation
with selection — choose the gradient vector that is most "centrally located"
among its nearest correct neighbors, using the n-f-2 nearest neighbors to
ensure the majority of those neighbors are correct workers. This majority-
in-neighborhood structure is the multi-dimensional analogue of the scalar
Byzantine-robust median, and it enables convergence proofs that transfer
directly from the adversarial setting to any weaker failure model (including
hardware crashes).

## Assumptions

- Workers are synchronous: all n workers submit gradient vectors each round
  before aggregation occurs.
- Exactly f workers are Byzantine (arbitrary); the remaining n-f workers are
  correct (unbiased i.i.d. gradient estimates).
- Correct gradients satisfy E[G(x,ξ)] = ∇Q(x) with bounded variance: E[||G -
  ∇Q||^2] ≤ σ^2.
- The feasibility condition 2f+2 < n holds (strictly more than 2f+2 workers
  total).
- The parameter server is itself trustworthy (not Byzantine); server fault
  tolerance is out of scope.
- Byzantine workers know the choice function F and all other workers'
  gradient vectors (worst-case adversary).
- Diminishing step sizes satisfy Robbins-Monro conditions: Σγ_t = ∞ and
  Σγ_t² < ∞.
- Objective function Q is measurable and admits a non-convex convergence
  argument (Bottou 1998 framework).

## Key results

- **Lemma 1 (Impossibility of linear aggregation).** For any linear
  combination F(V_1,...,V_n) = Σ λ_i V_i with λ_n ≠ 0, there exists a
  Byzantine worker sending V_n = (1/λ_n)·U - Σᵢ₌₁ⁿ⁻¹(λᵢ/λ_n)·Vᵢ that forces
  F to equal any target U regardless of correct workers.
  *Holds when:* Holds for any fixed coefficients λ_i with at least one
  nonzero λ_n; applies to averaging, weighted averaging, and any linear
  rule.
- **Proposition 1 (Krum Byzantine resilience).** Krum is (α, f)-Byzantine
  resilient with sin α = η(n,f)·√d·σ / ‖g‖, where η(n,f) =
  √(2(n-f+f(n-f-2)+f²(n-f-1))/(n-2f-2)).
  *Holds when:* Requires 2f+2 < n; η = O(√n) when f = O(1), η = O(n) when f
  = O(n); convergence basin scales as η·√d·σ.
- **Proposition 2 (Krum-SGD convergence).** SGD with Krum aggregation
  converges almost surely to a flat region ‖∇Q(x)‖ ≤ η(n,f)·√d·σ for non-
  convex objectives with Robbins-Monro step sizes.
  *Holds when:* Requires (α,f)-Byzantine resilience of Krum (Proposition 1);
  non-convex convergence; no convergence to local minimum guaranteed.
- **Lemma 2 (Krum complexity).** The Krum function can be computed in
  O(n²·(d + log n)) time.
  *Holds when:* Dominant cost is n² pairwise squared-distance computations,
  each O(d); sorting costs O(n log n) per worker.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | No linear combination of the n worker vectors (including weighted averaging) can tolerate even a single Byzantine worker. | strong | Proved as Lemma 1 via a constructive attack: the Byzantine worker proposes V_n = (1/λ_n)·U - Σᵢ₌₁ⁿ⁻¹ (λᵢ/λ_n)·Vᵢ, forcing the linear combination to equal any arbitrary target vector U regardless of what correct workers propose. |
| C2 | The Krum function is (α, f)-Byzantine resilient: its expected output is within angle α of the true gradient, where sin α = η(n,f)·√d·σ / ‖g‖. | strong | Proved as Proposition 1 using multi-dimensional stochastic calculus. Requires 2f+2 < n. The key step bounds the distance from any selected Byzantine vector to the true gradient using only correct-to-correct worker distances. |
| C3 | SGD using Krum as its aggregation rule converges almost surely to a region where the gradient norm is small (‖∇Q(x)‖ ≤ η(n,f)·√d·σ), for non-convex cost functions. | strong | Proved as Proposition 2, following the non-convex convergence framework of Bottou (1998). Convergence to a flat region (small gradient) is demonstrated; convergence to a local minimum is not claimed (standard limitation in non-convex settings). |
| C4 | The time complexity of the Krum function is O(n²·(d + log n)), making it practical for high-dimensional parameter spaces. | strong | Proved in Lemma 2: computing n pairwise squared distances costs O(n·d) per worker, sorting distances costs O(n·log n) per worker, summing n-f-1 terms costs O(n·d); total over all n workers is O(n²·(d + log n)). |
| C5 | The m-Krum variant (averaging the m best-scoring vectors) retains (α, f)-Byzantine resilience while utilizing more correct worker information, provided n-m > 2f+2. | moderate | Proved by sketch in Section 6: η(n-i, f) ≤ η(n, f) for all i ∈ [0, m-1], so each selected vector satisfies Byzantine resilience at least as strong as the 1-Krum bound. |
| C6 | A naive distance-based selector (choose the vector minimizing sum of squared distances to all others) fails when f ≥ 2: Byzantine workers can collude so that a Byzantine vector wins. | strong | Constructive argument in Section 4 (Figure 3): f-1 Byzantine workers push the barycenter away from the correct area; the remaining Byzantine worker proposes this barycenter, which always minimizes the sum of squared distances. |

## Method

**Krum (and m-Krum).**

Setup: n workers, up to f Byzantine, parameter server runs synchronous
rounds. In each round t: 1. Server broadcasts current parameter vector x_t ∈
ℝ^d to all workers. 2. Each correct worker i computes gradient estimate
V_i^t = G(x_t, ξ_i^t). Byzantine workers send arbitrary vectors. 3.
Parameter server computes pairwise squared distances ‖Vᵢ - Vⱼ‖² for all i ≠
j. 4. For each worker i, identify its n-f-2 closest neighbors (by squared
distance). 5. Compute score s(i) = Σ_{i→j} ‖Vᵢ - Vⱼ‖², summing over those
n-f-2 neighbors. 6. Select i* = argmin_i s(i); set Krum output = V_{i*}.
(For m-Krum: iteratively select the top-m lowest-scoring vectors, removing
each after selection, then average them.) 7. Update: x_{t+1} = x_t - γ_t ·
Krum(V_1^t, ..., V_n^t). Correctness requires 2f+2 < n (strict majority of
correct workers after accounting for Byzantine influence on neighborhood
scoring).

- Pairwise squared distance computation: O(n·d) per worker pair
- n-f-2 nearest neighbors per worker: ensures each correct worker has
  majority-correct neighborhood
- Score function s(i) = sum of squared distances to n-f-2 nearest neighbors
- Argmin selection: selects the most centrally located vector
- Condition 2f+2 < n: Byzantine resilience feasibility bound
- Diminishing step sizes γ_t satisfying Σγ_t = ∞, Σγ_t² < ∞ (Robbins-Monro)
- m-Krum: iterative selection of top-m vectors, then average

## Concepts

- **(α, f)-Byzantine resilience** — A choice function F is (α, f)-Byzantine
  resilient if, for any configuration of up to f Byzantine workers: (i)
  ⟨E[F], g⟩ ≥ (1 - sin α)·‖g‖², i.e., the expected output points in roughly
  the same direction as the true gradient g; and (ii) the moments of F up to
  fourth order are bounded above by a homogeneous polynomial in the moments
  of a correct gradient estimator. Together these ensure SGD convergence
  despite Byzantine failures.
- **Byzantine failure** — A worker exhibiting completely arbitrary behavior:
  it may send any vector, including vectors chosen adversarially with full
  knowledge of the system, all other workers' vectors, and the choice
  function F. In practice subsumes crashes, computation errors, data
  poisoning, and adversarial attacks.
- **Krum score s(i)** — For worker i, s(i) = Σ_{i→j} ‖Vᵢ - Vⱼ‖², where the
  sum runs over the n-f-2 closest vectors to Vᵢ. The worker with the minimum
  score is selected as the Krum output. The n-f-2 neighbor restriction
  ensures at least n-2f-2 of those neighbors are correct workers.
- **η(n, f)** — η(n,f) = √(2(n-f + f(n-f-2)+f²(n-f-1))/(n-2f-2)). A scalar
  factor quantifying how much the Byzantine workers can deflect the Krum
  selection from the true gradient. η = O(n) when f = O(n); η = O(√n) when f
  = O(1) (constant number of failures).
- **correct worker** — A worker that computes an unbiased i.i.d. estimate of
  the true gradient: E[G(x, ξ)] = ∇Q(x). Exactly n-f workers are correct in
  any given round.
- **resilience condition 2f+2 < n** — The necessary condition for Krum to be
  (α, f)-Byzantine resilient. Equivalently, f < (n-2)/2, meaning strictly
  fewer than half (minus one) of workers can be Byzantine.

## Connections

**Builds on.**

- Online Learning and Stochastic Approximations (Bottou, 1998) — Provides
  the non-convex SGD convergence framework (conditions i-iv) that Blanchard
  et al. extend with condition (v) to handle Byzantine workers. Krum's
  convergence proof directly imports Bottou's semi-martingale argument.
- The Byzantine Generals Problem (Lamport, Shostak & Pease, 1982) — Defines
  the Byzantine failure model adopted in this paper. Classical result
  showing fault tolerance requires n > 3f; this paper's 2f+2 < n condition
  is its ML analogue.
- Fault-Tolerant Multi-Agent Optimization (Su & Vaidya, 2016) — Prior work
  on Byzantine-tolerant optimization, but restricted to 1-dimensional
  parameter spaces. Blanchard et al. extend to arbitrary dimension d.

**Related.**

- Aggregathor / Robust Distributed SGD (follow-on work, various) — Krum
  sparked a line of work on Byzantine-robust aggregation rules (coordinate-
  wise median, geometric median, BULYAN, etc.) that build on or compare
  against Krum.

## Recommendations

- **R1** — Replace gradient averaging with Krum (or m-Krum) in any
  distributed SGD deployment where some workers may behave arbitrarily,
  including crashes, software bugs, or data corruption.
  *Topic:* robust gradient aggregation · *Strength:* strong · *When:* Requires
  2f+2 < n (more than twice as many correct workers as Byzantine ones). Adds
  O(n²·(d + log n)) computation overhead at the parameter server per round.
- **R2** — When deploying Krum, increase mini-batch size per worker to
  reduce per-worker gradient variance σ, since Krum's convergence basin
  scales as η(n,f)·√d·σ. Smaller σ yields convergence closer to a true
  minimum.
  *Topic:* mini-batch sizing for Krum · *Strength:* moderate · *When:* Applies
  whenever d is large (high-dimensional models) or f is a significant
  fraction of n, since η(n,f) = O(n) in that regime and the √d factor
  amplifies gradient noise.
- **R3** — Prefer m-Krum over 1-Krum to leverage more worker gradient
  information while retaining Byzantine resilience, provided the additional
  O(m) computation overhead is acceptable.
  *Topic:* aggregation rule selection · *Strength:* moderate · *When:*
  Applicable when n-m > 2f+2. Best when the number of Byzantine workers f is
  small relative to n, allowing m to be large and thus recovering closer to
  full-averaging efficiency.
- **R4** — When designing fault-tolerant distributed ML systems that only
  need to tolerate crash failures (not adversarial Byzantine failures), use
  Krum as a conservative upper bound on required robustness — its
  convergence guarantees hold a fortiori for crash-only failures.
  *Topic:* fault tolerance without restart · *Strength:* strong · *When:* Crash
  failures are a strict subset of Byzantine failures. Any system that
  tolerates f Byzantine workers also tolerates f crash workers. For
  hardware-only failures, median-based or simpler rules may suffice, but
  Krum provides a proven safe baseline.
- **R5** — For gossip/decentralized settings, apply Krum locally at each
  node over its k-neighbor gradient set, replacing the global feasibility
  condition 2f+2 < n with the local condition 2f+2 < k. Choose gossip fan-
  out k to satisfy this condition given expected hardware failure rate, with
  modest over-provisioning.
  *Topic:* decentralized fault tolerance · *Strength:* strong · *When:* Applies
  to gossip topologies where each node aggregates from k neighbors. Requires
  k > 2f+2 where f is the expected number of simultaneously failed neighbors
  per node. For 1% failure rate and k=32, this tolerates up to f=10
  simultaneous neighbor failures.

## Bearing on the record

Krum is the first demonstration that the plain mean has no robustness at any
cluster size — a single worker can steer it anywhere. That negative is the
part that bears: the record has no practice about aggregation robustness,
and the reason to have one is this paper's first result rather than Krum
itself.

## Limitations

- Krum selects a single vector (or m vectors), discarding n-m gradient
  estimates. This reduces statistical efficiency relative to averaging — in
  the failure-free case, 1-Krum wastes n-1 gradient computations per step.
- The convergence result only guarantees reaching a "flat region" where ‖∇Q‖
  ≤ η(n,f)·√d·σ, not convergence to a local or global minimum. With large f
  or large d, this basin can be far from any true minimum.
- Time complexity is O(n²·(d + log n)) at the parameter server each round.
  In high-throughput settings with many workers and very high-dimensional
  models (d ~ 10¹¹), this is a non-trivial bottleneck.
- The analysis assumes a reliable parameter server. Making the parameter
  server itself fault-tolerant requires additional state-machine
  replication, which is noted but not solved.
- The paper assumes synchronous rounds. Extending Byzantine resilience to
  asynchronous distributed SGD (where workers may be arbitrarily slow) is
  listed as an open problem.
- The condition 2f+2 < n is a strict lower bound on the ratio of correct
  workers. It is unknown whether this bound is tight.
- Krum's Byzantine resilience degrades gracefully but does not recover when
  Byzantine workers learn and adapt over time (it assumes Byzantine
  knowledge is static per round).

## Open questions

- Is the bound 2f+2 < n tight? Can a Byzantine-resilient aggregation rule
  exist with weaker requirements on the fraction of correct workers?
- Can η(n,f) = O(n) (when f = O(n)) be reduced? A tighter factor would allow
  convergence closer to true minima with fewer correct workers.
- How to achieve Byzantine resilience with asynchronous workers, where a
  Byzantine worker can also simply be "silent" (delaying responses
  indefinitely)?
- Can Krum be made communication-efficient? In its current form, each worker
  must send a full d-dimensional gradient to the server; combining with
  gradient compression is unproven.
- Does m-Krum with the "select top-m without re-scoring" variant (selecting
  m lowest-scoring vectors in a single pass, rather than iterating) retain
  (α, f)-Byzantine resilience?
