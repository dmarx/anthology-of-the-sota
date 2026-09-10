---
number: 1
status: Read
formerly:
- NOTE-tmp6zoh6
paper: LIT-025
title: 'Understanding and Improving Layer Normalization'
version: 1
tags:
- model-stability
date: '2026-09-09'
published: '2019-11-01'
summary: >-
  LayerNorm's benefit is in the backward pass — the derivatives of the mean and variance re-center and re-scale the gradients — not in forward normalization. Its bias and gain increase overfitting risk and "do not work in most cases".
---

# NOTE-001: Understanding and Improving Layer Normalization

## Contribution

LayerNorm was known to work and not known to work *why*; the standing
explanation was forward normalization, i.e. that controlling the
distribution of a layer's inputs is what buys the stability. This paper
tests that by **detaching** the derivatives of the mean and variance —
keeping the forward computation identical and removing only its
contribution to the backward pass — and shows the benefit largely goes with
them. It then finds, against its own expectation, that LayerNorm's learnable
bias and gain hurt: removing both outperforms keeping them on four datasets.
It proposes AdaNorm to replace them.

## Key insight

Normalization layers are usually explained by what they do to the forward
signal, and that explanation is at best incomplete for LayerNorm. The mean
and variance are *functions of the activations*, so differentiating through
them changes the gradient — re-centering it to zero mean and shrinking its
variance by `1/σ²`. That gradient normalization is the mechanism. Once you
see it that way, the learnable gain and bias look like what they are: extra
parameters attached to a forward transformation that was not the point,
which is why they add capacity to overfit and little else.

## Assumptions

An empirical and analytical paper; the theorems are algebraic identities
about gradients rather than convergence results, so they carry almost no
assumptions. What limits the conclusions is the setting:

- **Theorems 1 and 3** assume only that the loss is differentiable and
  LayerNorm is applied as defined. No smoothness, variance or data
  assumptions. They are exact statements, not bounds.
- **Theorem 2** assumes `φ(yᵢ)` derivable, `(1/H)Σφ(yᵢ) = C > 0`, and the
  transformed output bounded in mean: `|(1/H)Σzᵢ| < M`. Its conclusion is a
  uniqueness result under exactly those three requirements.
- **Empirically: 2019-era sequence models.** Machine translation (including
  En-Vi), language modelling and classification tasks — RNNs and the
  original Transformer. Not decoder-only language models, not at scale, not
  with the pretraining mixes the record's practices assume. The overfitting
  claim in particular is a small-data claim, and its transfer to a
  trillion-token regime is untested.

## Key results

- **Theorem 1** — For `∂ℓ/∂y = (g₁…g_H)` with mean `ḡ` and variance `D_g`,
  detaching the derivatives of `μ` and `σ` gives a gradient `∂ℓ/∂x` with
  mean `ā = ḡ/σ`. Under LayerNorm-simple (derivatives attached) the mean is
  **`d̄ = 0`** and the variance **`D_c = D_g/σ²`**.
  *So:* the derivative of `μ` **re-centers** the gradient to zero mean; the
  derivative of `σ` **re-scales** it, reducing its variance. Together the
  paper calls this *gradient normalization*, and it is the paper's
  explanation of LayerNorm.
- **Theorem 2** — Under the three requirements above, `φ(yᵢ) = C(1 − k·yᵢ)`
  is the **unique** solution. This is what fixes AdaNorm's form rather than
  leaving it a design choice; `φ(yᵢ) > 0` then requires `|yᵢ| < 1/k`, which
  Chebyshev bounds.
- **Detaching experiment** — removing only the backward contribution, with
  the forward pass untouched, degrades performance. This is the load-bearing
  empirical result, because it isolates the backward pass as the mechanism.
- **LayerNorm-simple** (bias and gain removed) beats LayerNorm on **four**
  datasets and reaches **state of the art on En-Vi** machine translation.
- **AdaNorm** beats LayerNorm on **seven of eight** datasets.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | LayerNorm's benefit comes from the derivatives of the mean and variance, not from forward normalization | strong | Theorem 1 gives the exact gradient identities; the detaching experiment isolates the effect |
| C2 | The derivative of `μ` re-centers the gradient and the derivative of `σ` re-scales it | strong | Theorem 1, exact — `d̄ = 0`, `D_c = D_g/σ²` |
| C3 | The learnable bias and gain increase the risk of over-fitting and do not help in most cases | moderate | four datasets where removal wins; the authors call it "beyond our expectation" |
| C4 | Removing them outright is a viable and sometimes better design | moderate | LayerNorm-simple, state of the art on En-Vi |
| C5 | `C(1 − k·y)` is the only transformation satisfying the three stated requirements | strong | Theorem 2, a uniqueness proof — but the requirements are the paper's own choice |
| C6 | AdaNorm improves on LayerNorm generally | moderate | seven of eight datasets, one group, 2019 architectures |

