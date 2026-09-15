---
status: Proposed
promote_when: >-
  A frontier-scale report comparing an upcycled model against one trained
  sparse from scratch at MATCHED TOTAL compute, dense pretraining included,
  and carried far enough to say where the advantage goes as the
  post-upcycling budget grows. A lab saying it upcycled satisfies nothing —
  that is adoption, and it does not answer the question this practice turns
  on.
title: 'Initialize a mixture-of-experts model from a dense checkpoint rather than training it from scratch'
version: 1
tags:
- model-architecture
date: '2026-09-15'
source:
- LIT-tmpolljg
introduced_by:
- LIT-tmpolljg
summary: >-
  Komatsuzaki et al. (2022), [LIT-tmpolljg](../literature.d/LIT-tmpolljg.md) — seed the experts from a dense
  checkpoint you already paid for. Upcycled T5 and ViT models beat their
  dense counterparts at ~50% of the dense pretraining sunk cost, and beat
  sparse models trained from scratch on 100% of it: same architecture, same
  compute, different initialization.
extends:
- SOTA-150
---

# SOTA-tmpmc10q: Initialize a mixture-of-experts model from a dense checkpoint rather than training it from scratch

## Source

Komatsuzaki et al. (2022), [LIT-tmpolljg](../literature.d/LIT-tmpolljg.md) — Sparse Upcycling.

[SOTA-150](SOTA-150.md) says make the feed-forward layers sparse. This says where the sparse
model should start, and the answer is: from a dense one you have already
trained.

## The comparison that carries it

The headline is the wrong one to read. That upcycled models beat their **dense
counterparts** at ~50% of the dense pretraining sunk cost is an argument for
sparsity, which [SOTA-150](SOTA-150.md) already makes.

The claim this practice rests on is the second comparison: upcycled models
also beat **sparse models trained from scratch on 100%** of that same budget.
Same architecture, same total compute, different initialization — which is
what makes it a recommendation about how to start rather than about what to
build.

<!-- inactive-ok-block: THEORY-tmptabiw — Proposed, and cited as the reason
     to EXPECT this rather than as evidence for it; the evidence is the
     comparison above, and this practice would stand without the account. -->
The reason to expect it is [THEORY-tmptabiw](../theory.d/THEORY-tmptabiw.md): the dense checkpoint already
contains a functional partition, so seeding experts from it is not an
arbitrary warm start but a handover of structure the dense run had already
found.

## Conditions, and why this is `Proposed`

The results are T5 Base/Large/XL and ViT Base/Large, in 2022. That is a real
demonstration and it is not frontier scale, and the record should not let a
2022 vision-and-language result stand in for what a 2026 trillion-parameter
run would do.

The unanswered question is the one a lab would actually ask: the advantage is
measured at a budget, and nobody has reported where it goes as the
post-upcycling budget grows. If the from-scratch model catches up given enough
tokens, upcycling is a way to spend a checkpoint you happen to have rather
than a reason to train densely first — a different and much narrower claim.

The paper itself offers no account of why the dense initialization helps, and
says so. The explanation is filed separately, which is the arrangement that
lets this practice be provisional while the finding under it is not.
