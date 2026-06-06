# Architectural Dossier
nastran-parser

---

## Actor/Action & Workflow

The actors, actions, and workflows are the basis for identifying the main modules and submodules of the system.

### Actors and Actions

Identified actors: **system only**

| # | Action |
|---|--------|
| 1 | Read BDF files from the local filesystem |
| 2 | Read BDF files from a network source (URL, REST endpoint) |
| 3 | Interpret NASTRAN card content from a stream and assign to internal data structures |
| 4 | Process BDF input as a data stream without loading the complete file into memory |
| 5 | Modify field values of NASTRAN cards |
| 6 | Write or stream BDF output to the local filesystem |
| 7 | Write or stream BDF output to a URL or REST API |
| 8 | Track card types and IDs encountered during processing and provide a file summary |

### Workflows

#### Workflow 1 — Read from data stream

**Stage 1 — Receive Stream**
- Accept incoming BDF data stream
- Determine task type: read-only
- Forward stream to interpreter

**Stage 2 — Interpret**
- Identify NASTRAN card type and format
- Extract field values
- Validate field types against card definition
- Assign values to internal card representation
- Record card type and ID in file summary
- Forward card to next stage

**Result:** Return file summary on stream completion

---

#### Workflow 2 — Renumber from data stream

**Stage 1 — Receive Stream**
- Accept incoming BDF data stream
- Determine task type: renumber
- Load renumbering ruleset
- Forward stream to interpreter

**Stage 2 — Interpret**
*(identical to Workflow 1, Stage 2)*

**Stage 3 — Renumber**
- Load ruleset defining target ID number ranges
- Extract card ID
- Generate next valid ID within the target range
- Record old → new ID mapping in lookup table
- Update card with new ID
- Forward card to next stage

**Stage 4 — Write to Sink**
- Accept card from previous stage
- Serialize and write/stream card to target (filesystem or URL)

**Result:** Return file summary (including renumbered ID mapping) on stream completion

---

*Further workflows will be added as requirements are defined.*

---

## Logical Design

From the actor/actions list we can derive the main software components inside the library
boundary and the external producers/consumers that connect to it.

Pipeline stages (inside nastran-parser boundary):

- **Interpreter** — assembles raw text lines into complete cards and instantiates typed card models
- **Analyzer** — transparent pass-through that accumulates the file summary
- **Renumberer** — remaps card IDs (renumber task only)
- **Exporter** — serialises card models back to BDF text lines

> **Note on Validator tester:** The original Excalidraw diagram shows a separate "Validator tester"
> stage. Based on the architectural decision to use Pydantic models, validation (type coercion,
> required-field checks, value constraints) is embedded inside the Interpreter at model-construction
> time. There is no separate runtime stage. The Excalidraw source should be updated to reflect this.

![Logical Design](diagrams/logical_design.svg)

<!-- Source: architecture/diagrams/logical_design.puml — edit the source; SVG re-exports automatically on save. -->

---

## Functional Breakdown

![Functional Breakdown](diagrams/functional_breakdown.svg)

<!-- Source: architecture/diagrams/functional_breakdown.puml — edit the source; SVG re-exports automatically on save. -->

> The **analyzer** runs on every BDF read. It profiles the file — counting cards and recording
> the ID ranges currently in use per card type — so the `FileSummary` is complete and usable
> as-is for a read-only task or as input to a subsequent renumber operation.

---

## Physical Design

*Diagrams will be added as PlantUML exports from `architecture/diagrams/` once the module structure stabilises.*
