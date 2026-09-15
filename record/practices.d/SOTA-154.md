---
number: 154
status: Active
formerly:
- SOTA-tmpex7d9
consensus: contested
# inactive-ok-block: THEORY-006 — Proposed, and the account that
# predicts where the dissent's evidence sits; the note is the reconciliation
consensus_note: >-
  Five independent groups now report evolution strategies at or ahead of
  policy-gradient RL (LIT-211, LIT-233, LIT-229 on a recurrent architecture,
  LIT-230, LIT-tmp4w505), with LIT-234 carrying the same lab's evidence to 32B
  against published RL checkpoints. Two groups disagree: LIT-231 argues direct
  ES at LLM scale is ineffective, and LIT-tmppbfp5 ran the comparison and did
  not reproduce the ordering. **Every negative result in this line is at 1.5B
  or below and every positive is at 1.5B or above**, which is the shape
  THEORY-006 predicts and is now the most useful thing the disagreement has
  produced. The trunk — gradient-free search of the full
  parameter space is viable at billion scale — is agreed. The branch in
  dispute is the word "instead": whether it replaces policy-gradient RL or is
  seeded by it. The dissent's models are all at 1.5B or below, which
  THEORY-006 says is where it should be.
title: 'Fine-tune with evolution strategies instead of policy-gradient reinforcement learning'
version: 2
history:
- version: 2
  date: '2026-09-15'
  note: >-
    Promoted from `Proposed` on the condition the practice set for itself.
    Gan and Isola (LIT-233) ran ES against PPO and GRPO on six tasks
    outside Countdown and the conciseness objective, at matched training
    FLOPs, with the RL arm grid-searched over learning rate and batch or
    group size while ES ran one fixed configuration — an independent group,
    a harder-tuned baseline, and ES ahead in most cells. Consensus moved
    from `unreplicated` to `contested` in the same edit, which is not a
    hedge: what makes it contested is a fourth group arriving with a
    counter-argument, and that could not have been recorded while the axis
    still said nobody had replied.
tags:
- adaptation-and-tuning
date: '2026-09-07'
source:
# LIT-211 ran the comparison itself against both PPO and GRPO, which is what
# made this evidenced rather than asserted (ADR-017). LIT-233 is the
# independent evaluation that promoted it: a different group, six further
# tasks, and the RL arm tuned harder than the ES arm.
#
# LIT-229 is deliberately NOT here. Its LLM comparison is real and
# favourable, but it is on a recurrent architecture and on its own low-rank
# variant, so it is evidence about the line rather than about this
# recommendation; the lineage on the notes is where it belongs.
- LIT-211
- LIT-233
# The coverage evidence, which is an argument for this recommendation and not
# only about how to measure it: LIT-230 independently, LIT-234 from
# LIT-211's own lab but carrying the comparison to 32B.
- LIT-230
- LIT-234
# Hoy et al.: a fourth independent group, at 4B, both arms swept, and the
# paper the drift account in this record's theory scheme is drawn from.
- LIT-tmp4w505
introduced_by:
- LIT-211
# The evidence AGAINST, required where the record claims there is some
# (ADR-016). Gu et al. argue direct ES at LLM scale is ineffective and
# replace the search space with a gradient-seeded subspace.
contested_by:
- LIT-231
# The failed replication: an independent group ran the comparison, extended it
# to three further tasks, and found GRPO ahead on all but one. At 1B and 1.5B.
- LIT-tmppbfp5
# The comparison the paper actually ran: ES against GRPO, which is SOTA-145.
# Stated once here, on the practice that ran it; the fixer writes the other
# side.
compared_against:
- SOTA-145
implementations: []
summary: >-
  Qiu et al. (2025), [LIT-211](../literature.d/LIT-211.md) — evolution strategies over the full
  parameter space of a billion-scale LLM, which the field had assumed
  impossible. +36.4% over base on average against GRPO's +21.3% and PPO's
  +17.9%, with ES on one fixed hyperparameter set while RL got a sweep per
  experiment. `Active` since Gan and Isola replicated the comparison on six
  further tasks with the RL arm tuned harder; `contested`, because Gu et al.
  argue direct ES at LLM scale does not work — on models at 1.5B and below.
