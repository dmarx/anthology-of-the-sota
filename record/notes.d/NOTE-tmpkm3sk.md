---
status: Read
paper: LIT-tmptlzmx
title: 'Fast Inference from Transformers via Speculative Decoding'
version: 1
date: '2026-09-16'
summary: >-
  Autoregressive decoding is serial and memory-bandwidth-bound, so the
  arithmetic units sit idle while weights stream. Speculative decoding spends
  that idle compute: a cheap draft proposes `gamma` tokens, the target scores
  all `gamma + 1` positions in one parallel pass, and an accept-reject rule
  keeps a prefix. The rule is constructed so the output distribution is
  exactly the target's, which is what makes this a free speedup rather than a
  quality trade.
---

<!-- inactive-ok-file: ADR-041 — Proposed, which is the resting state of
     most of this record's decisions, and cited here as the rule under
     which R2 and R3 stay in the reading rather than becoming practices. -->

# NOTE-tmpkm3sk: Fast Inference from Transformers via Speculative Decoding

## Contribution

An algorithm for sampling from a large autoregressive model faster, with the
sampled distribution unchanged and no retraining or architecture change. The
reported result is a 2x-3x walltime improvement on T5-XXL against a
production implementation, with identical outputs.

## Key insight

Decoding `K` tokens takes `K` serial model runs, and each run is limited by
streaming the weights rather than by arithmetic — so there is compute
available that the serial structure cannot use. A draft model turns that
spare compute into parallelism by *guessing*, and a rejection rule turns the
guesses into an unbiased sample.

## Assumptions

- Enough compute to run `gamma + 1` evaluations of the target concurrently
  without increasing walltime. The paper states this as a condition, not an
  incidental.
- Decoding is memory-bandwidth-bound rather than arithmetic-bound in the
  operating regime — true at small batch, progressively false as batch grows.
- The draft model's per-run cost `c` relative to the target is small enough
  that `gamma*c` does not eat the gain.
- The acceptance rates at successive positions are treated as i.i.d. for the
  expectation derivations; the paper flags this as a simplifying assumption.
- The draft exposes a probability for each token it proposes.

## Key results

- **Exact distribution preservation.** The accept-reject construction yields a
  sample distributed as the target model's.
  *Holds when:* draft and target define distributions over the same
  vocabulary; the rule is applied per position with the adjusted resample on
  rejection.
- **Acceptance rate in closed form.** `alpha = E(min(p, q)) = 1 - E(D_LK(p,q))`
  for the paper's divergence `D_LK`.
  *Holds when:* expectation over the prefix distribution.
- **Expected tokens per loop** `= (1 - alpha^(gamma+1)) / (1 - alpha)` — a
  capped geometric variable with success probability `1 - alpha` and cap
  `gamma + 1`.
  *Holds when:* the i.i.d. simplification above.
- **Expected walltime improvement** `= (1 - alpha^(gamma+1)) / ((1 - alpha)(gamma*c + 1))`,
  maximised over integer `gamma` numerically. For `c ≈ 0` the bound is
  `1/(1 - alpha)`.
  *Holds when:* the concurrency assumption; a fixed `gamma` per loop.
- **Never worse in serial target runs.** Every parallel target run emits at
  least one token, so the count cannot exceed plain decoding's.
  *Holds when:* unconditionally, by construction.
- **2x-3x measured**, T5-XXL 11B against the T5X implementation, outputs
  identical.
  *Holds when:* translation and summarization; TPU; that implementation as
  baseline.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The sampled distribution is exactly the target model's. | strong | Constructive proof of the accept-reject rule; the empirical results are reported against identical outputs. |
