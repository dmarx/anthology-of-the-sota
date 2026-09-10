---
number: 16
status: Read
formerly:
- NOTE-tmpkkuh5
paper: LIT-024
title: 'Fast Transformer Decoding: multi-query attention'
version: 1
tags:
- attention-techniques
date: '2026-09-09'
published: '2019-11-01'
summary: >-
  Incremental decoding is bounded by the memory bandwidth of reloading the keys and values, not by arithmetic. Share one key/value head across all query heads: much faster decoding, "only minor quality degradation".
---

# NOTE-016: Fast Transformer Decoding: multi-query attention

## Contribution

Training a Transformer parallelises across sequence positions; **incremental
decoding cannot**, and the paper identifies what actually limits it — the
memory bandwidth of repeatedly reloading the large keys and values tensors
that hold the attention layers' state. The fix proposed is one line of
architecture: share the keys and values across all attention heads, keeping
the queries separate. The tensors shrink by the head count, and so does the
bandwidth requirement.

## Key insight

An operation's cost is set by whichever resource it exhausts, and for
autoregressive decoding that resource is bandwidth rather than FLOPs. Every
step reads the whole KV cache to produce one token per sequence — so the
arithmetic intensity is terrible and the cache size *is* the step time.

The architectural consequence is that the K and V projections are the
expensive part of multi-head attention at inference, and they are also the
part with the most redundancy: whether every head genuinely needs its own view
of the keys is an empirical question nobody had asked. The answer is mostly
no, at a small cost.

## Assumptions

- **Incremental (autoregressive) decoding** is the regime. Nothing here helps
  training or a parallel forward pass, where the same tensors are read once
  for many positions.
- Modern accelerators, where bandwidth is the scarce resource relative to
  arithmetic — the premise of the whole analysis.
- The quality claim is **"only minor quality degradation"**, reported
  qualitatively rather than bounded.
- 2019 models and scales.

## Key results

- **The diagnosis**: incremental Transformer inference speed "is limited by
  the memory bandwidth necessary to reload the large keys and values tensors
  which encode the state of the attention layers".
- **Multi-query attention**: keys and values shared across all heads, queries
  kept per-head. The KV tensors shrink by a factor of the head count.
- **Much faster to decode**, with **only minor quality degradation** from the
  multi-head baseline.
- The paper includes a performance analysis deriving the bandwidth bound
  before proposing the variant — the diagnosis is load-bearing, not framing.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Incremental decoding is memory-bandwidth bound, not compute bound | strong | the performance analysis, and the fact that shrinking the tensors is what buys the speed |
| C2 | Keys and values can be shared across heads | strong | the architecture works |
| C3 | The quality cost is minor | moderate | asserted and measured at 2019 scale; "minor" is not quantified as a bound |
| C4 | Decoding is much faster as a result | strong | measured |

## Method

**Architecture:** multi-query attention.

In a multi-head attention layer, project queries per head as usual, but
project **one** set of keys and values shared by every head. At decode time
the cache holds a single K and V per layer instead of one per head.

## Concepts

- **Multi-query attention** — `h` query heads, one key head, one value head.
- **Incremental inference** — generating one token at a time, where the
  sequence-length parallelism that makes training fast is unavailable by
  construction.
- **The KV cache as the state** — the paper's framing: keys and values
  "encode the state of the attention layers", which is why their size sets
  the decode cost.

## Connections

Follows Vaswani et al.'s multi-head attention directly, as a variation on it.
Its successor in this record is **GQA**, which interpolates: `g` key/value
groups rather than one, recovering most of the quality at most of the
bandwidth saving. Its diagnosis — that the bottleneck is bandwidth, not
arithmetic — is the same one FlashAttention makes at the kernel level and
vLLM makes at the memory-management level, three papers finding the same
thing at three altitudes.

## Recommendations

- **R1** — Count bandwidth, not FLOPs, when reasoning about decode cost.
  *Topic:* inference. *Status:* standard. *Strength:* strong. *Applies when:*
  any autoregressive serving decision.
- **R2** — Reduce the KV cache by sharing key/value heads. *Topic:*
  architecture. *Status:* standard. *Strength:* strong. *Applies when:*
  decoding throughput matters — though see the successor, which does this
  better.
- **R3** — Decide the KV head count at design time. *Topic:* architecture.
  *Status:* standard. *Strength:* moderate. *Applies when:* it is a
  pretraining decision and expensive to revisit.

## Bearing on the record

**Both practices sourced to this note are confirmed**, and both were already
`Superseded` before the reading — by GQA, which is the right disposition and
is unaffected.

<!-- inactive-ok-block: SOTA-023, SOTA-024 — both Superseded by GQA before this reading; confirmed against the source, and the status is unchanged -->
| practice | disposition |
|---|---|
| [SOTA-023](../practices.d/SOTA-023.md) use MQA to reduce memory bandwidth | confirmed — C1 and C4; `Superseded` stands |
| [SOTA-024](../practices.d/SOTA-024.md) share K/V across heads, keep queries separate | confirmed — C2, the architecture verbatim; `Superseded` stands |

Worth recording that a `Superseded` practice can still be checked and can
still be right. The two schemes are allowed to disagree ([ADR-002](../decisions.d/ADR-002.md)) and this is
the benign version: the paper is sound, the practice accurately reported it,
and something better arrived. Nothing needed changing, which is itself a
result — three of the four failure modes this issue has found would have been
invisible in a note nobody re-read.

## Limitations

- C3 is the soft spot and always was. "Minor quality degradation" is not a
  bound, and at larger scales the degradation turned out to matter enough
  that GQA exists.
- 2019 scale; the KV cache has since grown enormously relative to weights,
  which strengthens C1 and changes the size of the prize.
- No exploration of intermediate points between one KV head and `h` — which
  is exactly the gap GQA fills.

## Open questions

- The paper goes from `h` KV heads to 1 without examining the interval. That
  GQA found the answer there suggests asking, generally, whether other
  binary architectural choices in this record are really continua.
- C1 is now made at three altitudes in this record — architecture here,
  kernel in FlashAttention, memory management in vLLM. Is there a fourth?
