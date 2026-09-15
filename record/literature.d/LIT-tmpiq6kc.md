---
status: Active
title: 'Beyond the Best Guess: Improving LLM Solution Coverage with Evolution Strategies'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
published: '2026-08-01'
arxiv: '2608.12679'
first_author: 'Hayes'
keywords:
- 'evolution-strategies'
- 'pass-at-k'
- 'test-time-scaling'
- 'solution-coverage'
- 'distribution-collapse'
# The same group as LIT-211 — Cognizant AI Lab, with Qiu as a shared author —
# applying that paper's method. `extends:`, and NOT an independent
# replication of it; SOTA-154's promotion condition excludes exactly this.
extends:
- LIT-211
implementations: []
summary: >-
  Hayes et al. (2026), [ARXIV-2608.12679](https://arxiv.org/abs/2608.12679). Takes evolution strategies up to 32B
  and asks one question: what does post-training do to the breadth of the
  output distribution? RL raises pass@1 and lowers pass@k, eventually below
  the base model; ES raises both, and never falls below base at any k or scale
  tested. The mechanism is visible in the accuracy histogram — RL increases
  the number of prompts solved in none of k samples, putting a hard ceiling on
  pass@k that no extra sampling can lift.
---

# LIT-tmpiq6kc: Beyond the Best Guess: Improving LLM Solution Coverage with Evolution Strategies

Hayes et al. (2026) — [ARXIV-2608.12679](https://arxiv.org/abs/2608.12679)

## Key takeaways

**The claim is about the shape of the output distribution, not about a
benchmark number.** RLVR sharpens the model around high-reward outputs, which
raises pass@1 and narrows coverage; ES raises pass@1 *without* narrowing.
Across Qwen2.5-Instruct at 1.5B, 3B and 7B and Qwen3 at 1.7B, 4B and 8B, ES
beats RL on pass@k with a crossover typically around k=4, after which RL's
curves plateau and ES's keep climbing.

**The most striking single result is RL losing to its own base model.** For
the Qwen2.5-Instruct models the base model overtakes the RL checkpoint at
sufficiently large k. ES never falls below base at any k or any scale tested.

**It runs at 14B and 32B, against real RL checkpoints.** ES-at-Scale applied
to Qwen2.5-Math-7B, Qwen2.5-14B and Qwen2.5-32B, compared on MATH500,
OlympiadBench and Minerva against **OatZero and SimpleRL-Zoo** — published RL
checkpoints rather than the authors' own RL runs. The advantage holds and on
Minerva at 32B the gap grows with k. This is the largest scale at which this
record has evidence for the ES line.

**The mechanism is legible in the accuracy histogram.** Binning prompts by the
fraction of k responses that are correct: RL increases the mass in the
all-correct bin, as its objective intends, **and also increases the mass in
the all-wrong bin relative to the base model.** Prompts the base model could
sometimes solve become ones it never solves. That is a hard ceiling on pass@k
that no amount of further sampling can overcome. ES reduces the all-wrong
mass instead, and spreads its gains across the partially-correct bins.

**Progressions and regressions are the honest way to count this.**
Progressions are prompts the base model got wrong and the tuned model gets
right; regressions are the reverse. The paper's point is that pass@1 nets
these together and hides the regressions, and that a method can look better on
pass@1 while destroying capability it will never get back.

## What the evidence does not cover

**This is the same group as [LIT-211](LIT-211.md) and it is not an independent
replication.** Cognizant AI Lab, with Qiu among the authors on both, applying
that paper's own ES-at-Scale method. It extends the *scale* of the evidence
enormously — 32B against published RL checkpoints — and it extends the *kind*
of claim to coverage. It does not add a second group, and
[SOTA-154](../practices.d/SOTA-154.md)'s promotion condition excluded "further results from the same
group" for exactly this reason. What makes the coverage finding credible
beyond one lab is [LIT-tmp81or2](LIT-tmp81or2.md), which reports the same shape independently.

**The comparisons at 14B and 32B are against third-party checkpoints**, not
against RL runs matched to the ES budget. That is a fair way to ask "does ES
beat what people actually ship" and not a controlled comparison of the two
methods under one protocol.

**Mathematical reasoning throughout**, on verifiable-answer benchmarks. The
discovery framing — science, open conjectures — is motivation rather than
something measured here.

## Standing in the anthology

<!-- inactive-ok-block: SOTA-129 is Active and named as the recipe stage this
     paper's finding bears on -->
**The finding that makes coverage collapse a property of RLVR rather than of
one RL implementation.** The paper's math experiments span multiple RL
algorithms and published checkpoints and see the same earlier pass@k
saturation each time, which is what licenses reading it as a consequence of
the RLVR objective rather than of any one optimizer. That bears directly on
[SOTA-129](../practices.d/SOTA-129.md), which makes RLVR the third stage of the reasoning recipe: the
stage does what it says, and it costs something the recipe never accounted
for.

Together with [LIT-tmp81or2](LIT-tmp81or2.md) it is the evidence behind the record's new
evaluation practice — that a post-training result reported only at pass@1 is
not enough to tell an improvement from a narrowing.
