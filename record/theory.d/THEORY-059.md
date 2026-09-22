---
number: 59
status: Proposed
formerly:
- THEORY-tmpo44nu
promote_when: >-
  The FLAT half measured: the singular value distribution of the quantization
  residual `W − Q(W)`, plotted beside those of `W` and the smoothed `Ŵ` for
  the same matrices, with the rank needed to capture a fixed fraction of each.
  That is the load-bearing premise — it is why applying the low-rank branch
  one step later underperforms — and it is asserted rather than plotted in
  every paper this record holds. What would NOT meet it: another method that
  puts a low-rank branch beside a quantized one and reports better images;
  nor a further measurement of `W`'s spectrum, which v2 records as answered.
title: 'A low-rank branch corrects quantization because weight spectra are steep and quantization-error spectra are flat'
version: 2
history:
- version: 2
  date: '2026-09-22'
  note: >-
    Half the promotion condition is met and the account survives it with a
    qualification it did not carry. Weight-spectrum steepness outside
    diffusion transformers is now measured by four papers across BERT,
    Pythia, Llama-3.1-8B, LLaMA-2 7B/13B, Mistral-7B and eleven GPT-2-style
    checkpoints — but it is strongly NON-UNIFORM by component and by depth,
    which the account stated as though it were a property of weight matrices
    in general. The `promote_when` is narrowed to the half still untouched:
    nobody has plotted the spectrum of `W - Q(W)`. Status unchanged, and the
    reasoning is unchanged; what changes is that the steep case now has a
    name (Marchenko-Pastur plus outliers) and a measured scope.
tags:
- numerics-and-precision
- inference-optimization
date: '2026-09-21'
source:
# LIT-512 is where the account comes from; the propositions and the
# ablation are its. The two added here are where its spectral premise is
# MEASURED outside the source's own model class, which is what the account
# could not survive losing now that it claims generality. Neither proposes
# the account, and the body says so.
- LIT-512
- LIT-517
- LIT-516
explains:
- SOTA-314
summary: >-
  Li et al. (2024), [LIT-512](../literature.d/LIT-512.md) — two propositions bound the
  output error by the *magnitude* of weights and activations, not only by
  their rounding errors. So a rank-`r` branch helps exactly when the thing it
  subtracts has a few dominant singular values. A weight matrix does; a
  quantization error does not, which is why the same trick applied to the
  error rather than the weights underperforms.
---


# THEORY-059: A low-rank branch corrects quantization because weight spectra are steep and quantization-error spectra are flat

## Source

The account is Li, Lin, Zhang, Cai, Li, Guo, Xie, Meng, Zhu and Han (2024),
[LIT-512](../literature.d/LIT-512.md) — read as [NOTE-257](../notes.d/NOTE-257.md). Propositions 4.1
and 4.2, with proofs in the appendix.

Its spectral premise is measured outside that paper's model class by Staats,
Thamm and Rosenow (2024), [LIT-517](../literature.d/LIT-517.md), and Jaiswal et al.
(2024), [LIT-516](../literature.d/LIT-516.md). Neither proposes this account; they are
cited as sources because what the account now claims — that this is how
weight matrices behave, not how diffusion transformer weight matrices behave
— rests on them.

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-314](../practices.d/SOTA-314.md) | absorb outliers into a high-precision low-rank branch taken from the weights, and fuse its kernels | the branch pays off because the weight matrix is nearly low-rank in its largest directions, and it would not pay off if applied one step later |

## The account

The usual mental model of post-training quantization is that the thing to
minimize is the **rounding error** — how far `Q(W)` is from `W`. On that
model, the natural way to use a spare high-precision branch is to have it
approximate the error: compute `W − Q(W)`, take its truncated SVD, add it
back. That is what LoRC does.

Proposition 4.1 says the model is incomplete. The error in the layer's output
is bounded by four quantities, not two: the rounding errors
`‖W − Q(W)‖_F` and `‖X − Q(X)‖_F`, **and the magnitudes** `‖W‖_F` and
`‖X‖_F`. Magnitude is a lever in its own right. Proposition 4.2 closes the
loop: the rounding error of a matrix is itself bounded by that matrix's
magnitude. So shrinking what you hand to the quantizer shrinks both terms at
once.

That makes the question spectral. Subtracting a rank-`r` matrix `L₁L₂` from
`M` reduces `‖M‖_F` by exactly as much as the first `r` singular values
contain — Eckart-Young gives the optimum as the truncated SVD. So the
manoeuvre is worth doing on a matrix whose spectrum is **steep**, and close to
worthless on one whose spectrum is **flat**.

A weight matrix is the steep case. The paper's Figure 5 shows the singular
values of `W` are highly imbalanced, and that after smoothing the first 32 of
`Ŵ` drop steeply while the rest decay gradually — so rank 32 removes a large
share of the magnitude.

A quantization error is the flat case. Rounding is close to independent across
entries, so `W − Q(W)` behaves like a matrix with no preferred directions and
its singular values are well spread. A rank-32 approximation of it captures
almost nothing, which is why applying the low-rank branch to the error
underperforms applying it to the weights.

**So the ordering matters more than the ingredient.** Decompose first and
quantize the residual; do not quantize first and try to patch what is left.
The same components in the other order do not work, and the spectrum is why.

## What the measurement outside diffusion transformers found

`v1` was `Proposed` partly because Figure 5 is diffusion transformer weights
and "weight matrices have steep singular spectra" was plausible beyond that
and not shown beyond it. It has now been shown beyond it, and the answer has
a shape the account did not anticipate.

