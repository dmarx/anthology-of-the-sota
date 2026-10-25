---
number: 452
status: Proposed
formerly:
- SOTA-tmpd2i1s
promote_when: >-
  A group other than these two runs a comparison on a benchmark outside small
  molecular graphs, with node features that carry little structure. The base
  model and parameter budget are held fixed and only the encoding varies: no
  PE, Laplacian eigenvectors with random flips, RWPE, and a sign-invariant
  eigenvector encoder. The same ordering appears. A leaderboard entry that
  uses RWPE or SignNet without that ablation does not count, nor does a
  result on ZINC.
title: 'Give a message-passing GNN random-walk positional encodings, or Laplacian eigenvectors through a sign-invariant encoder, rather than raw Laplacian eigenvectors with random sign flips'
version: 1
tags:
- graphs-and-networks
- representation-and-encoding
date: '2026-10-22'
source:
- LIT-833
- LIT-818
introduced_by:
- LIT-833
- LIT-818
consensus: unreplicated
consensus_note: >-
  Two independent groups, each comparing against raw Laplacian eigenvectors
  with random sign flips inside its own controlled ablation, and both
  measuring the decisive comparison on ZINC. Neither tests the other's
  encoding under the same protocol. Graph transformer toolkits such as GPS
  (LIT-842) offer both encodings as options. That is adoption, not
  evidence, and how widely either is the default has not been assessed
  here.
implementations: []
summary: >-
  Dwivedi et al. (2022), [LIT-833](../literature.d/LIT-833.md), and Lim et al. (2023), [LIT-818](../literature.d/LIT-818.md).
  On ZINC with the same GatedGCN and about 500k parameters, Laplacian
  eigenvectors with random sign flips give test MAE 0.202 and 0.198 in the
  two papers. Random-walk return probabilities (RWPE) at the input give
  0.122, and the same 8 eigenvectors through SignNet give 0.121. For GINE
  and PNA, flipped eigenvectors are no better than no encoding. On OGB
  molecules, whose features already mark rings, every gain is under 2%.
explained_by:
- THEORY-133
---

<!-- inactive-ok-file: THEORY-133 — Proposed, filed in this same contribution as the reason this practice gives -->

# SOTA-452: Give a message-passing GNN random-walk positional encodings, or Laplacian eigenvectors through a sign-invariant encoder, rather than raw Laplacian eigenvectors with random sign flips

## Source

Dwivedi et al. (2022), [LIT-833](../literature.d/LIT-833.md), read as [NOTE-386](../notes.d/NOTE-386.md). Lim et al.
(2023), [LIT-818](../literature.d/LIT-818.md), read as [NOTE-410](../notes.d/NOTE-410.md). The reason the raw
eigenvectors fall short is [THEORY-133](../theory.d/THEORY-133.md).

## The practice

Both halves come from controlled ablations against the same baseline.
Dwivedi et al. introduced RWPE in [LIT-833](../literature.d/LIT-833.md). With a 16-layer GatedGCN on
ZINC, eigenvectors at the input give 0.202 MAE and RWPE at the input gives
0.122, with nothing else changed (Table 3). Lim et al. introduced SignNet
in [LIT-818](../literature.d/LIT-818.md). With the same base model on ZINC, eigenvectors with random
flips give 0.198 and the same 8 eigenvectors through SignNet give 0.121
(Table 1). For GINE and PNA, flipped eigenvectors score 0.178 and 0.132,
no better than no encoding (0.170 and 0.133), while SignNet gives 0.147 and
0.105. Without edge features the gap is larger (Table 7). GIN goes from
0.341 with flipped eigenvectors to 0.238 with SignNet.

- **The cheap default is RWPE.** For each node, the probabilities of
  returning to itself after 1 to k random-walk steps, with k around 16–20 on
  molecules. Add it at the input. Adding it only at the final layer did
  nothing (0.249 against 0.251 with no encoding)
- **If you use eigenvectors, process them sign-invariantly.** Feed each
  eigenvector and its negation through a shared network φ and sum, as
  SignNet does. Do not fix the sign by a canonical rule. That scored 0.298,
  worse than no encoding
- **Then consider the extras.** LSPE's learnable positional channel takes
  RWPE from 0.122 to 0.093 at 1.7× epoch time. SignNet on all eigenvectors
  rather than 8 reaches 0.100. Both are smaller and costlier steps than the
  first one
- **Keep treating the encoding as a hyperparameter** for every model in a
  comparison, as [SOTA-349](SOTA-349.md) says. This practice narrows which candidates to
  include, not whether to tune

## Conditions

- **Measured where node features carry little structure.** ZINC gives bare
  atom and bond types. On OGB-MOLTOX21 and MOLPCBA, whose features already
  mark ring membership, LSPE's gains are 0.003–0.006 AUC or AP
- **One benchmark carries both halves.** Neither paper runs the other's
  encoding under its own protocol, and the head-to-head numbers (0.122 vs
  0.121) come from different codebases
- **It does not make the network fully invariant.** SignNet handles signs,
  not rotations within repeated eigenvalues, which 64% of ZINC graphs have.
  RWPE is not unique for every node
- **It goes beyond 1-WL, which [SOTA-351](SOTA-351.md)'s sum aggregation cannot.** That
  practice's own conditions point here for tasks that need more than 1-WL
