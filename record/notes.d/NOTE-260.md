---
number: 260
status: Read
formerly:
- NOTE-tmpyl1mo
paper: LIT-515
title: 'Block coordinate descent: a smaller machine bought with three times the steps'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist as the last of the 5-revisit tier. The method is
  sound and the accounting needs separating: the headline 2.6% mixes the
  method with the price of a 4090, the same-device figure is 33%, and the
  iteration counts in the paper's own Table 2 show BCD paying about 3× the
  steps for the memory it saves.
---

# NOTE-260: Block coordinate descent: a smaller machine bought with three times the steps

## Contribution

Full-parameter training where only one block of parameters is live at a time.
Freeze the rest, train the active block to local convergence, rotate. The
adaptation to deep learning is the partition rule: cut on layer boundaries,
because most operators live entirely inside a layer and a partition that
splits them keeps the parameter count while losing the optimized kernel.

## Key results

**The quality comparison, Table 2** — full-parameter Adam against BCD-Adam:

| model / data | Adam iters | Adam PPL | BCD iters | BCD PPL |
|---|---|---|---|---|
| GPT-2 2B, wiki | 9,968 | 96.69 | 28,870 | 97.96 |
| GPT-2 2B, alpaca | 9,652 | 28.30 | 25,898 | 27.85 |
| GPT-2 2B, slimpajama | 9,550 | 69.28 | 28,707 | **58.82** |
| LLaMA 2B, alpaca | 18,579 | 21.06 | 20,076 | 21.04 |

Comparable or better perplexity, at close to **3× the iterations** on the GPT-2
rows — which is what updating a third of the parameters per round costs. The
LLaMA row is the exception at 1.08×, and the paper does not remark on why.

**The hardware, which is where the money is.** Full-parameter needs two A800s
for 7B, three RTX 4090s for 2B; BCD needs one and two respectively. Memory
freed is the optimizer state and gradients of the frozen blocks — the paper
puts full-parameter at about `5.7W` of memory, `5W` with recomputation.

**Two cost figures that are not the same kind of claim.** 33% on A100/A800 at
7B isolates the method: same device both arms. 2.6% on RTX 4090 does not — the
paper states the 4090's hourly cost is about a quarter of an A100's, so that
number is the method *and* the hardware substitution multiplied together.

**Scope of what was actually trained.** ResNet-8 and ResNet-14 on CIFAR-10 and
CIFAR-100; GPT-2 0.15B on WikiText and WebText2; GPT-2 and LLaMA at 2B and 7B
on Wikipedia, Alpaca and SlimPajama subsets, which the paper calls small-scale.
Costs for 1.6B, 5.4B and 10B are **estimated** from measured single-round
speeds rather than trained.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Layer-boundary partitioning is the right cut | strong, and mostly a priori | operators live inside layers, so any finer cut loses the kernel |
| C2 | BCD reaches comparable quality | moderate at ≤2B | Table 2, one run per cell, small corpora |
| C3 | It cuts same-device cost to ~33% at 7B | moderate | measured, but no quality comparison at 7B |
| C4 | It cuts cost to 2.6% on 4090 | **misleading as stated** | includes a 4× hardware price difference the body discloses and the abstract does not |

## Limitations

**Quality and cost are measured at different scales.** The perplexity table
tops out at 2B; the 7B appears only in the economic experiments. The practice
being recommended is "train a big model on a small machine", and whether the
big model comes out the same is the one thing not shown at the big size.

**Three times the iterations is in the table and not in the abstract.** It is
not concealed — the iteration column is right there — but a reader taking the
headline gets an efficiency claim, and what the paper supports is an
affordability claim.

**No seeds, small corpora, one partition size.** Three submodels throughout,
with other settings in an appendix.

**Convergence is inherited.** The paper cites existing proofs that BCD
converges on deep networks rather than proving anything about transformers,
and "train each block to local convergence" is a schedule whose interaction
with the learning-rate schedules this record recommends elsewhere
([SOTA-140](../practices.d/SOTA-140.md)) is not discussed.

## Bearing on the record

<!-- inactive-ok-block: SOTA-155 — Proposed, named as a near-miss this practice is distinguished from -->
**It sits in a hole between two practices.** [SOTA-184](../practices.d/SOTA-184.md) trains a low-rank
update — cheap, and explicitly not full-parameter. [SOTA-155](../practices.d/SOTA-155.md) distributes
across poorly connected workers — which assumes workers. Neither answers "every
parameter, one small GPU", and the grep for block coordinate descent, layer
freezing and memory-efficient full-parameter training came back empty.

**So the practice is new, and `Proposed`.** The direction is credible and the
mechanism is close to a priori; what is missing is the quality check at the
size the cost claim is made at, which is what the `promote_when` asks for.

**One more instance of a shape this session has been counting, and it does
not extend the count.** Earlier units found reported numbers sensitive to a
choice the report did not state; the Gemini unit found complete disclosure
with a flattering headline anyway. This is the Gemini shape rather than the
first one — the iteration counts and the 4090 pricing are both in the body.
Counted in the practice's conditions, not promoted. [DP-009](../../docs/design-principles.md#dp-9),
[DP-010](../../docs/design-principles.md#dp-10).

## Open questions

- **Does three-block BCD hold quality at 7B?** One run each way at a fixed
  token budget, final loss and one downstream metric. That is the whole gap.
- **What does the partition-count dial do?** Two blocks should cost fewer
  extra steps and save less memory; six the reverse. The trade curve is the
  useful artifact and it is in an appendix at best.
- **Why is the LLaMA row 1.08× iterations when the GPT-2 rows are ~3×?**
  Unremarked, and if it is architectural it is the most interesting thing
  here.
