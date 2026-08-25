# data/ — the pre-migration corpus, frozen

These two files were the anthology before it became a record. They are kept
as the import's provenance and are **not maintained**: every claim in them
now lives in `record/`, and edits here reach nothing.

- `research.yaml` — 119 paper entries (118 after de-duplication), the source
  for `record/literature.d`.
- `registry.yaml` — 119 recommendations derived from the `sota:` fields
  above, the source for `record/practices.d`.

They stay because `src/scripts/migration/to_record.py` reads them, and that
script is what makes 238 generated documents auditable: a reviewer can re-run
it and diff rather than take the import on faith.

    python src/scripts/migration/to_record.py --check

What used to consume them — `scripts.registry.cli`, the `Build Registry`
workflow, `REGISTRY.md`, and the `web/` frontend — is retired. See
`record/decisions.d/ADR-008.md`.

Adding a paper means adding a note to the record, not an entry here.
