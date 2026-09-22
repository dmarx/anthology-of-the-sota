---
number: 272
status: Read
formerly:
- NOTE-tmp582ca
paper: LIT-528
title: 'An idealization that checks its own assumptions against ALBERT, and clusters within a few layers'
version: 1
date: '2026-09-22'
summary: >-
  Read a second time, in full, after being declined on a skim. The decline
  said the `t → ∞` frozen-weights idealization put it too far from a trained
  model to be evidence about one, and that it underwrites no practice. Both
  halves were wrong: the record's own schema says a theory need underwrite
  nothing, and the paper checks its hypotheses on ALBERT, gives the
  discrete-time analogue, and says clustering arrives within a few layers.
---

# NOTE-272: An idealization that checks its own assumptions against ALBERT, and clusters within a few layers

## Contribution

View a transformer as an interacting particle system: tokens are particles,
layers are time, and self-attention is the interaction. With `(Q, K, V)` held
fixed, ask where the particles go. The answer is a classification of limiting
geometries indexed by the spectrum of `V`.

## Key results

**The dynamics.** `ẋᵢ = Σⱼ Pᵢⱼ(t) V xⱼ(t)` with `P` the row-softmax of
`⟨Qxᵢ, Kxⱼ⟩`. Tokens diverge in norm without normalization, so the analysis
runs on `zᵢ(t) = e^{−tV} xᵢ(t)` — a rescaling the authors describe as a
mathematically justified surrogate for layer normalization, and which leaves
`P` unchanged.

**The classification, all proved:**

| value matrix | condition on `Q, K` | limit | theorem |
|---|---|---|---|
| `V = I_d` | `Qᵀ K ≻ 0` | boundary of a convex polytope; generically its **vertices**, and there are far fewer than `n` | 3.1 |
| `λ₁(V) > 0` simple | `⟨Qφ₁, Kφ₁⟩ > 0` | at most **three** parallel hyperplanes, perpendicular to `φ₁` | 4.2 |
| `V` paranormal | `Qᵀ K ≻ 0` | polytope in one subspace, linear subspace in the other | 5.2 |
| `V = −I_d` | `Qᵀ K = I_d` | every token collapses to the origin | 8.5 |

**Theorem 2.1, the low-rank result.** For `d = 1`, `V > 0`, `QK > 0`, and
pairwise distinct initial tokens, `P(t)` converges to a Boolean matrix of the
stated block form — generically **rank 1 or 2** — with doubly exponential rate
off one row. Reading: at most three tokens capture the attention of all but at
most one of the rest.

**The assumptions are tested against a trained model.** Section 11.2:
ALBERT-xlarge-v2, 16 heads, `n = 256`, `d = 128`. Heads 5 and 14 satisfy both
conditions of Definition 4.1, with `⟨Qφ₁, Kφ₁⟩` = **1.3060** and **0.6719**.
The paper states in the same breath that not all sixteen do.

**How generic is the leading-eigenvalue condition?** About **14%** of matrices
from the real Ginibre ensemble at `d = 128`, "known to vanish as `d → ∞`,
albeit very slowly". Also automatic by Perron-Frobenius if every entry of `V`
is positive. The paper reports both the favourable and the unfavourable half.

**Timescale.** Remark 3.3: no rate is proved, but numerically "convergence
happens very quickly — after few layers, most tokens are already clustered".

**Discrete time.** Remarks 1.1 and 3.4 give the forward-Euler iteration and
the rescaled discrete dynamics explicitly, and state the proofs carry through.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Tokens cluster under fixed-weight self-attention | strong, within the model | four theorems covering four spectral regimes |
| C2 | The spectrum of `V` decides the limiting geometry | strong, within the model | the classification is indexed by it |
| C3 | The attention matrix becomes low-rank and Boolean | strong at `d = 1`, conjectural above | Theorem 2.1; Remark 7.9 exhibits a `d = 2` counterexample and the authors expect it holds for almost all initial conditions |
| C4 | The assumptions hold in practice | partial, and honestly reported | 2 of 16 ALBERT heads shown; ~14% of random matrices at `d = 128` |
| C5 | Clustering persists with a feed-forward layer | numerical only | Section 12.2, left as an open problem |
| C6 | Multi-head clustering | open | stated as an open problem |

