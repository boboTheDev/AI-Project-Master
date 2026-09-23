# Project Master Integration Review

Review date: 2026-09-22 (updated for the two-repository project shape and the shared decision protocol)

This review covers all ten skills, shared contracts, templates, schemas, examples, defaults, adapters, and isolated bootstrap behavior. Static consistency, disposable filesystem checks, and real runtime use are reported separately.

## 1. Authority review

[AUTHORITY-MAP.md](AUTHORITY-MAP.md) now assigns one owner to every consequential domain and distinguishes four information classes:

- approved domain artifacts state intent;
- ADRs preserve rationale;
- CHG records and `STATUS.md` coordinate and index;
- implementation and review records provide evidence.

The owner remains the only governor of consequential intent. No skill, status entry, code path, test, schema, render, default, or conversation inference can grant approval. Conflicting approved sources return to Mastermind and the owner rather than being resolved by recency or implementation behavior.

## 2. Handoff review

The handoff map was checked in both directions:

- Business owns product meaning and sends feasibility, data, and journey questions to their specialists.
- Technical owns system boundaries and routes persistent-model detail to Data and interaction impact to UX.
- Data returns retention, deletion, permission, and lifecycle policy to Business; it sends visible states to UX.
- UX sends visual language to Design System and keeps product semantics with Business.
- Design System gives explicit rules and states to UI Prototyper.
- UI Prototyper gives routes, states, draft dependencies, simulations, and evidence gaps to UI Reviewer.
- UI Reviewer routes findings to UX, Design System, or implementation.
- Decision Manager records warranted rationale from an owning specialist.
- Enforcer checks alignment and sends missing or conflicting intent through Mastermind.
- Mastermind coordinates only affected domains and does not become a second knowledge base.

No full specialist pipeline is mandatory. Routine authorized work can proceed directly; consequential discoveries trigger a targeted feedback loop.

## 3. Scenario walkthroughs

| Scenario | Flow checked | Result |
| --- | --- | --- |
| New project | Mastermind creates root adapters, initially commits `.project-meta/`, and creates an empty sibling `workspace/` Git repository → agent runs from the root → relevant drafts → consolidated owner review → implementation → Enforcer | Coherent in isolated checks. Bootstrap precedes business discussion; generated adapters stay outside both repositories. |
| Existing-project backfill | Complete preflight → staged metadata baseline → repository snapshot → intact move under `workspace/` → root adapters → final validation or rollback → observation inventory → owner-reviewed baseline | Coherent for standalone repositories in isolated checks. History, branch, remotes, local configuration, tracked changes, and untracked files survive; an injected post-move failure restored the original layout. Linked worktrees require dedicated conversion. |
| Consequential feature | CHG → affected specialists follow the shared decision protocol (recommend, then ask only when blocked) → warranted ADR → exact review packet → canonical artifact promotion → implementation in `workspace/` → verification | Coherent after defining separate proposed replacement files, distinct CHG implementation state, and the shared decision protocol. |
| Routine implementation fix | Read approved context → implement within authorized scope inside `workspace/` → targeted check → optional Enforcer finding | Coherent. No unnecessary CHG, ADR, or owner review is required. |
| Conflicting approved artifacts | Name both sources → pause affected work → Mastermind presents focused choice → owner decides → owning specialists revise artifacts | Coherent. Neither code, recency, status, nor ADR automatically wins. |
| Database migration | Business policy → technical boundary → data design → owner approval → implementation handoff → separate operational authorization → verification | Coherent. Approving the schema does not authorize executing against real data. |
| UI proposal and review | Approved or labeled draft UX → design rules and a disposable preview in `.project-meta/prototype/`, isolated from `workspace/` → rendered UI review → targeted corrections or upstream proposal | Coherent. Prototype and review evidence never approve product, UX, or design intent, and the prototype's own lightweight stack never touches `workspace/`. |
| Specialist decision under the shared protocol | Technical/Data/UX/Design specialist analyzes constraints → proposes one decisive recommendation with rationale → proceeds as labeled draft if reversible, or bundles into a review packet if consequential → batches all currently known blockers → asks a later focused batch only if an answer or new evidence exposes a new blocker | Coherent. A default is supplied only when defensible; the protocol does not require invented confidence. |

## 4. Artifact lifecycle review

The lifecycle uses `draft`, `needs-review`, `approved`, and `superseded` consistently for consequential artifacts and ADRs. This review added an explicit replacement procedure:

1. Keep the canonical approved file intact.
2. Stage the next revision separately with the next revision number.
3. Review the exact proposed content.
4. Preserve the prior approved revision through version history or retained change evidence.
5. Promote only approved content to the canonical path.

CHG records now separate owner-review `status` from `implementation_state`. Evidence-only UI review, Enforcer review, and prototype-note templates remain plain Markdown so their presence cannot be mistaken for approved intent.

## 5. Operational consistency review

The following contracts align:

- Global skills and defaults are read-only during managed-project work.
- Project artifacts, decisions, and the disposable prototype stay under the managed project's private `.project-meta/`; evidence stays there too.
- Implementation stays inside the managed project's `workspace/`, a separate repository carrying no Project Master trace.
- Root `AGENTS.md` and `CLAUDE.md` provide runtime entry instructions outside both repositories; the sibling directory shape remains the runtime-independent project locator. Agents must run from the project root rather than `workspace/` alone.
- Durable files store a stable library ID. Each device resolves the library through `PROJECT_MASTER_HOME`, the invoked skill location, or ignored `.project-meta/local.yaml`.
- `project.yaml` configures directories, default approval categories, selected profile, and overrides; it does not replace domain artifacts.
- `STATUS.md` is derived and links underlying sources.
- Decision and change IDs use `ADR-###` and `CHG-###`.
- A selected technology profile fills unresolved choices but does not override approved project architecture.
- Mastermind performs transactional bootstrap through a deterministic helper. It validates before mutation, stages the metadata repository and baseline commit, verifies the result, and rolls handled failures back.
- `.project-meta/` commits mark bootstrap, review, approval, and closure checkpoints. Project Master makes no implementation-repository commits.
- Every specialist decision follows the shared decision protocol in SKILL-CONTRACT.md: recommend by default, ask only when genuinely blocked, avoid unsupported defaults, and batch currently known blockers.
- All ten skills use the common fourteen-section contract.

`tools/validate-library.py` checks static contracts, schemas, templates, local links, and adapter syntax. `tools/validate-bootstrap.py` exercises bootstrap behavior in disposable repositories.

Validation completed successfully on 2026-09-22:

- `python3 project-master/tools/validate-library.py` passed every static check.
- All skill and lifecycle-template frontmatter parsed with the available Ruby YAML parser.
- The Python validator compiled with its cache redirected to a writable temporary path.
- The bootstrap helper passed isolated new-project, invalid preflight, pre-arranged repository, existing-repository preservation, injected post-restructure rollback, and side-effect-free dry-run checks.
- `install-local.sh --dry-run` enumerated all ten skills for both configured target directories and made no writes.

## 6. Resolved findings

| Finding | Resolution |
| --- | --- |
| “Retain the approved artifact” lacked an operational proposal path | Defined separate `.proposed.md` or change-evidence staging, followed by reviewed promotion to the canonical path |
| CHG `status: approved` could be confused with completed implementation | Added independent `implementation_state` to the template, schema, status guidance, and contract |
| CHG approval could be mistaken for approval of all linked artifacts | Stated that each exact artifact and ADR revision keeps its own approval metadata |
| UI prototype state could be described as approved intent | Standardized prototype/evidence states such as exploratory, ready for review, verified, and unverified |
| Product policy and database mechanics overlapped | Assigned retention/deletion policy to Business and storage/migration design to Data |
| Review evidence could look like an authoritative artifact | Kept UI review, Enforcer review, and prototype notes as evidence-only documents without approval frontmatter |
| Handoffs were distributed across skills but hard to inspect | Added one cross-skill handoff and authority map |
| Initialization and common operating flows were spread across several files | Added [OPERATING-GUIDE.md](OPERATING-GUIDE.md) |
| Project onboarding required manual copying and placeholder edits | Added Mastermind bootstrap modes and a collision-safe helper that configures new or existing projects before planning |
| A single `.project/` beside code made it hard to share a project's implementation without also exposing AI-authored artifacts, and offered no real version history independent of the code repository | Split the managed project into two sibling repositories: private `.project-meta/` (context, decisions, changes, review evidence, and a disposable `prototype/`) and `workspace/` (real implementation, shareable with collaborators with no trace of Project Master). Every skill's artifact paths, the bootstrap helper, and all shared docs were updated to the new structure. |
| Locating a project depended on an in-repo pointer file, which did not port cleanly and put a Project Master trace inside the shared code repository | Kept `workspace/` clean, used sibling directory structure as the runtime-independent locator, and added local `AGENTS.md` and `CLAUDE.md` at the outer project root for supported runtime activation. |
| UI Prototyper wrote a rendered candidate directly into the project's real frontend folder, mixing throwaway exploration with production code and forcing it to match the real stack | Gave UI Prototyper its own `.project-meta/prototype/` folder with its own disposable, lightweight tooling, decoupled from `workspace/`'s stack and conventions. Dropped the pixel/icon-fidelity expectation: the candidate only needs to convey screens, states, and flow. |
| Specialist contracts permitted a decisive recommendation but did not make it the default, so a session could interrogate the owner with a question per choice instead of proposing one | Added a shared decision protocol to SKILL-CONTRACT.md: analyze, recommend decisively with rationale, proceed as a labeled draft when reversible, bundle consequential choices, and batch currently known blockers. A later focused batch is permitted only for a newly revealed blocker; defaults are stated only when defensible. |
| Failed backfill could leave `.project-meta/` or a partially restructured root | Moved all validation before mutation, prepared metadata in staging, validated the final shape, added rollback for handled failures, and exercised an injected failure after the repository move. |
| Structural discovery alone did not reliably activate runtime instructions | Added root `AGENTS.md` and `CLAUDE.md` outside both repositories and made opening the project root an operating requirement. |
| A durable absolute library path broke cross-device use | Replaced it with a stable library ID plus per-device environment, invoked-skill, and ignored local configuration resolution. |
| Prototype dependencies, secrets, and build output could enter metadata history | Added metadata and prototype `.gitignore` templates while retaining useful source, configuration, and lockfiles. |
| “Ask once” and “always recommend a default” were too absolute | Defined batches around currently known blockers, allowed newly discovered blockers, and required a default only when evidence supports one. |
| Metadata Git history had no defined checkpoints | Bootstrap now makes the baseline commit; the operating policy adds review, approval, and verified/closed checkpoints while leaving `workspace/` commits to the implementation project. |

## Remaining validation boundary

The written contracts and disposable bootstrap checks pass. These stronger validation layers have not been performed:

- creating personal skill symlinks;
- verifying skill discovery in Claude, Codex, or a VS Code agent;
- running Project Master end to end against a real new project and a real existing project.

Claims in this review are limited to static consistency and isolated filesystem behavior until those runtime and real-project pilots are completed.
