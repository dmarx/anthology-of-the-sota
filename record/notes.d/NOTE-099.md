---
number: 99
status: Read
formerly:
- NOTE-tmp5szin
paper: LIT-316
title: 'Distributed Deep Learning in Open Collaborations'
version: 1
date: '2026-09-15'
summary: >-
  By accumulating gradients until a fixed global batch size is reached
  regardless of how many peers are active, DeDLOC makes collaborative training
  mathematically equivalent to large-batch synchronous SGD, preserving
  training stability while tolerating dynamic peer arrival, departure, and
  heterogeneous hardware.
---
# NOTE-099: Distributed Deep Learning in Open Collaborations

## Contribution

Proposes DeDLOC, an algorithmic framework and system for collaborative deep
learning on heterogeneous volunteer hardware, featuring an adaptive
gradient-averaging algorithm that dynamically selects the optimal
communication strategy (AR-SGD, parameter server, BytePS, or hybrid) based
on current peer capabilities; demonstrated in a real 40-person collaborative
ALBERT pretraining for the Bengali language.

## Key insight

By accumulating gradients until a fixed global batch size is reached
regardless of how many peers are active, DeDLOC makes collaborative training
mathematically equivalent to large-batch synchronous SGD, preserving
training stability while tolerating dynamic peer arrival, departure, and
heterogeneous hardware.

## Assumptions

- Peers communicate over the public internet with heterogeneous and
  unpredictable bandwidth.
- Participant count is dynamic: peers may join or leave at any time between
  gradient averaging rounds.
- Data is IID across peers (for the sahajBERT experiment, data was shuffled
  and sharded uniformly).
- No peer is malicious; trust is social/organizational, not cryptographic.
- The global batch size target is fixed in advance and chosen to be
  compatible with standard large-batch SGD hyperparameters.
- NAT traversal succeeds for the majority of peers; a small fraction of
  peers require relay mode.

## Key results

- **Mathematical equivalence to large-batch SGD (informal).** Accumulating
  to a fixed global batch size before each optimizer step makes the update
  sequence identical in distribution to large-batch synchronous SGD,
  regardless of how many peers contributed each round.
  *Holds when:* Holds exactly when all gradients are accumulated before the
  optimizer step; DPU introduces one step of staleness, which is negligible
  in practice.
- **Adaptive averaging speedup (empirical).** LP-selected adaptive strategy
  runs 1.9x faster than ring All-Reduce on mixed server+workstation hardware
  with no loss in model quality.
  *Holds when:* 4 hardware configurations; 100 averaging rounds; ALBERT-
  large model.
- **Fault tolerance via group averaging (empirical).** Group-based averaging
  with group size m limits failure blast radius to 1/m of the global batch;
  the remaining groups proceed and the missed gradient contribution is
  simply absent from that step.
  *Holds when:* Groups of size ~8 used in sahajBERT; node dropout rate not
  formally characterized.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Adaptive averaging runs 1.9x faster than naive All-Reduce on hybrid heterogeneous hardware (servers + workstations) with no accuracy loss. | strong | Controlled timing experiment across 4 hardware configurations; mean over 100 averaging rounds. |
| C2 | DeDLOC with low-bandwidth workers and load balancing achieves 74% the speed of a high-bandwidth setup when adding part-time peers. | strong | ALBERT-large pretraining experiment with heterogeneous T4 instances and controlled bandwidth throttling. |
| C3 | sahajBERT, trained collaboratively by 40 volunteers, achieves competitive performance to XLM-R Large on Bengali NER and text classification despite using far fewer parameters and less expensive hardware. | moderate | WikiANN F1: 95.45 (sahajBERT) vs 96.48 (XLM-R Large); NCC: 91.97 vs 90.05. Real volunteer experiment with uncontrolled hardware. |
| C4 | DeDLOC's stepwise learning curves are virtually identical to regular large-batch SGD, confirming mathematical equivalence. | strong | Step-loss curve comparison between sahajBERT and an 8xV100 DDP baseline shown in appendix. |

## Method

**DeDLOC (Distributed Deep Learning in Open Collaborations).**

