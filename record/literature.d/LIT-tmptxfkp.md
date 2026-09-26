---
status: Active
title: 'Score-Based Generative Modeling through Stochastic Differential Equations'
version: 1
tags:
- generative-modeling
- inference-optimization
- analysis-and-evaluation
date: '2026-09-26'
published: '2020-11-26'
arxiv: '2011.13456'
first_author: 'Song'
keywords:
- 'score-based'
- 'reverse-time-sde'
- 'probability-flow-ode'
- 'predictor-corrector'
- 'controllable-generation'
implementations:
- 'NCSN++'
- 'DDPM++'
- 'score_sde'
summary: >-
  Song, Sohl-Dickstein, Kingma, Kumar, Ermon and Poole (2020),
  [ARXIV-2011.13456](https://arxiv.org/abs/2011.13456). The framework this record has been standing on without
  holding. **Classifier guidance is Eq. 14 here, six months before ADM**: the
  conditional reverse-time SDE adds `∇ₓ log pₜ(y|x)` to the unconditional score,
  and §5 gives the recipe for the noise-conditioned classifier that supplies it —
  sample `(x(0), y)`, noise it through the tractable forward SDE, train with a
  mixture of cross-entropy losses over timesteps. Also the probability flow ODE
  with exact likelihoods, predictor-corrector sampling, CIFAR-10 IS **9.89** /
  FID **2.20** / 2.99 bits/dim, and the first 1024×1024 samples from a score
  model. Its §I.2 imputation approximation is the "replacement" [SOTA-397](../practices.d/SOTA-397.md) exists
  to reject.
---

<!-- inactive-ok-file: SOTA-397, SOTA-412, SOTA-428 — all three Proposed, and none of them is support for anything this note claims. SOTA-397 is named because this paper is where the approach that practice *rejects* comes from, so a not-in-force rejection is exactly the right thing to point at. SOTA-412 and SOTA-428 appear in the list of what the paper's own closing limitation — sampler hyper-parameter proliferation — has since turned into work here; they are cited as instances of that programme, not as settled accounts. -->

# LIT-tmptxfkp: Score-Based Generative Modeling through Stochastic Differential Equations

Song, Sohl-Dickstein, Kingma, Kumar, Ermon and Poole (2020) —
[ARXIV-2011.13456](https://arxiv.org/abs/2011.13456)

## Key takeaways

- **The framework: one reverse-time SDE, and SMLD and DDPM are both special
  cases of it.** A forward SDE injects noise until the data reaches a tractable
  prior; the reverse-time SDE "depends only on the time-dependent gradient field
  (a.k.a., score) of the perturbed data distribution". Song & Ermon's
  score-matching-with-Langevin and Sohl-Dickstein/Ho's denoising diffusion are
  discretizations of the same object, which is what makes the rest of this
  record's diffusion vocabulary — VE, VP, sub-VP, probability flow — mean
  anything.
- **Classifier guidance, stated generally, in November 2020.** §5 gives the
  conditional reverse-time SDE:

      dx = {f(x,t) − g(t)²[∇ₓ log pₜ(x) + ∇ₓ log pₜ(y|x)]}dt + g(t)dw̄

  The conditional score is the unconditional score plus the gradient of the
  condition's log-likelihood. That is the whole of what later gets called
  classifier guidance, and everything in this record's guidance cluster is a
  special case, a scaling of, or an argument about the second term.
- **And the recipe for the noise-conditioned classifier.** "Since the forward
  SDE is tractable, we can easily create training data `(x(t), y)` … by first
  sampling `(x(0), y)` from a dataset, and then sampling `x(t) ∼ p₀ₜ(x(t)|x(0))`.
  Afterwards, we may employ a mixture of cross-entropy losses over different time
  steps." ADM's "we train these classifiers on the same noising distribution as
  the corresponding diffusion model" is this, at ImageNet scale.
- **The conditioning is not restricted to classifiers, and the paper says so.**
  Eq. 14 solves "a large family of inverse problems … once given an estimate of
  the gradient of the forward process". You can train a model for
  `log pₜ(y|x(t))`, or "estimate the gradient with heuristics and domain
  knowledge", and §I.4 gives a method needing no auxiliary model at all. Three
  applications are demonstrated: class-conditional generation, inpainting,
  colorization.
- **The imputation approximation that [SOTA-397](../practices.d/SOTA-397.md) rejects, exactly.** §I.2 wants
  `pₜ(z(t) | Ω(x(0)) = y)`, calls it "in general intractable", and approximates

      pₜ(z(t)|A) = 𝔼[pₜ(z(t)|Ω(x(t)), A)] ≈ 𝔼[pₜ(z(t)|Ω(x(t)))]

  dropping the conditioning on the *exact* known values at `t = 0` and keeping
  only the *noised* known dimensions at time `t`. That dropped term is the whole
  disagreement: it is why splicing noised known pixels into each step is not the
  same as conditioning on them, and why VDM's reconstruction guidance beats it
  136 FVD to 451.
- **Predictor-corrector sampling.** Take a step with a numerical SDE solver
  (predictor), then correct with score-based MCMC at that noise level
  (corrector), because a discretized reverse SDE accumulates error the score
  function can be used to fix. The record's later sampler practices are about
  higher-order deterministic solvers instead; this is the stochastic branch.
- **The probability flow ODE, which is where exact likelihoods come from.** An
  ODE sampling the same distribution as the SDE, enabling exact likelihood
  computation and "uniquely identifiable encoding". This is the object
  `SOTA-203`'s higher-order solvers integrate and `SOTA-412`'s likelihood targets
  are measured against.
- **Results.** CIFAR-10 unconditional: Inception score **9.89**, FID **2.20**,
  and a competitive **2.99 bits/dim** — records at the time — plus "high fidelity
  generation of 1024×1024 images for the first time from a score-based
  generative model".
- **The limitation it names, which the record has since been working through.**
  "The breadth of samplers one can use when given access to score functions
  introduces a number of hyper-parameters. Future work would benefit from
  improved methods to automatically select and tune these." Everything from
  `SOTA-203` and `SOTA-410` to `SOTA-416`'s timestep spacing and `SOTA-428`'s
  post-hoc EMA is that sentence being worked on.

## Standing in the anthology

Filed because the record was citing it as an authority three times without
holding it, which is the same defect the last three units closed:

| site | what it leaned on this paper for |
| --- | --- |
| `NOTE-358` | the guidance formula `ε − √(1−ᾱₜ)∇log p(y\|xₜ)`, "adapted from Song et al." |
| `NOTE-347` | "reconstruction guidance corrects the imputation approach of Song et al.'s SDE paper" |
| `NOTE-067` | the record's SDE framing, via "Song et al.'s *Score-Based…*" |

Sixteen documents name score-based modelling, probability flow or reverse SDEs.
Sohl-Dickstein et al. (`LIT-439`) was held; this was not.

What it supplies:

- the antecedent of `LIT-699`'s classifier guidance, in that paper's own words —
  a "score-based conditioning trick adapted from Song et al." and prior work that
  "uses a classifier to generate class-conditional CIFAR-10 images with a
  diffusion model";
- the source of the **replacement** approach `SOTA-397` is about, which that
  practice previously rejected without naming where it came from;
- a resolvable code for the three notes above.

**It does not supply a new practice or theory, and that is deliberate.** The
conditional-score decomposition is a derivation, not a contested explanation, so
filing a `THEORY` for it would be filing on novelty rather than on a defect —
the same call made about EDM2's magnitude-preserving layers. Predictor-corrector
sampling is a real recommendation but the record's sampler practices
(`SOTA-203`, `SOTA-410`, `SOTA-416`) are about the deterministic branch, and this
paper is not a controlled comparison against them. What this note does is put a
floor under documents that were already standing on it.