**The steep case is real, and it has a name.** A trained transformer's
singular spectrum is a Marchenko-Pastur bulk plus a few outliers — exact
agreement with the MP law at initialization, departures after training,
measured on BERT, Pythia-410M and Llama-3.1-8B
([LIT-517](../literature.d/LIT-517.md)). That is what "steep" means here: most
singular values sit in a narrow band and a handful stand above it, so
subtracting the top `r` removes a large share of `‖W‖_F`.

**That also names the flat case, and this is the useful part.** The account
says `W − Q(W)` is flat because rounding is near-independent across entries.
Near-independent entries with finite variance is precisely the hypothesis
whose singular values follow the MP law. So the two cases in this account are
"MP plus outliers" and "MP" — a sharper statement than the account made, and
still not a measurement, because nobody has plotted the residual's spectrum.
That is now the whole of the `promote_when`.

**But it is not a property of weight matrices; it is a property of some of
them.** [LIT-516](../literature.d/LIT-516.md) splits a transformer's matrices by whether
the sorted singular values have a heavy tail. Query, Key and MLP Gate do;
MLP Up, MLP Down and Value do not. Middle blocks resist and the first and
last few give way. At 50% effective-rank reduction on LLaMA-2 7B, `q_proj`
and `k_proj` take over 90% compression while others take almost none — and
choosing one global rank instead costs ~6.4× in perplexity at 30% reduction.
Eleven GPT-2-style checkpoints across six languages agree that concentration
varies systematically with depth, peaking in the residual-writing matrices of
the last few blocks ([LIT-519](../literature.d/LIT-519.md)).

**The shape is stable once it forms**, which is what makes reading it once
meaningful: the trace-normalized spectrum reaches stationarity within roughly
a thousand pretraining steps and holds across GPT-2 and LLaMA, three
schedules, varied weight decay, AdamW and Muon
([LIT-520](../literature.d/LIT-520.md)).

So the account generalizes, and the sentence "a weight matrix is the steep
case" does not. The corrected version is: *some* weight matrices are the steep
case, the difference is large enough to dominate a compression decision, and
which ones is a question you answer per model — which is
[SOTA-318](../practices.d/SOTA-318.md).

## What the measurement also cost this account

**The residual is not obviously the safe part.** The manoeuvre is: peel the
top singular directions into 16 bits, quantize what is left. What is left
includes the *bottom* of the spectrum, and in non-square transformer matrices
the bottom is not noise. Its singular vectors overlap the activation
covariance at 3σ, and zeroing the smallest decile of Llama-3 8B's
Down-Projection costs 41 points of GSM8K — second only to zeroing the largest
decile ([NOTE-263](../notes.d/NOTE-263.md)).

This is not a refutation and should not be read as one. Zeroing a direction is
not quantizing it, the measurement is on language models rather than diffusion
transformers, and [SOTA-314](../practices.d/SOTA-314.md)'s image results are what they are. What it
does is remove an assumption the account was leaning on without stating:
that once the dominant directions are extracted, the remainder is
undifferentiated and its treatment is a matter of average error. On the
evidence now in the record, the remainder has structure, and the account has
nothing to say about it.

## Why still `Proposed`

**The flat half has never been plotted.** The paper states that quantization
errors "exhibit a well-spread distribution of singular values" and infers from
it that LoRC underperforms; this record has not found the spectrum of
`W − Q(W)` plotted beside the others in any of the five sources now attached
to this cluster. The inference is sound, the measurement is one line of code,
and the difference between those two is what `Proposed` is for. It is also the
load-bearing premise — the asymmetry between decomposing-then-quantizing and
quantizing-then-patching rests on it entirely.

**Smoothing and decomposition are still not separated spectrally.** Smoothing
shifts outliers from activations into weights and changes `Ŵ`'s spectrum; the
ablation shows the combination beats either, but nothing reports how much of
the steepness rank-32 exploits was already in `W` and how much smoothing put
there. None of the new measurements touch `Ŵ`, because none of them smooth.

**Nothing has been measured on a diffusion transformer.** Everything in this
section is language models. Whether diffusion transformers show the same
non-uniformity, or the same informative bottom outliers, is unknown — and it
is the model class the practice is actually applied to.

## What it does not say

**It does not say low-rank adapters and this are the same thing.** The
arrangement resembles [SOTA-230](../practices.d/SOTA-230.md) — a 4-bit base with a 16-bit low-rank
side — and the purpose is opposite. There the branch carries *new* task
information and the base is frozen; here it carries *existing* weight
magnitude away from the quantizer and nothing is learned. The source is
explicit that the prior work in that line targets compression or fine-tuning,
uses weight-only quantization, and so yields no speedup.

**It does not say magnitude is the only lever.** Proposition 4.1 has four
terms. Block scaling ([SOTA-163](../practices.d/SOTA-163.md)) and error compensation
([SOTA-185](../practices.d/SOTA-185.md)) act on the other ones, and the source uses GPTQ on the
residual weights, so these compose rather than compete.

**It does not say magnitude order is importance order.** Eckart-Young makes
the truncated SVD the best rank-`r` approximation in Frobenius norm, and this
account is about Frobenius norm throughout — legitimately, because
Propositions 4.1 and 4.2 bound the output error by magnitudes. What it never
claims, and what a reader is likely to supply, is that the directions holding
least magnitude are the ones the model needs least.
[SOTA-317](../practices.d/SOTA-317.md) is the practice about that, and it points the
other way.

**It says nothing about activations beyond the smoothing step.** The account
of why the residual quantizes well is about `W`. The activation side is
handled by moving outliers out of it, and this theory does not explain what
makes that transfer safe.
