---
number: 102
status: 'Active'
title: 'Implement dynamic temperature scaling for mixing'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
published: '2023-12-01'
source:
- LIT-117
summary: >-
  Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).
---

# SOTA-102: Implement dynamic temperature scaling for mixing

## Source

Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).

## The source uses a bandit, not a temperature

Temperature-based mixing — raising domain proportions to a power to sharpen or
flatten them — is a real and widely used technique, and it is not [LIT-117](../literature.d/LIT-117.md)'s.
ODM's mechanism is a **multi-armed bandit**: each domain is an arm, the reward
is derived from perplexity on the batches training is already taking, and the
sampling distribution follows from the bandit's exploration policy rather than
from a temperature applied to fixed weights.

The two are not interchangeable. A temperature reshapes a distribution somebody
already chose; a bandit *discovers* the distribution and keeps revising it. The
practice as written asks for a knob on the first while citing the paper that
argues you should not have to choose the weights at all.

## What this needs

Either a source that actually recommends dynamic temperature scaling, or
restatement as what [LIT-117](../literature.d/LIT-117.md) does — allocate sampling across domains online
from a measured reward. The second is already [SOTA-103](SOTA-103.md)'s territory, which
suggests these two are one practice split in the import rather than two.

Flagged rather than retired: unlike the four retired from the [LIT-051](../literature.d/LIT-051.md) cluster,
this names a technique that exists and works. What it lacks is this paper as
evidence for it.
