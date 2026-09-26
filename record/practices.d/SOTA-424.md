---
number: 424
status: Active
formerly:
- SOTA-tmpfci2h
consensus: universal
consensus_note: >-
  Not doing this is what needs justifying. Every text-to-image diffusion model
  this record can name ships it — Stable Diffusion, Imagen, and the `diffusers`
  default — and the guidance weight is a user-facing control in consumer tools.
  `universal` is a statement about adoption rather than evidence (`DP-005`), and
  the evidence here is one paper plus everything built on top; what makes that
  acceptable is that the paper's own sweep is the thing being adopted, not a
  headline. Read as of 2026-09.
title: 'Train one network for both conditional and unconditional scores by dropping the condition on 10% of examples, then pick the guidance weight by which metric you are willing to lose'
version: 3
history:
- version: 2
  date: '2026-09-25'
  note: >-
    The capacity question this practice recorded as open is half answered
    by EDM2 (LIT-714): a separately trained unconditional model
    about a twelfth the size guided its largest conditional model as well as
    any larger one did. Also records EDM2's finding that the best EMA length
    moves strongly with the guidance weight, and that FID and FD_DINOv2
    choose different weights. Not a source: EDM2 does not train one network
    for both scores. Recommendation, status and consensus unchanged.
- version: 3
  date: '2026-09-25'
  note: >-
    Bounds two Conditions that were written as properties of guidance and are
    properties of *this* guidance. LIT-tmpbpv9d argues CFG's quality gain comes
    from the unconditional reference being a worse model, not from the class
    emphasis, and separates them: an unconditional model can be guided (11.67 to
    3.86 FID, where this practice says there is nothing to do), and the diversity
    loss goes with the class emphasis rather than with guidance. Recommendation,
    status and consensus unchanged — this practice is still how you get a CFG
    model — but "conditional generation only" and "diversity is what is being
    spent" now say which of the two they belong to.
tags:
- generative-modeling
- training-optimization
date: '2026-09-25'
source:
- LIT-693
introduced_by:
- LIT-693
implementations:
- 'Stable Diffusion'
- 'Imagen'
- 'diffusers'
summary: >-
  Ho and Salimans (2022), [LIT-693](../literature.d/LIT-693.md). Replace the conditioning with a null
  token on a fraction of training examples — **0.1 is the measured best**, with
  0.2 and 0.5 worse — so one network learns both scores, then extrapolate away
  from the unconditional estimate at sampling. The weight is not a quality dial:
  on ImageNet 64×64, `w` from 0.1 to 4.0 takes **FID from 1.55 to 26.22** and
  **IS from 66.11 to 260.2**. Choose it by which of those you are prepared to
  sacrifice, and never compare two models at different weights.
---

<!-- inactive-ok-file: SOTA-428 — Proposed; named as where the EMA side of the guidance sweep is held, not as support for this practice -->
# SOTA-424: Train one network for both conditional and unconditional scores by dropping the condition on 10% of examples, then pick the guidance weight by which metric you are willing to lose

## Source

