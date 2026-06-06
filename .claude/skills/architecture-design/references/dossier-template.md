# Architectural Dossier
<!-- Replace this line with the system name -->

---

## Actor/Action & Workflow

<!-- Identify all actors. For system-only operation state that explicitly. -->
<!-- List all actions the system performs, numbered. -->

### Actors and Actions

Identified actors: <!-- e.g. "system only" or "user, system" -->

| # | Action |
|---|--------|
| 1 | <!-- e.g. Read BDF from filesystem / network --> |
| 2 | |

<!-- Add one Workflow subsection per distinct processing path. -->

### Workflows

#### Workflow 1 — <!-- name, e.g. "Read from data stream" -->

<!-- Describe each stage of the workflow as a numbered step. -->
<!-- Stage 1 → Stage 2 → ... → Return result -->

---

## Logical Design

<!-- Component diagram: external sources/sinks outside the package boundary,
     internal pipeline stages inside. Rendered from the .puml source file. -->

![Logical Design](diagrams/logical_design.svg)

<!-- Source: architecture/diagrams/logical_design.puml
     Diagram type: component diagram (@startuml / @enduml)
     Edit the .puml file; the SVG re-exports automatically on save. -->

---

## Functional Breakdown

<!-- WBS diagram: root → stage (must match Logical Design) → leaf components (ABBREV-N).
     Leaf nodes use ***_ (no box). Rendered from the .puml source file. -->

![Functional Breakdown](diagrams/functional_breakdown.svg)

<!-- Source: architecture/diagrams/functional_breakdown.puml
     Diagram type: WBS diagram (@startwbs / @endwbs)
     Edit the .puml file; the SVG re-exports automatically on save.
     Module names at ** level must match Logical Design stage labels exactly. -->

---

## Requirements

<!-- Requirements are maintained in architecture/requirements/*.sdoc (StrictDoc format).
     The static HTML export is committed at architecture/requirements-html/html/ and
     regenerates automatically when Claude edits a .sdoc file (PostToolUse hook).
     After manual edits: run "strictdoc export . --output-dir architecture/requirements-html"
     (venv activated) then commit architecture/requirements-html/html/ alongside the .sdoc change. -->

**Browse (static HTML):** [requirements report](requirements-html/html/index.html)

**Browse (live server with edit UI):**
```
.venv\Scripts\activate
strictdoc server .
```
Then open http://localhost:8080

<!-- Every function ID from the Functional Breakdown must have at least one FR
     in architecture/requirements/functional_requirements.sdoc. -->

---

## Physical Design

*Diagrams will be added as exports from `architecture/diagrams/` once the module structure stabilises.*

<!-- Add image links here as implementation progresses:
     ![Module Layout](diagrams/physical_design.svg) -->
