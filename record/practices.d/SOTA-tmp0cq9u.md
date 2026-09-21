---
status: Active
consensus: unassessed
consensus_note: >-
  Nobody has assessed where the field stands on this, and the honest reading
  of the two papers here is that the field does not follow it: one quotes its
  headline rFID from a token count its own phrasing does not name, and the
  other compares at matched token count while its tokens carry five
  unquantized floats each. The practice is `Active` because the measurement
  supporting it is unambiguous, not because anyone has counted who complies.
title: 'State the token count and input resolution beside any reconstruction FID, and compare tokenizers only at equal rate'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-21'
source:
- LIT-tmpflmiq
- LIT-494
introduced_by:
- LIT-tmpflmiq
implementations: []
summary: >-
  Sun et al. (2024), [LIT-tmpflmiq](../literature.d/LIT-tmpflmiq.md) — the **same tokenizer** at
  downsample 16 scores rFID **2.19, 0.94 and 0.70** on 256, 576 and 1024
  tokens, all evaluated on `256×256` reconstructions. A three-fold range from
  a knob that is not the tokenizer. Two papers in this line then quote
  reconstruction numbers whose rate a reader cannot recover from the sentence
  they appear in.
---

# SOTA-tmp0cq9u: State the token count and input resolution beside any reconstruction FID, and compare tokenizers only at equal rate

## Source

Sun, Jiang, Chen, Zhang, Peng, Luo and Yuan (2024),
[LIT-tmpflmiq](../literature.d/LIT-tmpflmiq.md) — whose Table 3 is the measurement — with
Dong et al. (2025), [LIT-494](../literature.d/LIT-494.md) as the second case.

## When this applies

You are reporting, reading or comparing a reconstruction metric for a
tokenizer or autoencoder — rFID, PSNR, SSIM, anything scored on decoded
output. It applies with equal force to the numbers you publish and the
baselines you quote.

## Why it is needed

The same LlamaGen tokenizer, unchanged, on ImageNet 50k validation, with every
reconstruction resized to `256×256` before scoring:

| downsample | input | tokens | rFID |
|---|---|---|---|
| 16 | 256 | 256 (16×16) | 2.19 |
| 16 | 384 | 576 (24×24) | **0.94** |
| 16 | 512 | 1024 (32×32) | **0.70** |
| 8 | 256 | 1024 (32×32) | 0.59 |
| 8 | 384 | 2304 (48×48) | 0.37 |

Three-fold in rFID, one model, no retraining. "Downsample ratio 16" pins none
of it, because the ratio and the input size together determine the token
count and only the token count is the rate.

## Do this

1. **Report the token count and the input resolution**, not only the
   downsample ratio. `f = 16` at `256×256` and `f = 16` at `384×384` are
   different operating points that differ by more than a factor of two in
   rFID.
2. **Say what the reconstruction was resized to before scoring.** LlamaGen
   resizes everything to `256×256`, which is why a 576-token encoding of a
   larger image can beat a 256-token encoding of the same content — it is
   spending more tokens on a picture that gets shrunk before measurement.
3. **Count everything a token carries.** A codebook index at size 1024 is 10
   bits. If your token also carries continuous side information, that is part
   of the rate and belongs in the comparison.
4. **When quoting a baseline, quote the row that matches your rate**, and say
   which row it is.

## The two failures this is drawn from

**Quoting the favourable row without naming it.** LlamaGen's abstract offers
"an image tokenizer with downsample ratio of 16, reconstruction quality of
0.94 rFID". Every clause is true. A reader maps "downsample 16" to a `256×256`
image and gets 256 tokens, whose number is 2.19. The 0.94 is the 576-token
row. §4's prose gives the same pair as 2.43 and 0.99, matching neither the
abstract nor Table 3 — three versions of one comparison.

**Matching the count and missing the rate.** [LIT-494](../literature.d/LIT-494.md)
compares at equal token count and says so plainly, quoting LlamaGen at the
correct 2.19 row. But each of its tokens is an index *plus* five continuous
parameters — roughly 80 further bits at fp16 against the index's 10 — so the
comparison is matched on the quantity the paper controlled and unmatched on
the quantity that determines the answer. Neither paper computes bits per
image.

## Conditions

**This is a reporting discipline, not a finding about tokenizers.** It says
what a number must carry to be interpretable. It does not say any of the
numbers above are wrong: every one is correctly measured, and the source
publishes the table that makes the sensitivity visible.

**"Equal rate" is not always computable.** A token carrying continuous
parameters has a rate that depends on the precision those parameters actually
need, which nobody has measured for the one case here. Where the rate cannot
be computed, say so — that is still more than either source does.

**rFID has its own instabilities** — sample count, resizing, the Inception
weights — that this practice does not address and that do not go away once the
rate is stated.

**One measurement, two illustrations.** Table 3 is the evidence and it comes
from a single paper on a single dataset. The second source demonstrates the
failure rather than replicating the measurement. A sweep of this kind on a
different tokenizer family is what would make the size of the effect, rather
than its existence, something the record could state.
