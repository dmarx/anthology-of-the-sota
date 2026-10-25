---
status: Read
paper: LIT-tmpo2awb
title: 'TransE'
version: 1
date: '2026-10-22'
summary: >-
  Relations as translations, h + r ≈ t, trained with a margin ranking loss
  against corrupted triples. Fewer parameters and better link prediction
  than the matrix-per-relation models of its time, and the source of FB15k
  and filtered ranking. Read in full.
---

# NOTE-tmp228zz: TransE

## Contribution

The simplest knowledge-graph embedding that worked at scale: one vector per
entity and one per relation, scored by distance after translation. It also
introduced the FB15k and FB1M datasets and the filtered evaluation that
removes true triples from the ranking.

## Key insight

**A more expressive model that cannot be fitted loses to a simpler one that
can.** SE can represent everything TransE can and fits its training data
worse. The translation prior is chosen for hierarchies, and it costs the
ability to separate the two sides of a symmetric relation, which must map to
a zero vector.

## Key results

- Filtered hits@10: WN 89.2%, FB15k 47.1%; best baselines 81.6% and 44.1%
  (Table 3)
- FB1M raw hits@10: 34.0%, against 17.5% for SE and 2.9% for the
  translation-free Unstructured model (Table 3)
- By relation type on FB15k, TransE leads on 1-to-1 and many-to-many and
  trails SME(bilinear) on the 1-to-many head and many-to-1 tail (Table 4)
- Hits@10 of 18% on an unseen relation from 10 examples (Figure 1)

## Limitations

- **Small tuning grid**: k ∈ {20, 50}, three learning rates, three margins,
  for TransE and the baselines alike
- **Benchmarks later found to leak** through inverse relations, which
  FB15k-237 and WN18RR remove
- **Symmetric and many-to-many structure** are where translation is weakest,
  and the authors note failure on the three-way Kinships data
- **No spreads**
