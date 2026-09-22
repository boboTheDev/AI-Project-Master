#!/usr/bin/env python3
"""Create a Project Master bootstrap without overwriting existing project files.

A managed project is a project root containing two sibling directories:
  <root>/.project-meta/   a private repository (project/ + prototype/)
  <root>/workspace/       the real implementation, a separate repository

This helper creates and configures .project-meta/. It creates an empty
workspace/ for a brand-new project. For backfill, it can either use an
already-arranged workspace/ or restructure a normal repository root in place
by moving its complete working tree, including .git, into workspace/.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


LIBRARY_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = LIBRARY_ROOT / "templates" / "project-meta"
PROJECT_NAME_TOKEN = "REPLACE_WITH_PROJECT_NAME"
LIBRARY_PATH_TOKEN = "REPLACE_WITH_ABSOLUTE_PATH_TO_PROJECT_MASTER"
META_DIR_NAME = ".project-meta"
WORKSPACE_DIR_NAME = "workspace"


@dataclass
class BootstrapResult:
    created: list[Path] = field(default_factory=list)
    preserved: list[Path] = field(default_factory=list)
    configured: list[Path] = field(default_factory=list)
    git_initialized: list[Path] = field(default_factory=list)
    moved: list[tuple[Path, Path]] = field(default_factory=list)


def fail(message: str) -> None:
    raise ValueError(message)


def relative(path: Path, target: Path) -> str:
    try:
        return str(path.relative_to(target))
    except ValueError:
        return str(path)


def template_files() -> list[Path]:
    if not TEMPLATE_ROOT.is_dir():
        fail(f"Project-meta template is missing: {TEMPLATE_ROOT}")
    return sorted(path for path in TEMPLATE_ROOT.rglob("*") if path.is_file())


def ensure_external_target(root: Path) -> None:
    if root == LIBRARY_ROOT or LIBRARY_ROOT in root.parents:
        fail("A managed project cannot be created inside the Project Master library.")


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def git_root(path: Path) -> Path | None:
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return Path(completed.stdout.strip()).resolve()


def git_snapshot(path: Path) -> tuple[bytes, bytes, bytes]:
    commands = (
        ["git", "-C", str(path), "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        ["git", "-C", str(path), "remote", "-v"],
        ["git", "-C", str(path), "rev-parse", "--verify", "HEAD"],
    )
    outputs: list[bytes] = []
    for index, command in enumerate(commands):
        completed = subprocess.run(command, capture_output=True, check=False)
        if completed.returncode != 0 and index != 2:
            fail(f"Unable to inspect existing git repository at {path}.")
        outputs.append(completed.stdout if completed.returncode == 0 else b"")
    return tuple(outputs)  # type: ignore[return-value]


def git_init(path: Path, dry_run: bool, result: BootstrapResult) -> None:
    if is_git_repo(path):
        return
    result.git_initialized.append(path)
    if dry_run:
        return
    completed = subprocess.run(
        ["git", "init", "--quiet", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"git init failed for {path}: {completed.stderr.strip()}")


def preflight(mode: str, root: Path) -> bool:
    ensure_external_target(root)
    meta_dir = root / META_DIR_NAME
    workspace_dir = root / WORKSPACE_DIR_NAME
    if meta_dir.exists() and not meta_dir.is_dir():
        fail(f"{META_DIR_NAME} exists and is not a directory: {meta_dir}")
    if workspace_dir.exists() and not workspace_dir.is_dir():
        fail(f"{WORKSPACE_DIR_NAME} exists and is not a directory: {workspace_dir}")
    if mode == "new":
        if meta_dir.exists() and any(meta_dir.iterdir()):
            fail(
                f"{meta_dir} already has content. Use existing mode to preserve and "
                "integrate it."
            )
        if workspace_dir.exists() and any(workspace_dir.iterdir()):
            fail(
                f"{workspace_dir} already has content. Use existing mode: this helper "
                "never modifies an existing workspace/."
            )
        return False
    if mode == "existing":
        if workspace_dir.is_dir() and any(workspace_dir.iterdir()):
            return False
        if not root.is_dir() or not any(root.iterdir()):
            fail(
                f"Existing mode expects either a populated {workspace_dir} or an "
                f"existing repository at {root}. Use new mode for a brand-new project."
            )
        if meta_dir.exists() or workspace_dir.exists():
            fail(
                f"Cannot restructure {root}: {META_DIR_NAME} or {WORKSPACE_DIR_NAME} "
                "already exists. Resolve the collision before backfill."
            )
        if git_root(root) != root:
            fail(f"Existing-project target is not a git repository root: {root}")
        if not (root / ".git").is_dir():
            fail(
                "Automatic restructuring currently requires a standalone repository "
                "with a .git directory; linked worktrees need a dedicated conversion."
            )
        return True
    return False


def restructure_existing_repository(root: Path, dry_run: bool, result: BootstrapResult) -> None:
    workspace_dir = root / WORKSPACE_DIR_NAME
    entries = sorted(root.iterdir(), key=lambda path: path.name)
    for entry in entries:
        result.moved.append((entry, workspace_dir / entry.name))
    result.created.append(workspace_dir)
    if dry_run:
        return

    before = git_snapshot(root)
    staging = root / ".project-master-workspace-staging"
    if staging.exists():
        fail(f"Workspace staging path already exists: {staging}")
    staging.mkdir()
    moved: list[tuple[Path, Path]] = []
    try:
        for source in entries:
            destination = staging / source.name
            source.rename(destination)
            moved.append((source, destination))
        staging.rename(workspace_dir)
        if git_root(workspace_dir) != workspace_dir:
            fail("Restructured workspace is not the original git repository root.")
        if git_snapshot(workspace_dir) != before:
            fail("Git HEAD, remotes, or working-tree state changed during restructuring.")
    except (OSError, ValueError):
        if workspace_dir.exists() and not staging.exists():
            workspace_dir.rename(staging)
        if staging.exists():
            for original, staged in reversed(moved):
                if staged.exists() and not original.exists():
                    staged.rename(original)
            if staging.exists() and not any(staging.iterdir()):
                staging.rmdir()
        raise


def configure_bootstrap(meta_dir: Path, project_name: str, dry_run: bool, result: BootstrapResult) -> None:
    replacements = {
        meta_dir / "project" / "project.yaml": {
            PROJECT_NAME_TOKEN: project_name,
        },
        meta_dir / "project" / "README.md": {
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
    root = target.expanduser().resolve()
    restructure_existing = preflight(mode, root)
    result = BootstrapResult()

    meta_dir = root / META_DIR_NAME
    workspace_dir = root / WORKSPACE_DIR_NAME

    if not dry_run:
        root.mkdir(parents=True, exist_ok=True)
        meta_dir.mkdir(parents=True, exist_ok=True)

    if restructure_existing:
        if not dry_run:
            meta_dir.rmdir()
        restructure_existing_repository(root, dry_run, result)
        if not dry_run:
            meta_dir.mkdir(parents=True, exist_ok=True)

    for source in template_files():
        rel = source.relative_to(TEMPLATE_ROOT)
        destination = meta_dir / rel
        if destination.exists():
            if destination.is_dir():
                fail(f"Expected a file but found a directory: {destination}")
            result.preserved.append(destination)
            continue
        result.created.append(destination)
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    configure_bootstrap(meta_dir, project_name, dry_run, result)
    git_init(meta_dir, dry_run, result)

    if mode == "new":
        if not workspace_dir.exists():
            result.created.append(workspace_dir)
            if not dry_run:
                workspace_dir.mkdir(parents=True, exist_ok=True)
        git_init(workspace_dir, dry_run, result)
    else:
        if not restructure_existing:
            result.preserved.append(workspace_dir)
        if not (restructure_existing and dry_run) and not is_git_repo(workspace_dir):
            fail(
                f"{workspace_dir} is not a git repository. Initialize and configure "
                "it before backfill."
            )

    return result


def print_result(root: Path, mode: str, dry_run: bool, result: BootstrapResult) -> None:
    prefix = "Bootstrap preview" if dry_run else "Bootstrap complete"
    print(f"{prefix}: {mode} project at {root.expanduser().resolve()}")
    for label, paths in (
        ("create", result.created),
        ("configure", result.configured),
        ("git-init", result.git_initialized),
        ("preserve", result.preserved),
    ):
        for path in paths:
            print(f"{label}: {relative(path, root.expanduser().resolve())}")
    for source, destination in result.moved:
        print(
            f"move: {relative(source, root.expanduser().resolve())} -> "
            f"{relative(destination, root.expanduser().resolve())}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create and configure a Project Master .project-meta/ bootstrap as a "
            "sibling of workspace/, without touching an existing workspace/."
        )
    )
    parser.add_argument("mode", choices=("new", "existing"))
    parser.add_argument("--target", required=True, type=Path, help="Project root directory")
    parser.add_argument("--name", help="Project display name; defaults to the target folder name")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.name:
        args.name = args.target.expanduser().resolve().name
    if not args.name.strip():
        parser.error("project name cannot be empty")
    args.name = json.dumps(args.name.strip(), ensure_ascii=False)
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
