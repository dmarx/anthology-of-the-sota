---
status: Read
paper: LIT-tmpjz77h
title: 'Communication-Efficient Learning of Deep Networks from Decentralized Data'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
summary: >-
  Performing multiple local SGD steps on each client's private data before
  averaging model parameters is far more communication-efficient than a single
  gradient step per round, and the resulting averaged model is robust to non-
  IID and unbalanced data distributions provided all clients share the same
  initialization each round.
---
# NOTE-tmp98kf8: Communication-Efficient Learning of Deep Networks from Decentralized Data

## Contribution

Introduces Federated Learning and the FederatedAveraging (FedAvg) algorithm,
which trains a shared deep network model by aggregating locally-computed SGD
updates from mobile devices without centralizing raw data. Demonstrates
10-100x reduction in communication rounds compared to synchronized SGD
across multiple model architectures and datasets.

## Key insight

Performing multiple local SGD steps on each client's private data before
averaging model parameters is far more communication-efficient than a single
gradient step per round, and the resulting averaged model is robust to non-
IID and unbalanced data distributions provided all clients share the same
initialization each round.

## Assumptions

- All clients share the same global model initialization at the start of
  each communication round (required for parameter-space averaging to work).
- Client data is fixed and non-streaming; each client has a local dataset of
  size n_k drawn i.i.d. from its local distribution.
- The server can reliably contact all selected clients each round (no client
  dropout or asynchrony in the base analysis).
- For the IID setting: each client's data is an i.i.d. sample from the
  global data distribution, so local objectives are unbiased estimates of
  the global objective.
- Local objectives are smooth enough for mini-batch SGD to converge within E
  epochs of local training.

## Key results

- **Communication round reduction (empirical, Sections 3–4).** Increasing
  local epochs E from 1 to 20 reduces required communication rounds by up to
  45x on MNIST 2NN and up to 28x on CNN, with comparable or better final
  accuracy.
  *Holds when:* IID data, C=0.1, B=10; gains are smaller but still present
  under non-IID partitions.
- **IID convergence equivalence (informal, Section 3).** Under IID data,
  FedAvg with sufficiently many local steps per round converges to a
  solution of comparable quality to centralized SGD, because the local
  gradient estimates are unbiased with respect to the global loss.
  *Holds when:* IID data distribution; no formal rate derived in this paper
  — tight rates established by later work.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | FedAvg reduces required communication rounds by 10-100x compared to FedSGD on MNIST and language modeling tasks. | strong | Empirical comparison across five model architectures and four datasets; Tables 2 and 4 quantify speedups up to 45x on MNIST 2NN. |
| C2 | FedAvg is robust to highly non-IID and unbalanced data distributions. | moderate | Experiments with pathological non-IID MNIST partition (2 digits per client) still show convergence, though speedups are smaller than IID case. |
| C3 | Model averaging in parameter space works well when models share the same random initialization. | strong | Figure 1 shows that shared-initialization averaging achieves lower loss than either parent model, whereas different-initialization averaging can fail. |

## Method

**FederatedAveraging (FedAvg).**

The server selects a random fraction C of K clients each round and
broadcasts the current global model. Each selected client runs E epochs of
mini-batch SGD with batch size B on its local dataset, producing an updated
model. The server then computes a weighted average of these models (weighted
by each client's dataset size) to form the new global model. The process
repeats for as many rounds as needed. Three hyperparameters control compute-
communication tradeoff: C (client fraction), E (local epochs), and B (local
batch size).

- Client fraction C controlling parallelism
- Local epoch count E controlling per-client computation
- Local mini-batch size B controlling update granularity
- Weighted server averaging proportional to local dataset sizes n_k

## Concepts

- **Federated Learning** — Training paradigm where a model is learned from
  data distributed across many devices, with only model updates (not raw
  data) communicated to a central server.
- **Non-IID data** — Data distribution where each client's local dataset is
  not representative of the global population distribution, a defining
  challenge of federated settings.
- **FedSGD** — Baseline federated algorithm computing one full gradient step
  per round using a fraction of clients; equivalent to FedAvg with E=1 and
  B=infinity.
- **Communication round** — One cycle of server broadcasting a model,
  clients performing local updates, and server aggregating the results; the
  primary unit of communication cost in federated learning.
- **Focused collection / data minimization** — Privacy principle of
  collecting only the minimal information necessary; federated learning
  embodies this by transmitting model updates rather than raw data.

## Connections

**Builds on.**

- Distributed training via model averaging (McDonald et al. 2010, Povey et
  al. 2015) — FedAvg adapts iterative model averaging from the data-center
  cluster setting to the federated mobile-device setting with non-IID
  unbalanced data.

**Related.**

- Epidemic Learning: Boosting Decentralized Learning with Randomized
  Communication ([LIT-tmpl3bu5](../literature.d/LIT-tmpl3bu5.md)) — Builds on federated/decentralized learning
  paradigm established by FedAvg, proposing randomized topologies to improve
  convergence speed.
- Achieving Tighter Finite-Time Rates for Heterogeneous Federated Stochastic
  Approximation under Markovian Sampling ([LIT-tmpeunc6](../literature.d/LIT-tmpeunc6.md)) — Provides
  theoretical convergence guarantees for federated SA that FedAvg-style
  methods lack under heterogeneity and Markovian data.

## Recommendations

- **R1** — Tune the local batch size B first (as it is free in wall-clock
  time on parallel hardware) before increasing E, to reduce communication
  rounds with minimal extra cost.
  *Topic:* hyperparameter tuning · *Strength:* strong · *When:* When client
  hardware can exploit batch-level parallelism and communication is the
  primary bottleneck.
- **R2** — Fix client fraction C at around 0.1 as a good balance between
  convergence speed and computational overhead; diminishing returns above
  C=0.1 in most experiments.
  *Topic:* client selection · *Strength:* moderate · *When:* Systems with 100 or
  more clients and moderate non-IID data.
- **R3** — Decay the amount of local computation (reduce E or increase B) in
  later training stages if FedAvg plateaus or diverges, analogous to
  learning rate decay.
  *Topic:* training schedule · *Strength:* moderate · *When:* Observed plateau
  or divergence with large E for tasks like character-level LSTM language
  modeling.

## Bearing on the record

FedAvg is the reason averaging weights after several local epochs is a
default rather than an experiment. The record's local-update practice
descends from it through DiLoCo, and this reading is where the E-versus-B
trade-off it leaves implicit is stated.

## Limitations

- No theoretical convergence guarantees for non-convex objectives; analysis
  is purely empirical.
- Performance degrades under highly non-IID data; speedups in the
  pathological non-IID case are much smaller than IID.
- Does not address client dropout, asynchrony, or communication failures
  common in real deployments.
- Privacy guarantees are limited; model updates can still leak information,
  especially for sparse gradient models.

## Open questions

- What theoretical conditions on data heterogeneity guarantee FedAvg
  convergence to the global optimum?
- How can differential privacy or secure aggregation be combined with FedAvg
  without destroying its communication efficiency?
- What is the optimal partitioning of computation between local epochs E and
  communication rounds?
