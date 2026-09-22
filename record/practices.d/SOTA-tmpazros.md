---
status: Active
title: 'Enforce output structure by masking logits against a grammar, with masks precomputed per automaton state and built on the CPU while the GPU runs the forward pass'
version: 1
tags:
- inference-optimization
- systems-optimization
date: '2026-09-23'
source:
- LIT-tmpeekbd
introduced_by:
- LIT-tmpeekbd
consensus: emerging
consensus_note: >-
  Grammar-constrained decoding is widely offered by serving engines, through
  several libraries (Outlines, llama.cpp grammars, lm-format-enforcer,
  XGrammar). The specific design here, a per-node mask cache overlapped
  with the forward pass, comes from one group, which reports integrating
  it into major open-source engines. The record holds no independent
  measurement.
implementations:
- XGrammar
- SGLang
- MLC-LLM
summary: >-
  Dong et al. (2024), [LIT-tmpeekbd](../literature.d/LIT-tmpeekbd.md) — split the vocabulary by whether a
  token's validity depends only on the grammar automaton's current node
  (over 99% of tokens for JSON). Precompute those per node, check the rest
  against the full stack at runtime, and build each mask on the CPU during
  the GPU forward pass. Mask time is 0.018 ms per token after the ablated
  optimizations, and end-to-end overhead is 0.1–0.2 ms. It guarantees
  syntax. It does not measure whether answers stay correct.
---

# SOTA-tmpazros: Enforce output structure by masking logits against a grammar, with masks precomputed per automaton state and built on the CPU while the GPU runs the forward pass

## Source

Dong et al. (2024), [LIT-tmpeekbd](../literature.d/LIT-tmpeekbd.md) — XGrammar. Read as [NOTE-tmpkzvug](../notes.d/NOTE-tmpkzvug.md).

## The practice

**If downstream code parses the output, constrain decoding to the grammar,
and do not rely on prompting and retrying.** At each step, set the logits of
tokens that would violate the grammar to −∞ before sampling. Unconstrained,
Llama-3.1 8B produced valid function-call JSON 62% of the time and valid XML
80%. The failures were extra prose and wrong types. With the mask, both are
100% by construction.

**Make the mask cheap enough not to matter:**

- **Precompute per automaton node.** Most tokens' validity depends only on
  the current position in the current rule (the stack top), not on the whole
  parse stack. Cache those verdicts per node, stored as whichever of the
  accept or reject lists is smaller. Check only the context-dependent
  remainder (1,134 of 128k tokens for JSON) against the full stack
- **Build the mask on the CPU while the GPU computes logits**, and
  synchronize only before sampling. Build the per-grammar cache during
  prefill
- **Use a full context-free grammar when the structure nests.** Regex
  engines cannot express arbitrarily nested JSON

| optimization (cumulative) | mask latency per token |
|---|--:|
| PDA over the full vocabulary | 65.8 ms |
| + node merging | 38.3 ms |
| + per-node mask cache | 0.154 ms |
| + rule inlining | 0.035 ms |
| + context expansion | 0.018 ms |

End to end on Llama-3.1 8B (MLC-LLM), TPOT goes from 6.2 to 6.3 ms at
batch 1 and from 9.0 to 9.2 ms at batch 16.

## Conditions

- **It guarantees syntax, not correctness.** The paper's "accuracy" is
  syntactic validity. Masking tokens and renormalizing the rest can
  change the distribution the model samples from, and whether task accuracy holds
  up under the constraint is not measured here. Check the end task
  ([SOTA-308](SOTA-308.md) makes the same point for retrieval)
- **A spare CPU core per stream**, for the overlap to hide the cost
- **Measured on one model family** against library versions from late
  2024

## Known implementations

- XGrammar (as a library), used as the backend in SGLang and MLC-LLM
