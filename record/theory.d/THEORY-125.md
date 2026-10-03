---
number: 125
status: Proposed
formerly:
- THEORY-tmpx14qc
promote_when: >-
  The negative half is proved: with one affine autoregressive block every
  conditional is a single Gaussian, which one line of the paper's Eq. 4
  shows and anyone can check. The positive half is a sketch. It argues that
  each conditional becomes an infinite Gaussian mixture and that such
  mixtures are dense, but not that the mixing distribution a second or
  third block induces can be made arbitrary, which is what density needs.
  Two kinds of result would settle it. One is a complete proof that stacks
  of three affine autoregressive blocks in alternating orders are dense in
  L1, or a citation of an existing one that covers this architecture. The
  other is a low-dimensional test that could come out the other way: a
  target whose last coordinate is multimodal given the rest, fitted by two
  and by three blocks of matched capacity, where the account predicts two
  blocks miss that coordinate's modes and three do not. Another image model
  whose one-block arm fails would not count; that half is not in doubt.
title: "One affine autoregressive flow block makes every conditional a single Gaussian and cannot approximate an arbitrary density, while two blocks in opposite orders make every conditional but the last a Gaussian mixture and three make all of them one"
version: 1
tags:
- generative-modeling
- flows-and-transport
- model-architecture
date: '2026-10-03'
source:
- LIT-785
- LIT-794
summary: >-
  Gu et al. (2025), [LIT-785](../literature.d/LIT-785.md), §3.1, Prop. 1 and App. A.1. In one
  affine autoregressive block each coordinate is a mean plus a scale times
  fresh Gaussian noise, both functions of the coordinates before it, so
  every conditional is one Gaussian and no multimodal conditional can be
  represented. A second block in the opposite order feeds later latents
  into those parameters and turns each conditional into an infinite
  Gaussian mixture, except the last coordinate's; a third restores that
  one. The one-block half is proved and is what TarFlow ([LIT-794](../literature.d/LIT-794.md))
  measured, FID 267 at matched depth. The universality half is a sketch.
---

<!-- inactive-ok-file: THEORY-120 — Proposed; named to separate its account of TarFlow's noise requirement from this one, not as a settled result -->

# THEORY-125: One affine autoregressive flow block makes every conditional a single Gaussian and cannot approximate an arbitrary density, while two blocks in opposite orders make every conditional but the last a Gaussian mixture and three make all of them one

## Source

Gu, Chen, Berthelot, Zheng, Wang, Zhang, Dinh, Bautista, Susskind and Zhai
(2025), [LIT-785](../literature.d/LIT-785.md) — STARFlow, §3.1, Prop. 1, Eqs. 4–5, App. A.1 and
Figs. 10e–f. Zhai, Zhang, Nakkiran, Berthelot, Gu, Zheng, Chen, Bautista,
Jaitly and Susskind (2024), [LIT-794](../literature.d/LIT-794.md) — TarFlow, §3.5 and Fig. 6b.

## The account

**One block is a Gaussian autoregressive model.** An affine autoregressive
flow block writes each coordinate as x_d = μ(x_<d) + σ(x_<d)·z_d, with z_d
standard normal. STARFlow ([LIT-785](../literature.d/LIT-785.md), App. A.1) points out what this
forces: given x_<d, the only randomness in x_d is z_d, so p(x_d | x_<d) is
a single Gaussian whatever networks compute μ and σ. The joint can be
complicated, but no conditional can be multimodal or heavy-tailed. This is
the proved half, and it needs nothing but Eq. 4 read with one block.

**A second block in the opposite order makes the conditionals mixtures.**
With two blocks, x_d = μ_b(x_<d) + σ_b(x_<d)·y_d, where y_d itself comes
from a block that runs the other way and depends on the later latents
y_>d. Integrating those out (Eq. 5) makes p(x_d | x_<d) a Gaussian whose
mean and scale depend on y_>d, averaged over y_>d: an infinite Gaussian
mixture. STARFlow then appeals to the density of Gaussian mixtures,
"with the expressive power of neural networks", to call these conditionals
universal.

**The last coordinate is the exception, and a third block removes it.**
For d = D there are no later latents, y_D is a plain Gaussian, and so is
x_D given the rest. A third block feeds fresh latents into that
coordinate's parameters and makes it a mixture too (App. A.1). Hence the
paper's statement: three or more blocks in alternating orders are
universal, two are universal on D − 1 coordinates, and in high dimensions
the authors expect the missing one to be "negligible".

## What was measured

- **One block fails at matched depth, in two papers.** TarFlow
  ([LIT-794](../literature.d/LIT-794.md), §3.5, Fig. 6b) holds the total number of layers fixed
  and varies the split between blocks and layers per block on conditional
  ImageNet 64×64. The one-block model "degenerates to an incapable model",
  with high loss and FID 267, "equivalent to random guess", where two
  blocks give "much more reasonable performance". STARFlow's Fig. 10f does
  the same in latent space at 28 layers in total. Read from the plot (no
  values are tabled), one deep block of 28 layers ends near 16.5 FID on
  4,096 samples, and two blocks of 26 and 2 layers near 11.5, with the four
  arms of two to eleven blocks clustered there too.
- **Beyond two blocks, nothing changes measurably.** STARFlow's Fig. 10e
  keeps an 18-layer deep block and varies the total block count from one
  to seven. One block ends near 19 FID, and two through seven sit together
  near 11.5 (read from the plot; the one-block arm also has two to twelve
  fewer layers). The text: "Performance drops sharply when T < 2, while
  models with T ≥ 2 perform similarly—consistent with Prop. 1."

## What this does not say

- **Not that three blocks are universal, as a theorem.** The step from "each
  conditional is an infinite Gaussian mixture" to "the family is dense in
  L1" needs the mixing distribution, p(y_>d | x_<d), to be free enough to
  approximate any mixture. That distribution is itself produced by the
  other block and tied across coordinates, and the sketch does not show it
  can be. The paper labels the argument a "Sketch of Proof".
- **Not that the two-versus-three distinction shows up in images.** Every
  experiment varies the block count from one upward and sees one block fail.
  None could see the difference between two and three, which concerns one
  coordinate out of thousands. Fig. 10e's flat curves from two blocks on
  are what the account predicts and are also what a model indifferent to
  the last coordinate would show.
- **Not that block count is what makes a flow good.** Fig. 10f's arm with
  fourteen 2-layer blocks is as bad as one 28-layer block. Universality is
  about the limit of capacity, and says nothing about how depth should be
  spread across blocks. STARFlow's own conclusion from these figures is
  that "block depth is more critical than quantity".
- **Not the same account as the noise requirement.** [THEORY-120](THEORY-120.md) is
  about why TarFlow samples only when its data carry Gaussian noise, a
  question of how well the inverse is conditioned over the latent. This
  account is about what a stack of blocks can represent at all. TarFlow's
  one-block failure and its uniform-noise failure are different
  observations, and neither paper varies the block count and the noise
  together, so nothing tests whether the two interact.