## Limitations

**Weights are time-independent**, which the paper defends twice: as
mathematical convenience, and by pointing at ALBERT, where cross-layer
parameter sharing is the actual architecture. That is a real defence and it is
narrow — one model family.

**Pure self-attention.** No multi-head, no feed-forward, no layer
normalization. The rescaling substitutes for the last of these, and the first
two are open problems with numerics attached.

**Theorem 2.1 is one-dimensional**, and Remark 7.9 gives the obstruction
directly: at `d = 2`, `n = 2` with `x₁(0) = (1, ε)` and `x₂(0) = (1, −ε)`, both
tokens converge to `(1, 0)` — one cluster — while `P` converges to the
identity, which has rank 2. So the rank of the limit is not the cluster count
in general.

**`Qᵀ K ≻ 0` is not necessary and is not known to be droppable.** Section 12.1
shows the clustering pattern persisting under random `Qᵀ K` violating the
assumption; that is numerics, not a theorem.

**No trained-model forward pass is measured.** The bridge to practice is the
eigenvalue check on ALBERT's weights, not the token trajectories of a real
model on real text.

## Bearing on the record

**It is the trunk under a premise the record already uses.**
[NOTE-105](NOTE-105.md) treats rank collapse of transformer projection matrices as
established, and the record holds neither Dong et al. nor this. This one also
corrects the naive reading: rank collapse into a single tight cluster is what
happens *without* skip connections, and with them the structure is richer —
polytope vertices, hyperplanes, or the origin, depending on `V`.

**It is the theoretical root of an assumption two filed practices stand on.**
The paper names Linformer and LoRA as motivated by the near-low-rank structure
of `P`, and notes that in both the low-rank structure is *imposed* rather than
extracted. Theorem 2.1 extracts it. [SOTA-184](../practices.d/SOTA-184.md) and
[SOTA-147](../practices.d/SOTA-147.md) inherit that assumption without a source for it, and
now have one — with its conditions attached.

**It answers a question the spectral cluster filed this week does not ask.**
Those documents ask what a weight matrix's spectrum does to *training*
stability. This asks what the value matrix's spectrum does to the
*representations*, and gives a classification. Same object, orthogonal
question, no citation in either direction.

**Adjacent to neural collapse**, which the paper names: representations of
different classes forming a tight simplex in late layers. The record holds no
neural-collapse document either.

## Why the first reading was wrong

Recorded because the error is instructive rather than embarrassing.

**"It underwrites no practice the record holds" is not a reason to decline,
and the schema says so in as many words.** `explains` is optional on a theory
precisely because "a finding that underwrites nothing YET is still a finding,
and requiring this would mean filing it nowhere — which is the state this
scheme exists to end."

**"The `t → ∞` frozen-weights idealization is too far from a trained model"
survives as a *condition* and not as a disqualifier**, and I had not read far
enough to know that the paper closes part of the gap itself: the ALBERT
eigenvalue check, the explicit discrete-time analogue, and clustering arriving
within a few layers. The record also already holds
[THEORY-009](../theory.d/THEORY-009.md) — mean-field gradient flow on an infinite-width
limit — at `Active`. An idealization is a thing the record files with its
conditions stated, not a thing it refuses.

**And I missed the connections entirely**, because the query I was running was
"does this plot a weight spectrum?" The low-rank-attention link to LoRA and
Linformer, and the refinement of rank collapse, are both in the related-work
section I skimmed past. [DP-004](../../docs/design-principles.md#dp-4), for the second time in this batch.

## Open questions

- **Does a trained transformer's forward pass cluster this way?** Track token
  representations layer by layer in a real model, count clusters per head, and
  plot against the spectrum of that head's `V` — including the heads whose `V`
  violates Definition 4.1. That is the measurement standing between this and
  `Active`, and it needs no training.
- **Multi-head**, which the paper leaves open with numerics suggesting the
  phenomenon persists.
- **Does the ALBERT defence survive without weight sharing?** Every model that
  makes the time-independence assumption literal is in one family, and nothing
  says how fast the picture degrades when weights vary across layers.
