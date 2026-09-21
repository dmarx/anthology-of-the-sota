---
number: 240
status: Read
formerly:
- NOTE-tmptc2jq
paper: LIT-491
title: 'Noise hypernetworks'
version: 1
date: '2026-09-21'
summary: >-
  Read as the amortized counterpart to `SOTA-301`. The headline — recover half
  of test-time optimization at 1/100th the latency — is well measured. The
  finding that carries further is the control: direct reward fine-tuning of
  the same model makes it worse, and worse the more steps you sample.
---

<!-- inactive-ok-file: SOTA-301 — Proposed, and cited throughout as the other
     side of a trade rather than as support: it is the inference-time route,
     this is the amortized one, and the comparison is between their cost
     profiles. A contrast does not wait on the contrasted document being
     settled, and both carry the same `unreplicated` standing -->

# NOTE-240: Noise hypernetworks

## Contribution

Test-time scaling in diffusion works and is unusable: reward-guided noise
optimization buys a large quality gain and costs 20–40 seconds a sample. This
asks whether the *knowledge* that optimization discovers can be moved into a
one-time post-training stage, and answers with a lightweight network that
predicts the optimized noise in a single forward pass.

What is true afterwards that was not before: the reward-tilted distribution
for a **step-distilled** generator can be learned with a tractable
regularizer, by adapting the input noise rather than the model — and the
obvious alternative, fine-tuning the generator against the same reward,
actively degrades it.

## Key insight

**Move the adaptation to where the regularizer is computable.**

The target is the tilted distribution `p* ∝ p(x)·exp(r(x)/λ)` — upweight high
reward, stay near the base model. The staying-near term is the whole game: a
reward with no anchor produces reward-hacking, superficially high scores off
the data manifold. For a distilled one-step generator, that KL needs Jacobian
determinants through the generator and is intractable.

But the generator is a fixed map from noise to image. So instead of asking
which *model* produces the tilted output distribution, ask which *noise
distribution* does — and regularize there. In noise space the base
distribution is a standard Gaussian, the change of variables plus Stein's
lemma reduces the KL to `½‖Δ(ε)‖²` under a Lipschitz condition, and the data
processing inequality guarantees it upper-bounds the data-space divergence
you could not compute.

That is the paper: a reparameterization that makes the regularizer exist.

## Assumptions

- **A step-distilled generator**, one to four steps. The method targets these
  explicitly because they are cheap enough to backpropagate through during
  training.
- **A differentiable reward.** Here an ensemble — ImageReward, HPSv2.1,
  PickScore, CLIP-score — with ReNO's own weights, so the reward is held
  identical to the baseline it is compared against.
- **The log-determinant approximation** holds when the modulation's Lipschitz
  constant is small; Theorem 1 bounds the error and the implementation keeps
  it small by initializing the modulation to exactly zero.
- Training needs no data samples: only base noise, the frozen generator, the
  reward, and conditions.

## Key results

**GenEval, base → HyperNoise (ReNO for reference):**

- SD-Turbo **0.49 → 0.57** (ReNO 0.63). 0.2 s → 0.3 s against ReNO's 20 s.
- SANA-Sprint **0.70 → 0.75** (ReNO 0.81, best-of-N 0.79, prompt
  optimization 0.75). 0.2 s → 0.3 s against 30 s.
- FLUX-schnell **0.68 → 0.72** (ReNO 0.76). 0.7 s → 0.9 s against 40 s.
- **33×–300× faster** than the test-time methods.

**The direct-fine-tuning control, which is the load-bearing one:** on
SANA-Sprint, LoRA reward fine-tuning gives **0.67 / 0.66 / 0.62** at one, two
and four steps against a base of 0.70 / 0.72 / 0.73. It is worse than doing
nothing and gets worse with more steps. At lower LoRA rank it collapses
further — rank 8 gives 0.59.

**Where it stops working:** the gain decays with NFEs — 8-step 0.74 → 0.76,
16-step 0.73 → 0.75, 32-step 0.71 → 0.72.

