---
status: Proposed
promote_when: >-
  The same comparison run on a different kind of artifact, by a group that is
  not selling the scaffold: one model, one budget, generating long constrained
  outputs both unit-by-unit-with-freezing and one-shot-with-retry, with
  validity judged by a checker written before either arm ran, and token cost
  reported for both. What would not meet it: a system paper reporting a high
  validity rate for its own agent loop with no one-shot arm. That is the
  common shape, it is what every such paper can report, and it says nothing
  about the decomposition.
consensus: unreplicated
consensus_note: >-
  One group, one artifact type, one checker. The general shape — decompose,
  check, retry locally — is widely used in agentic coding systems and is close
  to folklore; what is unreplicated is anybody measuring it against the
  one-shot alternative under a fixed budget, which is the comparison that
  makes it a recommendation rather than a habit.
title: 'Generate a long program unit by unit, freezing each unit that passes an execution-based check, instead of regenerating the whole artifact on failure'
version: 1
tags:
- in-context-learning
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-tmpesppq
introduced_by:
- LIT-tmpesppq
implementations: []
summary: >-
  Cheng, Clark and Richardson (2025), [LIT-tmpesppq](../literature.d/LIT-tmpesppq.md) — on 100 held-out
  proposals, the same model produced valid implementations **92%** of the time
  generating unit by unit against an execution-based checker, and **6%** of
  the time one-shot with retries; the one-shot outputs were also trivial, 49
  lines against 181. Removing the checker alone costs 62 points, removing the
  decomposition alone costs 19 — so if you build one, build the checker.
---

# SOTA-tmpe69t0: Generate a long program unit by unit, freezing each unit that passes an execution-based check, instead of regenerating the whole artifact on failure

## Source

Cheng, Clark and Richardson (2025),
[LIT-tmpesppq](../literature.d/LIT-tmpesppq.md) — read as [NOTE-tmpavng3](../notes.d/NOTE-tmpavng3.md).

## When this applies

You need a fixed model to produce a long artifact that must satisfy hard
constraints — a module conforming to an interface, a program that must compile
and run, a configuration that must validate. Two conditions: the artifact
decomposes into pieces that can be checked before the whole exists, and a
cheap automatic check exists for a piece. Without the second there is nothing
to freeze against, and the practice has no content.

## Do this

1. **Fix an interface the pieces must satisfy**, so that a partial artifact is
   a checkable object rather than a fragment. The source's is a PyTorch module
   contract of type `(X, Z) → (X, Z)`; the point is that any unit, on its own,
   can be initialized and run.
2. **Generate one unit at a time.** Let the generator declare children it
   needs and leave them as placeholders; take them off the queue in turn.
3. **Check each unit as it lands**, with execution and not only with a parser.
   The source's checker runs AST validation, interface conformance,
   initialization, a forward pass, a backward pass, a causality check, a
   differentiability-and-unused-parameter check, and a short training run for
   gradient stability and FLOPs.
4. **Freeze what passes; revert only what failed.** A failure costs one unit's
   retry, not the artifact's.

## What it buys

On 100 held-out proposals, the same model producing the same artifacts:

| configuration | valid | function-body lines |
|---|---|---|
| full loop | **92%** | 181 |
| without the checker | **30%** | 167 |
| without unit-by-unit generation | 73% | 75 |
| one-shot prompting with retries | **6%** | 49 |

For scale, the human-written reference library averages 220 lines. One-shot
prompting does not merely fail more often; when it succeeds it produces
something trivial — the source's example is "basic ConvNets".

**If you build only one of the two, build the checker.** Removing it costs 62
points of validity against the 19 that removing the decomposition costs. The
ordering is worth stating because the decomposition is the interesting idea
and the checker is the boring one.

## Why it works

One-shot generation with retries needs `E[calls] = 1/p`, where `p` is the
probability that the entire artifact is simultaneously valid. That `p` falls
off a cliff as artifacts get long, and no amount of retrying changes the
exponent. Generating `A = I₀ … I_N` and committing each unit that passes turns
one joint probability into a product of local ones, each paid for separately —
a Viterbi-style search, which the source argues from first principles reduces
expected calls and billable tokens exponentially in the number of units.

Nothing in that argument mentions neural architectures. It is a claim about
generating constrained artifacts under a checker, and the recommendation is
stated at that level deliberately.

## Conditions

**One group, one artifact type, one checker.** Every number above comes from a
single system generating one kind of object. The mechanism is general and the
measurement is not.

**The independence assumption is doing work in the proof and is not tested.**
The exponential result assumes per-unit success is i.i.d. Generated-code
failures are plausibly correlated — one bad plan makes several units wrong
together — and the source does not treat that case. Expect the empirical
advantage to be smaller than the bound.

**Part of the 92% is the interface, not the loop.** A well-specified module
contract is itself a heavy constraint on what the model can write, and no arm
of the ablation removes it. How much of the gap is the contract and how much
is the unit-wise procedure is not separated.

**It costs about 50× the tokens per artifact.** The source reports this in the
same table as the win, which is the right place for it. At 92% versus 6% the
trade is favourable per *valid* artifact, but if a cheap generator already
clears your bar, this buys you nothing and charges you for it.

**Two components in the loop did almost nothing.** Removing the planner (91%)
or the observer agent (89%) barely moved validity. The source argues they
matter qualitatively; on the measured quantity they did not. An agent count is
not the mechanism here.

## What this is not

**It is not a recommendation about automated architecture discovery.** The
source's headline is that its discovered designs are competitive with GPT2 and
Mamba2 on 6 of 9 benchmarks, and that claim is a maximum over the five best of
1,062 designs on tasks selected from the search's own statistics — on the
average column the five discovered designs land **below** the five human seeds
they were bred from. The record files the code generation and not the
discovery, and [LIT-tmpesppq](../literature.d/LIT-tmpesppq.md) says why at length.
