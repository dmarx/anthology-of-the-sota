---
number: 213
status: Proposed
formerly:
- SOTA-tmpdcmgg
promote_when: >-
  Anchored Weight Decay reproduced by a group unconnected to the authors, or
  adopted in a released ES post-training recipe. What would not satisfy this:
  a further demonstration that ES drifts, or that a larger population reduces
  it — both are already established and neither says the cheap remedy works.
consensus: emerging
consensus_note: >-
  The mechanism has two groups behind it (LIT-235 derives the scaling,
  LIT-238 measures the population dependence and confirms it), and the
  population knob follows from it directly. The anchor penalty has one group
  and one paper, from the lab whose method the criticism was aimed at.
title: 'Control evolution-strategies drift with a larger population or an anchor penalty, not by stopping training early'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
source:
# LIT-238 is primary: it is the paper that measures the population
# dependence, introduces the cheap remedy, and shows why the obvious
# alternative — stopping early — is the wrong move.
- LIT-238
- LIT-235
- LIT-237
# The third arrival at the population knob, from the curvature side: larger N
# raises the terminal plateau and suppresses late-time degradation. It is also
# the source of the target-reward stopping rule below, which is a different
# claim from the prior-task one this practice rejects.
- LIT-236
introduced_by:
- LIT-238
extends:
- SOTA-154
implementations: []
summary: >-
  Schweighofer et al. and Liang et al. (2026), [LIT-238](../literature.d/LIT-238.md) and
  [LIT-236](../literature.d/LIT-236.md), on the scaling Hoy et al. derived
  in [LIT-235](../literature.d/LIT-235.md) — ES drift is a random walk whose size falls with population
  size, so raising the population from 30 to 128 halves the update norm and
  monotonically reduces prior-task degradation. Anchored Weight Decay buys the
  same reduction at population 30 for 1-2% runtime. Do not stop early instead:
  the prior-task dip is often transient and recovers by the end of training.
explained_by:
- THEORY-007
---

# SOTA-213: Control evolution-strategies drift with a larger population or an anchor penalty, not by stopping training early

## Source

