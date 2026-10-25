---
number: 419
status: Read
formerly:
- NOTE-tmpxapd8
paper: 'LIT-808'
title: 'Open Graph Benchmark'
version: 1
date: '2026-10-22'
summary: >-
  Fifteen larger graph datasets with application-driven splits and fixed
  evaluators. Wherever the authors re-ran a model on a random split of the
  same proportions, it scored higher, by 1.8 to 27 points, and its
  train–test gap almost closed. Read in full, including Appendix A.
---

# NOTE-419: Open Graph Benchmark

## Contribution

A benchmark suite, a package that downloads, splits and scores every
dataset the same way, and a public leaderboard. The datasets are larger
than the ones the field had used, and their splits are chosen to resemble
how a model would be used.

## Key insight

**A random split measures interpolation, and most applications ask for
extrapolation.** Products are labeled by popularity, papers arrive after
the training set, drugs bind new targets, and molecules come from new
scaffolds. Scoring on a random split removes the shift the model will face.

## Key results

- Same model, same split ratio, random against realistic (§4–6):
  products 88.20 / 78.50, proteins 87.83 / 77.68, arxiv 73.54 / 71.74,
  ddi 80.88 / 53.90, molhiv 82.73 / 77.07, molpcba 34.40 / 27.03, tox21
  86.03 / 77.57, ppa 92.91 / 70.37, code2 21.64 / 15.95
- Train–test gap: GraphSAGE on proteins 10.18 points under the species
  split against 0.27 under a random split. On ogbg-ppa it is almost 30
  points under the species split
- ogbn-mag (Table 8): mini-batch GraphSAINT and neighbor sampling beat
  full-batch R-GCN (47.51 and 46.78 against 39.77%), which the authors
  attribute to sampling noise acting as regularization
- ogbl-citation2 (Table 12): there, mini-batch training is worse than
  full-batch, the reverse of the node tasks
- Molecular graphs (Tables 15–16, Appendix A): GIN + virtual node +
  additional features is best on molhiv and molpcba. The best architecture
  varies across the 10 further MoleculeNet sets

## Limitations

- **Light baselines.** Width 256 or 300, two to five layers fixed, dropout
  from {0, 0.5}. They are reference points, not tuned comparisons
- **"Realistic" is argued, not measured.** No deployment data shows that
  the chosen split matches use. ogbl-biokg keeps a random split for lack
  of timestamps
- **Datasets were replaced** after release (ogbg-code to code2 for target
  leakage, ogbl-citation and wikikg for negative-sample bugs), so early
  leaderboard numbers are not comparable with later ones
