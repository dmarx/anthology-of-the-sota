---
# inactive-ok: LIT-044 — Rejected, and this document is the reading that says why the paper is in the attic and what survives it
paper: LIT-044
status: Read
title: 'Contrastive Learning with Hard Negative Samples'
version: 1
tags:
- training-optimization
date: '2026-09-09'
summary: >-
  Samples hard negatives without labels by reweighting the contrastive objective rather than changing the sampling procedure — two extra lines of code, no computational overhead — with a tunable hardness knob. The knob exists because harder negatives are more likely to be false negatives, so hardness trades learning signal against contamination.
---

# NOTE-tmpspi68: Contrastive Learning with Hard Negative Samples

## Contribution

Hard negatives help metric learning, and contrastive learning cannot use the
standard strategies because they need true similarity information and the setting
is unsupervised. This paper builds a **tunable sampling distribution over
negatives that prefers currently-similar pairs**, without labels, using two
ingredients: positive-unlabeled learning to correct for false negatives, and
importance sampling to make it cheap.

The implementation is the selling point: **reweight the objective instead of
modifying the sampling procedure**, which costs "only two extra lines of code"
and **no computational overhead**.

## Key insight

The hardness knob is not a convenience, it is forced by a real tension, and the
paper states it precisely: **the hardest negatives are the points closest to the
anchor, and those are exactly the ones most likely to share the anchor's label.**
The false-negative correction is only approximate, so its residual error grows
with hardness. Hardness therefore trades a better learning signal against
increasing contamination, and the right setting is interior.

The limiting cases make the family legible: turn hardness fully down and you
recover the earlier debiased-contrastive method; push it up and you get a
representation that "tightly clusters each class and pushes different classes as
far apart as possible".

## Assumptions

- **Class priors are estimable well enough** for the positive-unlabeled
  correction — the standard assumption of that literature.
- Representation similarity is a usable proxy for "hard", which is circular
  during early training and works anyway.
- Image and other modalities at 2020 self-supervised scale.

## Key results

- **Improves downstream performance across multiple modalities**, with a
  two-line implementation and no overhead.
- Concrete instance: **MoCo-v2 on CIFAR-10 linear readout 88.08% → 88.47%** with
  hard negatives at `β = 0.2`, `τ⁺ = 0`, 200 epochs, batch 128. Small.
- The hardness parameter recovers a prior method at one extreme and a
  maximally-separated representation at the other.
- Theoretical bounds relating the loss to downstream classification error.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Hard negatives improve unsupervised contrastive representations | moderate | consistent direction, modest margins |
| C2 | Hardness can be tuned without labels | strong | the construction |
| C3 | Hardness trades signal against false-negative contamination | strong | argued from the geometry; it is why the knob exists |
| C4 | Reweighting is equivalent to resampling here, at zero cost | strong | the importance-sampling derivation |
| C5 | The method generalises across modalities | moderate | demonstrated on several, all small |

## Method

Reweight each negative's contribution to the contrastive loss by a factor
increasing in its current similarity to the anchor, with a debiasing correction
from positive-unlabeled learning, and a hardness parameter controlling the
strength.

## Concepts

- **Reweight instead of resample** — the implementation trick, and general:
  an importance weight can stand in for a sampling distribution wherever the
  loss is an expectation.
- **Hardness as a contamination trade** — C3, and the reason "use harder
  examples" is never unconditional advice.
- **A knob whose extremes are two known methods** — a good way to present a
  family.

## Connections

<!-- inactive-ok-block: LIT-057, LIT-092 — Rejected, and named as a paper this one argues with; each has its own reading saying why it is in the attic -->
`LIT-057`, in the same batch, manipulates the **views**; this manipulates the
**negatives**; and both hit the same wall — without labels you cannot guarantee
what you are preserving or excluding. `LIT-092`, also here, argues that reasoning
of this kind cannot predict downstream performance anyway, because the function
class and optimiser are missing from it.

<!-- inactive-ok-block: SOTA-124 — Proposed, named as a parallel shape of reasoning rather than relied on -->
C3 is the same shape as the record's data-repetition reasoning in `SOTA-124`:
a resource helps up to the point where its downside dominates, and the practice
is about locating that point rather than about the direction.

## Recommendations

- **R1** — Prefer an importance weight to a change in sampling when the loss is
  an expectation; the effect is the same and the cost is nothing. *Topic:*
  training optimization. *Strength:* strong, and general.
- **R2** — Where "harder examples" is proposed, ask what makes them hard and
  whether that also makes them wrong. *Strength:* strong — C3 is the clean
  statement of it.
- **R3** — Present a method as a family whose extremes are known methods.
  *Strength:* moderate; a presentational point that makes a contribution
  checkable.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice**, and the
document is `Rejected`. Unsupervised contrastive learning at 2020 image scale is
not a line the anthology tracks, and the CIFAR-10 margin here is 0.39%.

R1 is the transferable finding and it is not about contrastive learning at all:
**reweighting and resampling are interchangeable when the objective is an
expectation, and reweighting is free.** That applies to data mixing, to
curriculum ordering and to any place the record recommends changing what a model
sees.

R2 is the second: the record has several practices that recommend more of
something difficult, and this is a clean statement of why such advice needs a
ceiling.

The document's takeaways — "importance of negative sample selection", "mining
strategies comparison", "impact on representation quality", "implementation
efficiency" — describe a survey. **"Mining strategies comparison" is wrong**:
this paper proposes one method and derives a family around it; it does not
compare mining strategies.

## Limitations

- Small models and datasets; MoCo-v2/CIFAR-10 gains under half a point.
- The false-negative correction is approximate by construction, and its residual
  is what limits the method.
- Class-prior estimation is assumed.
<!-- inactive-ok-block: LIT-092 — Rejected, and named as a paper this one argues with; each has its own reading saying why it is in the attic -->
- `LIT-092` argues the whole augmentation-and-objective framing is insufficient.

## Open questions

- Where is the hardness optimum, and does it move with scale? The knob is the
  contribution and the paper gives settings rather than a rule.
