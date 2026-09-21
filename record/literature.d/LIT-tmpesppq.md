---
status: Active
title: 'Language Modeling by Language Models'
version: 1
tags:
- model-architecture
- in-context-learning
- analysis-and-evaluation
date: '2026-09-21'
published: '2025-06-25'
arxiv: '2506.20249'
first_author: 'Cheng'
keywords:
- 'automated-scientific-discovery'
- 'neural-architecture-search'
- 'genetic-programming'
- 'llm-agents'
- 'code-generation'
- 'ladder-of-scales'
implementations: []
summary: >-
  Cheng, Clark and Richardson (2025), [ARXIV-2506.20249](https://arxiv.org/abs/2506.20249). An LLM agent
  system that proposed, implemented and pretrained **1,062 verified** language-model
  block designs at 14M–350M parameters. The result that survives its own
  controls is the code generation: decomposing a long program into units and
  freezing each one that passes an execution-based checker takes valid-design
  rate from **6% to 92%**. The architecture-discovery headline does not
  survive as well — the five best designs average **0.6 points below** the
  five human seeds they were bred from.
---

<!-- inactive-ok-file: SOTA-tmpe69t0 — Proposed, filed in this same
     contribution; Standing names it as the one recommendation this paper
     supports, and the citation is that statement -->

# LIT-tmpesppq: Language Modeling by Language Models

Cheng, Clark and Richardson (2025) —
[ARXIV-2506.20249](https://arxiv.org/abs/2506.20249), read as [NOTE-tmpavng3](../notes.d/NOTE-tmpavng3.md).

## Key takeaways

- **The largest automated architecture-discovery experiment published:** 1,162
  designs proposed, 1,062 fully verified by pretraining, >1B tokens, 2.76M
  lines of generated code, 86K agent interactions, all artifacts public.
- **The load-bearing result is Table 4, and it is about code generation, not
  architecture.** On 100 held-out proposals, generating the program unit by
  unit with an execution-based checker at each step yields **92%** valid
  implementations. One-shot prompting with retries yields **6%**, and its
  outputs are trivial — about 49 lines of function body, "e.g. basic
  ConvNets", against 181 for the full system and 220 for the human reference
  library.
- **Within that, the checker is the bigger lever than the decomposition.**
  Removing the symbolic checker drops validity to **30%**; removing unit-based
  generation drops it to **73%** and halves code complexity. If you take one
  thing, take the checker.
- **The mechanism is stated and is not specific to architectures.** One-shot
  generation needs `E[calls] = 1/p` where `p` is the chance the whole artifact
  is valid, and `p` collapses as artifacts get complex. Generating
  `A = I₀ … I_N` and freezing each unit that passes turns one joint
  probability into a product of local ones — a Viterbi-style search, with the
  argument given from first principles in the appendix.
- **The architecture claim is true as worded and weaker than it sounds.**
  "Outperform GPT2, Mamba2, etc., on 6/9 common benchmarks" is a maximum taken
  over the five best of 1,062 designs against five seeds. Per-benchmark it
  checks out — 6 wins, 3 losses. On the average column the best discovered
  design beats the best seed by **0.03 points** (61.81 vs 61.78), and the five
  discovered designs average **60.17** against the seeds' **60.77**.
- **The nine evaluation benchmarks were chosen from statistics of the search
  itself.** Table 16 selects them from the verification pool by largest
  standard deviation across designs and by the best design beating random by
  more than 5%. The paper says so plainly. It also means the final comparison
  is not held out of the fitness function, which is defined as average
  downstream performance on exactly this kind of task.

## Standing in the anthology

Kept for the code-generation result, which is a clean internally-controlled
comparison of two strategies for getting a long, constrained artifact out of a
fixed model — and the record had nothing on it. `SOTA-tmpe69t0` is that
practice.

The architecture-discovery result is filed as context and not as a
recommendation. Nothing here says to run an automated architecture search, and
the paper does not claim it should: its own summary is "feasibility ... at
least at the functional level", and its discussion says no single model
dominated. The record's reading is that the margins are inside the
design-to-design spread the paper itself publishes — Table 16 gives a standard
deviation of 0.0138 on CoLA and SST2 across all verified designs, against
Table 5 margins of half a point to two and a half — which is a use of the
paper's own instrument on the paper's own headline, not a charge of
overclaiming.

**Worth recording in the paper's favour.** The abstract's precise number,
"~86 percentage point improvement", is exactly 92 − 6 and is described as
*percentage points*, which is the correct and less flattering framing of a
15× ratio. Table 16 is published, the selection standard is stated, and every
design artifact and training run is online. A paper that hands you the means
to check its weakest claim has done something most do not.
