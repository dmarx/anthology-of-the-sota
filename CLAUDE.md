# CLAUDE.md

**Before anything else, read [the design principles](docs/design-principles.md)
in full.** They are short, they are specific to this project, and the rest of
this file assumes you hold them.

<!-- inactive-ok-file: ADR-020 — Superseded by ADR-026, which carries its decision forward; every mention here names it as the superseded document, deliberately -->

This is an anthology of current ML practice: what to do, and the published
work that says why. Organized by the **kind of claim**, not by the domain a
technique was discovered in ([ADR-026](record/decisions.d/ADR-026.md), superseding [ADR-020](record/decisions.d/ADR-020.md)). **The topics are
an axis, not a scope:** if something the anthology wants cannot be placed on
it, that is a finding about the axis — add the topic, never decline the
document ([ADR-059](record/decisions.d/ADR-059.md)). The bias toward language-model training is
a bias, not a boundary, and since [ADR-026](record/decisions.d/ADR-026.md) the practice registry and the
reading list share one topic vocabulary — the two schemes differ in what a
document *is*, not in what it may be *about*. Its memory is a Luria record — scaffolded,
generated and linted by the `luria` CLI. This file is a map, not a copy: when
it disagrees with `luria --help` or with the record, this file is wrong.

## Where things are

- `record/` is where you **file**. `practices.d/` holds one document per
  recommendation, `theory.d/` one per explanation, `literature.d/` one note
  per paper, plus the decisions,
  principles, changelog fragments and curation journal.
- `docs/` is where a reader **browses**. Everything in it is generated — see
  [docs/README.md](docs/README.md). Never edit an assembled page; edit the
  `README.stub` beside the sources and run `luria index`.
- `data/` is the pre-migration YAML, frozen. Nothing reads it at build time;
  it is the import's provenance, and keeps
  `src/scripts/migration/to_record.py` re-runnable. See
  [ADR-008](record/decisions.d/ADR-008.md) and `data/README.md`.

## The three schemes, and why there are three

<!-- inactive-ok-block: ADR-031 — Proposed, and named from a map rather
     than cited as a settled rule: the scheme exists and this section describes
     it; whether it earns its keep is what its promotion condition asks. -->

A **practice** (`SOTA`) is a claim about what you should do. A **theory**
(`THEORY`) is a claim about why it works. A **note** (`LIT`) is a paper's
standing in the anthology. They have separate statuses and are allowed to
disagree: a foundational paper can carry advice that has moved on, a paper in
the attic can be the source of something everybody still does, and a
technique everybody uses can have been published with an explanation that was
later refuted. Collapsing the first and the third is what the old schema did,
and [ADR-002](record/decisions.d/ADR-002.md) is why it stopped; splitting the
second out of the first is [ADR-031](record/decisions.d/ADR-031.md).

The test when filing: **if it tells the reader what to do it is a practice,
and if it says what is true it is a theory.** `Rejected` does not mean the
same thing in the two schemes — on a practice it means do not do this, on a
theory it means the reason is wrong, and the thing it explained may still
work perfectly well.

## Rules that are actually enforced

- **Every practice and every theory names a `source:`.** A recommendation with
  no paper behind it fails the lint, and so does an explanation. If the paper
  is not in the record, `luria new lit` first.
- **Every note names a source.** At least one of `arxiv:`, `doi:`, `url:`,
  in that order of preference — the first two resolve through a remote, a
  URL is a string nothing can check ([ADR-009](record/decisions.d/ADR-009.md)). Two papers reached the old
  corpus with no identifier at all; that is now impossible.
- **The first tag is the primary topic, and a document may carry more than
  one.** The twenty live in the `topics` vocabulary in `luria.yaml` — one
  table, named by the practice registry and the reading list alike, glosses
  included. List the topic the document is *most* about first: `primary_topic`
  derives `{tags[0]}`, so tag order is what the indexes read. **Tag the
  document's subject, liberally** — more than one topic is normal and three is
  fine. The test is whether a tag is *justifiably appropriate*: would someone
  browsing that topic be right to expect this document? Not whether it is the
  single best word, and not why the record went and got the thing (`ADR-046`).
