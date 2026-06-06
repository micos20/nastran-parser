# nastran-parser — Developer Guide for Claude

## Project structure

```
nastran-parser/
├── src/nastran_parser/       # library source code
├── tests/                    # pytest tests (mirrors src/ tree)
├── architecture/
│   ├── requirements/         # StrictDoc .sdoc files (FR-, NFR-)
│   ├── diagrams/             # PlantUML source files (.puml) + generated SVGs
│   └── architectural_dossier.md  # main architecture document
├── strictdoc_config.py       # StrictDoc project config
└── pyproject.toml            # all Python project config (tools, deps, metadata)
```

- Runtime library code lives exclusively under `src/nastran_parser/`.
- Dev dependencies are declared in `[dependency-groups] dev` in `pyproject.toml`.
- Python minimum: 3.12. `match`/`case` is available and preferred for card-type dispatch.

## Git workflow

Do not stage or commit changes on your own. When you finish making file changes,
summarise what you changed and stop — let the user decide when to commit.

**Exception:** When the `/commit` skill (`workflow:commit`) is active, you are
explicitly authorised to stage files, run `git commit`, and push to the remote.

## Architecture workflow

Use the `architecture-design` skill for all work involving the architectural dossier,
StrictDoc requirements, or diagrams. It contains the complete three-artifact workflow
guide, the StrictDoc field reference, and diagram conventions (PlantUML + SVG).

## Testing standards

- Framework: `pytest`; run with `pytest` (venv activated).
- Every public function and class should have at least one test.
- Tests use real (minimal) BDF text snippets as inline strings or fixtures — do not mock the file format.
- Coverage target: 90%+ on `src/nastran_parser/`; run `pytest --cov` to measure.

## Linting and type checking

```
ruff check src/ tests/     # linting — errors should be fixed before merging; warnings acceptable
ruff format src/ tests/    # formatting — run before committing
mypy src/                  # strict type checking — errors should be fixed; new code must be fully typed
```

These are quality gates, not blockers for exploratory branches.

## NASTRAN card reference

Use the `nastran-card-structure` skill for all card lookups. It contains:

- Bulk Data format rules (small/large/free-field, field types, continuation lines)
- A card dependency map (element → property → material chains)
- Pre-extracted summaries for several nastran cards in `references/cards/*.md`
- A local Bulk Data PDF (`references/QRG-BULKDATA.pdf`) as fallback for unlisted cards — ask before reading it (high token cost)

**Which cards to implement:** specified as requirements in `architecture/requirements/`. Do not implement a card without a corresponding `FR-` UID.

nastran-parser targets **Bulk Data** cards only unless a requirement explicitly specifies otherwise.
