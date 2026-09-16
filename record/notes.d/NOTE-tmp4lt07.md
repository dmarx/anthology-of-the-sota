---
status: Read
paper: LIT-tmp3me1q
title: 'Training language models to follow instructions with human feedback'
version: 1
date: '2026-09-16'
summary: >-
  Making a language model bigger does not make it better at following
  instructions, so stop buying parameters and buy human feedback instead:
  demonstrations to fine-tune on, rankings to fit a reward model to, then
  policy optimization against that reward with a KL leash back to the
  supervised model. A 1.3B model tuned this way is preferred to 175B GPT-3.
  The cost is a measurable regression on held-out NLP tasks, and the paper
  supplies both the name for it and a fix.
---

# NOTE-tmp4lt07: Training language models to follow instructions with human feedback

## Contribution

A three-stage recipe for aligning a pretrained language model to user intent,
and the evidence that it dominates scale on the axis it targets. The recipe —
SFT, reward model, RL against the reward — became the default shape of
post-training; the paper's own contribution is applying it to *general
instruction following* rather than to one task, and measuring what it costs.

## Key insight

Preference is cheap to *express* and expensive to *demonstrate*. Humans
ranking four outputs produce far more signal per unit of labeler time than
humans writing ideal outputs, so the demonstrations train a starting policy
and the rankings train a reward model that can then be optimized against
indefinitely. The KL penalty is what stops that optimization running off the
end of where the reward model is valid.

## Assumptions

- The prompt distribution used for training resembles the one the model will
  face. Here it is the OpenAI API's, which is why the comparison against
  public-task instruction tuning goes the way it does.
- Labeler preferences are a usable proxy for the target behaviour. The paper
  states the limit of this explicitly rather than assuming it away.
- The reward model generalises far enough beyond its training distribution
  that PPO can optimize against it — bounded in practice by the KL penalty.
- The 6B reward model is adequate for policies up to 175B; larger reward
  models were available and not used.
- Labeler agreement is high enough for a single scalar reward to be
  meaningful; inter-annotator agreement is reported, not assumed.

## Key results

- **A 1.3B InstructGPT is preferred to 175B GPT-3.** 100x fewer parameters.
  *Holds when:* the API prompt distribution; labeler evaluation; comparisons
  against GPT-3 with and without prompting.
- **85 ± 3% win rate** for 175B InstructGPT over 175B GPT-3, **71 ± 4%** over
  few-shot 175B GPT-3.
  *Holds when:* held-out customer prompts; 95% confidence intervals.
- **73.4 ± 2% against the SFT baseline**, versus 26.8 ± 2% for T0 and
  29.8 ± 2% for FLAN.
  *Holds when:* the API prompt distribution — the comparison is explicitly on
  real user prompts rather than on public NLP tasks, which is the whole point
  of it.
- **The alignment tax is real and measured**: regressions on SQuAD, DROP,
  HellaSwag and WMT'15 French-English.
  *Holds when:* the public-dataset evaluations, against the GPT-3 baseline.
- **PPO-ptx greatly reduces the tax at no cost in preference.** Mixing
  pretraining-distribution log-likelihood updates into the PPO updates
  recovers most of the regression "without compromising labeler preference
  scores".
  *Holds when:* the pretraining mix coefficient is tuned; reported as a large
  reduction rather than elimination.
- **It generalises to held-out labelers** who contributed no training data, at
  about the same preference rate.
  *Holds when:* a preliminary experiment, the paper's own word; not a study of
  broader populations.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Fine-tuning with human feedback beats a 100x larger model at following instructions. | strong | Head-to-head labeler preference on held-out customer prompts, three model sizes, confidence intervals reported. |
| C2 | Human-preference tuning on a real prompt distribution beats instruction tuning on compiled public tasks. | strong | Direct comparison against FLAN and T0++ trained by the same authors; 73.4% vs 26.8%/29.8%. |
| C3 | RLHF imposes a measurable alignment tax on unrelated capabilities. | strong | Regressions on four public datasets against the GPT-3 baseline. |
| C4 | Mixing pretraining gradients into the RL updates removes most of that tax for free. | moderate | PPO-ptx compared against PPO across the public evaluations; one configuration, one lab. |
| C5 | The result reflects the preferences of ~40 screened contractors, not of humanity. | strong | Stated by the authors as a scope limit, with the labeler demographics and selection reported. |

## Method

**RLHF for instruction following, in three steps.**

1. **SFT.** Labelers write demonstrations on the prompt distribution; fine-tune
   the pretrained model on them supervised.
2. **Reward model.** Labelers rank 4-9 sampled outputs per prompt; train a 6B
   reward model on the pairwise comparisons.
3. **PPO.** Optimize the SFT policy against the reward model, with a per-token
   KL penalty back to the SFT policy. **PPO-ptx** adds a pretraining
   log-likelihood term with coefficient `gamma`; `beta` is the KL coefficient.

