# Managed Project Bootstrap

This `.project-meta/` directory is a private repository that holds this project's persistent intent, decisions, prototype, and state. It is a sibling of `workspace/`, the separate repository that holds the project's real implementation and is shared with collaborators. Project Master skills are reusable global instructions resolved as described below. Agents may read that library during project work and must put project-specific outputs only in this private repository or in `workspace/` as the write boundary below states.

## Bootstrap configuration

- **Project Master library ID:** `project-master`
- **Project root:** the parent directory containing this `.project-meta/` directory and its sibling `workspace/`
- **Project owner:** one person, represented in artifacts as `project_owner`

Resolve the global library on each device in this order: a valid `PROJECT_MASTER_HOME` environment variable, the canonical location of the invoked Project Master skill, then device-local `.project-meta/local.yaml`. The durable project files never store an absolute device path. If none resolves, ask the owner once for the local library location and write only `local.yaml`, which is ignored by this repository.

For cross-skill ownership and operating procedure, consult `AUTHORITY-MAP.md` and `OPERATING-GUIDE.md` under the configured Project Master library.

## Finding this project

There is no pointer file inside `workspace/` and no symlink between the two repositories. An agent locates a managed project by finding the nearest ancestor directory, from its current location or by walking upward, that directly contains both `.project-meta/` and `workspace/`. That ancestor is the project root. If no such directory exists, the project is not initialized here; report that plainly and do not guess a root or silently bootstrap one. This convention uses only relative directory structure, so it works identically across devices and operating systems.

Run Codex, Claude Code, or another filesystem-scoped agent from the project root, not from `workspace/` alone. Root `AGENTS.md` and `CLAUDE.md` are generated local adapters outside both repositories; they route supported runtimes to this bootstrap without adding a Project Master trace to `workspace/`.

## Read and write map

| Location | Purpose | Agent access during project work |
| --- | --- | --- |
| Project Master library above | Skills, defaults, templates, and references | Read only |
| `.project-meta/project/` | Project context, approved intent, drafts, decisions, changes, and retained review evidence | Read and write within the task's scope |
| `.project-meta/prototype/` | A disposable, scoped frontend candidate with its own lightweight tooling | Read and write within the task's scope |
| `workspace/` | Real implementation and its local tests, pushed to the shared/team remote | Read and write within the task's scope |

Use `.project-meta/project/project.yaml` for project configuration and default review policy. Use `.project-meta/project/STATUS.md` to find active work, then inspect the linked artifacts before relying on their content. Do not write project-specific outputs to the global library. Do not write a prototype or any Project Master artifact into `workspace/`; that repository stays clean of AI-authored documents, decisions, or scaffolding so it can be pushed and shared without exposing them. Do not create every possible specialist folder at setup; add `business/`, `tech/`, `database/`, `ux/`, `design/`, `ui/`, `decisions/`, and `changes/` under `.project-meta/project/` only as needed. Decision and change records go to the directories configured in `project.yaml`.

## Authority and review

- Approved `.project-meta/project/` artifacts state current project intent. Decision records preserve why meaningful choices were made. Code in `workspace/` shows current implementation. Report conflicts among them to Mastermind; do not silently pick a winner.
- Mark new consequential artifacts `draft` or `needs-review` until the project owner reviews the concrete revision and gives a green light. For a proposed change to approved intent, retain the current approved revision until the replacement is approved.
- Record an approved revision with `status: approved`, `revision`, `approved_by: project_owner`, and `approved_on`. An older approval does not approve a later consequential edit.
- Do not overwrite or demote the current approved artifact while proposing a replacement. Keep the proposed next revision in a separate `.proposed.md` file or the active change's evidence area. After the owner approves that exact revision, preserve the prior revision through version history or change evidence and promote the reviewed content to the canonical path.
- Follow `approval_required_for` in `project.yaml` unless the owner explicitly authorizes a particular change or adjusts the policy. Routine implementation within approved scope, checks, and meaning-preserving corrections may complete without another approval step.
- A change record coordinates work. Its `status` records owner review of that packet, while `implementation_state` records execution progress. It does not replace approval metadata on linked artifacts or ADRs.
- Update `STATUS.md` when project state changes. It is a derived index and needs no separate owner approval when it accurately reflects the underlying artifacts.

Commit this private repository at meaningful lifecycle checkpoints: the bootstrap baseline, a coherent `needs-review` packet, the corresponding approval and promotion, and verified or closed change state. Routine draft edits between checkpoints need no commit. Include relevant `CHG-###` or `ADR-###` identifiers in commit messages. Project Master never commits to `workspace/`; that repository follows its own project policy.

## Starting a task

1. Locate the project root as described above, then read this file, `project.yaml`, and `STATUS.md`.
2. Read the relevant approved artifacts, drafts, and decision records; inspect `workspace/` code when current behavior matters.
3. Load only the needed global skills and defaults. Keep assumptions and open questions visible.
4. Write outputs in the areas above. Present consequential proposals with their impact for the owner's review; continue routine authorized work.
