---
number: 153
status: Read
formerly:
- NOTE-tmpwu96a
paper: LIT-323
title: 'Overlap Local-SGD: An Algorithmic Approach to Hide Communication Delays in Distributed SGD'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
summary: >-
  By decoupling synchronization into a background thread that maintains an
  anchor model and having workers pull back toward that anchor rather than
  waiting for direct peer communication, computation and communication are
  fully overlapped, reducing the effective communication-to-computation ratio
  from ~35% to ~1.5% in practical settings.
---
# NOTE-153: Overlap Local-SGD: An Algorithmic Approach to Hide Communication Delays in Distributed SGD

## Contribution

Proposes Overlap-Local-SGD, which introduces a per-node anchor model updated
asynchronously in a dedicated communication thread, allowing local SGD
computation and inter-node communication to run in parallel. This nearly
eliminates communication latency from the critical training path while
achieving better accuracy than competing Local SGD variants.

## Key insight

By decoupling synchronization into a background thread that maintains an
anchor model and having workers pull back toward that anchor rather than
waiting for direct peer communication, computation and communication are
fully overlapped, reducing the effective communication-to-computation ratio
from ~35% to ~1.5% in practical settings.

## Assumptions

- Objective function is L-smooth (Lipschitz continuous gradient).
- Stochastic gradients have bounded variance: E[||g_i - ∇f_i||^2] ≤ σ^2.
- Gradient heterogeneity is bounded: ||∇f_i(x) - ∇f(x)||^2 ≤ kappa^2 for all
  workers i.
- The mixing matrix is column-stochastic (not necessarily doubly-stochastic)
  to support the non-blocking anchor update structure.
- Communication latency is large enough that overlapping hides meaningful
  overhead (benefit diminishes when interconnects are very fast).
- IID or mildly non-IID data across workers (kappa^2 small); the convergence
  bound degrades quadratically in heterogeneity kappa^2.

## Key results

- **Theorem 1 (Overlap-Local-SGD convergence).** For non-convex smooth
  objectives, Overlap-Local-SGD converges at rate O(1/sqrt(mK)) where m is
  the number of workers and K is the number of communication rounds,
  matching fully synchronous SGD.
  *Holds when:* Requires L-smooth objective, bounded gradient variance σ^2,
  bounded heterogeneity kappa^2, and appropriately chosen learning rate;
  convergence bound includes an additional O(tau^2 * kappa^2 / K)
  heterogeneity term.
- **Empirical communication overhead reduction.** With tau=2 local steps,
  communication overhead is reduced from 34.6% to 1.5% of total training
  time while maintaining identical loss-versus-iterations convergence to
  synchronous SGD.
  *Holds when:* 16-node cluster, 40 Gbps Ethernet, ResNet-18 on CIFAR-10.
- **Accuracy vs. baselines.** Overlap-Local-SGD achieves higher test
  accuracy than CoCoD-SGD and EAMSGD for all tau in {1, 2, 8, 24} under both
  IID and non-IID data partitions; CoCoD-SGD diverges at tau=8 under non-
  IID.
  *Holds when:* CIFAR-10, ResNet-18, 16 workers; non-IID setting uses
  strongly skewed class distribution.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | With tau=2 local updates, Overlap-Local-SGD reduces the communication-to-computation overhead from 34.6% to 1.5% while maintaining the same loss-versus-iterations convergence as fully synchronous SGD. | strong | Empirical measurement on 16-node cluster with 40 Gbps Ethernet training ResNet-18 on CIFAR-10 (Figure 4). |
| C2 | Overlap-Local-SGD achieves higher final test accuracy than CoCoD-SGD and EAMSGD for all tested values of tau under both IID and non-IID data partitions. | strong | Tables 1 and 2 reporting test accuracy at convergence for tau in {1, 2, 8, 24}; CoCoD-SGD diverges at tau=8 under non-IID while Overlap-Local-SGD reaches 91.45%. |
| C3 | Overlap-Local-SGD converges to a stationary point of non-convex objectives at the same rate O(1/sqrt(mK)) as fully synchronous SGD when the learning rate is chosen appropriately. | moderate | Theorem 1 convergence bound (Eq. 12-13) proven in Appendix A under L-smooth, bounded variance, and bounded gradient heterogeneity assumptions. |

## Method

**Overlap-Local-SGD.**

