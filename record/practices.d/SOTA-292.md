---
number: 292
status: Proposed
formerly:
- SOTA-tmpxrcae
promote_when: >-
  The detection method run on a corpus other than this one — ideally an ML
  corpus rather than a social-media one — with the undisclosed share reported
  again. The method is mechanical and the corpus construction is reusable, so
  what is missing is somebody running it elsewhere, not a better technique.
consensus: unreplicated
consensus_note: >-
  One study, one field, four firms, seven journals. Metascience on conflicts
  of interest is an established genre with independent groups working in
  medicine and nutrition; what is unreplicated is this measurement in a
  computational field, and this record holds no comparable figure for its own
  sources.
title: 'Check industry ties yourself when reading a literature about deployed platforms — disclosure is unreliable and the ties are mechanically detectable'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-481
introduced_by:
- LIT-481
implementations: []
---

# SOTA-292: Check industry ties yourself when reading a literature about deployed platforms — disclosure is unreliable and the ties are mechanically detectable

## Source

Bak-Coleman, West, O'Connor and Bergstrom (2026), [LIT-481](../literature.d/LIT-481.md) — read
as [NOTE-231](../notes.d/NOTE-231.md). 295 papers in *Science*, *Nature*, *PNAS* and
their transfer journals, 1210 authors.

## The claim

**49% of high-profile social media papers have a disclosable industry tie and
most go undisclosed.** The published competing-interest statement is therefore
not a reliable signal, and a reader who treats its absence as the absence of a
tie will be wrong about half the time.

The reason this is a practice rather than a complaint is that **the ties are
detectable**: funding, collaboration and employment records in OpenAlex, plus
publicly announced RFPs and fellowships, plus CVs for editors. The source
validated every funding and employment tie against sources independent of
OpenAlex. Anyone can do this, and it takes a query rather than an
investigation.

## What to actually look at

**The topical distribution, more than any individual paper.** The skew is the
finding with the largest implications: ties are over-abundant in the cluster
about *what users share* and sparse in the cluster about *platform dynamics*.
If you are reading to find out whether a platform-scale design choice has an
effect, that is the cluster with the least industry money in it and the
fewest papers.

**Authors, not just papers.** 49% of papers carry a tie and only **21% of
authors** do. That gap says a small group with durable relationships appears
on half the output — a different situation from a field broadly engaged with
industry, and one disclosure norms alone will not fix.

**Editors and reviewers.** The same detection finds undisclosed ties there
too, where disclosure norms are weakest and where the effect on what gets
published is most direct.

**Attention, as a reason to look rather than a reason to trust.** Industry-tied
work draws more citations, more news coverage and more policy references. The
corpus as a whole reaches 745 policy documents. [DP-005](../principles.d/DP-005.md) in the
direction it is least often read: being well-adopted is what makes a body of
work worth auditing.

## Conditions

**The 49% is a floor.** Detection requires a public trace, so undetected ties
push the figure down rather than up. That is the conservative direction and it
means the number should not be quoted as an estimate.

**"Disclosable tie" is narrower than "conflict of interest"**, deliberately —
it is defined to be detectable and to match each journal's own policy window
(three years for Nature, four for PNAS, five for Science). Do not read it as
capturing everything a reader might reasonably want disclosed.

**The topical skew is correlational and the source says so.** Researchers
already interested in user-level questions may attract industry funding rather
than being directed toward it. The design cannot separate those, and the
practice's instruction — look at the distribution — survives either way.

**Four firms, seven journals, one field.** Meta, X, Google, Microsoft;
*Science*, *Nature*, *PNAS* and transfer venues. Ties outside that set are
invisible, and nothing establishes the same rates elsewhere.

**And this record has not run the check on itself.** The method is mechanical
and its corpus construction is reusable; whether the anthology's own sources
carry comparable rates is unknown, and the promotion condition asks for
exactly that measurement somewhere other than social media.
