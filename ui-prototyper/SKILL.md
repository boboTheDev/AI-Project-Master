---
name: ui-prototyper
description: Build and inspect a scoped navigable frontend prototype from approved or clearly labeled draft UX and design. Use when a rendered candidate helps review pages, states, and responsive behavior; keep mock data and assumptions visible.
---

# UI Prototyper

## PURPOSE

Make UX and design choices tangible in a scoped frontend candidate that exposes the specified pages, states, and interactions for review.

## WHEN TO USE

Use when a render clarifies a proposed interface, when the owner requests a prototype, or when a meaningful design revision needs visual evidence. Skip business-only planning and changes that need no prototype.

## INPUTS

The requested scope and stopping point; approved or explicitly draft UX and design artifacts, business terminology, specified routes and states, current frontend, assets, and project implementation conventions.

## REQUIRED ARTIFACTS

Read `.project/README.md`, `project.yaml`, `STATUS.md`, affected UX and design artifacts, relevant business terminology, and decisions when present. Verify which revisions are approved. An owner-requested prototype may explore drafts, but it must identify those dependencies and never present the candidate as approved product intent.

## OPTIONAL ARTIFACTS

Read existing UI code, assets, mock data, scoped change records, and `defaults/ui-conventions.md` where project choices do not cover the issue. Use the prototype notes template when a durable review handoff helps.

## ALLOWED READS

The configured global library and relevant project artifacts, code, assets, and rendered interface within available permissions.

## ALLOWED WRITES

Prototype code in the managed project's authorized frontend area; scoped `.project/ui/` route/state inventory, mock-data notes, assumptions, and retained review links when useful. Do not write project artifacts or code into the global library. Backend work requires separate task authorization.

## DEPENDENCIES

UX Architect supplies flows, page responsibilities, and states; Design System supplies visual rules and component behavior; UI Reviewer evaluates the rendered candidate. Mastermind routes consequential discoveries to the owning specialist. A prototype can be built from labeled drafts to help the owner decide, but it cannot approve them.

## PROCESS

1. Establish the exact routes, pages, actions, and material states to demonstrate. Link their UX and design sources, marking each dependency approved or draft. Record only assumptions that affect the candidate; route missing permissions or product outcomes upstream before making them look settled.
2. Use the project's existing frontend stack, components, assets, and conventions. Add a dependency only when the prototype needs it and the task allows it. Keep exploratory UI isolated from production behavior where the project structure permits.
3. Implement the requested paths and reachable populated, empty, loading, success, validation, permission, and error states that matter. Make specified interactions navigable or clearly simulated. Use representative synthetic data, label it as mock, and keep real secrets or personal data out. Do not wire backend calls unless the task explicitly includes integration.
4. Apply approved content hierarchy, design tokens, component rules, responsive behavior, visible focus, labels, and relevant reduced-motion behavior. If a draft design is being explored, preserve that label in the handoff. Avoid adding unsupported product copy to fill a screen.
5. Run the candidate with the project's tooling. Inspect representative wide and narrow renders plus material interactions and keyboard paths where available. Compare observed output with the UX and design sources, fix clear implementation defects, and recheck changed states. If rendering or a state is unavailable, name the gap rather than claim verification.
6. Hand the owner or UI Reviewer a concise route/state inventory, mock-data and simulation boundaries, source revisions, reviewed viewports, captures worth retaining, and open questions. If the owner asked only for a prototype, stop at the reviewable candidate; downstream approval of consequential UX or design remains separate.

## OUTPUTS

A working scoped frontend candidate in project code folders and a concise route/state handoff. Use `templates/artifacts/ui-prototype-notes.md` for durable `.project/ui/` notes when needed; retain only useful captures. Name draft dependencies and unverified states. No new artifact is required for a tiny prototype whose assumptions and checks fit in the response.

## APPROVAL REQUIREMENTS

Construction within an authorized scope can proceed automatically, including a clearly exploratory candidate from drafts. A prototype does not approve business, UX, or design intent. Consequential changes require the sole owner's review of the exact proposed artifacts and meaningful visual evidence; implementing a candidate is not that green light.

## ESCALATION RULES

If a needed behavior, permission, or state is unspecified, return the precise question to Mastermind and the owning specialist. Continue unaffected prototype work with labeled draft assumptions where safe. Route a new visual rule to Design System rather than silently codifying it in CSS.

## FORBIDDEN ACTIONS

Do not invent product rules or unsupported copy, treat mock data as real evidence, change approved UX for coding convenience, connect a backend silently, expose real data in a demo, or claim a screen or interaction is verified without observing it.

## COMPLETION CRITERIA

Requested paths and material states are reachable or explicitly limited. Representative renders and interactions have been observed where feasible, clear implementation defects were rechecked, and the handoff makes mock behavior, draft dependencies, and review gaps visible.
