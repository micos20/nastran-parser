"""Export a PlantUML .puml file to SVG using the local plantuml.jar."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _find_project_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "pyproject.toml").exists():
            return p
    raise FileNotFoundError("pyproject.toml not found — run from within the project tree")


def _find_plantuml_jar() -> Path:
    env_path = os.environ.get("PLANTUML_JAR")
    if env_path:
        jar = Path(env_path)
        if jar.is_file():
            return jar
        sys.exit(f"PLANTUML_JAR={env_path!r} does not point to a file")

    userprofile = os.environ.get("USERPROFILE", "")
    if userprofile:
        candidates = sorted(
            Path(userprofile).glob(".vscode/extensions/jebbs.plantuml-*/plantuml.jar"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if candidates:
            return candidates[0]

    sys.exit(
        "plantuml.jar not found.\n"
        "Set the PLANTUML_JAR environment variable to its absolute path, or\n"
        "install the VS Code PlantUML extension (jebbs.plantuml)."
    )


def export(puml_file: Path, jar: Path) -> None:
    out_dir = puml_file.parent
    result = subprocess.run(
        ["java", "-jar", str(jar), "-tsvg", "-o", str(out_dir), str(puml_file)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"plantuml failed for {puml_file}:\n{result.stderr}")
    svg = out_dir / (puml_file.stem + ".svg")
    print(f"Exported: {svg}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export .puml file(s) to SVG")
    parser.add_argument("file", nargs="?", help="Path to the .puml file to export")
    parser.add_argument("--all", action="store_true", help="Export all .puml files in architecture/diagrams/")
    args = parser.parse_args()

    if not args.all and not args.file:
        parser.error("Provide a .puml file path or pass --all")

    jar = _find_plantuml_jar()

    if args.all:
        project_root = _find_project_root(Path(__file__).resolve())
        diagrams_dir = project_root / "architecture" / "diagrams"
        puml_files = sorted(diagrams_dir.glob("*.puml"))
        if not puml_files:
            sys.exit(f"No .puml files found in {diagrams_dir}")
        for f in puml_files:
            export(f, jar)
    else:
        puml_file = Path(args.file).resolve()
        if not puml_file.is_file():
            sys.exit(f"File not found: {args.file}")
        export(puml_file, jar)


if __name__ == "__main__":
    main()
