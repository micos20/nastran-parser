# Requirements

> Auto-generated — do not edit directly.
> Source: `architecture/requirements/*.sdoc`
> To update: run `python .claude\skills\architecture-design\scripts\generate_requirements_md.py`
> Live edit UI: `.venv\Scripts\activate` then `strictdoc server .` → http://localhost:8080

---

## Functional Requirements

| UID | Title | Status | Functions |
| --- | --- | --- | --- |
| FR-1 | Read BDF from filesystem | DRAFT | INT-1 |
| FR-2 | Read BDF from network | DRAFT | INT-1 |
| FR-3 | Interpret NASTRAN card stream | DRAFT | INT-1, INT-2, INT-3 |
| FR-4 | Modify card field values | DRAFT | INT-3 |
| FR-5 | Write BDF to filesystem | DRAFT | EXP-1, EXP-2 |
| FR-6 | Write BDF to network | DRAFT | EXP-1, EXP-2 |
| FR-7 | Track file content summary | DRAFT | ANL-1, ANL-2, ANL-3 |
| FR-8 | Chunked stream processing | DRAFT | INT-1 |
| FR-9 | Task-based pipeline configuration | DRAFT |  |
| FR-10 | Renumber card IDs | DRAFT | RNB-1, RNB-2 |
| FR-11 | ID mapping table | DRAFT | RNB-3 |

### FR-1 — Read BDF from filesystem

**Status:** DRAFT | **Functions:** INT-1

**Statement:**

The system shall read BDF input files from the local filesystem as a data stream.

**Acceptance Criteria:**

A BDF file on the local filesystem can be opened and its content streamed card by card
through the pipeline. The file is not fully loaded into memory at any point.

**Means of Compliance:**

Implement a FileSystemSource class that opens files using Python buffered I/O and yields
card-aligned chunks on demand via the iterator protocol.

---

### FR-2 — Read BDF from network

**Status:** DRAFT | **Functions:** INT-1

**Statement:**

The system shall read BDF input from a URL or REST endpoint as a data stream.

**Acceptance Criteria:**

A BDF file served over HTTP can be streamed through the pipeline without downloading
the complete file first. The source yields data as the network delivers it.

**Means of Compliance:**

Implement a NetworkSource class using an HTTP client with streaming enabled (e.g.
httpx with stream=True), yielding card-aligned chunks as they arrive.

---

### FR-3 — Interpret NASTRAN card stream

**Status:** DRAFT | **Functions:** INT-1, INT-2, INT-3

**Statement:**

The system shall parse and validate NASTRAN card content from a chunked data stream,
identifying card type, extracting field values, and validating field types.

**Acceptance Criteria:**

Given a stream of BDF content, the interpreter correctly identifies all card types,
extracts every field value, and rejects fields whose values do not match the declared
type (Integer, Real, or Character). Continuation lines are assembled into a single card.

**Means of Compliance:**

Implement a card interpreter that detects small-field, large-field, and free-field
formats per card. Use card definitions to extract and type-validate each field.
Accumulate continuation lines before dispatching the completed card downstream.

---

### FR-4 — Modify card field values

**Status:** DRAFT | **Functions:** INT-3

**Statement:**

The system shall allow modification of individual field values on a parsed NASTRAN card.

**Acceptance Criteria:**

A field value on a parsed card can be updated programmatically. The change is reflected
when the card is subsequently serialized. Assignment of a value with an incompatible
type raises a descriptive error.

**Means of Compliance:**

Expose mutable field attributes on each typed card class. Validate the new value against
the field type constraint on assignment and raise a TypeError with the field name and
expected type if the constraint is violated.

---

### FR-5 — Write BDF to filesystem

**Status:** DRAFT | **Functions:** EXP-1, EXP-2

**Statement:**

The system shall serialize and write BDF output to the local filesystem.

**Acceptance Criteria:**

A sequence of card objects can be serialized to a file. The resulting BDF file is
parseable as valid input by the same parser without errors or data loss.

**Means of Compliance:**

Implement a FileSystemSink class that serializes each card back to its original format
(small-field, large-field, or free-field) and writes to a file using buffered I/O,
flushing on completion.

---

### FR-6 — Write BDF to network

**Status:** DRAFT | **Functions:** EXP-1, EXP-2

**Statement:**

The system shall serialize and stream BDF output to a URL or REST endpoint.

**Acceptance Criteria:**

A sequence of card objects can be serialized and sent to an HTTP endpoint without
buffering the complete output in memory. The endpoint receives valid BDF content.

**Means of Compliance:**

Implement a NetworkSink class that streams serialized card data to a URL via HTTP using
chunked transfer encoding, writing each card as it is received from the upstream stage.

---

### FR-7 — Track file content summary

**Status:** DRAFT | **Functions:** ANL-1, ANL-2, ANL-3

**Statement:**

The system shall record the card type and card ID for every card encountered during
stream processing and return a file summary upon stream completion.

**Acceptance Criteria:**

After processing a BDF stream, the returned FileSummary lists every distinct card type
encountered, the total count per type, and the ID of each individual card. The summary
is correct even when the stream is processed in a single pass without re-reading.

**Means of Compliance:**

Accumulate a FileSummary data structure during stream processing. Each interpreted card
contributes its type and ID to the summary before being forwarded to the next stage.
Return the completed summary when the stream is exhausted.

---

### FR-8 — Chunked stream processing

**Status:** DRAFT | **Functions:** INT-1

**Statement:**

The system shall process BDF input in chunks without loading the complete file into memory.
The chunk boundary shall align to card boundaries (not byte offsets).

**Acceptance Criteria:**

Processing a BDF file larger than available RAM completes successfully. Peak memory usage
measured by a memory profiler does not grow proportionally with file size.

