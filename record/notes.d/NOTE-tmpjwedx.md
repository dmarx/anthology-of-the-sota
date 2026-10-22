---
status: Read
paper: LIT-tmpdibco
title: 'RotatE'
version: 1
date: '2026-10-22'
summary: >-
  Relations as rotations of complex vectors model symmetry, inversion and
  composition, and self-adversarial negative sampling trains them. The
  paper's own control shows TransE trained the same way nearly matches it on
  FB15k-237 and stays well behind on FB15k. Read in full, including the
  appendix proofs and ablations.
---

# NOTE-tmpjwedx: RotatE

## Contribution

A knowledge-graph embedding in which each relation rotates entity vectors
element-wise in the complex plane, an analysis of which relation patterns
each earlier model can represent, and a negative-sampling scheme that
weights negatives by how plausible the current model finds them.

## Key insight

**Rotation keeps what translation gets right and adds what it cannot.**
Composing rotations adds angles, as composing translations adds vectors, and
inverting is conjugation; but a rotation by π is its own inverse, so a
symmetric relation needs no collapse to zero. With entity moduli fixed and
small angles, RotatE reduces to TransE (Theorem 4). The second insight is
the paper's ablation: much of what a scoring function seems to buy is the
training recipe.

## Key results

- Filtered MRR: FB15k 0.797, WN18 0.949, FB15k-237 0.338, WN18RR 0.476
  (Tables 4–5)
- TransE trained with the same sampling and loss: FB15k-237 0.332, FB15k
  0.735 (Table 8)
- Self-adversarial sampling on FB15k-237: RotatE 0.297 to 0.338, TransE
  0.297 to 0.332 (Table 13)
- Learned phases show symmetry at 0 or π and inversion as conjugation
  (Figure 2)

## Limitations

- **The lemmas are about representation, not learning.** Each proof shows
  that if a pattern holds exactly, the relation vectors must satisfy an
  equation; whether training finds that solution is the histograms'
  evidence, on a few hand-picked relations
- **Main tables compare against reported numbers** from other papers'
  training, which Table 8 shows matters as much as the score function on
  FB15k-237
- **Three seeds** for spreads, reported only for RotatE (Table 14)
- **Large grid on validation**: dimension up to 1000, up to 1024 negatives,
  seven margins
