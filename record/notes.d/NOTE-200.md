---
number: 200
status: Read
formerly:
- NOTE-tmpk9vmg
paper: LIT-452
title: 'Scaling Laws for Fact Memorization'
version: 1
date: '2026-09-20'
summary: >-
  Fact capacity is linear in model size and saturates in epochs along a
  negative exponential; all of Wikidata would want ~1000B non-embedding
  parameters at 100 epochs. Redundant facts cost full price unless they
  share direction and structure. Generalisation to unseen facts exists and
  scales like ordinary pretraining.
---

# NOTE-200: Scaling Laws for Fact Memorization
<!-- inactive-ok-file: THEORY-025 — Proposed, and the account this reading corroborates in different units -->

## Contribution

Puts a price on keeping a knowledge base in weights. Prior work had
established that fact storage grows with model size; this fits the law in
both model size and training epochs, extrapolates it to a real knowledge base
of known size, and reports what that would cost. It then shows the cost is
worse than the law alone suggests, because derivable facts are not stored
derivably — the model pays separately for each — and separately establishes
that generalisation to *unseen* facts does exist and follows a different,
ordinary scaling law, so the negative result is about knowledge bases rather
than about factual competence.

## Key insight

**Memorisation and generalisation are two different scaling regimes running
at once, and only one of them is cheap.** Facts a model must store
individually cost capacity linearly and take many epochs to acquire — far
more than the single pass general pretraining gets. Facts whose type carries
strong input-output correlation are partly derivable, and there the model
generalises to instances it never saw, at ordinary pretraining scaling. The
same quantity — correlation strength between the fact's input and output —
predicts both which facts are easy to memorise and which generalise well.
Redundancy makes this concrete: two facts that a human would call the same
fact cost twice unless their surface direction and structure happen to match,
which is a statement about what the model is actually keying on.

## Assumptions

- **Facts are Wikidata-style triples**, and "memorised" means accurate recall
  of the object given subject and relation.
- **Non-embedding parameters** are the capacity measure, which matters for
  the 1000B figure.
- Training is repeated-epoch on a fact set, not single-pass pretraining, and
  the epoch counts are deliberately far above one.
- The 1000B extrapolation assumes the fitted law holds several orders of
  magnitude beyond the measured range.
- Generalisation is evaluated on held-out facts of the same *types* as those
  trained on.

## Key results

- **Fact capacity is linear in model size** at fixed epochs. *Holds when:*
  trained to saturation at that epoch count.
- **Fact capacity is negative-exponential in epochs** — rising, then
  saturating. Many epochs are needed; one is far from enough.
- **Extrapolation**: memorising all ~15B Wikidata triples wants roughly
  **1000B non-embedding parameters at 100 epochs**.
- **Memorisation rate falls as the number of training facts rises** at fixed
  size and epochs, which is the direct evidence for a capacity ceiling.
- **Redundant facts do not compress.** Memorisation rate is similar for
  redundant and non-redundant sets of the same size; compression happens only
  when correlated facts share direction and structure.
- **Preference**: more frequent and more difficult facts are memorised
  preferentially.
- **Generalisation exists** on unseen facts, with a scaling law the authors
  describe as highly similar to Kaplan's. Generalisability varies by fact
  type.
- **One qualitative relation ties the two**: within a fact type, the easier
  to memorise, the better the generalisation — read as both tracking
  input-output correlation strength.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Fact capacity is linear in model size | strong | fitted across model sizes, consistent on a synthetic set and on Wikidata |
| C2 | Fact capacity saturates in epochs along a negative exponential | moderate | fitted; the saturation is clear, the functional form is a fit |
| C3 | Memorising all of Wikidata is implausible in a pretraining budget | moderate | an extrapolation several orders of magnitude past the measured range; the qualitative conclusion is robust to the exact constant |
| C4 | Redundant facts are not stored efficiently | strong | direct comparison of redundant and non-redundant sets at matched size |
| C5 | Models generalise to unseen facts, at ordinary pretraining scaling | moderate | measured per fact type, with substantial variation by type |
| C6 | Memorisation ease and generalisation quality both track input-output correlation | weak | a qualitative relation observed across fact types, offered as interpretation |

## Method

