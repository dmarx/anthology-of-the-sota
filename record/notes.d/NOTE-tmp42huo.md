---
status: Read
paper: LIT-tmp81ryb
title: 'A data-free lineage check built on the products that survive permutation and scaling'
version: 1
date: '2026-09-22'
summary: >-
  Read because the grep came back empty: the record holds no document about
  model provenance. The method is one good idea executed cleanly — compare
  the spectra of matrix products that functionality-preserving transforms
  cannot change — and the honest limit is that it is evidence of derivation,
  not proof against an adversary who has read the paper.
---
<!-- inactive-ok-file: THEORY-061 THEORY-062 SOTA-tmp3ot5z — all
     Proposed. The two theories are named to record a coincidence of subject
     matter between unconnected literatures; the practice is the one this
     reading yields and is filed in the same contribution. -->

# NOTE-tmp42huo: A data-free lineage check built on the products that survive permutation and scaling

## Contribution

A method for deciding whether one language model is derived from another,
using only the weights. The contribution is choosing quantities that
functionality-preserving obfuscation cannot alter.

## Key results

**Why raw weights fail.** A model can be permuted or rescaled so the weights
look different and the function is identical. Comparing `W_q`, `W_k`, `W_v`,
`W_o` head-on is therefore defeated by an attacker doing nothing clever.

**The invariants.** Per layer `i`:

    M_qk = W_q^(i) (W_k^(i))ᵀ      M_vo = W_v^(i) W_o^(i)

These products absorb the permutations and rescalings that cancel between the
paired matrices, so their singular spectra survive. The fingerprint of a model
is the sequence of per-layer spectra of both products.

**Two comparison metrics.** *GhostSpec-mse* compares spectra directly, with
truncation set by each spectrum's effective rank. *GhostSpec-corr* reduces
each layer to a scalar — the mean of the top-K normalized singular values —
producing two trend sequences per model, aligns sequences of differing length
by dynamic alignment, and scores by distance correlation. The second is the
cheap one and handles models whose depth differs.

**The evaluation.** 55 model pairs built from Llama-2-7b and Mistral-7B,
spanning fine-tuning (Vicuna, Llemma), adversarial transforms (scaled,
permuted), unstructured pruning at 50% with retraining and at 70%, merging and
expansion.

| method | F1 |
|---|---|
| **GhostSpec-mse** | **0.9867** |
| GhostSpec-corr | 0.9730 |
| REEF | 0.9610 |
| Logits | 0.9268 |
| QueRE | 0.9157 |
| PCS | 0.9014 |

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | `M_qk` and `M_vo` spectra are invariant to permutation and scaling | strong, and mostly algebraic | the products cancel the transforms |
| C2 | The fingerprint survives fine-tuning, pruning, merging and expansion | moderate-to-strong | 55 pairs across those categories |
| C3 | It beats prior fingerprinting methods | moderate | one benchmark the authors constructed |
| C4 | It is practical | strong | data-free, weights-only, no model modification |

## Limitations

**The benchmark is the authors'.** 55 pairs, assembled by them, with baselines
they ran. That is the normal state of a young subproblem and it means the
ranking is not independent.

**Two base models.** Llama-2-7b and Mistral-7B. Whether the fingerprint
discriminates as well among architectures that are genuinely similar by
convergent design rather than by derivation is the hard case, and it is not
the case tested.

**The threat model is implicit.** The adversarial transforms considered are
permutation and scaling. An adversary who has read this paper and wants to
break the fingerprint specifically — retraining attention projections,
inserting a learned orthogonal factor that does not cancel — is not modelled.
The method is evidence of derivation, not a proof of it, and a legal or policy
use would need that distinction stated loudly.

**Thresholds are empirical.** Both metrics use a discrimination threshold `τ`
fitted on this benchmark, so the reported F1 includes the benefit of a
threshold chosen where it is evaluated.

## Bearing on the record

**It opens a subject, which is the strongest reason to spend a unit.** The
practices contain nothing on watermarking, fingerprinting or provenance. Three
hundred recommendations about how to build, train and serve models, and none
about establishing where one came from — a question with public instances
already, and squarely inside `deployment-and-society`. [DP-004](../../docs/design-principles.md#dp-4):
an absence produces no unresolved code and no unbound relation, so nothing in
the machinery would have pointed at it.

**The same matrix, two literatures, no contact.** `W_q W_k^T` is the object
whose spectral energy concentration [THEORY-062](../theory.d/THEORY-062.md) says
predicts a training crash, and whose spectral norm bounds attention entropy in
[THEORY-061](../theory.d/THEORY-061.md). Here the same product's spectrum is an
identifier. Neither literature cites the other. Recorded as an observation
rather than a claim — this record has not shown the two uses are connected,
and the obvious question, whether a model trained with spectral control has a
less distinctive fingerprint, is asked by nobody.

**It is filed as a practice because the instruction is short and the
alternative is nothing.** [SOTA-tmp3ot5z](../practices.d/SOTA-tmp3ot5z.md) states it, `Proposed`,
with the threat-model limit in its conditions.

## Open questions

- **Does spectral control weaken the fingerprint?** A model trained with
  σReparam or Pion has a spectrum shaped by the optimizer rather than by the
  data. Whether that makes two independently trained models look related is
  unexamined and would matter to both literatures.
- **Convergently similar models.** Two models trained on the same public
  corpus with the same recipe and no derivation — does the fingerprint
  separate them? That is the false-positive case that decides whether this can
  support a claim about anyone.
- **What does an adaptive adversary cost?** Every fingerprinting method meets
  one eventually; the paper's transforms are the naive ones.
