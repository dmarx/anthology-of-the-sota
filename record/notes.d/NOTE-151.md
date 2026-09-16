---
number: 151
status: Read
formerly:
- NOTE-tmpwigvz
paper: LIT-254
title: 'Stochastic Gradient Push for Distributed Deep Learning'
version: 1
date: '2026-09-15'
summary: >-
  Using the PushSum protocol's ratio-based de-biasing trick removes the
  requirement for symmetric (bidirectional) communication, allowing
  decentralized SGD to operate on directed graphs and substantially reduce
  communication overhead versus AllReduce SGD in bandwidth-constrained
  settings.
---
# NOTE-151: Stochastic Gradient Push for Distributed Deep Learning

## Contribution

This paper proposes Stochastic Gradient Push (SGP), which combines PushSum
gossip with SGD to enable decentralized deep learning over directed, sparse,
and time-varying communication topologies, and introduces Overlap SGP (OSGP)
to hide communication latency by overlapping gradient computation with
message passing.

## Key insight

Using the PushSum protocol's ratio-based de-biasing trick removes the
requirement for symmetric (bidirectional) communication, allowing
decentralized SGD to operate on directed graphs and substantially reduce
communication overhead versus AllReduce SGD in bandwidth-constrained
settings.

## Assumptions

- L-smooth objective: each local loss function has L-Lipschitz gradients
- Bounded stochastic gradient variance: E[||g_i - grad f_i(x)||^2] <=
  sigma^2
- Bounded message delay: gossip delays are finite and bounded (required for
  convergence guarantee)
- Mixing connectivity: the directed graph is repeatedly jointly strongly
  connected over bounded windows
- Column-stochastic mixing matrices (weaker than doubly-stochastic; allows
  directed graphs)
- IID or mildly heterogeneous data (non-IID heterogeneity degrades
  convergence)

## Key results

- **Theorem 1 and 2.** SGP converges to a stationary point at rate (1/K) *
  sum_k E[||grad f(z_avg_k)||^2] = O(sigma / sqrt(nK) + consensus_error / K)
  *Holds when:* Non-convex L-smooth objectives; directed exponential graph
  with log2(n)-round exact consensus; convergence matches O(1/sqrt(nK)) of
  AllReduce SGD asymptotically
- **Overlap SGP empirical result.** 1-OSGP trains ResNet-50 on ImageNet to
  77.1% top-1 accuracy in 2.7 hrs on 32 nodes vs 76.2% in 5.1 hrs for
  AllReduce SGD
  *Holds when:* 32 nodes, 10 Gbps Ethernet, bandwidth-limited regime;
  advantage disappears on high-bandwidth InfiniBand

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | SGP converges to a stationary point of smooth nonconvex objectives at rate O(1/sqrt(nK)), matching the convergence rate of parallel AllReduce SGD. | strong | Formal proof (Theorem 1 and 2) under smoothness, bounded variance, bounded delay, and mixing connectivity assumptions. |
| C2 | Overlap SGP (1-OSGP) achieves the same final validation accuracy as AllReduce SGD in approximately 1/3 the wall-clock time on 32 nodes over 10 Gbps Ethernet. | strong | Empirical results training ResNet-50 on ImageNet with 256 GPUs over 10 Gbps Ethernet; 77.1% top-1 accuracy in 2.7 hrs vs 76.2% in 5.1 hrs. |
| C3 | SGP is strictly more general than D-PSGD: when the topology is undirected and mixing weights are symmetric, SGP is mathematically equivalent to D-PSGD. | strong | Analytical argument showing push-sum weights collapse to 1 under symmetric doubly-stochastic mixing. |

## Method

**Stochastic Gradient Push (SGP) / Overlap SGP (OSGP).**

