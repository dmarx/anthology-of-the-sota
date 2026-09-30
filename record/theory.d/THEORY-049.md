---
number: 49
status: Proposed
formerly:
- THEORY-tmpgsr9o
promote_when: >-
  The competition measured directly rather than inferred from the benefit of
  separating — gradient conflict or interference between modalities in a
  shared feed-forward, reported against a matched separated model. The
  leave-one-out result shows separation helps and that its benefit is
  asymmetric; it does not show what the shared parameters were doing.
title: 'Modalities compete for the same feed-forward parameters, the competition is not symmetric between them, and that is where separating by modality pays'
version: 1
tags:
- multimodal-learning
- training-optimization
date: '2026-09-21'
source:
- LIT-483
explains:
- SOTA-262
summary: >-
  Liang et al. (2024), [LIT-483](../literature.d/LIT-483.md) — untying transformer components
  by modality at controlled FLOPs pays most in the **feed-forward**, less in
  the attention projections, and not at all in the layer norms. Merging any two
  modalities into one tower degrades both, and by different amounts in each
  direction.
---

# THEORY-049: Modalities compete for the same feed-forward parameters, the competition is not symmetric between them, and that is where separating by modality pays

## Source

Liang, Yu, Luo, Iyer and colleagues (2024), [LIT-483](../literature.d/LIT-483.md) §3.5 and §4
— read as [NOTE-232](../notes.d/NOTE-232.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-262](../practices.d/SOTA-262.md) | give each modality its own weights and let the streams attend jointly | relief from a specific contention, located in a specific component — which is why the practice can now say *which* weights to untie and in what order |

## The account

A dense multi-modal transformer asks one set of parameters to serve tokens
with different statistics and, in the mixed-objective case, different training
signals. The claim is that they contend, and that the contention is located
rather than diffuse.

**The location is the feed-forward.** Untying components one at a time with
FLOPs held to the dense architecture, the feed-forward step is the large one
and the gains land on the image modality. Adding the `Q`/`K`/`V` projections
helps further but by less — about 33.3% FLOPs saved on image and 10% on text
against feed-forward-only. Adding the layer norms on top does essentially
nothing.

Two reasons are offered for that ordering. At the context length used (4,096)
the feed-forward is simply the larger share of the FLOPs. And the feed-forward
is where a transformer keeps its memory, so giving each modality its own
memory is where separation should pay — which is an argument about what the
component does rather than about how big it is.

**The competition is not symmetric.** The leave-one-out study merges pairs of
modalities into one tower and measures both. Every merge hurts both, and it
hurts them unequally: merging image with speech leaves image with most of its
gains while speech deteriorates; merging text with speech damages both. The
paper calls this non-reciprocal modality competition, and it means the cost of
sharing depends on which modality you are asking about, not only on how many
modalities share.

**Attention stays global throughout.** Separating the parameters does not
separate the normalization: every variant attends over the whole sequence.
So the account is about parameter contention specifically, and says nothing
about whether the modalities need to see each other — which they still do.

## Why `Proposed`

Because the competition is inferred from the benefit of relieving it, not
observed. Nothing here measures gradient conflict, interference, or capacity
contention in the shared parameters. What is measured is that separating
helps, that it helps most in one component, and that it helps modalities
unequally — all consistent with contention and all consistent with other
stories, including simply that more effective parameters per modality is
better and the feed-forward is where most parameters are.

The promotion condition asks for the mechanism measured rather than the
remedy's payoff.

## What this does not say

**It does not say layer norms should never be untied.** The authors are
explicit: their result is about untying layer norms *on top of* the
feed-forward and attention untyings, and says nothing about untying them
alone. That is a caveat worth carrying because "layer norms don't matter" is
the shorter and wrong version.

**It does not establish that global attention is necessary.** No arm varies
it. [SOTA-262](../practices.d/SOTA-262.md)'s promotion condition offered an ablation separating the
per-modality weights from the joint attention as an alternative satisfier, and
after two independent papers that ablation still does not exist.

**And the feed-forward ordering may be context-dependent.** Part of the
argument for it is the feed-forward's share of FLOPs at a 4,096-token context.
That share falls as context grows, so the ordering is a finding at one scale
rather than a property of transformers.
