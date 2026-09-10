---
number: 102
status: Superseded
superseded_by: SOTA-103
status_note: >-
  Names a real component of ODM's policy imprecisely rather than something
  the paper does not do — the two were one practice split in the import,
  and SOTA-103 now describes the whole method
title: 'Implement dynamic temperature scaling for mixing'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Superseded by SOTA-103 after reading the source (#114), and the body's
    central argument is corrected. It claimed a temperature and a bandit
    are different kinds of thing; Exp3's policy is a tempered softmax whose
    exploration rate is the inverse temperature, so this named a real part
    of ODM imprecisely rather than naming something absent from the paper.
tags:
- data-pipeline
date: '2026-08-24'
source:
- LIT-117
summary: >-
  Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).
compared_against:
- SOTA-103
---

# SOTA-102: Implement dynamic temperature scaling for mixing

## Source

Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).

## The temperature is real, and it is inside the bandit

This practice's body used to argue that a temperature and a bandit are
different kinds of thing — "a temperature reshapes a distribution somebody
already chose; a bandit *discovers* the distribution". Reading [LIT-117](../literature.d/LIT-117.md) for
[#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) shows that is wrong about this bandit.

Exp3's policy is a **Gibbs distribution** — a softmax over importance-weighted
rewards — mixed with a uniform distribution for exploration:

    πₜ(Dᵢ) = (1 − K·ℰₜ) · exp(ℰₜ₋₁·R̂ᵢ) / Σⱼ exp(ℰₜ₋₁·R̂ⱼ)  +  ℰₜ

The exploration rate `ℰₜ` multiplies the reward inside the exponent, which is
exactly the role an inverse temperature plays, and it varies over training.
So "dynamic temperature scaling for mixing" is an imprecise name for something
ODM genuinely has.

## Why superseded rather than rejected

Because it names a component, not a practice. The temperature is one term in
a policy whose other parts — the domain arms, the training-loss reward, the
importance weighting — are what make the method work, and a recommendation to
tune the temperature alone would be advice about a knob detached from the
machine it belongs to.

[SOTA-103](SOTA-103.md) now describes the whole method, which is what the two of these were
between them. The record's older body already suspected this, saying the two
"are one practice split in the import rather than two". That was right; the
reason given for it was not.

## The correction is the point

Two of the three retirements in this cluster stand on the paper containing a
string zero times. This one does not, and it would have been retired on the
same evidence if the reading had stopped at a keyword search. The word
`temperature` appears nowhere in [LIT-117](../literature.d/LIT-117.md); the mechanism it names is in
equation form on the page.
