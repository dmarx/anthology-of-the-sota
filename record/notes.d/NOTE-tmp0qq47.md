---
status: Read
paper: LIT-tmpphacm
title: 'Overcoming Forgetting in LLM Fine-Tuning with Evolution Strategies'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
summary: >-
  Prior-task degradation under ES is transient drift rather than irreversible
  forgetting, is not specific to ES, and is driven by the random walk Hoy et
  al. predicted — whose size falls with population exactly as their equation
  says. Anchored Weight Decay buys a population-128 reduction at population 30
  for 1-2% runtime.
---

# NOTE-tmp0qq47: Overcoming Forgetting in LLM Fine-Tuning with Evolution Strategies

## Contribution

Turns a reported failure mode into a controlled parameter, in three steps that
are worth keeping separate because they have different strengths. It shows the
reported degradation is largely transient and not ES-specific; it confirms an
existing theory's scaling by varying the term that theory says is the handle;
and it introduces a regularizer that gets the same effect for a fraction of
the cost. The first is a reinterpretation, the second is a replication, the
third is a method.

## Key insight

**Averaging the prior tasks hid a recovery.** Mean prior-task accuracy falling
monotonically through training looks like irreversible damage. Per task, the
curves are U-shaped: HellaSwag loses about 8% over 300 iterations and comes
back to baseline by the end, MMLU-Pro and ARC-Challenge do likewise, and
ProofWriter runs the trajectory upside down — improving, then settling back.

That is what a random walk through directions the target task does not
constrain should look like from outside: excursions in both directions, on
tasks unrelated to the one being optimized, with no reason for the sign to
persist. The degradation is real while it lasts; it is not the accumulation
of damage the word "forgetting" implies.

## Assumptions

- **Verifiable, accuracy-scored tasks** throughout; targets are Countdown,
  GSM8K and ProofWriter, priors are HellaSwag, PIQA, ARC-Challenge and
  MMLU-Pro, plus whichever target tasks are not being trained on.
- **200 training examples** per target task; evaluation on 500–2,000 examples
  per task with greedy decoding.
- **Qwen2.5-3B-Instruct as the standard model**, chosen to line up with the
  paper being answered, with Llama-3.2 and other Qwen sizes used for the
  family and scale sweeps.
- **The `α²Td/N` scaling is taken from [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md)**, not re-derived. This
  paper tests it.
- **The penalty weights all parameters equally**, unlike Elastic Weight
  Consolidation's Fisher weighting — a deliberate choice, justified by there
  being no task-importance information when the prior tasks are everything the
  model could previously do.

## Key results

- **Transient drift.** HellaSwag −8% over the first 300 iterations, back to
  its original level by the final iteration; same shape on MMLU-Pro and
  ARC-Challenge; inverse on ProofWriter.
- **Not ES-specific.** With ProofWriter as the target task, **GRPO** shows
  considerable forgetting — chiefly a large GSM8K drop, with MMLU-Pro and
  Countdown also degrading — while ES shows little on average.
- **No dependence on target task, model family or model size** across the
  swept conditions.
- **Population size reduces drift.** 30 → 128 halves the update norm; 256
  remains more than an order of magnitude above GRPO. Prior-task degradation
  falls monotonically with population (Table 1). The paper's statement: "the
  update norm is indeed inversely proportional to the population size."
- **AWD.** At population 30, brings the update norm to roughly population-128
  levels; closes the prior-task KL gap to GRPO; **1–2% runtime** overhead with
  reference weights streamed layer-wise from pinned RAM.
- **KL divergence.** Larger populations or AWD bring prior-task KL down to
  GRPO's level. On the *target* task the ordering reverses: GRPO's divergence
  is much higher than any ES variant's at the same accuracy.
- **The mechanistic conclusion.** Since norms stay an order of magnitude apart
  while prior-task KL converges, "it is the randomness of the drift
  unconstrained by the target task that leads to prior task forgetting for ES,
  rather than the magnitude of updates alone."
- **Penalty tuning.** A stable band of `λ` preserves target performance while
  cutting drift; past it target performance drops sharply. Recommended
  procedure: start high, decrease until the target-task drop vanishes. `L2` is
  more robust and degrades more smoothly; `L1` below the critical magnitude
  *systematically improved* target-task performance.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Prior-task degradation under ES is largely transient | strong | per-task trajectories across three target tasks; the recovery is the measurement |
| C2 | Forgetting is not specific to ES | strong | GRPO forgets on ProofWriter; the symmetry is the point |
| C3 | Forgetting does not depend on target task, model family or size | moderate | a sweep with no significant dependence; a null result over a modest grid |
| C4 | Larger populations reduce drift, as `α²Td/N` predicts | strong | three population sizes, norm and degradation both moving the predicted way |
| C5 | AWD achieves large-population benefits at small-population cost | moderate | one paper, one lab, Countdown as target |
| C6 | It is the randomness rather than the magnitude of drift that harms | moderate | inferred from norms staying apart while prior-task KL converges — a good argument, not an intervention |
| C7 | ES changes the output distribution less than GRPO on the target task | strong | KL measured at matched accuracy, and a genuine surprise |
| C8 | AWD preserves alignment and safety properties | not claimed | named as future work |

