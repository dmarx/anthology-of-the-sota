---
number: 364
status: Read
formerly:
- NOTE-tmp4wfnp
paper: LIT-705
title: 'Dropout and BN variance shift'
version: 1
date: '2026-09-25'
summary: >-
  Dropout upstream of batch norm changes a unit's variance between train and
  test mode, and BN's frozen moving variance does not follow. The measured
  cost is large: CIFAR-100 DenseNet 77.42% → 68.55%, and the model
  misclassifies its own training data in eval mode. It shrinks with a
  lower drop rate and with a wider fan-in. Moving dropout after the last BN
  avoids the cost, but adds only about 0.2 top-1 on ImageNet by itself.
---

<!-- inactive-ok-file: SOTA-427 — Proposed; the practice this reading sources, filed with it -->

# NOTE-364: Dropout and BN variance shift

## Contribution

A named, derived and measured mechanism for a folk observation that
dropout and BN "don't combine". The mechanism is a train/test variance
mismatch that BN's stored statistics cannot follow. Before this paper the
observation was Ioffe and Szegedy's conjecture that BN makes dropout
redundant, with Wide ResNet as an unexplained exception. After it, the
exception has a quantitative reason: fan-in.

## Key insight

Dropout's test-time rule preserves the *mean* of a unit, and that is all it was
designed to preserve. A BN layer downstream also depends on the *variance*,
which it froze in train mode. So the network evaluated at test time is
normalized with constants from a different network.

## Assumptions

- Inverted dropout: `x̂ = a·x/p` in training, `x̂ = x` at test,
  `a ~ Bernoulli(p)`, where `p` is the retain ratio.
- Inputs i.i.d. with `E[x] = c` and `Var[x] = v`. Dropout masks independent of
  inputs and of each other.
- Case (b) also assumes a linear regime, weights "constant" late in training,
  and one shared pairwise correlation `ρ` for all inputs.
- Only BN's "normalize" step is analysed. The affine step is ignored.
- Setting: convolutional image classifiers (PreResNet-110, ResNeXt-29 8×64,
  WRN-28-10, DenseNet-BC 100/12) on CIFAR-10 and CIFAR-100, plus three
  ImageNet models for one table. Nothing here concerns LayerNorm or
  transformers.

## Key results

- **Eq. 8, case (a), BN directly after dropout.**
  `Δ(p) = v / ((1/p)(c² + v) − c²)`, which is `p` when `c = 0`. The only way to
  make it 1 is `p → 1`.
- **Eq. 14, case (b), a weight layer between them.**
  `Δ(p, d) = (vρ + v(1−ρ)/(d cos²θ)) / (vρ + ((1/p − 1)c² + v(1/p − ρ))/(d cos²θ))`.
  It goes to 1 as `p → 1` or as `d → ∞`. Table 1 measures `cos²θ` at
  0.014–0.035 in all four networks, so `d cos²θ` grows roughly linearly with
  `d`. That term is 2.6–3.8 for PreResNet and DenseNet, 14.7 for ResNeXt and
  44–53 for WRN.
- **Figure 1.** DenseNet-BC on CIFAR-100: 77.42% with no dropout, 68.55% with
  dropout 0.5 in each bottleneck.
- **Figure 5.** Eval-mode accuracy *on training data* falls below train-mode
  accuracy for dropout-0.5 PreResNet and DenseNet, with weights fixed.
- **Table 3 (5 seeds).** Re-estimating BN statistics in eval mode, weights
  frozen, lowers error in all 16 cells. In case (a) on CIFAR-100: DenseNet
  31.45 → 26.98 and PreResNet 32.45 → 26.57.
- **Table 4 (5 seeds).** One dropout layer before the softmax. On CIFAR-10 the
  best gain over no dropout is 0.05–0.13. On CIFAR-100 the best is DenseNet at
  0.1, 22.58 → 21.86. Several cells get worse.
- **Table 5 (5 seeds, no spread).** Drop 0.2 before the classifier on ImageNet:
  top-1 improves 0.21–0.23 on ResNet-200, ResNeXt-101 and SENet.
- **Table 6 and Eq. 15 (Uout).** `x(1 + r)`, `r ~ U(−β, β)`, has variance
  ratio `3/(3 + β²)`, which is 0.9967 at β = 0.1. In case-(b) placement it
  gains about 0.1–0.3. ResNeXt is flat.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Dropout upstream of BN makes BN's frozen variance wrong at test time, by a factor that is `p` in the simplest case | strong | Eq. 7–8 derivation; Fig. 1 and Fig. 4 measured moving vs real variance per BN layer |
| C2 | That mismatch, not over-regularization, is what costs accuracy | strong | Fig. 5: eval-mode accuracy on the training set drops with weights fixed; Table 3: recalibrating statistics alone recovers much of the loss |
| C3 | The shift shrinks with fan-in, which is why WRN tolerates bottleneck dropout | moderate | Eq. 14 under strong simplifying assumptions; Table 1 measured `d cos²θ`; Fig. 4 ordering of networks |
| C4 | Putting dropout only after the last BN adds accuracy | weak | Table 4 CIFAR changes mostly < 0.3 and mixed in sign; Table 5 ImageNet ≈ 0.2 top-1, no spread reported |
| C5 | Uout is a more variance-stable dropout that improves BN networks | weak | Table 6, gains of 0.1–0.3 in case (b) only; not compared against dropout after the last BN at matched settings |
| C6 | Recalibrated models beat their baselines | weak as worded | Table 3 beats the *uncalibrated* model; case-(a) models stay worse than the no-dropout network (e.g. DenseNet C10 6.82 vs 4.72) |

