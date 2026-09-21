---
number: 215
status: Read
formerly:
- NOTE-tmpzsxfv
paper: LIT-465
title: 'Auxiliary Task Demands'
version: 1
date: '2026-09-21'
summary: >-
  Four capacities, each measured two ways; the higher-demand way scores lower
  and the gap shrinks with model size and training time. Reading it: the
  interaction is what matters, because it means cross-scale comparisons under
  a demanding evaluation overstate the difference between models.
---

# NOTE-215: Auxiliary Task Demands

## Contribution

Developmental psychology has a century of practice in distinguishing "the
child lacks the capacity" from "the task defeated the child", and a name for
the second: task demands. This imports the concept into language-model
evaluation and, more usefully, measures it. What is true afterwards is that
the demand gap is a quantity with a known sign, a known shape against scale,
and a statistical test behind it — not an anecdote about prompt sensitivity.

## Key insight

A score is never a measurement of a capacity. It is a measurement of the
capacity *through* a design, and the design has its own cost. That cost is
not a constant to be subtracted: it falls on weaker models harder. So the
standard move — compare a small and a large model on one evaluation and
attribute the difference to capability — double-counts, because part of the
gap is the smaller model paying more for the same test.

## Assumptions

- **Both methods target the same construct.** Forced choice and free
  production are taken to measure the same analogical reasoning; direct
  probability readout and metalinguistic prompting the same word prediction.
  This is argued rather than proved, and it is the assumption everything
  rests on.
- **Parameter count and training steps operationalize "capability."** Both
  are proxies and the paper says so.
- **Base models, no fine-tuning**, and open-weight only, because token-level
  logits are needed — so no closed API models appear.
- **Contamination is tolerated on purpose.** LAMBADA and BLiMP predate the
  models' cutoffs. The argument is that the object of study is the
  *difference* between two methods, and contamination has no reason to favour
  one. Reasonable, and not free: a contaminated item could be easier to
  retrieve than to judge metalinguistically.

## Key results

- **Production vs forced choice** (analogical and reflective reasoning) — the
  low-demand method scores higher, and the log-odds gap narrows as parameters
  increase, in every family except Pythia, where it is flat.
- **Metalinguistic judgement vs direct probability** (word prediction,
  grammaticality) — same direction, same narrowing. Flat for Pythia and OLMo
  on grammaticality, where neither is appreciably above chance under the
  metalinguistic method, so the effect may sit outside the size range tested.
- **The interaction is significant in three of four domains** — analogical
  reasoning, grammaticality judgement and word prediction, by mixed-effects
  models in `lme4` with model family as a grouping factor. **Not** in
  reflective reasoning, and the paper says why: larger models prefer the
  intuitive answer there, so raw performance does not rise with size to begin
  with.
- **The same pattern over training time** — OLMo 7B at 10 checkpoints. The
  low-demand method reveals the ability earlier; direct word-prediction log
  probabilities plateau quickly while metalinguistic ones keep climbing.
  Significant interaction with training steps in both domains tested.
- **Scope** — 13 models across five families (deduplicated Pythia, OLMo,
  Gemma, Llama-2, Mistral), 1B to 70B.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Higher-demand evaluation methods yield lower performance than lower-demand ones for the same capacity | strong | four domains, 13 models, consistent direction |
| C2 | The demand gap shrinks as models get larger | strong | significant size × method interaction in three of four domains, across five families |
| C3 | The demand gap shrinks with training time within one model | moderate | one model, 10 checkpoints, two domains, both significant |
| C4 | Model performance should not be read as a direct indication of capability | strong | follows from C1 and C2 |
| C5 | Some reported capability differences between small and large models are demand effects | moderate | implied by C2 and not quantified — the paper does not say what share |

## Concepts

- **Task demands** — auxiliary challenges of an evaluation that are unrelated
  to the capacity being measured.
- **Demand gap** — low-demand score minus high-demand score, in log odds or
  log probability.
- **Metalinguistic prompting** — asking the model, in words, for a judgement
  it could instead be read off from its probabilities.

## Connections

Builds on a line showing performance gaps between higher- and lower-demand
evaluations in linguistic domains, and on developmental psychology's use of
task demands. It is the systematic counterpart to the reasoning-model dispute
in [LIT-466](../literature.d/LIT-466.md) and [LIT-463](../literature.d/LIT-463.md), neither of which cites it
and both of which are arguing about one instance of what this measures across
four.

## Bearing on the record

- **It is the primary source for [SOTA-278](../practices.d/SOTA-278.md)**, and the reason that
  practice can be `Active` rather than `Proposed`: the caution rests on a
  measured, tested interaction across five model families, not on one
  contested dispute.
- **It is the mirror of [SOTA-200](../practices.d/SOTA-200.md).** That practice says a capability
  appearing with scale may be a metric artefact. This says a limit appearing
  at small scale may be a demand artefact. Same instrument problem, opposite
  sign, independent literatures — and the record now holds both ends.
- **It bears on [SOTA-196](../practices.d/SOTA-196.md)** and anything else comparing models across
  scale on a single evaluation, because C2 means such comparisons are
  inflated by an amount nobody has measured.
- **It produces [THEORY-039](../theory.d/THEORY-039.md)**, the account.

## Limitations

- **Base models only, open weights only, 1B–70B.** Nothing here covers
  instruction-tuned or frontier models, where the demand of following a
  prompt is exactly what tuning targets — so the gap could be much smaller,
  and the paper cannot say.
- **The construct-equivalence assumption** is the whole edifice and is
  argued, not established.
- **Pythia is flat**, and OLMo is flat in one domain. Reported plainly; it
  means the effect is not universal within the range tested.
- **No effect in reflective reasoning**, where the scale relationship is
  confounded by larger models preferring intuitive answers.
- **No quantity attached to C5.** The paper does not say what share of any
  reported scale effect is demand.

## Open questions

- Does the gap persist after instruction tuning, which is aimed precisely at
  task-demand competence?
- Is there a low-demand readout for the capacities people actually deploy
  for? Probability readouts work for word prediction; there is no obvious
  equivalent for multi-step planning, which is where the loudest capability
  disputes are.
- Why is Pythia flat?
