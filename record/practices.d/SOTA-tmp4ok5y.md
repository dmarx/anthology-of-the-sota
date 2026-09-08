---
status: Proposed
promote_when: >-
  A pretraining report above 2B that truncates the rotary frequencies and
  says so, or an independent group running p-RoPE against a base-rescaled
  RoPE at matched tuning and long context. What would not move it: another
  paper raising the base wavelength and reporting it works, which this
  explains as a blunt version of the same move rather than a rival to it.
consensus: unreplicated
consensus_note: >-
  One group, one paper, 2B. The alternative it argues against — raising the
  base wavelength — is what the field actually does, adopted from Code Llama
  through Llama 3 and everything since, on no mechanism at all until this
  paper supplied one.
title: "Truncate the rotary encoding's low frequencies rather than rescaling its base"
version: 1
tags:
- attention-techniques
date: '2026-09-08'
published: '2024-10-01'
source:
- LIT-210
implementations: []
summary: >-
  Barbero et al. (2024), [LIT-210](../literature.d/LIT-210.md) — RoPE's high frequencies build positional
  attention heads and its low frequencies carry semantics that provably
  cannot stay robust over long context. Keeping a fraction p of the
  frequencies holds performance and at 2B improves it; p=1 is RoPE and p=0 is
  NoPE, so the practice is a dial between two things the record already
  holds.
---

# SOTA-tmp4ok5y: Truncate the rotary encoding's low frequencies rather than rescaling its base

## Source

Barbero et al. (2024), [LIT-210](../literature.d/LIT-210.md) — [ARXIV-2410.06205](https://arxiv.org/abs/2410.06205).

**The justification everyone repeats for RoPE is wrong.** The original
argument was that the encoding helps because attention decays with relative
distance. That holds only for queries and keys already aligned, or constant
all-ones vectors; for Gaussian ones, misaligned pairs can have their dot
product *increase* with distance. The paper proves the sharp version: given
any key, a query exists making RoPE's contribution maximal at any chosen
relative distance, however large. Whatever RoPE does for a model, it is not
enforcing locality.

**The frequency band does two different jobs**, and the split is functional:

- **High frequencies build positional attention heads.** The paper constructs
  one — keys nearly identical, queries a rotation matching one of the highest
  frequencies — proves it robust, and finds a strikingly similar circuit
  inside a released 7B model. Previous-token and diagonal heads are what
  this buys.
- **Low frequencies carry semantics**, in distinct high-norm bands the
  authors read as information channels — and Theorem 6.1 proves those
  channels **cannot** be robust once the context is long.

## What to do, and the numbers

If the low frequencies are the fragile part, truncate them. Keeping a
fraction **p** of RoPE's frequencies holds performance and, at 2B, improves
it. Validation perplexity on Wiki / FlanV2:

| | Wiki | FlanV2 |
|---|---|---|
| NoPE | 4.8594 | 6.6429 |
| RoPE θ=10k | 4.4627 | 6.4429 |
| RoPE θ=500k | 4.4485 | 6.4593 |
| **0.75-RoPE** | **4.4414** | **6.4422** |

The truncated row is best on both.

## Why this is the practice and not the base-rescaling trick

Raising θ from 10,000 to 500,000 — introduced by Code Llama, adopted by Llama
3 and copied everywhere since — is a blunt version of the same move: it
pushes the fragile low-frequency channels toward being distance-agnostic. A
widely copied hyperparameter turns out to have a mechanism, and a cleaner
substitute. That is why the alternative is named here rather than treated as
a rival: it is the same idea, done with less control.

## The dial the record already has both ends of

<!-- inactive-ok-block: SOTA-153 — Proposed, named as the p=0 end of the dial
     this practice interpolates -->
**p=1 is RoPE and p=0 is NoPE.** The record holds [SOTA-151](SOTA-151.md), which rescales
RoPE for a longer context, and [SOTA-153](SOTA-153.md), which drops positional encoding from
a hybrid's global layers. This is the interpolant between them, and the
paper's own summary is three lines: NoPE is semantic but not positional, RoPE
is positional but not semantic, p-RoPE is both.

Filing it makes the two existing practices ends of a continuum rather than
two unrelated recommendations, which is the thing the record could not say
before.

## Conditions, and why this is Proposed

One group, one paper, 2B, and no adopter. The comparison a reader most wants
— p-RoPE against a base-rescaled RoPE at long context and matched tuning —
is not in the paper, which compares at fixed short-context validation.

## Known implementations

- None. The field does the blunt version.
