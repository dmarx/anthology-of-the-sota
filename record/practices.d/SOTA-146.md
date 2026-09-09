---
number: 146
status: Proposed
formerly:
- SOTA-tmpauaby
promote_when: >-
  A head-to-head of the published corrections — Dr. GRPO's unbiased length
  term, DAPO's decoupled clip and dynamic sampling, GSPO's sequence-level
  ratio — on one base and one dataset, reporting what each defect actually
  cost. A frontier recipe naming which correction it runs, and why, would also
  settle it. A fourth paper naming a fourth defect is not the missing
  evidence: three already exist and that is the problem.
consensus: emerging
consensus_note: >-
  Three independent groups published a correction within seventeen months
  (LIT-167, LIT-168, LIT-180), each locating the defect somewhere else and
  each keeping the group baseline. That the published objective needs
  correcting is agreed; which correction is not, and no recipe in this record
  names the one it runs.
title: 'Correct the GRPO objective before running it — the published form has three independently identified defects'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-07'
published: '2025-03-01'
source:
- LIT-167
- LIT-168
- LIT-180
# Corrective succession (ADR-017): the published GRPO objective has three independently identified defects.
corrects:
- SOTA-145
implementations: []
summary: >-
  Liu et al. (2025), [LIT-167](../literature.d/LIT-167.md); Yu et al. (2025), [LIT-168](../literature.d/LIT-168.md); Zheng et al. (2025),
  [LIT-180](../literature.d/LIT-180.md) — three groups, three defects in GRPO's objective, three published
  fixes, none of them the same fix. "We ran GRPO" does not say which of these
  you ran.
---

# SOTA-146: Correct the GRPO objective before running it — the published form has three independently identified defects

[SOTA-145](SOTA-145.md) is what everyone kept. This is what
everyone changed, and they did not change the same thing.

| paper | the defect | the fix |
|---|---|---|
| [LIT-167](../literature.d/LIT-167.md) | an optimization bias that inflates response length, **especially on incorrect outputs** | Dr. GRPO removes the bias; token efficiency improves at held accuracy |
| [LIT-168](../literature.d/LIT-168.md) | clipping range and sampling behaviour at scale | decoupled clip and dynamic sampling; 50 points on AIME 2024 from a Qwen2.5-32B base |
| [LIT-180](../literature.d/LIT-180.md) | the importance ratio defined per token | define it on sequence likelihood; clip, reward and optimise at sequence level |

## Why this is `Proposed` and not `Active`

Because the record cannot tell you which correction to run, and a practice
that says "correct it somehow" is not yet advice.

Each of the three is well-evidenced on its own terms and none of them is
tested against the others. They are not even obviously alternatives:
[LIT-167](../literature.d/LIT-167.md)'s length bias and [LIT-180](../literature.d/LIT-180.md)'s
token-level ratio are different parts of the objective, and a recipe could
plausibly want both. Nobody has published that recipe.

The [LIT-167](../literature.d/LIT-167.md) finding is the one worth reading twice. "The model
learned to think longer" is the usual reading of a length increase under RL;
part of that increase is the objective rewarding verbosity on answers that
were wrong.

## Why `emerging` rather than `contested`

The three groups are not arguing with each other. Each found a real defect,
published a real fix, and left the others alone — which is a field converging
on *"this objective needs work"* while nothing yet converges on which work.

`contested` would be the wrong word and the record now enforces the
<!-- inactive-ok: ADR-016 — Proposed, cited for the rule it introduced -->
difference: [ADR-016](../decisions.d/ADR-016.md) requires a `contested` practice to name what
contests it, and there is nothing honest to put there. Three sources agreeing
that a thing is broken are not evidence against the practice that says so.

## What would change this

The `promote_when:` above asks for a comparison rather than a fourth paper.
[LIT-180](../literature.d/LIT-180.md) is the one most likely to force the issue: it argues the
standard objective is unstable specifically on mixture-of-experts models, and
every frontier model this record holds is one.
