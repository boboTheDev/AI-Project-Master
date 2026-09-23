# Project Master Operating Guide

Use Project Master as a global read-only skill library. A managed project is a project root with two sibling repositories: `.project-meta/` (private: intent, decisions, coordination records, evidence, and a disposable prototype) and `workspace/` (the real implementation, shared with collaborators). `workspace/` contains no Project Master trace. `.project-meta/` and the root runtime adapters may refer to `workspace/` because they coordinate work there.

## 1. Initialize a managed project through Mastermind

Open the intended parent directory for a new project or the root of an existing Git repository, then invoke Mastermind in natural language. After bootstrap, open and run the agent from the generated project root so both repositories and its root adapters are in scope:

- “Use Mastermind. Create a new project called Acme here, then help me define its business model.”
- “Use Mastermind. Backfill this existing project.”

For a new project, Mastermind must create and verify `.project-meta/` and an empty `workspace/` as siblings before asking business, product, architecture, data, UX, or design questions. This gives every useful draft a project-local home from the start. If the project name or location is unclear, Mastermind asks only for the missing setup choice first.

For an existing project, Mastermind verifies that the current directory is the repository root, records its Git HEAD, branch, remotes, local configuration, and working-tree state, then restructures that directory in place. All existing entries, including `.git` and uncommitted files, move together under a new `workspace/` child. Mastermind verifies the same Git state afterward and creates `.project-meta/` beside it. If the repository is already arranged as `workspace/`, no restructure is needed.

Mastermind uses [mastermind/scripts/bootstrap_project.py](mastermind/scripts/bootstrap_project.py) for deterministic setup. The helper finishes validation before target writes, prepares `.project-meta/` and its baseline commit in staging, creates an empty `workspace/` Git repository for a new project, and restructures a normal existing repository without replacing its Git data. It also creates root `AGENTS.md` and `CLAUDE.md` outside both repositories. A handled failure after mutation starts rolls the folder layout back. Its detailed procedure is in [mastermind/references/project-bootstrap.md](mastermind/references/project-bootstrap.md).

After initialization:

1. Root `AGENTS.md` and `CLAUDE.md` direct supported runtimes to the private bootstrap while remaining outside both repositories.
2. `.project-meta/project/README.md` identifies the stable library ID and project-local write boundary.
3. `.project-meta/project/project.yaml` contains the project name, stable library ID, and default review policy.
4. `.project-meta/project/STATUS.md` begins `Unassessed` until evidence supports a stronger state.
5. `tech_profile` remains `null` unless the owner selects a defined profile.
6. `.project-meta/` and `workspace/` are each their own Git repository. `.project-meta/` has a baseline commit; the helper makes no `workspace/` commit and configures no remote.
7. `.project-meta/local.yaml` stores the current device's optional library hint and is ignored by Git.
8. Specialist folders are created only when actual work needs them.

The optional personal skill links in [adapters/README.md](adapters/README.md) make the ten skills discoverable to supported runtimes. Skill installation is a one-time device action; Mastermind then performs project initialization from the conversation.

### Finding an already-initialized project

There is no pointer inside `workspace/` and no symlink between the repositories. Root `AGENTS.md` and `CLAUDE.md` are local runtime adapters outside both repositories. Every skill locates the project root by finding the nearest ancestor that directly contains `.project-meta/` and `workspace/` as siblings. Run agents from that root; opening only `workspace/` can make its parent invisible to runtime discovery or permissions. If no such ancestor exists, report that the project is not initialized and stop unless the owner explicitly asked to create or backfill it.

Resolve the global library separately on each device: use `PROJECT_MASTER_HOME`, then the canonical location of the invoked skill, then ignored `.project-meta/local.yaml`. Ask once for the local path only if none resolves. Durable project artifacts store the library ID, never an absolute device path.

## 2. Start through Mastermind

Natural requests are enough:

- “Use Mastermind. Create a project called Acme here, then help me solidify the business logic.”
- “Use Mastermind. Backfill this project.”
- “Use Mastermind. Tell me where we are in this project.”
- “Use Mastermind as the brainstorming lead. Help me solidify this business logic.”
- “Use Mastermind. Plan and implement this feature.”
- “Use Enforcer. Check this behavior against approved intent.”

