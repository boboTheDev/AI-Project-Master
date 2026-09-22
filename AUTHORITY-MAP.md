# Project Master Authority Map

This map defines who owns each kind of project decision and what each project-local file means. The project owner is the sole governor of consequential intent. Skills prepare, inspect, coordinate, and implement within authorization; they do not grant themselves approval.

## Decision ownership

| Area | Owning skill | Consulted skills | Authoritative result after owner approval |
| --- | --- | --- | --- |
| Product vision, actors, outcomes, scope, terminology, business rules, permissions, retention and deletion policy, acceptance semantics | Business Architect | Mastermind, then affected specialists | `.project/context/` and `.project/business/` |
| System boundaries, component responsibilities, interfaces, integrations, deployment direction, selected technology profile | Technical Architect | Business, Data, UX | `.project/tech/` and approved `project.yaml` profile or overrides |
| Persistent model, storage constraints, consistency, indexes, data migration design | Data Architect | Business for policy, Technical for boundaries, UX for visible states | `.project/database/` |
| Journeys, navigation, information hierarchy, page responsibilities, interaction outcomes and material states | UX Architect | Business, Technical, Data | `.project/ux/` |
| Visual direction, semantic tokens, reusable component rules, responsive and interaction styling | Design System | UX, Business for claims | `.project/design/` |
| Lasting rationale for a meaningful choice | Decision Manager, using content from the owning specialist | Mastermind and affected specialists | `.project/decisions/ADR-*.md` |
| Cross-domain scope, review packet, implementation coordination and status | Mastermind | All affected skills | `.project/changes/CHG-*.md` and `.project/STATUS.md`; these coordinate and index rather than define behavior |
| Frontend candidate and simulated states | UI Prototyper | UX and Design System | Prototype code and optional `.project/ui/` notes; these demonstrate behavior but do not approve intent |
| Rendered UI findings | UI Reviewer | UX, Design System, implementer | `.project/ui/` evidence; findings do not define intent |
| Alignment findings and safe authorized corrections | Enforcer | Owning specialist and Mastermind | Evidence under `.project/changes/` or affected review area; findings do not define intent |
| Implementation | Authorized coding agent | Relevant owning specialists and Enforcer | Project code, tests, migrations, and configuration; these show current behavior but do not approve intent |

## Information authority

| Information | Meaning | Can it authorize project behavior? |
| --- | --- | --- |
| Owner's concrete reviewed decision | Final governance input; update affected project artifacts to preserve it | Yes, for the exact scope reviewed |
| Current approved domain artifact | Current project intent in that domain | Yes |
| Approved ADR | Rationale and consequences of a meaningful decision | It supports intent but does not replace the current domain artifact |
| `project.yaml` | Project Master configuration, directories, review policy, selected defaults and overrides | Only for its configuration fields; it is not a requirements document |
| Draft or `needs-review` artifact | Proposal or review candidate | No |
| CHG record | Scope, review packet, links, and implementation progress | No; linked revisions keep their own approval state |
| `STATUS.md` | Derived index of approved, draft, active, blocked, and unverified state | No |
| Code, tests, schema, migrations, logs, and rendered UI | Evidence of current implementation | No |
| UI review, Enforcer report, prototype notes, screenshots | Evidence, findings, or simulation boundaries | No |
| Global defaults and templates | Reusable starting points | No; approved project choices and explicit owner instructions govern |
| Conversation history | Temporary context | No; persist consequential decisions in project artifacts |

There is no automatic winner when two approved sources conflict. Mastermind names both sources, the affected scope, and available choices for the owner. The owning specialists then update the exact reviewed artifacts. Recency, code behavior, an ADR, or a status entry alone does not silently resolve the conflict.

## Handoff map

| Discovery | Route | Required handoff |
| --- | --- | --- |
| Missing actor, permission, eligibility, outcome, retention, deletion, or product claim | Mastermind → Business Architect | Affected rule, evidence, downstream impact, and focused owner question if needed |
| New or changed system boundary, integration, interface, deployment, or stack choice | Mastermind → Technical Architect | Approved capability, constraints, affected components, and migration or compatibility concern |
| New persistent invariant, storage lifecycle, schema, or migration concern | Mastermind → Data Architect | Approved rules, system boundaries, observed schema, readers/writers, and data risk |
| New journey, navigation, hierarchy, or user-visible state | Mastermind → UX Architect | Actor, outcome, governing rules, constraints, and affected routes/pages |
| New shared visual or component rule | Mastermind → Design System | Approved UX, product context, affected components/states, and representative content |
| Need to see or compare a UI candidate | UX/Design System → UI Prototyper | Source revisions, routes, states, synthetic-data limits, and review question |
| Need rendered visual or interaction evidence | UI Prototyper/implementation → UI Reviewer | Build, baseline revisions, routes, states, viewports, and known gaps |
| Lasting meaningful choice with alternatives or supersession | Owning specialist → Decision Manager | Exact choice, context, alternatives, consequences, affected artifacts, and prior ADRs |
| Implementation differs from clear approved intent | Enforcer → authorized implementer or Mastermind | Expected versus observed, reproducible evidence, severity, scope, and safe disposition |
| Two approved sources conflict or intent is missing | Any skill → Mastermind | Exact sources, conflict or gap, affected work, and options; pause only dependent work |

## Approval boundary

The owner reviews small, coherent whole revisions. A single review packet may include several related artifact and ADR revisions, but approval applies only to the exact revisions shown. Independent drafts remain unapproved. A dependent unanswered question keeps the affected revision draft.

Routine authorized implementation, evidence collection, accurate status updates, and meaning-preserving corrections do not need a new green light. New or changed consequential intent follows the review lifecycle in [OPERATING-GUIDE.md](OPERATING-GUIDE.md).
