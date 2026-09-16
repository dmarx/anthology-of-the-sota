---
number: 132
status: Read
formerly:
- NOTE-tmpm5eod
paper: LIT-265
title: 'Large Batch Optimization for Deep Learning: Training BERT in 76 minutes'
version: 2
history:
- version: 1
  date: '2026-09-15'
  note: >-
    Filed with a "Bearing on the record" that set this paper against LIT-058 as
    an unresolvable contradiction and refused a practice on those grounds.
- version: 2
  date: '2026-09-16'
  note: >-
    Tension closed against both papers. LIT-265 cites LIT-058 as motivation and
    reports its own large-batch results as untuned; the disagreement was in this
    note, not between the papers.
date: '2026-09-15'
summary: >-
  Scaling the learning rate layerwise by the ratio of the parameter norm to
  the update norm (inspired by LARS) stabilizes large-batch training across
  heterogeneous layer curvatures, allowing Adam-like adaptivity to compose
  with layerwise scaling and generalize across both vision and language models
  where LARS alone fails.
---

<!-- inactive-ok-file: THEORY-012 — Proposed, and cited in the bearing
     section as the account that replaced this note's claim of an
     unresolvable contradiction. -->
# NOTE-132: Large Batch Optimization for Deep Learning: Training BERT in 76 minutes

## Contribution

The paper proposes LAMB (Layer-wise Adaptive Moments optimizer for Batch
training), a layerwise adaptive large-batch optimizer that combines per-
dimension Adam normalization with per-layer learning rate scaling. LAMB
enables scaling BERT pre-training batch size to 32K–64K without accuracy
loss, reducing training time from 3 days to 76 minutes.

## Key insight

Scaling the learning rate layerwise by the ratio of the parameter norm to
the update norm (inspired by LARS) stabilizes large-batch training across
heterogeneous layer curvatures, allowing Adam-like adaptivity to compose
with layerwise scaling and generalize across both vision and language models
where LARS alone fails.

## Assumptions

- Local objectives are L-smooth; convergence theory uses Lavg (average per-
  layer smoothness) rather than global L_inf.
- Gradient noise is bounded in variance (standard SGD convergence
  assumption).
- Workers have synchronized AllReduce communication each step (fully
  synchronous data-parallel setting).
- Formal convergence proof covers simplified LAMB with beta1=0 (no first
  moment / momentum) and lambda=0 (no weight decay); practical LAMB with
  momentum and weight decay is used empirically without full theoretical
  coverage.
- Layerwise norm ratio phi(||x||)/||u|| is well-defined and non-zero; norm
  clipping [gamma_l, gamma_u] prevents degenerate layers.

## Key results

- **Nonconvex convergence of simplified LAMB (Theorem 1).** For simplified
  LAMB (beta1=0, lambda=0) with appropriate step size, the algorithm
  converges to an epsilon-stationary point at rate O(1/sqrt(T)) with
  complexity depending on Lavg (average layer smoothness) rather than L_inf
  (global smoothness), which can be significantly smaller for networks with
  heterogeneous curvature.
  *Holds when:* L-smooth nonconvex objective; bounded gradient variance;
  beta1=0, lambda=0; step size chosen per theorem conditions.
- **Large-batch accuracy preservation (empirical).** LAMB maintains BERT
  SQuAD F1 >= 90.4 at batch sizes up to 32,768 (64x baseline), while AdamW
  degrades at batch size > 16K; LARS fails entirely on BERT at all batch
  sizes.
  *Holds when:* BERT-Large on SQuAD v1.1; TPUv3 hardware; mixed-batch
  training schedule.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | LAMB maintains BERT pre-training accuracy (F1 ≥ 90.4 on SQuAD v1) when batch size is scaled from 512 to 32,768, while AdamW fails to scale beyond 16K. | strong | Empirical table comparing F1 scores of LAMB vs AdamW and LARS across batch sizes 512–32K on TPUv3 hardware. |
| C2 | LAMB reduces BERT pre-training wall-clock time from 3 days (81.4 hours) to 76 minutes using mixed-batch training on a TPUv3 Pod, achieving ~100% scaling efficiency. | strong | Empirical timing results in Table 1; 100.2% efficiency computed from 8599-iteration run finishing in 76.19 minutes. |
| C3 | LAMB is the first adaptive optimizer to achieve state-of-the-art top-1 accuracy on ImageNet/ResNet-50, whereas Adam/AdamW reach only 66–73% vs the 76.3% target. | strong | Comprehensive hyperparameter-tuned comparison in Table 3; LAMB achieves 76.6% at batch 2K and 76.4% at batch 32K. |
| C4 | LAMB's convergence rate in nonconvex settings depends on Lavg (average smoothness) rather than L_inf (maximum smoothness), giving it a theoretical advantage over SGD. | moderate | Formal convergence theorem for simplified LAMB (beta1=0, lambda=0); extension to general case left to future work. |

## Method

**LAMB (Layer-wise Adaptive Moments for Batch training).**

LAMB uses Adam as its base update rule to compute a per-parameter update
direction u_t incorporating first and second moment estimates. It then
scales this update layerwise: each layer's effective learning rate is
multiplied by phi(||x_t^(i)||) / ||u_t^(i)||, where phi clips the parameter
norm to [gamma_l, gamma_u]. This two-level adaptivity—per-dimension via Adam
and per-layer via the norm ratio—ensures the update magnitude stays
proportional to the parameter magnitude at every layer. For large batch
training, a square-root learning rate scaling rule and linear-epoch warmup
are applied without further hyperparameter tuning.

