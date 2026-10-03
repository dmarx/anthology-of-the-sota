---
status: Active
title: 'Aligning Text-to-Image Models using Human Feedback'
version: 1
tags:
- adaptation-and-tuning
- generative-modeling
- analysis-and-evaluation
date: '2026-10-03'
published: '2023-02-23'
arxiv: '2302.12192'
first_author: 'Lee'
keywords:
- 'learning-from-human-feedback'
- 'reward-weighted-likelihood'
- 'reward-model'
- 'prompt-classification'
- 'rejection-sampling'
- 'image-text-alignment'
- 'alignment-fidelity-tradeoff'
implementations: []
extends:
- LIT-377
compared_against:
- LIT-588
- LIT-tmp7vihu
- LIT-tmp9ntgf
- LIT-tmppb4sm
summary: >-
  Lee, Liu, Ryu, Watkins, Du, Boutilier, Abbeel, Ghavamzadeh and Gu, Google
  Research and UC Berkeley (2023), [ARXIV-2302.12192](https://arxiv.org/abs/2302.12192). RLHF's recipe carried
  to a text-to-image model, without the RL. Two labellers mark 27,528
  Stable Diffusion v1.5 images good or bad on templated count, colour and
  background prompts. A small head on frozen CLIP embeddings learns that
  label. One offline round of reward-weighted likelihood plus a pre-training
  loss then fine-tunes the model. Alignment wins 50% of 120 prompts by a
  two-thirds vote against 3% for the base. Fidelity loses: FID 13.97 to
  16.76, and 3% against 20% when compared with best-of-16 sampling from the
  base under the same reward. One run, no diversity measure.
---

# LIT-tmpznned: Aligning Text-to-Image Models using Human Feedback

Lee, Liu, Ryu, Watkins, Du, Boutilier, Abbeel, Ghavamzadeh and Gu, Google
Research and UC Berkeley (2023) — [ARXIV-2302.12192](https://arxiv.org/abs/2302.12192). Read at v1 (23 Feb
2023), the only arXiv version, appendices A–E included.

## Key takeaways

- **The data is narrow on purpose** (§3.1, Tables 1–2, App. B). Prompts
  combine one of 25 objects with a count (1–6), a colour (9) or a
  background (8), or all three. App. B counts 2,774 prompts and §4.1 says
  2,700. Stable Diffusion v1.5 drew 27,528 images, 60 or 6 per prompt.
  Labellers saw three images at a time and marked each good or bad for
  alignment only: 46.5% good, 48.5% bad, 5.0% skipped. App. B says the
  training labels came from two labellers. Counting was the weak category,
  at 34.4% good, against 70.4% for colour.
- **The reward is a small head on frozen CLIP** (§3.2, App. D). A
  two-layer MLP with 1,024 hidden units reads ViT-L/14 image and text
  embeddings and is regressed by MSE onto the binary label. An auxiliary
  loss (Eq. 1, T = 2, λ = 0.5) helps it generalize. For each image labelled
  good, rule-generated prompts with another colour, count, object or
  background serve as negatives, and the reward must pick the true prompt
  out by softmax. On held-out images it predicts which of two images a rater
  preferred better than CLIP similarity does, on seen and unseen prompts,
  and the auxiliary loss helps on both (Fig. 3a). The paper puts unseen-prompt
  accuracy near 80%. Halving the images per prompt lowers accuracy on both
  (Fig. 3b).
- **The update is one offline round of reward-weighted likelihood** (§3.3,
  Eq. 2). It is the reward-weighted negative log-likelihood of the model's
  own earlier samples, plus β times the negative log-likelihood of
  pre-training data. The samples are 23K labelled images and 16K more scored
  by the reward model. The pre-training data is a 625K LAION-5B subset
  filtered by the aesthetic predictor. All images are drawn once, from the
  pre-trained model. Training is 10,000 AdamW steps at batch 512, half
  pre-training data. β is not given, and neither is the learning rate. The
  log-likelihood is written as such; the code base is the diffusers
  text-to-image script (App. D), so in practice it is the denoising loss.
- **Alignment rises and fidelity falls** (§4.2, Fig. 4, App. C). On 120
  prompts, 60 seen and 60 with five held-out objects, nine raters compared
  sets of four images from the tuned and base models. The tuned model won
  alignment by two-thirds or more of the votes on 50% of prompts, the base
  on 3%, and 10% were ties. On fidelity the tuned model won 10% and the base
  15%. Per category, alignment win rates are 53–69% and fidelity win rates
  39–54% (Table 5).
- **The pre-training term repairs most of the damage, and alignment does
  not pay for it** (§4.4, Table 3). FID on 40,504 MS-COCO captions at 256 px
  is 13.97 for the base. Trained on the labelled images alone it is 26.59.
  Adding the reward-scored images gives 21.02 and adding pre-training data
  16.76. The training reward on the test prompts goes 0.43 → 0.69 → 0.79 →
  0.79 over the same steps. The cost that remains is 2.8 FID.
- **Best-of-n with the same reward is the stronger baseline** (§4.3,
  Fig. 6, Tables 6–7). Draw 16 images from the base model and keep the 4 the
  reward scores highest. Against 4 random draws, that wins alignment on 46%
  of prompts with no fidelity cost (12% against 9%). Against it, the tuned
  model wins alignment 20% to 10% and loses fidelity 3% to 20%.
- **The failures are named and not measured** (§4.2, §5). Some prompts give
  oversaturated or non-photorealistic images, entities are sometimes
  duplicated, and samples for one prompt vary less. The authors expect RL
  with online samples and a KL to the prior model to do better (§3.3, §5),
  and defer it because RL "usually requires extensive hyperparameter
  tuning".

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Up to 47% improvement in image-text alignment"** (§1) is the gap
  between 50% and 3% of prompts won by a two-thirds vote. It is a count of
  decisive prompts, not an alignment score, and ties and narrow wins are
  outside it.
- **"Mildly degraded image fidelity"** (§1) is the fidelity loss against
  the base. Against best-of-16 from the base under the same reward, the
  tuned model loses fidelity 3% to 20%, and FID is 2.8 worse even with the
  pre-training term.
- **The evaluation prompts are the training templates.** "Unseen" means
  five objects held out of the same count, colour and background templates.
  Artistic and open prompts appear only as samples (Fig. 2c, Figs. 10–11),
  chosen by the authors.
- **The reward model is judged on its own distribution.** Fig. 3a is
  held-out images of templated prompts, scored against labels from the same
  pipeline. Its bars carry no values in the text and no intervals.
- **The details do not all agree.** The prompt count is 2,774 in App. B and
  2,700 in §4.1. Labels come from "multiple human labelers" in §3.1 and two
  in App. B. Table 3's caption mentions CLIP scores that the table does not
  contain. App. D gives four GPUs at 8 per GPU and a total batch of 512, and
  does not mention accumulation.
- **One run per setting, no diversity measure.** The ± values in Tables 5–7
  are not explained. Lower diversity is reported only as an observation.

## Which comparisons are like for like

- **Tuned against base (Fig. 4)** shares prompts, sets of four and nine
  raters per query. It is the fair comparison, on templated prompts.
- **Tuned against best-of-16 (Fig. 6b)** spends four times the sampling at
  inference on the baseline's side, which the paper says. It also uses the
  same reward as the tuned model, so it isolates the update rather than the
  reward.
- **Reward model against CLIP similarity (Fig. 3a)** sets a model trained on
  the test distribution against a zero-shot score.
- **Table 3's data ablation** varies only the training mixture, one run
  each, scored by the training reward and FID.

## Standing in the anthology

It extends InstructGPT ([LIT-377](LIT-377.md)), whose recipe it carries to images and
cuts down. The reward model is fitted to human judgements of the model's
own outputs, as there. The pre-training loss in Eq. 2 is the term
InstructGPT added as PPO-ptx, cited here to keep the tuned model from
overfitting a narrow dataset. What it drops is the RL: PPO becomes one
round of reward-weighted likelihood on samples drawn once, with no KL to
the starting model. Its own discussion predicts that both omissions cost
something.

It compares its reward model against CLIP ([LIT-588](LIT-588.md)). CLIP image-text
similarity is the baseline judge of alignment in Fig. 3a, and a 2-layer
head on the same frozen CLIP embeddings, trained on 23K binary labels,
predicts the raters' choices better. The reward is thus CLIP features with
a learned readout. The base model is Stable Diffusion v1.5, from the
latent diffusion line ([LIT-062](LIT-062.md)).

Three later papers in the record ran this method as their baseline, each
in a changed form. DPOK ([LIT-tmp9ntgf](LIT-tmp9ntgf.md)), from mostly the same authors,
takes Eq. 2's first term as its supervised baseline, adds its own KL
terms instead of the pre-training loss, and scores it with ImageReward. It
finds online RL ahead on reward and on a held-out aesthetic score.
ImageReward ([LIT-tmppb4sm](LIT-tmppb4sm.md)) reimplements it as "Reward Weighted" on open
DiffusionDB prompts. It min-max normalizes its own reward into [0, 1] to
do so, and finds it below the untuned model in human ranking (39.52% win
rate). DDPO ([LIT-tmp7vihu](LIT-tmp7vihu.md)) calls this method "one iteration" of
reward-weighted regression. Its RWR baseline weights by exponentiated or
thresholded reward, drops the pre-training term and runs many rounds.
This paper's single round is one end of its interleaving sweep (Fig. 11),
and no setting of that sweep reaches DDPO.

Filed without a `NOTE`. The takeaways come from one full reading of v1,
appendices included, done for this filing. Figure values are quoted only
where the text or a figure label gives them.
