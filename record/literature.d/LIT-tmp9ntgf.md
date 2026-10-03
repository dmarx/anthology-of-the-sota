---
status: Active
title: 'DPOK: Reinforcement Learning for Fine-tuning Text-to-Image Diffusion Models'
version: 1
tags:
- adaptation-and-tuning
- generative-modeling
date: '2026-10-03'
published: '2023-05-25'
arxiv: '2305.16381'
first_author: 'Fan'
keywords:
- 'dpok'
- 'denoising-as-mdp'
- 'policy-gradient'
- 'kl-regularization'
- 'online-vs-supervised-fine-tuning'
- 'imagereward'
- 'value-function-baseline'
implementations: []
extends:
- LIT-377
compared_against:
- LIT-tmpznned
- LIT-tmp7vihu
summary: >-
  Fan, Watkins, Du, Liu, Ryu, Boutilier, Abbeel, Ghavamzadeh, K. Lee and
  K. Lee, Google Research, UW–Madison, UC Berkeley, Amazon and KAIST (2023),
  [ARXIV-2305.16381](https://arxiv.org/abs/2305.16381). Policy gradient over the denoising steps, as in DDPO, with
  a KL to the pre-trained model. The KL on the final image is intractable,
  so each step's KL is summed, which bounds it from above. Stable Diffusion
  v1.5 with LoRA is trained on ImageReward, one model per prompt, against
  the same reward-weighted objective trained offline on 20K samples. Online
  RL scores higher on ImageReward and on the held-out aesthetic predictor,
  and eight raters prefer it. The KL ablation is one prompt. The training
  reward is also the main metric, and no human compares against the base
  model.
---

<!-- inactive-ok-file: SOTA-302, SOTA-tmp6jbkw — Proposed; named for how this paper's tractable per-step anchor bears on them, not cited as settled advice -->

# LIT-tmp9ntgf: DPOK: Reinforcement Learning for Fine-tuning Text-to-Image Diffusion Models

Fan, Watkins, Du, Liu, Ryu, Boutilier, Abbeel, Ghavamzadeh, Kangwook Lee and
Kimin Lee, Google Research, UW–Madison, UC Berkeley, Amazon and KAIST (2023)
— [ARXIV-2305.16381](https://arxiv.org/abs/2305.16381). NeurIPS 2023. Read at v3 (1 Nov 2023), appendices
included. v1 (25 May 2023) was checked for what changed.

## Key takeaways

- **The denoising chain as an MDP** (§4.1, Eq. 4, Lemma 4.1). The state is
  (prompt, x_{T−t}), the action is the next latent, and the reward
  r(x_0, z) arrives at the last step. The covariance is held fixed and only
  the mean is trained (footnote 1), so each step is a Gaussian policy. The
  reward gradient is then REINFORCE over the per-step log-probabilities
  (Eq. 6). The lemma is adapted from Fan and Lee's earlier policy gradient
  for DDPM sampling.
- **The KL is bounded step by step** (Lemma 4.2, Eqs. 7–9, App. A.2–A.3).
  KL(p_θ(x_0|z) ‖ p_pre(x_0|z)) has no closed form. By the data processing
  inequality it is at most the KL between the two chains, which the Markov
  property splits into a sum over steps of the expected KL between two
  Gaussians. The objective is α times the negative reward plus β times that
  sum (Eq. 8). The gradient used (Eq. 9) drops the term that charges each
  step's KL to earlier actions, "for efficient training"; App. A.3 says
  that "already works well".
- **Defaults** (§5.1, App. B). Stable Diffusion v1.5 with LoRA on the UNet,
  ImageReward as the reward, α = 10, β = 0.01, AdamW at 10⁻⁵. Each
  sampling step draws 10 trajectories, then takes 5 gradient steps on
  minibatches of 32, with importance sampling and a clip range of 10⁻⁴ and
  gradient norm clipped to 0.1. Training stops at 20,000 online samples,
  10K gradient steps. One model is trained per prompt.
- **Online RL against the same objective trained offline** (§5.2, Figs. 2–3).
  The supervised arm minimizes reward-weighted negative log-likelihood on
  20K images drawn once from the pre-trained model, with a KL term of its
  own (below). On four prompts, one each for colour, composition, count
  and location, RL scores higher on ImageReward on all four. Supervised
  tuning lowers the LAION aesthetic score relative to RL, "and sometimes
  relative to the pre-trained model", and often oversaturates. Eight raters
  compared sets of four images from the RL and supervised models, 40
  images per prompt. RL "consistently outperforms" on alignment and on
  quality. Fig. 3c's values are not in the text.
- **KL helps online and trades off offline** (§5.3, Fig. 4, App. E.1,
  Figs. 8–9). On "A green colored rabbit", RL without the KL gives
  oversaturated colours and unnatural shapes, and RL with it reaches high
  ImageReward and aesthetic scores together. For supervised tuning the
  paper derives two KL surrogates (Lemma 4.3). KL-D shifts every weight by γ
  toward uniform. KL-O adds an L2 penalty between the tuned and pre-trained
  predictions. KL-O at γ = 2 removes some failures but lowers ImageReward,
  and across γ ∈ {0.1, 1, 2, 5} no supervised setting gets both scores high.
  The weight r + γ must be non-negative. Without clipping it at zero,
  supervised training "could fail" (App. B).
- **Many prompts, with a learned critic** (§5.5, Table 1, App. A.5, E.3).
  Trained on 104 MS-COCO prompts, ImageReward goes 0.22 → 0.55 and
  aesthetic score 5.39 → 5.43. On 183 DrawBench prompts it goes 0.13 → 0.58
  and 5.31 → 5.35. Each is scored on 30 images per prompt. This setting uses
  45 samples per step, β = 0.001, 50,000 samples and a value function
  V(x_t, z) as the baseline. On "A dog on the moon" the value function
  raises ImageReward from 0.86 to 1.51 and aesthetic score from 5.57 to
  5.60. There is no supervised arm here.
- **ImageReward was checked before it was used** (App. C, Table 2). On the
  authors' own binary-labelled pairs it beats CLIP and BLIP similarity on
  colour (86.06 against 82.46 for CLIP), count (73.65 against 66.11) and
  composition (79.65 against 70.98). CLIP is ahead on location (80.60
  against 79.73). On ImageReward's own test set it scores 65.13, against
  54.83 and 57.79.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The reward is also the main metric.** Every ImageReward number is the
  training reward. The held-out check is the LAION aesthetic predictor. The
  multi-prompt aesthetic gains are 0.04 on each set. There is no FID and no
  diversity measure.
- **No human compares against the base model.** The only human evaluation
  is RL against supervised tuning, eight raters, four prompts. It was added
  after v1, which had none.
- **"Without over-optimization issue"** (App. D) rests on that one held-out
  aesthetic score. The KL ablation behind it is one prompt and 50 samples,
  with no seeds and no values in the text (Fig. 4).
- **The anchor is a bound, minimized by a truncated gradient.** The summed
  per-step KL bounds the image KL from above, and Eq. 9 drops part of its
  gradient. Neither gap is measured.
- **The value function's story changed between versions.** v1's App. B
  says the value function speeds training on one prompt "but would cause
  instability in training under the multi-prompt setting", blamed on too
  few samples to fit it. v3 uses it in the multi-prompt setting and
  credits it with a higher final reward (Fig. 7). v1's multi-prompt section
  trained all four prompts jointly, with a supervised arm. v3 replaced it
  with 104 and 183 prompts and no supervised arm. v1's four-prompt table
  had joint RL at 1.10 ImageReward against 1.25 for the per-prompt models,
  from a base of 0.23.
- **"For stable training, we freeze the weights in batch norm"** (App. B).
  LoRA already freezes every base weight, and the paper does not say what
  this changes.

## Which comparisons are like for like

- **RL against supervised tuning (Figs. 3–4)** matches the number of images,
  20K, and the reward. Everything else differs: RL takes 10K steps of 32 at
  10⁻⁵, supervised tuning 8K steps of 128 at 2·10⁻⁵. The supervised arm's
  learning rate and γ were chosen from sweeps. RL's α and β are not
  reported as swept. The supervised arm is the paper's own construction:
  Lee et al.'s first term with DPOK's KL-O added, no pre-training data and
  ImageReward instead of a reward trained on its own labels.
- **The KL ablation (Fig. 4)** is the same configuration with and without
  the KL, on one prompt.
- **The multi-prompt runs (Table 1)** compare only against the base model.
- **The value-function result (App. A.5)** is one prompt with and without a
  learned baseline. It is not a comparison with any other baseline.

## Standing in the anthology

It extends InstructGPT ([LIT-377](LIT-377.md)) through the KL. InstructGPT keeps its PPO
policy near the supervised model with a KL penalty on every token. DPOK
carries that penalty, "similar to" InstructGPT and the summarization work
before it ([LIT-433](LIT-433.md)), to every denoising step. Lemma 4.2 says what the sum of
those step penalties bounds: the KL on the final image, which is the one the
paper wants. The importance ratio and clip in App. A.6 are PPO's ([LIT-241](LIT-241.md)),
at a clip range of 10⁻⁴.

It compares itself against Lee et al. ([LIT-tmpznned](LIT-tmpznned.md)), which shares eight of
its nine authors. Its supervised arm is Lee et al.'s reward-weighted
objective (Eq. 10), and the motivation is Lee et al.'s oversaturated
images. The finding is that the same objective trained online, with a KL
to the pre-trained model, scores higher on both the reward and the
aesthetic predictor. The comparison is with that objective, not with Lee et
al. as published, which had a pre-training loss and its own reward.

It is concurrent with DDPO ([LIT-tmp7vihu](LIT-tmp7vihu.md)). The two papers use the same MDP
and the same clip range. DDPO has no KL and trains on many prompts at
once, and DPOK has a KL and mostly trains one model per prompt. DDPO
later compared itself against DPOK's published numbers on DPOK's four
prompts and came out ahead without a KL, in a comparison that is not like
for like; its note says why. ImageReward ([LIT-tmppb4sm](LIT-tmppb4sm.md)) is the reward
throughout. Diffusion-DPO ([LIT-tmp4m2nj](LIT-tmp4m2nj.md)) derives its loss in this MDP
(its Supp. S3) and lists DPOK as limited to a small vocabulary, without
running it.

The critic bears on [SOTA-145](../practices.d/SOTA-145.md), without testing it. DPOK's value function is
a learned critic, and on one prompt it beat no baseline at all. It is not
compared with a group or per-prompt baseline, which is the choice that
practice is about. The v1 report that the critic destabilized multi-prompt
training was withdrawn in v3 without a stated reason.

The per-step KL is the diffusion antecedent of the anchor [SOTA-tmp6jbkw](../practices.d/SOTA-tmp6jbkw.md)
takes from Flow-GRPO ([LIT-tmpdktqx](LIT-tmpdktqx.md)). Lemma 4.2 is the bound that makes
such an anchor mean something about the image. [THEORY-tmpr00tj](../theory.d/THEORY-tmpr00tj.md) explains why
the anchor is computable: each step is a Gaussian. For [SOTA-302](../practices.d/SOTA-302.md), DPOK is
another multi-step sampler where weight-space reward tuning with a
tractable anchor kept the held-out aesthetic score, on one prompt. It
tests no distilled model. The base model is Stable Diffusion from the
latent diffusion line ([LIT-062](LIT-062.md)), tuned with LoRA ([LIT-046](LIT-046.md)).

Filed without a `NOTE`. The takeaways come from one full reading of v3,
appendices included, done for this filing. v1 was read for its multi-prompt
section, App. B and its human evaluation. Figure values are quoted only
where the text or a table gives them.
