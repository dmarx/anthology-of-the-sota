### Added

- A Luria record: `record/practices.d` (one document per recommendation),
  `record/literature.d` (one note per paper), decisions, design principles,
  a changelog and a curation journal. Browsable views are generated into
  `docs/`.
- The topic consolidation specified in 2024 and never applied: seven
  categories for practices, twelve for the reading list, with the
  one-primary-topic rule enforced by `luria lint`.
- arXiv as a configured remote — `ARXIV-1412.6980` written anywhere in the
  record resolves and links.

### Fixed

- Two papers had no arXiv identifier at all (Imagen and DALL-E 2); both now
  carry one, and `requires = ["arxiv"]` makes the omission impossible to
  repeat.
- PaLM appeared twice in the corpus under one identifier with two different
  takeaway lists. The entries are merged.
- The `sota_maybe` hedge on the AdamW paper reached no consumer, because the
  registry builder only ever read `sota`. It is now a `Deferred` practice.

### Changed

- Recommendation and paper statuses are now separate claims, and can
  disagree. Under the old schema both lived on the paper.
- The attic is a status (`Rejected`, or `Superseded` naming its successor)
  rather than a nested mapping nothing could resolve.

### Documentation

- Six decisions recording choices that had been implicit for years: the
  record adoption, the paper/practice split, the topic consolidation, the
  attic, the identifier scheme, and the deferred registry inversion.