Mastermind identifies the requested stopping point and invokes only affected skills. Planning does not automatically authorize implementation. A routine request with clear approved intent can go directly to implementation and verification without a full planning sequence.

## 3. Classify the request

| Request | Default handling |
| --- | --- |
| New project | Create and verify `.project-meta/` and an empty `workspace/` as siblings first, then continue with the requested discovery or planning |
| Status | Check `STATUS.md` against linked sources and report supported state; do not start an audit or change automatically |
| Brainstorming | Use Business Architect first and add affected specialists only when needed; finish with a concrete draft or approved planning outcome |
| Routine implementation | Read approved context, implement within scope inside `workspace/`, run targeted checks, and use Enforcer only when alignment is in question |
| Consequential change | Create a CHG record, route affected domains, prepare concrete revisions and warranted ADRs, request owner review, then implement if requested |
| Existing-project backfill | Restructure the existing repository in place under `workspace/`, bootstrap sibling `.project-meta/`, verify Git state, inventory observed behavior, reconstruct useful drafts, obtain owner review, then establish the approved baseline |
| Conflict | Name the exact approved sources and affected work, obtain the owner's decision, and update the owning artifacts; do not pick a winner silently |

## 4. Use the authority model

Read [AUTHORITY-MAP.md](AUTHORITY-MAP.md) when ownership is unclear. In short:

- Approved business, technical, database, UX, and design artifacts state current intent.
- ADRs explain meaningful choices.
- CHG records coordinate review and execution.
- `STATUS.md` indexes state.
- `workspace/` code, tests, schema, rendered UI, Enforcer findings, and UI reviews provide evidence.
- Global defaults fill unresolved gaps only after project choices and explicit owner instructions.

Every specialist choice follows the shared decision protocol in [SKILL-CONTRACT.md](SKILL-CONTRACT.md): decide by default, ask only when genuinely blocked, recommend a default only when evidence supports one, and consolidate all currently known blockers into one batch. A later batch is allowed when an answer or new evidence reveals a blocker that could not reasonably have been known earlier.

The owner is the sole governor of consequential intent. A concrete owner instruction can resolve a choice, but the affected project artifacts still need to be updated so future work does not depend on conversation history.

## 5. Manage artifact revisions

Authoritative domain artifacts use this lifecycle:

| Status | Meaning |
| --- | --- |
| `draft` | Incomplete, exploratory, or dependent on an unsettled choice |
| `needs-review` | Coherent and ready for owner review |
| `approved` | The owner reviewed and approved this exact revision |
| `superseded` | Retained history that is no longer current |

For a new consequential artifact:

1. Create it as `draft`.
2. Resolve dependent questions or keep the whole revision draft.
3. Set `needs-review` when the revision is coherent.
4. Show the owner the exact content, impact, evidence, alternatives when meaningful, and exclusions.
5. After the owner's green light, set `status: approved`, retain its revision number, and add `approved_by: project_owner` and `approved_on`.

For a change to an approved artifact:

1. Leave the canonical approved file intact.
2. Stage the next revision separately as `<name>.proposed.md` or under the active change's evidence area.
3. Give it the next revision number and `draft` or `needs-review` status.
4. Review that exact revision with the owner and any related ADR.
5. Preserve the previous approved revision through project version history or retained change evidence.
6. Promote only the reviewed content to the canonical path with approval metadata and remove stale proposal ambiguity.

An independent open choice belongs in another linked draft. A question that changes the meaning or viability of the current revision keeps that revision draft.

## 6. Commit metadata at lifecycle checkpoints

`.project-meta/` uses commits as durable review checkpoints rather than an edit-by-edit activity log:

1. Bootstrap creates the initial baseline commit from known template content.
2. Commit a coherent `needs-review` packet before presenting it to the owner, so the reviewed revision is identifiable.
3. After approval, commit the promoted artifacts, approval metadata, ADR state, and updated `STATUS.md` together.
4. When implementation is verified or a CHG is closed, commit the resulting evidence and final coordination state.

Routine draft edits between these checkpoints need no commit. Use clear messages and include relevant `CHG-###` or `ADR-###` identifiers. Do not have Project Master make a commit in `workspace/`; that repository follows the implementation project's own commit policy.

