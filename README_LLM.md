## Development Guidelines

### What this repository is

An anthology of ML training practice, kept as a [Luria](https://github.com/dmarx/luria)
record. It is **not** a Python project. There is no application, no test
suite, and no build — the deliverable is the record in `record/` and the
generated views in `docs/`.

One script survives, `src/scripts/migration/to_record.py`, which produced
`record/` from the frozen YAML in `data/` and is kept re-runnable by
`record/decisions.d/ADR-008.md`. It needs `pyyaml` and nothing else.

If you are looking for how to work here, read `CLAUDE.md` first — it is the
map, and it links the design principles that the rest assumes.

### Working on the record

    luria new sota --title "..."   # or: lit, adr, dp, changelog
    luria link --fix               # spell the targets
    luria index                    # regenerate every view
    luria lint                     # the only command that can fail

Run all four before pushing, and do not commit what `luria index` wrote:
views land on `main` only (`record/decisions.d/ADR-018.md`). CI regenerates
and commits them on the push; a pull request writes none.

### Conventions

- Aim for files under 200 lines. Each file should have a single, clear
  purpose, and directory structure should carry the organisation. If you find
  yourself writing "... rest remains the same", the file is too long.
- Prefer many small files over few large ones. A file that cannot be replaced
  whole in one edit is a file that will be edited badly.
- Syntax permitting, a file begins with a comment naming itself and its path.
- Where Python is written at all: `loguru` for logging, `fire` for CLIs,
  `omegaconf` for YAML config, `pathlib` for paths, and type hints using
  built-in generics (PEP 585) and the union operator (PEP 604).
- GitHub Actions is the only runtime for script execution here.

### Why the shape matters

Large language models work best with clear, focused contexts. Complete file
contents beat partial updates with ellipsis; short files make it possible to
understand the whole context, suggest accurate modifications, and avoid the
errors that come from working with a fragment. The record's own documents are
written the same way and for the same reason.

## The record

The anthology's data is a Luria record, not a YAML registry. Sources live in
`record/`; every browsable view under `docs/` is generated from them.

- `record/practices.d` — one document per recommendation, each naming the
  paper it came from in a required `source:` field.
- `record/literature.d` — one note per paper, including the attic.
- `record/decisions.d`, `record/principles.d` — why the anthology is built
  this way.

Start at `docs/README.md`. The topic vocabulary and the one-primary-topic
rule are specified in `record/decisions.d/ADR-003.md` and enforced by
`luria lint` — that decision replaced a prose specification which sat in this
directory for two years without being applied, which is why it is a decision
now and not a document.

Commands: `luria new`, `luria link --fix`, `luria index`, `luria lint`.
