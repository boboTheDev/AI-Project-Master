---
name: design-system
description: Define or revise a managed project's visual direction, semantic tokens, component rules, responsive behavior, and interaction styling from approved UX. Use for shared or consequential design choices; skip isolated implementation defects.
---

# Design System

## PURPOSE

Turn approved UX into a coherent visual language and reusable component rules that can be judged in context and implemented consistently.

## WHEN TO USE

Use for a new product's visual direction, a consequential refresh, a shared component or token decision, or design-system backfill. Skip for an isolated implementation defect with an existing approved rule.

## INPUTS

The requested design scope and stopping point; approved UX, product context, audience and tasks, terminology, brand and accessibility constraints, existing components and assets, and approved design decisions.

## REQUIRED ARTIFACTS

Read `.project/README.md`, `project.yaml`, `STATUS.md`, affected approved `.project/ux/` and `.project/design/` artifacts, and related decisions when present. Check approval metadata. Inspect current tokens, components, and rendered UI when extending a project; they are evidence of implementation, not automatic approval of visual intent. Keep design that depends on draft UX provisional.

## OPTIONAL ARTIFACTS

Read `defaults/ui-conventions.md`, brand references, relevant content and assets, and scoped change records when useful. Global conventions prompt judgment; they never override approved project choices.

## ALLOWED READS

The configured global library and relevant project artifacts, code, assets, and rendered interface evidence within available permissions.

## ALLOWED WRITES

Scoped `.project/design/` drafts, previews and approval evidence, or approved revisions after owner review; design impact in a relevant `.project/changes/` record; accurate `STATUS.md` links. Write implementation tokens or components only when separately authorized. Keep project design out of the global library.

## DEPENDENCIES

UX Architect owns workflow, content hierarchy, and interaction outcomes. Business Architect owns product claims. UI Prototyper renders a design candidate; UI Reviewer supplies observed visual and interaction evidence. Mastermind routes conflicts and owner review. Decision Manager drafts an ADR only for a meaningful lasting visual choice.

## PROCESS

1. Establish the approved UX and design baseline, audience, content shape, existing system, and scope. Distinguish approved rules from observed UI and optional references. State a compact visual direction tied to the product's tasks and brand, with a reason for any departure.
2. Define only needed semantic color roles, typography hierarchy, spacing, sizing, surfaces, density, layout, responsive rules, motion, and imagery or icon treatment. Specify focus, hover, disabled, loading, error, and selected appearance where relevant. Prefer tokens and reusable rules over per-page exceptions; do not impose a universal aesthetic.
3. Define component roles and meaningful variants against approved UX states. Check contrast, legibility, visible focus, non-color cues, reduced motion, and the input modes that matter. Record how these will be verified in a render rather than claiming accessibility from a token list alone.
4. For a consequential direction, compare a small number of realistic visual approaches against task clarity, audience fit, brand constraints, reuse, accessibility, and implementation cost. Provide representative examples or a rendered preview for the screens and states the owner must judge. Use UI Prototyper for a provisional render when needed; label it draft.
5. Route a changed flow or content hierarchy to UX Architect and a new product claim to Business Architect through Mastermind. Keep dependent design draft until upstream meaning is settled. Independent token work may continue with labeled assumptions.
6. Present a small, coherent `.project/design/` revision and linked preview for owner review. Include the exact direction, token/component changes, affected screens, alternatives, and any warranted draft ADR. After approval of the exact revisions shown, record metadata, update links and `STATUS.md`, and hand the approved rules and state examples to UI Prototyper. If the request was only planning or critique, stop at that outcome.

## OUTPUTS

Only needed `.project/design/` artifacts, usually `design-system.md` and, when distinct, token or component specifications. Use `templates/artifacts/design-system.md` if helpful. Link representative previews when visual judgment requires them; retain meaningful owner-review evidence. A draft backfill records observed conventions without approving them.

## APPROVAL REQUIREMENTS

Consequential visual direction, shared component rules, and interaction styling require the sole owner's green light on the concrete revision and preview where needed. Approval covers only exact artifact and ADR revisions shown; retain the current approved system while a replacement is proposed. Minor consistent use of approved tokens can proceed in authorized work without a new review.

## ESCALATION RULES

Route workflow or information hierarchy changes to UX Architect, product claims to Business Architect, and conflicts with approved design decisions to Mastermind. Report missing visual evidence or inaccessible preview states instead of claiming a design was verified.

## FORBIDDEN ACTIONS

Do not turn global aesthetic defaults or inspiration samples into project truth, invent unsupported content or brand claims, change navigation or product rules, treat observed UI as approved intent, or mark a proposed direction approved before owner review.

## COMPLETION CRITERIA

The needed visual rules and component states are coherent, reusable, and tied to project context. Consequential direction has a reviewable example or stated evidence gap, an exact approval boundary, and enough detail for a prototype and rendered check.
