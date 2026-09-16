---
number: 117
status: Read
formerly:
- NOTE-tmpennkr
paper: LIT-362
title: 'Don''t Use Large Mini-Batches, Use Local SGD'
version: 1
date: '2026-09-15'
summary: >-
  Large-batch SGD converges to sharp minima that generalize poorly; switching
  to local SGD mid-training introduces beneficial gradient noise that finds
  flatter minima, recovering single-machine generalization performance without
  sacrificing parallelism or communication efficiency.
---
# NOTE-117: Don't Use Large Mini-Batches, Use Local SGD

## Contribution

Introduces post-local SGD—a two-phase scheme that first trains with large-
batch SGD then switches to local SGD—and empirically demonstrates it closes
the generalization gap of large-batch training while being more
communication-efficient than both large-batch and standard local SGD.

## Key insight

Large-batch SGD converges to sharp minima that generalize poorly; switching
to local SGD mid-training introduces beneficial gradient noise that finds
flatter minima, recovering single-machine generalization performance without
sacrificing parallelism or communication efficiency.

## Assumptions

- The generalization gap from large-batch training is attributable to
  convergence to sharp minima, not to other factors (data ordering, learning
  rate warmup artifacts, etc.).
- The first learning rate decay milestone is the correct transition point
  from large-batch to local SGD; this is a heuristic, not a principled
  choice.
- Local SGD's noise structure (independent local steps between global
  averages) is the mechanism for finding flatter minima; no formal proof of
  this mechanism is given.
- Convergence theory from Stich (2018) for convex objectives approximately
  transfers to the non-convex deep learning setting.
- The effective batch size of local SGD (K * H * B_loc per sync) is
  comparable to mini-batch SGD at the same total gradient computations per
  round.
- Phase 1 large-batch training does not harm phase 2 local SGD convergence;
  the warm-start is assumed beneficial, not neutral.

## Key results

- **Post-local SGD closes the generalization gap (Table 3).** Post-local SGD
  with K=16 workers and H=16 or H=32 local steps matches the single-machine
  (K=1) baseline accuracy of ~93% top-1 on CIFAR-10, while large-batch mini-
  batch SGD at K=16 achieves only ~91-92%. The gain is robust across
  ResNet-20, WideResNet, and DenseNet architectures.
  *Holds when:* Validated on CIFAR-10/100 and ImageNet (ResNet-50).
  Communication rounds are reduced by factor H relative to large-batch SGD
  at same per-step gradient budget.
- **Local SGD beats mini-batch SGD at fixed effective batch size (Figure
  2).** At the same effective batch size (K * H * B_loc = K * B), local SGD
  with H=4 achieves strictly higher test accuracy than mini-batch SGD,
  across all tested architectures on CIFAR-10.
  *Holds when:* Holds for K in {4, 8, 16} and H in {4, 16, 32}; effect is
  more pronounced at larger K.
- **Sharpness reduction (Figure 4).** Local SGD converges to minima with
  lower sharpness (smaller largest Hessian eigenvalue) than large-batch
  mini-batch SGD at the same effective batch size. Post-local SGD achieves
  sharpness similar to single-machine SGD.
  *Holds when:* Measured on CIFAR-10 ResNet-20; sharpness correlates with
  generalization gap across methods.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Local SGD with H=4 achieves better test accuracy than mini-batch SGD at the same effective batch size and same communication frequency. | strong | Extensive CIFAR-10/100 and ImageNet experiments across multiple architectures (ResNet-20, WideResNet, DenseNet, ResNet-50). |
| C2 | Post-local SGD matches or exceeds single-machine (small-batch) generalization accuracy while using 16x workers and significantly fewer communication rounds. | strong | Table 3 shows post-local SGD matches 93% top-1 accuracy of small-batch baseline on CIFAR with K=16 and H=16/32. |
| C3 | The generalization gap of large-batch SGD is not purely an optimization issue but reflects convergence to sharper minima. | moderate | Sharpness measurements and learning curve analysis; post-local SGD reaches flatter minima than large-batch SGD. |

## Method

**Post-local SGD.**

