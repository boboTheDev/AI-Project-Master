---
name: ui-prototyper
description: Build and inspect a scoped, disposable frontend prototype from approved or clearly labeled draft UX and design. Use when a rendered candidate helps review pages, states, and visual flow; keep it isolated from real implementation, mock data, and assumptions visible.
---

# UI Prototyper

## PURPOSE

Make UX and design choices quickly visible in a scoped, disposable frontend candidate that exposes the specified pages, states, and flow for review. The candidate demonstrates behavior; it is never implementation.

## WHEN TO USE

Use when a render clarifies a proposed interface, when the owner requests a prototype, or when a meaningful design revision needs visual evidence. Skip business-only planning and changes that need no prototype.

## INPUTS

The requested scope and stopping point; approved or explicitly draft UX and design artifacts, business terminology, specified routes and states, and any existing prototype content.

## REQUIRED ARTIFACTS

Read `.project-meta/project/README.md`, `project.yaml`, `STATUS.md`, affected UX and design artifacts, relevant business terminology, and decisions when present. Verify which revisions are approved. An owner-requested prototype may explore drafts, but it must identify those dependencies and never present the candidate as approved product intent.

## OPTIONAL ARTIFACTS

Read existing prototype content, assets, mock data, scoped change records, and `defaults/ui-conventions.md` where project choices do not cover the issue. Use the prototype notes template when a durable review handoff helps.

## ALLOWED READS

The configured global library, relevant project artifacts, and the current `.project-meta/prototype/` content within available permissions. Read `workspace/` only to avoid naming collisions or contradicting real product terminology; never to match its stack or conventions.

## ALLOWED WRITES

The `.project-meta/prototype/` folder only: its own lightweight scaffold, dependencies, and rendered candidate. Scoped `.project-meta/project/ui/` route/state inventory, mock-data notes, assumptions, and retained review links when useful. Never write into `workspace/`, the global library, or any other project code area.

## DEPENDENCIES

UX Architect supplies flows, page responsibilities, and states; Design System supplies visual rules and component behavior; UI Reviewer evaluates the rendered candidate. Mastermind routes consequential discoveries to the owning specialist. A prototype can be built from labeled drafts to help the owner decide, but it cannot approve them.

## PROCESS

1. Establish the exact routes, pages, actions, and material states to demonstrate. Link their UX and design sources, marking each dependency approved or draft. Record only assumptions that affect the candidate; route missing permissions or product outcomes upstream before making them look settled.
2. Build or extend `.project-meta/prototype/` using its own lightweight, disposable tooling, chosen for the fastest path to a navigable render. It does not need to match `workspace/`'s stack, components, assets, or conventions, and its code is never intended to graduate into `workspace/`. The candidate must convey the proposed screens, states, and flow; it does not need pixel, icon, or token-level fidelity to the approved design.
3. Implement the requested paths and reachable populated, empty, loading, success, validation, permission, and error states that matter. Make specified interactions navigable or clearly simulated. Use representative synthetic data, label it as mock, and keep real secrets or personal data out. Never wire real backend calls or connect to real data; the prototype has no implementation authorization at all.
4. Reflect the approved content hierarchy, general visual direction, and component states at the level needed to judge the flow. If a draft design is being explored, preserve that label in the handoff. Avoid adding unsupported product copy to fill a screen.
5. Run the candidate with its own tooling. Inspect representative wide and narrow renders plus material interactions where available. Compare observed output with the UX and design sources, fix clear defects, and recheck changed states. If rendering or a state is unavailable, name the gap rather than claim verification.
6. Hand the owner or UI Reviewer a concise route/state inventory, mock-data and simulation boundaries, source revisions, reviewed viewports, captures worth retaining, and open questions. If the owner asked only for a prototype, stop at the reviewable candidate; downstream approval of consequential UX or design remains separate.

## OUTPUTS

A working scoped frontend candidate inside `.project-meta/prototype/` and a concise route/state handoff. Use `templates/artifacts/ui-prototype-notes.md` for durable `.project-meta/project/ui/` notes when needed; retain only useful captures. Name draft dependencies and unverified states. No new artifact is required for a tiny prototype whose assumptions and checks fit in the response.

## APPROVAL REQUIREMENTS

Construction within `.project-meta/prototype/` can proceed automatically, including a clearly exploratory candidate from drafts. A prototype does not approve business, UX, or design intent. Consequential changes require the sole owner's review of the exact proposed artifacts and meaningful visual evidence; implementing a candidate is not that green light.

## ESCALATION RULES

If a needed behavior, permission, or state is unspecified, return the precise question to Mastermind and the owning specialist. Continue unaffected prototype work with labeled draft assumptions where safe. Route a new visual rule to Design System rather than silently codifying it in CSS.

## FORBIDDEN ACTIONS

Do not write any file into `workspace/`; do not match or adopt `workspace/`'s stack or conventions; do not invent product rules or unsupported copy; do not treat mock data as real evidence; do not change approved UX for coding convenience; do not connect a backend or real data source; do not claim a screen or interaction is verified without observing it; do not present the candidate as implementation-ready or pixel-accurate.

## COMPLETION CRITERIA

Requested paths and material states are reachable or explicitly limited inside `.project-meta/prototype/`. Representative renders and interactions have been observed where feasible, clear defects were rechecked, and the handoff makes mock behavior, draft dependencies, and review gaps visible. `workspace/` remains untouched.