**Means of Compliance:**

Implement the processing pipeline as a Python generator chain. Each stage yields one
card at a time and holds no references to previously yielded cards. Chunk boundaries
are determined by detecting the end of a complete card (including continuation lines).

---

### FR-9 — Task-based pipeline configuration

**Status:** DRAFT

**Statement:**

The system shall configure the processing pipeline via a task type supplied by the caller
at the start of a stream (e.g. read-only, renumber).

**Acceptance Criteria:**

The same pipeline infrastructure executes a read-only task and a renumber task when
supplied with the respective task descriptor, without any code change between runs.
Different task types produce the correct sequence of pipeline stages.

**Means of Compliance:**

Implement a pipeline factory that assembles the ordered list of stages based on the
supplied task descriptor before the stream is opened. Each task type maps to a fixed
stage composition defined in the factory.

---

### FR-10 — Renumber card IDs

**Status:** DRAFT | **Functions:** RNB-1, RNB-2

**Statement:**

The system shall renumber card IDs according to a caller-supplied ruleset during stream
processing, generating new IDs from defined number ranges.

**Acceptance Criteria:**

Given a renumbering ruleset, all card IDs in the output BDF fall within the specified
target ranges. IDs that cross-reference other cards are updated consistently so the
output BDF remains internally coherent.

**Means of Compliance:**

Implement a RenumberStage that loads the ruleset, maintains a counter per target range,
and maps each original ID to the next available ID in the corresponding range. Apply
the mapping to all ID fields of each card before forwarding it downstream.

---

### FR-11 — ID mapping table

**Status:** DRAFT | **Functions:** RNB-3

**Statement:**

The system shall maintain a lookup table mapping old card IDs to new card IDs during
renumbering, returned as part of the file summary on stream completion.

**Acceptance Criteria:**

The FileSummary returned after a renumber operation contains a complete mapping of every
original card ID to its assigned new ID. The mapping covers all card types that carry IDs.

**Means of Compliance:**

Maintain a dictionary in RenumberStage keyed by original ID and updated as each card
is processed. Include the completed mapping in the FileSummary returned on stream
completion.

---

---

## Non-Functional Requirements

| UID | Title | Status | Functions |
| --- | --- | --- | --- |
| NFR-1 | Processing performance | DRAFT |  |
| NFR-2 | Memory efficiency | DRAFT |  |
| NFR-3 | Adaptive memory consumption | DRAFT |  |
| NFR-4 | Modularity | DRAFT |  |
| NFR-5 | PyPI distribution | DRAFT |  |

### NFR-1 — Processing performance

**Status:** DRAFT

**Statement:**

The system shall process BDF streams with minimal CPU overhead, enabling handling of
large models without significant impact on overall execution time.

**Acceptance Criteria:**

A 100 MB BDF file is fully processed (read, interpreted, summary returned) in under
10 seconds on a modern laptop running Python 3.12. CPU utilisation during processing
does not exceed single-core capacity on the hot path.

**Means of Compliance:**

Use Python generator pipelines to eliminate intermediate allocations. Profile critical
parsing paths and apply targeted optimisations such as compiled regex patterns and
struct-based unpacking for fixed-width fields.

---

### NFR-2 — Memory efficiency

**Status:** DRAFT

**Statement:**

The system shall maintain a minimal memory footprint during stream processing,
avoiding accumulation of data beyond what is required for the current processing step.

**Acceptance Criteria:**

Peak memory usage measured by a memory profiler while processing a 1 GB BDF file does
not exceed a configurable budget (default 128 MB). Memory usage does not grow
proportionally with file size.

**Means of Compliance:**

Implement the pipeline as a generator chain so no stage holds references to previously
yielded cards. Use __slots__ on card classes to minimise per-object overhead. Release
references to completed cards immediately after they are forwarded downstream.

---

### NFR-3 — Adaptive memory consumption

**Status:** DRAFT

**Statement:**

The system shall dynamically adjust its memory consumption in response to the rate
and volume of incoming data, preventing unbounded memory growth.

**Acceptance Criteria:**

When a downstream stage processes cards more slowly than the source produces them,
the source reads no further ahead than one configured buffer. Memory usage under
back-pressure remains bounded and does not increase over time.

**Means of Compliance:**

Leverage Python generator back-pressure: the source only advances to the next chunk
when the downstream consumer calls next() on the iterator. No intermediate buffer or
queue is inserted between stages unless explicitly configured.

---

### NFR-4 — Modularity

**Status:** DRAFT

**Statement:**

The system shall support the addition of new processing pipeline stages without
requiring modification of existing stages or the core stream infrastructure.

**Acceptance Criteria:**

A new pipeline stage can be implemented, registered, and wired into a workflow by
adding a single class and a task descriptor entry, with no changes to existing stage
classes or the pipeline runner. Existing workflows continue to pass their tests.

**Means of Compliance:**

Define a PipelineStage abstract base class (or Protocol) with a standard
process(cards: Iterator[Card]) -> Iterator[Card] interface. The pipeline factory
assembles stages by composition based on the task descriptor, with no hard-coded
stage references in the runner.

---

### NFR-5 — PyPI distribution

**Status:** DRAFT

**Statement:**

The system shall be published as a Python package on PyPI and be installable via
pip or uv without additional build steps.

**Acceptance Criteria:**

pip install nastran-parser succeeds on Python 3.12+ on Windows, macOS, and Linux
without requiring a compiler or any system-level dependencies. The installed package
is importable immediately after installation.

**Means of Compliance:**

Maintain a pure-Python implementation with no C extensions or compiled dependencies.
Use uv build to produce a wheel and sdist, and uv publish to upload to PyPI. Automate
publishing via CI on tagged releases.

---
