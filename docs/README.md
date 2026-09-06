# Docs

The generated views. This directory is for *reading*; filing happens in
`record/`, whose `.d`-suffixed containers hold the sources.

**The anthology**

- [Practices](practices/README.md) — what to do and why, one document per
  recommendation, each citing its source.
- [Literature](literature/README.md) — the evidence base, one note per paper,
  including the attic.
- [Lines of work](lineage.md) — the sequences: what replaced what, and which
  designs have been measured against each other. Walked from the `extends:`
  and `compared_against:` fields, so it cannot go stale the way the
  paragraphs it replaces did.

**How the anthology is built**

- [Decisions](decisions/README.md) — why the record is shaped this way.
- [Design principles](design-principles.md) — the values those decisions cite.
- [Curation log](curation/README.md) — dated entries on what entered the
  anthology and what left.
- [Record](record.md) — the shape this project gave Luria: its schemes,
  journals and remotes, generated from `luria.toml`.
- [Reports](reports/reference-status.md) — citations of retired documents,
  codes that resolve to nothing, and the acknowledgements that keep either
  quiet on purpose.

Each of these is **generated** — run `luria index`. Never edit an assembled
page; the lint refuses hand edits, and anything in a view directory the
generator didn't write is an error. Edit the `README.stub` beside the sources
instead.
