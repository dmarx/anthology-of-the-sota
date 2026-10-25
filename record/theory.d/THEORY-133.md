---
number: 133
status: Proposed
formerly:
- THEORY-tmpurxbz
promote_when: >-
  An ablation on a second kind of graph data, not small molecules, that
  holds the encoder's architecture and capacity fixed and varies only how
  the sign symmetry is handled: random flips, per-eigenvector processing
  without the sign-invariant sum, and the full φ(v)+φ(−v). It reproduces
  the ordering. A result that changes the number of eigenvectors or the
  encoder's capacity alongside the sign handling does not count. Neither
  does one that only shows invariant encoders score well.
title: 'Raw Laplacian eigenvector encodings underperform because the network must learn invariance to an arbitrary sign on every eigenvector, and building that invariance into the encoder recovers most of what they carry'
version: 1
tags:
- graphs-and-networks
- representation-and-encoding
- analysis-and-evaluation
date: '2026-10-22'
source:
- LIT-818
explains:
- SOTA-452
summary: >-
  Lim et al. (2023), [LIT-818](../literature.d/LIT-818.md). An eigenvector is defined only up to
  sign, so k of them have 2^k equally valid forms. On ZINC with a GatedGCN
  and 8 eigenvectors, the MAE falls step by step as less invariance is left
  to learn. Random flips leave all 2^k and score 0.198. A per-eigenvector
  encoder leaves 2 and scores 0.148. SignNet's sign-invariant sum leaves
  none and scores 0.121. The basis half of the paper's argument, for
  repeated eigenvalues, is not tested on any graph task.
---

<!-- inactive-ok-file: SOTA-452 — Proposed, filed in this same contribution as the practice this account explains -->

# THEORY-133: Raw Laplacian eigenvector encodings underperform because the network must learn invariance to an arbitrary sign on every eigenvector, and building that invariance into the encoder recovers most of what they carry

## Source

Lim et al. (2023), [LIT-818](../literature.d/LIT-818.md). Read as [NOTE-410](../notes.d/NOTE-410.md).

## What was actually shown

Lim et al. ran the ablation in [LIT-818](../literature.d/LIT-818.md) (Table 1), with a GatedGCN on
ZINC, 8 eigenvectors, a 500k-parameter budget and 4 seeds per row. The
rows differ in how many sign configurations the network is left to learn
invariance to:

- **Raw eigenvectors with random sign flips during training:** all 2^k.
  Test MAE 0.198
- **`MLP([φ(v_i)]_i)`, each eigenvector through a shared φ, no sum:** the
  network sees one eigenvector at a time, so 2 per eigenvector. 0.148
- **SignNet, `MLP([φ(v_i) + φ(−v_i)]_i)`:** invariant by construction.
  0.121

The ordering could have come out flat. If raw eigenvectors were weak
because they carry little useful information, or because the GatedGCN
could not use them, the three rows would score alike. They do not. For
GINE and PNA, flipped eigenvectors score no better than no encoding, and
SignNet improves both (0.178 to 0.147, 0.132 to 0.105). Without edge
features, GIN goes from 0.341 to 0.238 (Table 7).

Dwivedi et al. ([LIT-833](../literature.d/LIT-833.md)) make the same argument for why their
random-walk encoding beats eigenvectors on ZINC (0.122 vs 0.202). Their
comparison also changes what information the encoding carries, so it is
consistent with this account and cannot test it.

## What it explains

- Why [SOTA-452](../practices.d/SOTA-452.md) steers away from eigenvectors fed raw with random
  flips. Sign-free alternatives (RWPE) and sign-invariant processing
  (SignNet) both remove the symmetry the network would otherwise have to
  learn, and on ZINC the two land at the same score (0.122, 0.121)
- Why flipped eigenvectors can be worth nothing at all to a GNN that
  already does well without them (GINE, PNA)

## What this does not say

- **It does not say sign is the only problem.** Fixing the sign by a
  canonical rule scored 0.298, worse than no encoding. A rule that removes
  the ambiguity but is discontinuous or permutation-sensitive can hurt more
  than it helps. The account is about invariance done smoothly
- **It says nothing measured about basis invariance.** 64.1% of ZINC graphs
  have a repeated eigenvalue, so SignNet itself is not fully invariant on
  them. BasisNet is tested only on fitting synthetic filters with no test
  set. That half of the paper's argument is untested here
- **"Most of what they carry" is a claim on one benchmark.** The gains
  shrink where node features already encode the structure, as LSPE's OGB
  results show for its encoding
- **It does not compare SignNet with RWPE under one protocol.** The two
  scores that match come from different papers
