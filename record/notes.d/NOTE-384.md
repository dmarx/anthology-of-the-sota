---
number: 384
status: Read
formerly:
- NOTE-tmp2catj
paper: 'LIT-829'
title: 'MPNN'
version: 1
date: '2026-10-22'
summary: >-
  Eight earlier graph networks are one form: summed messages, a node
  update, an invariant readout. Searching that space on QM9 gives a model
  at chemical accuracy on 11 of 13 targets, relative to DFT labels and on
  one random split. Long-range mechanisms, a master node or set2set, help
  most when geometry is withheld. Main text read in full, supplement
  skimmed.
---

# NOTE-384: MPNN

## Contribution

A shared vocabulary for graph neural networks: message, update and readout
functions. Under it, eight published models become points in one design
space. A search of that space produced the best QM9 results of its time
and a set of design findings for molecular property prediction.

## Key insight

**The models were variations on one computation, so stop inventing new
ones and push the family on one important task.** The paper's argument
for why is that convolutional networks needed careful empirical work, not
new theory, to displace hand-engineered features.

## Key results

- Table 2, error ratios on QM9: best single MPNN (edge network + set2set,
  explicit hydrogens) averages 0.68 and is below 1 on 11 of 13 targets.
  Gap (1.60) and ZPVE (1.27) miss. A five-model ensemble averages 0.52
- Table 3, no spatial input: GG-NN 3.47, + virtual edges 2.90, + master node
  2.62, + set2set 2.57. All three help on all 13 targets
- Table 4, towers: joint training 1.92 → 1.75, per-target 1.53 → 1.37
- Supplementary Table 6: with 11k training molecules the model already
  matches the best 110k-sample baseline on R² and ω₁

## Limitations

- **One random split** of 110k / 10k / 10k and no repeated seeds. The
  validation set chose among 50 random hyperparameter trials per target
- **Labels are DFT outputs.** Chemical accuracy relative to DFT is a
  statement about fitting the simulator
- **Table 3 used partial charges**, a DFT output, as an input feature. The
  headline Table 2 does not
- **Small molecules only** (up to 9 heavy atoms). The authors name
  generalization to larger graphs as the open problem, and note that their
  best spatial models use a fully connected graph whose message count
  grows with size
