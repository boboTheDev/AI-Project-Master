#!/usr/bin/env python3
"""Create a Project Master bootstrap without overwriting existing project files."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path


LIBRARY_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = LIBRARY_ROOT / "templates" / "project"
PROJECT_NAME_TOKEN = "REPLACE_WITH_PROJECT_NAME"
LIBRARY_PATH_TOKEN = "REPLACE_WITH_ABSOLUTE_PATH_TO_PROJECT_MASTER"


@dataclass
class BootstrapResult:
    created: list[Path] = field(default_factory=list)
    preserved: list[Path] = field(default_factory=list)
    configured: list[Path] = field(default_factory=list)
    merge_required: list[Path] = field(default_factory=list)


def fail(message: str) -> None:
    raise ValueError(message)


def relative(path: Path, target: Path) -> str:
    try:
        return str(path.relative_to(target))
    except ValueError:
        return str(path)


def template_files() -> list[Path]:
    if not TEMPLATE_ROOT.is_dir():
        fail(f"Project template is missing: {TEMPLATE_ROOT}")
    return sorted(path for path in TEMPLATE_ROOT.rglob("*") if path.is_file())


def ensure_external_target(target: Path) -> None:
    if target == LIBRARY_ROOT or LIBRARY_ROOT in target.parents:
        fail("A managed project cannot be created inside the Project Master library.")


def preflight(mode: str, target: Path) -> None:
    ensure_external_target(target)
    if mode == "new":
        if target.exists() and not target.is_dir():
            fail(f"New-project target exists and is not a directory: {target}")
        if target.exists() and any(target.iterdir()):
            fail(
                f"New-project target is not empty: {target}. "
                "Use existing mode to preserve and integrate its contents."
            )
    elif not target.is_dir():
        fail(f"Existing-project target is not a directory: {target}")


def integration_is_present(path: Path, relative_path: Path) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8")
    expected = {
        Path("AGENTS.md"): ".project/README.md",
        Path("CLAUDE.md"): "@AGENTS.md",
        Path(".github/copilot-instructions.md"): ".project/README.md",
    }
    marker = expected.get(relative_path)
    return marker is not None and marker in content


def configure_bootstrap(target: Path, project_name: str, dry_run: bool, result: BootstrapResult) -> None:
    replacements = {
        target / ".project" / "project.yaml": {
            PROJECT_NAME_TOKEN: json.dumps(project_name, ensure_ascii=False),
        },
        target / ".project" / "README.md": {
            LIBRARY_PATH_TOKEN: str(LIBRARY_ROOT),
        },
    }
    for path, values in replacements.items():
        if not path.is_file() and not dry_run:
            fail(f"Required bootstrap file was not created: {path}")
        if dry_run and not path.exists():
            result.configured.append(path)
            continue
        content = path.read_text(encoding="utf-8")
        updated = content
        for token, value in values.items():
            updated = updated.replace(token, value)
        if updated != content:
            result.configured.append(path)
            if not dry_run:
                path.write_text(updated, encoding="utf-8")


def bootstrap(mode: str, target: Path, project_name: str, dry_run: bool) -> BootstrapResult:
    target = target.expanduser().resolve()
    preflight(mode, target)
    result = BootstrapResult()

    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    entry_files = {
        Path("AGENTS.md"),
        Path("CLAUDE.md"),
        Path(".github/copilot-instructions.md"),
    }
    for source in template_files():
        rel = source.relative_to(TEMPLATE_ROOT)
        destination = target / rel
        if destination.exists():
            if destination.is_dir():
                fail(f"Expected a file but found a directory: {destination}")
            result.preserved.append(destination)
            if rel in entry_files and not integration_is_present(destination, rel):
                result.merge_required.append(destination)
            continue
        result.created.append(destination)
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    configure_bootstrap(target, project_name, dry_run, result)
    return result


def print_result(target: Path, mode: str, dry_run: bool, result: BootstrapResult) -> None:
    prefix = "Bootstrap preview" if dry_run else "Bootstrap complete"
    print(f"{prefix}: {mode} project at {target.expanduser().resolve()}")
    for label, paths in (
        ("create", result.created),
        ("configure", result.configured),
        ("preserve", result.preserved),
    ):
        for path in paths:
            print(f"{label}: {relative(path, target.expanduser().resolve())}")
    for path in result.merge_required:
        print(f"merge-required: {relative(path, target.expanduser().resolve())}")
    if result.merge_required:
        print("Existing agent instructions were preserved. Merge the Project Master entry guidance into the listed files.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create and configure a Project Master bootstrap while preserving existing files."
    )
    parser.add_argument("mode", choices=("new", "existing"))
    parser.add_argument("--target", required=True, type=Path, help="Project directory")
    parser.add_argument("--name", help="Project display name; defaults to the target folder for existing projects")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.mode == "new" and not args.name:
        parser.error("new mode requires --name")
    if not args.name:
        args.name = args.target.expanduser().resolve().name
    if not args.name.strip():
        parser.error("project name cannot be empty")
    args.name = args.name.strip()
    return args


def main() -> int:
    args = parse_args()
    try:
        result = bootstrap(args.mode, args.target, args.name, args.dry_run)
        print_result(args.target, args.mode, args.dry_run, result)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
