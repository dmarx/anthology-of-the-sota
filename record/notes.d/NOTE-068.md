---
number: 68
status: Read
formerly:
- NOTE-tmpw3qeb
paper: LIT-036
title: 'Denoising Diffusion Probabilistic Models'
version: 1
tags:
- generative-modeling
date: '2026-09-09'
published: '2020-06-01'
summary: >-
  The paper that made diffusion work. Its Table 2 is the underquoted part: predicting ε rather than the posterior mean matters *only* under the simplified objective, learned reverse-process variances destabilise training, and the principled variational bound gives better codelengths while the unprincipled simplified loss gives better samples.
---

# NOTE-068: Denoising Diffusion Probabilistic Models

## Contribution

Diffusion models existed and did not produce good samples. This paper makes
them work, and the mechanism is a set of parameterisation choices rather than a
new model class: predict the **noise** `ε` instead of the posterior mean, use
**fixed** rather than learned reverse-process variances, and train on a
**simplified, unweighted** objective rather than the true variational bound.

It also establishes the equivalence that reframed the field: this
parameterisation is **denoising score matching over multiple noise levels**,
with sampling as annealed Langevin dynamics.

## Key insight

The best-performing objective is not the correct one, and the paper says so
plainly:

> training our models on the true variational bound yields better codelengths
> than training on the simplified objective, as expected, but the latter yields
> the best sample quality.

The simplified objective is the variational bound with its per-timestep
weighting dropped. Dropping the weighting downweights the low-noise terms
relative to their correct value, and that is what buys sample quality. So the
field's foundational result is a **deliberate mis-weighting of a principled
loss**, adopted because it works.

That single observation is the seed of everything downstream: EDM's `λ(σ)` is a
derivation of what the right weighting should be, and `SOTA-188` is the record's
statement of it.

## Assumptions

- Gaussian forward process with a **fixed** variance schedule — `L_T` is
  constant and drops out.
- Reverse-process variances fixed rather than learned. Table 2 says learning
  them "leads to unstable training and poorer sample quality".
- Images; CIFAR-10, CelebA-HQ and LSUN at 256×256, 2020 scale.

## Key results

- **FID 3.17** and Inception 9.46 on unconditional CIFAR-10 — state of the art
  at the time; LSUN 256×256 comparable to ProgressiveGAN.
- **Table 2, the ablation that matters.** Predicting `ε` performs *about as
  well* as predicting the posterior mean `μ̃` when trained on the variational
  bound with fixed variances, but **much better** under the simplified
  objective. The choice of prediction target is not independently good — it is
  good *in combination with* the loss.
- The baseline `μ̃` parameterisation "works well **only** when trained on the
  true variational bound", not under unweighted MSE.
- **Learned reverse-process variances destabilise training.**
- **Most of the model's lossless codelength describes imperceptible detail**
  (§4.3), analysed as lossy compression. Sampling is progressive decoding along
  a bit ordering that generalises autoregressive decoding.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Diffusion models can produce high-quality samples | strong | the demonstration; the paper's stated purpose |
| C2 | The ε-parameterisation is equivalent to multi-level denoising score matching | strong | derived |
| C3 | ε-prediction only outperforms μ̃-prediction under the simplified objective | strong | Table 2, both cells |
| C4 | Learned reverse variances hurt | strong | ablated |
| C5 | The principled objective and the best-sampling objective differ | strong | measured on both axes, and stated |
| C6 | Most codelength goes to imperceptible detail | strong | measured |

## Method

Fixed Gaussian forward schedule. Train a network to predict `ε` under the
unweighted simplified loss. Sample by iterated denoising with fixed variances.

## Concepts

- **ε-prediction** — the parameterisation, and the default everything since
  either uses or argues against.
- **The simplified objective** — dropping the weighting, deliberately.
- **Codelength on imperceptible detail** — C6 is the argument latent diffusion
  (`LIT-062`) later acts on: if most capacity describes what nobody sees, move
  the model somewhere that detail has been removed.

## Connections

`LIT-038` (DDIM) is the immediate successor and takes the sampler apart without
retraining; `LIT-067` shows ε-prediction becomes unstable at the low
signal-to-noise ratios few-step sampling lives at, and introduces
**v-prediction**; `LIT-075` (EDM) derives the preconditioning and the loss
weighting that this paper set by hand, and is the source of `SOTA-188`.

C6 is the premise `SOTA-187` rests on — most of a pixel-space model's capacity
goes to perceptually irrelevant detail — and this is where it is *measured*
rather than asserted. `LIT-062`'s reading records that claim as "the paper's
premise, supported by the compression working at all". It has a measurement,
here, two years earlier.

## Recommendations

- **R1** — Choose the prediction target and the loss weighting together; the
  ablation says they are not separable. *Topic:* generative modelling.
  *Strength:* strong.
- **R2** — Fix the reverse-process variances rather than learning them.
  *Strength:* strong for this setting.
- **R3** — When a principled objective and an empirical one disagree, report
  both metrics rather than picking the flattering one. *Topic:* analysis and
  evaluation. *Strength:* strong — this paper does exactly that and it is why
  the disagreement is known at all.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice** —
`SOTA-188` is correctly sourced to EDM, which derives what this paper fixed by
hand.

The reading supplies two things the record was carrying without provenance.
`SOTA-187` (train the generative model in a learned compressed latent) rests on
the claim that most capacity goes to imperceptible detail, which its own
source treats as a premise; **§4.3 here is the measurement.** And `SOTA-188`'s
whole subject — that the loss weighting across noise levels is a decision — is
visible here as the gap between the variational bound and the simplified
objective, three years before EDM closed it.

The document's takeaways are directionally right and generic, except that
"fixed noise schedule" names the *forward* schedule while the paper's more
consequential fixed quantity is the **reverse-process variance**, which is the
one that was ablated and the one that destabilises training when learned.

## Limitations

- 2020, images, CIFAR/LSUN scale.
- Sampling takes hundreds to thousands of steps — the defect the next four
  papers in this batch exist to remove.
- C5 is reported and not explained; why the mis-weighting helps is left open
  and stays open until EDM.

## Open questions

- The paper measures that the correct objective is not the best one and does
  not ask why. EDM answers it by deriving the weighting, but the general
  question — when is a principled loss the wrong loss? — is a good one and this
  is the cleanest instance of it in the corpus.
