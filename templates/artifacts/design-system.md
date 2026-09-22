---
status: draft
owner: project_owner
revision: 1
depends_on: []
---

# Design System

## Owner review brief

State the exact direction or shared rule revision, affected screens and states, linked preview, related artifact and draft ADR revisions shown to the owner, and exclusions.

## Approved inputs and existing UI

Link approved UX and design sources, brand constraints, and decisions. Describe current tokens, components, and renders separately as observations.

## Visual direction

Explain the product context, audience, tasks, and intended visual character in a few sentences. Give the reason for a significant departure from existing approved direction.

## Principles and tokens

Define only needed semantic color roles, typography hierarchy, spacing, sizing, surfaces, density, layout, responsive, motion, and imagery or icon rules. Link token files when they exist; do not invent a full catalog for a narrow change.

## Components and states

List reusable roles, variants, relevant focus, hover, disabled, loading, error, and selected states. State contrast, legibility, non-color cue, focus, and reduced-motion checks where relevant.

## Examples and review

Link representative wide and narrow previews or screens and material states when visual judgment requires them. State what was rendered and what remains unverified. Compare meaningful alternatives and mark proposed versus approved rules.

## Open questions and handoff

Route missing UX or product behavior upstream. Name the approved rules and examples a prototype should use; keep dependent design draft.

## Approval record

After the owner approves this exact revision, record `status: approved`, `revision`, `approved_by: project_owner`, and `approved_on` in frontmatter. A linked ADR remains draft unless its exact revision was also reviewed.
