---
status: Active
title: 'Leaner Transformers: More Heads, Less Depth'
version: 1
tags:
- model-architecture
- attention-techniques
date: '2026-09-22'
published: '2025-05-27'
arxiv: '2505.20802'
first_author: 'Saratchandran'
keywords:
- 'multi-head attention'
- 'condition number'
- 'depth-width trade-off'
- 'parameter efficiency'
- 'vision transformers'
implementations: []
summary: >-
  Saratchandran, Teney and Lucey (2025), [ARXIV-2505.20802](https://arxiv.org/abs/2505.20802) — a
  theorem that more attention heads lower the condition number of the
  attention block, and twelve redesigned architectures trading heads for
  layers. In the five configurations where the MLP width is held fixed,
  accuracy holds or improves at **29–53% fewer parameters**. Read as
  [NOTE-tmph5061](../notes.d/NOTE-tmph5061.md).
---
<!-- inactive-ok-file: SOTA-190 THEORY-041 — both Proposed. SOTA-190 is
     named as the practice this paper pulls against, in a passage saying the
     tension is unexamined; THEORY-041 is named as the record's other source
     on conditioning. Both uses require them to be unsettled. -->

# LIT-tmpqux2k: Leaner Transformers: More Heads, Less Depth

Saratchandran, Teney and Lucey (2025) —
[ARXIV-2505.20802](https://arxiv.org/abs/2505.20802). Read as
[NOTE-tmph5061](../notes.d/NOTE-tmph5061.md).

## Key takeaways

- **A role for multi-head attention nobody had named.** Theorem 3.2: the
  condition number `κ(A) = σ₁(A)/σ_k(A)` of the attention block falls as the
  number of heads rises. Better-conditioned blocks are easier for
  gradient descent, so heads buy optimization rather than only expressiveness.
- **The trade that follows.** If conditioning is what depth was buying, then
  more heads should let you remove layers. Twelve architectures redesigned
  this way on ImageNet-1k, plus GLUE, TinyStories and Long-Range Arena.
- **Crammed BERT:** 16 layers / 12 heads at 119M scores GLUE average 78.6;
  10 layers / 24 heads at **84M (−29%)** scores 78.6.
- **The clean rows, where only depth and head count move.** XCiT-M 84.4M →
  59.0M with 81.4 → 81.7; TNT-B 65.4M → **30.9M (−53%)** at 82.3 → 82.3;
  DaViT-B 88.0M → 62.0M at 83.3 → 83.5; XCiT-L 189.1M → 103.8M at 82.1 →
  82.4; DaViT-L 196.8M → 140.0M at 83.6 → 83.6.
- **The paper says what it has not shown.** "While we lack a full theoretical
  explanation for this trade-off" — the theorem is about conditioning, the
  depth trade is empirical.

## Standing in the anthology

**It pulls against a practice the record holds, and nobody has run the
comparison.** [SOTA-190](../practices.d/SOTA-190.md) says to increase depth before any other
dimension when scaling. This removes depth and gets it back from head count.
The axes are not identical — that practice is about depth against width, this
is about depth against head count at fixed width — and the tension is real
enough to record in both documents and too unexamined to declare as a
relation.

**Its mechanism is the same quantity [THEORY-041](../theory.d/THEORY-041.md) is about.** That
account holds that unconstrained transformer matrices drift into a badly
conditioned shape and that the conditioning is correlated with slower
training. This says conditioning is improvable by an architectural choice
and measures the improvement. Neither cites the other; together they are the
record's two sources on conditioning as a design variable.

**Half the configurations change three things at once.** The ViT, DeiT and
VOLO rows shrink the MLP width alongside depth and heads, so their parameter
savings are not attributable to the trade the title names. The five rows that
hold the MLP fixed are the evidence, and they are enough.
