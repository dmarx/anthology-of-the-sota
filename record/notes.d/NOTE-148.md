---
number: 148
status: Read
formerly:
- NOTE-tmpuu97x
paper: LIT-276
title: 'Smoothing DiLoCo with Primal Averaging for Faster Training of LLMs'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
summary: >-
  DiLoCo's performance improves with more inner steps because the two-loop
  structure inadvertently provides stronger smoothing of the iterate sequence;
  GPA replicates this smoothing effect at every step by decoupling the
  gradient-computation interpolation constant from the model-evaluation
  averaging constant, eliminating the need for a two-loop structure.
---
# NOTE-148: Smoothing DiLoCo with Primal Averaging for Faster Training of LLMs

## Contribution

Introduces Generalized Primal Averaging (GPA), a unified optimizer that
decouples Nesterov's two interpolation constants to produce a smoother,
single-loop alternative to DiLoCo and Schedule-Free, achieving 8-10% fewer
training steps than AdamW on Llama models while reducing memory overhead and
hyperparameter count.

## Key insight

DiLoCo's performance improves with more inner steps because the two-loop
structure inadvertently provides stronger smoothing of the iterate sequence;
GPA replicates this smoothing effect at every step by decoupling the
gradient-computation interpolation constant from the model-evaluation
averaging constant, eliminating the need for a two-loop structure.

## Assumptions

- Base optimizer has O(sqrt(T)) regret in the convex setting; convergence
  theory is convex-only.
- mu_x and mu_y are fixed constants throughout training (not adaptively
  scheduled).
- A learning rate schedule is required; GPA is not schedule-free and does
  not self-regulate LR decay.
- Validated primarily on dense transformer architectures (Llama, ViT);
  sparse/MoE or non-transformer applicability is untested.
- Single-node training experiments only; distributed multi-worker GPA is
  proposed conceptually but not empirically validated.

## Key results

- **Theorem 1 (GPA convergence).** For any base optimizer with O(sqrt(T))
  regret, GPA achieves O(1/sqrt(T)) convergence with negative Bregman
  divergence correction terms that can accelerate convergence beyond the
  base optimizer rate.
  *Holds when:* Convex setting; fixed mu_x, mu_y; base optimizer satisfying
  O(sqrt(T)) regret bound.
- **Empirical speedup on Llama models (Table 2).** GPA-AdamW achieves 8.71%
  fewer steps to target loss than AdamW on Llama-160M and 10.13% fewer steps
  on Llama-1B.
  *Holds when:* Llama-160M and Llama-1B; C4 dataset; mu_y=0.7 (robust
  default); mu_x set via DiLoCo heuristic.
- **Large-batch speedup on ImageNet ViT (Figure 10).** GPA provides a 25.5%
  step reduction over AdamW in the large-batch regime on ViT-S/16.
  *Holds when:* ViT-S/16; ImageNet; large batch size setting; cosine LR
  schedule.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | GPA-AdamW consistently outperforms single-worker DiLoCo-AdamW and AdamW across all tested inner step configurations on Llama-160M and Llama-1B. | strong | Table 2: GPA achieves lowest validation loss (3.0908 vs. DiLoCo 3.1051) on Llama-160M; speedups of 8.71% and 10.13% over AdamW for 160M and 1B models. |
| C2 | GPA achieves comparable or superior performance to DiLoCo with fewer hyperparameters (3 vs. 4) and lower memory overhead. | strong | Table 4: memory-efficient GPA variant stores one fewer model copy than DiLoCo; no momentum buffer required. |
| C3 | GPA provides speedups of 7% and 25.5% over AdamW on ImageNet ViT in small-batch and large-batch settings respectively. | strong | Figures 5 and 10: GPA outperforms AdamW throughout training on ViT-S/16 across both batch size settings. |
| C4 | For any base optimizer with O(sqrt(T)) regret, GPA matches or exceeds the base optimizer's convergence rate when Bregman divergence terms dominate. | moderate | Theorem 1: convergence bound O(1/sqrt(T)) with negative Bregman divergence terms that can accelerate convergence. |

## Method

**Generalized Primal Averaging (GPA).**

