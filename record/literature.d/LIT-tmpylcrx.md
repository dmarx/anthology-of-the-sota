---
status: Active
title: 'Scaling Laws for Reward Model Overoptimization'
version: 1
tags:
- adaptation-and-tuning
- analysis-and-evaluation
- training-optimization
date: '2026-10-03'
published: '2022-10-19'
arxiv: '2210.10760'
first_author: 'Gao'
keywords:
- 'reward-overoptimization'
- 'goodharts-law'
- 'reward-model'
- 'best-of-n'
- 'kl-penalty'
- 'rlhf'
- 'scaling-laws'
- 'synthetic-gold-reward'
implementations: []
extends:
- LIT-377
summary: >-
  Gao, Schulman and Hilton, OpenAI (2022), [ARXIV-2210.10760](https://arxiv.org/abs/2210.10760). InstructGPT's
  6B reward model stands in for people and labels comparisons for proxy
  reward models of 3M to 3B parameters. Optimizing a 1.2B policy against
  a proxy, the gold reward rises and then falls as a function of
  d = √KL from the initial policy: d(α − βd) for best-of-n and
  d(α − β log d) for PPO. The coefficients move smoothly with the proxy's
  size, so the peak is predictable. Larger proxies and more comparison
  data push the peak out, and a 6B policy peaks at the same KL as a 1.2B
  one. A KL penalty in the reward did not improve gold reward at a given
  KL; its effect was like early stopping, a result the authors flag as
  possibly hyperparameter-sensitive. RL spends far more KL than best-of-n,
  so KL does not compare optimization across methods. Synthetic labels,
  one environment.
---

<!-- inactive-ok-file: SOTA-tmp6jbkw SOTA-302 SOTA-284 — Proposed practices whose reward-model and KL-anchor arguments this paper bears on, named as what it informs -->

# LIT-tmpylcrx: Scaling Laws for Reward Model Overoptimization

Leo Gao, John Schulman and Jacob Hilton, OpenAI (2022) — [ARXIV-2210.10760](https://arxiv.org/abs/2210.10760).
Read at v1 (19 Oct 2022), the only arXiv version, appendices
included. The figures carry most of the results without numeric labels;
values are quoted only where the text gives them.

## Key takeaways

- **The setup replaces people with a fixed model** (§2, Fig. 2). Policies
  are GPT-3-series models after two epochs of SFT on InstructGPT
  demonstrations, on InstructGPT's prompts. The 6B InstructGPT reward
  model is the "gold" reward. It labels pairs of policy samples
  deterministically, higher score wins, and 100,000 such comparisons
  (10% held out) train proxy reward models from 3M to 3B parameters.
  Optimization against the proxy is PPO or best-of-n (BoN), and the gold
  model scores the result.
- **Gold reward is a function of distance from the start** (§1, §3.1,
  Fig. 1). With d = √KL(π ‖ π_init):
  - BoN: R(d) = d(α_bon − β_bon·d). KL for BoN is log n − (n − 1)/n.
  - RL: R(d) = d(α_RL − β_RL·log d). This form has infinite slope at the
    origin, and the authors expect it to fail near zero (footnote 1, App. B).
  - Gold reward rises, peaks and declines, while the proxy keeps rising.
    The BoN form was chosen on data up to n = 1,000 (about 6 nats) and then
    predicted a run to n = 60,000 (about 10 nats) in advance.
- **A bigger reward model overoptimizes less, smoothly** (§3.2, Fig. 3).
  With policy (1.2B) and data (90,000) fixed, α_bon, β_bon and β_RL vary
  smoothly, roughly logarithmically, with proxy size. α_RL can be held
  constant across sizes. That predicts the peak gold score for a proxy of
  a given size (Fig. 12).
- **Data has a floor, and repeats do not substitute for it** (§3.3, Figs.
  4–6, 13). Below about 2,000 comparisons every proxy is near chance.
  Above it, more data gives better gold scores and less Goodharting, and
  larger proxies gain faster. Four epochs over 2,000 comparisons did no
  better than one; one epoch over 8,000 did substantially better. Two
  proxies with equal validation loss are about equally robust, whatever
  mix of size and data got them there (weak evidence, Fig. 5).
- **Policy size changes the start, not the overoptimization** (§3.4, §4.4,
  Figs. 7, 24). A 6B policy gains less from optimization than a 1.2B one.
  Both peak at almost the same KL, and the proxy–gold gap is almost the
  same. Only two policy sizes were run.
- **RL spends KL much faster than BoN** (§3.5, Fig. 8). BoN searches near
  the initial policy. RL's KL grows roughly quadratically with steps
  without a penalty. Plotted against proxy score instead of KL, the two
  look alike, and RL then peaks at a higher gold score. So KL is a fine
  axis within one method and a bad one between methods (§4.1).
- **The KL penalty acted like early stopping** (§3.6, Figs. 9, 14). With
  the penalty added to the reward at several strengths, gold reward
  depended only on the KL the policy had reached. A stronger penalty made
  the policy converge earlier on the same gold-versus-KL frontier and
  never moved the frontier. It did raise the proxy reward at a given KL,
  so the proxy–gold gap was larger with it. The authors note "some
  evidence that this result could be particularly sensitive to
  hyperparameters". All other RL runs used no penalty. PPO's clipped
  update limits KL to the previous policy, which slows growth of the KL to
  the initial one, and that implicit limit "appears to lead to less
  overoptimization than an explicit KL penalty", for reasons the authors
  do not know.
- **What the coefficients mean** (§4.2). Under noise independent of the
  true reward, the gold reward can only rise with the proxy (Eq. 1, App.
  A), so the observed decline needs another cause. The authors read α as
  regressional Goodhart, noise in the proxy, and β as extremal Goodhart,
  the policy leaving the proxy's training distribution. Iterated RLHF with
  fresh reward models gains β_RL·d·log k over k rounds, under assumptions
  stated as untested (§4.3).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The gold standard is a model.** The study measures the gap between a
  proxy and another reward model, not between a reward model and people.
  The authors name the second gap, between labels and what people intend,
  as the main thing it does not capture (§4.5). Gold and proxies share the
  GPT-3 architecture and pretraining, which may correlate their errors.
- **The labels are clean.** Comparisons are decided by the gold score with
  no noise. Sampling labels gave noisier results (footnote 4). Real
  preference data is noisier, with ties and disagreement.
- **The KL-penalty result is the softest in the paper.** It is one sweep,
  at one policy and reward-model size (both 1.2B), with default PPO
  settings, and flagged by the authors as possibly hyperparameter-
  sensitive. It concerns a penalty added to the reward, not a KL term in
  the loss, and is judged on the gold-versus-KL frontier.
- **The fits are of the gold score only.** The proxy score could not be
  fit satisfactorily (§3.1), and extrapolation underestimates it.
- **Recalibration is post hoc.** Rewards are recentred and the proxies'
  logits rescaled after the runs. That does not affect BoN and "likely" not
  PPO.
- **Some of it contradicts the authors' other work.** That larger reward
  models do not pass the data floor earlier "contradicts some other
  internal findings" (footnote 8).
- **No seeds or intervals** except where Fig. 5's caption says points are
  averaged over seeds. Adversarial Goodhart, a policy deliberately
  manipulating the proxy, is out of reach of these models (§4.2.4), and
  the authors warn that the laws may break when it is not.

## Which comparisons are like for like

- **Reward-model size (Figs. 1, 3)** holds policy (1.2B) and data
  (90,000) fixed. Clean.
- **Data size (Figs. 4–6)** holds the proxy at 12M for RL; the BoN sweep
  covers every size and data combination (Fig. 10).
- **Policy size (Fig. 7)** is two sizes against a 12M proxy, repeated with
  a 3B proxy (Fig. 22). The 6B policy starts higher, so gains are read
  from different baselines.
- **RL against BoN (Fig. 8)** is compared on the proxy axis because the KL
  axis is not comparable between them, which is one of the findings.
- **KL penalties (Fig. 9)** are compared at equal KL. Compared at equal
  steps, the penalty looks like protection, because it stops the policy
  earlier.

## Standing in the anthology

It extends InstructGPT ([LIT-377](LIT-377.md)). The environment, the SFT policies, the
prompts and above all the gold reward are InstructGPT's 6B reward model.
The study measures what InstructGPT's pipeline does when optimized harder,
with that pipeline's own reward model as ground truth. It bears directly on
InstructGPT's design choice: InstructGPT adds a per-token KL penalty to
mitigate reward-model overoptimization. In InstructGPT's own setting, that
penalty did not improve the true reward at a given distance from the SFT
policy; it stopped the policy earlier. The method used is PPO ([LIT-241](LIT-241.md)),
whose clipped update the paper finds to do more against overoptimization
than the explicit penalty. Best-of-n's KL formula is from the
summarization work ([LIT-433](LIT-433.md)).

**What this means for the record's image-generation papers.** DDPO
([LIT-tmp7vihu](LIT-tmp7vihu.md)) cites this paper for the view that a KL penalty may amount
to early stopping, and runs with no KL term and hand-picked checkpoints:
early stopping by a person. Flow-GRPO ([LIT-tmpdktqx](LIT-tmpdktqx.md)) argues the opposite
for its KL term, that it is "not empirically equivalent to early
stopping", without citing this paper. The two are not measuring the same
thing. Flow-GRPO plots reward against training steps and judges quality by
other reward models, at equal reward; this paper plots a gold reward
against KL. Flow-GRPO's KL is the per-step term in GRPO's objective,
tuned to keep the divergence "small and nearly constant", and its text
gives no KL distances. So [SOTA-tmp6jbkw](../practices.d/SOTA-tmp6jbkw.md)'s claim that the anchor keeps quality and
this paper's finding can both hold. Telling them apart needs quality
plotted against KL, with and without the term. [SOTA-302](../practices.d/SOTA-302.md)'s argument that a
weight-space reward fine-tune "reward-hacks" without its KL anchor is
consistent with distance being what matters. This paper adds that a
penalty is one way to limit distance and early stopping is another.

PickScore ([LIT-tmpjt45z](LIT-tmpjt45z.md)) and VideoReward ([LIT-tmp3txak](LIT-tmp3txak.md)) are learned proxies
of exactly this kind, used as rewards and as judges. VideoReward's paper
reports one dimension of the reward falling while the others rise, and
quality loss that its own reward did not see. Neither is studied under
this paper's protocol.

[SOTA-284](../practices.d/SOTA-284.md) recommends choosing checkpoints for Best-of-N by coverage, where
success is judged by a verifier that accepts correct answers. With a
learned scorer in place of a verifier, this paper shows the true quality
of the best-of-n pick falling as n grows past a size-dependent peak.

Filed without a `NOTE`. The takeaways come from one full reading of v1,
appendices included, done for this filing. Coefficient values and curve
positions are not quoted; the text gives none.
