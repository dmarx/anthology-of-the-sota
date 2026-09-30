---
number: 432
status: Superseded
formerly:
- SOTA-tmp0s2gj
superseded_by: SOTA-428
status_note: >-
  A duplicate of SOTA-428, which was filed from LIT-714 hours earlier and is the
  same recommendation from the same paper. SOTA-428 is also the better document:
  it carries the architecture, learning-rate, guidance and metric dependences,
  where this one had only the first two. The `Active`/`unreplicated` pairing this
  note argued for is a judgement SOTA-428 declined, at `Proposed`, and that is the
  one that stands.
consensus: unreplicated
consensus_note: >-
  One group, one paper, one setting — ImageNet-512 diffusion with EDM2's own
  architecture — and the group is the EDM/StyleGAN line, so its own earlier work
  is not independent support. What makes the practice `Active` rather than
  `Proposed` despite that is that the claim is arithmetic, not an empirical
  regularity: the reconstruction is a least-squares fit between averaging
  profiles, its error is measured at `O(1/n⁴)` in snapshot count, and nothing in
  it is specific to diffusion. What is *not* replicated is the payoff — that
  sweeping the length post hoc materially changes which other hyperparameters
  matter. Nothing in the record's language-model averaging line replicates that;
  `SOTA-415`'s sources found the window stops mattering late in training, which is
  a different finding and in mild tension with the optimum drifting longer here.
  Per `DP-005`, the reference implementation shipping it is adoption, not
  evidence. Read as of 2026-09.
title: 'Maintain two power-function weight averages during training and snapshot them, so the averaging length is a post-hoc sweep instead of a guess you have to make before the run'
version: 1
tags:
- training-optimization
- generative-modeling
- model-stability
date: '2026-09-25'
source:
- LIT-720
introduced_by:
- LIT-720
implementations:
- 'EDM2'
summary: >-
  Karras et al. (2023), [LIT-720](../literature.d/LIT-720.md). Keep two power-function averages of the
  weights during training (`σ_rel` 0.05 and 0.10) and store both in each periodic
  snapshot; afterwards, reconstruct the average for any averaging length by a
  least-squares fit over the stored profiles, with error falling as `O(1/n⁴)` in
  the snapshot count. The averaging length stops being a pre-training commitment.
  Worth it because that commitment is expensive in a way that does not show up in
  its own column: with the length pinned at 13%, the learning-rate decay moves FID
  **by up to 72%** across `t_ref ∈ [30k, 160k]`; swept post hoc, the same bracket
  is **within 10% of the optimum**.
---

<!-- inactive-ok-file: SOTA-415, SOTA-408, SOTA-217, THEORY-111 — the neighbouring averaging practices, all Proposed, cited to be distinguished from this one rather than relied on; SOTA-415 is named for a justification this practice qualifies and SOTA-408 for a cost that does not transfer, so their not-being-in-force is beside the point. THEORY-111 is this practice's own account and Proposed for the reason stated there. -->

<!-- inactive-ok-file: SOTA-428, LIT-720 — this practice is Superseded, a same-day duplicate of SOTA-428, and cites it as its own replacement; LIT-720 is the duplicate note it was filed from, also retired. Nothing here is relied on. -->

# SOTA-432: Maintain two power-function weight averages during training and snapshot them, so the averaging length is a post-hoc sweep instead of a guess you have to make before the run

## Source

