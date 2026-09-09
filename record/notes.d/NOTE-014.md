---
number: 14
status: Read
formerly:
- NOTE-tmpe24hp
paper: LIT-115
title: 'Monarch Mixer'
version: 1
tags:
- attention-techniques
date: '2026-09-09'
summary: >-
  One sub-quadratic primitive — Monarch matrices — along both sequence length and model dimension. Matches BERT-base/large on GLUE with up to 27% fewer parameters and 9.1× throughput at 4K, and beats ViT-b by 1% at half the parameters. Attention-free, not hybrid.
---

# NOTE-014: Monarch Mixer

## Contribution

Transformers scale quadratically along **two** axes — sequence length and
model dimension — and the attention-efficiency literature almost entirely
addresses the first. This paper asks for a single primitive that is
sub-quadratic along both, and proposes Monarch matrices: a class of
structured matrices expressive enough to capture many linear transforms,
sub-quadratic to apply, and — the part that makes it practical — high in
hardware utilisation on GPUs because it decomposes into GEMMs. It then shows
the resulting architecture is competitive in three unrelated domains.

## Key insight

Most efficient-attention work replaces the sequence mixer and leaves the MLP
alone, which caps the achievable saving because the model dimension is still
quadratic. Using **the same primitive for both mixers** is the move, and the
reason it is possible is that Monarch matrices are general enough to serve as
either.

The second insight is a hardware one and it is why this differs from the long
line of FFT-based long-convolution models: attention blocks are memory-bound,
so even FlashAttention reaches relatively low FLOP utilisation. A primitive
built out of GEMMs gets the tensor cores that attention cannot.

## Assumptions

- **Proof-of-concept scale.** BERT-base/large, ViT-b, and small GPT-style
  models. Nothing here approaches frontier scale, and the paper calls it a
  proof of concept.
- Three domains are tested — non-causal BERT-style LM, ViT-style image
  classification, causal GPT-style LM — and the causal case is the hard one.
- **Causality introduces a quadratic bottleneck.** Enforcing it by masking
  reintroduces the cost the architecture exists to avoid; the paper develops
  new theory (a multivariate-polynomial view of Monarch matrices) to get
  around it.
- Several results set the Monarch matrices to the DFT and inverse DFT, i.e.
  the architecture is evaluated at a particular instantiation rather than
  learned in full generality.

## Key results

- **BERT-style**: matches BERT-base and BERT-large on downstream GLUE with up
  to **27% fewer parameters**, and up to **9.1× higher throughput at sequence
  length 4K**.
- **ImageNet**: M2-ViT beats ViT-b by **1% accuracy with half the
  parameters**. Built on HyenaViT-b, replacing its long convolutions with the
  M2 operator *and* its MLP blocks with M2.
- **Causal GPT-style**: M2-GPT combines Hyena's convolutional filter with
  H3's parameter sharing across heads, under a causal parameterisation that
  avoids the masking bottleneck. The paper's reading: "radically different
  architectures than Transformers may be performant on causal language
  modeling."
- **The motivation for GEMMs**: attention blocks are memory-bound, so even
  optimised implementations like FlashAttention have relatively low FLOP
  utilisation. Monarch matrices get high utilisation "out of the box".

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | One sub-quadratic primitive can serve both the sequence and dimension mixers | strong | the architecture works in three domains |
| C2 | M2 matches BERT quality at 27% fewer parameters and 9.1× throughput at 4K | strong | measured, non-causal |
| C3 | M2-ViT beats ViT-b by 1% at half the parameters | moderate | one benchmark, one baseline |
| C4 | Structured matrices reach higher FLOP utilisation than attention because they are GEMMs | strong | architectural, and the premise of the design |
| C5 | Causal modelling is achievable without reintroducing the quadratic cost | moderate | new theory plus small-scale results; the paper frames it as suggestive |
| C6 | Attention can be dispensed with entirely | moderate | at proof-of-concept scale, in three domains |

## Method

**Architecture:** Monarch Mixer (M2).

Replace both the sequence mixer (attention) and the dimension mixer (MLP)
with operators built from **Monarch matrices** — block-diagonal matrices
interleaved with permutations, which decompose into GEMMs and so run at high
utilisation. For causal modelling, use the multivariate-polynomial view to
parameterise causality directly rather than masking a non-causal operator.

