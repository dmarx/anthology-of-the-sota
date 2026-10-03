---
number: 121
status: Proposed
formerly:
- THEORY-tmpko5v1
promote_when: >-
  A second group, on another backbone, distils one teacher by distribution
  matching alone and by consistency at the same step count, with guidance
  swept from none, and tables a coverage measure (recall, or a diversity
  score that is not a Fréchet distance) for each arm. The account predicts
  the distribution-matching arm loses recall at guidance 1, where guidance
  cannot be the cause. sCM's Fig. 7 already shows that once, as curves read
  by eye, from the authors of the consistency method. A further test would
  separate the direction of the divergence from DMD's own account (score
  scale invariance and low-noise score error), for example by a
  distribution-matching run restricted to high noise levels. Neither an FID
  table nor samples would settle it.
title: "Distribution-matching distillation loses coverage because it descends a reverse divergence on the student's own samples, and a consistency term on teacher trajectories restores it"
version: 1
tags:
- generative-modeling
- few-step-generation
date: '2026-10-03'
source:
- LIT-790
- LIT-783
- LIT-643
- LIT-646
explains:
- SOTA-447
summary: >-
  Lu and Song (2024), [LIT-790](../literature.d/LIT-790.md), Fig. 7, and Zheng et al. (2025),
  [LIT-783](../literature.d/LIT-783.md). DMD ([LIT-643](../literature.d/LIT-643.md)) descends KL(p_student ‖ p_teacher), evaluated
  on the student's own samples. That direction penalizes mass where the
  teacher has none and is indifferent to a mode the student no longer
  produces. A consistency loss supervises points along the teacher's
  trajectories that the student did not choose. On one backbone, sCM found
  distribution matching raising precision and losing recall as guidance
  rises, while consistency stayed near the teacher; read from the curves,
  the recall gap is already there at guidance 1. The account is rCM's
  framing. That figure is its only measurement, from one group and one
  backbone, and DMD's own authors give a different mechanism.
---

<!-- inactive-ok-file: SOTA-447 — Proposed, and declared in `explains:`; the practice this account underwrites. Explaining a practice not yet in force is the normal case. -->
<!-- inactive-ok-file: SOTA-394 — Proposed; named for its diversity condition, which rests on the claim this account states, not as settled advice -->
<!-- inactive-ok-file: THEORY-110 — Proposed; cited for why an FID table cannot settle this account, not as support for it -->

# THEORY-121: Distribution-matching distillation loses coverage because it descends a reverse divergence on the student's own samples, and a consistency term on teacher trajectories restores it

## Source

Lu and Song (2024), [LIT-790](../literature.d/LIT-790.md), §5.2 and Fig. 7. Zheng et al. (2025),
[LIT-783](../literature.d/LIT-783.md), §1, Fig. 2 and §4.1. Yin et al. (2023), [LIT-643](../literature.d/LIT-643.md), Eqs. 1–2
and §3.3. Yin et al. (2024), [LIT-646](../literature.d/LIT-646.md), App. B and Table 6.

## The account

**The objective's direction.** DMD ([LIT-643](../literature.d/LIT-643.md)) trains a one-step generator on
KL(p_fake ‖ p_real), the student's distribution against the teacher's
(Eq. 1). Its gradient is the difference of two scores, evaluated on noised
samples the generator itself produced (Eq. 2). The direction has a
standard consequence. The integrand is weighted by the student's density,
so the loss is large where the student puts mass the teacher lacks and
says nothing about a region the student has stopped visiting. Nothing in
the gradient pulls a dropped mode back.

**What a consistency term adds.** A consistency loss regresses the student
onto the teacher's ODE at points drawn along trajectories from data or
teacher noise, not from the student's own outputs. A mode the student has
lost still appears in the training points, and failing to reach it is
penalized. rCM ([LIT-783](../literature.d/LIT-783.md), §1, Fig. 2) frames the pair as forward
divergence, "mode-covering", on "external, offline" data, against reverse
divergence, "mode-seeking", on "self-generated, on-policy" samples. It
argues they are complementary, and on that basis keeps sCM's consistency
loss primary and adds DMD's at weight 0.01.