## 7. Coordinate a consequential change

Create `CHG-###-slug.md` in the configured `change_directory` when work changes consequential approved intent across a meaningful scope. The record links the current baseline, proposed revisions, owner review packet, implementation, and verification. It does not replace the underlying artifacts.

Track two separate states:

- `status`: `draft`, `needs-review`, `approved`, or `superseded` for owner review of the CHG packet.
- `implementation_state`: `not-started`, `in-progress`, `implemented`, `verified`, or `blocked` for execution.

An approved CHG does not approve an artifact or ADR the owner did not see. Mark each reviewed revision separately. Use `verified` only after the implementation is checked against approved sources.

Create an ADR only when a choice has lasting rationale, meaningful alternatives or consequences, a cross-domain tradeoff, an exception, or supersession. The owning specialist supplies the decision content; Decision Manager maintains its lifecycle.

## 8. Implement and verify

An implementation handoff names:

- approved source revisions;
- affected behavior and interfaces;
- likely `workspace/` code, schema, and configuration areas;
- rollout or migration constraints;
- material states and failure paths;
- checks needed to show alignment.

Routine coding choices inside approved boundaries need no new owner review. A discovery that requires new consequential intent returns only the affected question to Mastermind and its owning specialist. Independent authorized work can continue.

Use Enforcer for a focused alignment check. It compares observed implementation with approved intent, records reproducible evidence, fixes clear authorized mismatches when safe, and routes ambiguity. Use UI Reviewer when the question requires rendered visual, responsive, interaction, keyboard, or accessibility judgment.

## 9. Backfill an existing project

1. Invoke Mastermind from the existing Git repository root.
2. Run complete preflight, then restructure that same directory into the managed-project root: move all existing entries together under `workspace/`, preserving `.git`, remotes, history, branches, local Git configuration, and uncommitted files.
3. Bootstrap and initially commit `.project-meta/` beside `workspace/`, install the root runtime adapters, and verify that the implementation repository matches its pre-restructure state. If a handled failure occurs, restore the original layout before reporting it.
4. After backfill, re-anchor the shell or relaunch the agent from the outer project root before issuing further commands; do not continue from a moved subdirectory.
5. Use Enforcer to inventory `workspace/` code, configuration, schema, migrations, tests, documentation, and rendered behavior.
6. Label findings as observations because no approved baseline exists yet.
7. Ask affected specialists to reconstruct only useful domain artifacts as `draft` or `needs-review`.
8. Separate observed behavior, inferred intent, contradictions, and unknowns.
9. Ask the owner only about choices evidence cannot establish, and give the owner small, concrete review packets.
10. After approval, promote the reviewed artifacts and update `STATUS.md`. Future Enforcer checks can use them as the baseline.

## 10. Maintain `STATUS.md`

`STATUS.md` is a concise derived index. It should link:

- domain state and source artifact;
- active changes with both CHG `status` and `implementation_state`;
- exact revisions awaiting owner review;
- persistent material drift;
- open questions and affected scope.

Use `Unassessed` or `Unknown` when evidence is insufficient. For authoritative domains, use `Draft`, `Needs review`, `Approved`, or `Conflict` with a source link. For prototypes and evidence, use factual states such as `Exploratory`, `Ready for review`, `Verified`, or `Unverified`; do not call a prototype approved product intent.

## 11. Keep the library and projects separate

During managed-project work:

- Resolve and read Project Master from the device's environment, invoked skill location, or ignored local configuration.
- Write project knowledge, decisions, and evidence only under that project's `.project-meta/project/`; write a disposable prototype only under `.project-meta/prototype/`.
- Write implementation only inside that project's `workspace/`.
- Change this global library only during intentional Project Master maintenance.

The library can be updated centrally without copying its skills into every project. Project artifacts remain local and continue to preserve the project's approved intent. Because `.project-meta/` and `workspace/` are separate repositories, `workspace/` can be pushed to a shared or team remote with no trace of Project Master. `.project-meta/` keeps its own private history and may refer to `workspace/`; it can be pushed to a private remote or left local at the owner's discretion. Root adapters remain outside both repositories.
