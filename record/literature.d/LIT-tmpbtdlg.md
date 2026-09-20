---
status: Active
title: 'How do language models learn facts? Dynamics, curricula and hallucinations'
version: 1
tags:
- training-optimization
- data-pipeline
date: '2026-09-20'
published: '2025-03-01'
arxiv: '2503.21676'
first_author: 'Zucchet'
keywords:
- 'learning-dynamics'
- 'factual-recall'
- 'attention-circuits'
- 'data-curricula'
- 'hallucination'
implementations: []
summary: >-
  Zucchet et al. (2025), [ARXIV-2503.21676](https://arxiv.org/abs/2503.21676). Factual recall is learned
  in three phases with a long plateau between generic statistics and
  individual knowledge, and the plateau is the attention recall circuit
  forming — shown by patching a reference model's attention patterns in, at
  which point the plateau disappears. Imbalanced data shortens the plateau
  and slows acquisition afterwards, so a schedule beats either distribution.
---

# LIT-tmpbtdlg: How do language models learn facts? Dynamics, curricula and hallucinations
<!-- inactive-ok-file: SOTA-130 — Proposed, and named as one of the task-stage curricula this contrasts with -->
<!-- inactive-ok-file: SOTA-tmp8nitg — Proposed, and filed in this same contribution from this note -->

## Key takeaways

- **Three phases, not a curve.** A short first phase learning generic
  attribute-value statistics; then a **plateau** at exactly the loss an ideal
  model with no individual-specific knowledge would reach; then the
  acquisition of subject-attribute associations. The plateau's length grows
  almost linearly with the number of individuals.
- **The plateau is the recall circuit being built**, and the evidence is an
  intervention rather than a correlation. Patching in the attention patterns
  of a reference checkpoint makes the plateau *disappear*; patterns taken
  progressively later in the plateau are progressively better. Before the
  circuit exists, prediction errors at the attribute token do not backpropagate
  to the name tokens, so the rest of the model cannot learn.
- **Attention patterns from very early training are worse than the untrained
  ones** — the model first attends to attribute-type tokens to predict the
  generic distribution, which is exactly the wrong place for recall.
- **A trade-off in the data distribution.** Plateau length is set by the
  frequency of the *most* common individuals; acquisition speed after the
  plateau is set by the frequency of the *least* common. So imbalance
  shortens the plateau and slows what follows, and the optimum imbalance
  grows as the plateau takes a larger share of the budget — larger
  populations, shorter runs.
- **Therefore a schedule beats any fixed distribution**: start imbalanced to
  escape the plateau, then flatten to acquire the tail. The authors call this
  a rare case where a curriculum genuinely helps self-supervised learning.
  Optimal fixed imbalance is an inverse power law with exponent between 1 and
  2; a dynamic schedule beats the best fixed one.
- **Hallucinations arrive with knowledge, not after it.** Overconfident
  predictions on unseen individuals begin exactly when individual-specific
  knowledge does.
- **Fine-tuning is a poor way to add knowledge**: new facts are absorbed
  slowly and the process corrupts existing parametric memories quickly.

## Standing in the anthology

**It supplies a mechanism for something the record has only ever recorded as
a phenomenon.** Loss plateaus appear throughout the record's training
material as things to wait out or schedule around. This says that at least
one kind of plateau is a circuit under construction, and that the stall is
causal: without the extraction circuit, gradient signal does not reach the
tokens that need it. [THEORY-tmp8a4gm](../theory.d/THEORY-tmp8a4gm.md) is that account, and the patching
experiment is why it is more than a story.

**It gives the record its first data-schedule practice with a stated
mechanism.** [SOTA-tmp8nitg](../practices.d/SOTA-tmp8nitg.md) is the recommendation. The record holds several
curriculum practices ([SOTA-129](../practices.d/SOTA-129.md), [SOTA-130](../practices.d/SOTA-130.md), [SOTA-123](../practices.d/SOTA-123.md)) and all of them are
about stages of *task* — pretrain, then SFT, then RL. This is a curriculum
over the *distribution within* a stage, justified by two quantities moving in
opposite directions, which is a different and more falsifiable kind of claim.

**The fine-tuning result belongs beside [SOTA-199](../practices.d/SOTA-199.md)**, which regularises a
narrow fine-tune against the base model's own samples to stop it drifting.
That practice treats drift as a side effect to be contained; this says that
for *knowledge* specifically the corruption is fast and the absorption is
slow, so the trade is bad before any regulariser is applied.

**What it is, and is not.** A synthetic biography task, chosen so that
knowledge can be counted rather than probed. Everything here is a claim about
that setting, and the value is that the setting admits interventions —
attention patching, exact population control — that a natural corpus does
not.
