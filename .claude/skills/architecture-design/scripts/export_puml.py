"""Export a PlantUML .puml file to SVG using plantuml CLI or plantuml.jar."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _find_project_root(start: Path) -> Path:
    markers = ("pyproject.toml", "package.json", "Cargo.toml", "go.mod", ".git")
    for p in [start, *start.parents]:
        if any((p / m).exists() for m in markers):
            return p
    raise FileNotFoundError(
        "Could not find project root — run the script from within a project directory"
    )


def _find_plantuml() -> tuple[str, list[str]]:
    """Return (mode, command_prefix) where mode is 'cli' or 'jar'."""
    # Prefer plantuml on PATH (cross-platform, no Java invocation needed)
    if shutil.which("plantuml"):
        return "cli", ["plantuml"]

    env_path = __import__("os").environ.get("PLANTUML_JAR")
    if env_path:
        jar = Path(env_path)
        if jar.is_file():
            return "jar", ["java", "-jar", str(jar)]
        sys.exit(f"PLANTUML_JAR={env_path!r} does not point to a file")

    home = Path.home()
    candidates: list[Path] = []

    # Windows — VS Code extension
    candidates += sorted(
        home.glob(".vscode/extensions/jebbs.plantuml-*/plantuml.jar"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    # macOS — VS Code extension (same path on macOS)
    if not candidates:
        candidates += sorted(
            home.glob("Library/Application Support/Code/User/extensions/jebbs.plantuml-*/plantuml.jar"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
    # standalone jar in common locations
    for candidate in [home / "plantuml.jar", Path("/usr/local/lib/plantuml.jar")]:
        if candidate.is_file():
            candidates.append(candidate)

    if candidates:
        return "jar", ["java", "-jar", str(candidates[0])]

    sys.exit(
        "plantuml not found.\n"
        "Options:\n"
        "  1. Put 'plantuml' on your PATH (e.g. brew install plantuml)\n"
        "  2. Set PLANTUML_JAR=/path/to/plantuml.jar\n"
        "  3. Install the VS Code PlantUML extension (jebbs.plantuml)"
    )


def export(puml_file: Path, cmd_prefix: list[str]) -> None:
    out_dir = puml_file.parent
    result = subprocess.run(
        [*cmd_prefix, "-tsvg", "-o", str(out_dir), str(puml_file)],
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

    _, cmd_prefix = _find_plantuml()

    if args.all:
        project_root = _find_project_root(Path.cwd())
        diagrams_dir = project_root / "architecture" / "diagrams"
        puml_files = sorted(diagrams_dir.glob("*.puml"))
        if not puml_files:
            sys.exit(f"No .puml files found in {diagrams_dir}")
        for f in puml_files:
            export(f, cmd_prefix)
    else:
        puml_file = Path(args.file).resolve()
        if not puml_file.is_file():
            sys.exit(f"File not found: {args.file}")
        export(puml_file, cmd_prefix)


if __name__ == "__main__":
    main()
