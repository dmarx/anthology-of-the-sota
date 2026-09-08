---
status: Active
title: Adoption is not evidence — who does a thing and whether it works are different questions
version: 1
tags:
- craft
date: '2026-09-08'
influenced_by:
- ADR-010
- ADR-015
- ADR-017
---

# DP-tmp2v4jc: Adoption is not evidence — who does a thing and whether it works are different questions

Two facts about a recommendation feel like the same fact and are not. One:
somebody tested it and reports what happened. Two: somebody shipped it. The
second is easier to collect, arrives in greater volume, and is what a
practitioner most wants to hear — which is precisely why it ends up doing a
job it cannot do.

A report that ships a design without measuring it is evidence that the design
was *chosen*. It is not evidence that the choice was right, and it is
frequently not even independent: the group shipping it read the same paper
you did, or wrote it. Stack four such reports in the column meant for
evidence and the recommendation looks four times better supported while
nothing has been tested twice.

The confusion is not sloppiness. It is that both facts genuinely bear on the
recommendation, so the instinct to record both is correct. What is wrong is
recording them in one place, because they answer different questions and a
reader cannot recover which is which once they are merged.

Applied here: `source:` holds the work that produced evidence *about the
claim* — the ablation, the controlled comparison, the paper that isolated a
change — while adoption goes to `consensus:` and its note, where counting is
the right operation. One practice had written the distinction in its own
prose, calling four model reports "four generations of adoption rather than
one result", and then listed all four as support anyway. It now names the one
work that ran the comparison.

The corollary that makes this pay: once separated, both columns start
answering questions they could not before. A recommendation with one source
and eight adopters is a different object from one with eight sources and no
adopters, and telling a reader which they are looking at is most of what a
collection like this is for.
