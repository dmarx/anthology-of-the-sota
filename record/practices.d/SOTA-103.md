---
number: 103
status: 'Active'
title: 'Adjust data mixing proportions online from per-domain training loss'
version: 2
history:
- version: 2
  date: '2026-09-09'
  # inactive-ok-block: SOTA-102 — Superseded into this practice by this same
  # change; naming it is the point of the note
  note: >-
    Retitled from "Adjust mixing ratios based on validation performance"
    after reading the source (#114). The loop was right and the signal was
    wrong: ODM's reward is the per-domain training loss on the batch
    already drawn, and avoiding a validation pass is the entire basis of
    its efficiency claim. SOTA-102 is superseded into this, since the two
    were one practice split in the import.
tags:
- data-pipeline
date: '2026-08-24'
published: '2023-12-01'
source:
- LIT-117
compared_against:
- SOTA-102
summary: >-
  Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).
---

# SOTA-103: Adjust data mixing proportions online from per-domain training loss

## Source

Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).

## The method

Group the corpus into domains. Treat each domain as the arm of a multi-armed
bandit, and the **per-domain training loss on the batch you just took** as the
reward. Update the sampling distribution at every step. [LIT-117](../literature.d/LIT-117.md) uses Exp3,
whose policy is a Gibbs distribution over importance-weighted rewards mixed
with a uniform distribution for exploration:

    πₜ(Dᵢ) = (1 − K·ℰₜ) · exp(ℰₜ₋₁·R̂ᵢ) / Σⱼ exp(ℰₜ₋₁·R̂ⱼ)  +  ℰₜ

At 1B parameters over 50B tokens from 22 Pile domains: the next best method's
final perplexity in **19% fewer iterations**, **+1.9% relative** on 5-shot
MMLU, and negligible added wall-clock time.

## Why the signal has to be the training loss

This practice read "adjust mixing ratios based on **validation performance**"
until [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114). That is the natural-seeming choice and it is the wrong one,
for a reason worth writing down rather than rediscovering.

A validation-driven loop needs held-out data per domain and a forward pass
over it at every adjustment. That is expensive enough that the update interval
becomes coarse — and a coarse interval cannot track a quantity that moves
during training, which is the only reason to be online at all. The training
loss is already computed to take the step, so the reward is free and the
interval can be every step. Avoiding the validation pass is not an
optimisation of this method; it is the method.

## What the signal is and is not

It is **learnability**, not quality. The authors' argument is
information-theoretic — perplexity is expected information gain, so sample
most from the domain with most left to learn — and it has a failure mode the
paper does not test: noise also has high loss. A loss-driven sampler
preferentially feeds on whatever it understands least, and cannot distinguish
rare valuable text from garbage.

## Conditions

The domain partition is an **input**, not something the method learns. ODM
optimises proportions over a grouping someone else chose, and a bad grouping
caps what it can do.

The evidence is 1B parameters, 50B tokens, one corpus. Whether an online
mixture still pays against a modern curated mixture — where the hand-set
proportions already encode substantial prior work that a bandit would discard
and rediscover — is untested and is the question a reader should ask first.