Train language models of varying size for varying numbers of epochs on sets
of fact triples of varying size, and measure the maximum number recalled
accurately — the capacity. Fit capacity against size at fixed epochs, and
against epochs at fixed size. Repeat on Wikidata and extrapolate.

For redundancy, construct sets containing derivable pairs and matched sets
without them, and compare memorisation rates at equal set size.

For generalisation, hold out facts of the same types as those trained on and
measure accuracy, fitting a scaling law and reporting per-type variation.

## Concepts

- **Fact knowledge capacity** — the maximum number of fact triples recalled
  accurately, at a given size and epoch count. An empirical quantity with a
  training procedure inside it.
- **Redundant facts** — facts derivable from others, such as the two
  directions of a family relation. A human counts them once.
- **Fact type** — the relation in the triple. Generalisability varies sharply
  across types, which is the paper's handle on why.

## Connections

The measurement sits alongside [LIT-440](../literature.d/LIT-440.md), which measures capacity in bits on
random bitstrings where generalisation is impossible and gets ~3.6 bits per
parameter, linear in parameter count. Two instruments, two units, one
functional form. Neither converts to the other.

Prior work on fact storage — Roberts et al., Allen-Zhu and Li — established
linearity for facts; this fits the law properly, adds the epoch dimension,
and does the extrapolation nobody had committed to.

The negative result is the standard argument for retrieval augmentation, and
the paper makes it explicitly.

## Recommendations

- **R1** — Keep a knowledge base outside the weights. Parameters are a
  quantifiably expensive and lossy place to store facts, and the cost is
  worse than the capacity law alone implies because redundancy is not
  compressed. *Topic:* knowledge. *Status:* standard. *Strength:* strong.
  *Applies when:* the facts are enumerable and a retrieval path exists.
- **R2** — Budget many epochs if facts must be memorised; one pass is far from
  enough, and the return saturates. *Topic:* training. *Status:*
  experimental. *Strength:* moderate. *Applies when:* deliberate
  memorisation is the goal.
- **R3** — Do not assume derivable facts come for free; state both directions
  if both are needed. *Topic:* data. *Status:* experimental. *Strength:*
  moderate. *Applies when:* curating a knowledge-dense corpus.

## Bearing on the record

- **Should produce a practice** for R1, and the gap is larger than it looks.
  The record holds [LIT-060](../literature.d/LIT-060.md) — RETRO, which established retrieval-augmented
  pretraining — and the only practice drawn from it is [SOTA-197](../practices.d/SOTA-197.md), about
  contamination in evaluation. The record has the evidence that the
  alternative works and has never recommended it.
- **Corroborates [THEORY-025](../theory.d/THEORY-025.md)'s linear-in-parameters claim** through a second
  instrument. That account measures bits on random data; this measures facts
  on Wikidata. The agreement is on the functional form, not on a constant,
  because nobody has converted facts to bits.
- **Qualifies any reading of R1 as "models can't do facts".** C5 says the
  opposite for fact types with strong input-output correlation. The advice is
  about knowledge bases, not about factual competence.
- **C4 bears on the record's data-curation material.** A corpus in which the
  same fact appears in several forms is paying capacity for each form, which
  nothing in the record's deduplication or quality-filtering practices
  accounts for.

## Limitations

- The 1000B figure is an extrapolation several orders of magnitude past the
  measurements, and reads as precise when it is an order-of-magnitude claim.
- Capacity is measured under repeated-epoch training on fact sets, which is
  not how pretraining sees facts; whether the same law governs incidental
  acquisition during a single pass is untouched.
- Wikidata triples are a specific and unusually clean form of fact.
- C6 is a qualitative relation across fact types, offered as interpretation;
  no intervention manipulates correlation strength.
- Model sizes are modest relative to the extrapolation's target.

## Open questions

- How many bits is a fact? That conversion is what would let this and
  [LIT-440](../literature.d/LIT-440.md) be checked against each other rather than merely agreeing in
  shape.
- Does the epoch saturation interact with the mixing thresholds of
  [LIT-451](../literature.d/LIT-451.md)? Both are about how much of a small dense corpus gets
  stored, from different directions, and neither cites the other.
- Can redundancy be made to compress by construction — canonicalising facts
  into a single direction and structure before training?
