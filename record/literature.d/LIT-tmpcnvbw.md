---
status: Active
title: 'Adaptive Estimators Show Information Compression in Deep Neural Networks'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-21'
published: '2019-02-25'
arxiv: '1902.09037'
first_author: 'Chelombiev'
keywords:
- 'mutual information estimation'
- 'adaptive binning'
- 'kernel density estimation'
- 'information plane'
- 'compression'
implementations: []
compared_against:
- LIT-tmpm2gzh
- LIT-tmpsld21
summary: >-
  Chelombiev, Houghton and O'Donnell (2019), [ARXIV-1902.09037](https://arxiv.org/abs/1902.09037) — the
  third voice, and the one whose body is weaker than its abstract. Argues that
  [LIT-tmpsld21](LIT-tmpsld21.md)'s ReLU result is an artifact of non-adaptive binning and that
  with adaptive estimators saturation is not required for compression. Its own
  Figure 6 shows that **averaged over 50 initializations a ReLU network has no
  distinct phase at all**, and it agrees with the rebuttal that hidden-layer
  compression does not correlate with generalization. Read as
  [NOTE-tmplxznx](../notes.d/NOTE-tmplxznx.md).
---

# LIT-tmpcnvbw: Adaptive Estimators Show Information Compression in Deep Neural Networks

Chelombiev, Houghton and O'Donnell (2019) — [ARXIV-1902.09037](https://arxiv.org/abs/1902.09037), read
as [NOTE-tmplxznx](../notes.d/NOTE-tmplxznx.md).

## Standing

**Held because leaving it out would misrepresent the dispute, and because
what it actually shows is not what it is usually taken to show.** Read from
its abstract it is a defence of the compression phase against
[LIT-tmpsld21](LIT-tmpsld21.md); read from its figures it is a third independent demonstration
that the estimator determines the answer, pointing the opposite way to the
rebuttal's demonstration and reaching the same conclusion about
generalization.

**Its technical criticism is specific and lands.** [LIT-tmpsld21](LIT-tmpsld21.md) binned
ReLU activity over a single global range `[0, m]`, `m` being the largest
activity anywhere in the network across all of training. This paper shows the
last ReLU layer dominates that maximum, so one global range under-resolves the
earlier layers, and that non-adaptive binning therefore under-estimates
compression.

**Its headline does not survive its own averaging.** The compression it
showcases is one initialization. Over 50, fitting and compression "mostly
cancel out" and `I(T;X)` is largely flat.
