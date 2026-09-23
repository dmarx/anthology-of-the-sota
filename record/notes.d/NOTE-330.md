---
number: 330
status: 'Read'
formerly:
- NOTE-tmpkgbhw
paper: 'LIT-608'
title: 'Baroni, Dinu & Kruszewski: Don''t count, predict!'
version: 1
date: '2026-09-23'
summary: >-
  84 count and predict models on 14 lexical-semantics benchmarks from one
  2.8B-token corpus. word2vec CBOW beats count vectors almost everywhere and
  is far more robust to bad settings. The count side lacked word2vec's
  smoothing and negative shift, which is how [LIT-607](../literature.d/LIT-607.md) later reversed the
  result. Read in full.
---

# NOTE-330: Baroni, Dinu & Kruszewski: Don't count, predict!

## Contribution

The first broad, same-corpus comparison of count-based distributional vectors
against prediction-trained ones. It concluded decisively for prediction, and
became the standard citation for that view.

## Key insight

**The result depends on what each family was allowed.** The paper shows this
twice. Swapping word2vec for Collobert and Weston's vectors reverses the
conclusion, as the authors note. Giving the count models word2vec's
smoothing and shift also reverses it, as [LIT-607](../literature.d/LIT-607.md) found a year later. A
comparison between two families is a comparison between the two specific
configurations chosen to represent them.

## Key results

- Best per task (Table 2), count against predict: rg 74 / 84, ws 62 / 75,
  wss 70 / 80, wsr 59 / 70, men 72 / 80, TOEFL 76 / 91, ap 66 / 75,
  analogies 49 / 68. Selectional preference ties (up 41 / 41, mcrae 27 / 28)
- Worst setup across tasks: count rg 11 and analogies 1, predict rg 74 and
  analogies 27
- Tuned on rg and tested on the rest: predict stays close to its best, and
  count changes little
- Best count model: window 2, PPMI, uncompressed 300K dimensions. Best
  predict model: window 5, 10 negatives, subsampling, 400 dimensions

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | predict vectors beat count vectors on lexical semantics | weak | corrected by [LIT-607](../literature.d/LIT-607.md): settings were not equalized |
| C2 | predict vectors are more robust to parameter choice | moderate | Table 2, within these grids |
| C3 | negative sampling beats hierarchical softmax, and subsampling helps | moderate | Table 4 ranks, one benchmark mix |
| C4 | the choice of implementation can reverse a family comparison | strong | the cw result, stated by the authors |

## Limitations

- The count grid omits smoothing and the negative shift, and uses SVD with
  singular-value weighting
- CBOW only, with no skip-gram
- Several benchmarks are tiny, and there are no significance tests

## Recommendations

- **R1** — use prediction-based vectors over count-based ones. *Filed as
  retired*: [SOTA-380](../practices.d/SOTA-380.md), `Rejected` on [LIT-607](../literature.d/LIT-607.md)'s evidence.

<!-- inactive-ok-file: SOTA-380 — Rejected, and named as the retired recommendation; this citation records its retirement -->
