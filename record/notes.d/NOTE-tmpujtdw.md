---
status: Read
paper: LIT-tmpglyct
title: 'SVDQuant: a low-rank branch on the weights, not on the error'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist. The idea that travels is an ordering: decompose
  the weights and quantize the residual, rather than quantize and then patch
  the error. Two propositions and Eckart-Young say why, and a published method
  that does it the other way round is the control.
---

<!-- inactive-ok-file: SOTA-234 — Proposed, named in a list of the
     quantization practices this paper's error bound maps, to say what each
     one acts on. A survey of neighbours, not a recommendation relied on. -->

# NOTE-tmpujtdw: SVDQuant: a low-rank branch on the weights, not on the error

## Contribution

4-bit weights **and** activations for diffusion transformers, with the
arithmetic speedup rather than only the memory saving. Three moves: smooth
outliers from activations into weights; peel the top singular directions of
the smoothed weight into a 16-bit rank-32 branch and quantize the residual;
fuse that branch's kernels into the low-bit ones so it costs nothing.

## Key results

**The bound that motivates it.** Proposition 4.1 bounds a layer's output error
by four quantities — `‖W‖_F`, `‖X‖_F`, `‖W − Q(W)‖_F`, `‖X − Q(X)‖_F`. The
magnitudes are levers alongside the rounding errors, which is the step most
treatments skip. Proposition 4.2 bounds a matrix's rounding error by its own
magnitude, so shrinking the input to the quantizer shrinks both terms.
Eckart-Young makes the truncated SVD the optimal rank-`r` way to shrink it:
`L₁ = UΣ_{:,:r}`, `L₂ = V_{:r,:}`.

**Figure 5 is the empirical premise.** Singular values of `W` are "highly
imbalanced"; after smoothing, the first 32 of `Ŵ` "exhibit a steep drop, while
the remaining values are much more gradual". Rank 32 therefore removes a large
share of the magnitude.

**The control is a published method doing it one step later.** LoRC puts a
low-rank branch on the quantization *error*. The paper's explanation is that
quantization errors "exhibit a well-spread distribution of singular values",
so low-rank compensation captures little. The ablation ordering on PixArt-Σ
matches: naïve quantization and SVD-only both poor, smoothing alone slightly
better, LoRC suboptimal, decompose-then-quantize much better, and adding
smoothing on top better again.

**The systems half, quantified.** A rank-32 branch run independently adds
**57%** latency, from the extra 16-bit read in Down Projection and the extra
16-bit write in Up Projection. Nunchaku fuses Down Projection with Quantize
(shared input) and Up Projection with the 4-bit compute (shared output).

**What the system reaches.** 3.5× memory on 12B FLUX.1; 3.0× over W4A16 on a
16GB laptop 4090 with INT4; 3.1× on an RTX 5090 with NVFP4; PSNR 21.5 on
FLUX.1-dev with NVFP4. Rank 16 at 8 bits, rank 32 at 4. INT4 group size 64
with 16-bit scales; NVFP4 group size 16 with FP8 scales. Residual weights
quantized with GPTQ rather than round-to-nearest.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Decomposing the weights and quantizing the residual beats compensating the quantization error | **strong** | two propositions with proofs, Eckart-Young, and an ablation against LoRC as the control |
| C2 | The low-rank branch is free only if fused | strong | 57% measured overhead unfused, on the paper's own hardware |
| C3 | Weight spectra are steep and quantization-error spectra are flat | moderate | the first is plotted (Figure 5); the second is asserted and used, not plotted |
| C4 | 4-bit quality matches 16-bit | **overstated in one place** | PSNR and LPIPS support "close"; on FLUX.1-dev the 4-bit model *exceeds* BF16 on Image Reward, which is a claim about the metric |

## Limitations

**Diffusion only, and image only.** SDXL, PixArt-Σ and FLUX.1. The activation
outlier structure that most of the quantization literature argues about is a
language-model phenomenon, and nothing here touches it.

**The speedups are the engine's as much as the method's.** Measured with the
authors' own fused kernels against a W4A16 baseline. This is disclosed clearly
and it means the quantization contribution and the systems contribution cannot
be separated from the headline numbers — the 57% figure is what lets a reader
see the split at all.

**The error spectrum is inferred.** The claim that `W − Q(W)` has well-spread
singular values is the load-bearing reason LoRC underperforms, and it is
stated rather than plotted beside Figure 5. One line of code away.

**Smoothing and decomposition are entangled.** Both change `Ŵ`'s spectrum and
the ablation shows the pair beating either, but nothing says how much of the
exploitable steepness was in `W` already.

**A 4-bit model beating its own BF16 source should not be reported as
preference.** The source writes that exceeding BF16 on Image Reward suggests
"stronger human preference". The cheaper explanation is that Image Reward is a
learned model with its own biases, and the other metrics do not invert.

## Bearing on the record

**A mechanism the quantization cluster did not have.** [SOTA-185](../practices.d/SOTA-185.md)
compensates rounding error into not-yet-quantized columns; [SOTA-163](../practices.d/SOTA-163.md)
shrinks a scale's blast radius; [SOTA-234](../practices.d/SOTA-234.md) trains in the target format
instead. None removes magnitude before quantizing. Proposition 4.1's four
terms are a useful map of that cluster: these act on different terms of one
bound and compose rather than compete, which is why the source itself runs
GPTQ on its residual.

**Superficially [SOTA-230](../practices.d/SOTA-230.md), and opposite in purpose.** QLoRA also puts a
16-bit low-rank side beside a 4-bit base. There the branch carries new task
information into a frozen base; here it carries existing weight magnitude away
from the quantizer and learns nothing. The source names the distinction
itself: that line targets compression or fine-tuning, quantizes weights only,
and therefore yields no speedup.

**The practice states two halves as one instruction**, which is unusual here
and is what the 57% number earns. A reader who takes the decomposition and
leaves the fusion has implemented something slower than where they started.

## Open questions

- **Do weight spectra stay steep outside diffusion?** The whole account rests
  on it, it is plotted once, and the measurement is cheap on any model this
  record already holds.
- **How much steepness does smoothing create versus reveal?** Plot the
  spectrum of `W` and `Ŵ` at matched scale and the split is immediate.
- **Does the ordering argument apply to pruning?** The same bound says
  magnitude matters; whether removing magnitude before a sparsity mask helps
  the way it helps before a quantizer is untested and is the nearest
  generalization.
