---
name: architecture-design
description: |
  Use when the user is working on the architectural dossier, system design,
  requirements, or diagrams. Triggers for: architectural dossier, design workflow,
  three-artifact workflow, StrictDoc, FR-, NFR-, sdoc, .sdoc, REQUIREMENT,
  STATEMENT, ACCEPTANCE_CRITERIA, MEANS_OF_COMPLIANCE, FUNCTIONS field, MID,
  UID, DRAFT, IN_WORK, ACCEPTED, IMPLEMENTED, functional requirement,
  non-functional requirement, system design session, Q&A design session,
  actor/action, workflow, logical design, functional breakdown, physical design,
  PlantUML diagram, .puml, SVG export, diagram auto-export, plantuml skill,
  module name sync, architecture/architectural_dossier.md,
  architecture/requirements/, architecture/diagrams/.
version: 1.0.0
---

# Architecture Design Skill

This skill governs the three-artifact architecture workflow used in this project.
Read this skill in full before touching the dossier, any `.sdoc` file, or any `.puml` file.

---

## Three-Artifact Overview

| Artifact | Location | Purpose | Edit target |
|---|---|---|---|
| Architectural Dossier | `architecture/architectural_dossier.md` | Living design document: Actor/Action, Workflows, diagram image links | Yes — prose and image links |
| Requirements | `architecture/requirements/*.sdoc` | FR-N and NFR-N requirement records | Yes — add/edit `[REQUIREMENT]` blocks |
| Diagrams | `architecture/diagrams/*.puml` | PlantUML source for Logical Design and Functional Breakdown | Yes — edit `.puml`; run `export_puml.py` to produce SVG |

**SVG files** in `architecture/diagrams/` are generated output — never edit them directly.
**Dossier** contains `![Label](diagrams/X.svg)` image links — never embed diagram code in the dossier.

---

## Dossier Structure

The dossier has five sections in this fixed order:

1. **Actor/Action & Workflow** — who acts, what they do, and the stage-by-stage processing paths.
2. **Logical Design** — pipeline boundary diagram. Image link to `diagrams/logical_design.svg`.
3. **Functional Breakdown** — component hierarchy diagram. Image link to `diagrams/functional_breakdown.svg`.
4. **Requirements** — link to `requirements/requirements.md` (generated Markdown preview) and live-server instructions. No embedded requirement text.
5. **Physical Design** — placeholder until module structure stabilises.

To start a new dossier from scratch: read `references/dossier-template.md` and write it to `architecture/architectural_dossier.md`.

---

## Q&A Session Protocol

When asked to create or extend the architectural dossier, drive this 10-step interaction:

1. **System name and problem** — "What is the system name? What problem does it solve?" Produces the dossier header.
2. **Actors and actions** — "Who are the actors? System-only or user + system? List all actions the system performs." Produces the Actor/Action table.
3. **Workflows stage-by-stage** — "Walk me through each workflow. What are the named stages?" One `#### Workflow N` subsection per flow. Offer to draft if the user is unsure.
4. **Derive logical pipeline stages** — Summarise: "From these workflows I see these logical stages: X, Y, Z. Does that match?" Confirm before proceeding.
5. **Draft Logical Design component diagram** — Invoke the `plantuml` skill. Read `references/diagram-conventions.md`. Show the draft `@startuml` block for user review **before** writing the file. External sources/sinks outside the `package` boundary; internal stages inside. On user approval: write `architecture/diagrams/logical_design.puml`, then run `python .claude/skills/architecture-design/scripts/export_puml.py architecture/diagrams/logical_design.puml` to produce `logical_design.svg`. Then add the image link to the dossier's `## Logical Design` section.
6. **Derive component IDs** — Propose `ABBREV-N` IDs for each leaf function under each stage. Confirm abbreviations with the user.
7. **Draft Functional Breakdown WBS diagram** — Invoke the `plantuml` skill. Read `references/diagram-conventions.md`. Show the draft `@startwbs` block for review. Leaf nodes use `***_` (no box, stacked vertically). On approval: write `architecture/diagrams/functional_breakdown.puml`, then run `python .claude/skills/architecture-design/scripts/export_puml.py architecture/diagrams/functional_breakdown.puml` to produce `functional_breakdown.svg`. Add image link to dossier's `## Functional Breakdown` section.
8. **Draft functional requirements per function ID** — Read `references/sdoc-grammar.md`. For each function ID in the approved WBS (in WBS order), scan `architecture/requirements/functional_requirements.sdoc` for any existing `[REQUIREMENT]` whose `FUNCTIONS` field includes that ID. Present proposals grouped by stage — mark existing FRs as `(existing) UID — TITLE`; for uncovered functions propose all mandatory fields (TITLE, STATEMENT, ACCEPTANCE_CRITERIA, MEANS_OF_COMPLIANCE). Ask: "Reply with (a) approve all, (b) edit specific items, or (c) add additional requirements." On approval: write new `[REQUIREMENT]` blocks to `functional_requirements.sdoc` (fresh UUID, next sequential UID, `STATUS: DRAFT`; never modify existing FRs). Then run `python .claude/skills/architecture-design/scripts/generate_requirements_md.py` and confirm `architecture/requirements/requirements.md` was updated. Add the `## Requirements` section to the dossier (link to `requirements/requirements.md` + live-server instructions). Stage both the `.sdoc` file and `requirements.md` for the user to commit.
9. **Non-functional properties** — "Are there known NFR properties: performance, memory, distribution, modularity?" Seeds NFR requirements.
10. **Physical Design** — Leave as placeholder; note in the dossier that diagrams will be added once module structure stabilises.

