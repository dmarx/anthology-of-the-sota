---
status: 'Read'
paper: 'LIT-tmp56jtw'
title: 'Levy, Goldberg & Dagan: lessons from word embeddings'
version: 1
date: '2026-09-23'
summary: >-
  The prediction-over-count advantage for word embeddings came from design
  choices bundled with word2vec, not from the algorithm. Ported to PPMI and
  SVD and tuned alike across 672 representations, no method wins
  consistently, SGNS beats GloVe, and context-distribution smoothing is the
  only universally safe setting. Read in full.
---

# NOTE-tmpebd0y: Levy, Goldberg & Dagan: lessons from word embeddings

## Contribution

A controlled comparison of four word-representation methods (PPMI, SVD,
SGNS, GloVe) in which the "hyperparameters" hidden inside the neural methods'
implementations are named, ported to the count-based ones and tuned for all.
It replaces a settled-looking result (prediction beats counting, GloVe beats
word2vec) with "no consistent winner once you control for design".

## Key insight

**An algorithm's reported advantage includes everything shipped with it.**
Dynamic windows, subsampling, the negative-sample shift and the 0.75
smoothing exponent were each introduced in passing or only in code. Each is a
choice about how to weight co-occurrence statistics, and each can be given to
any method that uses those statistics. Once they are, the differences between
methods are small and change sign from task to task.

## Assumptions

- Bag-of-words contexts from a fixed window. Other context types are out of
  scope
- 500 dimensions for the dense methods, and a vocabulary of words seen at
  least 100 times in 1.5B tokens
- GloVe keeps its default weighting function and cannot express shifted PMI
  or smoothing

## Key results

- Vanilla, word2vec defaults and oracle-tuned settings (Tables 2–4): up to
  +15.7 points from tuning, more than 6 on average
- 2-fold cross-validated tuning (Table 5): within about 1 point of the oracle
- Similarity: SVD ≥ SGNS on average at windows 2 and 5, gap ≤ 1.7
- Google analogies: SGNS and GloVe lead PPMI by 3.7. MSR analogies: the only
  large gap, in SGNS's favour
- SGNS > GloVe on every task, including at 10.5B tokens
- cds = 0.75 against 1 (Table 8d): PPMI +0.0 to +9.2, SVD −0.3 to +2.2,
  SGNS 0 to +1.4
- sub (Table 8b): SGNS similarity up to +2.2, analogies −4.4 and −5.4. PPMI
  analogies −5.0 and −12.2
- eig (Table 6): at window 5, .616 (eig 0) and .612 (0.5) against .534 (1)

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | tuned alike, no method is consistently best on similarity and analogy | moderate | Table 5, 8 datasets, one corpus, no significance tests |
| C2 | Baroni et al.'s count-vs-predict gap was an artefact of unequal settings | moderate | the settings named, and reversed when equalized |
| C3 | SGNS outperforms GloVe | moderate | every task in Table 5, and at 10.5B tokens |
| C4 | context-distribution smoothing (0.75) is safe to apply blindly | moderate | Table 8d, all methods and tasks, one alternative value |
| C5 | smoothing helps because PMI overweights rare contexts | weak | argued (§3.2), and consistent with PPMI gaining most |
| C6 | eig = 1 is harmful for SVD word vectors | strong | Table 6, consistently large drops |

## Limitations

- One corpus and one language. Similarity and analogy benchmarks only
- No significance testing
- The smoothing exponent is compared at two values only
- Count methods are absent from the large-corpus comparison

## Recommendations

- **R1** — give baselines the same design choices and tuning before crediting
  a method. *Filed* as [SOTA-tmpl3rwi](../practices.d/SOTA-tmpl3rwi.md).
- **R2** — always apply context-distribution smoothing. *Folded into*
  [SOTA-375](../practices.d/SOTA-375.md) as its first measurement. The account is [THEORY-tmpghqdh](../theory.d/THEORY-tmpghqdh.md).
- **R3** — do not use eig = 1 for SVD word vectors. *Left in the reading*
  ([ADR-041](../decisions.d/ADR-041.md)): it is a setting of one method.
- **R4** — prefer many negatives for SGNS, and try w + c. *Left in the
  reading*: w + c changes sign across tasks.

<!-- inactive-ok-file: SOTA-375, THEORY-tmpghqdh — Proposed; named as where this reading's recommendation R2 was folded -->
