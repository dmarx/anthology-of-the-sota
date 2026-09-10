---
number: 52
status: Read
formerly:
- NOTE-tmpmgnf7
paper: LIT-085
title: 'Progress measures for grokking via mechanistic interpretability'
version: 2
history:
- version: 2
  date: '2026-09-10'
  note: >-
    Corrected. The reading recorded the data-fraction result as
    something any claim about delayed generalization needs to know, and
    in the same breath declined to argue with the paper's Rejected
    status. Filing SOTA-tmpwccgh, which needs this paper, made that
    untenable; LIT-085 is now Active and this note says so.
tags:
- analysis-and-evaluation
date: '2026-09-09'
summary: >-
  Reverse-engineers a one-layer transformer trained on modular addition and finds it computes a Fourier multiplication algorithm — embed inputs as rotations, combine with trigonometric identities. Uses that to define continuous progress measures showing grokking is three phases, and finds grokking vanishes entirely above about 60% data.
---

# NOTE-052: Progress measures for grokking via mechanistic interpretability

## Contribution

Takes an apparently discontinuous phenomenon and finds the continuous quantity
underneath it, by **fully reverse-engineering the network** rather than by
fitting a curve to the loss.

The model — a one-layer transformer on `a + b mod 113` — is shown to implement a
**Fourier multiplication algorithm**: the embedding maps `a` and `b` to sines
and cosines at a sparse set of key frequencies `w_k`; attention and MLP combine
them with trigonometric identities into `sin(w_k(a+b))` and `cos(w_k(a+b))`; the
output matrices recombine. **Addition is done by rotating on a circle.**

From that algorithm, two progress measures are defined that increase
*continuously* through the apparently sudden grokking transition.

## Key insight

The methodological one: **you can only define a good progress measure if you
know what the network is computing.** "Restricted loss" and "excluded loss" are
computed by projecting onto or removing the key frequencies — quantities that
are meaningless without the reverse-engineering, and which reveal that the
network is making steady progress the whole time.

The empirical one, which deflates the phenomenon: **grokking is a function of
data fraction.** With ≥60% of the `113 × 113` pairs, generalization is
**immediate** — no grokking at all. Smaller fractions grok more slowly. So the
dramatic delayed generalization is not a fundamental property of learning; it is
what happens in a specific data-starved regime.

## Assumptions

- **Modular addition with `P = 113`, one-layer transformers, full-batch
  training.** Everything here is about a task chosen because it is small enough
  to fully understand.
- The algorithm found is the algorithm used — checked by ablation (§4.4) and
  replicated across five random seeds.
- AdamW, `γ = 0.001`, weight decay `λ = 1`, 40,000 epochs. The weight decay is
  large and is load-bearing (§5.3).

## Key results

- **The unembedding `W_L` is approximately rank 10** — five key frequencies × a
  sine and a cosine each. Projecting MLP activations onto its components
  produces multiples of `cos(w_k(a+b))` and `sin(w_k(a+b))`.
- **Individual neurons are well approximated by degree-2 polynomials of sines
  and cosines at a *single* frequency**, and the matching `W_L` direction carries
  only that frequency. Computation is **localised across frequencies** and
  **mostly aligned with the neuron basis** — a strong and unusual result about
  where structure lives.
- **Three phases: memorization, circuit formation, cleanup**, identified via
  excluded loss, restricted loss, Gini coefficients of `W_U` and `W_L`, and the
  sum of squared weights.
- **≥60% data fraction removes grokking entirely.**
- Replicated across 4 additional seeds; ablations excluding each key frequency
  show interpolation between memorising and generalising.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The network computes modular addition by Fourier multiplication | strong | weights, neurons, ablations, five seeds |
