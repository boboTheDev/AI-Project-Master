#!/usr/bin/env python3
"""Create a physically separated Project Master project with transactional setup.

A managed project root contains local runtime adapters plus two sibling Git
repositories:

  <root>/.project-meta/   private intent, decisions, evidence, and prototype
  <root>/workspace/       real implementation shared with collaborators

For backfill, a standalone repository at <root> is restructured in place by
moving its complete contents, including .git, under workspace/. All validation
and metadata preparation happen before that move, and handled failures roll the
folder structure back.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


LIBRARY_ROOT = Path(__file__).resolve().parents[2]
META_TEMPLATE_ROOT = LIBRARY_ROOT / "templates" / "project-meta"
ROOT_TEMPLATE_ROOT = LIBRARY_ROOT / "templates" / "project-root"
PROJECT_NAME_TOKEN = "REPLACE_WITH_PROJECT_NAME"
META_DIR_NAME = ".project-meta"
WORKSPACE_DIR_NAME = "workspace"
RESTRUCTURE_STAGE_NAME = ".project-master-workspace-staging"
REQUIRED_META_FILES = (
    Path("project/README.md"),
    Path("project/project.yaml"),
    Path("project/STATUS.md"),
    Path("prototype/README.md"),
)


@dataclass(frozen=True)
class GitSnapshot:
    status: bytes
    remotes: bytes
    head: bytes
    symbolic_head: bytes
    local_config: bytes


@dataclass(frozen=True)
class BootstrapPlan:
    kind: str
    root: Path
    workspace: Path
    project_name: str
    git_user_name: str | None
    git_user_email: str | None
    workspace_snapshot: GitSnapshot | None = None


@dataclass
class BootstrapResult:
    created: list[Path] = field(default_factory=list)
    preserved: list[Path] = field(default_factory=list)
    configured: list[Path] = field(default_factory=list)
    git_initialized: list[Path] = field(default_factory=list)
    git_committed: list[Path] = field(default_factory=list)
    moved: list[tuple[Path, Path]] = field(default_factory=list)


def fail(message: str) -> None:
    raise ValueError(message)


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def run_git(path: Path | None, args: list[str], allow_failure: bool = False) -> subprocess.CompletedProcess[bytes]:
    command = ["git"]
    if path is not None:
        command.extend(["-C", str(path)])
    command.extend(args)
    completed = subprocess.run(command, capture_output=True, check=False)
    if completed.returncode != 0 and not allow_failure:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        fail(f"Git command failed ({' '.join(command)}): {detail}")
    return completed


def git_root(path: Path) -> Path | None:
    completed = run_git(path, ["rev-parse", "--show-toplevel"], allow_failure=True)
    if completed.returncode != 0:
        return None
    return Path(completed.stdout.decode().strip()).resolve()


def git_snapshot(path: Path) -> GitSnapshot:
    status = run_git(path, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
    remotes = run_git(path, ["remote", "-v"]).stdout
    head_result = run_git(path, ["rev-parse", "--verify", "HEAD"], allow_failure=True)
    symbolic_result = run_git(path, ["symbolic-ref", "-q", "HEAD"], allow_failure=True)
    local_config = run_git(path, ["config", "--local", "--list", "-z"]).stdout
    return GitSnapshot(
        status=status,
        remotes=remotes,
        head=head_result.stdout if head_result.returncode == 0 else b"",
        symbolic_head=symbolic_result.stdout if symbolic_result.returncode == 0 else b"",
        local_config=local_config,
    )


def git_value(path: Path | None, key: str) -> str | None:
    completed = run_git(path, ["config", "--get", key], allow_failure=True)
    if completed.returncode != 0:
        return None
    value = completed.stdout.decode("utf-8", errors="replace").strip()
    return value or None


def resolve_git_identity(
    repository: Path | None,
    requested_name: str | None,
    requested_email: str | None,
) -> tuple[str, str]:
    if bool(requested_name) != bool(requested_email):
        fail("Provide both --git-user-name and --git-user-email, or neither.")
    name = requested_name or git_value(repository, "user.name") or os.environ.get("GIT_AUTHOR_NAME")
    email = requested_email or git_value(repository, "user.email") or os.environ.get("GIT_AUTHOR_EMAIL")
    if not name or not email:
        fail(
            "A Git identity is required for the initial .project-meta commit. "
            "Configure user.name and user.email, or pass --git-user-name and "
            "--git-user-email."
        )
    return name.strip(), email.strip()


def ensure_templates() -> None:
    for template_root in (META_TEMPLATE_ROOT, ROOT_TEMPLATE_ROOT):
        if not template_root.is_dir():
            fail(f"Bootstrap template is missing: {template_root}")
    for rel in REQUIRED_META_FILES:
        if not (META_TEMPLATE_ROOT / rel).is_file():
            fail(f"Required metadata template is missing: {META_TEMPLATE_ROOT / rel}")
    for name in ("AGENTS.md", "CLAUDE.md"):
        if not (ROOT_TEMPLATE_ROOT / name).is_file():
            fail(f"Required root adapter template is missing: {ROOT_TEMPLATE_ROOT / name}")


def ensure_external_target(root: Path) -> None:
    if root == LIBRARY_ROOT or LIBRARY_ROOT in root.parents:
        fail("A managed project cannot be created inside the Project Master library.")
    if not root.parent.is_dir():
        fail(f"The project parent directory does not exist: {root.parent}")
    if shutil.which("git") is None:
        fail("Git is required to bootstrap a managed project.")


def adapter_collision(root: Path, normal_repository: bool) -> None:
    if normal_repository:
        return
    for source in sorted(ROOT_TEMPLATE_ROOT.iterdir()):
        if not source.is_file():
            continue
        destination = root / source.name
        if destination.exists() and (
            not destination.is_file()
            or destination.read_text(encoding="utf-8") != source.read_text(encoding="utf-8")
        ):
            fail(f"Root adapter collision requires review before bootstrap: {destination}")


def valid_metadata_repository(meta_dir: Path) -> bool:
    return (
        meta_dir.is_dir()
        and git_root(meta_dir) == meta_dir.resolve()
        and all((meta_dir / rel).is_file() for rel in REQUIRED_META_FILES)
    )


def preflight(
    mode: str,
    root: Path,
    project_name: str,
    requested_name: str | None,
    requested_email: str | None,
) -> BootstrapPlan:
    ensure_templates()
    ensure_external_target(root)
    meta_dir = root / META_DIR_NAME
    workspace = root / WORKSPACE_DIR_NAME

    if mode == "new":
        if root.exists() and (not root.is_dir() or any(root.iterdir())):
            fail(f"New-project target must be missing or empty: {root}")
        name, email = resolve_git_identity(None, requested_name, requested_email)
        return BootstrapPlan("new", root, workspace, project_name, name, email)

    if not root.is_dir():
        fail(f"Existing-project target is not a directory: {root}")
    if meta_dir.exists() and not meta_dir.is_dir():
        fail(f"{META_DIR_NAME} exists and is not a directory: {meta_dir}")
    if workspace.exists() and not workspace.is_dir():
        fail(f"{WORKSPACE_DIR_NAME} exists and is not a directory: {workspace}")

    if workspace.is_dir():
        if not any(workspace.iterdir()):
            fail(f"Existing workspace is empty: {workspace}")
        if git_root(workspace) != workspace.resolve():
            fail(f"Existing workspace is not a Git repository root: {workspace}")
        adapter_collision(root, normal_repository=False)
        if meta_dir.exists():
            if not valid_metadata_repository(meta_dir):
                fail(f"Existing metadata directory is incomplete or invalid: {meta_dir}")
            return BootstrapPlan("managed", root, workspace, project_name, None, None)
        name, email = resolve_git_identity(workspace, requested_name, requested_email)
        return BootstrapPlan(
            "arranged",
            root,
            workspace,
            project_name,
            name,
            email,
            git_snapshot(workspace),
        )

    if meta_dir.exists():
        fail(f"Cannot restructure a repository while {meta_dir} already exists.")
    if (root / RESTRUCTURE_STAGE_NAME).exists():
        fail(f"Resolve the stale restructure staging path first: {root / RESTRUCTURE_STAGE_NAME}")
    if git_root(root) != root.resolve():
        fail(f"Existing-project target is not a Git repository root: {root}")
    if not (root / ".git").is_dir():
        fail(
            "Automatic restructuring currently requires a standalone repository "
            "with a .git directory; linked worktrees need a dedicated conversion."
        )
    adapter_collision(root, normal_repository=True)
    name, email = resolve_git_identity(root, requested_name, requested_email)
    return BootstrapPlan(
        "restructure",
        root,
        workspace,
        project_name,
        name,
        email,
        git_snapshot(root),
    )


def copy_template_tree(source_root: Path, destination_root: Path) -> None:
    for source in sorted(source_root.rglob("*")):
        if not source.is_file():
            continue
        destination = destination_root / source.relative_to(source_root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def configure_metadata(meta_dir: Path, project_name: str) -> None:
    manifest = meta_dir / "project" / "project.yaml"
    content = manifest.read_text(encoding="utf-8")
    manifest.write_text(
        content.replace(PROJECT_NAME_TOKEN, json.dumps(project_name, ensure_ascii=False)),
        encoding="utf-8",
    )
    (meta_dir / "local.yaml").write_text(
        f"library_path: {json.dumps(str(LIBRARY_ROOT), ensure_ascii=False)}\n",
        encoding="utf-8",
    )


def initialize_git_repository(path: Path) -> None:
    run_git(None, ["init", "--quiet", str(path)])


def prepare_metadata_stage(plan: BootstrapPlan) -> Path:
    assert plan.git_user_name is not None and plan.git_user_email is not None
    stage = Path(
        tempfile.mkdtemp(
            prefix=f".{plan.root.name}.project-meta-staging-",
            dir=str(plan.root.parent),
        )
    )
    try:
        copy_template_tree(META_TEMPLATE_ROOT, stage)
        configure_metadata(stage, plan.project_name)
        initialize_git_repository(stage)
        run_git(stage, ["config", "user.name", plan.git_user_name])
        run_git(stage, ["config", "user.email", plan.git_user_email])
        run_git(stage, ["add", "--all"])
        run_git(
            stage,
            [
                "commit",
                "--quiet",
                "--no-gpg-sign",
                "--no-verify",
                "-m",
                "Initialize Project Master metadata",
            ],
        )
        if git_root(stage) != stage.resolve():
            fail("Prepared metadata staging directory is not a valid Git repository.")
        return stage
    except (OSError, ValueError):
        shutil.rmtree(stage, ignore_errors=True)
        raise


def prepare_workspace_stage(root: Path) -> Path:
    stage = Path(
        tempfile.mkdtemp(
            prefix=f".{root.name}.workspace-staging-",
            dir=str(root.parent),
        )
    )
    try:
        initialize_git_repository(stage)
        return stage
    except (OSError, ValueError):
        shutil.rmtree(stage, ignore_errors=True)
        raise


def restructure_repository(plan: BootstrapPlan, result: BootstrapResult) -> None:
    root = plan.root
    staging = root / RESTRUCTURE_STAGE_NAME
    entries = sorted(root.iterdir(), key=lambda path: path.name)
    staging.mkdir()
    moved: list[tuple[Path, Path]] = []
    try:
        for source in entries:
            destination = staging / source.name
            source.rename(destination)
            moved.append((source, destination))
            result.moved.append((source, plan.workspace / source.name))
        staging.rename(plan.workspace)
        if git_root(plan.workspace) != plan.workspace.resolve():
            fail("Restructured workspace is not the original Git repository root.")
        if git_snapshot(plan.workspace) != plan.workspace_snapshot:
            fail("Git state changed during repository restructuring.")
    except (OSError, ValueError):
        if plan.workspace.exists() and not staging.exists():
            plan.workspace.rename(staging)
        if staging.exists():
            for original, staged in reversed(moved):
                if staged.exists() and not original.exists():
                    staged.rename(original)
            if staging.exists() and not any(staging.iterdir()):
                staging.rmdir()
        raise


def rollback_restructure(plan: BootstrapPlan) -> None:
    staging = plan.root / RESTRUCTURE_STAGE_NAME
    if not plan.workspace.exists():
        return
    plan.workspace.rename(staging)
    for staged in sorted(staging.iterdir(), key=lambda path: path.name):
        staged.rename(plan.root / staged.name)
    staging.rmdir()


def install_root_adapters(root: Path, result: BootstrapResult) -> list[Path]:
    created: list[Path] = []
    temporary: Path | None = None
    try:
        for source in sorted(ROOT_TEMPLATE_ROOT.iterdir()):
            if not source.is_file():
                continue
            destination = root / source.name
            if destination.exists():
                result.preserved.append(destination)
                continue
            temporary = root / f".{source.name}.project-master-staging"
            shutil.copy2(source, temporary)
            temporary.replace(destination)
            temporary = None
            created.append(destination)
            result.created.append(destination)
        return created
    except OSError:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        for destination in created:
            destination.unlink(missing_ok=True)
        raise


def validate_final(plan: BootstrapPlan) -> None:
    meta_dir = plan.root / META_DIR_NAME
    if not valid_metadata_repository(meta_dir):
        fail("Installed .project-meta repository failed validation.")
    if git_root(plan.workspace) != plan.workspace.resolve():
        fail("Installed workspace failed Git repository validation.")
    if plan.workspace_snapshot is not None and git_snapshot(plan.workspace) != plan.workspace_snapshot:
        fail("Workspace Git state differs from its pre-bootstrap snapshot.")
    for source in sorted(ROOT_TEMPLATE_ROOT.iterdir()):
        destination = plan.root / source.name
        if not destination.is_file() or destination.read_text(encoding="utf-8") != source.read_text(encoding="utf-8"):
            fail(f"Root runtime adapter failed validation: {destination}")


def describe_dry_run(plan: BootstrapPlan, result: BootstrapResult) -> None:
    meta_dir = plan.root / META_DIR_NAME
    if plan.kind == "managed":
        result.preserved.extend([meta_dir, plan.workspace])
    else:
        for source in sorted(META_TEMPLATE_ROOT.rglob("*")):
            if source.is_file():
                result.created.append(meta_dir / source.relative_to(META_TEMPLATE_ROOT))
        result.configured.extend([meta_dir / "project/project.yaml", meta_dir / "local.yaml"])
        result.git_initialized.append(meta_dir)
        result.git_committed.append(meta_dir)
    if plan.kind == "new":
        result.created.append(plan.workspace)
        result.git_initialized.append(plan.workspace)
    elif plan.kind == "restructure":
        for source in sorted(plan.root.iterdir(), key=lambda path: path.name):
            result.moved.append((source, plan.workspace / source.name))
        result.created.append(plan.workspace)
    else:
        result.preserved.append(plan.workspace)
    normal_repository = plan.kind == "restructure"
    for source in sorted(ROOT_TEMPLATE_ROOT.iterdir()):
        destination = plan.root / source.name
        if destination.exists() and not normal_repository:
            result.preserved.append(destination)
        else:
            result.created.append(destination)


def bootstrap(
    mode: str,
    target: Path,
    project_name: str,
    dry_run: bool,
    git_user_name: str | None = None,
    git_user_email: str | None = None,
) -> BootstrapResult:
    root = target.expanduser().resolve()
    plan = preflight(mode, root, project_name, git_user_name, git_user_email)
    result = BootstrapResult()
    if dry_run:
        describe_dry_run(plan, result)
        return result

    if plan.kind == "managed":
        created_adapters: list[Path] = []
        try:
            created_adapters = install_root_adapters(root, result)
            validate_final(plan)
            return result
        except (OSError, ValueError):
            for path in created_adapters:
                path.unlink(missing_ok=True)
            raise

    meta_stage = prepare_metadata_stage(plan)
    workspace_stage: Path | None = None
    root_created = False
    workspace_installed = False
    meta_installed = False
    restructured = False
    created_adapters: list[Path] = []
    try:
        if plan.kind == "new":
            workspace_stage = prepare_workspace_stage(root)
            if not root.exists():
                root.mkdir()
                root_created = True
            workspace_stage.rename(plan.workspace)
            workspace_installed = True
        elif plan.kind == "restructure":
            restructure_repository(plan, result)
            restructured = True

        meta_dir = root / META_DIR_NAME
        meta_stage.rename(meta_dir)
        meta_installed = True
        created_adapters = install_root_adapters(root, result)
        validate_final(plan)

        for source in sorted(META_TEMPLATE_ROOT.rglob("*")):
            if source.is_file():
                result.created.append(meta_dir / source.relative_to(META_TEMPLATE_ROOT))
        result.configured.extend([meta_dir / "project/project.yaml", meta_dir / "local.yaml"])
        result.git_initialized.append(meta_dir)
        result.git_committed.append(meta_dir)
        if plan.kind == "new":
            result.created.append(plan.workspace)
            result.git_initialized.append(plan.workspace)
        elif plan.kind == "arranged":
            result.preserved.append(plan.workspace)
        return result
    except (OSError, ValueError) as error:
        for path in created_adapters:
            path.unlink(missing_ok=True)
        if meta_installed and (root / META_DIR_NAME).exists():
            (root / META_DIR_NAME).rename(meta_stage)
        if workspace_installed and plan.workspace.exists() and workspace_stage is not None:
            plan.workspace.rename(workspace_stage)
        if restructured:
            rollback_restructure(plan)
        if root_created and root.exists() and not any(root.iterdir()):
            root.rmdir()
        shutil.rmtree(meta_stage, ignore_errors=True)
        if workspace_stage is not None:
            shutil.rmtree(workspace_stage, ignore_errors=True)
        raise ValueError(f"Bootstrap failed and was rolled back: {error}") from error


def print_result(root: Path, mode: str, dry_run: bool, result: BootstrapResult) -> None:
    resolved = root.expanduser().resolve()
    prefix = "Bootstrap preview" if dry_run else "Bootstrap complete"
    print(f"{prefix}: {mode} project at {resolved}")
    for label, paths in (
        ("create", result.created),
        ("configure", result.configured),
        ("git-init", result.git_initialized),
        ("git-commit", result.git_committed),
        ("preserve", result.preserved),
    ):
        seen: set[Path] = set()
        for path in paths:
            if path in seen:
                continue
            seen.add(path)
            print(f"{label}: {relative(path, resolved)}")
    for source, destination in result.moved:
        print(f"move: {relative(source, resolved)} -> {relative(destination, resolved)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a physically separated Project Master bootstrap with sibling "
            ".project-meta/ and workspace/ Git repositories."
        )
    )
    parser.add_argument("mode", choices=("new", "existing"))
    parser.add_argument("--target", required=True, type=Path, help="Managed-project root")
    parser.add_argument("--name", help="Project display name; defaults to the target folder name")
    parser.add_argument("--git-user-name", help="Git author name for the initial metadata commit")
    parser.add_argument("--git-user-email", help="Git author email for the initial metadata commit")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.name:
        args.name = args.target.expanduser().resolve().name
    if not args.name.strip():
        parser.error("project name cannot be empty")
    args.name = args.name.strip()
    return args


def main() -> int:
    args = parse_args()
    try:
        result = bootstrap(
            args.mode,
            args.target,
            args.name,
            args.dry_run,
            args.git_user_name,
            args.git_user_email,
        )
        print_result(args.target, args.mode, args.dry_run, result)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