| C2 | Walltime improves 2x-3x on a production 11B model with no retraining. | strong | Measured against T5X on translation and summarization with T5-XXL. |
| C3 | Draft quality is measurable in advance as `alpha = E(min(p, q))`, and the optimal `gamma` follows from `alpha` and `c`. | moderate | Derived under an i.i.d. acceptance assumption; verified against measured `alpha` in the experiments. |
| C4 | The method can never increase the number of serial target evaluations. | strong | Structural: each loop emits at least one token. |

## Method

**Speculative decoding.**

Per loop: sample `gamma` tokens from the draft autoregressively; evaluate the
target on all `gamma + 1` prefixes in one batched call; for each position draw
`r_i ~ U(0,1)` and accept while `r_i <= p_i(x)/q_i(x)`; at the first rejection
resample that position from the normalised positive part of `p - q` and stop;
if nothing was rejected, take the free extra token from the target's
distribution at position `gamma + 1`.

- A draft model cheaper than the target by a factor `1/c`
- One batched target evaluation per loop over `gamma + 1` positions
- Per-position accept-reject with an adjusted resample
- `gamma` chosen numerically from `alpha` and `c`

## Concepts

- **Acceptance rate `alpha`** — how often a draft token survives the rule;
  equals `E(min(p, q))`, so it measures agreement between the two
  distributions rather than draft quality in the abstract.
- **Cost coefficient `c`** — draft time per run over target time per run. With
  `alpha`, the only two numbers the walltime formula needs.
- **Negligible-cost draft** — `c ≈ 0`, where the improvement approaches
  `1/(1 - alpha)`. The regime every later self-drafting method aims at.
- **Speculative execution** — the borrowed idea: do work that is probably
  needed before knowing that it is, and discard it if wrong.

## Connections

**Related.**

- [LIT-185](../literature.d/LIT-185.md) (EAGLE-3) — a later method for making the draft nearly free, which
  is this paper's `c ≈ 0` regime approached by architecture.
- [LIT-163](../literature.d/LIT-163.md) (multi-token prediction) — trains heads that can serve as the draft,
  removing the separate model.

## Recommendations

- **R1** — Use speculative decoding for latency-bound autoregressive serving;
  it changes nothing about the output distribution and needs no retraining.
  *Topic:* decoding latency · *Strength:* strong · *When:* Memory-bandwidth-bound
  decoding with spare arithmetic capacity — small batch, large model.
- **R2** — Choose `gamma` by maximising `(1 - alpha^(gamma+1)) / ((1 - alpha)(gamma*c + 1))`
  numerically, rather than fixing it by habit.
  *Topic:* speculation depth · *Strength:* moderate · *When:* `alpha` has been
  measured for the draft-target pair on representative prompts.
- **R3** — Select a draft by measured `alpha` and `c` together, not by size or
  benchmark score.
  *Topic:* draft model selection · *Strength:* moderate · *When:* Several
  candidate drafts are available.

## Bearing on the record

The practice the record was missing while holding two of its refinements.
[SOTA-tmp6mgiw](../practices.d/SOTA-tmp6mgiw.md) is filed from this and [LIT-tmphbbt7](../literature.d/LIT-tmphbbt7.md); R2 and R3 stay here as
algorithm-local settings under [ADR-041](../decisions.d/ADR-041.md).

## Limitations

- The concurrency assumption is load-bearing and is exactly what fails at high
  batch: once the arithmetic units are saturated by other sequences, the
  speculative work competes rather than filling a gap.
- The i.i.d. treatment of acceptance across positions is a simplification;
  acceptance is plainly correlated within a phrase.
- A fixed `gamma` per loop leaves something on the table — the paper estimates
  up to ~60% more improvement from adapting it, and does not pursue it.
- 2022 models and hardware: T5-XXL, LaMDA, TPU. No result here is on a modern
  decoder-only serving stack with paged attention and continuous batching.

## Open questions

- How should `gamma` adapt within a generation, given that acceptance varies
  sharply between easy and hard spans?
- How does the gain interact with batching and KV-cache paging, which are the
  other two things a serving stack does to the same bottleneck?
