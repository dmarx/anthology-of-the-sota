---
number: 48
status: Active
formerly:
- THEORY-tmp5y2y6
title: 'Randomizing individuals estimates an individual quantity, and when the units interact the collective effect is not the sum of it — so a null from such a trial is not evidence of no effect'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-482
explains:
- SOTA-291
summary: >-
  Bak-Coleman et al. (2025), [LIT-482](../literature.d/LIT-482.md) — four named reasons an
  individual-level randomized trial fails to estimate a collective effect:
  non-linearity across scale, hysteresis, feedback in time, and violation of
  the stable unit treatment value assumption through the network. The power
  grid shows the first and the last together: treat too few and the system
  absorbs it, treat enough and the controls fail too.
---

# THEORY-048: Randomizing individuals estimates an individual quantity, and when the units interact the collective effect is not the sum of it — so a null from such a trial is not evidence of no effect

## Source

Bak-Coleman, Lewandowsky, Lorenz-Spreen, Narayanan, Orben and Oswald (2025),
[LIT-482](../literature.d/LIT-482.md) — read as [NOTE-230](../notes.d/NOTE-230.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-291](../practices.d/SOTA-291.md) | evaluate a specific intervention, not the net effect, and do not read an individual-level null as absence | not caution about noisy measurement but a mismatch between the design's estimand and the question's, with four separable causes |

## The account

The question is usually collective: does this system change polarization,
mental health, vaccine uptake. The trial is usually individual: randomize
users, compare arms. The step between them assumes the collective effect over
a long period equals the sum of individual effects over a short one, and in a
system whose units interact that assumption is false in four separable ways.

**Non-linearity across scale.** The clearest demonstration is a power grid
where demand spikes are randomized across substations. Treat a small share and
the grid absorbs the load — no difference between arms. Treat a large enough
share and the grid fails, blacking out **the control substations too** — again
no difference. The same null appears from either side of a real effect,
because the quantity estimated was never the quantity of interest.

**Hysteresis.** The system's response depends on its history, so removal is
not the inverse of addition. Relieve the load after a blackout and nothing
comes back on; that does not show load was innocent. This is the structural
objection to **every withdrawal design** — deactivation studies, reduced-use
studies, feature-removal studies — each of which reads the effect of having
the thing as the negative of the effect of taking it away. Stop a long-time
language learner for a week, find their fluency intact, conclude the app does
not teach.

**Feedback in time.** Effects are non-monotonic and depend on when you look.
Two weeks of smoking cessation produces irritability and weight gain; by the
reasoning common in this literature that establishes smoking as a way to lose
weight and relax. And where the system learns from behaviour — which is what a
recommender does — the object under study changes during the study, so trials
of different durations should be *expected* to disagree rather than
reconciled.

**SUTVA violation.** The stable unit treatment value assumption requires one
unit's outcome not to depend on another unit's treatment. Assign someone a
chronological feed and they still receive algorithmically-ranked content,
because their neighbours share what the algorithm showed them. Take one
teenager off a platform and their outcome still depends on whether their
friends left too. Escaping this requires randomizing entire subnetworks, and
the source reports that no trial in this literature does.

Two of the four — hysteresis and SUTVA — are structural rather than
empirical. A withdrawal study assumes a symmetry that a path-dependent system
does not have, and a trial whose units interact is not estimating what its
design says it estimates. Neither can be fixed by a larger sample.

## Why `Active`

Because the mechanisms are established and the application is a derivation
rather than a conjecture. SUTVA is a stated assumption of the design; either
it holds or the estimate is not what the design claims. Hysteresis is a
property of the system, and the inference withdrawal studies make from it is a
symmetry assumption that can be written down and seen to be unwarranted.

The status is about the account. [SOTA-291](../practices.d/SOTA-291.md) is `Proposed`,
because a sound reason not to trust a design is not by itself evidence that a
different programme works.

## What this does not say

**It does not say these trials are worthless**, and the source's "bound to be
of limited value" is a judgement rather than a result. Nothing here quantifies
the distortion in any specific published study, and a narrower estimand — the
short-run individual effect — is estimated perfectly well by the design that
estimates it.

**It does not say the effects are large, or that they exist.** The claim is
that a null from this design is uninformative about the collective question,
which is symmetric: it is equally not evidence that the effects are real.

**It is not specific to social media, and the record should not file it as
though it were.** The argument concerns randomizing interacting units and
asking about an aggregate. Every deployed recommender, ranking system and
assistant at population scale has that shape, and an offline benchmark
measuring a model that will be deployed into a population that interacts has
something of it too — which is a reading rather than a result, and nobody has
made it.

**And the positive programme is a separate claim.** That evaluating specific
affordances continuously is better is argued from three advantages, and no
result establishes it.