- 40 screened contractors, prompts from the API plus labeler-written ones
- One 6B reward model shared across all policy sizes
- Per-token KL penalty against over-optimization
- Optional pretraining mix to pay down the alignment tax

## Concepts

- **Alignment tax** — the capability regression that alignment training causes
  on tasks it does not target. Named here, and the name is most of why this
  paper is cited outside its own subject.
- **Reward-model over-optimization** — pushing the policy into a region where
  the reward model's predictions no longer track human preference. The KL
  penalty is the mitigation, not a solution.
- **PPO-ptx** — the pretraining-mixed variant. The paper's own answer to its
  own worst finding, and the part most summaries drop.
- **Preference over demonstration** — ranking outputs is cheaper per unit of
  signal than writing them, which is the economic argument the whole pipeline
  rests on.

## Connections

**Builds on.**

- Christiano et al. (2017) — learning from human preferences; the origin this
  paper follows and which this record does not hold.
- Stiennon et al. (2020) — the same method applied to summarization.

**Related.**

- [LIT-169](../literature.d/LIT-169.md) (DPO) — removes the explicit reward model and the RL step, and is
  defined against this pipeline.
- [LIT-082](../literature.d/LIT-082.md) (Constitutional AI) — replaces the human preference labels with
  model-written ones against stated principles.

## Recommendations

- **R1** — Spend on post-training before spending on parameters when the goal
  is instruction following; a 1.3B tuned model beat a 175B untuned one.
  *Topic:* where to spend · *Strength:* strong · *When:* The target behaviour is
  following user intent rather than raw capability.
- **R2** — Train the preference data on the prompt distribution you will
  serve, not on compiled public task suites.
  *Topic:* preference data · *Strength:* strong · *When:* Real user prompts are
  available; this is the FLAN/T0 comparison.
- **R3** — Mix pretraining-distribution updates into the RL objective to pay
  down the alignment tax.
  *Topic:* alignment tax · *Strength:* moderate · *When:* Capability regression
  on untargeted tasks is measured and unacceptable.
- **R4** — Keep a per-token KL penalty back to the supervised policy.
  *Topic:* over-optimization · *Strength:* strong · *When:* Any policy
  optimization against a learned reward model.
- **R5** — Report who the labelers are and what distribution their preferences
  represent.
  *Topic:* reporting · *Strength:* moderate · *When:* Publishing a
  preference-tuned model.

## Bearing on the record

This is the trunk under [SOTA-126](../practices.d/SOTA-126.md), [SOTA-183](../practices.d/SOTA-183.md), [LIT-169](../literature.d/LIT-169.md) and [LIT-082](../literature.d/LIT-082.md), and it was
absent. What it should *not* do is acquire a practice by default, and this
reading does not propose one:

**R1 and R2 are the record's [DP-007](../../docs/design-principles.md#dp-7) problem, not its solution.** "Do
post-training" and "use your own prompt distribution" are things every lab now
does, which is exactly why nobody publishes them and exactly why they read as
vacuous rather than as recommendations. Filing them would produce two
documents saying what the corpus already assumes on every page.

**R4 is close to filed already** wherever a practice here prescribes a KL or
trust-region term, and the record should check that before adding another.

**R3 is the live candidate.** Mixing pretraining gradients into the alignment
objective is specific, actionable, cheap, measured against a named cost, and —
unlike the rest — *not* universally done. [SOTA-199](../practices.d/SOTA-199.md) regularizes a narrow
fine-tune against the pre-fine-tuning model's own samples, which is a
different mechanism aimed at the same failure. Whether the two are variants of
one practice or two is the question a filer should answer, and answering it
needs [SOTA-199](../practices.d/SOTA-199.md)'s source read alongside this one. Left open deliberately rather
than guessed at.

## Limitations

- One lab, one prompt distribution, one labeler pool of about 40 people. The
  paper is unusually direct that its notion of "aligned" is that pool's.
- PPO-ptx is reported as a fix at one configuration; there is no sweep of the
  pretraining-mix coefficient against the preference/tax trade.
- The reward model is 6B for every policy. Whether the tax, the
  over-optimization or the win rates change with reward-model scale is
  untested here, deliberately, to keep the policy comparison clean.
- GPT-3 era models and PPO. Every subsequent method in this record's
  preference line — DPO and its descendants — changes step 3, so results
  attached to PPO specifically should not be assumed to carry.
- "Preferred by labelers" is the metric throughout. It is the right metric for
  the claim and it is not a capability measurement, which is what makes the
  alignment tax a separate finding rather than a contradiction.

## Open questions

- Does the alignment tax persist when step 3 is DPO rather than PPO, and does
  a pretraining mix still pay it down?
- How far does the reward model have to generalise, and does a larger one move
  the KL coefficient that stops over-optimization?
- What does the win rate look like against a labeler pool selected
  differently — the paper's own framing invites this and it has not been run
  here.
