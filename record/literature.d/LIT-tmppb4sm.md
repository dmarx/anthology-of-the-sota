---
status: Active
title: 'ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation'
version: 1
tags:
- adaptation-and-tuning
- analysis-and-evaluation
- generative-modeling
date: '2026-10-03'
published: '2023-04-12'
arxiv: '2304.05977'
first_author: 'Xu'
keywords:
- 'imagereward'
- 'reward-model'
- 'human-preference'
- 'refl'
- 'reward-feedback-learning'
- 'text-to-image-evaluation'
- 'best-of-n'
implementations: []
extends:
- LIT-377
compared_against:
- LIT-588
- LIT-tmpznned
- LIT-tmpdktqx
summary: >-
  Xu, Liu, Wu, Tong, Li, Ding, Tang and Dong, Tsinghua, Zhipu AI and BUPT
  (2023), [ARXIV-2304.05977](https://arxiv.org/abs/2304.05977). A reward model for text-to-image preference: a BLIP
  backbone trained on 136,892 ranked pairs over 8,878 DiffusionDB prompts.
  It picks the rater's choice 65.14% of the time, against 54.82% for CLIP
  similarity, about as often as one annotator agrees with another (65.3%).
  ReFL, added in v3, backpropagates the reward through one denoising step
  taken late in the chain. On Stable Diffusion v1.4 it is ranked over the
  base model 58.79% of the time, ahead of filtering, reward weighting and
  RAFT. Best-of-64 under the same reward reaches 73.33%. Its premise, that a
  diffusion model has no likelihood for RLHF to use, is true of the whole
  chain and not of a step.
---

# LIT-tmppb4sm: ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation

Xu, Liu, Wu, Tong, Li, Ding, Tang and Dong, Tsinghua University, Zhipu AI
and Beijing University of Posts and Telecommunications (2023) —
[ARXIV-2304.05977](https://arxiv.org/abs/2304.05977). NeurIPS 2023. Read at v4 (28 Dec 2023), appendices A–J
included. v1 (12 Apr 2023) is the reward model alone. ReFL and the
comparison with HPS and PickScore (App. D) are in v3 (6 Jun 2023), which
was checked for both.

## Key takeaways

- **The data is real prompts, ranked by trained annotators** (§2.1,
  App. A–B). A graph-based selection over Sentence-BERT embeddings picked
  10,000 diverse prompts from DiffusionDB, each with 4–9 of its images.
  Annotators rated every image on three seven-point scales (overall,
  alignment, fidelity), ticked problem boxes, then ranked the images into
  five slots with at most two per slot. Two months gave 8,878 prompts and
  136,892 pairs. The guideline puts fidelity and harmlessness ahead of
  alignment "in most cases" (App. B). Each prompt had one annotator plus a
  quality inspector (App. H). Body problems were flagged on 21.14% of
  images, the most common fault (App. A.4).
- **The model** (§2.2, §4.1). A BLIP backbone, ViT-L for images and a
  12-layer text encoder with cross-attention, feeds an MLP that outputs a
  scalar. The loss is −log σ(f(x_i) − f(x_j)) over every pair from a ranked
  list (Eq. 1). It overfits fast. Freezing 70% of the transformer layers,
  learning rate 10⁻⁵ and batch 64 gave the best accuracy.
- **It agrees with raters about as often as raters agree** (Tables 2a, 3,
  5). On a held-out 466 prompts and 6,399 pairs, ImageReward picks the
  preferred image 65.14% of the time, BLIP similarity 57.76%, the LAION
  aesthetic predictor 57.35% and CLIP similarity 54.82%. In App. D, HPS
  scores 60.79% and PickScore 62.78%. On a separate 40 prompts, one
  annotator agrees with another 65.3% of the time and one researcher with
  another 71.2%. A CLIP backbone trained the same way reaches 62.98%
  (Table 2b). BLIP's accuracy grows from 63.07% at 1k training prompts to
  65.14% at 8k.
- **As a metric it ranks models the way people did** (§2.3, Table 1).
  Six models generated 10 images for each of 100 real prompts, and the
  authors ranked the best image from each model. ImageReward's ranking of
  the models matches theirs exactly (Spearman 1.00); CLIP similarity's
  gives 0.60. On MS-COCO, ImageReward gives 0.77 and zero-shot FID 0.09.
- **As a selector it beats the alternatives** (Fig. 5). Top three of 9, 25
  or 64 images, ranked by three annotators: ImageReward's picks win 77.1%
  against random picks, 69.3% against CLIP's, 69.8% against the aesthetic
  predictor's and 65.8% against BLIP's.
- **ReFL backpropagates the reward through one late step** (§3, Alg. 1,
  Eq. 2). Sample without gradients down to a random step t, take one
  denoising step with gradients, predict x'_0 from it in one shot, decode
  and score it, and descend λφ(r). Alternate with the ordinary denoising
  loss on a 625K LAION aesthetic subset. The motivation is Fig. 4: the
  one-shot x'_0 prediction's ImageReward separates good from bad seeds after
  about 30 of 40 steps. Gradients from the last step alone were "very
  unstable". Settings (§4.2): SD v1.4, learning rate 10⁻⁵, batch 128 split
  evenly, φ = ReLU, λ = 10⁻³, T = 40.
- **ReFL against the other ways to use a reward** (§4.2, Table 4, Fig. 6).
  Each method got Stable Diffusion v1.4, ImageReward, 20,000 samples, one
  epoch and the same learning rate and batch. People ranked the outputs
  for 466 DiffusionDB prompts and 90 MT-Bench prompts. Win rates against
  the base: ReFL 58.79% and 58.49%; dataset filtering 55.17% and 51.72%;
  reward weighting 39.52% and 43.33%; RAFT 49.86% and 42.31% after one
  iteration, 20.97% and 26.19% after three. ReFL wins every pairwise
  comparison.
- **Picking from 64 samples beats ReFL** (App. D, Table 6). Ranked against
  the base on real prompts, best-of-64 under ImageReward wins 73.33% and
  ReFL with ImageReward 58.38%. ImageReward's mean score is 0.1058 for the
  base, 0.6072 after ReFL and 1.3374 for best-of-64. ReFL on HPS and
  PickScore wins 52.86% and 56.91%.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Outperforms … CLIP (by 38.6%), Aesthetic (by 39.6%), and BLIP (by
  31.6%)"** (§1) is not preference accuracy, where the gaps are 10.3, 7.8
  and 7.4 points. Each figure equals twice Fig. 5's average win rate minus
  100: a selection margin in a human ranking, never defined in the text.
- **The test set is its own.** The 65.14% comes from the same pipeline,
  restricted to annotators who agreed more with the researchers. HPS and
  PickScore were trained elsewhere and tested here. The margin over
  PickScore is 2.4 points on ImageReward's home ground.
- **Spearman 1.00 is six models,** ranked by "researcher annotation (i.e.,
  by authors)" — "by 3 authors" in v1. The FID column mixes sources:
  DALL·E 2's is taken from its paper.
- **The ReFL step range is stated two ways.** §3 says gradients go to "a
  randomly-picked latter step t (in our case t ∈ [30, 40])". §4.2 sets
  [T1, T2] = [1, 10]. These may count from opposite ends; the paper does not
  say. φ = ReLU is given without its argument, so the sign and offset of the
  loss cannot be recovered from the text.
- **"Cannot yield likelihoods"** (§3) is ReFL's premise for not using RLHF
  directly. It holds for the image's marginal likelihood and not for a step.
  With a stochastic sampler each step is a Gaussian with an exact
  likelihood, which DDPO ([LIT-tmp7vihu](LIT-tmp7vihu.md)) and DPOK ([LIT-tmp9ntgf](LIT-tmp9ntgf.md)), both
  submitted in May 2023, used for policy gradient. "The first direct tuning
  method" (§5) is a priority claim the paper does not support.
- **ReFL has no KL anchor and no diversity measure.** Its regularizer is
  the pre-training loss. Its gains are judged by people, but App. H calls
  ReFL "an approximation of original RLHF algorithms", and the paper does
  not say who ranked the ReFL outputs. Its human evaluation is described as
  "consistent with Section 2.3", whose rankers were the authors.
- **Two numbers for one comparison.** ReFL with ImageReward against the base
  on real prompts is 58.79% in Table 4 and 58.38% in Table 6. The text does
  not say why.

## Which comparisons are like for like

- **Reward models (Tables 3, 5)** are scored on ImageReward's test set.
  CLIP, BLIP and the aesthetic predictor are zero-shot. HPS and PickScore
  were trained on other data.
- **ReFL against the other tuning methods (Table 4)** shares the base model,
  the reward, 20,000 samples, one epoch and the learning rate and batch
  (App. E). The data does not match. RAFT generates 100,000 images per
  iteration. Reward weighting needed ImageReward min-max normalized into
  [0, 1] to reproduce its weights, with β = 0.5, on prompts unlike the ones
  its authors used. ReFL also uses the reward's gradient, which no baseline
  does.
- **Best-of-64 against ReFL (Table 6)** is 64 samples at inference against
  one.
- **Table 1's FID** is computed at 256 px on MS-COCO 2014 with each model's
  guidance chosen by grid search, except DALL·E 2's, which is quoted.

## Standing in the anthology

It extends InstructGPT ([LIT-377](LIT-377.md)) through the reward model, trained "similar
to RM training for language model of previous works": rank several outputs
for one prompt and fit every pair from the ranking with a Bradley–Terry loss
(Eq. 1). The labelling guide follows InstructGPT's as well. It ranks
fidelity and harmlessness above alignment as InstructGPT ranked truthfulness
and harmlessness above helpfulness, and its second rule still says
"truthfulness and harmlessness" (App. B).

It compares itself against CLIP ([LIT-588](LIT-588.md)) twice. As a judge, CLIP
image-text similarity predicts the raters' choice 54.82% of the time, the
lowest of the scorers tested, and its ranking of six models agrees with
the authors' at Spearman 0.60. As a backbone, CLIP fine-tuned the same way
reaches 62.98%, below BLIP. The paper puts the gap down partly to BLIP's
bootstrapped training data and its image-grounded text encoder.

It compares ReFL against Lee et al. ([LIT-tmpznned](LIT-tmpznned.md)), reimplemented as
"Reward Weighted" on open prompts. That method fell below the untuned
model. The authors blame weights confined to [0, 1], which keep the
influence of non-preferred images. Their reimplementation also changed the
reward and the prompts, so the test is of the objective, not the paper.

Later work used it as the reward. DPOK ([LIT-tmp9ntgf](LIT-tmp9ntgf.md)) trains on it and
checks it on its own labels (its App. C), where CLIP is ahead only on
location prompts. DDPO ([LIT-tmp7vihu](LIT-tmp7vihu.md)) uses it in its comparison with DPOK.
Flow-GRPO ([LIT-tmpdktqx](LIT-tmpdktqx.md)) reports it as a quality metric and runs ReFL as a
baseline on SD3.5-M with PickScore, where Flow-GRPO comes out ahead (its
Fig. 8). The base model is Stable Diffusion v1.4, from the latent diffusion
line ([LIT-062](LIT-062.md)).

ReFL is the reward-gradient family that [THEORY-tmpr00tj](../theory.d/THEORY-tmpr00tj.md) sets aside. A
likelihood-ratio gradient needs a density for each step and only the
reward's value. ReFL needs no density and the reward's gradient instead.
DPOK calls backpropagating through the whole chain memory-inefficient and
prone to numerical instability (its §4.1). ReFL sidesteps that by taking
the gradient through one step and predicting the image from it.

Filed without a `NOTE`. The takeaways come from one full reading of v4,
appendices included, done for this filing. v1 and v3 were checked for
what each added. Figure values are quoted only where the text, a table or
a figure label gives them.