Schweighofer et al. (2026), [LIT-238](../literature.d/LIT-238.md) — [ARXIV-2605.30148](https://arxiv.org/abs/2605.30148); Hoy et al.
(2026), [LIT-235](../literature.d/LIT-235.md) — [ARXIV-2604.01499](https://arxiv.org/abs/2604.01499); Abdi et al. (2026),
[LIT-237](../literature.d/LIT-237.md) — [ARXIV-2601.20861](https://arxiv.org/abs/2601.20861).

## What is being controlled, and why it has a knob

[THEORY-008](../theory.d/THEORY-008.md) is the account. An ES update splits into a component that
changes the loss and one that cannot, and the second is a random walk whose
squared norm grows as `σ²dT/N`. Two of those four terms are budget decisions,
which is what makes this a practice rather than an observation:

- **Population size divides it.** Raising `N` from 30 to 128 cuts the update
  norm by about half, and prior-task degradation falls monotonically across
  30, 128 and 256 ([LIT-238](../literature.d/LIT-238.md), Table 1).
- **Steps multiply it.** Which is why the temptation is to stop early, and
  why that turns out to be wrong.

## Do not stop early — the dip usually recovers

This is the correction, and it is the reason to read the sources rather than
the mechanism. [LIT-237](../literature.d/LIT-237.md) ran Countdown for 500 iterations and watched
average prior-task accuracy fall throughout, which reads as a clear argument
for stopping once the target task converges at around 200.

Tracking the prior tasks *individually* rather than averaged tells a different
story. HellaSwag falls about **8% over the first 300 iterations and returns to
its original level by the final iteration**; MMLU-Pro and ARC-Challenge do the
same; ProofWriter does the mirror image, improving and then settling back
([LIT-238](../literature.d/LIT-238.md)). The degradation is transient drift, not irreversible
forgetting — and **a stopping rule fitted to the average would stop at the
bottom of the dip**, which is the worst point available.

Two further findings from the same paper narrow the problem rather than the
method. Forgetting is **not specific to ES**: with ProofWriter as the target,
GRPO forgets considerably, mostly on GSM8K. And varying target task, model
family and model size produces **no significant dependence** on any of them.

## Anchored Weight Decay

The remedy that does work, and it is four lines of change. Add a penalty on
`w − w₀` to the objective; since there is no loss to backpropagate, apply it
as a decay directly in the update rule — take the standard ES step, then pull
the weights back toward the initial parameters.

At population 30, this brings the update norm down to roughly what population
128 achieves, and closes the prior-task KL gap to GRPO. Cost: the reference
weights must be available each iteration, streamed layer-wise from pinned RAM
rather than held in VRAM, for a measured **1–2% runtime** overhead — against
the 4× evaluation cost of getting the same effect by quadrupling the
population.

**Tuning, as a procedure rather than a range.** Small `λ` barely helps; there
is a stable band that preserves target performance while substantially
reducing drift; past it target performance drops sharply. So **start with a
high `λ` and decrease it until the target-task drop disappears** relative to
ES without AWD. `L2` is slightly more robust and degrades more gracefully when
set too high. `L1` below the critical magnitude *systematically improved*
target-task performance, which is worth a try and is one paper's observation.

## There is a reason to stop early, and it is a different curve

This practice says drift is not controlled by stopping early. That is not the
same as saying never stop early, and the record should not be read as
conflating the two.

[LIT-236](../literature.d/LIT-236.md) reports **rise-then-decay**: under fixed hyperparameters the
*target* reward improves, peaks, and then degrades — in GRPO as well as ES. Its
account is the same geometry from the other side. Stiff, curvature-active
directions relax fast and pay out early; the near-zero bulk relaxes slowly and
keeps accumulating variance. Once the stiff modes are exhausted the
accumulation dominates and performance falls. *Rushing downhill before the
valley floods.*

So there are two curves and two different answers:

| Curve | Shape | What to do |
|---|---|---|
| Prior-task accuracy | dips, then **recovers** ([LIT-238](../literature.d/LIT-238.md)) | do not stop early — you would stop at the dip |
| Target-task reward | rises, **peaks, decays** ([LIT-236](../literature.d/LIT-236.md)) | stop near the peak |

The practical rule that satisfies both: **stop on the target reward's own
peak, not on a prior-task decline.** Watch the curve you are optimizing.

<!-- inactive-ok-block: THEORY-007 — Proposed, filed in this same change
     and named as the account behind this section -->
[LIT-236](../literature.d/LIT-236.md) also confirms the population knob a third time and from a
third direction — larger `N` raises the terminal plateau and suppresses the
late decay — and proposes two interventions this practice does not yet carry
because nobody has run them end to end: **noise scheduling** (reduce `σ`,
temperature, or effective update noise over training) and **adaptive step
sizes** that shrink once curvature-active progress saturates. Both follow from
[THEORY-007](../theory.d/THEORY-007.md) and are, for now, derivations rather than results.

Its last suggestion is free and worth taking: treat non-monotonic training
reward as a **diagnostic**. Its presence says the curvature is heterogeneous
and the late regime is variance-dominated — which is exactly when this
practice applies.

## Conditions, and what is not established

**The remedy is one paper, from an interested lab.** [LIT-238](../literature.d/LIT-238.md) is
Cognizant AI Lab answering a criticism of [LIT-211](../literature.d/LIT-211.md)'s method, with Qiu on
both. The measurements are ones anyone could repeat and the paper reproduces
the negative result before qualifying it — but AWD has not been independently
tested, which is what the promotion condition asks for.

**Verifiable domains only.** Whether an anchor penalty preserves alignment and
safety properties rather than benchmark accuracy is untested, and the authors
flag it.

**Norm is not the thing to minimize.** Even with AWD or a large population, ES
update norms stay an order of magnitude above GRPO's while the prior-task
distributional shift becomes comparable. What matters is how much of the
displacement is unconstrained by the target task, not how far the weights
moved — so do not treat a small update norm as the goal or a large one as the
problem.

<!-- inactive-ok-block: SOTA-212 — Proposed, and named as the practice this
     failure mode cannot reach; that is what the citation is for -->
**It does not apply to [SOTA-212](SOTA-212.md).** That practice's whole form is a single
parallel round, so `T = 1` and there is no trajectory for a random walk to
accumulate along.

**The blessing side is unmeasured.** The same random walk that costs
prior-task accuracy may be what lets ES escape local optima a gradient method
stays in — [LIT-238](../literature.d/LIT-238.md) raises this and does not test it. Constraining
drift may cost something nobody has priced.

## Known implementations

- None released. AWD is implemented on top of [LIT-211](../literature.d/LIT-211.md)'s ES codebase, with
  the reference weights streamed from pinned RAM during the weight update.
