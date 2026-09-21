---
number: 316
status: Proposed
formerly:
- SOTA-tmpz9mlh
promote_when: >-
  Quality compared at the scale the cost is claimed at: a 7B-or-larger model
  trained both ways to the same token budget, with the final loss and at least
  one downstream metric reported for each, and the iteration counts stated. The
  cost figure should isolate the method — same GPU model on both arms — with
  the hardware-price saving reported separately if at all. What would NOT meet
  it: another economic table on cheaper GPUs, which is evidence about GPU
  pricing.
consensus: unreplicated
consensus_note: >-
  One group, one paper. Block coordinate descent itself is old and its
  convergence on deep networks has been studied by others, which the paper
  cites; what is unreplicated is the claim that partitioning this way at LLM
  scale costs nothing in quality. Nobody outside this group has run it, and
  the field's answer to the same problem is still a low-rank adapter.
title: 'When you are memory-bound rather than time-bound, train all the parameters a block at a time, partitioned on layer boundaries'
version: 1
tags:
- systems-optimization
- training-optimization
date: '2026-09-21'
source:
- LIT-515
introduced_by:
- LIT-515
implementations: []
summary: >-
  Liu et al. (2025), [LIT-515](../literature.d/LIT-515.md) — freeze all but one block of
  layers, train it to local convergence, rotate. Memory falls to roughly the
  active block, so a 7B trains on one A800 where full-parameter needs two, and
  perplexity at 2B matches or beats the full-parameter baseline. The price is
  about **three times the iterations**, which the paper's own table shows and
  its abstract does not.
---

# SOTA-316: When you are memory-bound rather than time-bound, train all the parameters a block at a time, partitioned on layer boundaries

## Source

Liu et al. (2025), [LIT-515](../literature.d/LIT-515.md) — read as [NOTE-260](../notes.d/NOTE-260.md).

## When this applies

You want **every** parameter trained — pretraining from scratch, or a
fine-tune broad enough that a low-rank update will not do it — and the binding
constraint is GPU memory rather than calendar time. If you are time-bound this
practice is the wrong trade, and the next section says why in numbers.

## Do this

**Cut the blocks on layer boundaries.** Block coordinate descent puts no
mathematical constraint on the partition, so the choice is free and should be
made for the kernels: most operators live entirely inside a layer, so freezing
whole layers keeps the optimized paths intact. Partitioning *within* a layer —
updating some fraction of each layer's parameters at once — keeps the same
parameter count but loses the kernel, and the paper's Figure 1 is about
exactly that.

**Train the active block to local convergence, then rotate.** The optimizer
inside a block is unchanged — SGD, AdamW, whatever you were using; the paper
is explicit that this choice is not what matters.

**Size the partition to the memory you have.** Three submodels in all the
paper's experiments, so a third of the parameters update per round. The
memory freed is the optimizer state and gradients of the frozen blocks, which
is where most of the `5.7W` of a full-parameter run goes.

**Expect to pay in steps.** This is the part the abstract omits and the table
states.

| model / data | full-parameter Adam | BCD-Adam |
|---|---|---|
| GPT-2 2B, wiki | 9,968 iters, PPL 96.69 | 28,870 iters, PPL **97.96** |
| GPT-2 2B, alpaca | 9,652 iters, PPL 28.30 | 25,898 iters, PPL **27.85** |
| GPT-2 2B, slimpajama | 9,550 iters, PPL 69.28 | 28,707 iters, PPL **58.82** |
| LLaMA 2B, alpaca | 18,579 iters, PPL 21.06 | 20,076 iters, PPL **21.04** |

Roughly **3× the iterations** for comparable or better perplexity — which is
what a third of the parameters per round buys. The economics only work because
each iteration runs on a smaller, cheaper machine.

## What it buys, and in which currency

**Fewer GPUs, which is where most of the saving is.** 7B: two A800s
full-parameter, **one** with BCD. 2B: three RTX 4090s, **two** with BCD.

**33% of the cost on the same device** (7B, A100/A800). This is the figure
that isolates the method.

**2.6% on RTX 4090 — a different claim.** That number includes the 4090's
hourly cost being about a quarter of an A100's, so it measures the method
*and* the hardware substitution together. Quote it only with that said.

## Why `Proposed`

**Quality is verified at 2B and the cost is claimed at 7B.** The perplexity
comparison runs on ResNets, GPT-2 0.15B and the 2B models; the 7B appears in
the economic experiments, and larger sizes are estimated from single-round
speeds rather than trained. Whether three-block BCD preserves quality at 7B is
the thing to check, and it is not checked.

**Small datasets.** Wikipedia, Alpaca and SlimPajama subsets — the paper calls
them small-scale itself. Perplexity after a short run on a small corpus is
weak evidence that a training procedure scales.

**No seeds.** One run per cell.

## Conditions

**The trade is memory for time, and that is a real cost.** Three times the
iterations on a machine that is cheaper per hour can still be slower in
wall-clock. If a deadline binds, this practice is the wrong answer and
[SOTA-184](SOTA-184.md)'s low-rank update — which does not train every parameter, and
says so — may be the right one.

**It is not a general speedup.** Nothing here says BCD reaches a given loss in
less compute. It says a given loss is reachable on less hardware.

**The partition size is a dial nobody swept here.** Three submodels
throughout, with other settings relegated to an appendix. Whether two or six
changes the quality-versus-steps trade is unmeasured in the main results.

**Convergence is inherited, not shown.** The paper rests on existing proofs
that BCD converges on deep networks and cites them; it does not prove anything
about transformers specifically, and "trains to local convergence per block"
is a schedule whose interaction with modern learning-rate schedules
([SOTA-140](SOTA-140.md)) is not discussed.

## Known implementations

None named beyond the authors' own runs. The datasets are published through
ModelScope.
