---
status: Read
paper: LIT-tmp1lc2w
title: 'Towards Crowdsourced Training of Large Neural Networks using Decentralized Mixture-of-Experts'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
summary: >-
  Mixture-of-Experts architectures are uniquely suited to volunteer computing
  because each input activates only a small fraction of all experts, making
  asynchronous training with stale gradients far less harmful than in dense
  networks, while the DHT enables scalable decentralized bookkeeping without
  any central coordinator.
---
# NOTE-tmpoe1a8: Towards Crowdsourced Training of Large Neural Networks using Decentralized Mixture-of-Experts

## Contribution

Proposes Learning@home, the first training paradigm and infrastructure
enabling crowdsourced distributed training of large neural networks on
volunteer hardware, using Decentralized Mixture-of-Experts (DMoE) layers and
a Kademlia DHT for fault-tolerant, low-bandwidth expert discovery.

## Key insight

Mixture-of-Experts architectures are uniquely suited to volunteer computing
because each input activates only a small fraction of all experts, making
asynchronous training with stale gradients far less harmful than in dense
networks, while the DHT enables scalable decentralized bookkeeping without
any central coordinator.

## Assumptions

- Workers communicate over the public internet with arbitrary and variable
  latency (up to 1000ms simulated).
- Up to 10% of nodes may fail silently at any time (crash-stop model).
- Each expert is a self-contained sub-network that can be independently
  evaluated; no dense layer requires all workers to participate.
- Gating function activates only a small top-k fraction of experts per
  input, making gradient staleness per expert low.
- DHT peers are honest (no Byzantine behavior); security against adversarial
  participants is out of scope.

## Key results

- **DHT lookup latency scaling.** Beam search latency grows from 317ms at
  100 nodes to 764ms at 10,000 nodes — sub-linear (empirical O(log N)).
  *Holds when:* Kademlia DHT on real cloud instances; d-dimensional grid
  beam search with fixed beam width.
- **Throughput under latency (empirical).** DMoE throughput is near-constant
  for network latency up to 200ms; dense model-parallel throughput degrades
  by 2-5x over the same range.
  *Holds when:* 4x GTX 1080 GPUs; simulated exponential latency
  distribution; asynchronous Trainer/Runtime architecture.
- **Fault tolerance under 10% failure rate (empirical).** DMoE with 256
  experts converges on MNIST and WikiText-2 under 10% node failure rate with
  minimal accuracy degradation vs. no failures.
  *Holds when:* Crash-stop failures; DHT re-routes expert queries to
  surviving nodes; no explicit convergence rate formula provided.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Asynchronous DMoE training maintains near-constant throughput under network latency up to 200ms, whereas model-parallel training throughput degrades rapidly. | strong | Benchmark on 4x GTX 1080 GPUs with simulated exponential latency; validated on real cloud instances across 3 geographic regions. |
| C2 | DMoE converges more robustly than dense feedforward models under high latency and 10% node failure rates. | strong | MNIST convergence experiment comparing FFN to DMoE variants with 4, 16, and 256 experts under high/low latency and failure conditions. |
| C3 | DMoE achieves competitive language modeling perplexity on WikiText-2 under 1000ms latency and 10% failure rate. | moderate | Single Transformer-XL experiment; qualitative comparison to baseline, not a rigorous benchmark. |
| C4 | DHT-based expert lookup scales logarithmically, with beam search latency growing from 317ms at 100 nodes to 764ms at 10,000 nodes. | strong | Empirical measurement of DHT lookup time at three scales on cloud instances. |

## Method

**Learning@home with Decentralized Mixture-of-Experts (DMoE).**

Each worker runs three components: a Trainer that generates batches and
orchestrates forward/backward passes, a Runtime that hosts expert sub-
networks on GPU and processes incoming forward/backward requests, and a DHT
Node using Kademlia for bookkeeping. Experts are organized on a
d-dimensional grid; a structured additive gating function selects the top-k
experts via beam search over the DHT in O(dk log N) queries. Training is
fully asynchronous: trainers process many concurrent batches without waiting
for results, and runtimes apply gradient updates immediately on backward
requests. Gradient checkpointing is used to avoid storing intermediate
activations, enabling high throughput under high concurrency.

