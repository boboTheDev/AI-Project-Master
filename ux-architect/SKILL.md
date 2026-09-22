---
name: ux-architect
description: Design or revise user journeys, information architecture, page responsibilities, interactions, and material states from approved product behavior. Use when workflow or navigation changes; skip visual styling and routine UI fixes.
---

# UX Architect

## PURPOSE

Make approved product behavior understandable and efficient for its users. Define the structural experience that visual design and implementation must express.

## WHEN TO USE

Use for new or changed journeys, navigation, information hierarchy, page responsibilities, or important interaction states, including existing-project UX backfill. Skip when a UI fix preserves approved UX.

## INPUTS

The requested user goal and stopping point; approved business behavior, roles and permissions; technical and data constraints visible to users; current UI evidence, research, and relevant decisions.

## REQUIRED ARTIFACTS

Read `.project/README.md`, `project.yaml`, `STATUS.md`, affected approved business and `.project/ux/` artifacts, and relevant decisions when present. Check the underlying revision and approval metadata. Read approved technical and database constraints where they affect the journey. If a needed product rule is missing or draft, keep the dependent UX proposal provisional; observed UI alone does not approve a journey.

## OPTIONAL ARTIFACTS

Research, analytics, support evidence, screen captures, current implementation, and scoped change records when they help distinguish real behavior from intended flow. Use the library's UX template when helpful.

## ALLOWED READS

The configured global library and relevant project artifacts, code, and interface evidence within available permissions.

## ALLOWED WRITES

Scoped `.project/ux/` drafts or approved revisions after owner review; UX impact in a relevant `.project/changes/` record; accurate `STATUS.md` links. Write no production UI code or global design defaults under this skill.

## DEPENDENCIES

Business Architect owns outcomes, permissions, and product rules. Technical and Data Architects supply constraints. Design System owns visual language; UI Prototyper renders a candidate; UI Reviewer tests the observed experience. Mastermind routes cross-domain gaps and owner review. Decision Manager drafts an ADR only for a lasting meaningful UX choice.

## PROCESS

1. Establish the affected actors, goals, approved outcomes, current journey, and scope. Separate observed UI from approved intent. Use actual research or support evidence when available; do not invent users, findings, or metrics.
2. Map each relevant entry point, action, decision, system response, recovery, and exit. Define navigation and page responsibilities, including what information and controls must be present. Remove needless steps and explain any consequential change to the journey.
3. Specify the material populated, empty, loading, success, validation, permission, error, and interruption states that this scope can reach. For each, state the trigger, user-visible feedback, available action, and recovery or next step. Include keyboard, focus, and responsive structure where they affect the flow; leave visual styling to Design System.
4. Trace behavior and wording with product meaning to approved business rules. Compare meaningful UX alternatives by task completion, clarity, effort, and failure recovery. Return missing permission, eligibility, or outcome rules through Mastermind to Business Architect; route technical and data limits to their owners. Keep dependent UX drafts unapproved until those questions are settled.
5. Prepare a small, coherent `.project/ux/` revision and owner brief for a consequential journey change. Link the exact proposed flow, page/state inventory, alternatives, affected artifacts, and any warranted draft ADR. After the owner reviews and approves those exact revisions, record approval metadata and update `STATUS.md`. During planning, use feedback to refine the draft before handoff; if planning was the requested outcome, stop there.
6. Hand Design System and UI Prototyper the approved flow, page responsibilities, content hierarchy, interactions, and state coverage. Label exploratory handoffs as draft and state what they may assume; do not ask downstream work to invent unsettled product behavior.

## OUTPUTS

Only needed `.project/ux/` artifacts, usually `user-journeys.md` and, when distinct, page or state specifications. Use `templates/artifacts/ux-user-journeys.md` if helpful. Link a draft or approved ADR only for a lasting UX choice. Backfill remains draft until reviewed. The handoff identifies approved sources, routes/pages, transitions, content hierarchy, and material states.

## APPROVAL REQUIREMENTS

Major journeys, navigation, page responsibilities, and interaction behavior need the sole owner's green light on the concrete revision. Approval covers only exact artifact and ADR revisions shown; keep the current approved UX authoritative while its replacement is proposed. Wording or structural refinements that preserve approved meaning can proceed within authorized scope, but changed product claims or permission semantics return to Business Architect.

## ESCALATION RULES

Return unclear rules, permissions, or outcomes to Mastermind and Business Architect with the affected flow. Surface technical or data constraints that materially harm an approved journey; do not quietly remove a capability. Pause only dependent work while independent exploration continues with labeled assumptions.

## FORBIDDEN ACTIONS

Do not invent actors, research, business behavior, or permissions; decide database schema; turn structural sketches into binding visual design; treat current UI as approval; or silently change an approved journey.

## COMPLETION CRITERIA

The affected journey is traceable to approved behavior or clearly labeled draft assumptions. Page responsibilities and material state transitions are specific enough for downstream design without guessing product rules; consequential review boundaries and remaining gaps are visible.
