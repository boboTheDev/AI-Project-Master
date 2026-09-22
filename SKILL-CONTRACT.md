# Project Master Skill Contract

This is the shared authoring contract for future Project Master skills. It implements the boundaries and approval model in [IDEA.md](../IDEA.md). The contract is independent of a particular agent runtime; small runtime adapters can add discovery metadata without changing its project rules.

## Package and discovery

Each skill has one canonical directory, `project-master/<skill-name>/`, with a `SKILL.md`. Use a short, distinct name and a description that says when the skill applies and when it does not. Start `SKILL.md` with `name` and `description` in YAML frontmatter. Keep the core procedure concise; place detailed examples, checklists, and optional methods in `references/` when they become necessary.

The `name` and `description` frontmatter follows the current [OpenAI skill format](https://developers.openai.com/codex/skills/). Compatibility with Claude CLI and the intended VS Code agent must be checked through their runtime adapters before installation; this contract does not assume that one discovery path works everywhere.

## Required sections

| Section | State explicitly |
| --- | --- |
| `PURPOSE` | The result this skill is responsible for. |
| `WHEN TO USE` | Triggers, scope, and cases that belong elsewhere. |
| `INPUTS` | Information received from the request, coordinator, or project. |
| `REQUIRED ARTIFACTS` | Project artifacts that must be read when present, and what to do when a needed artifact is absent or unapproved. Use `None` if none are required. |
| `OPTIONAL ARTIFACTS` | References to load only when relevant. |
| `ALLOWED READS` | Global library and project paths or information the skill may inspect. |
| `ALLOWED WRITES` | Exact project-local artifact or implementation areas it may change. |
| `DEPENDENCIES` | Required prior decisions, handoffs, and affected specialists. |
| `PROCESS` | The shortest reliable sequence, including how to handle evidence and feedback. |
| `OUTPUTS` | Concrete deliverables, their project-local paths, and their draft or approved meaning. |
| `APPROVAL REQUIREMENTS` | Which outputs need the sole project owner's green light and what can proceed automatically. |
| `ESCALATION RULES` | How to report missing intent, conflicts, or upstream impact to Mastermind or the owner. |
| `FORBIDDEN ACTIONS` | Scope and authority violations specific to this skill. |
| `COMPLETION CRITERIA` | Evidence that the requested work and handoff are finished. |

Use these headings in `SKILL.md`; the `NAME` requirement is satisfied by frontmatter `name`. A section may say `None` with a reason, but may not be silently omitted.

## Rules shared by every skill

1. **Locate the managed project first.** A managed project is two sibling directories under one project root: `.project-meta/` (private, its own version history) and `workspace/` (the shared implementation, its own version history). Find the project root by checking the current directory, then walking upward, for the nearest ancestor containing both siblings. If no such ancestor exists, fail clearly and report that no managed project was found; do not guess a root or silently bootstrap one. Read `.project-meta/project/README.md`, `project.yaml`, and relevant `STATUS.md` entries. Check the underlying artifacts before consequential work; status is an index, not authority.
2. **Respect the write boundary.** During managed-project work, read the global library as needed. Write project knowledge, proposals, decisions, change records, and review evidence only to that project's `.project-meta/project/`; write a disposable frontend candidate only to `.project-meta/prototype/`; write implementation only inside `workspace/`. Change this library only during intentional Project Master maintenance.
3. **Keep authority visible.** Distinguish approved intent, observed implementation, sourced facts, proposals, assumptions, and open questions. Code describes current behavior; it does not silently approve a requirement. An approved decision record explains a choice; current approved artifacts express current intent. Surface conflicts rather than guessing.
4. **Use approval proportionally.** Only the project owner approves consequential intent. Prepare a small, coherent revision and its impact for review; approval applies to the whole presented revision. Keep independent unresolved rules in separate drafts, and keep a revision draft when an open question changes its meaning. Retain an existing approved version while its replacement is proposed. Record approval and update dependent artifacts after the green light. Routine work within approved scope, checks, and meaning-preserving index or formatting updates can finish automatically.
5. **Route feedback narrowly.** A downstream discovery that changes upstream intent returns to Mastermind and the affected specialist. Pause only affected work; do not restart an entire pipeline or silently invent the missing rule. Draft exploration can continue when its assumptions are labeled.
6. **Keep outputs proportional.** Create only artifacts needed for this request. Reference related approved artifacts and decision records rather than duplicating them into a second source of truth.
7. **Decide by default; ask only when blocked.** A specialist making a domain choice should analyze available intent, constraints, evidence, and defaults, then proceed with one decisive recommendation and concise rationale rather than opening with a question. Continue on that recommendation as a labeled draft assumption when the choice is reversible or low-stakes; bundle a consequential choice into one coherent review packet instead of pausing for it in isolation. Ask before recommending only when a real blocker exists — required owner-owned intent is missing, approved sources conflict, the choice is difficult to reverse or unusually costly, or the decision is primarily a matter of the owner's preference with no clear default. Even then, state the recommended default alongside the question. When a request surfaces more than one open question, consolidate them into a single batch asked once rather than a drip of follow-ups across separate turns; ask only what genuinely blocks the work, not what a reasonable default can safely resolve.

## Artifact classes and lifecycle

Project Master uses four classes of project-local information:

| Class | Examples | Authority |
| --- | --- | --- |
| Intent | Approved business, technical, database, UX, and design artifacts | Current approved revision states what the project intends. |
| Rationale | ADRs | Explains a meaningful choice; it does not replace current intent. |
| Coordination | CHG records and `STATUS.md` | Tracks scope, review, implementation, and links; it does not define behavior. |
| Evidence | Code, tests, schema, renders, UI reviews, and Enforcer reports | Shows observed implementation or verification; it does not grant approval. |

Use artifact `status` consistently:

- `draft`: incomplete, exploratory, or dependent on an unsettled choice.
- `needs-review`: coherent and ready for the owner to review.
- `approved`: the owner reviewed this exact revision and gave a green light.
- `superseded`: retained history that is no longer current; link its replacement when one exists.

Do not demote or overwrite the current approved artifact while proposing a replacement. Stage the next revision separately, normally as `<name>.proposed.md` beside the canonical artifact or under the active change's project-local evidence area. Give it the next revision number and `draft` or `needs-review` status. After the owner approves that exact revision, preserve the former approved revision through project version history or retained change evidence, promote the reviewed content to the canonical path with approval metadata, and remove stale proposal ambiguity. A purely meaning-preserving correction may update the canonical artifact without this proposal flow.

A CHG record has two independent states: its artifact `status` records whether the owner reviewed the exact coordination packet, while `implementation_state` records execution progress. Marking a CHG approved does not approve an unseen linked artifact or ADR. Update each reviewed revision's own metadata after the green light.

## Starting skeleton for a future `SKILL.md`

This is a writing aid, not an installed skill:

```markdown
---
name: skill-name
description: Use when ...; do not use for ...
---

# Skill Name

## PURPOSE
...

## WHEN TO USE
...

## INPUTS
...

## REQUIRED ARTIFACTS
...

## OPTIONAL ARTIFACTS
...

## ALLOWED READS
...

## ALLOWED WRITES
...

## DEPENDENCIES
...

## PROCESS
...

## OUTPUTS
...

## APPROVAL REQUIREMENTS
...

## ESCALATION RULES
...

## FORBIDDEN ACTIONS
...

## COMPLETION CRITERIA
...
```
