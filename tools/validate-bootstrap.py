#!/usr/bin/env python3
"""Exercise Project Master bootstrap behavior in disposable repositories."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "mastermind/scripts/bootstrap_project.py"
IDENTITY = ("--git-user-name", "Project Master Test", "--git-user-email", "test@project-master.local")


def fail(message: str) -> None:
    raise AssertionError(message)


def command(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HELPER), *map(str, args)],
        capture_output=True,
        text=True,
        check=False,
    )


def git(path: Path, *args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        capture_output=True,
        text=text,
        check=False,
    )
    if result.returncode:
        stderr = result.stderr if text else result.stderr.decode(errors="replace")
        fail(f"git {' '.join(args)} failed in {path}: {stderr}")
    return result.stdout


def init_repository(path: Path, name: str, email: str) -> None:
    path.mkdir(parents=True)
    result = subprocess.run(["git", "init", "--quiet", str(path)], capture_output=True, check=False)
    if result.returncode:
        fail(result.stderr.decode(errors="replace"))
    git(path, "config", "user.name", name)
    git(path, "config", "user.email", email)


def snapshot(path: Path) -> dict[str, str | bytes]:
    return {
        "head": git(path, "rev-parse", "HEAD"),
        "branch": git(path, "symbolic-ref", "HEAD"),
        "remotes": git(path, "remote", "-v"),
        "config": git(path, "config", "--local", "--list", "-z", text=False),
        "status": git(path, "status", "--porcelain=v1", "-z", "--untracked-files=all", text=False),
    }


def validate_new(base: Path) -> None:
    target = base / "new-project"
    result = command("new", "--target", target, "--name", "New: Project", *IDENTITY)
    if result.returncode:
        fail(result.stderr)
    if not all((target / name).is_file() for name in ("AGENTS.md", "CLAUDE.md")):
        fail("new bootstrap did not install both root adapters")
    for repository in (target / ".project-meta", target / "workspace"):
        if Path(str(git(repository, "rev-parse", "--show-toplevel")).strip()).resolve() != repository.resolve():
            fail(f"not a distinct Git root: {repository}")
    if str(git(target / ".project-meta", "rev-list", "--count", "HEAD")).strip() != "1":
        fail("metadata repository does not have exactly one baseline commit")
    if str(git(target / ".project-meta", "ls-files", "local.yaml")).strip():
        fail("device-local library path was committed")
    if "New: Project" not in (target / ".project-meta/project/project.yaml").read_text():
        fail("project name was not configured")


def validate_preflight(base: Path) -> None:
    target = base / "invalid-arranged"
    workspace = target / "workspace"
    workspace.mkdir(parents=True)
    (workspace / "file.txt").write_text("not a repository\n")
    result = command("existing", "--target", target, *IDENTITY)
    if result.returncode == 0:
        fail("populated non-Git workspace was accepted")
    if sorted(path.name for path in target.iterdir()) != ["workspace"]:
        fail("failed preflight mutated the target")


def validate_arranged(base: Path) -> None:
    target = base / "arranged"
    workspace = target / "workspace"
    init_repository(workspace, "Arranged User", "arranged@example.test")
    (workspace / "app.txt").write_text("app\n")
    git(workspace, "add", "app.txt")
    git(workspace, "commit", "--quiet", "-m", "app")
    before = snapshot(workspace)
    result = command("existing", "--target", target)
    if result.returncode:
        fail(result.stderr)
    if snapshot(workspace) != before:
        fail("pre-arranged workspace Git state changed")
    if not (target / ".project-meta/.git").is_dir():
        fail("pre-arranged project did not receive metadata repository")


def validate_restructure(base: Path) -> None:
    target = base / "existing"
    init_repository(target, "Existing User", "existing@example.test")
    (target / "tracked.txt").write_text("base\n")
    git(target, "add", "tracked.txt")
    git(target, "commit", "--quiet", "-m", "base")
    git(target, "remote", "add", "origin", "git@example.test:team/existing.git")
    (target / "tracked.txt").write_text("dirty\n")
    (target / "untracked.txt").write_text("untracked\n")
    before = snapshot(target)
    result = command("existing", "--target", target)
    if result.returncode:
        fail(result.stderr)
    workspace = target / "workspace"
    if snapshot(workspace) != before:
        fail("restructured repository Git state changed")
    if not (workspace / "untracked.txt").is_file():
        fail("untracked file was lost during restructure")


def validate_rollback(base: Path) -> None:
    target = base / "rollback"
    init_repository(target, "Rollback User", "rollback@example.test")
    (target / "source.txt").write_text("source\n")
    git(target, "add", "source.txt")
    git(target, "commit", "--quiet", "-m", "source")
    (target / "dirty.txt").write_text("dirty\n")
    before = snapshot(target)

    spec = importlib.util.spec_from_file_location("project_master_bootstrap_validation", HELPER)
    if spec is None or spec.loader is None:
        fail("could not load bootstrap helper")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    def injected_failure(*_args: object, **_kwargs: object) -> list[Path]:
        raise OSError("injected post-restructure failure")

    module.install_root_adapters = injected_failure
    try:
        module.bootstrap("existing", target, "Rollback", False)
    except ValueError as error:
        if "rolled back" not in str(error):
            fail(f"unexpected rollback error: {error}")
    else:
        fail("injected failure did not stop bootstrap")

    if snapshot(target) != before:
        fail("rollback did not restore Git state")
    if not (target / ".git").is_dir() or (target / "workspace").exists():
        fail("rollback did not restore the original repository layout")
    for unexpected in (".project-meta", "AGENTS.md", "CLAUDE.md"):
        if (target / unexpected).exists():
            fail(f"rollback left generated path: {unexpected}")


def validate_dry_run(base: Path) -> None:
    target = base / "dry-run"
    result = command("new", "--target", target, "--dry-run", *IDENTITY)
    if result.returncode:
        fail(result.stderr)
    if target.exists():
        fail("dry run changed the target")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="project-master-bootstrap-") as temporary:
        base = Path(temporary)
        checks = (
            ("new project", validate_new),
            ("preflight without mutation", validate_preflight),
            ("pre-arranged workspace", validate_arranged),
            ("existing repository preservation", validate_restructure),
            ("post-restructure rollback", validate_rollback),
            ("side-effect-free dry run", validate_dry_run),
        )
        for label, check in checks:
            check(base)
            print(f"ok: {label}")
    print("Project Master isolated bootstrap validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