Ho and Salimans (2022), [LIT-693](../literature.d/LIT-693.md) —
[ARXIV-2207.12598](https://arxiv.org/abs/2207.12598).

## What to do

**At training time.** With probability `p_uncond`, replace the conditioning
signal with a null token before computing the loss. One network, one training
run, both scores. Use **`p_uncond = 0.1`**: the paper's sweep puts the best
achievable FID at 1.55 for 0.1, against 1.62 for 0.2 and 1.91 for 0.5, so more
unconditional training costs and does not buy.

**At sampling time.** Combine the conditional and unconditional score estimates,
extrapolating away from the unconditional one by a weight `w`. There is no
classifier and no second model.

## Choosing `w`, which is the part that is usually got wrong

The weight is **not** a quality knob with a best setting. It is a position on a
trade, and the trade is steep. ImageNet 64×64 at `p_uncond = 0.1`, 50 000
samples per point:

| `w` | FID ↓ | IS ↑ |
| --- | --- | --- |
| 0.0 | 1.80 | 53.71 |
| **0.1** | **1.55** | 66.11 |
| 0.3 | 3.03 | 92.80 |
| 1.0 | 12.60 | 170.1 |
| 2.0 | 21.03 | 225.5 |
| **4.0** | 26.22 | **260.2** |

**FID degrades about 17-fold across the range while IS nearly quintuples.** So:

- want the best FID → `w` around **0.1 to 0.3**;
- want the best IS, or visibly sharper individual images → `w ≥ 4`;
- there is no setting that is best at both, and the paper does not claim one.

**Never compare two models at different `w`.** A guidance sweep can produce
almost any FID or IS you like from one checkpoint, so a comparison that does not
fix the weight is not a comparison. [SOTA-307](SOTA-307.md) says to search the scale per cell
and to report the search tolerance; this is the measurement that makes that
non-negotiable rather than fastidious.

## Conditions and costs

**The visible cost at high `w` is saturation.** The paper reports that strongly
guided samples "display saturated colors" at `w = 3.0`. That is the excursion
[SOTA-202](SOTA-202.md) exists for — predictions leaving the training range — so at high
guidance the two practices are used together, and [SOTA-410](SOTA-410.md) is the sampler
constraint that makes the clamp available.

**Conditional generation only — for *this* recipe, not for guidance.** There has
to be a condition to drop, so nothing in the training change above applies to an
unconditional model.
<!-- inactive-ok: SOTA-397, SOTA-tmpj70gp — both Proposed, named as the two places a reader goes when this practice's precondition fails; a scope boundary is where a not-yet-in-force holding is the right thing to point at. -->
[SOTA-397](SOTA-397.md) is the record's holding on conditioning a
<!-- inactive-ok: SOTA-tmpj70gp — Proposed, and named as the guidance that needs no condition, i.e. the far side of this practice's own scope boundary; not support for its recommendation. -->
model trained without one, and [SOTA-tmpj70gp](SOTA-tmpj70gp.md) is guidance that needs no condition at
all — it reaches unconditional EDM2-S from FID 11.67 to 3.86, a regime this
practice excludes.

**A capacity question the paper does not answer.** One network now represents two
distributions. The sweep over `p_uncond` bounds how much unconditional training
is useful and says nothing about whether a larger model would prefer a different
split, or whether the conditional score is worse than it would have been from a
dedicated model.

EDM2 ([LIT-714](../literature.d/LIT-714.md)) answers the half of this that concerns the unconditional
score, from the other design: it trains the unconditional model **separately**,
and an XS model (125M parameters) guides its XXL conditional model (1.5B) as
well as any larger unconditional model did — "using a larger unconditional
model did not improve the results at all" — at almost half the sampling cost of
guidance. One table, one conditional model, ImageNet-512. It says the
unconditional score needs far less capacity than the conditional one; it does
not say whether sharing one network, as recommended here, costs the conditional
score anything.

**The weight is not the only thing guidance moves.** EDM2 also finds the best
EMA length depends "very strongly" on the guidance weight, and that FID and
FD_DINOv2 disagree on the weight itself (1.4 against 1.9 in EDM2's convention,
where 1 means no guidance — 0.4 against 0.9 on this practice's scale). A weight swept at one
EMA length and reported at another is not the sweep it claims to be; the EMA
side is [SOTA-428](SOTA-428.md).

**Diversity is what is being spent, and it is the class emphasis that spends
it.** The paper is explicit that raising the weight decreases sample variety and
increases individual fidelity, and for this recipe that trade is real: plan for it
if your application needs coverage, because the default high weights consumer tools
ship are the wrong end of it.

What [LIT-tmpbpv9d](../literature.d/LIT-tmpbpv9d.md) adds is that the trade is **not a property of guidance**. It
argues the quality gain comes from the unconditional reference model being a worse
fit — a harder task on a smaller training budget — and the diversity loss from the
class emphasis, and it separates them by swapping the reference for a degraded copy
<!-- inactive-ok: THEORY-tmput07n — Proposed, cited as the account of why this practice's diversity cost belongs to the class emphasis rather than to guidance; its being an open account is why this practice's recommendation is unchanged. -->
of the conditional model. [THEORY-tmput07n](../theory.d/THEORY-tmput07n.md) is the account. So the sentence to carry
forward is not "guidance costs diversity" but "*this* reference model costs
diversity".

## Known implementations

- **Stable Diffusion**, where the weight is user-facing and typically defaulted
  around 7.5.
- **Imagen**, which pairs it with the thresholding of [SOTA-202](SOTA-202.md).
- **diffusers**, as `guidance_scale`.
