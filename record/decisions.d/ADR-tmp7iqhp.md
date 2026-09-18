---
status: Active
title: 'Every relation says what it means, and extends already covered specialization'
version: 1
tags:
- record
date: '2026-09-18'
summary: >-
  Twenty-one relations across four schemes carried a `scheme`, a `required`
  and a `many` and no statement of what they MEAN — the knowledge existed, as
  YAML comments nothing renders. All twenty-one now carry `label:` and
  `blurb:`, which luria has supported since `LU-#254` and no record had used.
  Writing `extends`'s blurb answered the open question from [ADR-tmpv09o2](ADR-tmpv09o2.md): it
  already covers a narrower case, so `specializes:` is not needed and
  [SOTA-085](../practices.d/SOTA-085.md)'s edge to [SOTA-083](../practices.d/SOTA-083.md) was simply in the wrong field. Rejected:
  splitting `extends` into three relations.
---

<!-- inactive-ok-file: ADR-036 — Superseded, and named as one of the two
     decisions that asked for the relation this one declines to add; the
     citation is to what it asked for, not to a rule in force -->

<!-- inactive-ok-file: SOTA-107 — Rejected, and named only as the far end of
     an edge this decision deliberately leaves alone -->

# ADR-tmp7iqhp: Every relation says what it means, and extends already covered specialization

## Context

The generated contract page shows the asymmetry plainly. `status`,
`consensus` and `tags` each render with an italic gloss saying what the field
means. Every relation renders as a bare type declaration:

> `extends` — optional, one or more `SOTA` codes when present

The knowledge was not missing. `luria.yaml` carries paragraphs of comment
around these fields explaining exactly this. It is in a form nothing can
render, quote or scaffold from — which is the case luria's own `Reference`
docstring makes for the `label:` and `blurb:` keys it has supported since
`LU-#254` and that no record had filled in.

The cost was not theoretical. `ADR-tmpv09o2` closed asking for a
`specializes:` relation, because `SOTA-083` (custom kernels for critical
ops) and `SOTA-085` (flash attention) are a general rule and its instance,
joined by `compared_against`, which `ADR-011` defines as *this work evaluates
itself against that one*. Nobody ran that comparison. The edge was in the
wrong field, and two passes read that as evidence the vocabulary was short a
word rather than that a filer had picked wrongly from a vocabulary nobody had
written down.

## Decision

**All twenty-one relations across `SOTA`, `THEORY`, `LIT` and `NOTE` carry
`label:` and `blurb:`.** Where a YAML comment already said it, the prose
moves into the data and the comment keeps only the reasoning the blurb does
not need to carry.

**`extends` is not split, because writing its blurb showed one coherent
idea:**

> the earlier practice this one builds on and could not stand without — a
> later version of the same recommendation, a narrower case of it, or a rule
> that only exists because the earlier one is followed

Those three looked like three relations from a distance. They are one
assertion — *B carries A's claim further and does not stand without A* — and
the line reads correctly oldest-first in every case. `SOTA-106` (a later
version of flash attention), `SOTA-085` (a narrower case of custom kernels)
and `SOTA-161` (a rule that exists only because flash attention is used) all
belong on one line under one arrow.

**`SOTA-085` and `SOTA-106` now `extend` `SOTA-083` rather than being
`compared_against` it.** That is a correction under `ADR-011`'s existing
definition, not a new policy, and the practice line now reads: use custom
kernels for critical ops → use flash attention → use flash-attention-2.

## Alternatives considered

- **Add `specializes:`.** What `ADR-036` and `ADR-tmpv09o2` both asked for.
  Rejected once `extends` was written down: a narrower case *is* a case of
  building on and not standing without. Adding it would split one true
  relation into two that filers must choose between, and a wrong choice
  between two similar relations is silent.
- **Split `extends` into `supersedes-version`, `specializes` and
  `depends-on`.** The fuller version of the same move. It buys precision the
  record has no use for — nothing reads the distinction, no view renders it,
  no check depends on it — at the cost of three vocabulary decisions per
  filing. `DP-008`'s corollary is the general form: do not add a category to
  admit a single document.
- **Leave the blurbs in comments and write an ADR instead.** What the record
  has been doing. A decision is where a choice is argued; the contract page
  is where a filer looks while filing, and it was rendering nothing. The two
  are not substitutes.
- **Keep `compared_against` on `SOTA-083`** and treat the crossing as a
  vocabulary problem. Rejected: the relation asserts somebody ran a
  comparison and nobody did. The unbound-lineage report was right that
  something was wrong there and wrong about what.

## Consequences

**The contract page now says what every relation means**, which is where a
filer is looking at the moment they need it. Twenty-one glosses, generated,
not a second copy to drift.

**`ADR-tmpv09o2`'s standing request is withdrawn**, and the `SOTA-089` ↔
`SOTA-107` pair it also cited is left alone — that edge's far end is in the
attic and it is a comparison the record genuinely made.

**The unbound relation does not disappear, and should not.** `SOTA-083`
carries `systems-optimization` and `SOTA-085` carries `attention-techniques`,
so the edge still crosses a vocabulary fault line — now as part of a line
rather than as a comparison nobody ran. `SOTA-085`'s frontmatter comment
asked that this edge *"keep showing up until someone answers it"*; this
answers what the relation is, not what the tags are, and the report is
correct to go on showing the second.

**Blurbs are now a thing a new relation needs.** Anything added to
`references:` without one will render as a bare type on a page where
everything around it explains itself, which is the kind of gap that gets
noticed.