## What was measured

- **One controlled comparison on coverage.** sCM ([LIT-790](../literature.d/LIT-790.md), §5.2,
  Fig. 7) runs one-step variational score distillation, DMD's gradient
  without its regression term, against two-step sCD on one EDM2-M backbone
  at ImageNet-512, with VSD's weighting and proposal tuned, across a sweep of
  guidance scales. VSD "increases fidelity (as evidenced by higher precision
  scores) while decreasing diversity (as shown by lower recall scores)". The
  effect grows with guidance, "ultimately causing severe mode collapse".
  sCD's precision and recall stay comparable to the teacher's. The figure
  also plots one-step sCD and starts the sweep at guidance 1.0, so a
  matched comparison is in it, though only as curves. Read by eye, at
  guidance 1.0 one-step VSD's recall is near 0.65 against about 0.70 for
  one-step sCD and 0.72 for the teacher, and its precision is higher. The gap
  is present before any guidance is applied and widens with it. The figure
  also carries VSD + sCD, the two losses simply added. Its recall curves
  track VSD's, not sCD's, and the text does not discuss them.
- **One diversity number from the DMD line.** DMD2 ([LIT-646](../literature.d/LIT-646.md), App. B,
  Table 6) scores pairwise LPIPS over four images per prompt at 0.61, against
  0.64 for its SDXL teacher, and calls it "a slight degradation".
- **The repair is shown in samples.** rCM's diversity advantage over DMD2 is
  five videos per method (Fig. 1). Its pure-sCM arm, against which the DMD
  term is said to fix detail, is never tabled.

## What it explains

**[SOTA-447](../practices.d/SOTA-447.md)'s ordering of the two terms.** The practice adds a small
DMD term to continuous-time consistency distillation, and keeps consistency
primary. On this account the consistency term keeps coverage, and the
reverse term adds the fidelity pure consistency lacks at scale. Weighting
the reverse term small keeps its mode-seeking pull from dominating. sCM's
summed arm is the case the weighting avoids: added at equal weight, the
combination's recall follows VSD's. rCM's weight of 0.01 was chosen from
VBench and samples, not from that figure, so this is the account's reading
of why a small weight works, not rCM's stated reason.

It also states the mechanism [SOTA-394](../practices.d/SOTA-394.md)'s diversity condition takes from
CausVid, that the diversity loss of a DMD-distilled video student is
"characteristic of reverse KL". The account does not touch that practice's
recommendation, which is about the teacher's attention mask.

## What this does not say

- **That guidance plays no part.** Guidance trades recall for precision on
  its own, and sCM describes VSD's artifacts as "similar to those from
  applying large guidance scales". DMD2's SDXL real score runs at guidance
  8. sCM's curves put part of the gap at guidance 1.0 and show guidance
  widening it, so on that one figure both contribute. In DMD2's diversity
  number they are not separated at all.
- **That DMD's authors agree.** [LIT-643](../literature.d/LIT-643.md) never says "reverse KL" or
  "mode-seeking". It puts its mode-dropping risk on the score being
  "invariant to scaling of probability density" and on the real score being
  unreliable at low noise. It adds its regression loss "to ensure all modes
  are preserved", on the evidence of a 2-D toy and one image grid. That is a
  rival account of the same symptom, and a regression onto teacher outputs
  is a forward-direction term on either reading.
- **That the reading is precise.** The values above are read off a plot.
  The text states only the direction, and there are no seeds.
- **That FID could settle it.** FID weights coverage more than fidelity
  ([THEORY-110](THEORY-110.md)), so a distiller that lost recall and gained precision can
  move FID either way. DMD2 and DMAD ([LIT-770](../literature.d/LIT-770.md)) each find that a real-data
  adversarial term alone gives their best SDXL FID and worst CLIP score.
  DMAD measures no diversity at all.
- **That the student's samples are the only reason.** DMD2 found that
  distribution matching without the regression loss oscillated until the
  fake score was updated five times per generator step ([LIT-646](../literature.d/LIT-646.md), Table 3).
  A critic that lags the generator is a further way an on-policy objective
  can drift, and it is not separated from mode-seeking either.
