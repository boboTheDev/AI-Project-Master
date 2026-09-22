# Project Master Operating Guide

Use Project Master as a global read-only skill library. A managed project keeps all of its own intent, decisions, coordination records, evidence, and implementation inside that project's repository.

## 1. Initialize a managed project

For a new project with no conflicting instruction files, copy the project template contents into its root:

```sh
cp -R /absolute/path/to/project-master/templates/project/. /absolute/path/to/managed-project/
```

For an existing project, copy `.project/README.md`, `.project/project.yaml`, and `.project/STATUS.md`, then merge `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` with existing instructions. Do not replace repository-specific rules blindly.

Configure:

1. Replace `REPLACE_WITH_PROJECT_NAME` in `.project/project.yaml`.
2. Replace `REPLACE_WITH_ABSOLUTE_PATH_TO_PROJECT_MASTER` in `.project/README.md`.
3. Leave `tech_profile: null` unless the owner explicitly selects a defined profile.
4. Reconcile `.project/STATUS.md` with real evidence. For an existing project, begin with domains marked `Unassessed` until backfill establishes more.
5. Create specialist folders only when the project needs them.

The optional personal skill links in [adapters/README.md](adapters/README.md) can make the ten skills discoverable to supported runtimes. Installation and runtime discovery are separate from project initialization.

## 2. Start through Mastermind

Natural requests are enough:

- “Use Mastermind. Tell me where we are in this project.”
- “Use Mastermind as the brainstorming lead. Help me solidify this business logic.”
- “Use Mastermind. Plan and implement this feature.”
- “Use Enforcer. Check this behavior against approved intent.”

Mastermind identifies the requested stopping point and invokes only affected skills. Planning does not automatically authorize implementation. A routine request with clear approved intent can go directly to implementation and verification without a full planning sequence.

## 3. Classify the request

| Request | Default handling |
| --- | --- |
| Status | Check `STATUS.md` against linked sources and report supported state; do not start an audit or change automatically |
| Brainstorming | Use Business Architect first and add affected specialists only when needed; finish with a concrete draft or approved planning outcome |
| Routine implementation | Read approved context, implement within scope, run targeted checks, and use Enforcer only when alignment is in question |
| Consequential change | Create a CHG record, route affected domains, prepare concrete revisions and warranted ADRs, request owner review, then implement if requested |
| Existing-project backfill | Inventory observed behavior, reconstruct only useful drafts, obtain owner review, then establish the approved baseline |
| Conflict | Name the exact approved sources and affected work, obtain the owner's decision, and update the owning artifacts; do not pick a winner silently |

## 4. Use the authority model

Read [AUTHORITY-MAP.md](AUTHORITY-MAP.md) when ownership is unclear. In short:

- Approved business, technical, database, UX, and design artifacts state current intent.
- ADRs explain meaningful choices.
- CHG records coordinate review and execution.
- `STATUS.md` indexes state.
- Code, tests, schema, rendered UI, Enforcer findings, and UI reviews provide evidence.
- Global defaults fill unresolved gaps only after project choices and explicit owner instructions.

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

## 6. Coordinate a consequential change

Create `CHG-###-slug.md` in the configured `change_directory` when work changes consequential approved intent across a meaningful scope. The record links the current baseline, proposed revisions, owner review packet, implementation, and verification. It does not replace the underlying artifacts.

Track two separate states:

- `status`: `draft`, `needs-review`, `approved`, or `superseded` for owner review of the CHG packet.
- `implementation_state`: `not-started`, `in-progress`, `implemented`, `verified`, or `blocked` for execution.

An approved CHG does not approve an artifact or ADR the owner did not see. Mark each reviewed revision separately. Use `verified` only after the implementation is checked against approved sources.

Create an ADR only when a choice has lasting rationale, meaningful alternatives or consequences, a cross-domain tradeoff, an exception, or supersession. The owning specialist supplies the decision content; Decision Manager maintains its lifecycle.

## 7. Implement and verify

An implementation handoff names:

- approved source revisions;
- affected behavior and interfaces;
- likely code, schema, and configuration areas;
- rollout or migration constraints;
- material states and failure paths;
- checks needed to show alignment.

Routine coding choices inside approved boundaries need no new owner review. A discovery that requires new consequential intent returns only the affected question to Mastermind and its owning specialist. Independent authorized work can continue.

Use Enforcer for a focused alignment check. It compares observed implementation with approved intent, records reproducible evidence, fixes clear authorized mismatches when safe, and routes ambiguity. Use UI Reviewer when the question requires rendered visual, responsive, interaction, keyboard, or accessibility judgment.

## 8. Backfill an existing project

1. Bootstrap `.project/` with `STATUS.md` marked `Unassessed`.
2. Use Enforcer to inventory code, configuration, schema, migrations, tests, documentation, and rendered behavior.
3. Label findings as observations because no approved baseline exists yet.
4. Ask affected specialists to reconstruct only useful domain artifacts as `draft` or `needs-review`.
5. Separate observed behavior, inferred intent, contradictions, and unknowns.
6. Give the owner small, concrete review packets.
7. After approval, promote the reviewed artifacts and update `STATUS.md`. Future Enforcer checks can use them as the baseline.

## 9. Maintain `STATUS.md`

`STATUS.md` is a concise derived index. It should link:

- domain state and source artifact;
- active changes with both CHG `status` and `implementation_state`;
- exact revisions awaiting owner review;
- persistent material drift;
- open questions and affected scope.

Use `Unassessed` or `Unknown` when evidence is insufficient. For authoritative domains, use `Draft`, `Needs review`, `Approved`, or `Conflict` with a source link. For prototypes and evidence, use factual states such as `Exploratory`, `Ready for review`, `Verified`, or `Unverified`; do not call a prototype approved product intent.

## 10. Keep the library and projects separate

During managed-project work:

- Read Project Master from its configured global path.
- Write project knowledge and evidence only under that project's `.project/`.
- Write implementation only inside that project's code directories.
- Change this global library only during intentional Project Master maintenance.

The library can be updated centrally without copying its skills into every project. Project artifacts remain local and continue to preserve the project's approved intent.