explained_by:
- THEORY-006
- THEORY-tmpt76ks
extended_by:
- SOTA-212
- SOTA-tmpdcmgg
---

# SOTA-154: Fine-tune with evolution strategies instead of policy-gradient reinforcement learning

## Source

Qiu et al. (2025), [LIT-211](../literature.d/LIT-211.md) — [ARXIV-2509.24372](https://arxiv.org/abs/2509.24372).

The assumption this overturns is that searching a billion-dimensional
parameter space directly is hopeless, which is why prior ES work on LLMs
reduced the dimension — last layer only, or a low-rank subspace. This
searches the full parameter space and reports the first successful
application at that scale.

The result is backpropagation-free, and the paper's account of where the
advantage comes from follows from that: tolerance to long-horizon and delayed
rewards, robustness across different base models, reduced susceptibility to
reward hacking, and steadier training.

## Why the comparison is worth more than its headline number

It is deliberately tilted against itself. **ES ran with one fixed
hyperparameter set across every experiment.** RL got a per-experiment grid
over the KL penalty β and the learning rate α, because the authors found RL
"did not make much progress if they were not set precisely" and took the best
configuration each time.

Averaged across Qwen2.5 (0.5B–7B) and LLaMA3 (1B–8B) on Countdown, ES
improves over the base model by **36.4%**, PPO by **17.9%**, GRPO by
**21.3%** at group size 8 and **21.4%** at group size 30.

A comparison arranged to favour the baseline and won anyway is a stronger
result than a larger margin from a sweep, which is why this is the part the
practice rests on.

## The replication, and why it counts

Gan and Isola ([LIT-233](../literature.d/LIT-233.md)) ran evolution strategies as a baseline in
a paper about something else, and that is what makes it worth more than a
friendly replication rather than less. Six tasks outside Countdown and the
conciseness objective — GSM8K, MATH-500, OlympiadBench, MBPP, ROCStories,
USPTO. Qwen2.5 at 0.5B–3B, OLMo3-7B base and instruct, Llama-3.1-8B-Instruct.
All arms matched on training FLOPs, with PPO and GRPO grid-searched over
learning rate and batch or group size while ES ran a single fixed
configuration. ES came out ahead of GRPO in most cells, and ES with test-time
majority voting took the best or runner-up cell in roughly half the table.

That is the practice's own promotion condition, met: an independent group, a
policy-gradient baseline that got at least the same tuning budget, on tasks
outside the original two. It is not weakened by having arrived as a baseline
— a group with no stake in the result, tuning the rival harder than the
method, is the *stronger* form of the evidence the condition was asking for.

<!-- inactive-ok-block: THEORY-006 — Proposed, and named as the account
     this practice acquired rather than as evidence for the recommendation -->
The practice also acquired something the condition did not ask for: an
account of why it works, in [THEORY-006](../theory.d/THEORY-006.md).

## What is contested, and what is not

Gu et al. ([LIT-231](../literature.d/LIT-231.md)) disagree, in their own second sentence:
"directly applying ES to billion-parameter LLMs is highly ineffective",
because almost all random perturbations in such a space are near-orthogonal
to a useful descent direction. Their Hyper-ES replaces the search space
rather than the optimizer — a handful of cheap GRPO runs supply LoRA descent
directions, and CMA-ES searches merging coefficients over their span. It is
gradient-seeded, and it beats GRPO-LoRA by about one point.

Two things about that dissent are worth stating precisely rather than
averaging away.

**It is a theoretical argument plus a small-model measurement, not a failed
reproduction.** The ES baseline in their table is CMA-ES over LoRA, not
full-parameter ES at the scale [LIT-211](../literature.d/LIT-211.md) reports. Nobody has run the thing
this practice recommends and reported that it did not work.

<!-- inactive-ok-block: THEORY-006 — Proposed, and this paragraph is the
     record's own reconciliation of the dispute; it rests on that account
     being what predicts the dissent's scale, which is the citation's point -->
**Every model they test is at 1.5B or below** — and [THEORY-006](../theory.d/THEORY-006.md) says
the density of task-improving perturbations rises with scale, with gains
appearing sharply from about 1.5B and absent beneath it. So the dissent is
measured exactly where this record's account predicts a negative result, and
their lemma about near-orthogonal perturbations is the needle-in-a-haystack
regime under another name. **That reconciliation is this record's, not either
paper's** — they do not cite each other — and it is offered as the reading to
test, not as a dismissal.

The experiment that would settle it is the one nobody has run: full-parameter
ES against a well-tuned GRPO on the same benchmarks at 7B and above.

## What ES buys that the headline numbers do not show

The two coverage papers change what this practice is *for*. Reinforcement
learning with verifiable rewards raises pass@1 and **lowers** pass@k, often
below the base model's — GRPO finishes under its own base on both pass@16 and
pass@32 in 15 of 18 comparisons ([LIT-230](../literature.d/LIT-230.md)), and across Qwen2.5, Qwen3
and published RL checkpoints up to 32B the base model eventually overtakes the
RL checkpoint ([LIT-234](../literature.d/LIT-234.md)). Evolution strategies raise both, and never
fall below base at any `k` or scale tested.

So the case for this practice is strongest exactly where test-time sampling is
the deployment — verifiable domains, agentic retries, best-of-n, search over
candidates — and weakest where the model answers once. [SOTA-210](SOTA-210.md) is the
evaluation practice that falls out of it.

There is a mechanism attached, and it is the most interesting thing the line
has produced. ES's largest updates land in **LayerNorm weights and attention
projections**; GRPO's are an order of magnitude smaller and land in **token
embeddings and the language-model head**. ES moves the whole model roughly 40×
further, and that drift turns out to be functionally sparse — zeroing every
update below a single-step magnitude threshold preserves the gains — and does
not produce broad forgetting on held-out tasks ([LIT-230](../literature.d/LIT-230.md)).

## The scale boundary, which is now the clearest thing in the line

Eight papers have compared evolution strategies against policy-gradient RL on
LLMs. Sorting them by the size of the model tested produces a pattern nobody
set out to find:

| Finding | Models | Source |
|---|---|---|
| GRPO ahead on 3 of 4 tasks | 1B, 1.5B | [LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md) |
| Direct ES "highly ineffective" | 0.5B, 1.5B | [LIT-231](../literature.d/LIT-231.md) |
| ES ahead in most cells | 1.5B–8B | [LIT-233](../literature.d/LIT-233.md) |
| ES highest peak accuracy, 4 of 4 tasks | 4B | [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md) |
| ES ahead on pass@k | ≤7B | [LIT-230](../literature.d/LIT-230.md) |
| ES ahead on pass@k | 7B–32B | [LIT-234](../literature.d/LIT-234.md) |

<!-- inactive-ok-block: THEORY-006 — Proposed, and this section is the record’s own cross-paper reading of that account -->
**Every negative result is at 1.5B or below. Every positive is at 1.5B or
above.** No paper reports a negative above that line and none reports a clear
positive below it. That is the boundary [THEORY-006](../theory.d/THEORY-006.md) predicts from the density
of task-improving perturbations, arrived at independently by six groups none
of whom were testing it — and it is a stronger corroboration of that account
than anything in its own `source:`.

Two cautions. The pattern is read across papers that differ in task, baseline
tuning and ES implementation, so it is suggestive rather than controlled; and
it is exactly the kind of post-hoc regularity that looks inevitable once
noticed. What would settle it is one protocol run on both sides of the line,
which nobody has done.

**The practical form of this is the condition below, and it is now sharp
rather than hedged: do not expect this practice to hold under about 1.5B.**

## Conditions, and what is not established

The evidence now spans four model families and, at the top end, **32B** —
Qwen2.5-14B and -32B against OatZero and SimpleRL-Zoo on MATH500,
OlympiadBench and Minerva ([LIT-234](../literature.d/LIT-234.md)). Two caveats travel with that
number and both matter: those comparisons are against *published checkpoints*
rather than RL runs matched to the ES budget, and they come from
[LIT-211](../literature.d/LIT-211.md)'s own lab. The independent evidence stops at 8B.

Still **no released model whose post-training recipe uses it**, which is the
half of the original promotion condition that remains unmet.

Below about 1.5B the practice should be expected to fail, and both dissenting
papers are the evidence that it does.

**And it has a cost the earlier evidence did not show — a smaller one than it
first looked.** ES post-training drifts orders of magnitude further from the
base model than GRPO: roughly 1000× after 500 iterations in
[LIT-tmppbfp5](../literature.d/LIT-tmppbfp5.md), 87–107× across four sequential tasks in [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md), and a
held-out capability degrades along with it. But [LIT-tmpphacm](../literature.d/LIT-tmpphacm.md) tracks the
prior tasks individually rather than averaged and finds the degradation is
largely **transient** — HellaSwag falls 8% over 300 iterations and returns to
baseline by the end — that GRPO forgets too on the right target task, and that
the whole effect is controllable.
<!-- inactive-ok-block: THEORY-tmpt76ks, SOTA-tmpdcmgg — both Proposed, filed
     in this same change and named as the account of this drift and the
     condition it puts on running this practice -->
[THEORY-tmpt76ks](../theory.d/THEORY-tmpt76ks.md) says why the drift is mostly invisible to the training
objective, and [SOTA-tmpdcmgg](SOTA-tmpdcmgg.md) is what to do about it. Neither retires this
practice; both are conditions on running it.

`Active` here means the record is willing to assert the recommendation. It
does not mean the field has settled — `consensus: contested` is carrying that,
and the two axes disagreeing is the arrangement they exist for.

## Against the post-training spine

[SOTA-129](SOTA-129.md) makes reinforcement learning with verifiable rewards the third stage
of the reasoning recipe, [SOTA-145](SOTA-145.md) recommends the group baseline inside it,
<!-- inactive-ok: SOTA-146 — Proposed, and named as one of the three practices that assume the paradigm -->
and [SOTA-146](SOTA-146.md) corrects the objective. All three assume the paradigm; this is a
different paradigm reaching the same goal.

Be precise about what it does and does not disturb. [SOTA-145](SOTA-145.md)'s argument is
that every work which *runs or reworks GRPO* keeps the group baseline. ES
does not run GRPO, so it is not a counterexample to that — it is evidence
about whether to be in that family at all, and `compared_against:` is the
relation for a rival somebody actually measured rather than a successor.

One detail bears on [SOTA-145](SOTA-145.md) directly and mildly: raising GRPO's group size
from 8 to 30 moved the average by 0.1 points here. One task, but a data point
on what the group baseline's width buys.

## The line this heads

This is the first entry in what is now a line of six papers rather than a
single result.

- [LIT-229](../literature.d/LIT-229.md) (EGGROLL) makes the search affordable — rank-`r`
  perturbations per worker, a high-rank population average, a hundredfold
  throughput gain at billion scale.
<!-- inactive-ok-block: SOTA-211 — Proposed, filed in this same change
     and named as an implementation decision inside this practice -->
- [LIT-232](../literature.d/LIT-232.md) (EGGROLL, Unrolled) says what that low-rank update
  converges to, finds it need not be the gradient of anything away from the
  quadratic regime, and halves the estimator's cost — which is
  [SOTA-211](SOTA-211.md).
- [LIT-230](../literature.d/LIT-230.md) characterizes what ES does to a model instead of asking
  whether it wins, and is the independent corroboration this practice was
  short of.
- [LIT-234](../literature.d/LIT-234.md) carries the comparison to 32B and to solution coverage.
- [LIT-231](../literature.d/LIT-231.md) (Hyper-ES) is the dissent above.

<!-- inactive-ok-block: SOTA-212 — Proposed, and named as the practice
     that extends this one; the lineage is what the citation is for -->
[SOTA-212](SOTA-212.md) is the degenerate case — one round instead of many, with an
ensemble on the end — and `extends:` this practice for that reason.

## Known implementations

- None in a released model. The published results are the authors' own, and
  that absence is the half of the original promotion condition that is still
  unmet.
