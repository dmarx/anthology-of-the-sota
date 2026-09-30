---
status: Active
title: 'Relations a reader cannot weigh without prose must be explained in the body'
version: 1
tags:
- record
date: '2026-09-30'
summary: >-
  Ten reference fields declare `explain: true` (luria 0.33): a practice's and
  a theory's evidence, a practice's origin, a theory's `explains`, every
  `corrects`, `contested_by`, and `extends` on practices and theories. Each
  code they hold must be cited in the body with the relation stated. Rejected:
  every field (converse back-references, `compared_against` and `NOTE.paper`
  are frontmatter facts, and together they would have been ~700 findings of
  noise), and `LIT.extends` for now (84 uncited, left as follow-up).
---

# ADR-tmp7icjh: Relations a reader cannot weigh without prose must be explained in the body

## Context

A relation in frontmatter says *that* two documents are related, never *how*.
`source: LIT-541` on a practice tells a reader which paper to blame and
nothing about what the paper showed; `corrects: LIT-045` says a paper was
wrong without saying about what. Until luria 0.33 nothing checked that the
prose ever said it, and measuring showed the gap was real but narrow: with
every reference field opted in on a scratch copy, practices already cited 575
of their 590 sources in the body, while notes cited 40 of the 378 papers they
are readings of.

luria 0.33 added the check (`explain: true` on a reference). A code the field
holds must be cited in the body, and the citation carries a `ref::` statement
of the relation. `luria link --fix` writes the statement beside an existing
citation; a code the body never cites is `unexplained-relations`, which only
a person can fix, by writing the sentence. A statement's `— reason` also counts
as an explanation.

## Decision

`explain: true` on ten fields, chosen by one test: **would a reader need
prose to weigh this relation?**

- **Evidence and origin.** `SOTA.source`, `SOTA.introduced_by`,
  `THEORY.source`. A recommendation is only as good as what its paper showed,
  and the body is where that is said.
- **The explanation link.** `THEORY.explains`. Which part of the practice the
  account explains is the claim itself.
- **Disputes.** `corrects` on all three schemes and `SOTA.contested_by`. A
  correction that does not say what was wrong cannot be checked.
- **Lineage of claims.** `extends` on practices and theories: what the later
  claim could not stand without.

The explanation must be prose a reader sees. An HTML comment explaining a
relation does not count, and neither does a code in backticks, which is a
mention rather than a citation.

## Alternatives considered

- **Every reference field.** It measured at 974 unexplained relations. Most
  are on fields whose meaning is complete in frontmatter:
  - the converse back-references `luria link --fix` writes (`extended_by`,
    `corrected_by`, `explained_by`), whose other end carries the prose;
  - `compared_against`, a symmetric fact that somebody ran a comparison
    (280 uncited);
  - `NOTE.paper`, where the note *is* the reading (338 uncited).

  Making each of those a finding teaches people to ignore the class.
- **`LIT.extends` now.** It passes the test, but 84 notes would need a
  sentence each, and a paper note's lineage is read less than a practice's.
  Left for a follow-up rather than filled with thin sentences to clear a count.
- **Acknowledging the uncited ones with `— reason` statements instead of
  prose.** That is legitimate where the relation needs no more than a clause.
  It was not the default here: a reason hidden in a comment is exactly the
  invisible explanation this decision exists to end.
- **Status quo.** Every relation stays unexplained until someone happens to
  write about it. That is how 81 of them accumulated.

## Consequences

- `luria link --fix` wrote 1346 statements beside citations the prose already
  made. The pin moved from luria 0.31.0 to 0.33.1 in the same contribution (0.33.0 crashed on the DOI-labelled links in five notes; 0.33.1 is its fix).
- 23 relations were cited only as backticked mentions: sources in recent
  practices and theories, and a few `explains`. They became citations.
- The remaining 58 had no citation at all, and each got a sentence written
  from what the two documents say. Relations whose documents did not support
  them were not explained into existence. They are listed in the
  contribution rather than papered over.
- From now on, a new practice or theory that names a source it never
  discusses fails nothing, but it is reported, and the report names the file.
