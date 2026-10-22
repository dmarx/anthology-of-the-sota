---
status: Active
title: 'MACE: Higher Order Equivariant Message Passing Neural Networks for Fast and Accurate Force Fields'
version: 1
tags:
- physical-sciences
- graphs-and-networks
- model-architecture
date: '2026-10-22'
published: '2022-06-15'
arxiv: '2206.07697'
first_author: 'Batatia'
keywords:
- 'mace'
- 'interatomic-potentials'
- 'many-body-messages'
- 'atomic-cluster-expansion'
- 'body-order'
- 'equivariant-message-passing'
- 'learning-curves'
implementations:
- 'ACEsuit/mace'
compared_against:
- LIT-tmpm07pb
summary: >-
  Batatia, Kovács, Simm, Ortner, Csányi (NeurIPS 2022), [ARXIV-2206.07697](https://arxiv.org/abs/2206.07697).
  MACE builds each message as a symmetric tensor product of a neighbor
  sum, so one layer carries up to four-body correlations at roughly pairwise
  cost, and two layers suffice where two-body equivariant models need four to
  six. On 3BPA at 1200 K its force RMSE is 62.0 meV/Å against NequIP's 76.2,
  at about a quarter of NequIP's latency in the authors' code. On aspirin,
  raising body order steepens the learning curve (slopes −0.33, −0.51, −0.64)
  and, at body order four, adding equivariant features does not (−0.64,
  −0.63, −0.64).
---
<!-- inactive-ok-file: THEORY-tmpghjc1 — Proposed, filed in the same contribution from this paper's Figure 2; named as the record's reading of that figure -->

# LIT-tmpj25em: MACE: Higher Order Equivariant Message Passing Neural Networks for Fast and Accurate Force Fields

Batatia, Kovács, Simm, Ortner, Csányi, Cambridge, ENS Paris-Saclay and UBC
(NeurIPS 2022) — [ARXIV-2206.07697](https://arxiv.org/abs/2206.07697)

## Key takeaways

- **Many-body messages** (§4): a two-body equivariant feature A_i is pooled
  over neighbors, then a product basis B_i is formed from ν-fold tensor
  products of A_i with itself, which gives (ν + 1)-body messages without
  summing over pairs or triplets explicitly. The expensive tensor product
  runs on edges once; the higher-order products run on nodes. Readouts are
  linear except the last, to keep the body order
- **Two layers** (Figure 1, 3BPA): two-body models (NequIP, BOTNet) need up
  to five layers to converge; MACE with ν = 3 converges at two. The 3BPA
  molecule is about 9 Å across and the cutoff is 5 Å, so two layers already
  see the whole molecule
- **Learning curves** (Figure 2, aspirin, rMD17, force MAE): invariant MACE
  with ν = 1, 2, 3 has slopes −0.33, −0.51, −0.64. At ν = 3, raising L from
  0 to 1 to 2 leaves the slope at −0.64, −0.63, −0.64 and shifts the curve.
  At ν = 1, L = 1 and 2 steepen it to −0.44 and −0.45
- **rMD17** (Table 1, 950 training configurations): aspirin forces 6.6
  meV/Å against NequIP 8.2 and Allegro 7.3. Allegro is lower on six of the
  ten molecules' forces. With 50 training configurations MACE beats NequIP
  on all ten molecules' forces (aspirin 43.9 against 52.0)
- **3BPA extrapolation** (Table 2, RMSE, trained at 300 K): at 1200 K,
  forces 62.0 meV/Å for MACE L = 2, 76.2 for NequIP in its own code, 86.4 for
  NequIP in the MACE code, 83.0 for Allegro. Invariant MACE (L = 0) has
  latency 10.5 ms against 103.5 ms for NequIP in the MACE code, with force
  errors at or above the equivariant models' (300 K: 14.6 against
  10.8–13.0)
- **Acetylacetone** (Table 3): MACE has lower force error at 300 K and 600 K;
  NequIP has the lower energy error at 300 K (0.81 against 0.9 meV)

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It is `compared_against` NequIP ([LIT-tmpm07pb](LIT-tmpm07pb.md)), which it
benchmarks on rMD17, 3BPA and acetylacetone, re-implements in its own code
for timing, and re-reads. NequIP attributed its steeper learning curve to
equivariance; MACE's Figure 2 replicates the aspirin experiment and finds an
invariant model of higher body order steepens the curve as much, while
equivariance at fixed high body order only shifts it. [THEORY-tmpghjc1](../theory.d/THEORY-tmpghjc1.md) is that
finding stated as an explanation.

**The speed claim is measured in one codebase.** Every timing in Table 2 is
from the authors' `mace` code, with NequIP and BOTNet re-implemented there.
The paper says itself that "accurate speed comparisons between codes are
hard to obtain". The 30-minute training figure on 3BPA is against BOTNet
taking more than a day, on A100s.

**"State of the art" on rMD17 is shared.** MACE is best on aspirin,
paracetamol and toluene forces; Allegro is lower on most of the
others, and most entries are within a few tenths of a meV/Å.

Read — [NOTE-tmpbbjt7](../notes.d/NOTE-tmpbbjt7.md).
