"""Generate architecture/requirements/requirements.md from .sdoc source files."""
from __future__ import annotations

import os
import re
from pathlib import Path


def _find_project_root(start: Path) -> Path:
    markers = ("pyproject.toml", "package.json", "Cargo.toml", "go.mod", ".git")
    for p in [start, *start.parents]:
        if any((p / m).exists() for m in markers):
            return p
    raise FileNotFoundError(
        "Could not find project root — run the script from within a project directory"
    )


PROJECT_ROOT = _find_project_root(Path.cwd())
REQUIREMENTS_DIR = PROJECT_ROOT / "architecture" / "requirements"
OUTPUT_FILE = REQUIREMENTS_DIR / "requirements.md"

_SCRIPT_REL = os.path.relpath(Path(__file__).resolve(), Path.cwd())

_BLOCK_RE = re.compile(r"^\[(\w+)\]$")
_FIELD_RE = re.compile(r"^(\w+):\s*(.*)")


def parse_sdoc_file(path: Path) -> tuple[str, list[dict[str, str]]]:
    """Return (document_title, list_of_requirement_dicts)."""
    lines = path.read_text(encoding="utf-8").splitlines()

    doc_title = ""
    requirements: list[dict[str, str]] = []
    block_type: str | None = None
    current: dict[str, str] = {}
    current_field: str | None = None
    multiline_buf: list[str] = []

    def flush_multiline() -> None:
        nonlocal current_field
        if current_field:
            current[current_field] = "\n".join(multiline_buf).strip()
        current_field = None
        multiline_buf.clear()

    def flush_block() -> None:
        nonlocal doc_title
        flush_multiline()
        if block_type == "DOCUMENT":
            doc_title = current.get("TITLE", "")
        elif block_type == "REQUIREMENT" and "UID" in current:
            requirements.append(dict(current))

    for line in lines:
        stripped = line.strip()

        m_block = _BLOCK_RE.match(stripped)
        if m_block:
            flush_block()
            block_type = m_block.group(1)
            current = {}
            current_field = None
            multiline_buf.clear()
            continue

        if block_type not in ("DOCUMENT", "REQUIREMENT"):
            continue

        if current_field is not None:
            if stripped == "<<<":
                flush_multiline()
            else:
                multiline_buf.append(line.rstrip())
        else:
            m_field = _FIELD_RE.match(stripped)
            if not m_field:
                continue
            fname, fval = m_field.group(1), m_field.group(2).strip()
            if fval == ">>>":
                current_field = fname
                multiline_buf.clear()
            else:
                current[fname] = fval

    flush_block()
    return doc_title, requirements


def _md_table_row(*cells: str) -> str:
    return "| " + " | ".join(cells) + " |"


def generate_markdown(docs: list[tuple[str, list[dict[str, str]]]]) -> str:
    out: list[str] = [
        "# Requirements",
        "",
        "> Auto-generated — do not edit directly.",
        "> Source: `architecture/requirements/*.sdoc`",
        f"> To update: run `python {_SCRIPT_REL}`",
        "> Live edit UI: `.venv\\Scripts\\activate` then `strictdoc server .` → http://localhost:8080",
        "",
    ]

    for doc_title, requirements in docs:
        out += ["---", "", f"## {doc_title}", ""]

        # Summary table
        out += [
            _md_table_row("UID", "Title", "Status", "Functions"),
            _md_table_row("---", "---", "---", "---"),
        ]
        for req in requirements:
            out.append(_md_table_row(
                req.get("UID", ""),
                req.get("TITLE", ""),
                req.get("STATUS", ""),
                req.get("FUNCTIONS", ""),
            ))
        out.append("")

        # Detail sections
        for req in requirements:
            uid = req.get("UID", "")
            title = req.get("TITLE", "")
            status = req.get("STATUS", "")
            funcs = req.get("FUNCTIONS", "")

            out += [f"### {uid} — {title}", ""]

            meta: list[str] = [f"**Status:** {status}"]
            if funcs:
                meta.append(f"**Functions:** {funcs}")
            out += [" | ".join(meta), ""]

            for field_key, label in (
                ("STATEMENT", "Statement"),
                ("ACCEPTANCE_CRITERIA", "Acceptance Criteria"),
                ("MEANS_OF_COMPLIANCE", "Means of Compliance"),
            ):
                body = req.get(field_key, "").strip()
                if body:
                    out += [f"**{label}:**", "", body, ""]

            out += ["---", ""]

    return "\n".join(out)


def main() -> None:
    sdoc_files = sorted(REQUIREMENTS_DIR.glob("*.sdoc"))
    docs: list[tuple[str, list[dict[str, str]]]] = []
    for sdoc in sdoc_files:
        title, reqs = parse_sdoc_file(sdoc)
        if title and reqs:
            docs.append((title, reqs))

    OUTPUT_FILE.write_text(generate_markdown(docs), encoding="utf-8")
    print(f"Written: {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