Karras, Aittala, Lehtinen, Hellsten, Aila and Laine (2023), [LIT-720](../literature.d/LIT-720.md) —
[ARXIV-2312.02696](https://arxiv.org/abs/2312.02696).

## What to do

**During training.** Maintain two running averages of the weights using a
power-function profile rather than an exponential one:

    θ̂_γ(t) = β_γ(t)·θ̂_γ(t−1) + (1 − β_γ(t))·θ(t),   β_γ(t) = (1 − 1/t)^(γ+1)

at `σ_rel = 0.05` and `σ_rel = 0.10` (`γ = 16.97` and `6.94`). Store **both**
vectors in every snapshot you were already writing. The paper snapshots every
~8M training images.

**After training.** For whatever averaging length you want, solve the
least-squares fit between the stored profiles and the target profile, and take
that linear combination of the stored vectors. Then sweep the length like any
other evaluation-time parameter.

**Two averages, not one, is the whole trick.** With two per snapshot,
reconstruction error falls as `O(1/n⁴)` in the snapshot count and a few dozen
snapshots is "virtually perfect". With one it still works, "albeit with much
lower accuracy" — which is what makes the retroactive case possible.

## Why the pre-training guess costs more than it looks

The averaging length has no obvious price: you pick a decay constant, the run
proceeds, and the number you report is whatever that choice produced. What the
paper measures is that freezing it **inflates the apparent sensitivity of other
hyperparameters**:

| learning-rate decay `t_ref` | EMA length fixed at 13% | EMA length swept post hoc |
| --- | --- | --- |
| `[30k, 160k]` | FID up to **72%** worse than optimum | all **within 10%** |

So a run that reports "the learning-rate decay matters a lot" may be reporting a
fact about the pair, not about the decay. [THEORY-111](../theory.d/THEORY-111.md) is that account, and
it is `Proposed` because this is one measurement.

Three further reasons the length cannot be set once and reused:

- it "differs considerably between the configurations" of the same model family;
- the optimum **narrows** as the architecture gets better, so a value tuned on an
  earlier config is both wrong and wrong by more;
- it "slowly shifts towards relatively longer EMA as the training progresses",
  which is striking because the definition is already relative to run length.

## Why a power function rather than an exponential

Two reasons, both stated: a long exponential average "puts non-negligible weight
on initial stages of training where network parameters are mostly random"; and
longer runs want longer averages, so the profile should stretch with training
time rather than needing to be re-tuned. The power profile gives the
initialization weight exactly zero and is scale-independent. Report the length as
`σ_rel` — the peak's width as a fraction of training time — not as `γ`.

## Conditions and what it does not cover

**Measured in one setting.** ImageNet-512, EDM2's architecture, FID. The
reconstruction arithmetic is setting-independent; the claim that it changes which
*other* knobs matter is not.

**Storage, not compute.** The cost is two parameter vectors per snapshot instead
of one, and no extra training steps. This is what distinguishes it from [SOTA-408](SOTA-408.md),
whose ImageNet result buys +0.8 top-1 with **ten further epochs** of averaging —
a real compute charge that this approach does not incur, because the averages are
accumulated inside the run that was happening anyway. The two are not
alternatives measured against each other; they are different cost structures for
related ends, and nobody has compared them.

**It does not tell you which length to pick.** It makes the sweep possible, and
the sweep needs an evaluation metric — with FID that reopens everything
[SOTA-307](SOTA-307.md), [SOTA-383](SOTA-383.md) and [SOTA-425](SOTA-425.md) say about reading FID differences, and a sweep
over averaging lengths scored on a noisy metric is a selection problem, not a
measurement. Expect to need the error bar.

**Per-tensor lengths are open.** Sweeping one tensor's length against the global
optimum improved Config B's FID from 7.24 to ~6.5 — 10% — with the gain coming
from a *very short* length in one case and a *very long* one in another, which
the authors read as "any global choice is an uneasy compromise". They did not
pursue it. Worth noting that in their final configuration the effect vanished, so
this may be a diagnostic for an unfinished architecture rather than a knob to
turn.

## Related

- [SOTA-415](SOTA-415.md) — uniform-average recent checkpoints to estimate an annealed score.
  It recommends uniform averaging partly because "it has no hyperparameter";
  this practice is the argument that the hyperparameter is worth having.
- [SOTA-408](SOTA-408.md) — average the tail under a cyclical or high constant learning rate.
  Same family, different cost structure, and its extra-epochs objection does not
  apply here.
- [SOTA-409](SOTA-409.md) — average across a hyperparameter sweep rather than along one
  trajectory. Orthogonal: that averages *models*, this averages *time*.
- [SOTA-217](SOTA-217.md) — align permutations before averaging separately trained networks.
  Not needed here: every snapshot comes from one trajectory.

**Worth naming: this would be the only `Active` practice in that list.** The other
five averaging practices are all `Proposed`, one of them ([SOTA-408](SOTA-408.md)) with
`converged` consensus. The asymmetry is deliberate and narrow — what is `Active`
here is that you *can* reconstruct any averaging length from two stored averages,
which is arithmetic with a measured error rate, not that post-hoc sweeping is
known to be the right thing to do everywhere. A reader who takes the status as a
ranking against its neighbours has read it wrong.
