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

Diagrams are authored in Excalidraw (source files in `architecture/diagrams/`) and exported as Mermaid, then embedded directly in `architecture/architectural_dossier.md`.
Use fenced Mermaid blocks: ` ```mermaid ... ``` `

Do not edit Mermaid blocks manually unless correcting a rendering issue.

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

## NASTRAN 2025.1 Quick Reference Guide (QRG)

Before using the following url please use the reference documents in the nastran-card-structure SKILL.
A reduced version of this file containing only the BULK DATA ENTRIES can also found in the skill references.

**URL:** https://nexus.hexagon.com/documentationcenter/en-US/bundle/MSC_Nastran_2025.1_Quick_Reference_Guide/resource/MSC_Nastran_2025.1_Quick_Reference_Guide.pdf

### Purpose
The QRG is the authoritative source for card definitions. Fetch it with WebFetch when you need to look up a specific card. Each card section contains:

- **Description** — what the card does
- **Format** — fixed-field (small/large) or free-field layout
- **Fields table** — field position, name, type (Integer/Real/Character), default, constraints

### Which cards to implement
Cards to implement are specified as requirements in `architecture/requirements/`. Do not implement a card without a corresponding `FR-` UID.

### How to extract card information from the QRG

1. Fetch the PDF from the URL above (use WebFetch).
2. Search for the card name (e.g. `GRID`, `CBAR`, `MAT1`) — cards are alphabetical within sections.
3. Locate the **Format** subsection — column layout:
   - Small field: 10 fields × 8 characters per line
   - Large field: 5 fields × 16 characters per line (card name ends with `*`)
   - Free field: comma-separated values
4. Locate the **Fields** table — each row: field position, name, type, default, constraints.
5. Record this structure in the corresponding requirement `STATEMENT` block.

### QRG navigation notes
- nastran-parser targets **Bulk Data** cards only unless a requirement explicitly specifies otherwise.
- Some cards span continuation lines (field 1 = `+` or blank for small field; `*` for large field) — track these during parsing.
- Sections: Bulk Data → alphabetical by card name.
