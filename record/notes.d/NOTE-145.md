---
number: 145
status: Read
formerly:
- NOTE-tmptbs7j
paper: LIT-212
title: 'DiLoCo: Distributed Low-Communication Training of Language Models'
version: 1
date: '2026-09-15'
summary: >-
  Replacing the plain-averaging outer step of FedAvg with Nesterov momentum,
  while using AdamW for inner optimization over H~500 steps, enables language
  model pretraining across geographically distributed devices with minimal
  bandwidth requirements and strong robustness to data heterogeneity and
  worker availability.
---
# NOTE-145: DiLoCo: Distributed Low-Communication Training of Language Models

## Contribution

Proposes DiLoCo, a federated-averaging-style algorithm that trains
transformer language models across poorly-connected compute islands using
AdamW as the inner optimizer and Nesterov momentum as the outer optimizer,
achieving communication 500x less frequent than standard data parallelism
with competitive perplexity on C4.

## Key insight

Replacing the plain-averaging outer step of FedAvg with Nesterov momentum,
while using AdamW for inner optimization over H~500 steps, enables language
model pretraining across geographically distributed devices with minimal
bandwidth requirements and strong robustness to data heterogeneity and
worker availability.

## Assumptions

- Workers operate on i.i.d. or mildly non-i.i.d. data shards (robustness to
  heterogeneity is empirical, not theoretically guaranteed).
- Workers are homogeneous in speed; the synchronous outer step blocks on the
  slowest worker.
- Model parameters lie in a region of linear mode connectivity so that
  pseudo-gradient averaging is meaningful.
- Training budget is sufficient (88k+ steps) for DiLoCo to close the early-
  phase convergence gap with DDP.
- Inner optimizer state (Adam moments) is not shared; per-worker states
  evolve independently.

## Key results

- **Empirical convergence result (Table 2).** DiLoCo with 8 workers and
  H=500 achieves 15.02 PPL on C4 vs. 15.30 PPL for an 8x-batch single-worker
  baseline, communicating 500x less than DDP.
  *Holds when:* 150M decoder-only transformer; C4 dataset; 88k training
  steps; Nesterov outer lr=0.7, momentum=0.9.
- **Outer optimizer ablation (Figure 6).** Nesterov momentum is strictly the
  best outer optimizer; FedAvg (plain averaging) and Adam outer both yield
  significantly higher perplexity.
  *Holds when:* Same 150M/C4 setup; lr and momentum swept for each outer
  optimizer candidate.
- **Data heterogeneity robustness (Figure 5).** Non-i.i.d. clustered data
  shards converge to the same final PPL as i.i.d. shards after 88k steps,
  though i.i.d. converges faster in early training.
  *Holds when:* 8 workers; each worker's shard drawn from a single domain;
  i.i.d. baseline has uniformly mixed shards.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | DiLoCo with 8 workers and H=500 achieves lower perplexity than a single-worker baseline with 8x larger batch size, while communicating 500x less. | strong | Table 2 and Figure 2: DiLoCo reaches 15.02 PPL vs. 15.30 PPL for the 8x batch baseline on C4 with a 150M transformer. |
| C2 | DiLoCo is robust to non-i.i.d. data distribution across workers, matching i.i.d. final perplexity despite clustered data shards. | strong | Figure 5: non-i.i.d. and i.i.d. settings converge to similar final PPL after 88k steps, though i.i.d. converges faster early. |
| C3 | DiLoCo can operate without pretraining (random initialization) with only minimal degradation (-0.1 PPL) in final model quality. | strong | Figure 3: models trained from scratch reach similar final PPL as those pretrained for up to 24k steps. |
| C4 | Nesterov momentum is the best outer optimizer for DiLoCo; SGD (FedAvg) and Adam perform significantly worse. | strong | Figure 6: ablation over outer optimizers; Nesterov with lr=0.7, momentum=0.9 consistently best. |

## Method

**DiLoCo (Distributed Low-Communication).**

DiLoCo alternates between inner and outer optimization phases. Each outer
step t, k workers receive a shared global model and independently run H
inner steps of AdamW on their own data shard. Each worker then computes its
outer gradient as the difference between the pre- and post-inner-
optimization parameters. These outer gradients are averaged across workers
and fed to a Nesterov momentum outer optimizer to update the global model.
Workers do not communicate during inner steps; communication occurs only
once per H inner steps. Each worker maintains its own separate AdamW state
(first/second moments), which is not synchronized.

- Inner optimizer: AdamW run for H=500 steps per worker independently
- Outer gradient: parameter delta (old params minus new params) after H
  inner steps