Peers accumulate local gradients independently until the collaboration
collectively reaches a target global batch size, then trigger a gradient
averaging round. The averaging strategy is chosen by solving a linear
program every ~2 minutes given each peer's current upload/download
bandwidth, compute speed, and pairwise throughput; this recovers All-Reduce,
Parameter Server, BytePS, or hybrid strategies depending on conditions.
Group-based averaging (similar to gossip with alternating groups of size m)
replaces global all-reduce to limit the blast radius of individual peer
failures. Peers use a DHT to coordinate global step counts, discover groups,
and download up-to-date parameters if they fall behind. NAT traversal is
handled via hole punching, circuit relays, or client mode.

- Fixed target batch size accumulation for training stability
- Linear programming-based adaptive averaging strategy selection
- Group-based fault-tolerant averaging with adaptive group size m
- Hivemind DHT for peer coordination and parameter synchronization
- NAT traversal (hole punching, circuit relays)
- Streaming dataset sharding with shuffle buffer

## Concepts

- **DeDLOC** — Distributed Deep Learning in Open Collaborations; a framework
  enabling synchronous data-parallel training across heterogeneous volunteer
  devices connected via the internet.
- **Adaptive averaging** — A dynamic gradient aggregation strategy that
  solves a linear program to assign communication roles (compute, aggregate,
  or both) to each peer to maximize training throughput.
- **Delayed parameter updates (DPU)** — A technique that overlaps gradient
  computation and communication by allowing exactly one round of gradient
  staleness, improving hardware utilization.
- **NAT traversal** — Techniques (hole punching, relaying) that allow two
  peers behind network address translation to establish direct peer-to-peer
  connections.
- **Collaborative training** — A paradigm where many independent
  participants pool their heterogeneous compute resources to jointly train a
  single shared model.

## Connections

**Builds on.**

- Towards Crowdsourced Training of Large Neural Networks using Decentralized
  Mixture-of-Experts ([LIT-246](../literature.d/LIT-246.md)) — DeDLOC uses the Hivemind library
  developed as part of Learning@home and addresses the same volunteer
  computing scenario, but targets data-parallel rather than expert-parallel
  training.

**Related.**

- SWARM Parallelism: Training Large Models Can Be Surprisingly
  Communication-Efficient ([LIT-303](../literature.d/LIT-303.md)) — SWARM builds on DeDLOC's
  infrastructure (Hivemind) and extends the approach to model-parallel
  training of billion-scale models.
- OpenDiLoCo: An Open-Source Framework for Globally Distributed Low-
  Communication Training ([LIT-252](../literature.d/LIT-252.md)) — OpenDiLoCo uses Hivemind (from
  DeDLOC's ecosystem) as the communication backend for decentralized DiLoCo
  training.

## Recommendations

- **R1** — Fix a target global batch size and accumulate gradients
  asynchronously across peers rather than synchronizing on a per-step basis,
  to make collaborative training equivalent to standard large-batch SGD.
  *Topic:* training consistency · *Strength:* strong · *When:* Any heterogeneous
  volunteer training setup where participant count and hardware vary
  dynamically.
- **R2** — Use backbone peers (CPU-only, stable internet) to maintain DHT
  integrity and store checkpoints; these are inexpensive and only require
  one to be available at all times.
  *Topic:* infrastructure design · *Strength:* strong · *When:* All
  collaborative training runs requiring persistence and fault tolerance.
- **R3** — Apply adaptive averaging via linear programming to assign
  aggregator roles based on peer bandwidth, especially when mixing high- and
  low-bandwidth participants.
  *Topic:* gradient aggregation · *Strength:* strong · *When:* Collaborations
  with heterogeneous network capabilities where naive All-Reduce would be
  bottlenecked by slow peers.

## Bearing on the record

Collaborative training that keeps the run equivalent to standard large-batch
SGD by fixing the global batch and accumulating asynchronously. That
equivalence is the design constraint worth carrying, more than the system.

## Limitations

- Requires recruiting and retaining volunteers, which introduces social and
  organizational challenges outside the algorithm.
- Authentication and contribution accounting are rudimentary; no defense
  against gradient poisoning by malicious peers.
- Data-parallel approach limits model size to what fits in the memory of a
  single participant's GPU.
- LP-based strategy optimization adds overhead and may not scale to very
  large collaborations.
- Part-time volunteer participation creates throughput variance that is
  difficult to plan for.

## Open questions

- How can contribution be fairly credited and malicious participants
  identified in open collaborations?
- Can the adaptive averaging approach be extended to model-parallel or
  hybrid parallel settings?
- What is the minimum reliable participation level needed to sustain a
  collaborative training run?
