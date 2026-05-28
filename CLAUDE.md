# nastran-parser — Developer Guide for Claude

## Project structure

```
nastran-parser/
├── src/nastran_parser/       # library source code
├── tests/                    # pytest tests (mirrors src/ tree)
├── architecture/
│   ├── requirements/         # StrictDoc .sdoc files (FR-, NFR-)
│   ├── diagrams/             # Excalidraw source files (.excalidraw)
│   └── architectural_dossier.md  # main architecture document
├── strictdoc_config.py       # StrictDoc project config
└── pyproject.toml            # all Python project config (tools, deps, metadata)
```

- Runtime library code lives exclusively under `src/nastran_parser/`.
- Dev dependencies are declared in `[dependency-groups] dev` in `pyproject.toml`.
- Python minimum: 3.12. `match`/`case` is available and preferred for card-type dispatch.

## Working with StrictDoc requirements

**Browse:** activate the venv (`.venv\Scripts\activate`), then run `strictdoc server .` from the repo root. Opens on http://localhost:8080.

**Before implementing** any feature (new card type, format variant, mutation behavior, write-back option), locate or create the corresponding requirement UID in `architecture/requirements/`.

- Functional requirements: `architecture/requirements/functional_requirements.sdoc` (prefix `FR-`)
- Non-functional requirements: `architecture/requirements/nonfunctional_requirements.sdoc` (prefix `NFR-`)
- Add new requirements to the `.sdoc` files; use the next available UID in sequence.
- Reference a UID in code only when the mapping is non-obvious (module docstring or single inline comment).

## Working with diagrams

Mermaid diagrams are embedded directly in `architecture/architectural_dossier.md`
using fenced ` ```mermaid ... ``` ` blocks. These are the authoritative diagrams.
Excalidraw files in `architecture/diagrams/` are used for sketching only and are
not the source of truth.

Do not edit Mermaid blocks manually unless correcting a rendering issue.

### Module name consistency

The **Logical Design** diagram and the **Functional Breakdown** diagram are related.
The module names used in both diagrams must always be identical. Whenever a module
name is added, removed, or renamed in one diagram, apply the same change to the other
diagram and the surrounding prose in the same commit.

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