| C2 | Computation is localised by frequency and aligned with the neuron basis | strong | measured per neuron |
| C3 | Grokking decomposes into three phases with continuous progress measures | strong | the measures are defined from C1 and behave as claimed |
| C4 | Grokking disappears above ~60% data | strong | measured across data fractions |
| C5 | Weight decay drives the cleanup phase | moderate | §5.3, and `λ = 1` is unusually large |
| C6 | This generalises to emergence broadly | **weak — offered as "a proof of concept"** | one task, one tiny model |

## Method

Train a one-layer transformer on modular addition. Inspect the embedding for
periodicity. Decompose `W_L`; project MLP activations; fit neurons with
low-degree trigonometric polynomials. Ablate frequencies. Define restricted and
excluded loss from the recovered algorithm and plot them through training.

## Concepts

- **Progress measure** — a continuous quantity underlying a discontinuous
  capability, and the paper's contribution to how emergence is discussed.
- **Reverse-engineering as measurement design** — C1 is not the point; it is the
  instrument that makes C3 possible.
- **Grokking as a data-regime artefact** — C4, and the finding most people who
  cite this paper do not carry.

## Connections

`LIT-077` (BIG-bench), read in the same batch, is the same question at the other
end: which capabilities appear suddenly with scale, and it finds "breakthrough"
tasks are those with multiple steps or **brittle metrics**. Both papers point at
the same conclusion from opposite directions — **apparent discontinuity is often
a property of the measurement or the regime, not of the learning.**

The record's `LIT-011` neighbourhood (loss landscape, eigenvalue ratios) is the
other analysis-of-training-dynamics line, and `SOTA-070` (track gradient norm
ratios between layers) is the record's only practice of the "watch a continuous
quantity during training" kind.

## Recommendations

- **R1** — Before calling a capability emergent, check whether a continuous
  measure underlies it. *Topic:* analysis and evaluation. *Strength:* strong as
  a caution; the *construction* of such a measure required full
  reverse-engineering, so it is not cheap advice.
- **R2** — Check whether a training phenomenon survives a change in data
  fraction before treating it as fundamental. *Strength:* strong — C4.
- **R3** — Report the data regime alongside any claim about learning dynamics.
  *Strength:* strong.

## Bearing on the record

**This reading was filed against a `Rejected` document and did not argue with
the status. It should have, and the paper is now `Active`.**

What was written here first: that one 113-element modular-addition task on a
one-layer transformer is not a source for practice at the record's usual scale,
that the authors call the generalisation claim a proof of concept, and that R2
is nonetheless the reason to keep the paper — **grokking is the most-cited
"mysterious training phenomenon" of its period and it goes away above 60%
data.**

The last of those contradicts the first two. A finding that any claim about
delayed generalization needs to know is not "not interesting enough to carry",
which is what `Rejected` means for a paper in this vocabulary. The setting is
small, and a small setting is a limitation to state — this note states it under
Limitations — rather than a reason for the attic.

The contradiction became unavoidable when the same session filed
`SOTA-tmpwccgh` (check whether an emergent capability is a metric artefact),
which needs this paper for half of its claim. `ADR-002` does permit an attic
paper to source a live practice, and that permission is for a paper whose
*standing* moved while its *result* held. Nothing about this result moved.

**R2 is now a practice**, jointly with `LIT-077`.


The document's takeaways — "grokking measurement", "interpretability metrics",
"learning dynamics analysis", "phase transition detection" — name four
categories. None says what the network was found to be doing, which is the
paper's actual result and the thing that makes the metrics definable.

## Limitations

- One task, `P = 113`, one-layer transformer, 40,000 epochs of full-batch
  training. Nothing about scale.
- Weight decay is `λ = 1`, far from any practical setting, and it drives a phase.
- C6 is disclaimed by the authors and is nonetheless how the paper is usually
  cited.
- The progress measures are task-specific by construction; the method does not
  transfer without a new reverse-engineering.

## Open questions

- Is there a general recipe for progress measures that does not require solving
  the network first? The paper's method is a proof that they exist, not a way to
  find them.
