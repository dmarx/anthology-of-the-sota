---
status: Read
paper: LIT-tmpeekbd
title: 'XGrammar'
version: 1
date: '2026-09-23'
summary: >-
  Grammar-constrained decoding made nearly free. It splits the vocabulary
  into tokens whose validity depends only on the automaton's stack top,
  which are precomputed, and the under-1% that need the full stack, which
  are checked at runtime. The mask is built on the CPU during the forward
  pass. Each optimization is ablated. Output quality is measured only as
  syntactic validity. Read §1–6; the appendix was not read.
---

# NOTE-tmpkzvug: XGrammar

## Contribution

A constrained-decoding engine for full context-free grammars (not only
regular expressions) whose per-token cost is small enough to hide behind
the model's forward pass. The idea that makes this possible is splitting
tokens by what part of the parser state decides them.

## Key insight

**Validity usually depends only on where you are in the current rule.** A
pushdown automaton's full stack is unbounded, but a token that does not
return to a parent rule is decided by the stack top alone, which is one of
finitely many nodes. So almost the whole mask is a lookup, and the stack is
consulted only for the few tokens that could close a rule.

## Assumptions

- **A byte-level pushdown automaton** built from the grammar, handling
  tokens that split UTF-8 characters or grammar elements
- **A CPU core free** to build masks while the GPU decodes
- **Llama-3.1 (128k vocabulary)**, JSON, JSON Schema, XML and a Python
  DSL; H100 for the end-to-end numbers

## Key results

- **Table 3:** 65.8 ms → 0.018 ms per-token mask latency, most of it from
  the adaptive mask cache (248.6×)
- **Figure 9 (µs/token):** JSON Schema 36 against 125 / 7,069 / 6,147
  (Outlines, llama.cpp, lm-format-enforcer in legend order). For the CFG
  panels only two comparators are plotted, and the extracted text does not
  say which: unconstrained JSON 36 against 4,711 and 9,353, XML 52 against
  382,126 and 18,231, Python DSL 191 against 427,285 and 42,577
- **Figure 10:** end-to-end with SGLang and XGrammar, time per output token
  stays near 6–12 ms from batch 1 to 32, where llama.cpp and vLLM with
  Outlines climb to hundreds of milliseconds or time out
- **Table 2:** enabling XGrammar in MLC-LLM adds 0.0–0.2 ms per token
- **Table 4:** syntactic correctness 62% → 100% (function calling), 80% →
  100% (XML)

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Precomputing context-independent token verdicts removes nearly all mask cost | strong | Table 3 ablation |
| C2 | Overlapping mask generation with the forward pass makes structured generation near-zero overhead | strong | Table 2 |
| C3 | XGrammar is much faster than earlier engines | moderate | Figure 9, one model, the authors' own benchmark |
| C4 | Constrained decoding improves generation quality | weak | only syntactic validity is measured, and that is guaranteed by construction |

## Concepts

- **Context-independent token** — one whose validity is fixed by the stack
  top node
- **Context expansion** — precomputing, for each rule, what may follow its
  end in parent rules, to reject more tokens early
- **Persistent execution stack** — a tree of stacks sharing prefixes, so
  branching and rollback are constant-time

## Connections

It follows Outlines (regular expressions and lexer-level caching),
llama.cpp's grammar (full-vocabulary PDA checks) and SynCode (offline
lexer caches). It is complementary to front-ends such as SGLang, Guidance
and LMQL, and serves as their backend. Rollback support makes it compatible
with speculative decoding ([SOTA-227](../practices.d/SOTA-227.md)) and jump-forward decoding.

## Recommendations

- **R1** — Enforce structure with a grammar mask, not by retrying or
  post-hoc parsing, and use an engine that precomputes per-state masks and
  overlaps them with the forward pass. Filed as [SOTA-tmpazros](../practices.d/SOTA-tmpazros.md)

## Bearing on the record

- **[SOTA-tmpazros](../practices.d/SOTA-tmpazros.md)** is new. The record had no constrained-decoding practice
- **[SOTA-227](../practices.d/SOTA-227.md)** (speculative decoding): the persistent stack's rollback is
  what lets a grammar mask coexist with draft-and-verify

## Limitations

- **No semantic evaluation.** Nothing measures whether task accuracy moves
  under the constraint, in either direction
- **One model family** for the end-to-end numbers
- **The baselines are other libraries at particular versions.** The
  comparison dates quickly as they improve

## Open questions

- How much greedy masking distorts the model's distribution over valid
  outputs, and whether that matters on real tasks
