---
number: 10
status: 'Superseded'
status_note: >-
  Not a recommendation, and never was: it states what is true rather than what
  to do, which is a THEORY under [ADR-031](../decisions.d/ADR-031.md) and was one of the eight that
  decision named and declined to move. The claim is unchanged and is believed
  — it now lives at [THEORY-011](../theory.d/THEORY-011.md), with the figure's limits and the five
  practices it underwrites. `Superseded` rather than `Rejected` because
  `Rejected` on a practice means *do not do this*, and nobody should read this
  code as advice against skip connections. [ADR-034](../decisions.d/ADR-034.md) is the rule.
# `superseded_by` crosses schemes by design (LU-ADR-071), which is the right
# shape for a move: the successor is typed and walked, not named in prose.
superseded_by:
- THEORY-011
title: 'skip connections promote training stability by smoothing out the loss landscape'
version: 2
history:
- version: 1
  note: >-
    Filed as a practice at the migration, with a body arguing the loss-surface
    result and what does and does not follow from it.
- version: 2
  date: '2026-09-15'
  note: >-
    Moved to the THEORY scheme. The body moves with the claim rather than
    being kept in two places; what stays here is the redirect, the lineage
    this code carries, and the record that the move happened.
tags:
- training-optimization
- model-stability
date: '2026-08-24'
source:
- LIT-014
introduced_by:
- LIT-014
summary: >-
  Li et al. (2017), [LIT-014](../literature.d/LIT-014.md). Moved to [THEORY-011](../theory.d/THEORY-011.md) — the claim is a
  statement about why deep networks became trainable, not an instruction, and
  belongs in the scheme [ADR-031](../decisions.d/ADR-031.md) created for exactly that. This code stays so
  links into it resolve.
# Kept rather than moved: THEORY has no sibling relation, and these record
# that three readings of one figure were filed together as practices, which is
# history this code is the right place for ([ADR-034](../decisions.d/ADR-034.md)).
compared_against:
- SOTA-011
- SOTA-012
---

<!-- inactive-ok-file: ADR-034, ADR-031 — both Proposed: the decision
     under which this document moved, and the scheme it moved into. Between
     them they are the whole content of this page. -->

# SOTA-010: skip connections promote training stability by smoothing out the loss landscape

Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).

## Moved

**The claim is at [THEORY-011](../theory.d/THEORY-011.md).** It is true, it is believed, and it is not
a recommendation: it says why deep networks became trainable, which is what
the `THEORY` scheme holds. [ADR-031](../decisions.d/ADR-031.md) listed this document as one of eight
practices whose titles state a behaviour rather than an instruction and left
them in place pending a decision about what a vacated code should say;
[ADR-034](../decisions.d/ADR-034.md) is that decision and this is its first application.

**There is no practice under it.** The instruction the claim would imply — use
skip connections — is trunk, and [DP-007](../../docs/design-principles.md#dp-7) keeps the agreed trunk unfiled. That
is why this is a move rather than a split.

**Do not read `Superseded` as a judgement on skip connections.** On a practice
that status means a better recommendation exists; here it means the document
is in the wrong scheme and the record says where the right one is.
