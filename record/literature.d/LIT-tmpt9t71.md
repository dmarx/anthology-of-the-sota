---
status: Active
title: 'Round and Round We Go! What makes Rotary Positional Encodings useful?'
version: 1
tags:
- attention-techniques
date: '2026-09-07'
published: '2024-10-01'
arxiv: '2410.06205'
first_author: 'Barbero'
keywords:
- 'rope'
- 'positional-encoding'
- 'mechanistic-interpretability'
- 'long-context'
- 'attention-heads'
- 'frequency-analysis'
extends:
- LIT-045
# Table 2 runs NoPE, RoPE and p-RoPE at matched configuration, and the paper
# separately establishes that NoPE cannot build the positional heads RoPE's
# high frequencies allow.
compared_against:
- LIT-207
implementations:
- 'analysis of Gemma 7B'
- 'analysis of Llama 3.1 8B'
summary: >-
  Barbero et al. (2024), [ARXIV-2410.06205](https://arxiv.org/abs/2410.06205). Opens up a trained Gemma 7B to
  ask what RoPE is actually doing, and the answer is not the one RoPE's own
  paper gave: attention does not reliably decay with distance, and the model
  instead splits the frequency band in two — the highest frequencies build
  robust positional attention heads, the lowest carry semantic content in
  channels that are provably not robust over long context. Removing the
  lowest frequencies (p-RoPE) fixes that and improves perplexity at 2B, and
  p is a dial whose ends are exactly RoPE and NoPE.
---

# LIT-tmpt9t71: Round and Round We Go! What makes Rotary Positional Encodings useful?

Barbero et al. (2024) — [ARXIV-2410.06205](https://arxiv.org/abs/2410.06205)

## Key takeaways

**The decay story is wrong, and it was RoPE's own justification.** RoFormer
argued the encoding is useful because attention decays with relative
distance. That holds for the case the argument assumes — queries and keys
already aligned, or constant all-ones vectors — and fails for Gaussian ones,
where misaligned pairs can have their dot product *increase* with distance.
The paper proves the sharper version: given any key, a query exists making
RoPE's contribution maximal at any chosen relative distance, however large.
Whatever RoPE is doing for a model, it is not enforcing locality.

**The frequency band is used for two different jobs.** Gemma 7B
overwhelmingly prefers RoPE's *low* frequencies, with the first and last
layers the exception, making the heaviest use of the high ones. That split
is functional rather than incidental:

- **High frequencies build positional attention heads.** The paper gives a
  construction — keys nearly identical, queries a rotation matching one of the
  highest frequencies — that attends to a fixed offset, proves it robust, and
  then finds a strikingly similar circuit inside Gemma. Previous-token heads
  and diagonal heads are what this buys.
- **Low frequencies carry semantics**, in distinct high-norm bands the
  authors read as information channels — and Theorem 6.1 proves those
  channels *cannot* be robust once the context is long.

**p-RoPE, and why it is the paper this record most needed.** If the low
frequencies are the fragile part, truncating them should not hurt. It does
not: keeping a fraction p of RoPE's frequencies holds performance and, at 2B,
improves it. Validation perplexity on Wiki / FlanV2 — NoPE 4.8594 / 6.6429,
RoPE θ=10k 4.4627 / 6.4429, RoPE θ=500k 4.4485 / 6.4593, 0.75-RoPE 4.4414 /
6.4422. The best row is the truncated one, on both.

And p is an interpolant with named ends: **p=1 is RoPE and p=0 is NoPE**. The
paper's own summary table is three lines — NoPE is semantic but not
positional, RoPE is positional but not semantic, p-RoPE is both.

**It explains the base-wavelength trick.** Raising θ from 10,000 to 500,000,
introduced by Code Llama and adopted by Llama 3, is a blunt version of the
same move: it pushes the fragile low-frequency channels toward being
distance-agnostic. A widely copied hyperparameter turns out to have a
mechanism, and a cleaner substitute.

## Standing in the anthology

**This is the missing middle of the positional line.** [LIT-045](LIT-045.md) proposed
rotation, [LIT-207](LIT-207.md) argued the rotation is unnecessary, and this measures which
parts of it do what — then builds the dial between them. Filed as extending
[LIT-045](LIT-045.md) and compared against [LIT-207](LIT-207.md), which is what it is.

It also supplies the mechanism three notes here were reasoning around
without. [LIT-193](LIT-193.md) rescales per wavelength on the argument that dimensions
which never complete a rotation behave differently from ones that do; this
says what each band is *for*. [SOTA-151](../practices.d/SOTA-151.md)'s whole subject is what to do when
RoPE's frequencies do not survive a longer context; Theorem 6.1 is why they
do not.

**One finding cuts against [LIT-207](LIT-207.md) directly**, and the record should hold
both rather than pick. Kazemnejad et al. prove a decoder-only transformer
without positional encoding can *represent* absolute and relative position.
This paper finds NoPE cannot build the robust positional-attention heads
RoPE's high frequencies allow — representable and learnable are not the same
claim, and the disagreement is about the second. It is also consistent with
why the NoPE designs that work in practice ([LIT-208](LIT-208.md), [LIT-209](LIT-209.md), [LIT-133](LIT-133.md)) all
pair NoPE global layers with something local that has the positional job:
they are supplying exactly what this paper says NoPE cannot construct.

**And it is in apparent tension with [LIT-208](LIT-208.md), which resolves.** Cohere found
that raising θ from 10,000 to 4 million *damaged* long-context retrieval;
this explains why raising it helps. Both hold: Cohere measured needle
retrieval in a hybrid whose NoPE layers do the retrieving and are disrupted
by wide RoPE neighbours, while this measured short-context perplexity in a
pure-RoPE model. The two are not answering the same question, and noticing
that is the reason to hold both.
