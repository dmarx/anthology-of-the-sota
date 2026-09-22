---
status: Read
paper: LIT-tmpzz9pi
title: 'A proved bound under the entropy-collapse observation, and a reparameterization that removes four crutches'
version: 1
date: '2026-09-22'
summary: >-
  Read on its own merits after being triaged past once. The record already
  held the failure this paper is about and two remedies for it, and had
  neither the inequality that makes the failure inevitable nor this third
  remedy. The accuracy numbers are nearly flat; what changes is how many
  hyperparameters have to be right.
---
<!-- inactive-ok-file: THEORY-tmp4mah6 SOTA-122 SOTA-282 — all Proposed.
     The two practices are named as the nearest antecedents in a paragraph
     saying nobody has compared them; the theory is this reading's own
     account, filed in the same contribution. -->

# NOTE-tmp4pghv: A proved bound under the entropy-collapse observation, and a reparameterization that removes four crutches

## Contribution

Track attention entropy per head through training, observe that pathologically
low entropy and training instability arrive together across architectures and
modalities, prove that low entropy is forced by a large spectral norm, and
then reparameterize every linear layer so the spectral norm cannot run away.

## Key results

**Theorem 3.1.** With `σ = ‖W_K W_Q^T‖₂·‖XX^T‖₂`, the per-row attention
entropy obeys

    Ent(A_i) ≥ log(1 + (T−1)β) + σ√(T(T−1))·β / (1 + (T−1)β),  β = exp(−σ√(T/(T−1)))

so for large `σ` and `T` the minimum attainable entropy behaves like
`Ω(Tσe^{−σ})` — exponential decay in the spectral norm. The bound is tight:
inputs and weights attaining it exist.

**Proposition 3.2.** Model the stochastic gradient as `g = µ + ε` and take
Adam's idealized update `Δ = E[g]/√E[g²]`. Then `σ(Δ)` is bounded below by
something growing like `√w` in the width. Adaptive optimizers drive spectral
norms up, and faster in wider matrices — which is why the problem shows up at
scale.

**σReparam.** `Ŵ = γ·W/σ(W)`, `γ` scalar, learnable, initialized to 1, `σ(W)`
by power iteration on the parameters. Two matrix-vector products per step, no
per-activation cost, and `Ŵ` can be computed once and frozen at inference. The
claim is not that it constrains the model space — it does not, since `γ` is
free — but that it decouples the update rate of the spectral norm from the
matrix's dimensionality.

**ImageNet-1k, ViT-B, and the crutches removed:**

| | DeiT (B) | σReparam (B) | SN (B) | WN (B) |
|---|---|---|---|---|
| Top-1 | 81.8 | **82.2** | 69.81 | 77.51 |
| pre-LN | yes | **no** | no | yes |
| LR warmup | yes | **no** | no | no |
| weight decay | yes | **no** | no | no |
| optimizer | Adam | **LARS** | LARS | Adam |

**The ablation is the load-bearing row.** Spectral normalization without the
learned scalar gives **69.81%** — a 12-point collapse. WeightNorm gives 77.51
and diverges immediately without pre-LN. The `γ` is the method.

**Breadth.** Machine translation on WMT'17 En-De at 6, 18, 50 and 100 layers
in post-LN and DeepNorm configurations, 3 seeds. Speech recognition on
100h LibriSpeech, where a well-tuned post-LN baseline is still the best single
number (5.9 dev-clean / 17.7 dev-other) and σReparam variants land at 6.1–6.4
/ 17.8–19.4 — and the authors claim the first ASR transformer trained without
warmup and with plain SGD.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Attention entropy is lower-bounded, falling exponentially in `σ` | strong | proved, and tight |
| C2 | Adaptive optimizers grow spectral norms with width | moderate | proposition under idealized-update assumptions |
| C3 | Entropy collapse and instability co-occur | strong as correlation | five settings, figures throughout |
| C4 | Entropy collapse *causes* instability | weaker than the paper's framing | the intervention helps, but C4 is not separated from "σReparam helps for other reasons" |
| C5 | σReparam removes warmup, weight decay, pre-LN and adaptive optimizers | strong | Table 1 and the ASR and MT sections |
| C6 | The learnable scalar is essential | strong | 82.2 against 69.81 |

## Limitations

**The accuracy case is thin and the paper does not oversell it.** 81.8 → 82.2
on ViT-B; on ASR the tuned baseline wins. The result is robustness, not
quality, and reading it as a quality method would be reading it wrong.

**C4 is the soft spot.** Preventing entropy collapse and stabilizing training
co-occur under an intervention that changes the whole optimization geometry.
Nothing isolates entropy as the causal channel — an intervention that fixed
entropy without touching spectral norms would, and does not exist here.

**Pre-2023 scale.** ViT-B/L/H, 100-layer MT models, 100h LibriSpeech. Nothing
at language-model pretraining scale.

**Power iteration is an approximation**, with the iteration count unreported
in the main text.

## Bearing on the record

**The record held the failure and two remedies; this is the inequality and a
third remedy.** [SOTA-192](../practices.d/SOTA-192.md) normalizes queries and keys,
[SOTA-131](../practices.d/SOTA-131.md) clips the weights reactively. Both are stated on the
observation that logits grow and the softmax saturates. Theorem 3.1 is why
that is not bad luck, and σReparam acts on every linear layer instead of on
attention alone.

**It is the nearest antecedent to two things already filed.**
[SOTA-122](../practices.d/SOTA-122.md) attaches learnable multipliers so norms are learned rather
than left to the learning rate and weight decay; [SOTA-282](../practices.d/SOTA-282.md) puts
matrices on the unit hypersphere with a learned step size. σReparam is the
same move — strip the scale, learn it back — at the level of the spectral norm.
None of the three cites the others in this record's reading, and nobody has
compared them.

**Its account is contested by [LIT-tmp8a9ww](../literature.d/LIT-tmp8a9ww.md)**, which exhibits a
stable network in a state the entropy criterion says should crash. That
dispute is live and both sides are filed.

**Warmup, counted.** This is one of three papers in this cluster that remove
learning-rate warmup by controlling the spectrum, by three unrelated
mechanisms. The tempting move is to file the synthesis — warmup is a
workaround for uncontrolled spectral growth — as a theory. It is not filed,
because no paper here claims it and a theory sourced to papers that do not
make its claim is the failure [DP-010](../../docs/design-principles.md#dp-10) names. Recorded in prose in
all three documents instead.

## Open questions

- **Does an entropy-only intervention stabilize training?** That is the
  experiment separating C3 from C4, and neither this paper nor its critic runs
  it.
- **σReparam against QK-norm against QK-clip.** Three remedies, one invariant,
  no comparison. The cheapest useful experiment in this cluster.
- **What happens at pretraining scale?** Every result here predates the scales
  at which [SOTA-192](../practices.d/SOTA-192.md)'s failure became famous.
