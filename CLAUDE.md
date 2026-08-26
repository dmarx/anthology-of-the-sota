# CLAUDE.md

**Before anything else, read [the design principles](docs/design-principles.md)
in full.** They are short, they are specific to this project, and the rest of
this file assumes you hold them.

This is an anthology of current ML training practice: what to do, and the
published work that says why. Its memory is a Luria record — scaffolded,
generated and linted by the `luria` CLI. This file is a map, not a copy: when
it disagrees with `luria --help` or with the record, this file is wrong.

## Where things are

- `record/` is where you **file**. `practices.d/` holds one document per
  recommendation, `literature.d/` one note per paper, plus the decisions,
  principles, changelog fragments and curation journal.
- `docs/` is where a reader **browses**. Everything in it is generated — see
  [docs/README.md](docs/README.md). Never edit an assembled page; edit the
  `README.stub` beside the sources and run `luria index`.
- `data/` is the pre-migration YAML, frozen. Nothing reads it at build time;
  it is the import's provenance, and keeps
  `src/scripts/migration/to_record.py` re-runnable. See
  [ADR-008](record/decisions.d/ADR-008.md) and `data/README.md`.

## The two schemes, and why there are two

A **practice** (`SOTA`) is a claim about what you should do. A **note**
(`LIT`) is a paper's standing in the anthology. They have separate statuses
and are allowed to disagree: a foundational paper can carry advice that has
moved on, and a paper in the attic can be the source of something everybody
still does. Collapsing them is what the old schema did, and
[ADR-002](record/decisions.d/ADR-002.md) is why it stopped.

## Rules that are actually enforced

- **Every practice names a `source:`.** A recommendation with no paper behind
  it fails the lint. If the paper is not in the record, `luria new lit` first.
- **Every note names an `arxiv:`.** Two papers reached the old corpus without
  one; that is now impossible.
- **Exactly one primary topic**, from the seven in
  `record/practices.d/tags.yaml`. Secondary tags are free, but add one only
  when it is true — the import deliberately adds none.
<!-- inactive-ok-block: LIT-041 — an example of the citation syntax -->
- **Never hand-write a link target.** Write the bare code — `LIT-041`,
  `ADR-002`, `ARXIV-1412.6980` — and run `luria link --fix`. Prose renders
  into several directories and only the fixer knows which frame a target
  resolves from.
- **Retire by changing status, never by deleting.** `Rejected` is the attic;
  `Superseded` names its successor. The body stays.

## Working

    luria new sota --title "..."   # or: lit, adr, dp, changelog
    luria link --fix              # spell the targets
    luria index                   # regenerate every view
    luria lint                    # the only command that can fail

Run all four before pushing. `luria lint` is warn-first: warnings are real
findings, not noise, and the ones about retired citations are the check this
project adopted the record to get. Acknowledge a deliberate one with an
`inactive-ok:` comment at the citing site rather than leaving it on the
report.

Work goes to a branch and a pull request. File the fragment in the same
contribution as the work — a fact written while the context is loaded costs a
paragraph, and re-derived cold it costs a session.
