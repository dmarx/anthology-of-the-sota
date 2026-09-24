---
number: 121
status: Active
title: 'Use Muon with decoupled weight decay and AdamW-matched update RMS in place of AdamW'
version: 3
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to LIT-153 as well. It argues Muon's shrinking advantage is not
    intrinsic but an artefact of constant decoupled weight decay fixing the
    equilibrium norm, and recovers 20-30% by pinning the norms — a result
    about the magnitude of this practice's own claim, from a group outside
    the one making it. The body already turned on it when saying what should
    not be quoted any more. The recommendation is unchanged.
- version: 3
  date: '2026-09-24'
  note: >-
    Adds where the gain comes from. Wang et al. (LIT-654) ablate Muon
    block by block: value-output attention weights plus the FFN nearly recover
    the full-Muon trajectory, and query-key contributes little. This document
    recommended an optimizer without saying which parameters it pays for, and
    the answer is not the one parameter counting predicts — QK and VO are the
    same size. The recommendation is unchanged, because the finding is about
    where the benefit sits rather than whether to take it, and because the
    recovery is architecture-sensitive.
tags:
- training-optimization
- tiny-models
date: '2026-09-05'
source:
# The blogpost is where the practice is stated as a recipe; LIT-122 is the
# production form and the scaling evidence; LIT-159 is the origin;
# LIT-156 is the outside comparison that puts a smaller number on it, and
# LIT-153 is the argument that the smaller number is an artefact of how
# LIT-156 held weight decay — evidence about the size of the claim, from
# outside the group making it (ADR-017). The frontier adopters LIT-131,
# LIT-132 and LIT-139 stay in the body.
- LIT-119
- LIT-122
- LIT-159
- LIT-156
- LIT-153
introduced_by:
- LIT-159
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. Stable at nearly the same optimal LR as AdamW, better evaluations; used for every Falcon-H1-Tiny model.
corrected_by:
- SOTA-131
compared_against:
- SOTA-168
extends:
- SOTA-165
explained_by:
- THEORY-024
- THEORY-033
- THEORY-099
---

<!-- inactive-ok-file: THEORY-099 — Proposed, filed in this same
     contribution as the account under this practice's newly recorded scope
     finding. The practice declares explained_by on it, so the citation is the
     relation; the recommendation stands without the account, and the section
     citing it says in its own text that the evidence is one group at small
     scale. -->

# SOTA-121: Use Muon with decoupled weight decay and AdamW-matched update RMS in place of AdamW

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

Muon itself is Jordan et al. (2024), [LIT-159](../literature.d/LIT-159.md) — an optimizer for the hidden
layers, orthogonalising the momentum update via Newton-Schulz iterations and
leaving embeddings and the head to AdamW. It is a blog post rather than a
paper, which is why the record holds it under a `url:` ([ADR-009](../decisions.d/ADR-009.md)), and it is
what every practice in this line modifies.

Muon as modified in [ARXIV-2502.16982](https://arxiv.org/abs/2502.16982) ([LIT-122](../literature.d/LIT-122.md)): weight decay applied to the
orthogonalised update, and the update's RMS rescaled to match what AdamW
would produce, so that the learning rate and weight decay tuned for AdamW
carry over. Under that recipe the authors saw stable training at nearly the
same optimal learning rate as AdamW and better downstream evaluations, and
adopted it for every model in the series, at 90M and 0.6B.

Conditions: the comparison here is at tiny scale with a µP-parameterised
hybrid Mamba/attention model. The RMS matching is what makes the AdamW
hyperparameters transferable; without it the learning rate has to be
re-tuned. Muon applies to matrix parameters — embeddings, norms and other
vectors keep an Adam-style update.

At a trillion parameters this recipe alone let attention logits run past
1000; [SOTA-131](SOTA-131.md) is the addition that bounds them, and the chain is written
out there.

## How much it buys

Less than the record used to say, and the honest range is wide. [LIT-122](../literature.d/LIT-122.md)'s
scaling-law runs report roughly 2× the compute efficiency of AdamW. An
outside comparison tuning both optimizers separately and judging at the end
of training rather than mid-run ([LIT-156](../literature.d/LIT-156.md)) gets 1.4× at 0.1B, falling
to **1.1× at 1.2B** — and finds that ranking two optimizers on intermediate
checkpoints can reverse the answer, which is one way the larger figures were
reached.

The practice stands at 1.1×, for reasons the number does not carry: the gain
is free once the recipe is in place, Muon's smaller optimizer state and
hyperparameter transferability are not what that study measures, and every
frontier adopter in the record ([LIT-131](../literature.d/LIT-131.md), [LIT-132](../literature.d/LIT-132.md), [LIT-139](../literature.d/LIT-139.md)) trains far above
its largest scale. What should not be quoted any more is the 2×.

[LIT-153](../literature.d/LIT-153.md) argues the shrinkage is not intrinsic but an artefact of
constant decoupled weight decay fixing the equilibrium weight norm, and
recovers 20–30% by pinning the norms instead. If that holds up outside its
authors' group it changes this section again.

## Which parameters the gain is actually paid on

This practice says to use Muon in place of AdamW and does not say where the
advantage comes from. Wang et al. (`LIT-654`) ran the ablation: train with
Muon on some blocks and Adam on the rest, everything else matched.

- **VO + FFN nearly recovers the full-Muon trajectory**, in both gated and
  ungated FFN settings.
- **Query-key contributes little.** Applying Muon to `W_V` alone, or `W_O`
  alone, already beats applying it to the whole of QK.
- Within the effective set, `W_O` matters more than `W_V`, and `W_out` more
  than `W_in`.

Not a parameter-count effect, and the paper says so: **QK and VO are the same
size.** Their account is that VO and the FFN are the blocks that behave as
associative memories, and that orthogonalising an update is what treats each
stored outer-product direction alike — `THEORY-099`.

**Nothing here changes the recommendation**, for two reasons. The recovery is
architecture-sensitive: in the ungated setting VO + `W_out` alone nearly
recovers full Muon, and in the gated setting the same combination falls short.
And VO+FFN *nearly recovers* full Muon rather than beating it, so this is not
a reason to run a hybrid — it is an answer to what you are buying.

It does bear on cost. If a deployment cannot afford Muon everywhere, the
ablation says where to spend it first; that is a claim from one group at small
scale with a 0.7B check, and is not yet a practice.

## Known implementations

- Falcon-H1-Tiny (all released checkpoints); Kimi K2, Kimi K3 and DeepSeek-V4 with the additions in [SOTA-131](SOTA-131.md)
