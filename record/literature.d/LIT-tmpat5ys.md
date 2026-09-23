---
status: Active
title: 'Don''t count, predict! A systematic comparison of context-counting vs. context-predicting semantic vectors'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-23'
published: '2014-06-01'
doi: '10.3115/v1/P14-1023'
first_author: 'Baroni'
keywords:
- 'distributional-semantics'
- 'count-vs-predict'
- 'word2vec'
- 'cbow'
- 'ppmi'
- 'svd'
- 'benchmark-comparison'
implementations:
- word2vec
- dissect
summary: >-
  Baroni, Dinu and Kruszewski (ACL 2014). The first broad comparison of
  count-based distributional vectors (36 PPMI/LMI models, full, SVD and NMF)
  against word2vec CBOW vectors (48 models), on 14 lexical-semantics
  benchmarks and a 2.8B-token corpus. Predict wins on almost every task, often
  by 10 points or more, and is far more robust to its worst settings. The
  count models were not given word2vec's context smoothing or negative shift,
  and SVD kept its singular-value weighting. [LIT-607](LIT-607.md) traces the result to
  those differences and finds no consistent winner when both are tuned alike.
corrected_by:
- LIT-607
---

# LIT-tmpat5ys: Don't count, predict! A systematic comparison of context-counting vs. context-predicting semantic vectors

Baroni, Dinu and Kruszewski, University of Trento — *ACL 2014*, 238–247,
DOI 10.3115/v1/P14-1023.

## Key takeaways

- **The question** (§1). Prediction-trained vectors were spreading with
  "triumphalist overtones" and almost no direct comparison against count
  vectors. The authors are count-vector researchers, and say their "secret
  wish" was to find it was all hype.
- **The setup** (§2). One corpus (ukWaC + Wikipedia + BNC, 2.8B tokens) and
  300K words for both. Count: windows 2 and 5, PPMI or LMI, full or SVD/NMF
  at 200–500 dimensions, 36 models. Predict: word2vec CBOW only, windows 2
  and 5, hierarchical softmax or 5/10 negatives, subsampling on or off,
  200–500 dimensions, 48 models.
- **The benchmarks** (§3). Relatedness (rg, ws, wss, wsr, men), TOEFL
  synonyms, categorization (ap, esslli, battig), selectional preference (up,
  mcrae) and the Google analogies.
- **Predict wins almost everywhere** (Table 2). With the best setting per
  task: rg 84 vs 74, ws 75 vs 62, TOEFL 91 vs 76, analogies 68 vs 49.
  Selectional preference is the one tie.
- **Predict is far more robust** (Table 2, worst setup). The worst count
  model collapses (rg 11, analogies 1), while the worst predict model stays
  usable (rg 74, analogies 27).
- **Within each family** (Tables 3–4). Count: PPMI beats LMI, and
  uncompressed beats SVD beats NMF. Predict: negative sampling beats
  hierarchical softmax, and every top-10 model uses subsampling.
- **The implementation matters as much as the family** (§4). Collobert and
  Weston's predict vectors do worse than the count models. "Had we … based
  our systematic comparison … on the cw model, we would have reached
  opposite conclusions."

## Standing in the anthology

**It is the claim [LIT-607](LIT-607.md) reversed, and is filed to record both.** Levy,
Goldberg and Dagan (2015) trace this result to settings that were not
equalized. word2vec ran with its tuned smoothing and negative sampling, which
the count models were not given, and SVD used its worst eigenvalue weighting.
Tuned alike, no family wins consistently. [LIT-607](LIT-607.md) is filed as `corrects`
this paper.

**The recommendation is filed as retired.** [SOTA-tmpcx9ae](../practices.d/SOTA-tmpcx9ae.md), "use
prediction-based vectors rather than count-based ones", is `Rejected`, and
[SOTA-379](../practices.d/SOTA-379.md) (tune the baselines alike before crediting a method) is filed as
`corrects` it. The paper was cited for years as the evidence for embeddings
over counts. [DP-005](../../docs/design-principles.md#dp-5) applies: citation is adoption, not evidence.

**What survives.** The benchmarks and the within-family findings. Negative
sampling beating hierarchical softmax and PPMI beating LMI agree with the
record's other sources. That every top predict model subsamples is
independent support for [SOTA-374](../practices.d/SOTA-374.md) on this benchmark mix. [LIT-607](LIT-607.md)'s ablation
finds the opposite for analogies, and the practice is contested for that
reason.

**The robustness result is not reversed, only explained.** Predict was
robust across its grid and count was not. Part of that is the grid: the
count side's worst cell combined LMI, NMF and a narrow window, and
[LIT-607](LIT-607.md)'s point is that the count side lacked the settings that make it
robust.

## What it does not establish

- **"Systematic" means within the grid the authors chose.** The authors say
  this themselves: options they did not consider "would have improved count
  vector performance somewhat". [LIT-607](LIT-607.md) found those options.
- **CBOW only.** Skip-gram, the stronger word2vec model in later
  comparisons, is not tested.
- **Uneven analogy search.** Analogy accuracy depends on vocabulary size,
  which differs from the state-of-the-art systems it is compared with.
- **No significance tests,** and several benchmarks are tiny: rg has 65
  pairs and esslli 44 concepts. The paper blames esslli's brittleness on
  its size.

<!-- inactive-ok-file: SOTA-tmpcx9ae — Rejected, and named as the retired recommendation; this citation records its retirement -->