- Outer optimizer: Nesterov momentum (lr=0.7, momentum=0.9)
- Communication: AllReduce of outer gradients once per H inner steps
- Separate per-worker Adam optimizer states (not synchronized)

## Concepts

- **DiLoCo** — Distributed Low-Communication training algorithm using large
  inner step counts (H~500) with AdamW inner and Nesterov outer optimizers
  across compute islands.
- **Outer gradient** — The parameter-space delta computed as (old global
  params) - (post-inner-optimization params), serving as the gradient signal
  for the outer optimizer.
- **Compute island** — A cluster of co-located accelerators that can
  communicate efficiently internally but is poorly connected to other
  islands.
- **FedAvg (Federated Averaging)** — Algorithm by McMahan et al. where local
  workers average parameters periodically; DiLoCo generalizes this by
  replacing the averaging outer step with Nesterov momentum.
- **Linear mode connectivity** — Property of neural networks enabling
  meaningful linear interpolation in parameter space between separately
  trained models; underpins why DiLoCo's parameter averaging works.

## Connections

**Builds on.**

- Local SGD Converges Fast and Communicates Little ([LIT-361](../literature.d/LIT-361.md)) — DiLoCo
  applies local SGD ideas at LLM scale with infrequent synchronization
  justified by Stich's convergence analysis.
- Don't Use Large Mini-Batches, Use Local SGD ([LIT-362](../literature.d/LIT-362.md)) — Post-local
  SGD introduced AdamW-style inner + outer optimization separation; DiLoCo
  extends this to LLM pretraining.
- SlowMo: Improving Communication-Efficient Distributed SGD with Slow
  Momentum ([LIT-373](../literature.d/LIT-373.md)) — SlowMo's slow outer momentum directly inspired
  DiLoCo's Nesterov outer optimizer design.
- Adaptive Federated Optimization / FedOpt (Reddi et al., 2021) — DiLoCo is
  an instantiation of FedOpt with specific choice of AdamW inner and
  Nesterov outer optimizers.

**Related.**

- Smoothing DiLoCo with Primal Averaging for Faster Training of LLMs (LIT-
  tmpa847l) — GPA reinterprets single-worker DiLoCo through the lens of
  primal averaging and proposes a smoother, more memory-efficient
  alternative.

## Recommendations

- **R1** — Use H=500 inner steps with Nesterov outer optimizer (lr=0.7,
  momentum=0.9) as the default DiLoCo configuration for transformer LM
  pretraining.
  *Topic:* hyperparameter defaults · *Strength:* strong · *When:* C4-scale LM
  pretraining with 8 workers; may require retuning for other scales or
  datasets.
- **R2** — Do not synchronize inner optimizer states (Adam moments) across
  workers; it increases communication 3x with negligible quality gain.
  *Topic:* communication efficiency · *Strength:* strong · *When:* Always
  applicable when using DiLoCo with stateful inner optimizers.
- **R3** — Outer gradient pruning of up to 50% (by sign-based method) can
  further reduce communication with only 0.39% perplexity degradation.
  *Topic:* gradient compression · *Strength:* moderate · *When:* Bandwidth-
  constrained settings with many workers or large models.
- **R4** — DiLoCo can be initialized from scratch without requiring
  pretraining, simplifying deployment.
  *Topic:* initialization · *Strength:* strong · *When:* Total training budget
  of 88k+ steps; shorter budgets may benefit from warm-start.

## Bearing on the record

The paper is already `LIT-212` and the record already carries a practice
from it. This reading adds the part that practice does not state: the inner
optimizer state is deliberately not synchronized, which is where two thirds
of the communication saving comes from.

## Limitations

- Validated only on decoder-only transformer language modeling (C4);
  generalization to other architectures (CNNs) or modalities is not
  confirmed.
- Experiments limited to models up to 400M parameters; behavior at billion-
  scale LLM training is extrapolated but not validated.
- Assumes homogeneous workers; heterogeneous worker speeds cause
  inefficiency due to synchronization barriers.
- Diminishing returns observed beyond 8 workers; the algorithm does not
  scale ideally to very large numbers of compute islands.
- Outer update effectively uses a very large batch size, reducing per-step
  data efficiency relative to sequential training.

## Open questions

- Does DiLoCo's advantage grow, shrink, or remain constant as model scale
  increases to 70B+ parameters?
- How should DiLoCo be adapted for asynchronous settings where workers
  operate at different speeds?
- What is the theoretical reason Nesterov outer momentum outperforms simple
  averaging, and can this be formalized?
