---
status: Active
title: 'On the Information Bottleneck Theory of Deep Learning'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-21'
published: '2018-04-30'
doi: '10.1088/1742-5468/ab3985'
first_author: 'Saxe'
keywords:
- 'information bottleneck'
- 'information plane'
- 'compression phase'
- 'mutual information estimation'
- 'neural nonlinearity'
- 'deep linear networks'
implementations: []
compared_against:
- LIT-tmpm2gzh
- LIT-tmpcnvbw
summary: >-
  Saxe et al. (2018), ICLR — the rebuttal. Takes the three claims of
  [LIT-tmpm2gzh](LIT-tmpm2gzh.md) and shows none holds in general. The compression phase
  tracks the **nonlinearity**: `tanh` compresses, ReLU does not, replicated
  with the original authors' own code and confirmed by three independent MI
  estimators. Compression and generalization dissociate in all four
  combinations. Full-batch gradient descent compresses as much as SGD. Read as
  [NOTE-tmp11zjy](../notes.d/NOTE-tmp11zjy.md).
---

# LIT-tmpsld21: On the Information Bottleneck Theory of Deep Learning

Saxe, Bansal, Dapello, Advani, Kolchinsky, Tracey and Cox (2018) —
`doi:10.1088/1742-5468/ab3985`, read as [NOTE-tmp11zjy](../notes.d/NOTE-tmp11zjy.md).

## Standing

**The principal rebuttal, and the reason this dispute is filable at all.** It
does not argue from a different setup: it replicates [LIT-tmpm2gzh](LIT-tmpm2gzh.md) using
the original authors' released code, then varies one thing at a time.

**Which version was read.** This record read the **ICLR 2018 conference
paper**, supplied by the record's owner because no open route to it exists —
OpenReview returns 403 to `/pdf` and to its API, and the JSTAT page resolves
but serves no article text. The identifier filed is the JSTAT DOI, which is
the later and slightly expanded version and is what
[ADR-009](../decisions.d/ADR-009.md) prefers; any numbers quoted in
[NOTE-tmp11zjy](../notes.d/NOTE-tmp11zjy.md) are from the ICLR version, and that is said there too.

**What it leaves standing.** It addresses three claims. [LIT-tmpm2gzh](LIT-tmpm2gzh.md)'s
fourth — that the main benefit of depth is computational, dramatically
reducing epochs to good generalization — is not examined by this paper and is
not refuted by it.

**Its deepest point is not the one it is cited for.** It is usually cited for
"ReLU does not compress". The more general result is in its Appendix C: the
same `tanh` network, the same training run, binned evenly in *net input*
rather than evenly in *activity*, shows **no compression**. The true `I(h;X)`
in a deterministic network is infinite, so every finite number on an
information plane is a property of a noise model the analyst imposed and the
network never had.
