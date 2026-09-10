---
number: 41
status: Read
formerly:
- NOTE-tmpf3erq
paper: LIT-013
title: 'Population Based Training of Neural Networks'
version: 1
tags:
- training-optimization
date: '2026-09-09'
published: '2017-11-01'
summary: >-
  Train a population of models in parallel; periodically let a poor performer copy a good one's weights (exploit) and perturb its hyperparameters (explore). The output is a hyperparameter *schedule* rather than a fixed setting, discovered inside a single training run at roughly the cost of the population.
---

# NOTE-041: Population Based Training of Neural Networks

## Contribution

Collapses hyperparameter search and training into one process. A population of
`N` models trains in parallel and asynchronously; each member periodically
evaluates itself and, if it is underperforming, **exploits** — copies the
weights *and* hyperparameters of a better member — then **explores** by
perturbing those hyperparameters. Training continues from the copied weights
rather than restarting.

The consequence that matters is not the search efficiency. It is that the
result is a **schedule**: because hyperparameters change mid-run and the
lineage is preserved, PBT discovers time-varying settings that no
fixed-hyperparameter search can express.

## Key insight

Sequential hyperparameter methods (Bayesian optimisation and friends) pay for
every evaluation with a full training run, and parallel methods (random or
grid) cannot use partial results. PBT gets both by noticing that a partially
trained model is a **valid initialisation** for a different hyperparameter
setting. Weight copying is the whole trick — it makes an evaluation cost a
fraction of a run instead of a run, and it is what makes the greedy
exploit/explore loop affordable enough to run continuously.

## Assumptions

- **Weights transfer across a hyperparameter perturbation.** Copying weights
  from a model trained under one learning rate and continuing under another
  must not be destructive. True for small perturbations; the paper does not
  characterise where it breaks.
- **A usable fitness signal exists mid-training** — and one that is not the
  quantity you are ultimately judged on, if that would overfit. The GAN
  experiment is explicit about this: CIFAR Inception score is used for
  selection, ImageNet Inception score only for reporting, precisely to avoid
  selecting on the test metric.
- **Enough population for diversity.** PBT is greedy, so a small population
  gets stuck.

## Key results

- **Transformer / WMT En-De:** beats an already highly tuned baseline —
  validation BLEU 23.71 → **24.23** (newstest2012), test 22.30 → **22.65** —
  and trains faster. That is the strongest claim here, because the baseline
  was not a strawman.
- **The discovered LR schedule resembles the hand-tuned one**: a small initial
  rate, a jump of about three orders of magnitude, then something like
  exponential decay. Rediscovering warmup-then-decay from scratch is a better
  argument for warmup than most papers that recommend it.
- **Population size 20–40 is enough** for "strong and consistent"
  improvements; ≤10 shows high variance and local optima; larger is better
  with diminishing returns. A concrete number, which is unusual for this kind
  of method.
- Also applied to deep RL (FuN on Atari) and GANs, with gains in both.
- Decentralised and asynchronous by construction — no central scheduler.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Weight copying makes mid-training hyperparameter evaluation cheap | strong | the method works at all, which requires it |
| C2 | PBT beats a well-tuned fixed-hyperparameter baseline | moderate | one strong instance (Transformer), plus RL and GAN results |
| C3 | The gain comes substantially from *adaptivity*, not better search | moderate | the recovered schedule is the evidence, and it is suggestive rather than isolated |
| C4 | Population ≥ 20 suffices | moderate | measured on one task (FuN/Atari) |
| C5 | The method is domain-general | moderate | three domains, all 2017-scale |

## Method

Run `N` workers. Each trains normally and periodically: evaluate; if in the
bottom fraction of the population, copy a better member's weights and
hyperparameters; perturb the hyperparameters (multiplicative jitter); continue.
Asynchronous, so no worker waits.

## Concepts

- **Exploit/explore on a population of partially trained models** — the
  mechanism, and the part that generalises.
- **A hyperparameter schedule as the search output** — the reframing. Search
  normally returns a point; PBT returns a trajectory.
- **Selecting on a proxy metric to avoid overfitting the reported one** — a
  methodological move the GAN experiment makes deliberately and states.

## Connections

An ancestor of µP-style approaches in goal only: both want to stop sweeping,
and they take opposite routes — µP makes the optimum transfer analytically,
PBT finds it empirically and lets it move. The learning-rate schedule PBT
rediscovers is `SOTA-008`'s warmup and the decay literature, arrived at by a
process that had no prior about either.

## Recommendations

- **R1** — When a hyperparameter search is expensive, evaluate candidates from
  partially trained weights rather than from scratch. *Topic:* training
  optimization. *Strength:* moderate.
- **R2** — Ask whether the hyperparameter should be a schedule before
  searching for its value. *Strength:* moderate, and the more interesting half.
- **R3** — Select on a proxy, report on the target. *Topic:* analysis and
  evaluation. *Strength:* strong, and it costs nothing.

## Bearing on the record

<!-- inactive-ok-block: SOTA-144, SOTA-159 — both Proposed, and named as the record's alternative rather than relied on -->
**Nothing is sourced to this paper and this reading files no practice.** PBT's
economics do not survive the move to frontier scale: a population of 20–40 runs
is the reason. The record's answer to the same problem is µP (`SOTA-144`,
`SOTA-159`) — transfer the hyperparameters analytically from one small sweep
instead of running many large ones.

Worth keeping for R2, which is orthogonal to that and still unaddressed: the
record has practices about *what* to set several hyperparameters to and few
about which of them should be moving.

The document's takeaways — "automated hyperparameter optimization",
"population-based training strategy", "dynamic adaptation of hyperparameters",
"combines evolution and training" — are true, generic, and one of them is the
title restated.

## Limitations

- 2017 scales, and the cost model is the problem: `N` concurrent runs is
  affordable for a small Transformer and not for a large one.
- Greedy. The paper says so, and the population-size finding is the mitigation.
- Weight copying's failure boundary is never characterised.
- C3 — that adaptivity rather than search is doing the work — is argued from
  one recovered schedule.

## Open questions

- Is there a scale-free version? The insight (partially trained weights are a
  valid initialisation) does not obviously require a population of 20.
- Which of the record's fixed hyperparameters are fixed only because nobody
  looked for a schedule? PBT's own answer for learning rate turned out to be
  the one the field already used, which is either reassuring or a warning that
  the method rediscovers priors.
