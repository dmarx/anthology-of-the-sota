---
status: Read
paper: LIT-tmpqknia
title: 'ESSA'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
summary: >-
  The earliest ES-for-LLM paper in this record, and the one that accepted the
  dimensionality objection instead of overturning it: SFT-train LoRA adapters,
  take their SVD, and run CMA-ES over the top singular values only — reaching
  0.80 on GSM8K in under 25 minutes against GRPO's 50+, from 100 examples
  against 5,978, and aligning a 32B model at INT4.
---

# NOTE-tmpuefjy: ESSA

## Contribution

Establishes that ES is practical for LLM post-training by shrinking what it
searches, two months before the line's better-known paper established it by
not shrinking anything. Its durable results are about efficiency rather than
accuracy: sample efficiency, wall-clock, and the ability to train at
inference precision on hardware that cannot backpropagate.

## Key insight

**If ES is bad in high dimensions, the answer might be fewer dimensions rather
than a better ES.** Three nested reductions get from billions of parameters to
a few hundred search variables: LoRA instead of full parameters, SVD of each
adapter instead of the adapter, and the top fraction of singular values
instead of all of them. The second insight is that this only works from a
warm start — the adapters are supervised-fine-tuned first, so the search
begins in a region already adapted to the task format rather than anywhere.

The consequence worth carrying is the one about precision: because ES needs
only forward passes, **training precision can be inference precision**. A
model you can serve is a model you can align, on hardware with no backward
pass at all.

## Assumptions

- **Verifiable accuracy-based rewards**; mathematical reasoning throughout.
- **A strong pre-trained policy to start from** — the paper is explicit that
  ES's sample efficiency here depends on it, and on the SFT warm start.
- **LoRA is expressive enough** for the adaptation being sought, and the SVD
  truncation preserves what matters.
- The GRPO comparison uses different runtimes (vLLM against VERL) and
  deliberately different training-set sizes.

## Key results

- **Wall clock against GRPO**, GSM8K, Qwen2.5-Math-7B, 8 GPUs, identical
  initialization: ESSA (population 192) passes **0.80 accuracy in under 25
  minutes**; GRPO needs **more than 50** to approach it.
- **Sample efficiency**: ESSA used **100 training examples**; GRPO used the
  full **5,978**-example fold. Only the top 40% of singular values were
  trained.
- **Quantized alignment**: Qwen-32B aligned at BF16, INT8 and INT4 with
  population 192, and **INT4 and INT8 slightly outperform BF16** on both
  convergence speed and final accuracy.
- **Rank has an interior optimum**: LoRA ranks 4, 8 and 32 give the fastest
  convergence and highest final accuracy; rank 64 is slower and worse. The
  paper's reading is that a larger search space is harder for ES to explore.
- **Stability**: the paper claims ES removes the need for extensive
  hyperparameter tuning relative to RLHF, which it lists as one of the
  motivating properties.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | ES over a truncated LoRA-SVD subspace aligns LLMs effectively | strong for math reasoning | 7B and 32B, multiple precisions |
| C2 | ESSA converges faster in wall clock than GRPO | moderate | different runtimes and training-set sizes; a convincing demonstration, not a controlled comparison |
| C3 | ESSA is far more sample-efficient than GRPO | moderate | 100 vs 5,978 examples, but the two methods are using the data differently |
| C4 | ES can train at INT4/INT8 without loss | strong | measured, and structurally unsurprising given forward-only |
| C5 | Moderate LoRA rank beats high rank | strong | direct sweep, one model, one dataset |
| C6 | ES suits alignment to human preference | not established, and the authors say so | scalar verifiable fitness only; subjective feedback named as a limitation |

## Method

Train LoRA adapters by supervised fine-tuning on a small labelled set. For
each adapter, SVD-decompose both factors and keep the top `k` diagonal
singular values as the search variables. Run CMA-ES over those, sampling a
population of candidate singular-value vectors from a multivariate normal each
generation and adapting mean and covariance from the fitnesses. Population 192
throughout the headline experiments.

## Concepts

- **Singular-value search** — optimizing only the spectrum of an adapter,
  leaving its singular vectors fixed. What makes the search space a few
  hundred dimensions rather than millions.
- **Warm-started evolutionary search** — SFT first, evolve second; the
  structural move Hyper-ES makes later with GRPO steps in place of SFT.

## Connections

It cites DFO, LoRAHub and GENOME as prior attempts at ES over adapters, and
distinguishes itself by evolving *singular* values specifically, which it
argues makes the black-box optimization interpretable. Its relationship to the
rest of this record's line is chronological rather than genealogical — the
full-parameter work did not build on it. Lineage is on the LIT.

## Recommendations

- **R1** — If ES seems infeasible at your scale, reduce the search dimension
  before abandoning the method, and warm-start it. *Topic:* post-training.
  *Strength:* moderate.
- **R2** — Pick a moderate LoRA rank; more expressivity is not free for a
  population-based search. *Topic:* adaptation. *Strength:* moderate, one
  sweep.
- **R3** — Where gradients are impossible — quantized weights, low-power
  inference hardware — forward-only post-training is available and this is the
  demonstration. *Topic:* post-training. *Strength:* strong, and the most
  distinctive thing in the paper.

## Bearing on the record

Filed as [LIT-tmpqknia](../literature.d/LIT-tmpqknia.md). It carries no relation to the rest of the line
because the later work did not build on it — which is itself the finding: the
record acquired this paper last and it is the earliest, an artifact of
following citations backward from 2026.

<!-- inactive-ok-block: SOTA-154 is Active; named as the practice this paper
     sits outside rather than supports -->
**It does not support [SOTA-154](../practices.d/SOTA-154.md).** That practice recommends ES over the *full*
parameter space in place of policy-gradient RL. This is CMA-ES over a few
hundred SFT-initialized coefficients. Same family, a different recommendation,
and filing it under that practice would have been the easy mistake.

**What it does do is make the subspace approach a line.** [LIT-231](../literature.d/LIT-231.md) argues
from lemmas that full-parameter ES cannot work and searches a gradient-seeded
subspace instead; this did the same thing eighteen months earlier, without the
argument, and reported it working at 7B and 32B. Two independent arrivals at
*seed a low-dimensional subspace, then search it gradient-free* is a better
argument for the approach than either paper's own numbers — and it means the
record's `contested` reading of [SOTA-154](../practices.d/SOTA-154.md) is a live disagreement about
method rather than one group's objection.

## Limitations

Stated: scalar verifiable fitness limits applicability to subjective or sparse
feedback, and efficiency may still degrade at extreme dimensionality without
further reduction. From this reading: the GRPO comparison varies runtime and
data volume alongside the optimizer; no drift or forgetting measurement, though
searching a few hundred coefficients bounds drift by construction — which is
worth noticing given what [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md) says drift scales with.

## Open questions

- **How much of the sample efficiency is the SFT warm start?** No ablation
  without it, and the paper says the initialization is crucial.
- **Does the quantized-training result extend past alignment?** Training at
  INT4 on hardware that cannot backpropagate is the most consequential claim
  here and is demonstrated on one task.
- **Does the subspace approach beat full-parameter ES at 7B and above?** The
  comparison the whole `contested` question turns on, and nobody has run it.
