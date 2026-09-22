---
status: Read
paper: LIT-tmpcv53l
title: 'The trunk under a term the record was using for two different things'
version: 1
date: '2026-09-22'
summary: >-
  Read because four documents in this record lean on "rank collapse" and none
  of them held its source. Reading it produced a finding that was not the
  point of the unit: the record carries that term for two distinct phenomena,
  and the conflation is the field's rather than ours.
---
<!-- inactive-ok-file: SOTA-010 — Superseded, and named only to say where its
     claim went: into THEORY-011, which is the account this paper supplies a
     second and different reason alongside. Nothing here reads it as advice. -->

<!-- inactive-ok-file: THEORY-064 — Proposed, named in an open question that
     asks whether its account and this one pull against each other. The
     question requires both to be unsettled. -->

# NOTE-tmpsokgi: The trunk under a term the record was using for two different things

## Contribution

Decompose a self-attention network's output into a sum over *paths* — one head
choice per layer — and use the decomposition to prove that pure self-attention
degenerates. Then reintroduce the three components a real transformer has and
ask which of them stops the degeneration.

## Key results

**The path decomposition (Theorem 2.1).** The output of a depth-`L`, `H`-head
SAN is `Σ_path P_path X W_path + 1bᵀ`, each term a single-head deep network.
With skip connections, setting `h = 0` marks a skipped layer, and the number of
paths of length `l` becomes `C(L,l)·H^l` — so the path set is dominated by
*short* paths, including the one that skips everything.

**The collapse (Theorem 2.2).** With `res(X) = X − 1xᵀ` the residual after
removing the best rank-1 approximation,

    ‖res(SAN(X))‖₁,∞ ≤ (4γβ/√d_qk)^((3^L−1)/2) · ‖res(X)‖^(3^L)₁,∞

guaranteed to converge whenever `4γβ < √d_qk`, and empirically over a much
wider region. The rate is **cubic**, not linear, because the attention matrix's
rank depends on the rank of its own input — heads mix tokens faster when formed
from a low-rank matrix, which cascades with depth. The authors' calibration:
three orders of magnitude takes a linear rate about a dozen iterations and a
cubic rate two or three.

**Skip connections (Claim 3.1).** There are infinitely many parameterizations
with `‖res(X_L)‖ ≥ ‖res(X)‖`, holding even as `L → ∞` and for `β` arbitrarily
small. The proof is one line — the length-zero path preserves the residual —
and the authors are candid that the *upper* bound they can derive with skip
connections is vacuously large. **A tight lower bound is posed as an open
challenge to the community.**

**MLPs (Corollary 3.2).** The bound becomes `(4γβHλ/√d_qk)^((3^L−1)/2)` with
λ the MLP's Lipschitz constant: more powerful MLPs, slower collapse. A
tug-of-war. The paper states the cost against its own remedy — larger Lipschitz
constants render the model "less robust and more sensitive to input
perturbations", and raise gradient variance.

**Layer normalization does nothing, provably.** `LN(SA(X))` rewrites as
`Σ_h P_h X W̃_h + 1b̃ᵀ` with `W̃_h = W_h D_LN^{-1}`, so LN is absorbed as a
right multiplication plus a rank-1 shift, and right multiplication cannot
increase rank.

**Experiments.** BERT, ALBERT and XLNet, at initialization and pretrained,
plotting `‖res(SAN_l(X))‖/‖SAN_l(X)‖` against layer index for four ablations —
SAN, SAN+MLP, SAN+skip, full transformer. Pure attention converges rapidly;
skip is what flattens the curve.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Pure SANs collapse to rank 1 doubly exponentially | strong | proved, with the convergence region stated |
| C2 | Skip connections prevent it | strong in direction, weak in magnitude | a lower bound exists but is trivial; the tight one is an open problem the authors pose |
| C3 | MLPs slow it via their Lipschitz constant | moderate | a bound plus experiments |
| C4 | Layer normalization cannot help | strong, and nearly algebraic | right multiplication cannot raise rank |
| C5 | SANs with skips behave like ensembles of shallow networks | suggestive | follows from the decomposition; the ResNet analogue is cited |

## Limitations

**The headline object is not a transformer.** A "pure SAN" has no skip
connections and no MLP, which is not an architecture anyone trains. The paper
is explicit about this and the whole of §3 exists to say so — but the title
travels further than the theorem, and the record has an instance of it
travelling.

**C2 is the important claim and the weakest one.** What is proved is that
*some* parameterizations preserve the residual, by an argument that works
because a path can skip every layer. That is a long way from "skip connections
prevent rank collapse in trained transformers", which is what the figures
suggest and nothing proves.

**γ and β are bounds on quantities nobody reports.** `β ≥ ‖W_QK‖₁‖W_V‖₁,∞`
and γ depends on the attention entries; the convergence condition
`4γβ < √d_qk` is not checked against any trained model's actual values.

**The `ℓ₁,∞` composite norm is not a norm** — the authors say so; it fails the
triangle inequality.

## Bearing on the record

**The finding that was not the point of the unit: "rank collapse" names two
different things here, and the conflation is the field's.**
[LIT-350](../literature.d/LIT-350.md) — Subspace Networks — says in its own words that "as
training progresses, weight matrices exhibit rank collapse, converging to
low-rank subspaces", and [NOTE-105](NOTE-105.md) reports that faithfully. This
paper's rank collapse is a different object on a different axis:

| | what collapses | along what | prevented by |
|---|---|---|---|
| this paper | token representations, to rank 1 | **depth**, in one forward pass | skip connections |
| [LIT-350](../literature.d/LIT-350.md), [LIT-516](../literature.d/LIT-516.md) | weight matrices, to low-rank subspaces | **training time** | nothing claimed |

Neither is wrong; they are unrelated phenomena sharing a name. The record now
holds both, and this is the note that says which is which. Nothing in
[NOTE-105](NOTE-105.md) needs correcting — it is reporting its source.

**It gives skip connections a second reason to exist.**
[THEORY-011](../theory.d/THEORY-011.md) says they smooth the loss landscape — the account
[SOTA-010](../practices.d/SOTA-010.md) was superseded into. This says they preserve rank, and the
paper claims that effect was previously unknown. Different mechanisms, same
component, no relation declared and prose on both sides.

**The record has held its rebuttal all day with nothing to rebut.**
[LIT-521](../literature.d/LIT-521.md) names this account and rank collapse of activations
as the wrong locus, arguing the cause sits in the weight matrix. That is now a
dispute with both sides present.

**And the MLP caveat runs straight into [THEORY-064](../theory.d/THEORY-064.md).** That account
holds that transformers' robustness is made of their bias toward
low-sensitivity functions. This one says the component that counteracts rank
collapse does so by raising its Lipschitz constant, which makes the model *more*
sensitive to input perturbations. So preventing collapse and being robust pull
against each other. Three years apart, no citation in either direction, and
neither paper frames it as a trade.

## Open questions

- **The tight lower bound with skip connections**, which the authors pose as an
  open challenge and which is the claim everyone quotes this paper for.
- **Is `4γβ < √d_qk` satisfied by trained models?** The condition is stated and
  never evaluated. One measurement on a checkpoint the record holds.
- **Is the sensitivity trade real?** Rank preservation via large-Lipschitz MLPs
  against the low-sensitivity bias — measure both on one model family and see
  whether they actually oppose.
