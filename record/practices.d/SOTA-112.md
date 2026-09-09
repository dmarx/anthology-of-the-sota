---
number: 112
status: 'Active'
title: 'Combine Monarch Mixer layers with standard attention rather than replacing it wholesale'
version: 3
history:
- version: 3
  date: '2026-09-09'
  note: >-
    Bhardwaj → Fu in the citation line, with LIT-115's correction. The
    recommendation is unchanged.
- version: 1
  note: >-
    Titled "Combine with standard attention for hybrid approaches" — which never names its
    subject. All three practices from this source share the defect: they were
    bullets under a heading that supplied the subject, promoted one-to-one
    without it, so each reads as an instruction with no object.
- version: 2
  note: >-
    Subject restored to the title. The claim is unchanged; the source is
    LIT-115 and has always been Monarch Mixer.
tags:
- attention-techniques
date: '2026-08-24'
published: '2023-10-01'
source:
- LIT-115
summary: >-
  Fu et al. (2023), [LIT-115](../literature.d/LIT-115.md) — [ARXIV-2310.12109](https://arxiv.org/abs/2310.12109).
---

# SOTA-112: Combine Monarch Mixer layers with standard attention rather than replacing it wholesale

## Source

Fu et al. (2023), [LIT-115](../literature.d/LIT-115.md) — [ARXIV-2310.12109](https://arxiv.org/abs/2310.12109).

## Why hybrids rather than replacement

A structured mixer and attention fail differently. Attention is exact,
data-dependent and expensive; a Monarch mixer is cheap, fixed-pattern and
approximate. Interleaving them keeps a few layers able to do the exact
all-pairs comparison that some tasks need — retrieval from a long context,
precise copying — while the majority of layers pay the cheaper cost.

This is the same shape as the hybrid attention/state-space designs elsewhere
<!-- inactive-ok-block: SOTA-176 — Proposed, cited as the in-layer hybrid whose ratio is measured where this one's is not -->
in the record ([SOTA-132](SOTA-132.md)'s line, [SOTA-176](SOTA-176.md)'s in-layer version): the argument for
mixing two mechanisms is not that either is better, it is that their failure
modes are complementary and the ratio is a dial.

## The dial, and what nobody has set

The unstated parameter is *how many* attention layers and where. The hybrid
literature in this record puts the ratio at a small fraction — a handful of
full-attention layers in a stack of tens — but that is measured for
attention/SSM hybrids, not for this mixer, and the two are not obviously
interchangeable.

So the practice is directionally right and quantitatively empty, which the
title should not hide. Its value is as a warning against the wholesale
substitution [SOTA-110](SOTA-110.md) and [SOTA-111](SOTA-111.md) could be read as licensing.