GPA maintains three sequences: a gradient computation sequence y, an
unsmoothed sequence z updated by the base optimizer, and a smoothed model
evaluation sequence x. At each step, y is formed as a mu_y-weighted
interpolation of x and z; the base optimizer computes a search direction
from gradients at y and updates z; x is then updated as a mu_x-weighted
exponential moving average of x and the new z. The two interpolation
constants mu_x and mu_y are decoupled: mu_x controls smoothing of the model
evaluation sequence (analogous to DiLoCo's number of inner steps), while
mu_y controls the gradient computation point (analogous to DiLoCo's outer
momentum). A memory-efficient variant stores only y and z, reconstructing x
at evaluation time.

- Gradient computation sequence y: interpolates between x (smooth) and z
  (unsmoothed)
- Unsmoothed sequence z: updated by any base optimizer (e.g., AdamW) at
  gradient computation point y
- Smoothed model evaluation sequence x: exponential moving average of z with
  coefficient mu_x
- Decoupled interpolation constants mu_x and mu_y (vs. single mu in standard
  Nesterov)
- Memory-efficient formulation: store y instead of x, reconstruct x from y
  and z at evaluation

## Concepts

- **Generalized Primal Averaging (GPA)** — An optimizer framework extending
  Nesterov's primal averaging formulation by decoupling the interpolation
  constants for gradient computation and model evaluation into independent
  hyperparameters mu_y and mu_x.
- **Primal averaging formulation of Nesterov** — A reformulation of Nesterov
  momentum that explicitly separates a gradient computation sequence and a
  smoothed model evaluation sequence, enabling analysis as iterate averaging
  rather than gradient averaging.
- **Pseudo-gradient** — In DiLoCo's context, the parameter difference over H
  inner steps used as the outer optimizer's gradient signal; GPA replaces
  this with a continuous iterate average.
- **Schedule-Free optimizer** — An optimizer using uniform Polyak-Ruppert
  averaging of iterates with decoupled momentum; GPA generalizes it by
  replacing uniform with exponential moving averaging.
- **Step-K Nesterov** — Alternative name for single-worker DiLoCo,
  emphasizing that it applies Nesterov momentum to pseudo-gradients
  accumulated over K inner steps.
- **mu_x (GPA smoothing coefficient)** — Controls how aggressively the model
  evaluation sequence x is smoothed; set heuristically as mu_diloco^(1/H) to
  match DiLoCo's effective smoothing level.

## Connections

**Builds on.**

- DiLoCo: Distributed Low-Communication Training of Language Models
  ([LIT-212](../literature.d/LIT-212.md)) — GPA is explicitly framed as a smoothed, single-loop version of
  single-worker DiLoCo, inheriting its motivation and improving upon its
  two-loop structure.
- Schedule-Free Learning (Defazio et al.) — GPA generalizes Schedule-Free by
  replacing uniform averaging with exponential moving averaging via the
  decoupled mu_x parameter.
- Nesterov's Primal Averaging Formulation — GPA directly extends the primal
  averaging variant of Nesterov momentum by splitting its single mu into two
  independent constants.

## Recommendations

- **R1** — Initialize mu_x = mu_diloco^(1/H) to match an equivalent DiLoCo
  inner step count H, using the heuristic in Table 6; set mu_y ~ 0.7-0.9.
  *Topic:* hyperparameter initialization · *Strength:* strong · *When:* When
  transferring from a known DiLoCo configuration; mu_y=0.7 is robust across
  models and modalities.
- **R2** — Use the memory-efficient GPA formulation (store y and z,
  reconstruct x) to reduce additional model copies from 4 to 3 versus
  DiLoCo's 4.
  *Topic:* memory efficiency · *Strength:* strong · *When:* Memory-constrained
  training of large models; no quality degradation observed.
- **R3** — Pair GPA with a cosine learning rate schedule; unlike Schedule-
  Free, GPA requires an explicit schedule because exponential moving
  averaging does not self-regulate learning rate decay.
  *Topic:* learning rate scheduling · *Strength:* strong · *When:* Always
  required; GPA is not schedule-free by design.
- **R4** — For distributed training, use GPA's mu_x as a continuous
  hyperparameter independent of the number of inner steps, enabling cleaner
  disentanglement of communication frequency from optimizer smoothing.
  *Topic:* distributed training · *Strength:* moderate · *When:* Cross-regional
  distributed training where decoupling communication frequency from
  smoothing is desirable.

## Bearing on the record

Primal averaging in place of DiLoCo's outer optimizer, which makes the
smoothing strength continuous and independent of the inner step count.
Directly relevant to the practice the record already carries, and the most
recent paper in the batch.

## Limitations

- Convergence theory is limited to convex settings; non-convex convergence
  advantages over the base optimizer are not theoretically characterized.
- GPA requires a learning rate schedule (not schedule-free), adding a
  scheduling hyperparameter that Schedule-Free avoids.
- GPA incurs O(n) additional FLOPs per step vs. O(n/H) for DiLoCo, which
  amortizes its compute cost over H steps.
- Validated primarily on dense transformer architectures; compatibility with
  sparse models, MoE, or non-transformer architectures is untested.
- Single-node experiments; distributed multi-worker GPA design is proposed
  but not empirically validated.

## Open questions

- Can GPA's convergence advantage over the base optimizer be proven in the
  non-convex setting?
- How does GPA interact with other optimizers (Shampoo, SOAP, Muon) beyond
  AdamW as the base?
- Can mu_x be adapted dynamically during training rather than fixed, e.g.,
  using hyperparameter-free scheduling analogous to Schedule-Free?
- What is the optimal distributed variant of GPA where mu_x and the
  communication interval are separately tunable?
