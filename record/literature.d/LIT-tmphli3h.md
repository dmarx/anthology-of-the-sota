---
status: Active
title: 'Sub-Scaling Laws: On the Role of Data Density and Training Strategies in LLMs'
version: 1
tags:
- training-optimization
- data-pipeline
- analysis-and-evaluation
date: '2026-09-25'
published: '2025-07-13'
arxiv: '2507.10613'
doi: '10.18653/v1/2025.acl-long.1163'
first_author: 'Chen'
keywords:
- 'sub-scaling'
- 'data-density'
- 'over-training-ratio'
- 'scaling-law-fit'
- 'data-redundancy'
- 'compute-allocation'
implementations: []
compared_against:
- LIT-028
- LIT-068
summary: >-
  Chen, Wang, Xiao, Wang, Chen, Cai, He and Wang (ACL 2025),
  [ARXIV-2507.10613](https://arxiv.org/abs/2507.10613), published at ACL as "Revisiting Scaling Laws for Language
  Models: The Role of Data Quality and Training Strategies". It claims that
  gains decelerate faster than a power law when data is "dense" or when
  tokens per parameter run high, and fits a modified Chinchilla law over
  more than 400 models from 20M to 7B. **None of it should be leaned on.**
  The density metric's embedding, dimension and cluster count are never
  stated. The fitted law has no density term, only two logistic multipliers
  on D/N bounded in [1.5, 2). And the paper's own Table 4 contradicts its
  "across all model sizes".
---

<!-- inactive-ok-file: SOTA-243 — Proposed; named as where the redundancy reading is
     held with better evidence than this paper's, not relied on -->

# LIT-tmphli3h: Sub-Scaling Laws: On the Role of Data Density and Training Strategies in LLMs

Chen, Wang, Xiao, Wang, Chen, Cai, He and Wang (2025) — [ARXIV-2507.10613](https://arxiv.org/abs/2507.10613).
Also ACL 2025 (long), pp. 23881–23899, as *Revisiting Scaling Laws for
Language Models: The Role of Data Quality and Training Strategies*,
[DOI-10.18653/v1/2025.acl-long.1163](https://doi.org/10.18653/v1/2025.acl-long.1163). The two versions have the same text; only
the title differs. Both keep a line written to a reviewer: "as you correctly
pointed out".

## Key takeaways

**The thesis.** "Sub-scaling" means gains that decelerate faster than a power
law. It has two causes: "high data density and non-optimal training resource
allocations".

**Data density** is a per-cluster count over the volume of an n-ball, combined
into one number per corpus. The Pile scores 0.64, deduplicated Pile 0.56, and
a "Density-Based Pile" 0.47. That last one was *selected from the Pile by the
same metric*.

**Training strategy** uses the over-training ratio `OTR = D/N`. Fitting
`L = λ_C / C^{α_C}` per OTR, "when OTR ≤ 50, … α_C decreases when increasing
OTR. And when OTR > 50 and OTR ≤ 1700, α_C follows a normal distribution with
Mean 0.0521". Batch size and learning rate are ruled out because bad
hyperparameters "show poor performance from the beginning … rather than
causing a deceleration".

**The fitted law** is `L = 455.345·R_D/D^0.289 + 61.929·R_N/N^0.272 + 1.372`,
with `R_D = 1 + 1/(1+exp(−0.00810·OTR))` and `R_N = 1 + 1/(1+exp(−0.00114·OTR))`.
The runs use AdamW with cosine decay to 10% on the Pile, at 12 sizes from 20M
to 7B.

## Traps

- **The density metric cannot be reproduced.** The embedding, the dimension n,
  the clustering algorithm and K are not stated anywhere. With a realistic n
  and no normalization the formula gives numbers of astronomical size, not
  0.47–0.64. It is also circular: it selects the low-density set and then
  scores it. And it is compared on two corpora, where selection also changes
  domain mix, quality and size.
- **The law has no density term.** `R_D` and `R_N` depend only on OTR, and for
  OTR ≥ 0 both lie in [1.5, 2). This is Chinchilla's form with each
  coefficient allowed to grow by up to a third as OTR rises, bought with two
  extra constants. A better in-sample fit is expected.
- **Its own tables contradict "outperforms … across all model sizes".** In
  Table 4 the Kaplan form has the lowest *fit* error at 50M, 100M and 300M, and
  the Chinchilla form the lowest *prediction* error at 4B. In Table 1, at 5B
  tokens, the traditional law predicts better (0.00757 against 0.00887).
- **The threshold is quoted two ways**: 50 in the main text, "around 20" in
  Appendix F.
- **The information-theoretic model predicts the opposite of what it is used
  for.** With `I(n) = I₀ n^{−α}` inserted into `P = P₀(1 − e^{−βI})`,
  performance *falls* with n. A marginal gain was used where a cumulative one
  was needed.
- **Fits use intermediate checkpoints of cosine runs.** "we use the first
  quarter of the training data to predict subsequent loss values". That is the
  confound [LIT-145](LIT-145.md) describes: under cosine, a checkpoint mid-run is
  not the loss of a run trained to that length. The within-run bend it calls
  sub-scaling is confounded with the schedule.

## Standing in the anthology

Filed from the reading-time triage of 2026-09-25. That entry counted this
work and its ACL version as one work, which is right, and proposed it as
bearing on [LIT-028](LIT-028.md) and the data-constrained note. Having been read, it
sources nothing.

**Where the idea is held with better evidence.**
[LIT-166](LIT-166.md) (Muennighoff et al.) is the record's Chinchilla-form law with
decay terms, fitted over 400 controlled runs that actually repeat data. This
paper names its multipliers "repetition factors" and never repeats anything.
The reading that redundancy bends data scaling is
[SOTA-243](../practices.d/SOTA-243.md)'s, via [LIT-399](LIT-399.md).
[SOTA-164](../practices.d/SOTA-164.md) (deduplicate) gets nothing from Table 2, because
no model is trained on the deduplicated corpus.

It is kept because the ideas it gestures at are real and the record's
neighbours hold them well, and because a reader who meets its headline
should find this note first.
