---
status: Read
paper: LIT-tmp326fh
title: 'The observation outlived the method, and it is the observation the record needed'
version: 1
date: '2026-09-22'
summary: >-
  Read for one figure. The record holds two practices resting on attention
  being low rank and held no source for the claim; the record also already
  holds the verdict that this paper's *method* was overtaken. Those are
  different things and the reading keeps them apart.
---

# NOTE-tmpqs6fj: The observation outlived the method, and it is the observation the record needed

## Contribution

Two halves that have had very different lifespans. An empirical and
theoretical case that the self-attention matrix is approximately low rank; and
a method exploiting it to get `O(n)` attention.

## Key results

**The spectrum measurement.** SVD of the context mapping matrix `P` across
every layer and head of RoBERTa-base (12 layers) and RoBERTa-large (24), with
`n = 512`, averaged over 10k sentences, on masked language modelling over
Wiki103 and classification over IMDB. Normalized cumulative singular value
shows a long-tail distribution **across each layer, head and task**.

**Depth dependence.** A heatmap of the normalized cumulative singular value at
the **128th of 512** singular values, per layer and head: higher layers are
more skewed. More of the mass sits in the top directions the deeper you go, so
the effective rank falls with depth.

**Theorem 1.** For any `Q, K, V` and any column `w` of `VW_V`, there exists
`P̃` with `rank(P̃) = Θ(log n)` and
`Pr(‖P̃wᵀ − Pwᵀ‖ < ε‖Pwᵀ‖) > 1 − o(1)`. A Johnson-Lindenstrauss argument: the
guarantee is per-column and in probability, not a statement that `P` *is* low
rank.

**The method and its complexity claim.** Project keys and values to a fixed
`k`, independent of `n`. `O(n)` time and space, against `O(n²)` for the
transformer, `O(n√n)` for Sparse Transformer and `O(n log n)` for Reformer.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The attention matrix has a long-tail spectrum | strong | two model sizes, two tasks, every layer and head, 10k sentences |
| C2 | Effective rank falls with depth | strong for these models | the 128-of-512 heatmap |
| C3 | A `Θ(log n)` approximation exists | proved, with the caveat that it is per-column and probabilistic | Theorem 1 |
| C4 | The method matches full attention | moderate | three GLUE tasks plus IMDB |
| C5 | `O(n)` is the right thing to optimize | **overtaken** | the record's own [NOTE-005](NOTE-005.md) |

## Limitations

**Theorem 1 is weaker than the slogan.** "Self-attention is low rank" is the
section heading; what is proved is that for each column vector there exists a
rank-`Θ(log n)` matrix approximating that column's image with high
probability. That is not the same as `P` being globally well approximated at
that rank, and the empirical spectrum is doing more work than the theorem.

**Two models, one family.** RoBERTa-base and RoBERTa-large — the same
architecture at two sizes.

**`n = 512`.** The whole argument is about long sequences and the measurement
is at the length where quadratic attention was not yet the problem.

**The complexity claim is the part the field moved past.** Asymptotic
per-layer cost turned out to be the wrong objective when the real constraint
was memory traffic. The measurement is untouched by that.

## Bearing on the record

**Two practices stood on this and had no source for it.**
[SOTA-184](../practices.d/SOTA-184.md) trains a low-rank update to each weight matrix;
[SOTA-147](../practices.d/SOTA-147.md) compresses the KV cache into a shared latent. Both assume
attention carries usable low-rank structure. The assumption now has the
measurement behind it, with its conditions — one model family, `n = 512`, and
a theorem narrower than its heading.

**It is the empirical half of a pair completed three years later.**
[LIT-528](../literature.d/LIT-528.md) proves the attention matrix converges to a low-rank
Boolean limit under fixed-weight dynamics, and its own remark is that in
Linformer and LoRA the low-rank structure is *imposed rather than extracted*.
Reading them together: this measured it, that derived it, and the derivation
came with conditions the measurement could not see.

**The record's existing verdict is about the method and stays that way.**
[NOTE-005](NOTE-005.md) has FlashAttention undermining this literature's premise by
showing the cost model was wrong. That is a verdict on `O(n)` being the right
target, not on the spectrum. Keeping the two apart is why this is filed
`Active`.

**And it sits against [LIT-tmpcv53l](../literature.d/LIT-tmpcv53l.md) in a way neither paper
notices.** Linformer measures `P` as low rank and treats that as an
opportunity. Dong et al. proves `P` driving the representation to rank 1 is a
pathology that skip connections exist to prevent. Same structural fact, read as
a feature by one and a failure by the other, with the difference being whether
you are compressing the matrix or passing information through it. Neither
cites the other on this point, and the record is not joining them beyond
saying so.

## Open questions

- **Does the long-tail spectrum hold at the lengths that motivated it?** The
  measurement is at `n = 512` and the argument is about long sequences.
- **Is the depth trend the same phenomenon as the weight-spectrum depth trend?**
  [LIT-519](../literature.d/LIT-519.md) finds effective-rank entropy of *weights* falling in
  the last blocks; this finds the *attention matrix* lower rank in higher
  layers. Two different matrices, same direction, and nobody has asked whether
  one causes the other.
