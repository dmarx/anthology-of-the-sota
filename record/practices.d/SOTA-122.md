---
number: 122
status: Proposed
promote_when: >-
  An independent group training with learnable multipliers themselves. A
  group confirming the weight-decay equilibrium this practice diagnoses is
  not it — LIT-153 did that, at 1.2B, without adopting the remedy.
consensus: unreplicated
consensus_note: >-
  One team, one architecture family. LIT-153 confirmed the diagnosis from an
  independent group and adopted a different remedy, which is not agreement
  or disagreement about this one.
title: 'Attach learnable per-row and per-column multipliers to weight matrices so their norms are learned, not set by LR and WD'
version: 2
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to the paper the claim comes from, not only to the blogpost that
    validated it at 90M. LIT-121 is where the weight-decay-equilibrium result
    and the multiplier remedy are stated; naming only LIT-119 credited the
    validation with the claim. The recommendation is unchanged. LIT-153 stays
    out on purpose — it confirms the diagnosis with a different remedy, which
    the promotion condition already says is not the result this needs.
tags:
- training-optimization
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source:
# LIT-121 is the claim; LIT-119 is the 90M validation of it. The blogpost
# alone was named here until #58, which is the singular-source habit ADR-010
# replaced — and this practice is the example ADR-010 itself argues from.
# LIT-153 confirms the diagnosis with a different remedy and is deliberately
# absent: see the promotion condition.
- LIT-121
- LIT-119
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. Up to 20% relative gain on MMLU, BBH and GSM8K over a Muon baseline at 200 GT.
---

# SOTA-122: Attach learnable per-row and per-column multipliers to weight matrices so their norms are learned, not set by LR and WD

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

The claim, from [ARXIV-2601.04890](https://arxiv.org/abs/2601.04890) ([LIT-121](../literature.d/LIT-121.md)) and validated in the blogpost at the 90M
scale: under a decoupled weight decay, a matrix layer settles into an
equilibrium norm determined by the learning rate and the weight decay
coefficient rather than by the data. Attaching a learnable scalar multiplier
to each row and each column of every weight matrix (the authors' *learnable
multipliers*, LRM) lets the norm be learned, and lets the forward multipliers
that µP would otherwise fix be learned too.

Evidence: two 200 GT runs (50 GT of decay), Muon alone against Muon with
LRMs, on the final 90M architecture. Improvements on most benchmarks, up to
a 20% relative gain on MMLU, BBH and GSM8K — **"from random values"**, in the
source's own words, a qualifier this practice used to drop. At 90M those
three benchmarks sit near chance, so a fifth of the distance above chance is
a much smaller claim than a fifth of the score, and it is the claim the
blogpost makes. The authors then used LRMs for
every model in the series.

Why *Proposed* and not *Active*: one team, one architecture family, and the
larger-scale results live in the preprint rather than in this source.

The condition as first written — "an independent reproduction **or** a result
above 1B" — has since been half-met in a way that shows the *or* was doing
too much work. [LIT-153](../literature.d/LIT-153.md) is an independent group, at up to 1.2B, working on
exactly the phenomenon this practice rests on: the weight-decay equilibrium
that fixes a matrix's norm by hyperparameters rather than data. They confirm
the diagnosis and go further, arguing that equilibrium is *why* matrix
optimizers' advantage shrinks with scale.

But their remedy is the opposite of this one. Learnable multipliers give the
scale its own learned parameter; Hyperball pins the Frobenius norms to
constants and removes the degree of freedom. So an independent group above 1B
has confirmed the *mechanism* and declined the *fix*, which the original
condition would read as a promotion and which plainly is not one.

## Known implementations

- Falcon-H1-Tiny (all released checkpoints)
