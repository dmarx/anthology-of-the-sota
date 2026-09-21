---
number: 221
status: Read
formerly:
- NOTE-tmp04rue
paper: LIT-472
title: 'nGPT'
version: 1
date: '2026-09-21'
summary: >-
  Reading it: the headline is 4–20× and the footnote is 60–80% more time per
  step, so the honest wall-clock figure is roughly 5.5× at 4k. Still large.
  The part that generalises beyond this architecture is smaller and more
  interesting — that a matrix's norm is currently an accident of the learning
  rate and weight decay, and does not have to be.
---

<!-- inactive-ok-file: SOTA-122 — Proposed, cited in Connections as the other
     unreplicated arrival at this diagnosis; the reading's observation is that
     two groups reached it independently, which needs both to be unsettled -->

# NOTE-221: nGPT

## Contribution

A transformer in which nothing is ever off the unit sphere. Before it, the
sphere argument existed in representation learning — face verification, VAE
latents, contrastive uniformity — and normalization inside transformers was
a per-layer patch applied wherever it seemed to help. This puts every matrix,
every embedding and every hidden state on one sphere at once and shows the
consequences compose: normalization layers become redundant, weight decay has
nothing left to do, and the residual stream becomes a sequence of steps whose
sizes you can read off as learned parameters.

What is true afterwards that was not before: the residual update's magnitude
is an explicit, inspectable per-dimension quantity rather than an emergent
property of initialization and optimizer state.

## Key insight

Normalizing everything is not the insight — normalizing everything **and then
putting the scale back where it was load-bearing** is. The paper says this
directly: constraining the inputs of non-linear units is what would have
broken, so `s_u`, `s_v`, `s_qk` and `s_z` exist to restore exactly the
degrees of freedom the normalization removed and no others.

That framing also explains why the ablations are so flat. If the scaling
factors are compensation rather than mechanism, fixing them or sharing one
globally should cost little. It does.

## Assumptions

- **The optimizer's copy of the parameters is normalized too.** Named by the
  authors as a common bug, which means this is a real assumption rather than
  a detail — the method is not "add a normalization to the forward pass".
- **Learning rate is the only tuned hyperparameter**, for both arms.
- **RoPE unchanged**, base 10000; the length results come without touching it.
- **bf16 throughout**, on a 32k LLaMA-2 tokenizer and OpenWebText.
- **Parameter counts matched** to within 0.4M between arms.

## Key results

- 1B, 4k context: nGPT at 20k iterations = GPT at 200k iterations.
- 4× / 10× / 20× fewer tokens at 1k / 4k / 8k context.
- Step time +80% (4k), +60% (8k).
- `α_A` ≈ 0.25 → 0.20 and `α_M` ≈ 0.37 → 0.32 going 0.5B → 1B.
- GPT attention matrices show higher condition numbers and singular-value
  spectra consistent with rank deficiency; renormalizing GPT's matrices post
  hoc narrows but does not close the gap.
- Ablation: drop QK-norm → +0.12% loss, −12% step time. LERP → SLERP →
  −0.08% loss, +10% step time.

## Claims

Two, and they are very different in strength.

**The engineering claim** — this recipe reaches a given loss in fewer tokens —
is measured, at two sizes and three context lengths, with a tuned baseline.
It is as good as a single-group result gets.

**The interpretive claim** — that the network *is* a variable-metric optimizer
on the sphere, with blocks supplying gradients and `α` supplying step sizes —
is a reframing, not a test. Nothing here shows that this reading is why the
training is faster. It is a good frame and it earns the paper its title; it
is not evidence.

## Method

Two arms, same parameter count, LR swept for both; validation loss against
tokens at three context lengths and two sizes; downstream task averages;
post-hoc spectral inspection of trained matrices.

## Concepts

*Eigen learning rates* — the learnable per-dimension `α` on each residual
update, read as the diagonal of a variable-metric matrix. *Retraction*, from
Riemannian optimization, for the normalization after each update.

## Connections

- [SOTA-122](../practices.d/SOTA-122.md) is the record's other argument that a weight matrix's norm
  should be managed on purpose rather than left to the learning rate and
  weight decay. Different remedy, same diagnosis, different groups — and
  neither cites the other.
- [SOTA-008](../practices.d/SOTA-008.md) and [SOTA-009](../practices.d/SOTA-009.md) recommend warmup; this removes it.
  [SOTA-120](../practices.d/SOTA-120.md) recommends decoupled weight decay; this removes that too. Not a
  contradiction — a different architecture with a stated reason — but the
  conditions on all three now have an architecture they do not cover.
- [SOTA-032](../practices.d/SOTA-032.md) (pre-norm placement) is the question this dissolves rather
  than answers: with no normalization layers there is no placement to choose.

## Bearing on the record

It supports one practice, `Proposed` and `unreplicated`. The number that
should not enter the record unqualified is "4 to 20× faster", because the
paper's own footnote makes the wall-clock figure roughly half that and the
qualification is one sentence away from the headline.

## Limitations

**Scale.** 0.5B and 1B, on a corpus the authors call not of the highest
quality, with their own conclusion asking for larger sizes and real datasets.
The record's training-recipe practices are mostly argued at 10B–1T; this is
two orders below.

**The overhead is promised away, not measured away.** "Can be reduced after
code optimization" and "expected to further reduce" are both forward-looking.
Nobody has published the optimized version.

**The largest configuration needed a new knob.** 1B at 8k required raising
Adam's `ε` on `α` to 0.1. Two hyperparameters were removed and one appeared,
at the setting closest to where this would actually be used.

**The condition-number evidence is correlational.** GPT's matrices are worse
conditioned and nGPT trains faster; nothing connects the two causally, and
the paper does not claim it does.

**Growth with context length is unexplained.** 4× → 10× → 20× across 1k → 4k
→ 8k is the most striking number in the paper and gets no account at all. It
could be the mechanism or it could be that the baseline degrades with context
for unrelated reasons.

## Open questions

- Does the gap survive at 7B+ and on a modern data mixture? This is the whole
  question, and the paper agrees.
- Is the speedup the sphere, or the learnable per-dimension residual step
  size? Those are separable — `α` could be added to an ordinary pre-norm
  transformer — and nobody has separated them.
- Does the removal of warmup survive large-batch training? [SOTA-008](../practices.d/SOTA-008.md)'s claim
  is specifically about large batch size, and global batch 512 at 1B is not
  the regime that motivated it.