Each node maintains model parameters x_i, a PushSum scalar weight w_i, and
de-biased parameters z_i = x_i / w_i. At every iteration, each node
evaluates a stochastic gradient at z_i, updates x_i with a gradient step,
then performs one step of PushSum by sending (x_i, w_i) to out-neighbors in
the directed graph (nodes choose only outgoing weights, which form a column-
stochastic matrix). The ratio z_i = x_i / w_i corrects for the asymmetric
mixing, removing bias without requiring doubly-stochastic matrices. Overlap
SGP makes the communication non-blocking and allows up to tau gradient steps
to occur while messages are in flight, hiding communication latency.

- PushSum gossip protocol with column-stochastic mixing matrices
- Ratio-based de-biasing (z_i = x_i / w_i) to correct asymmetric averaging
- Directed exponential graph topology cycling through 2^k-hop neighbors
- Non-blocking message passing to overlap communication and computation
  (OSGP)

## Concepts

- **PushSum** — A gossip algorithm using column-stochastic matrices where
  each node tracks a scalar weight w_i; the ratio x_i/w_i converges to the
  true average even with asymmetric communication.
- **Column-stochastic mixing matrix** — A nonneg matrix where each column
  sums to 1, allowing directed (asymmetric) message passing; weaker
  requirement than doubly-stochastic.
- **Directed exponential graph** — A time-varying directed graph where node
  i sends to node (i + 2^k mod n) at iteration k, achieving exact consensus
  in log2(n) rounds.
- **Overlap SGP (tau-OSGP)** — Variant of SGP where communication is non-
  blocking and up to tau gradient steps are computed while awaiting incoming
  messages, hiding communication cost.

## Connections

**Builds on.**

- Can Decentralized Algorithms Outperform Centralized Algorithms? A Case
  Study for Decentralized Parallel SGD ([LIT-302](../literature.d/LIT-302.md)) — Generalizes D-PSGD
  from undirected/symmetric graphs to arbitrary directed graphs by replacing
  doubly-stochastic with column-stochastic mixing via PushSum.
- Stochastic Gradient Push for Strongly-Convex Functions (Nedic 2016) —
  Extends the original SGP algorithm (analyzed only for strongly-convex
  objectives) to smooth nonconvex functions as arise in deep learning.

## Recommendations

- **R1** — Use 1-OSGP (tau=1) over plain SGP when communication is a
  bottleneck, as it reduces training time by ~40% with negligible accuracy
  loss.
  *Topic:* communication-computation overlap · *Strength:* strong · *When:*
  Communication latency is significant relative to gradient computation time
  (e.g., Ethernet inter-node links).
- **R2** — Use a denser topology (2-peer vs 1-peer) during the first ~30
  epochs when parameter deviations are largest, then switch to a sparse
  topology for speed.
  *Topic:* adaptive topology scheduling · *Strength:* moderate · *When:*
  Training deep networks where early-stage parameter divergence is a
  concern.
- **R3** — Prefer directed exponential graphs over random or ring
  topologies; they achieve exact consensus in log2(n) rounds and balance
  communication load.
  *Topic:* graph topology selection · *Strength:* strong · *When:* When
  designing the gossip communication schedule for SGP.

## Bearing on the record

Directed exponential graphs reach exact consensus in `log2(n)` rounds, which
is the topology result the gossip practices would cite. Its overlap result —
hide the communication behind the next local step — is the same move the
record already recommends for allreduce.

## Limitations

- Approximate distributed averaging introduces a consensus error that grows
  with sparsity of the communication graph, degrading accuracy at scale
  (observed for 32-node experiments).
- Convergence analysis requires bounded message delays; very long delays can
  break guarantees.
- Performance degrades on high-bandwidth networks (InfiniBand) where
  AllReduce is no longer a bottleneck, reducing the advantage of SGP.

## Open questions

- Can SGP be combined with gradient compression
  (quantization/sparsification) for additional communication savings?
- What is the optimal tau (overlap) and graph topology as a joint function
  of network bandwidth and model size?
- How does SGP perform under highly heterogeneous data distributions across
  nodes?