- Decentralized Mixture-of-Experts (DMoE) layer
- Kademlia DHT for expert address book and weight persistence
- Additive gating function with d-dimensional grid structure
- Beam search over DHT for top-k expert selection
- Fully asynchronous Trainer/Runtime architecture
- Gradient checkpointing for memory efficiency

## Concepts

- **Decentralized Mixture-of-Experts (DMoE)** — A layer containing
  independent expert sub-networks distributed across volunteer nodes,
  selected via a gating function that uses a DHT-backed beam search.
- **Distributed Hash Table (DHT)** — A decentralized key-value data
  structure allowing any participant to store and retrieve expert metadata
  in O(log N) queries with no central server.
- **Kademlia** — A specific DHT protocol using XOR distance metric for peer
  routing, widely used in BitTorrent and adopted by Learning@home for expert
  bookkeeping.
- **Structured gating function** — An additive expert selection function
  organized over a d-dimensional grid that reduces gating cost from O(N) to
  O(d*M) and supports efficient beam search.
- **Volunteer computing** — A paradigm where individuals donate idle compute
  resources (consumer PCs) to a distributed scientific computation project.

## Connections

**Builds on.**

- Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts
  Layer (Shazeer et al., 2017) — DMoE extends sparse MoE from centralized to
  fully decentralized settings, adopting the load-balancing regularization
  idea.
- Large Memory Layers with Product Keys (Lample et al., 2019) — Borrows the
  factorized product-key gating structure and adapts it for DHT-based
  distributed lookup.

**Related.**

- Distributed Deep Learning in Open Collaborations ([LIT-tmplekdf](../literature.d/LIT-tmplekdf.md)) — DeDLOC
  builds on Learning@home's infrastructure (Hivemind) to enable data-
  parallel collaborative training with real volunteers.
- SWARM Parallelism: Training Large Models Can Be Surprisingly
  Communication-Efficient ([LIT-tmpi6utz](../literature.d/LIT-tmpi6utz.md)) — SWARM parallelism extends the
  decentralized model-parallel idea from Learning@home to support billion-
  scale models with pipeline parallelism.

## Recommendations

- **R1** — Use gradient checkpointing in asynchronous distributed MoE
  training to avoid storing intermediate activations, significantly
  improving throughput and reducing memory footprint under high concurrency.
  *Topic:* memory management · *Strength:* strong · *When:* Any asynchronous
  distributed training setup where many batches are processed concurrently
  and GPU memory is a constraint.
- **R2** — Apply load-balancing regularization on the gating function to
  distribute computation evenly across experts and improve hardware
  utilization in volunteer settings.
  *Topic:* load balancing · *Strength:* moderate · *When:* Large MoE models with
  many experts where uneven expert utilization would bottleneck slower
  nodes.

## Bearing on the record

Training a mixture of experts across volunteered hardware. Filed for the
line rather than for a practice: nothing in this record is about training on
machines you do not control.

## Limitations

- Only demonstrated at small scale (MNIST, WikiText-2); scalability to truly
  large models is theoretical.
- Security vulnerabilities: malicious experts can poison gradients
  propagated through backpropagation.
- DHT lookup latency (hundreds of ms) is non-trivial and grows with network
  size.
- No mechanism for consistent model checkpointing or recovery of the global
  model state.
- Asynchronous training introduces stale gradients; theoretical convergence
  guarantees are limited.

## Open questions

- Can Learning@home be secured against Sybil attacks and gradient poisoning
  at scale?
- How does convergence degrade as the number of experts grows into the
  millions?
- Can DMoE be combined with data-parallel strategies for hybrid scaling
  without requiring fast interconnects?