## Concepts

- **Gradient normalization** — the paper's name for the combined effect in
  Theorem 1: the backward re-centering and re-scaling that differentiating
  through `μ` and `σ` produces. Coined here; not the same as gradient
  clipping or normalized gradient descent.
- **Detaching** — computing `μ` and `σ` in the forward pass but treating
  them as constants in the backward pass. The paper's central experimental
  instrument, and the thing that makes C1 testable at all.
- **LayerNorm-simple** — LayerNorm with the bias and gain removed; the
  normalization only.
- **AdaNorm** — bias and gain replaced by `φ(y) = C(1 − k·y)` applied to the
  normalized output, so the scaling adapts to the input instead of being
  learned as a free parameter.

## Connections

Directly extends Ba et al. ([LIT-005](../literature.d/LIT-005.md)), which introduced LayerNorm and gave
each neuron "its own adaptive bias and gain" without arguing for the
parameters or stating an initialisation. This paper is the first in the
record to ask whether they earn their place, and answers no.

The obvious comparison is RMSNorm ([LIT-023](../literature.d/LIT-023.md)), published the same year, which
also concludes that part of LayerNorm is unnecessary — and picks the **other
part**. RMSNorm drops the re-centering and keeps the gain; this paper keeps
the normalization whole and drops the gain and bias. Both claim a
simplification, they are not the same simplification, and the field adopted
RMSNorm's.

## Recommendations

- **R1** — Do not assume a normalization layer works by controlling the
  forward distribution. *Topic:* normalization. *Status:* standard.
  *Strength:* strong. *Applies when:* reasoning about why a normalization
  helps, or designing a replacement for one.
- **R2** — Consider removing LayerNorm's learnable gain and bias rather than
  tuning them. *Topic:* normalization. *Status:* experimental. *Strength:*
  moderate. *Applies when:* the setting resembles the paper's — moderate
  data, where overfitting is the binding constraint.
- **R3** — Use detaching as an instrument. *Topic:* methodology. *Status:*
  experimental. *Strength:* moderate. *Applies when:* you need to separate a
  component's forward contribution from its backward one; it generalises well
  past normalization.

## Bearing on the record

**Contradicted all three practices that cited it.** [SOTA-025](../practices.d/SOTA-025.md), [SOTA-026](../practices.d/SOTA-026.md) and
<!-- inactive-ok-block: SOTA-027 — Rejected in #114; this paragraph is the record of why -->
[SOTA-027](../practices.d/SOTA-027.md) each recommend how to *set* the bias and gain — a 0.97–1.0
initialisation range, a zero bias, a reduced learning rate for both. C3 and
C4 are an argument for deleting those parameters. The paper contains the
string `0.97` **zero times** and `smaller learning rate` **zero times**.

<!-- inactive-ok-block: SOTA-027 — Rejected in #114; named as where the third practice went -->
`SOTA-025` and `SOTA-026` moved to [LIT-005](../literature.d/LIT-005.md), where the parameters are defined,
and `SOTA-027` is `Rejected`.

<!-- inactive-ok-block: SOTA-191 — Proposed; the practice this reading produced, and its status is the point -->
**Produces [SOTA-191](../practices.d/SOTA-191.md)** from R2 — `Proposed`, `contested_by: LIT-023`.
The contest is C4 against RMSNorm's opposite simplification.

**R1 bears on [SOTA-182](../practices.d/SOTA-182.md)** without contradicting it. That practice says the
re-scaling buys the stability and the re-centering is free to drop; C2 says
the re-centering does something specific and measurable to the gradient. Both
can hold — the question nobody in the record answers is whether what it does
is worth its cost.

## Limitations

- 2019 architectures and dataset sizes throughout. C3's overfitting argument
  is the claim least likely to survive to the scales the record cares about,
  since overfitting is not the binding constraint there.
- Theorem 2's uniqueness is uniqueness **given the paper's three
  requirements**, which are motivated but not derived. A different bounding
  requirement gives a different unique solution.
- The gain is what RMSNorm kept and what every model in this record uses.
  Whatever C3 established, the field did not act on it, and the paper cannot
  say why.
- No ablation separating the bias from the gain: they are removed together
  throughout, so C3 and C4 are about the pair.

## Open questions

<!-- inactive-ok-block: SOTA-191 — Proposed; named as the practice this open question would promote -->
- Does C3 hold at scale, where overfitting is not the constraint? A gain-free
  decoder-only model at contemporary size would settle it, and is
  [SOTA-191](../practices.d/SOTA-191.md)'s promotion condition.
- Bias or gain — which one carries the effect? Nobody has separated them.
- This paper and RMSNorm each drop a different half of LayerNorm and each
  report an improvement. Is there a model that drops **both** the centering
  and the gain, and what happens?
