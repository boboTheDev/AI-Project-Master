# Project Master Integration Review

Review date: 2026-09-22

This static review covers all ten skills, shared contracts, templates, schemas, examples, defaults, project entry files, and local-link adapters. It checks the written system as one operating model. Runtime discovery and a real-project pilot remain separate activities.

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
| New project | Bootstrap → Mastermind → relevant domain drafts → consolidated owner review → approved artifacts → implementation → Enforcer | Coherent. Empty specialist folders and unnecessary ADRs or CHGs are avoided. |
| Existing-project backfill | Bootstrap as unassessed → Enforcer observation inventory → specialist reconstructions → owner review → approved baseline | Coherent. Code and tests remain evidence until the owner approves reconstructed intent. |
| Consequential feature | CHG → affected specialists → warranted ADR → exact review packet → canonical artifact promotion → implementation → verification | Coherent after defining separate proposed replacement files and distinct CHG implementation state. |
| Routine implementation fix | Read approved context → implement within authorized scope → targeted check → optional Enforcer finding | Coherent. No unnecessary CHG, ADR, or owner review is required. |
| Conflicting approved artifacts | Name both sources → pause affected work → Mastermind presents focused choice → owner decides → owning specialists revise artifacts | Coherent. Neither code, recency, status, nor ADR automatically wins. |
| Database migration | Business policy → technical boundary → data design → owner approval → implementation handoff → separate operational authorization → verification | Coherent. Approving the schema does not authorize executing against real data. |
| UI proposal and review | Approved or labeled draft UX → design rules and preview → prototype with simulations → rendered UI review → targeted corrections or upstream proposal | Coherent. Prototype and review evidence never approve product, UX, or design intent. |

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
- Project artifacts and evidence stay under the managed project's `.project/`.
- Implementation stays in project code directories.
- `project.yaml` configures directories, default approval categories, selected profile, and overrides; it does not replace domain artifacts.
- `STATUS.md` is derived and links underlying sources.
- Decision and change IDs use `ADR-###` and `CHG-###`.
- A selected technology profile fills unresolved choices but does not override approved project architecture.
- Project entry files lead agents to the canonical `.project/README.md` bootstrap.
- All ten skills use the common fourteen-section contract.

The reusable validator in `tools/validate-library.py` checks the skill set and headings, frontmatter basics, JSON syntax, template metadata, required bootstrap files, local Markdown links, adapter shell syntax, and exact CHG implementation-state agreement.

Validation completed successfully on 2026-09-22:

- `python3 project-master/tools/validate-library.py` passed every static check.
- All skill and lifecycle-template frontmatter parsed with the available Ruby YAML parser.
- The Python validator compiled with its cache redirected to a writable temporary path.
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

## Remaining validation boundary

The static integration model is complete. These activities have not been performed:

- creating personal skill symlinks;
- verifying skill discovery in Claude, Codex, or a VS Code agent;
- running Project Master against a real new project and existing project.

Those are installation and pilot steps rather than unresolved document-contract issues.
