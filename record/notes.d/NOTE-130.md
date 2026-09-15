---
number: 130
status: Read
formerly:
- NOTE-tmpko07h
paper: LIT-252
title: 'OpenDiLoCo: An Open-Source Framework for Globally Distributed Low-Communication Training'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
summary: >-
  DiLoCo's dual-optimizer local-SGD approach reduces inter-node communication
  by up to 500x with negligible quality loss, and pseudo-gradients can be all-
  reduced in FP16 without performance degradation, making billion-scale
  decentralized training practical.
---
# NOTE-130: OpenDiLoCo: An Open-Source Framework for Globally Distributed Low-Communication Training

## Contribution

Open-source implementation and replication of the DiLoCo method built on the
Hivemind library, scaling it to 1.1B parameters and demonstrating real-world
globally distributed training across 2 continents and 3 countries at 90–95%
compute utilization.

## Key insight

DiLoCo's dual-optimizer local-SGD approach reduces inter-node communication
by up to 500x with negligible quality loss, and pseudo-gradients can be all-
reduced in FP16 without performance degradation, making billion-scale
decentralized training practical.

## Assumptions

- Workers are geographically distributed with low inter-island bandwidth;
  the primary constraint is communication frequency, not latency.
- Data is approximately i.i.d. across workers (or mildly non-i.i.d. as in
  the original DiLoCo); no formal heterogeneity correction is applied.
- Training budget is long enough (44k–88k steps) for DiLoCo to close the
  FLOP-efficiency gap with DDP.
- Pseudo-gradients have sufficient numerical range to be safely cast to FP16
  without overflow or significant quantization error.
- Each worker uses PyTorch FSDP internally, so intra-worker scaling is
  handled separately from inter-worker DiLoCo sync.

## Key results

- **Replication result (150M model, 8 workers).** DiLoCo achieves perplexity
  13.73 vs. DDP baseline 13.68 at 500x less inter-island communication after
  88k steps on C4.
  *Holds when:* 150M Llama; H=500; 8 H100 workers; C4 dataset; Nesterov
  outer optimizer.
- **FP16 pseudo-gradient all-reduce (ablation).** FP16 all-reduce of pseudo-
  gradients causes no measurable perplexity degradation versus FP32, halving
  communication volume.
  *Holds when:* 4 and 8 workers; 150M model; all other settings identical.
- **Scaling to 1.1B parameters (4 workers, H=125).** DiLoCo at 1.1B
  parameters with H=125 reaches perplexity within 0.24 of DDP while
  communicating 125x less after 44k steps.
  *Holds when:* 1.1B Llama; 4x H100 nodes; 44k steps; limited scaling
  experiment.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | DiLoCo with 8 replicas matches the perplexity of full data-parallel training at 500x less communication on a 150M Llama model after 88,000 steps. | strong | Controlled experiment on C4 dataset; final perplexity 13.73 (DiLoCo) vs 13.68 (DDP baseline). |
| C2 | FP16 all-reduce of pseudo-gradients causes no measurable performance degradation compared to FP32. | strong | Ablation with 4 and 8 workers; perplexity curves overlap across FP16 and FP32 conditions. |
| C3 | DiLoCo scales to 1.1B parameters with 4 workers and 125 local steps achieving perplexity within 0.24 of the DDP baseline while communicating 125x less. | moderate | Single scaling experiment with 4x H100 nodes; limited steps (44k) relative to 150M experiment. |
| C4 | DiLoCo does not accelerate early-phase convergence; it achieves parity with DDP only after many steps. | moderate | FLOP-efficiency ablation shows single-machine training is more compute-efficient early in training. |

## Method

**DiLoCo (Distributed Low-Communication, local SGD variant).**

Each worker maintains a local copy of the model and runs an inner AdamW
optimizer for H steps independently. After H steps, pseudo-gradients
(difference between original and updated weights) are all-reduced across
workers and applied via an outer Nesterov SGD optimizer. The Hivemind
implementation wraps both optimizers into a single class, uses a DHT for
peer coordination, and supports PyTorch FSDP for intra-worker scaling.
Communication happens only once every H inner steps, reducing bandwidth
requirements by a factor of H.

- Inner optimizer: AdamW with local gradient steps
- Outer optimizer: Nesterov SGD applied to pseudo-gradients
- Hivemind DHT for decentralized peer coordination and fault tolerance
- PyTorch FSDP integration for multi-GPU workers
- FP16 all-reduce of pseudo-gradients

## Concepts

- **DiLoCo** — Distributed Low-Communication training; a local-SGD method
  that synchronizes model replicas infrequently using pseudo-gradients
  averaged via an outer optimizer.
- **Pseudo-gradient** — The difference between a worker's locally updated
  weights and the weights at the start of the local phase; used as the
  signal for the outer optimizer.
- **Local SGD** — A distributed training paradigm in which workers run many
  gradient steps independently before synchronizing, reducing communication
  frequency.
- **Hivemind** — A Python library for decentralized deep learning using DHT-
  based peer discovery and fault-tolerant all-reduce over the internet.

## Connections

**Builds on.**

- DiLoCo: Distributed Low-Communication Training of Language Models
  ([LIT-212](../literature.d/LIT-212.md)) — OpenDiLoCo replicates, open-sources, and scales the original
  DiLoCo experiments by Douillard et al.
- Hivemind: a Library for Decentralized Deep Learning — Uses Hivemind as the
  infrastructure layer for decentralized peer communication and DHT-based
  coordination.

## Recommendations

- **R1** — Use 4–8 DiLoCo workers with H=125–500 local steps for practical
  globally distributed LLM pretraining; FP16 all-reduce halves communication
  cost with no quality loss.
  *Topic:* decentralized training configuration · *Strength:* moderate · *When:*
  Models up to ~1B parameters; workers connected via internet-grade
  bandwidth; sufficient training budget to reach convergence parity with
  DDP.
- **R2** — Prefer fewer DiLoCo workers (2–4) if training budget is limited,
  as more workers improve final quality but converge more slowly per FLOP.
  *Topic:* worker count selection · *Strength:* moderate · *When:* Short
  training runs where reaching full convergence parity is not feasible.

## Bearing on the record

The open reproduction, and the worker-count guidance the original does not
give. It bears on the record as the evidence that the DiLoCo practice it
already carries reproduces outside the lab that published it.

## Limitations

- DiLoCo shows slower FLOP efficiency than DDP during early training,
  requiring long runs to amortize the benefit.
- All-reduce synchronization creates idle time for faster workers;
  asynchronous outer-step execution is future work.
- Scaling beyond 8 workers does not yet match DDP compute efficiency.
- Experiments limited to up to 1.1B parameters; behavior at larger scales is
  untested.

## Open questions

- Can asynchronous outer optimizer steps eliminate inter-worker idle time
  without harming convergence?
- How does DiLoCo scale beyond 1.1B parameters and with batch sizes larger
  than those tested?
- Can more sophisticated model-merging strategies (beyond Nesterov pseudo-
  gradient averaging) accelerate convergence?
