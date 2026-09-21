---
status: Read
paper: LIT-tmpci13h
title: 'Limitations of multi-layer Transformers'
version: 1
date: '2026-09-21'
summary: >-
  First unconditional lower bound for a decoder-only transformer of more than
  one layer. Reading it: the bound comes from causal masking rather than from
  circuit complexity, and it buys an exponential depth-width tradeoff, an
  encoder/decoder separation, and a provable benefit of chain of thought.
---

<!-- inactive-ok-file: SOTA-125 SOTA-tmphvq7d — SOTA-125 is Proposed and is named as the independently-reached tiny-model counterpart, not as support for this result; SOTA-tmphvq7d is Proposed and filed here from this reading -->
# NOTE-tmpdirge: Limitations of multi-layer Transformers

## Contribution

Before this, unconditional lower bounds existed only for one-layer
transformers; for two layers and up, every limitation result assumed an
unproven complexity conjecture, and there was a published argument that this
was unavoidable — that beating it would require breakthrough circuit lower
bounds. This proves one unconditionally. What is true afterwards that was not
before is that there is at least one concrete task a constant-depth
decoder-only transformer provably cannot do at small size, with nothing
assumed.

## Key insight

The barrier is dodged rather than broken, and the dodge is the idea. Circuit
lower bounds are hard because a general circuit is unstructured. A
decoder-only transformer has a structure nobody else was using: causal
masking. A position can only send information rightwards, and — the part that
does the work — a position does not retain what it forwarded. Model that as
a communication game between *forgetful* players on a line, one epoch per
attention layer, and the bottleneck becomes provable. Sequential composition
is hard because it needs information to flow back through positions that have
already spoken and forgotten.

## Assumptions

- **Decoder-only.** The bound depends on causal masking and does not apply to
  an encoder — indeed the encoder solving the same task is one of the
  results.
- **Constant depth `L`**, with context length `n` the growing parameter.
  "Small" means the model has `n^o(1)` parameters in the paper's convention.
- **Bounded precision `p`** per embedding entry, which enters the bound.
- **Representability, not learnability.** The claim is that no parameter
  setting computes the function. Nothing is claimed about what gradient
  descent finds, what a trained model does, or what happens at any fixed
  finite `n`.
- **The hard task is constructed.** `k`-sequential function composition is
  chosen to be hard for this model, not sampled from anything anyone trains
  on.

## Key results

- **Theorem 1.1** — an `L`-layer decoder-only transformer cannot solve
  `k`-sequential function composition when the model is small relative to
  prompt length, for any constant `L`. *Holds when:* the head count, head
  dimension and precision multiply to below the stated bound.
- **Corollary 1.2 (depth-size tradeoff)** — a `log k`-layer transformer
  solves the task with polylogarithmic parameters; any constant-layer one
  needs polynomially many. Exponential, and — the paper is pointed about this
  — obtained for a benign function, where the analogous feed-forward ReLU
  result runs into natural-proof barriers and existing work has to use
  wildly oscillating functions instead.
- **Corollary 1.3 (encoder/decoder separation)** — an encoder solves it
  exponentially shallower and smaller. The first such separation with no
  conjecture; the prior one assumed hardness of a triplet-counting problem.
- **Corollary 1.4 (provable benefit of chain of thought)** — a **one-layer**
  transformer with `k` steps of chain of thought solves it with
  polylogarithmic parameters. Prior CoT results needed `TC⁰ ≠ P`-style
  assumptions to say anything; this needs none.
- **Lemma 3.1** — a decoder-only transformer is simulated by an
  autoregressive communication protocol whose message size is proportional to
  each player's input length. This is the bridge the whole paper crosses.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Constant-depth small decoders cannot do `k`-sequential composition | strong | Theorem 1.1, unconditional |
| C2 | Depth buys exponentially more than width on composition tasks | strong | Corollary 1.2, from C1 plus an explicit construction for the upper bound |
| C3 | Encoders are strictly more powerful than decoders on some task | strong | Corollary 1.3, unconditional where the prior result was conjectural |
| C4 | Chain of thought provably substitutes for depth | strong | Corollary 1.4 — but see below for what it does *not* establish |
| C5 | This explains empirically observed compositional failure | weak | the paper offers it as "theoretical justification" for prior empirical findings; no experiment here, and asymptotic results do not transfer to a measured failure without an argument nobody makes |

## Concepts

- **`k`-sequential function composition** — given `k` functions and a query,
  compute `f_k(...f_1(q))`.
- **Autoregressive communication model** — players on a line, messages
  rightward only, each player forgetful of what it sent. One epoch per
  attention layer.
- **Small vs large transformer** — the paper's convention: small is `n^o(1)`
  parameters, large is `n^Ω(1)`, with `n` the prompt length.

## Connections

Extends the one-layer lower bounds (two-function composition, 3SUM,
induction heads) to constant depth. Sits against the conditional line that
places transformers inside `TC⁰`, log-space, or massively parallel
computation — all of which need a conjecture. Cites empirical work finding
that transformers degrade rapidly as composition depth grows, and work
finding depth matters more than width for reasoning, as the phenomena it
justifies.

## Bearing on the record

- **It is the record's first lower bound.** Everything else here says what to
  do or why something works. A claim about what is unavailable at any tuning
  is a different shape, and the record had none.
- **It produces [SOTA-tmphvq7d](../practices.d/SOTA-tmphvq7d.md)** — buy depth rather than width for
  compositional tasks — which is the general-scale theoretical counterpart to
  [SOTA-125](../practices.d/SOTA-125.md), filed from tiny-model experiments.
- **It produces [THEORY-tmpahhzk](../theory.d/THEORY-tmpahhzk.md)**, the forgetfulness account.
- **It does not produce a chain-of-thought practice, and the record has
  none.** [SOTA-127](../practices.d/SOTA-127.md) says to filter chain-of-thought traces out of tiny
  models' training data; that is the record's only CoT document. Corollary 1.4
  is a representability result — it says a one-layer model *with* CoT can
  express the composition, not that a trained model uses CoT this way or that
  emitting steps helps on any task anyone runs. Sourcing "use chain of
  thought" to it would be sourcing a recommendation about inference to an
  existence proof, which is what [ADR-017](../decisions.d/ADR-017.md) asks about. The gap is named
  instead.

## Limitations

- Asymptotic. No constant is small enough to tell you anything about a
  concrete model at a concrete context length.
- The hard task is adversarially constructed for this model class.
- Representability only: a bound on what can be expressed says nothing about
  what training finds.
- Constant `L` throughout, so it does not speak to the regime where depth
  grows with the problem.
- No experiments at all, which is appropriate for the claim and worth saying
  because the paper's framing invites reading it as an explanation of
  measured behaviour.

## Open questions

- Does the bound survive as `L` grows with `n`?
- Is there a *natural* task — one people train on — that the technique
  reaches, rather than a constructed one?
- The encoder/decoder separation is real; does anything follow for
  architecture choice, given that decoder-only won for reasons of generation
  and efficiency that this does not touch?