## Method

For each configuration, fine-tune on a target task and evaluate all prior
tasks at intervals through training, plotting target against prior accuracy
with iteration as the colour axis. For the mechanism, measure the Euclidean
norm of `w_t − w₀` per iteration across population sizes, and the
KL-divergence between base and final model per task. AWD: after the standard
reward-weighted ES update, apply an elementwise decay of `w` toward `w₀`
scaled by `λ`, with `L1` or `L2` geometry; reference weights held in pinned
RAM and streamed layer-wise during the update.

## Concepts

- **Performance drift** — the paper's replacement for "forgetting": a
  transient excursion in prior-task accuracy that has no reason to persist.
- **Anchored Weight Decay** — weight decay toward `w₀` rather than toward
  zero, applied in the update rule because ES has no loss to regularize.
- **The blessing and curse of random walks** — the paper's own framing: the
  drift that costs prior-task accuracy is also what lets ES keep exploring
  when the reward signal flattens, where a gradient method stops.

## Connections

It answers the forgetting paper directly and adopts Hoy et al.'s decomposition
as its explanation, citing both. It positions AWD against Elastic Weight
Consolidation and related regularization approaches, differing in weighting
all parameters equally. It cites Liang et al. (2026) for low-dimensional
curvature of fine-tuning landscapes as the explanation for why very small
populations suffice at billion scale — a paper this record does not hold.
Lineage is on the LIT.

## Recommendations

<!-- inactive-ok-block: SOTA-tmpdcmgg — Proposed, filed from this reading in
     this same change; naming it is the point -->
- **R1** — Control ES drift with population size or an anchor penalty; do not
  stop training early. *Topic:* post-training. *Status:* experimental.
  *Strength:* strong for the mechanism, moderate for AWD. Filed as
  [SOTA-tmpdcmgg](../practices.d/SOTA-tmpdcmgg.md).
- **R2** — Report prior-task curves per task, not averaged. The average is
  what made a recovery look like permanent damage. *Topic:* evaluation.
  *Strength:* strong, and the cheapest thing in the paper.
- **R3** — Tune the penalty from above: start high, decrease until the
  target-task drop vanishes. *Strength:* moderate.
- **R4** — Do not use update norm as the safety metric. Norms stay an order of
  magnitude apart while the distributional shift converges. *Strength:*
  moderate.

## Bearing on the record

<!-- inactive-ok-block: SOTA-tmpdcmgg — Proposed, filed in this same change
     and rewritten because of this reading; naming it is the point -->
**It rewrote [SOTA-tmpdcmgg](../practices.d/SOTA-tmpdcmgg.md) before that practice was merged.** The practice was
drafted from [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) as a stopping rule — stop when the target task
converges, because drift keeps accumulating. If the prior-task dip recovers,
that rule stops at the worst point on the curve. The durable half of the
original claim, that drift is bought down with population rather than spent on
steps, is what this paper confirms; AWD is the cheaper form of it.

**And it promoted [THEORY-tmpt76ks](../theory.d/THEORY-tmpt76ks.md) to `Active`.** That account's condition
asked for the scaling measured by an independent group, on a transformer at a
different scale, with the population dependence tested directly rather than
inferred. Table 1 and Figure 6 are that, on Qwen2.5-3B rather than Qwen3-4B,
by a group sharing no authors with [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md).

**On [SOTA-154](../practices.d/SOTA-154.md)** it weakens one of the two objections behind that practice's
`contested` reading — but only one. [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md)'s failed replication on
*accuracy* stands untouched; what is qualified is its forgetting claim.

## Limitations

Stated: AWD's small compute cost and its need for the reference weights;
verifiable domains only, with alignment and safety untested. From this
reading: it is the same lab as [LIT-211](../literature.d/LIT-211.md) answering a criticism of that
paper's method, which does not make the measurements wrong and does mean
nobody independent has checked AWD; the no-dependence result in §4.2 is a null
over a modest grid; and C6, the paper's sharpest mechanistic claim, is an
inference from two measurements moving differently rather than an experiment
that separates randomness from magnitude.

## Open questions

- **Does AWD cost the escape-from-local-optima benefit?** The paper raises
  this as "the blessing and curse of random walks" and does not test it. It is
  the most interesting open question in the line.
- **Does anyone outside this lab reproduce AWD?** The promotion condition on
  the practice asks exactly this.
- **What does a Huber penalty do?** The paper suggests combining `L1`'s
  target-task benefit with `L2`'s robustness and leaves it.
- **Does the transience survive longer horizons and task sequences?** Recovery
  within one target task is not recovery across four.