---

## PlantUML Diagram Workflow

**Before writing any `.puml` content:**
1. Invoke the `plantuml` skill.
2. Read `references/diagram-conventions.md`.

**Logical Design** uses a component diagram (`@startuml` / `@enduml`).
**Functional Breakdown** uses a WBS diagram (`@startwbs` / `@endwbs`) with `***_` leaf nodes.

After writing a `.puml` file, run the export command:

```
python .claude/skills/architecture-design/scripts/export_puml.py architecture/diagrams/<file>.puml
```

This produces the SVG in the same directory. To regenerate all diagrams, pass `--all`.

Immediately after the SVG is produced, add or update the image link in the dossier:

```markdown
![Logical Design](diagrams/logical_design.svg)
<!-- Source: architecture/diagrams/logical_design.puml — edit the source, then run export_puml.py. -->
```

---

## Module Name Sync Rule

The `**` stage names in `functional_breakdown.puml` **must always match** the component labels in `logical_design.puml`.

When a stage name changes:
1. Update `logical_design.puml`.
2. Update `functional_breakdown.puml` (the `**` entry).
3. Update component IDs if the abbreviation changes — also update all `FUNCTIONS` field values in every `.sdoc` file that reference the old component IDs.
4. Update any prose in the dossier that names the stage.
5. Run `python .claude/skills/architecture-design/scripts/export_puml.py --all` to regenerate both SVGs.
6. All changes go in the same commit.

See `references/diagram-conventions.md` for the step-by-step procedure.

---

## StrictDoc Requirements

**Before adding or editing any requirement:** read `references/sdoc-grammar.md`.

Key rules:
- `MID`: generate a fresh UUID hex: `python -c "import uuid; print(uuid.uuid4().hex)"`
- `UID`: next sequential integer in the file (`FR-12` if highest is `FR-11`)
- `STATUS`: new requirements always start as `DRAFT`
- Multi-line field values use `>>>` / `<<<` delimiters
- `FUNCTIONS`: comma-separated component IDs linking to the Functional Breakdown (e.g. `INT-1, ANL-2`); omit when there is no clear mapping
- SEVERITY and OBLIGATION are optional — omit rather than guess
- Reference a UID in code only when the mapping is non-obvious (module docstring or inline comment)

StrictDoc server: `.venv\Scripts\activate` then `strictdoc server .` → `http://localhost:8080`

---

## Requirements Markdown

After Claude writes or edits any `.sdoc` file, run:
```
python .claude/skills/architecture-design/scripts/generate_requirements_md.py
```
This regenerates `architecture/requirements/requirements.md`. Stage both files together for the user to commit.

The dossier's `## Requirements` section links to `requirements/requirements.md`, which renders natively on GitHub and in VS Code without a server.

---

## Diagram Conventions Summary

| Rule | Detail |
|---|---|
| Edit target | `.puml` source files only |
| SVG export | Run `export_puml.py <file.puml>` after each `.puml` edit |
| Dossier references | `![Label](diagrams/X.svg)` image links only — no embedded code |
| Logical Design | Component diagram; external sources/sinks outside package boundary |
| Functional Breakdown | WBS diagram; `***_` leaf nodes (no box, stacked vertically) |
| `@startuml` name | Must match the `.puml` filename stem so the SVG has the correct name |

See `references/diagram-conventions.md` for full rules and anti-patterns.

---

## Reference Files Index

| File | Load when |
|---|---|
| `references/sdoc-grammar.md` | Adding or editing any `[REQUIREMENT]` block |
| `references/dossier-template.md` | Starting a new dossier from scratch |
| `references/diagram-conventions.md` | Creating or editing any `.puml` diagram |
