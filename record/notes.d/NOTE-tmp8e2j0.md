---
status: Read
paper: LIT-tmp85dyu
title: 'Comment on the Illusion of Thinking'
version: 1
date: '2026-09-21'
summary: >-
  Argues the reported collapse is evaluation design. Reading it: the
  unsolvable-instance claim is a checkable fact and lands; the rest is a
  reinterpretation of a measurement the two papers agree on, from a preprint
  that is underpowered and has already been corrected once.
---

# NOTE-tmp8e2j0: Comment on the Illusion of Thinking

## Contribution

Takes a widely-read result about the limits of reasoning models and asks
whether the evaluation could produce that result without the limit being
real. It finds three ways it could, one of which is a plain error in the
benchmark rather than a matter of interpretation.

## Key insight

"The question isn't whether LRMs can reason, but whether our evaluations can
distinguish reasoning from typing." Tower of Hanoi requires exponentially
many moves and a trivial decision at each one. An evaluation that demands the
moves be enumerated is, past some size, measuring willingness to produce
output. The capability and the transcript come apart, and the scorer only
sees the transcript.

## Assumptions

- **That the models' stated reasons for stopping are their real reasons.**
  The quoted "to avoid making this too long" is taken at face value as
  evidence of a decision rather than a post-hoc rationalization.
- **That solving Tower of Hanoi by emitting a Lua generating function
  demonstrates the same capability** the enumeration was meant to test. This
  is the load-bearing move of §5 and it is arguable: generating the recursive
  algorithm is a different task from executing it.
- **10 tokens per move**, verified against the OpenAI tokenizer, for the
  length arithmetic.

## Key results

- **River Crossing includes unsolvable instances.** Missionaries–Cannibals
  variants have no solution for more than five pairs with boat capacity
  three. [LIT-tmpzsiks](../literature.d/LIT-tmpzsiks.md) tests such instances and scores zero for
  them. *Holds when:* always — it is a published combinatorial fact, not a
  measurement.
- **The collapse happens below the token limit, and both papers say so.**
  §4's arithmetic gives maximum solvable sizes above where collapse is
  reported. The comment's own conclusion from this is that models terminate
  early and "may be poorly calibrated about their own context length
  capabilities". [LIT-tmpzsiks](../literature.d/LIT-tmpzsiks.md) reports the same fact — models are
  "well below their generation length limits" — and reads it as a scaling
  limitation of thinking. **The disagreement is about what the shared
  observation means, not about the observation.**
- **Representation change restores performance** — asking for a Lua function
  that prints the Tower of Hanoi solution for 15 disks gives high accuracy
  across Claude 3.7 Sonnet, Claude Opus 4, o3 and Gemini 2.5, under 5,000
  tokens. *Holds when:* unclear — the author states budget prevented enough
  trials for a powered sample and calls full validation future work.
- **Solution length is not difficulty** — Hanoi is `2^n − 1` moves with a
  trivial branching factor; Blocks World is shorter and NP-hard to optimize.
  And the Blocks World prompt demands the minimum sequence while the checker
  accepts any valid one, so a compliant model attempts the harder variant.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Some River Crossing instances tested are unsolvable and were scored as failures | strong | a mathematical fact about the puzzle family, independently checkable |
| C2 | Apparent collapse partly reflects output-length decisions rather than reasoning failure | moderate | quoted model behaviour plus token arithmetic; the interpretation is the contested part, not the arithmetic |
| C3 | Models retain the algorithm when asked for a compact representation | weak | explicitly preliminary, underpowered by the author's own statement |
| C4 | Solution length is a poor complexity metric | strong | follows from the puzzles' known complexity |
| C5 | Blocks World scoring and prompting are mismatched | moderate | reading of the published prompt against the published checker |

## Concepts

- **Reasoning versus typing** — the distinction the paper is built on:
  whether an evaluation separates knowing a procedure from emitting its
  output.
- **Programmatic evaluation hazard** — a scorer that cannot represent
  "correctly declined" or "impossible" collapses them into "wrong".

## Connections

A direct comment on [LIT-tmpzsiks](../literature.d/LIT-tmpzsiks.md), declared as `corrects`. The
general form of its argument — that evaluation demands unrelated to the
capacity depress measured performance — is [LIT-tmpmftfr](../literature.d/LIT-tmpmftfr.md), which is a
systematic study rather than a dispute, and which this does not cite.

## Bearing on the record

- **It supplies the worked example for [SOTA-tmpwqjj5](../practices.d/SOTA-tmpwqjj5.md)**, and a good
  one, because the three failure modes it names — an output cap, a scorer
  that cannot express refusal, and instances with no solution — are things a
  reader can check in their own evaluation this afternoon.
- **It does not license treating [LIT-tmpzsiks](../literature.d/LIT-tmpzsiks.md) as debunked.** That
  paper is NeurIPS 2025, camera-ready, revised five months after this comment
  appeared. Its three-regime result is untouched by anything here.
- **`corrects` is declared for what the document is, not for who won.**

## Limitations

The record should hold these as prominently as the argument.

- **Single-author preprint**, not peer-reviewed. The author states that
  Claude Opus wrote the bulk of it and was removed as co-author under arXiv
  policy.
- **The central experiment is underpowered by the author's own admission.**
- **It has already been corrected once in public.** §4 replaces an earlier
  version's assumption that the evaluation required intermediate states;
  commenters showed models jump to the final move list. The author notes the
  irony that the mistaken assumption came from a human reviewer of the draft.
- **Its own bibliography miscites the paper it comments on**, giving
  `ARXIV-2501.12948` — DeepSeek-R1 — for Shojaee et al. The arXiv metadata
  names the right target, so this is a reference-list error rather than a
  confusion about what is being commented on. Small, and worth recording
  beside an argument that turns on care in checking things.
- **C1 is the only claim that does not depend on interpreting model
  behaviour**, and the paper's rhetorical weight is spread evenly across all
  of them.

## Open questions

- How much does the collapse threshold move once unsolvable instances are
  dropped? Neither paper says.
- Does the generating-function result hold in a powered study?
- Is emitting a correct recursive algorithm the same capability as executing
  it? The comment assumes so; that assumption is exactly what
  [LIT-tmpci13h](../literature.d/LIT-tmpci13h.md) suggests might be false, since a task can be easy to
  express and hard to carry out within a fixed depth.
