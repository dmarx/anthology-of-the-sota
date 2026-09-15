---
status: 'Active'
title: 'SWARM Parallelism: Training Large Models Can Be Surprisingly Communication-Efficient'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2023-01-01'
arxiv: '2301.11913'
first_author: 'Ryabinin'
keywords:
- 'pipeline-parallelism'
- 'unreliable-workers'
- 'internet-scale'
- 'activation-compression'
implementations: []
summary: >-
  Ryabinin et al. (2023), [ARXIV-2301.11913](https://arxiv.org/abs/2301.11913). SWARM parallelism: pipeline stages
  over unreliable heterogeneous workers connected by slow links, rebalanced as
  workers come and go.
---
# LIT-tmpi6utz: SWARM Parallelism: Training Large Models Can Be Surprisingly Communication-Efficient

Ryabinin et al. (2023) — [ARXIV-2301.11913](https://arxiv.org/abs/2301.11913)

## Key takeaways

Introduces SWARM parallelism, a fault-tolerant pipeline-parallel training
algorithm for heterogeneous unreliable devices, and formalizes the "square-
cube law" showing that larger models become progressively less
communication-intensive in pipeline-parallel settings; demonstrates training
a 1B-shared-parameter (~13B effective) Transformer on 400 preemptible T4
GPUs with under 200Mb/s bandwidth.

- **Square-cube law (analytical).** For a Transformer with hidden dimension
  n, per-layer FLOPs scale as O(n^3) and inter-stage activation bandwidth
  scales as O(n^2), so the compute-to-communication ratio scales as O(n).
  Models with n >= ~4096 (GPT-3 scale) achieve >50% GPU utilization at
  500Mb/s and 100ms latency.
  *Holds when:* Pipeline parallelism with one layer per stage; single
  microbatch per forward pass; applies to dense Transformer blocks.
- **Adaptive rebalancing efficiency (empirical).** SWARM with T=300s
  rebalancing period achieves 95.8% of theoretically optimal throughput on
  preemptible T4 instances; no rebalancing achieves only 82.7%.
  *Holds when:* Simulation over 32-hour real preemption logs; 10 runs
  averaged; 32-stage pipeline.
- **Convergence parity with A100 baseline (empirical).** 1B shared-parameter
  (~13B effective) Transformer trained with SWARM on 400 preemptible T4 GPUs
  matches training loss trajectory of 128-A100 data-parallel baseline on the
  Pile dataset.
  *Holds when:* 4-week training run; qualitative convergence curve
  comparison; layer sharing (ALBERT-style) used.

## What the evidence does not cover

- Stage rebalancing requires downloading model parameters and optimizer
  state, which adds overhead when nodes switch stages frequently.
- Demonstrated only on a specific architecture (Transformer with layer
  sharing); generalization to diverse architectures is unverified.
- Scaling to many pipeline stages degrades rebalancing effectiveness due to
  increased variance in preemption events.
- Pipeline bubble overhead still exists, though mitigated by stochastic
  wiring and delayed parameter updates.
- Security against malicious nodes in the DHT or pipeline is not addressed.

## Standing in the anthology

Read — the reading is [NOTE-tmpmtu16](../notes.d/NOTE-tmpmtu16.md). Arrived in the imported batch, which
brought in the volunteer- and internet-scale branch, where workers join and
leave.
