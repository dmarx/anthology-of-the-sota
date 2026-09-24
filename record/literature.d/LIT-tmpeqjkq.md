---
status: Active
title: 'ResiDual: Transformer with Dual Residual Connections'
version: 1
tags:
- model-stability
- model-architecture
- analysis-and-evaluation
date: '2026-09-24'
published: '2023-04-01'
arxiv: '2304.14802'
first_author: 'Xie'
keywords:
- 'pre-ln'
- 'post-ln'
- 'representation-collapse'
- 'gradient-vanishing'
- 'residual-connections'
implementations: []
extends:
- LIT-114
summary: >-
  Xie et al. (2023), [ARXIV-2304.14802](https://arxiv.org/abs/2304.14802). Gives the representation-collapse
  argument a **rate**: in a Pre-LN transformer the per-layer change in the
  normalised hidden state decays as `O(1/√k)`, and adding a layer to an `N−1`
  layer model moves the output by `O(1/√N)`. Also measures what Pre-LN's
  no-warmup claim costs — **32.28 against 35.12 BLEU** at E6D6, and 31.82
  against 35.18 at E12D12.
---
<!-- inactive-ok-file: THEORY-tmpt3lzt — Proposed, filed in this same contribution as the account under SOTA-032's cost. The practice declares explained_by on it, so the citation is the relation itself; the practice stands without the account and the account is the weaker of the two, which is why their statuses differ -->

# LIT-tmpeqjkq: ResiDual: Transformer with Dual Residual Connections

Xie, Zhou, Gu, He, Lin, Liu, Qin and colleagues (2023) — [ARXIV-2304.14802](https://arxiv.org/abs/2304.14802)

## Key takeaways

- **The collapse argument gets a rate, which is the reason to hold this.**
  Theorem 3.3: assuming block outputs `xᶠ_k ~ N(0, σ²I)` independently, the
  change in the normalised hidden state between consecutive Pre-LN blocks is
  `xˡⁿ_{k+1} − xˡⁿ_k ~ N(0, ω_k² I)` with

      ω_k² = 2 / (√k (√(k−1) + √k))

  Corollary 3.4: `E[|(xˡⁿ_{k+1} − xˡⁿ_k)ᵢ|] ~ O(1/√k)`. Corollary 3.5: adding
  a block to an `N−1` block Pre-LN transformer changes the output by
  `O(1/√N)` per coordinate. **"Adding [an] extra layer in the deep Pre-LN
  Transformer has little impact on the output."**

- **The observation is not theirs and they say so.** *"The issue with the
  representation capability of Pre-LN was initially observed by Liu et al.
  2020"* — who showed the ratio `√Var[xᶠ_k] / √Var[xᵃ_k + xᶠ_k]` shrinks for
  higher blocks. This paper's contribution is the *convergence rate*, via "a
  novel analysis approach that directly examines the distribution of hidden
  state changes." **The record holds neither Liu et al. nor this**, and has
  been making the argument in prose.

- **The two defects are symmetric and both are about where the normalisation
  sits.** In Post-LN, `xᶠ_k` is normalised `N−k` times and so are its
  gradients, which is why gradient norm decays exponentially from deep layers
  to shallow ones — Xiong et al.'s result, `LIT-114`, restated here as the
  motivation for the other half. In Pre-LN, `y = LN(Σₖ xᶠ_k)`, so each block
  output is normalised exactly once and nothing is blocked in either
  direction — and the price is that the sum stops moving.

- **What Pre-LN's no-warmup claim costs, measured.** IWSLT BLEU:

  | method | warm-up | E6D6 | E12D12 |
  | --- | --- | --: | --: |
  | Post-LN | yes | 35.37 | **fail** |
  | Post-LN | no | fail | fail |
  | Pre-LN | yes | 35.12 | 35.18 |
  | Pre-LN | **no** | **32.28** | **31.82** |
  | ResiDual | yes | 35.63 | 36.09 |
  | ResiDual | no | 35.76 | 35.57 |

  **Pre-LN without warm-up loses 2.84 BLEU at E6D6 and 3.36 at E12D12.** It
  trains, which is Xiong et al.'s claim, and it is meaningfully worse, which
  is not in Xiong et al.

- **Their prose is looser than their own table.** The text says *"Pre-LN and
  our method can train effectively without it"* — with a three-point drop in
  the row above. Anyone citing the sentence rather than the table carries
  Xiong et al.'s claim forward unqualified. The ResiDual rows are the ones
  that earn that phrasing: 35.76 without warm-up against 35.63 with it, at
  E6D6.

- **Post-LN does not merely need warm-up, it stops working.** E12D12 fails
  *with* warm-up. The depth at which the two architectures diverge is lower
  than the usual framing suggests.

- **The method, for completeness.** Two residual streams — one Pre-LN-like to
  avoid gradient vanishing, one Post-LN-like to avoid collapse — summed at
  the output. Filed here for the analysis rather than the architecture.

## Standing in the anthology

Unit 4 of `#326`, reversed from `#290`'s `D-variant` declines. The paper *is*
an architecture variant, so the decline was not a heading leak this time — it
was the rule itself: **the variant is the contribution and the analysis is
what the record needed.**

`SOTA-032` recommends Pre-LN, is `Active`, and already carries the collapse
argument in its own prose: *"deep pre-norm models can see later blocks
contributing proportionally less — the representation collapse argument."*
**With no citation.** Nineteen files in this record discuss Pre-LN and ten
discuss Post-LN; the cost of the recommended choice was stated everywhere and
sourced nowhere.

Two things follow, both applied in this contribution. The argument gets a
source and a rate (`THEORY-tmpt3lzt`). And `SOTA-032`'s stated headline
consequence — that Pre-LN makes warm-up removable — gets the measurement it
did not have, which does not overturn it and does put a number on it.

`extends: LIT-114` — it builds directly on Xiong et al.'s gradient result,
restating it as the Post-LN half of a two-sided problem.
