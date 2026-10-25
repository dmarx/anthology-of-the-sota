---
number: 453
status: Proposed
formerly:
- SOTA-tmphec3z
promote_when: >-
  A re-evaluation by a group that did not author any of the models, training
  several knowledge-graph score functions (at least TransE, DistMult,
  ComplEx and one later model) under one shared and separately tuned
  procedure on FB15k-237 and WN18RR, and reporting how far the published
  ranking of the score functions changes. A new-model paper that retunes its
  own baselines does not meet this: that is what the source already is.
consensus: unreplicated
consensus_note: >-
  One paper's ablation, on two datasets. The same point appears in the
  source's own Table 4, where DistMult as re-tuned by Kadlec et al. (2017)
  scores 0.798 MRR on FB15k, level with RotatE; that paper is not in the
  record. The lesson recurs for GNNs (SOTA-349, SOTA-350) and word
  embeddings (SOTA-379) from other groups. How far KGE papers now retune
  baselines has not been assessed here.
title: 'Before crediting a knowledge-graph embedding score function, train the baselines with the same loss, negative sampling and embedding size'
version: 1
tags:
- analysis-and-evaluation
- representation-learning
- graphs-and-networks
date: '2026-10-22'
source:
- LIT-819
# Kadlec et al. (2017) made the point earlier, by re-tuning DistMult, and is
# cited in the source's Table 4; it is not in the record, so the source is
# also named as the origin.
introduced_by:
- LIT-819
implementations:
- KnowledgeGraphEmbedding
summary: >-
  Sun et al. (2019), [LIT-819](../literature.d/LIT-819.md) — RotatE's main tables beat TransE's
  reported FB15k-237 MRR of 0.294 with 0.338. Trained with RotatE's own
  self-adversarial negative sampling, loss and 1000 dimensions, TransE
  reaches 0.332, and the authors note it then beats every earlier model on
  that dataset. On FB15k, which needs symmetric relations TransE cannot
  represent, the gap survives (0.797 against 0.735). Give every score
  function the same training before attributing a gap to the score function.
---

# SOTA-453: Before crediting a knowledge-graph embedding score function, train the baselines with the same loss, negative sampling and embedding size

## Source

Sun et al. (2019), [LIT-819](../literature.d/LIT-819.md). Read as [NOTE-406](../notes.d/NOTE-406.md). The same lesson
for other model families is [SOTA-349](SOTA-349.md), [SOTA-350](SOTA-350.md) and [SOTA-379](SOTA-379.md).

## The practice

The evidence is RotatE's own control, in [LIT-819](../literature.d/LIT-819.md). Sun et al. anticipated
that the gain might come from their new sampler rather than their score
function, and re-trained TransE and ComplEx in RotatE's setting. On
FB15k-237, self-adversarial sampling lifts TransE from 0.297 to 0.332 MRR
and RotatE from 0.297 to 0.338 (Table 13), so with training held equal the
two are 0.006 apart, where the main table's comparison to TransE's reported
0.294 shows 0.044. On FB15k the re-trained TransE stays at 0.735 against
RotatE's 0.797 (Table 8), consistent with the symmetry argument that
motivates RotatE. The control separated the two contributions; the headline
tables did not.

- **Hold the training recipe fixed across score functions.** The same loss
  (margin ranking or negative-sampling log-sigmoid), negative sampler,
  number of negatives, embedding size and tuning budget
- **Report the new sampler or loss as its own contribution**, with its
  effect on the baselines, since it transfers to them
- **Prefer FB15k-237 and WN18RR**, and say which relation patterns a
  dataset exercises when a gap is attributed to modeling a pattern
- **Count parameters, not nominal dimensions.** A complex embedding of
  "dimension k" has 2k reals

## Conditions

- **Two datasets and one older baseline in the decisive ablation.** ComplEx
  was re-trained only for Table 8, and DistMult and ConvE not at all
- **Filtered link prediction (MRR, hits@k)** on the standard Freebase and
  WordNet subsets
- **The score function can still matter.** The FB15k gap shows a case where
  it does, so the practice is about attribution, not about which model to
  use

## Known implementations

- `KnowledgeGraphEmbedding` (the RotatE authors' code)
