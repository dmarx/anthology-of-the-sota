---
status: Active
title: 'Training Diffusion Models with Reinforcement Learning'
version: 1
tags:
- adaptation-and-tuning
- generative-modeling
- training-optimization
date: '2026-10-03'
published: '2023-05-22'
arxiv: '2305.13301'
first_author: 'Black'
keywords:
- 'ddpo'
- 'denoising-as-mdp'
- 'policy-gradient'
- 'reward-weighted-regression'
- 'cfg-training'
- 'vlm-reward'
- 'reward-overoptimization'
implementations: []
extends:
- LIT-241
compared_against:
- LIT-tmp4m2nj
- LIT-tmpdktqx
summary: >-
  Black, Janner, Du, Kostrikov and Levine, UC Berkeley and MIT (2023),
  [ARXIV-2305.13301](https://arxiv.org/abs/2305.13301). Treat each denoising step of a stochastic sampler as an
  action. Each step is then an isotropic Gaussian with an exact likelihood,
  so policy gradient (DDPO) can fine-tune a diffusion model on any black-box
  reward of the final image. On Stable Diffusion v1.4, with JPEG
  compressibility, LAION aesthetic score and a LLaVA + BERTScore alignment
  reward, both DDPO estimators beat reward-weighted regression per reward
  query, and the PPO-clipped one is slightly ahead. There is no KL term.
  Over-optimization is shown and handled by picking checkpoints by hand.
  Prompt sets are narrow (45–398 animals), there is no human evaluation, and
  the run count is not stated.
---

<!-- inactive-ok-file: SOTA-302 — Proposed; named as the practice this paper's missing anchor bears on, not as settled advice -->

# LIT-tmp7vihu: Training Diffusion Models with Reinforcement Learning

Black, Janner, Du, Kostrikov and Levine, UC Berkeley and MIT (2023) —
[ARXIV-2305.13301](https://arxiv.org/abs/2305.13301). Read at v4 (4 Jan 2024), appendices included. v1
(22 May 2023) was checked for what changed.

## Key takeaways

- **Denoising as a multi-step MDP** (§4.3). The state is (prompt, t,
  x_t), the action is x_{t−1}, and the reward r(x_0, c) arrives only at the
  last step. With a DDPM-style sampler each step p_θ(x_{t−1} | x_t, c) is an
  isotropic Gaussian (Eq. 2), so its log-likelihood and gradient are exact.
  The alternative it argues against treats the whole chain as one action and
  has only the ELBO for a likelihood. That is reward-weighted regression
  (RWR, §4.2), which the paper calls "not theoretically justified" for
  diffusion.
- **Two estimators.** DDPO_SF is REINFORCE, one update per batch of
  samples. DDPO_IS adds an importance ratio to the previous parameters and
  PPO's clipped surrogate, so it can take several updates per batch. The
  clip range is 10⁻⁴, "very small compared to standard RL tasks" (App.
  D.1). The defaults (App. D.5) are 50 sampling steps, guidance weight 5,
  AdamW at 10⁻⁵, and 256 samples per iteration. DDPO_IS takes four
  minibatch updates per iteration.
- **Policy gradient beats reward-weighted likelihood** (§6.1, Fig. 4). On
  compressibility, incompressibility and aesthetic score, both DDPO variants
  climb faster per reward query than RWR with either exponential or binary
  weights. DDPO_IS is slightly ahead of DDPO_SF. In the figure, RWR's
  aesthetic curve ends below where it started. The comparison confounds the
  objective with how on-policy the data is: RWR collects 10,000 samples per
  iteration, DDPO 256 (App. E.2). Fig. 11 varies RWR from 16,384 down to 256
  samples per iteration. More interleaving helps up to a point and then
  hurts, and no setting reaches DDPO.
- **Train the guided prediction, not the conditional one** (App. E.1,
  Fig. 10). Fine-tuning only the conditional ε-prediction degraded quickly
  after the first round, which the authors put down to the guidance weight
  becoming miscalibrated. Training on the classifier-free-guided
  ε-prediction with a fixed weight ("CFG training") fixed it. On RWR_sparse
  it makes no difference after one round and is essential after that.
- **The baseline is a per-prompt reward normalization** (App. D.3).
  Rewards are standardized by a running mean and standard deviation kept
  separately for each prompt. The paper calls this the analogue of a value
  baseline. There is no critic.
- **A VLM as the reward** (§5.3, §6.2, Fig. 5). LLaVA describes the image
  and the reward is BERTScore recall of the prompt against that
  description. On "a(n) [animal] [activity]" prompts (45 animals × 3
  activities), samples become more faithful and also more cartoon-like,
  which was not asked for. Prompts with zero initial success, such as "a
  dolphin riding a bike", improved only through transfer from other
  prompts.
- **It generalizes beyond the training prompts, narrowly** (§6.3, App. F,
  Fig. 12). The aesthetic model trained on 45 animals improves as much on
  38 unseen animals, and less on 50 everyday objects.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"More effective than alternative reward-weighted likelihood
  approaches"** (abstract) rests on curves (Fig. 4) whose shaded bands are
  not explained. The paper gives no seed count, and there is no table of
  final values. RWR ran on a v3-128 TPU pod and DDPO on a v4-64, each about
  4 hours to 50k samples (App. D.4).
- **There is no KL term, and the anchor is a person.** App. A shows the
  incompressibility model degrading into noise. Asked for "n animals", the
  alignment model wrote text such as "sixx ttutttas" that LLaVA read as the
  number, a typographic attack on the reward. The qualitative results use
  "the last checkpoint before a model began to deteriorate", identified
  manually for each method. The paper leaves over-optimization "for future
  work" and cites the argument that a KL penalty may amount to early
  stopping. v1 had this as a main-text subsection (§6.4). v4 moved it to
  App. A and added the manual checkpoint choice.
- **The rewards are proxies, and no human looks.** The aesthetic reward is
  a linear head on CLIP embeddings trained on 176,000 ratings (§5.2). The
  alignment reward is a VLM's caption scored by BERTScore. Every
  quantitative result is the training reward or a second reward model.
  There is no human evaluation and no diversity measure.
- **The prompt sets are small.** The training sets are 398 ImageNet
  animals (compressibility), 45 animals (aesthetics) and 135 animal-activity
  prompts (alignment), all on SD v1.4 at 512 px. The authors call the image
  range "constrained" (§7). Later work reports that DDPO did not carry over
  to an open-vocabulary preference set; see Standing below.
- **The DPOK and universal-guidance comparisons were added after v1**
  (Apps. B and C). v1's appendices held only implementation details, CFG
  training and samples.

## Which comparisons are like for like

- **RWR (Fig. 4)** shares the model, rewards, prompts, sampler and
  optimizer settings (App. D.5), but not the samples per iteration or the
  updates per iteration. Fig. 11 addresses the first. It keeps updates per
  iteration fixed, so more interleaving also means more updates per sample.
- **DPOK (App. C, Fig. 8)** is not like for like. DPOK's numbers are copied
  from its paper at the one point it reports, 20k reward queries. DDPO is
  rerun on SD v1.5 with LoRA ([LIT-046](LIT-046.md)) at a learning rate of 3·10⁻⁴, with
  its own hyperparameters rather than DPOK's. It trains one model for all
  four prompts where DPOK trains one per prompt, and it has no KL term,
  which DPOK has. With ImageReward as the reward and LAION aesthetics as the
  held-out metric, DDPO is ahead on all four prompts. The held-out
  aesthetic score drops on "four wolves in the park" within 25k queries.
  The paper calls this "significant overoptimization" in one sentence and
  "not severe or unreasonably fast" in the next.
- **Universal guidance (App. B, Table 1)** is one prompt ("wolf"), 50
  samples: base 5.95 ± 0.03, universal guidance 6.14 ± 0.05, DDPO_IS at 20k
  queries 6.63 ± 0.03. Guidance takes almost 2 minutes per image on an A100
  against 4 seconds.

## Standing in the anthology

It extends PPO ([LIT-241](LIT-241.md)). DDPO_IS is PPO's clipped importance-ratio
surrogate applied to each denoising step as a separate action, with the
clip range cut to 10⁻⁴. Advantages come from per-prompt running statistics
rather than a learned value function. That is the same move GRPO
([LIT-127](LIT-127.md)) later made in language, where the baseline comes from a group of
samples for the same prompt. So DDPO is earlier evidence for [SOTA-145](../practices.d/SOTA-145.md)
outside language. It is not GRPO, though. Its statistics run across
iterations rather than within one group, and the paper never compares
against a critic.

It is the root of the line that Flow-GRPO ([LIT-tmpdktqx](LIT-tmpdktqx.md)) carries to flow
matching. Flow-GRPO's tractable policy is DDPO's, a Gaussian step with a
closed-form likelihood. Flow-GRPO gets that Gaussian by converting the
deterministic flow ODE into an SDE, where DDPO had a stochastic DDPM
sampler to begin with. Flow-GRPO adds a group baseline and a KL to the
reference. It also runs DDPO itself, through its own SDE on SD3.5-M with
PickScore (its Fig. 8). There DDPO rises more slowly and "eventually
collapses", and Flow-GRPO keeps improving. That is the update rule being
compared, not DDPO as published. Flow-GRPO also reports that RWR did not
improve with training on its task, and calls that consistent with DDPO. In
DDPO's Fig. 4, RWR does improve on the two compression rewards, only more
slowly.

Diffusion-DPO ([LIT-tmp4m2nj](LIT-tmp4m2nj.md)) is the offline, preference-pair alternative.
Its authors report that public DDPO implementations gave no stable PickScore
improvement on Pick-a-Pic's open-vocabulary prompts over a hyperparameter
sweep. They give no numbers (their §5.1 and Supp. S1). Their explanation is
that high-reward prompts dominate the gradient. That overlooks DDPO's
per-prompt reward normalization, which exists to stop exactly that, so the
failure is reported but not explained.

The missing KL anchor is what [SOTA-302](../practices.d/SOTA-302.md)'s argument turns on. HyperNoise
([LIT-491](LIT-491.md)) finds weight-space reward fine-tuning of a distilled generator
harmful because the anchor is intractable there. DDPO has a tractable
per-step likelihood and still runs without an anchor. Its over-optimization
examples are the failure that practice's condition is about.

The other ingredients are already in the record. The base model is Stable
Diffusion from the latent diffusion line ([LIT-062](LIT-062.md)). CFG training is about
classifier-free guidance ([LIT-693](LIT-693.md)). The aesthetic predictor sits on CLIP
([LIT-588](LIT-588.md)). The VLM reward is modelled on AI feedback in language
([LIT-082](LIT-082.md)).

Filed without a `NOTE`. The takeaways come from one full reading of v4,
appendices included, done for this filing. v1 was read for its abstract,
the over-optimization section and its appendix list. Figure values are not
quoted except where the text or a table gives them.
