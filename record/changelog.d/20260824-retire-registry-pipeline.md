### Removed

- The registry pipeline: `scripts.registry.cli`, the `Build Registry`
  workflow, the `build-registry` entry point, `data/REGISTRY.md`, and the
  flat registry listing injected into the README. The record generates the
  same corpus as a browsable view with working links and a status column
  that distinguishes records.
- The `web/` frontend and its deploy workflow, replaced by `luria site`.
- The topic-vocabulary specification in the LLM README templates, superseded
  by [ADR-003](record/decisions.d/ADR-003.md) and enforced since.
- The generated project-structure tree.

### Added

- A `Pages` workflow that publishes the record with `luria site`. **Requires
  Settings → Pages → Source set to "GitHub Actions" before the first deploy
  succeeds.**

### Changed

- README rendering moved into the `Docs` workflow's generate job, so exactly
  one job commits generated files and its commit carries a skip marker. Two
  committing workflows had left the branch tip unlinted.
- The luria actions are pinned to a released tag rather than `@main`.
- `data/` is frozen and documented as the import's provenance.