- **An unbound relation is a defect, and "somebody looked at it" is not an
  answer.** `chains` declare `invariant: tags`, so a relation the report calls
  unbound has exactly two readings — the invariant is missing, or the relation
  is wrong — and never a third (`ADR-049`, which took 22 unbound relations and
  10 unbound lines to zero and rejected an acknowledgement directive for the
  purpose). So the report is where you find documents that are not saying what
  they are about, and answering one by adding a true topic is the intended
  response. The narrow thing that stays forbidden is inventing a *label* to
  satisfy the check (`ADR-035` §4) — impossible on `SOTA`, `LIT` and `THEORY`
  anyway, where the vocabulary is closed. If the honest tags will not bind,
  say so and fix it: either the relation is wrong, or the vocabulary is short
  a word and the next bullet is what to do about it.
- **The tag vocabulary is closed, and that is an invitation.** A tag not in
  `topics` fails the lint on `SOTA`, `LIT` and `THEORY`. That is there so
  every tag is one somebody chose and blurbed — **not** because the list is
  finished. If a document wants a word the vocabulary cannot say, the intended
  move is to add it, with a label and a blurb and a decision saying why,
  exactly as `representation-and-encoding` and `analysis-and-evaluation` were
  added. Reaching for the nearest wrong tag because the right one is absent is
  the failure this is meant to prevent, and the lint's message does not yet
  say so (`LU-#273`).
<!-- inactive-ok-block: LIT-041 — an example of the citation syntax -->
- **Never hand-write a link target.** Write the bare code — `LIT-041`,
  `ADR-002`, `ARXIV-1412.6980` — and run `luria link --fix`. Prose renders
  into several directories and only the fixer knows which frame a target
  resolves from.
- **Retire by changing status, never by deleting.** `Rejected` is the attic;
  `Superseded` names its successor. The body stays.

## Working

    luria new sota --title "..."   # or: theory, lit, adr, dp, changelog
    luria repair                  # created:, status notes, stale config refs
    luria link --fix              # spell the targets, complete the relations
    luria index                   # regenerate every view
    luria lint                    # the only command that can fail

<!-- inactive-ok-file: ADR-054 — Proposed, and cited as the decision that put `repair` in this sequence and the hook behind the discard step; Proposed is the resting state of an unmoved decision here, not a sign the sequence is unsettled. -->

Or `make ready`, which runs those four and discards the views ([ADR-054](record/decisions.d/ADR-054.md)).
**You need both `repair` and `link --fix`, and neither contains the other.**
`repair` populates a journal entry's `created:` from the path `luria new`
chose, moves a note out of `status:`, and retires a stale config reference.
`link --fix` **writes the converse of a declared relation**, which `repair`
does not — measured, not assumed: `repair` reported nothing to do on a tree
where `link --fix` then wrote two back-references.

Run all of them before pushing — then **do not commit what `luria index`
regenerated.** Views land on `main` only: CI regenerates and commits them on
the push, and a pull request writes none ([ADR-018](record/decisions.d/ADR-018.md)). Run `index` locally
anyway, because `docs/reports/reference-status.md` is what tells you which
citations the lint is about to flag; then `git checkout -- docs/` before you
commit. A branch carrying views is not more up to date, it is a conflict with
every other branch. Run `make hooks` once per clone and the tracked
`pre-commit` hook refuses them for you.

`luria lint` is warn-first: warnings are real findings, not noise, and the
ones about retired citations are the check this project adopted the record to
get. Acknowledge a deliberate one with an `inactive-ok:` comment at the
citing site — and write it **from the lint's own report, after running it**,
never from memory of a document's status. A directive naming no code vouches
for nothing, and one vouching for an `Active` document is itself a finding.

Work goes to a branch and a pull request. File the fragment in the same
contribution as the work — a fact written while the context is loaded costs a
paragraph, and re-derived cold it costs a session.