## Concepts

- **Monarch matrix** — a structured matrix formed from block-diagonal factors
  and permutations; sub-quadratic to apply, expressive enough to capture many
  standard linear transforms including the DFT.
- **Sequence mixer / dimension mixer** — the two places a Transformer moves
  information: attention across positions, the MLP across channels. Naming
  them separately is what makes "sub-quadratic along both axes" statable.
- **The causal bottleneck** — enforcing causality by masking a non-causal
  operator costs quadratic work, so an attention-free causal model needs
  causality built into the parameterisation.

## Connections

Builds directly on the long-convolution line — Hyena, H3, HyenaViT — which
replaces attention with FFT-computed long convolutions; M2-GPT takes Hyena's
filter and H3's head-sharing. Its argument against that line is the same one
it makes against attention: FFT operations do not use tensor cores well, and
GEMM-decomposable structure does.

## Recommendations

- **R1** — When the model dimension is as much of a bottleneck as the
  sequence length, look for a primitive that addresses both. *Topic:*
  architecture. *Status:* experimental. *Strength:* moderate. *Applies when:*
  scaling width and context together.
- **R2** — Prefer GEMM-decomposable structure to FFT-based operators for
  efficiency work on tensor-core hardware. *Topic:* kernels. *Status:*
  experimental. *Strength:* moderate. *Applies when:* the operator is a
  choice; utilisation, not FLOP count, is the thing to compare.
- **R3** — Build causality into the parameterisation rather than masking a
  non-causal operator. *Topic:* architecture. *Status:* experimental.
  *Strength:* moderate. *Applies when:* designing an attention-free causal
  model.

## Bearing on the record

**Two of three practices confirmed; one is the opposite of what the paper
does.**

<!-- inactive-ok-block: SOTA-112 — Rejected in this same change; the table is the record of why -->
| practice | disposition |
|---|---|
| [SOTA-110](../practices.d/SOTA-110.md) consider M2 in place of attention for very long sequences | confirmed |
| [SOTA-111](../practices.d/SOTA-111.md) use M2 where attention's quadratic cost bottlenecks | confirmed, and **understated** |
| [SOTA-112](../practices.d/SOTA-112.md) combine M2 layers with standard attention rather than replacing all | `Rejected` |

<!-- inactive-ok-block: SOTA-112 — Rejected in this same change; the paragraph is the record of why -->
**`SOTA-112` inverts the paper.** M2 is **attention-free**. The string
`hybrid` occurs **zero times**; what the paper does is *replace* attention —
"attention-free models by replacing attention layers", "M2-ViT ... replaces
the long convolutions with the M2 operator", "radically different
architectures than Transformers". Its own summary of the causal result is
that Transformers may be dispensable, not that they should be interleaved.

The practice's reasoning — that a structured mixer and attention fail
differently, so a hybrid gets the best of both — is a real argument, and it
is the argument made by the *attention/SSM* hybrid literature elsewhere in
this record, not by this paper. Attributing it here is the fourth inversion
in [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) and the most direct: not a wrong emphasis or a transposed
constant, but a recommendation the source argues against.

**`SOTA-111` understates its own source.** It says to use M2 where
attention's quadratic cost is the bottleneck — sequence length. The paper's
contribution is sub-quadratic scaling along **sequence length *and* model
dimension**, using one primitive for both, and the dimension half is what
distinguishes it from the entire efficient-attention literature.

## Limitations

- Proof-of-concept scale throughout; BERT-large is the largest thing here.
- C3 rests on one benchmark against one baseline.
- Several results fix the Monarch matrices to DFT/inverse-DFT, so the
  learned-general case is less tested than the headline suggests.
- The causal results are the weakest and the paper says so — the masking
  bottleneck needed new theory, and the evidence after it is suggestive.

## Open questions

- Does any of this survive to frontier scale? Nothing in this record trains
  an M2 model above BERT-large.
- The record holds attention/SSM hybrids that *do* interleave mechanisms.
  Whether a Monarch mixer would benefit from the same treatment is an open
  question and, importantly, **not one this paper asks**.
- C4 says utilisation rather than FLOPs is what to compare. That is the same
  claim FlashAttention makes about memory traffic, one level down. How many
  of the record's efficiency practices compare the wrong quantity?