- Adam base optimizer (per-dimension first and second moment normalization)
- Layerwise learning rate scaling by ratio of parameter norm to update norm
- Norm clipping to [gamma_l, gamma_u] to prevent degenerate scaling
- Square-root LR scaling rule for automatic batch-size adaptation
- Linear-epoch warmup scheduling
- Mixed-batch training with re-warmup for sequence-length phase transition

## Concepts

- **Layerwise Adaptive Learning Rate** — Per-layer scaling of the update
  step by a function of the layer's parameter norm divided by its
  gradient/update norm, adapting the effective step size to each layer's
  geometry.
- **LARS (Layer-wise Adaptive Rate Scaling)** — Predecessor to LAMB using
  SGD with momentum as the base optimizer and layerwise norm-ratio scaling;
  works for ResNet but fails for attention models like BERT.
- **Mixed-Batch Training** — BERT training strategy using a larger batch
  size in the short-sequence phase (seq_len=128) and a smaller batch in the
  long-sequence phase (seq_len=512), maximizing TPU utilization throughout.
- **Critical Batch Size** — The batch size beyond which further increases
  slow convergence due to reduced gradient variance benefit; LAMB extends
  this threshold significantly compared to prior optimizers.

## Connections

**Builds on.**

- Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour (Goyal et al.,
  2017) — LAMB generalizes the linear LR scaling and warmup insights of
  Goyal et al. to adaptive optimizers and much larger batch sizes.
- LARS: Large Batch Training of Convolutional Networks (You et al., 2017) —
  LAMB replaces LARS's momentum SGD base with Adam, adding per-dimension
  adaptivity that enables generalization to language models where LARS
  diverges.

**Related.**

- Moshpit SGD: Communication-Efficient Decentralized Training on
  Heterogeneous Unreliable Devices ([LIT-372](../literature.d/LIT-372.md)) — Moshpit SGD uses LAMB as
  the optimizer for ALBERT pretraining experiments, demonstrating LAMB's
  applicability in decentralized settings.

## Recommendations

- **R1** — Use LAMB with square-root LR scaling and linear-epoch warmup to
  scale batch size without per-batch-size hyperparameter tuning.
  *Topic:* large-batch optimizer configuration · *Strength:* strong · *When:*
  Large-batch training (batch size >4K) of transformer models or ResNet;
  requires TPU or multi-GPU setup.
- **R2** — Apply re-warmup when switching between training phases with
  different sequence lengths or batch sizes to stabilize the optimizer
  state.
  *Topic:* multi-phase training stability · *Strength:* moderate · *When:* BERT-
  style two-stage pre-training or any scenario where the effective
  optimization landscape changes significantly mid-training.
- **R3** — Prefer LAMB over AdamW for large-batch BERT training; AdamW fails
  to maintain accuracy beyond batch size 16K and cannot be tuned to work at
  64K.
  *Topic:* optimizer selection for large-batch NLP · *Strength:* strong ·
  *When:* Batch sizes exceeding 16K for transformer pre-training tasks.

## Bearing on the record

**Resolved, and the tension was this note's, not the papers'.** The reading
above set LAMB's no-retuning claim against [SOTA-218](../practices.d/SOTA-218.md) as though the two could not
both hold. Going back to the paper closes it three ways. LAMB *cites* [LIT-058](../literature.d/LIT-058.md)
approvingly in its related work, as motivation — "learning rate scaling
heuristics with the batch size do not hold across all problems or across all
batch sizes". It labels its own large-batch tables *untuned* and says in three
places that manual tuning does better. And [LIT-058](../literature.d/LIT-058.md) never swept a
layerwise-normalized optimizer, so LAMB is not a counterexample to it.

What the paper claims is that a square-root rule plus warmup is *sufficient to
reach a fixed target without a sweep* under a two-level normalized optimizer.
What [SOTA-218](../practices.d/SOTA-218.md) forbids is drawing a steps-to-target curve that way and reasoning
from its shape. Different claims about different activities.

[SOTA-221](../practices.d/SOTA-221.md) is the practice this note now supports, and [THEORY-012](../theory.d/THEORY-012.md) is the
account that lets it stand beside [SOTA-218](../practices.d/SOTA-218.md) — that where a scaling heuristic
stops working is a property of the optimizer applying it. The reading's own R1,
R2 and R3 transcribe the paper correctly; it was the paragraph here that
overstated.

## Limitations

- Convergence theory only covers simplified LAMB (beta1=0, lambda=0); the
  general case with momentum and weight decay is left unproven.
- Scaling efficiency drops to ~76.7% at 64x hardware due to gradient
  communication overhead for BERT's 300M parameters.
- Mixed-batch training requires careful re-warmup tuning; decreasing batch
  size between phases risks optimization instability.
- Results are demonstrated primarily on TPUv3 hardware; behavior on GPU
  clusters with different interconnects may differ.

## Open questions

- What is the theoretical convergence rate of LAMB with beta1 > 0 and lambda
  > 0 in the nonconvex setting?
- Can LAMB's layerwise scaling be extended to second-order methods or
  Kronecker-factored curvature approximations?
- Is there a principled criterion for determining the maximum useful batch
  size for a given model, analogous to the critical batch size concept?