## Method

1. *Variance-shift statistic.* Train to convergence. Record each BN layer's
   moving variance, averaged over channels. Freeze the weights, switch to eval
   mode, and pass the training data, with the same augmentation, through the
   network again, accumulating the real variance the same way. Report
   `max(real/moving, moving/real)` per layer.
2. *Recalibration.* The same eval-mode pass, used to overwrite BN's moving
   mean and variance.
3. *Relocation.* A single dropout layer immediately before the softmax.
4. *Uout.* `x + x·r`, `r ~ U(−β, β)` in training, and identity at test.

## Concepts

- **Variance shift** — the ratio `Var_test(X) / Var_train(X)` for the input of
  a BN layer, where the train-mode value is what BN stored.
- **Dropout-(a) / Dropout-(b)** — dropout directly before a BN layer, and
  dropout before the last conv of a bottleneck (WRN's placement), respectively.
- **`p`** — the *retain* ratio throughout. "Drop ratio" is `1 − p`.

## Connections

It analyses the inverted form of dropout from Srivastava et al. ([LIT-395](../literature.d/LIT-395.md)) and
the moving statistics of batch normalization ([LIT-002](../literature.d/LIT-002.md)). The paper builds Uout
from [LIT-395](../literature.d/LIT-395.md)'s Gaussian multiplicative variant, swapping the Gaussian for a
bounded uniform. It gives an account of why Wide ResNet's dropout helps where
DenseNet's and ResNeXt's do not, which Zagoruyko and Komodakis reported without
explaining.

## Recommendations

- **R1** — In a network with BatchNorm, don't put dropout where a BN layer
  will normalize its output. *Topic:* model-stability. *Status:* standard.
  *Strength:* strong for avoiding the damage. *Applies when:* BN uses stored
  moving statistics at inference.
- **R2** — If dropout is wanted, put it after the last BN, i.e. before the
  classifier. *Topic:* model-stability. *Status:* standard. *Strength:* weak for
  the gain, which is about 0.2 top-1. *Applies when:* the model is overfitting
  enough to want dropout at all ([SOTA-240](../practices.d/SOTA-240.md)).
- **R3** — If a model already has dropout upstream of BN, re-estimate the BN
  statistics in eval mode on training data before evaluating. *Topic:*
  model-stability. *Status:* experimental. *Strength:* moderate, since Table 3
  improves every cell. *Applies when:* retraining is not an option. It recovers
  much of the loss, not all of it.

## Bearing on the record

- **Sources `SOTA-427`** (R1 and R2), filed `Proposed` with
  `consensus: unreplicated`. The practice is stated so it rests on C1–C2, and
  it says that C4 is small. It extends [SOTA-240](../practices.d/SOTA-240.md): this is where to put dropout
  once that practice says to use it.
- **[SOTA-005](../practices.d/SOTA-005.md)** ("Use running statistics for inference") gains a cause it does
  not list. Its subtle direction is statistics that go stale because the data
  moved. Here they are wrong on the training data itself, because dropout
  changed the network between accumulating them and using them. R3 is the same
  repair [SOTA-005](../practices.d/SOTA-005.md) implies, updating the statistics. It is **not** edited here.
  The practice cross-references it instead, and whether [SOTA-005](../practices.d/SOTA-005.md) should name
  this case is left to whoever next revises it.
- **[SOTA-240](../practices.d/SOTA-240.md)** is not contradicted. Wide ResNet's benefit from bottleneck dropout
  is another data point on that practice's "can memorize" side, a 36M-parameter
  model on 50k images. This paper adds that architecture decides whether that
  benefit survives BN.
- **[THEORY-016](../theory.d/THEORY-016.md)** is not touched. This paper takes the geometric-mean reading
  of test-time scaling for granted and is about the *variance*, which that
  account does not address.

## Limitations

- Everything is image classification with BN, mostly CIFAR. The largest effects
  are CIFAR only. No run is on a model without stored normalization statistics.
- Tables 3–6 report means of 5 seeds and no spread. At 0.1–0.3 points that
  matters.
- The case-(b) derivation's assumptions (linear regime, one shared `ρ`,
  constant weights) are not checked. Its predictions are.
- The paper does not compare dropout after the last BN against Uout at matched
  settings, so which remedy is better is not shown.
- The "code would be released soon" note is in v1. No code is cited here.

## Open questions

- Does the mismatch arise, and matter, with GroupNorm or with BN in train mode
  at test time? The mechanism predicts it does not, and nothing here tests
  that.
- Is the relocated dropout worth anything once the other regularizers of a
  modern recipe are present (stochastic depth, mixup, label smoothing)? A
  controlled run with those on would settle the size of C4.