Each worker node maintains two models: a local model x^(i) and a shared
anchor model z. In a dedicated background communication thread, the anchor
is updated by averaging all workers' local models (via AllReduce or
parameter server) and optionally applying a momentum term. In the main
computation thread, each worker performs tau local SGD steps on its local
data; at the end of every tau steps the local model is pulled toward the
current anchor by blending: x^(i) <- x^(i) - alpha*(x^(i) - z). Because the
communication thread is non-blocking, computation continues uninterrupted
while the anchor is being synchronized, hiding network latency. Stragglers
are naturally tolerated because no worker blocks waiting for others.

- Dual-model architecture: local model x^(i) and shared anchor model z
- Background non-blocking communication thread for anchor synchronization
- Periodic pullback of local model toward anchor after tau local steps
- Optional slow momentum on anchor update (Overlap-Local-SGD-M variant)
- Column-stochastic mixing matrix (non-doubly-stochastic) enabling the
  overlap structure

## Concepts

- **Anchor model** — A stale synchronized version of the average of all
  workers' local models, maintained asynchronously in a background thread
  and used as a consensus target for local models to pull toward.
- **Pullback coefficient alpha** — The fraction by which a worker's local
  model is moved toward the anchor after tau local updates; controls the
  trade-off between local drift and communication correction strength.
- **Local SGD (periodic averaging SGD)** — Distributed training method where
  each worker performs tau gradient steps on local data before averaging
  parameters with other workers; reduces communication frequency by factor
  tau but can increase error at convergence.
- **Straggler effect** — Performance degradation in synchronous distributed
  training caused by slower workers forcing faster workers to idle while
  waiting for synchronization; Overlap-Local-SGD mitigates this via non-
  blocking communication.

## Connections

**Builds on.**

- Deep Learning with Elastic Averaged SGD (Zhang, Choromanska, LeCun, 2015)
  — Inspired by EASGD's pullback-toward-anchor mechanism but makes
  communication non-blocking to actually exploit the overlap, which EASGD
  did not utilize.
- Faster Distributed Deep Net Training: CoCoD-SGD (Shen et al., IJCAI 2019)
  — Addresses the same communication-computation overlap problem; Overlap-
  Local-SGD consistently outperforms CoCoD-SGD in accuracy, especially under
  non-IID data and large tau.

## Recommendations

- **R1** — Set tau=2 for typical distributed training scenarios; this
  reduces communication overhead to ~1.5% of computation time while
  maintaining accuracy nearly identical to fully synchronous SGD.
  *Topic:* local update frequency · *Strength:* strong · *When:* Applies when
  network communication latency is the bottleneck (e.g., wireless, 10 Gbps
  Ethernet); benefit diminishes with very fast interconnects (NVLink) where
  communication is already cheap.
- **R2** — Use Overlap-Local-SGD with alpha=0.6 and anchor momentum beta=0.7
  as a starting point for non-IID data settings where plain Local SGD
  diverges at large tau.
  *Topic:* non-IID federated training · *Strength:* moderate · *When:*
  Empirically validated on CIFAR-10 with strongly skewed class distribution;
  hyperparameters may require tuning for other datasets or architectures.

## Bearing on the record

`tau=2` reduces communication to about 1.5% of computation with accuracy
indistinguishable from synchronous SGD. If that survives checking it is the
cheapest practice in the batch.

## Limitations

- Convergence bound includes a term O(tau^2 * kappa^2 / K) reflecting
  gradient heterogeneity across nodes; performance degrades significantly
  under highly non-IID data with large tau.
- The anchor model lags behind local models by one synchronization period,
  introducing staleness that grows with tau and communication latency.
- Experiments are limited to CIFAR-10 with ResNet-18; scalability to very
  large models (LLMs) or very large numbers of nodes is not evaluated.
- The non-blocking communication requires infrastructure support for
  concurrent compute and communicate threads; may not be directly available
  in all distributed training frameworks.

## Open questions

- Can Overlap-Local-SGD be combined with gradient compression (e.g.,
  PowerSGD) to further reduce bandwidth while preserving the accuracy
  advantage over CoCoD-SGD?
- How does the optimal pullback coefficient alpha and local step count tau
  depend on the degree of data heterogeneity across workers?
- Does the overlap approach generalize to second-order optimizers (e.g.,
  distributed Shampoo) where communication of preconditioner matrices is
  even more expensive than gradient communication?
