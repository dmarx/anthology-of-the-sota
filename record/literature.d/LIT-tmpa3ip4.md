---
status: Active
title: 'Distilling the Knowledge in a Neural Network'
version: 1
tags:
- inference-optimization
- training-optimization
- model-stability
date: '2026-09-25'
published: '2015-03-09'
arxiv: '1503.02531'
first_author: 'Hinton'
keywords:
- 'knowledge-distillation'
- 'soft-targets'
- 'softmax-temperature'
- 'ensemble-compression'
- 'specialist-models'
- 'model-compression'
implementations: []
summary: >-
  Hinton, Vinyals and Dean (NIPS 2014 Deep Learning Workshop),
  [ARXIV-1503.02531](https://arxiv.org/abs/1503.02531). This is where the word "distillation" in 112 files of
  this record comes from. It trains a student on the teacher's softmax at a
  raised temperature, adds a down-weighted hard-label term, and scales the
  soft term by `T²`. On speech, a 10-model ensemble distils into one model of
  the *same size as each member*, keeping 86% of the frame-accuracy gain and
  all of the 0.2-point WER gain. Three things usually quoted from it are not
  in it: the phrase "dark knowledge", a high temperature on the realistic task
  (the best was `T = 2`), and an ablation of `T²`.
---

<!-- inactive-ok-file: SOTA-tmprzws7 THEORY-tmpm6tyr — Proposed; the practice and account
     this paper sources, filed with it, Proposed for the reasons its Traps give -->

<!-- inactive-ok-file: SOTA-257 — Proposed; named as the practice this paper joins
     for its distillation leg only -->

# LIT-tmpa3ip4: Distilling the Knowledge in a Neural Network

Hinton, Vinyals and Dean (2015) — [ARXIV-1503.02531](https://arxiv.org/abs/1503.02531)

A workshop paper (NIPS 2014 Deep Learning Workshop) with one arXiv version
and one run per cell. That is part of why its instructions are not ablated.

## Key takeaways

**The recipe.** `q_i = exp(z_i/T) / Σ_j exp(z_j/T)`. The student is trained on
a transfer set against the teacher's softened distribution at the same high
`T`, and runs at `T = 1` afterwards. With labels, add a cross-entropy on them
at `T = 1`. "the best results were generally obtained by using a
condiderably lower weight on the second objective function" (typo original).
And: "Since the magnitudes of the gradients produced by the soft targets
scale as 1/T² it is important to multiply them by T² … This ensures that the
relative contributions of the hard and soft targets remain roughly unchanged
if the temperature … is changed while experimenting with meta-parameters."

**Logit matching is the high-temperature limit, under two conditions.** For
`T` large relative to the logits, and with logits "zero-meaned separately for
each transfer case", the gradient approaches `(1/(NT²))(z_i − v_i)`: logit
regression. At lower `T`, distillation "pays much less attention to matching
logits that are much more negative than the average". "Which of these effects
dominates is an empirical question."

**Speech: ensemble to one member-sized model** (85M DNN, 8 × 2560 ReLU,
14,000 outputs, about 2,000 hours):

| system | test frame accuracy | WER |
| --- | --- | --- |
| baseline | 58.9% | 10.9% |
| 10× ensemble | 61.1% | 10.7% |
| distilled single model | 60.8% | 10.7% |

That is 86% of the frame-accuracy gain. The student has the baseline's
architecture and data, and only its targets differ. It is one run on one test
set, and 0.2 WER on 23K words is about 46 words.

**Soft targets as a regularizer.** With 3% of the speech data, the baseline
reaches 44.5% test frame accuracy. With soft targets it reaches **57.0%**,
against 58.9% for the baseline on all the data. The teacher was trained on
all of it.

**MNIST.** A 2×800 student with "no regularization" makes 146 errors, and 74
with soft targets at `T = 20`. The regularized 2×1200 teacher makes 67. At
300 or more units any `T > 8` is about the same. At 30 units, "temperatures
in the range 2.5 to 4 worked significantly better".

**Specialists on JFT.** 61 specialists over confusable class clusters, combined
at inference by per-image KL minimization, give 25.0% → 26.1% top-1 in a
single run. **They are never distilled.** "We have not yet shown that we can
distill the knowledge in the specialists back into the single large net."

## Traps

- **"Dark knowledge" is not in the paper.** It is a phrase from talks. The
  paper's version is the BMW, garbage truck and carrot example. The two
  experiments offered for it do not separate "similarity structure over wrong
  classes" from generic confidence regularization. The omitted-digit result
  needs a bias shift tuned on the test set "(which optimizes overall
  performance on the test set)". The 3%-data result has a teacher that saw
  the other 97%.
- **On the realistic task the best temperature was 2.** For speech "we tried
  temperatures of [1, 2, 5, 10] … bold font indicates the best value". The
  bold is on 2, confirmed from the PDF's font data. `T = 20` is MNIST.
- **`T²` is a derivation, not a result.** No run compares with and without it.
  It rests on the high-`T`, zero-mean approximation, which is not obviously in
  force at `T = 2` on 14,000 classes, and the paper does not check.
- **The speech student is not smaller than a member.** "a single neural net of
  the same size". The compression shown is ensemble to member. Big-to-small is
  MNIST only.
- **The MNIST comparison is confounded.** The student baseline has no
  regularization at all, while the teacher has dropout and jitter. No
  dropout-regularized student is reported.

## Standing in the anthology

Filed as substrate from the reading-time triage of 2026-09-25: 112 files
mention distillation, and none held its source.

- It sources `SOTA-tmprzws7` (the soft-target recipe) and `THEORY-tmpm6tyr`
  (the account of why soft targets carry information). Both are `Proposed`,
  for the reasons in the traps.
- **It joins [SOTA-257](../practices.d/SOTA-257.md)'s evidence for the distillation leg
  only.** It is an independent measurement of ensemble-to-single-model
  distillation keeping most of the gain: 86% here against [LIT-441](LIT-441.md)'s
  83%. **The two use different methods.** [LIT-441](LIT-441.md) uses *sequence-level*
  distillation (Kim and Rush), not this temperature-softened logit matching.
  This paper never compares an ensemble against a single model of the same
  *total* size, which is [SOTA-257](../practices.d/SOTA-257.md)'s headline claim.
- [LIT-664](LIT-664.md) (DINO) calls itself "a form of knowledge distillation [35]
  with no labels", and [35] is this paper. Its student and teacher
  temperatures are this mechanism, repurposed.
- **No lineage relation is declared to either.** [LIT-441](LIT-441.md) cites this paper
  but runs Kim and Rush's method. DINO repurposes the temperature mechanism
  for a different problem. Declaring `extends` from both joined a
  language-model data line and a self-supervised vision line through this
  note, and the lint found they share no topic. The relation was stronger
  than the facts, so it is prose here.
- **The word is shared, not the method.** The record's diffusion step- and
  consistency-distillation documents use the same word for a different
  technique, with no soft targets or temperature, and should not cite this
  paper.
