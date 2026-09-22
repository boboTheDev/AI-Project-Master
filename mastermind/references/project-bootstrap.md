# Project Bootstrap Procedure

Read this procedure when the owner asks to create a new managed project or backfill an existing repository.

## Choose the project root

For a new project, resolve the intended parent directory, project display name, and folder name before discussing business or product behavior. Infer the folder name from the project name when the choice is ordinary. Ask one focused question only when the target or naming choice is materially ambiguous.

For an existing project, use the repository root containing its code and version-control metadata. Inspect only enough structure to confirm that root and identify bootstrap collisions before initialization.

Do not create a managed project inside the global Project Master library. Filesystem permission prompts imposed by the runtime are separate from Project Master's owner-approval lifecycle.

## Run the deterministic bootstrap

The helper lives at `mastermind/scripts/bootstrap_project.py` under the Project Master library.

For a new project:

```sh
python3 /absolute/path/to/project-master/mastermind/scripts/bootstrap_project.py new \
  --target /absolute/path/to/parent/project-folder \
  --name "Project display name"
```

For an existing project:

```sh
python3 /absolute/path/to/project-master/mastermind/scripts/bootstrap_project.py existing \
  --target /absolute/path/to/repository
```

Use `--dry-run` first when the target already contains files or its state is uncertain. The helper:

- creates the requested project folder in `new` mode;
- refuses a nonempty new-project target and directs it to `existing` mode;
- copies only missing bootstrap files;
- fills the project name and absolute Project Master library path;
- preserves every existing file;
- reports agent instruction files that need an intelligent merge; and
- refuses to place a managed project inside the global library.

## Complete instruction integration

When the helper reports `merge-required`, read the existing file and merge the intent of the corresponding template without deleting or weakening repository-specific instructions.

- `AGENTS.md` must direct relevant agents to `.project/README.md`, `.project/project.yaml`, and `.project/STATUS.md`.
- `CLAUDE.md` should import `@AGENTS.md` unless its existing structure provides an equivalent route.
- `.github/copilot-instructions.md` should route relevant work to the managed-project instructions.

Do not duplicate guidance when an equivalent route already exists. Resolve a true instruction conflict with the owner instead of silently choosing one.

## Verify before planning

Confirm that:

1. `.project/README.md` contains the actual absolute Project Master path.
2. `.project/project.yaml` contains the intended project name.
3. `.project/STATUS.md` exists and begins unassessed.
4. At least one applicable project entry file routes the current runtime to the bootstrap.
5. No existing project instruction was overwritten.

After these checks, treat the project as initialized. Set the working directory to the new or existing project root, read its bootstrap, and only then begin brainstorming, backfill analysis, planning, or implementation. Create specialist directories and artifacts only when the work needs them.