Training proceeds in two phases. In phase 1 (up to step t'), all workers run
synchronized large-batch mini-batch SGD (H=1) with a linearly scaled
learning rate and gradual warmup. At step t' (typically the first learning
rate decay), training switches to phase 2 where each worker runs H>1 local
SGD steps between synchronizations. The transition point t' is set at the
first learning rate decay milestone. The result is a method that combines
the fast early convergence of large-batch SGD with the generalization
benefits of local SGD's stochastic noise.

- Phase 1: large-batch mini-batch SGD with linear LR scaling and warmup
- Phase 2: local SGD with H >> 1 local steps between AllReduce
  synchronizations
- Transition at first learning rate decay milestone
- Hierarchical variant for multi-level cluster topologies

## Concepts

- **Post-local SGD** — A two-phase training scheme that starts with large-
  batch SGD then switches to local SGD at a curriculum milestone to recover
  generalization.
- **Generalization gap** — The accuracy difference between models trained
  with small vs. large batch sizes, caused by large batches converging to
  sharp, poorly-generalizing minima.
- **Hierarchical local SGD** — A variant of local SGD that applies nested
  local SGD at each level of a hardware hierarchy (GPU, node, rack),
  adapting to different bandwidths at each level.
- **Effective batch size** — The total number of gradient samples used per
  synchronization step: K * H * B_loc for local SGD, versus K * B for mini-
  batch SGD.

## Connections

**Builds on.**

- Local SGD Converges Fast and Communicates Little ([LIT-361](../literature.d/LIT-361.md)) — Provides
  the theoretical convergence foundation for local SGD; this paper applies
  it empirically to deep learning.
- Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour (Goyal et al.,
  2017) — Establishes the large-batch SGD baseline and LR scaling rules that
  post-local SGD builds on in phase 1.

**Related.**

- SlowMo: Improving Communication-Efficient Distributed SGD with Slow
  Momentum ([LIT-373](../literature.d/LIT-373.md)) — SlowMo cites post-local SGD and generalizes the
  idea of a slow outer update on top of local SGD.
- DiLoCo: Distributed Low-Communication Training of Language Models
  ([LIT-212](../literature.d/LIT-212.md)) — DiLoCo references post-local SGD's finding that pretraining
  before local SGD phases matters, though DiLoCo contradicts the requirement
  for warm-start.

## Recommendations

- **R1** — Use post-local SGD instead of large-batch SGD when scaling to
  many workers: run mini-batch SGD until the first LR decay, then switch to
  local SGD with H=16 or H=32.
  *Topic:* generalization vs. scalability trade-off · *Strength:* strong ·
  *When:* Training budget fixed, K >= 4 workers, goal is to match small-
  batch generalization accuracy.
- **R2** — Prefer local SGD over mini-batch SGD at the same effective batch
  size (same compute per communication round) for better generalization and
  communication efficiency.
  *Topic:* communication efficiency · *Strength:* strong · *When:*
  Communication-restricted setting where synchronization time dominates
  gradient computation time.
- **R3** — Apply hierarchical local SGD in multi-level clusters by nesting
  local SGD at each bandwidth level of the hardware topology.
  *Topic:* heterogeneous systems · *Strength:* moderate · *When:* Clusters with
  hierarchical network topology (intra-node fast, inter-node slow).

## Bearing on the record

Post-local SGD is the strongest single practice candidate in the batch: it
is a schedule, it is one line to implement, and it claims to recover the
generalization that large-batch training loses. What it needs before filing
is a check that the result survives at transformer scale, which the paper
does not reach.

## Limitations

- Experiments limited to vision benchmarks (CIFAR, ImageNet); generalization
  to NLP or other modalities not validated.
- Post-local SGD's transition point t' requires tuning and is heuristically
  set at the first LR decay.
- Local SGD with very large H and K can encounter early-training
  optimization difficulties that affect later generalization.
- Theory from Stich (2018) covers only convex objectives; non-convex
  guarantees for post-local SGD are lacking.

## Open questions

- What is the optimal transition step t' from mini-batch SGD to local SGD,
  and can it be chosen automatically?
- Why exactly does local SGD find flatter minima—is it the noise structure,
  the averaging, or both?
- Can post-local SGD principles be applied to language model pretraining at
  scale?
