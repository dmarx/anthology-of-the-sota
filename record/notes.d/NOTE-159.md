---
number: 159
status: Read
formerly:
- NOTE-tmpbfbli
paper: LIT-375
title: 'Accelerating Large Language Model Decoding with Speculative Sampling'
version: 1
date: '2026-09-16'
summary: >-
  The same construction as [NOTE-160](NOTE-160.md), reached independently two months
  later and demonstrated at 70B in a distributed setup. Its contribution to
  the record is corroboration plus two sharper statements: the guarantee holds
  "within hardware numerics" rather than absolutely, and the achieved tokens
  per second exceed the memory-bandwidth ceiling that bounds autoregressive
  decoding — which is the family's premise, measured rather than assumed.
---

# NOTE-159: Accelerating Large Language Model Decoding with Speculative Sampling

## Contribution

Speculative sampling: draft `K` tokens with a faster autoregressive model,
score them in one target call, accept a prefix under a modified rejection
sampling scheme that recovers the target's distribution. Benchmarked on
Chinchilla at 70B, distributed, for a 2-2.5x decoding speedup without
modifying the model or biasing the samples.

## Key insight

The latency of scoring a short continuation in parallel is comparable to the
latency of sampling one token — so the target call is nearly free to widen.
Everything then turns on an acceptance rule good enough to keep the
distribution and cheap enough to beat the drafting overhead.

## Assumptions

- Parallel scoring of `K` continuations costs about what scoring one does,
  which is the memory-bandwidth-bound regime.
- The draft exposes logits for the tokens it proposes.
- Draft and target share a tokenizer and vocabulary.
- The acceptance rate is high enough to offset drafting cost — the paper
  frames this as a break-even condition rather than a guarantee.

## Key results

- **Distribution preserved within hardware numerics.** The modified rejection
  sampling scheme recovers the target's distribution; the qualifier is the
  paper's own and is the honest version of "lossless".
  *Holds when:* the rule is applied per position with resampling on rejection.
- **2-2.5x speedup on Chinchilla 70B**, varying by evaluation domain, in a
  distributed serving setup.
  *Holds when:* that model, that hardware, those domains; no modification to
  the target.
- **Throughput exceeds the memory-bandwidth ceiling.** Mean tokens per second
  "often exceeds the idealised ceiling on auto-regressive sampling speed
  imposed by the memory bandwidth".
  *Holds when:* the ceiling is computed for single-token autoregressive
  decoding, which is what speculative sampling escapes.
- **At least one token per loop.** Reject the first draft token and a valid
  one is resampled in its place.
  *Holds when:* unconditionally.
- **Robust to the sampling knobs.** Nucleus, top-k and temperature are applied
  to the probabilities before rejection, and the acceptance rate is reported
  as robust to their exact values.
  *Holds when:* standard sampling configurations; reported as an observation
  rather than a swept result.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Speculative sampling preserves the target distribution within hardware numerics. | strong | Derivation of the modified rejection scheme; sample quality unchanged on benchmarks. |
| C2 | 2-2.5x decoding speedup on a 70B model in a distributed setup. | strong | Measured on Chinchilla across evaluation domains against the same model's autoregressive baseline. |
| C3 | The achieved tokens/second can exceed the memory-bandwidth ceiling on autoregressive sampling. | moderate | Reported comparison against an idealised ceiling; the ceiling is a computed quantity, not a measured baseline. |
| C4 | The acceptance rate is robust to nucleus, top-k and temperature settings. | weak | Stated as an observation; no sweep is reported. |

## Method

**Speculative Sampling (SpS).**

Given target `q` and draft `p` — note the paper's naming is the reverse of
[NOTE-160](NOTE-160.md)'s — draft `K` tokens, score all positions with the target in one
call, then accept left to right under the modified rejection rule, resampling
the first rejected position from the normalised positive part of the
difference.

- An autoregressive draft model, or a parallel one
- One batched target call per loop
- Modified rejection sampling with resample-on-reject
- Sampling knobs applied to probabilities before the rule

## Concepts

- **Modified rejection sampling** — the accept-reject construction that makes
  the composite sampler unbiased for the target.
- **Break-even acceptance rate** — the rate at which drafting overhead is
  exactly repaid. Below it speculation costs time; the paper's point is that
  real draft-target pairs sit well above it.
- **Idealised memory-bandwidth ceiling** — the tokens-per-second bound implied
  by streaming the weights once per token. The number this method is built to
  beat.

## Connections

**Related.**

- [LIT-376](../literature.d/LIT-376.md) — the same algorithm, two months earlier, independently. The
  pair is why the record can file this as more than one group's result.
- [LIT-185](../literature.d/LIT-185.md) (EAGLE-3) — a later draft architecture aimed at the low-cost end.

## Recommendations

- **R1** — Apply speculative sampling to an existing large model for
  latency-bound serving; no retraining, no architecture change, no change to
  sample quality.
  *Topic:* decoding latency · *Strength:* strong · *When:* Large target model,
  small batch, a cheaper model available with the same tokenizer.
- **R2** — Choose the draft on measured acceptance rate and latency, not on
  benchmark quality; any model exposing logits is admissible because the
  acceptance rule carries the guarantee.
  *Topic:* draft model selection · *Strength:* strong · *When:* Several drafts
  are available.
- **R3** — Keep the usual sampling configuration; apply nucleus, top-k and
  temperature to the probabilities before the rejection step.
  *Topic:* sampling configuration · *Strength:* moderate · *When:* Any
  non-greedy decoding.

## Bearing on the record

Corroborating source for [SOTA-227](../practices.d/SOTA-227.md). Two independent groups at two scales
is what moves that practice past `unreplicated`, and this paper supplies the
frontier-scale half.

## Limitations

- The distributional guarantee is exact in the mathematics and approximate in
  floating point, and the paper says so; a record that quotes "lossless"
  without the qualifier is quoting the first paper's phrasing, not this one's.
- The advantage is a latency result at serving batch sizes where arithmetic is
  idle. It is not a throughput result and the paper does not claim one.
- Chinchilla and 2023 infrastructure; nothing here interacts with paged
  attention or continuous batching, which the record holds separately.
- C4's robustness claim is an aside, not a measurement.

## Open questions

- Where is the batch size at which speculation stops paying, and does it move
  with paged attention?
- How does acceptance degrade as the draft and target diverge through
  post-training, when the draft is not retrained alongside?
