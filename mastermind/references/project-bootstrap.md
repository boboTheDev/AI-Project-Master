# Project Bootstrap Procedure

Read this procedure when the owner asks to create a managed project or backfill an existing repository.

## Project shape

A managed project root contains local runtime adapters and two physically separate sibling repositories:

```text
<root>/
├── AGENTS.md          # local runtime adapter, outside both repositories
├── CLAUDE.md          # local runtime adapter, outside both repositories
├── .project-meta/     # private Project Master repository
└── workspace/         # real implementation repository
```

`.project-meta/` holds `project/` for intent, decisions, changes, and evidence, plus `prototype/` for disposable UI work. `workspace/` contains the implementation and no Project Master file or reference. The root adapters may refer to `.project-meta/`; they are intentionally outside both repositories.

Open and run Codex, Claude Code, or another filesystem-scoped agent from `<root>`. Opening `workspace/` alone can hide its parent and the private repository from runtime discovery or filesystem permissions. An already running session may need to be relaunched from the root after bootstrap.

## Choose the project root

For a new project, resolve the parent directory and display name before discussing product behavior. Infer an ordinary folder slug. Ask only when the location or name cannot be resolved honestly.

For an existing project, use its current standalone Git repository root. Bootstrap keeps that outer path, moves the complete repository under `workspace/`, and creates `.project-meta/` beside it. Moving `.git` with the working tree preserves history, branch, remotes, local Git configuration, tracked changes, and untracked files. A project already arranged with a populated Git repository under `workspace/` is accepted without moving it. Linked worktrees are rejected because moving their `.git` file would require a dedicated conversion.

Do not create a managed project inside the global Project Master library. Runtime filesystem permission prompts remain separate from Project Master's owner approval.

## Run the helper

The helper is `mastermind/scripts/bootstrap_project.py` in the Project Master library.

For a new project:

```sh
python3 /path/to/project-master/mastermind/scripts/bootstrap_project.py new \
  --target /path/to/parent/project-root \
  --name "Project display name"
```

For an existing project:

```sh
python3 /path/to/project-master/mastermind/scripts/bootstrap_project.py existing \
  --target /path/to/project-root
```

Use `--dry-run` when the target or intended moves need inspection. If no usable Git identity is configured, pass both `--git-user-name` and `--git-user-email`; otherwise the helper stops before changing the target.

The helper performs the operation transactionally:

1. It validates the target mode, templates, collisions, Git repository shape, Git identity, and existing `workspace/` before any target mutation.
2. It prepares `.project-meta/` and its first commit in a temporary sibling directory.
3. For a new project, it prepares a fresh empty Git repository for `workspace/`. For backfill, it snapshots the existing repository and moves it intact under `workspace/`.
4. It installs root `AGENTS.md` and `CLAUDE.md`, then validates both repositories, adapters, and the backfilled Git snapshot.
5. If a handled filesystem or validation failure occurs after mutation starts, it removes generated adapters and metadata and restores the original folder layout. A failed backfill must not leave a half-managed project.

The initial `.project-meta/` commit uses the existing workspace repository's effective Git identity during backfill, or the configured/requested identity for a new project. The helper does not commit to `workspace/` and does not configure a remote for either repository.

## Resolve the global library on each device

Durable project files store the stable library ID `project-master`, never an absolute device path. Resolve the installed library in this order:

1. a valid `PROJECT_MASTER_HOME` environment variable;
2. the canonical location of the invoked Project Master skill;
3. `.project-meta/local.yaml`, which is device-local and ignored by the metadata repository;
4. one focused owner question when none of the above resolves.

Bootstrap writes `local.yaml` as a convenience for the current device. Copy `local.example.yaml` when configuring another device manually.

## Verify before planning

Confirm that:

1. `AGENTS.md` and `CLAUDE.md` exist at the project root, outside both repositories.
2. `.project-meta/project/project.yaml` contains the intended project name and stable library ID.
3. `.project-meta/project/STATUS.md` begins unassessed.
4. `.project-meta/` has one baseline commit and ignores `local.yaml` plus generated prototype content.
5. `.project-meta/` and `workspace/` are distinct Git roots; `workspace/` contains no Project Master trace.
6. For backfill, HEAD, branch, remotes, local Git configuration, tracked changes, and untracked files match the pre-restructure snapshot.

Then relaunch or set the agent's working root to the directory containing the adapters and both repositories. Read `.project-meta/project/README.md` before continuing with brainstorming, analysis, planning, or implementation. Create specialist directories only when work needs them.
