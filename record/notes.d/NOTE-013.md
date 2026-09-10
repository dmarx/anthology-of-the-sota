---
number: 13
status: Read
formerly:
- NOTE-tmpe03a9
paper: LIT-084
title: 'DeepNet'
version: 1
tags:
- model-stability
date: '2026-09-09'
published: '2022-03-01'
summary: >-
  Scale the residual by α and initialise the residual branch with gain β, both constants determined only by depth. Bounds the model update theoretically, combines Post-LN's quality with Pre-LN's stability, and reaches 1,000 layers.
---

# NOTE-013: DeepNet

## Contribution

Post-LN trains well and destabilises with depth; Pre-LN is stable and gives up
quality. DeepNet takes both by modifying the residual connection —
**DeepNorm** — with an accompanying **theoretically derived initialization**,
and shows analytically that the model update is bounded. It scales
Transformers to **1,000 layers** (2,500 sublayers), an order of magnitude
deeper than prior work, and a 200-layer 3.2B model beats a 48-layer 12B model
by **5 BLEU** across 7,482 translation directions.

## Key insight

Depth instability is a statement about the *magnitude of the update* a step
produces, and that magnitude can be computed rather than tuned around. Once
you can bound it, the two knobs that matter fall out as constants: how much
of the identity path survives the normalization (`α`), and how large the
residual branch starts (`β`). Both depend only on the architecture and its
depth — nothing is swept.

That is what separates this from the surrounding literature: it does not
propose a heuristic that empirically helps deep models, it derives the
scaling from a bound and then confirms it at a depth nobody had reached.

## Assumptions

- The derivation studies the **1-head attention case** without loss of
  generality, and models the sublayer's magnitude behaviour under Xavier
  initialization — under which "the output can preserve the input variance",
  equivalent to `v = w = 1`.
- Constants are per-architecture: encoder-only, decoder-only and
  encoder-decoder each get their own `α`, `β`, with `N` encoder and `M`
  decoder layers.
- Machine translation is the demonstration domain, at 2022 scales.

## Key results

- **DeepNorm**: `LayerNorm(x·α + f(x))` — the residual scaled by `α` before
  normalization.
- **Initialization**: Xavier with gain `β` on `ffn`, `v_proj` and `out_proj`;
  gain `1` on `q_proj` and `k_proj`. The query and key projections are
  deliberately *not* downscaled.
- **The constants**, depending only on depth:

  | architecture | `α` | `β` |
  |---|---|---|
  | encoder-only (BERT) | `(2N)^(1/4)` | `(8N)^(−1/4)` |
  | decoder-only (GPT) | `(2M)^(1/4)` | `(8M)^(−1/4)` |
  | encoder-decoder (encoder side) | `0.81·(N⁴M)^(1/16)` | `0.87·(N⁴M)^(−1/16)` |
  | encoder-decoder (decoder side) | `(3M)^(1/4)` | `(12M)^(−1/4)` |

- **Model updates are bounded**, which is the paper's analytic claim and the
  reason the constants are derived rather than searched.
- **1,000 layers** trained "without difficulty".
- **200 layers / 3.2B beats 48 layers / 12B by 5 BLEU** on a 7,482-direction
  multilingual benchmark — depth substituting for width at a quarter of the
  parameters.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Depth instability is a bounded-update problem, not an inherent limit | strong | the derivation, confirmed at 1,000 layers |
| C2 | `α` and `β` depend only on the architecture and depth | strong | derived in §4.3, tabulated, nothing swept |
| C3 | DeepNorm gets Post-LN's quality with Pre-LN's stability | moderate | the paper's framing, measured on translation |
| C4 | Depth can substitute for width at equal or better quality | moderate | one comparison — 200L/3.2B vs 48L/12B — on one benchmark family |
| C5 | Query and key projections should not be downscaled | strong | explicit in the initialization rule, and derived |

## Method

Replace each residual connection with `LayerNorm(x·α + f(x))`. Initialise the
residual-branch weights — feed-forward, value and output projections — with
Xavier gain `β`, leaving query and key projections at gain 1. Read `α` and `β`
off the table for the architecture and depth.

## Concepts

- **DeepNorm** — the modified residual, `LayerNorm(x·α + f(x))`.
- **Bounded model update** — the quantity the derivation controls. The
  paper's real object; the constants are consequences of bounding it.
- **`α` / `β`** — how much identity path survives normalization, and how
  small the residual branch starts. Note they move in opposite directions
  with depth: `α` grows as `N^(1/4)`, `β` shrinks as `N^(−1/4)`.

## Connections

Sits directly between Post-LN and Pre-LN, taking the stated advantage of
each. Its downscaled residual-branch initialization is the same instinct as
the record's other start-the-branches-quiet practices, and unlike those it is
derived rather than chosen.

## Recommendations

- **R1** — Scale the residual and downscale the residual branch by
  depth-determined constants when training very deep Transformers. *Topic:*
  stability. *Status:* standard for the depths measured. *Strength:* strong.
  *Applies when:* depth is the binding constraint on stability.
- **R2** — Do not downscale query and key projections along with the rest.
  *Topic:* initialization. *Status:* standard. *Strength:* strong.
  *Applies when:* applying any residual-branch downscaling; this one is easy
  to get wrong by treating "the projections" uniformly.
- **R3** — Prefer a derived constant to a swept one where a bound is
  available. *Topic:* methodology. *Status:* standard. *Strength:* moderate.
  *Applies when:* the quantity being tuned has an analysable magnitude.

## Bearing on the record

**The one practice sourced to this note is confirmed, and is much vaguer than
its source.**

| practice | disposition |
|---|---|
| [SOTA-052](../practices.d/SOTA-052.md) use smaller variance for deep networks | confirmed, and understated |

"Smaller variance for deep networks" is a true description of `β` and states
none of it: not that `β = (8N)^(−1/4)` for a decoder, not that `α` grows as
the same root while `β` shrinks, and not that **query and key projections are
excluded**. That last is the part a reader would most plausibly get wrong from
the practice as written, and it is explicit in the source.

This is the same shape as `SOTA-017`/`SOTA-019` under GPipe: the practice was
right and stated at a level nobody could act on, which is what a note nobody
read against its paper produces even when nothing in it is wrong.

## Limitations

- Machine translation throughout; no language-modelling evidence here.
- C4 rests on a single size-for-depth comparison.
- The derivation assumes Xavier-initialized projections preserving input
  variance; a different initialization scheme changes the constants and the
  paper does not say how.
- 1,000 layers is a demonstration of stability, not of usefulness — nothing
  argues that depth is where the next gain is.

## Open questions

- The constants are derived for three architecture families. What are they
  for a hybrid, or for a model with non-uniform sublayers?
- `α` and `β` move oppositely with depth. Is there an equivalent statement in
  the µP language, where per-layer scaling is a property of the
  parameterisation?
