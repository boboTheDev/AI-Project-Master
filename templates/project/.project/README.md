# Managed Project Bootstrap

This `.project/` directory holds this project's persistent intent, decisions, and state. Project Master skills are reusable instructions at the global location below. Agents may read that library during project work and must put project-specific outputs in this project.

## Configure before use

- **Project Master library:** `REPLACE_WITH_ABSOLUTE_PATH_TO_PROJECT_MASTER`
- **Project root:** the directory containing this `.project/` directory
- **Project owner:** one person, represented in artifacts as `project_owner`

Replace the library path with the actual absolute path on this device. If it is missing or inaccessible, resolve that before invoking Project Master skills. Project-root `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md` may point here; this document is the project's canonical bootstrap.

For cross-skill ownership and operating procedure, consult `AUTHORITY-MAP.md` and `OPERATING-GUIDE.md` under the configured Project Master library.

## Read and write map

| Location | Purpose | Agent access during project work |
| --- | --- | --- |
| Project Master library above | Skills, defaults, templates, and references | Read only |
| `.project/` | Project context, approved intent, drafts, decisions, changes, and retained review evidence | Read and write within the task's scope |
| Project code directories | Implementation and its local tests | Read and write within the task's scope |

Use `.project/project.yaml` for project configuration and default review policy. Use `.project/STATUS.md` to find active work, then inspect the linked artifacts before relying on their content. Do not write project-specific outputs to the global library. Do not create every possible specialist folder at setup; add `business/`, `tech/`, `database/`, `ux/`, `design/`, `ui/`, `decisions/`, and `changes/` only as needed. Decision and change records go to the directories configured in `project.yaml`.

## Authority and review

- Approved `.project/` artifacts state current project intent. Decision records preserve why meaningful choices were made. Code shows current implementation. Report conflicts among them to Mastermind; do not silently pick a winner.
- Mark new consequential artifacts `draft` or `needs-review` until the project owner reviews the concrete revision and gives a green light. For a proposed change to approved intent, retain the current approved revision until the replacement is approved.
- Record an approved revision with `status: approved`, `revision`, `approved_by: project_owner`, and `approved_on`. An older approval does not approve a later consequential edit.
- Do not overwrite or demote the current approved artifact while proposing a replacement. Keep the proposed next revision in a separate `.proposed.md` file or the active change's evidence area. After the owner approves that exact revision, preserve the prior revision through version history or change evidence and promote the reviewed content to the canonical path.
- Follow `approval_required_for` in `project.yaml` unless the owner explicitly authorizes a particular change or adjusts the policy. Routine implementation within approved scope, checks, and meaning-preserving corrections may complete without another approval step.
- A change record coordinates work. Its `status` records owner review of that packet, while `implementation_state` records execution progress. It does not replace approval metadata on linked artifacts or ADRs.
- Update `STATUS.md` when project state changes. It is a derived index and needs no separate owner approval when it accurately reflects the underlying artifacts.

## Starting a task

1. Read this file, `project.yaml`, and `STATUS.md`.
2. Read the relevant approved artifacts, drafts, and decision records; inspect code when current behavior matters.
3. Load only the needed global skills and defaults. Keep assumptions and open questions visible.
4. Write outputs in this project under the areas above. Present consequential proposals with their impact for the owner's review; continue routine authorized work.
