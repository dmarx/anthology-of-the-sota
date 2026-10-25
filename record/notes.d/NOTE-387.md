---
number: 387
status: Read
formerly:
- NOTE-tmp58sq2
paper: LIT-812
title: 'EGNN'
version: 1
date: '2026-10-22'
summary: >-
  Equivariance without spherical harmonics: messages see squared distances,
  coordinates move along relative position vectors. Clear gains on a
  synthetic N-body task and graph autoencoding; on QM9 it runs as an
  invariant model. Main text and appendices read, the proofs skimmed.
---

# NOTE-387: EGNN

## Contribution

A message-passing layer equivariant to rotations, reflections, translations
and permutations in any dimension, at the cost of an ordinary GNN, by
updating a coordinate per node with a learned scalar weighting of relative
position vectors.

## Key insight

**Keep features invariant and let only the coordinates carry direction.**
Squared distances go into the message, and the coordinate update is a
weighted sum of differences, so nothing higher than a vector ever appears.
Whether that loses expressiveness depends on the task: the appendix shows it
does not for scalar targets on a complete graph.

## Key results

- N-body MSE 0.0071 against 0.0104 (Radial Field) and 0.0107 (GNN), with
  forward time 0.0062 s against 0.0343 for TFN
- Data sweep from 100 to 50,000 trajectories: EGNN best throughout, the
  feature-free Radial Field good early and flat late (Figure 2)
- Graph autoencoding with noise coordinates: 0.11% edge error on
  Erdős–Rényi against 1.25% for a GNN given the noise as features
- QM9, as an invariant model: U0 11 meV against SchNet 14 and DimeNet++ 6

## Limitations

- **Fully connected graphs.** Every experiment exchanges messages between
  all pairs, at most 29 nodes. The distance argument and the cost advantage
  are both untested at the scale and with the cutoffs molecular simulation
  uses
- **Equivariance is exercised on one synthetic task.** The QM9 model skips
  the coordinate update, and the autoencoder's coordinates are noise
- **Baselines.** TFN and the SE(3)-Transformer were run from one
  implementation with a swept degree and width; the GNN shares EGNN's MLPs,
  which makes it a fair ablation rather than a strong baseline