**Corroborated on two more benchmarks** (T2I-CompBench, DPG-Bench) with the
same direction and smaller margins.

## Claims

**Well supported:** that a noise hypernetwork recovers a substantial fraction
of test-time optimization's gain at negligible inference cost. Three base
models spanning 0.6B to 12B, three benchmarks, the reward held identical to
the baseline's, and latency reported rather than FLOPs.

**Well supported and stated with unusual restraint:** "about half of the
performance gains achieved by ReNO". The numbers give 0.05 of 0.11 on
SANA-Sprint. A paper wanting a bigger number could have quoted the SD-Turbo
row, where 0.57 beats SDXL at 2× the parameters — and it does mention that,
without leaning on it.

**The finding most likely to matter elsewhere, and it is a negative:** direct
reward fine-tuning degrades the model. Not "helps less" — **worse than the
untouched base**, monotonically worse with sampling steps, worse at lower
adapter rank. That is a strong, controlled result about where reward
adaptation should be applied, and it is reported as a baseline rather than
framed as the contribution.

**Proved under a condition the implementation then engineers for:** the
log-determinant approximation needs a small Lipschitz constant, and the
modulation is initialized to output exactly zero so the condition holds at
the start of training. That is honest and it is also the assumption doing the
work — nothing verifies it *stays* small.

**Not tested:** whether the amortized policy generalizes off the reward it
was trained against. The hypernetwork learns one reward ensemble's tilt; what
happens under a different reward at inference is not examined.

## Method

Characterize the tilted noise distribution whose pushforward through the
frozen generator is the tilted data distribution; derive the noise-space KL
and approximate it as an `L2` penalty under a Lipschitz bound; parameterize
the modulation as LoRA over the generator's own architecture, initialized to
zero; train by reward maximization plus that penalty; evaluate on GenEval,
T2I-CompBench and DPG-Bench against test-time baselines and direct
fine-tuning.

## Connections

- [SOTA-301](../practices.d/SOTA-301.md) and [LIT-490](../literature.d/LIT-490.md) are the opposite side of the same
  decision — steer the sampler at inference with a correctly-ordered gradient
  step, paying per sample. Declared `compared_against` on the literature note.
  Neither dominates: that one needs no training and costs every sample, this
  one costs a training run and almost nothing after.
- [SOTA-184](../practices.d/SOTA-184.md) — adapt with a low-rank update rather than the matrix — is
  the mechanism, applied to an unusual target. The adapter here produces the
  generator's *input*, which is precisely what makes the regularizer
  tractable.
- [SOTA-187](../practices.d/SOTA-187.md) — train in a learned compressed latent — is the other
  practice in the record that gets its benefit from choosing which space to
  work in.

## Bearing on the record

One practice and one theory, and a trade the record can now state from both
sides. `SOTA-301` was filed an hour ago as the inference-time route with no
amortized counterpart in the corpus; this supplies it with numbers, so the
choice between paying per sample and paying once is a decision someone can
actually make.

## Limitations

**One modality, one task family.** Text-to-image, three distilled models. The
noise-space argument is general in principle and untested outside it.

**Few-step only, and the paper shows the decay** rather than leaving it to be
discovered. Past roughly eight NFEs there is little left to recover.

**It recovers half, not all.** If quality matters more than latency, the
test-time method is still better, and the paper does not claim otherwise.

**Reward-specific.** Trained against one ensemble; transfer to a different
reward is unexamined.

**"Recovers most of the improvements" for SD-Turbo** is the one place the
prose runs slightly ahead of the table — 0.57 against a 0.49→0.63 range is
about 57%, which is "most" only generously. The SANA-Sprint phrasing is
precise.

## Open questions

- Does the noise-space regularizer work for non-distilled multi-step models,
  where the initial noise has less leverage over the output?
- How far does an amortized tilt transfer across rewards, and can one
  hypernetwork carry several?
- Why does direct fine-tuning get *worse* with more sampling steps? The paper
  demonstrates it cleanly and offers manifold divergence as the explanation
  without isolating it.
