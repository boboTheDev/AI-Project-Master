# Project Bootstrap Procedure

Read this procedure when the owner asks to create a new managed project or backfill an existing repository.

## Project shape

A managed project is a project root with two sibling directories:

- `<root>/.project-meta/` — a private repository holding `project/` (context, approved intent, decisions, changes, review evidence) and `prototype/` (a disposable frontend candidate). It is never pushed to a shared or team remote.
- `<root>/workspace/` — the real implementation, its own separate repository, pushed to the shared or team remote. For backfill, this is the owner's existing repository moved intact beneath the managed-project root. It carries no Project Master file, document, or reference of any kind.

There is no pointer file inside `workspace/` and no symlink between the two directories. An agent finds the project root by locating the nearest ancestor, from the current directory or by walking upward, that directly contains both `.project-meta/` and `workspace/`. This is pure relative-path convention, so it holds identically on every device and operating system. If no such ancestor exists, the project is not initialized at this location; report that plainly and do not guess a root or silently bootstrap one.

## Choose the project root

For a new project, resolve the intended parent directory and project display name before discussing business or product behavior. Infer the folder name from the project name when the choice is ordinary. Ask one focused question only when the target or naming choice is materially ambiguous.

For an existing project, use the current repository root as the managed-project root. The helper verifies that it is a standalone Git repository, snapshots its HEAD, remotes, and working-tree state, then moves every existing entry together under a new `workspace/` child. Moving `.git` with the working tree preserves history, branches, remotes, configuration, tracked files, and uncommitted files. The outer directory remains at the same path and becomes the parent of sibling `.project-meta/` and `workspace/` directories. If the repository is already arranged under `workspace/`, the helper retains it there.

Do not create a managed project inside the global Project Master library. Filesystem permission prompts imposed by the runtime are separate from Project Master's owner-approval lifecycle.

## Run the deterministic bootstrap

The helper lives at `mastermind/scripts/bootstrap_project.py` under the Project Master library.

For a new project:

```sh
python3 /absolute/path/to/project-master/mastermind/scripts/bootstrap_project.py new \
  --target /absolute/path/to/parent/project-root \
  --name "Project display name"
```

For an existing project, run from its current repository root:

```sh
python3 /absolute/path/to/project-master/mastermind/scripts/bootstrap_project.py existing \
  --target /absolute/path/to/project-root
```

Use `--dry-run` first when the target already contains files or its state is uncertain. The helper:

- creates `.project-meta/` and configures it as a fresh git repository;
- in `new` mode, creates an empty `workspace/` and initializes it as a fresh git repository, refusing if either directory already has content;
- in `existing` mode, accepts either a normal standalone Git repository root or a project already arranged with a populated Git repository under `workspace/`;
- for a normal repository root, moves its complete contents under `workspace/` and verifies that HEAD, remotes, and working-tree state match the pre-move snapshot;
- preserves the existing `.git` directory rather than initializing or replacing it;
- fills the project name and absolute Project Master library path inside `.project-meta/`;
- preserves every existing file it encounters; and
- refuses to place a managed project inside the global library.

The helper never configures a remote for either repository. Add the shared/team remote to `workspace/` and, if the owner wants durable off-device history for `.project-meta/`, a private remote for it, as separate steps outside this helper.

## Verify before planning

Confirm that:

1. `.project-meta/project/README.md` contains the actual absolute Project Master path.
2. `.project-meta/project/project.yaml` contains the intended project name.
3. `.project-meta/project/STATUS.md` exists and begins unassessed.
4. `.project-meta/` and `workspace/` are each their own git repository, and `workspace/` contains no Project Master file.
5. For backfill, the existing repository's HEAD, remotes, and working-tree state match their pre-restructure values.

After these checks, treat the project as initialized. Set the working root to the project root containing both siblings, read `.project-meta/project/README.md`, and only then begin brainstorming, backfill analysis, planning, or implementation. Create specialist directories and artifacts only when the work needs them.
