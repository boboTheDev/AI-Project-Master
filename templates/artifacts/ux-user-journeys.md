---
status: draft
owner: project_owner
revision: 1
depends_on: []
---

# User Journeys

## Owner review brief

State the exact journey revision, actor and outcome, affected pages, related artifact and draft ADR revisions shown to the owner, and independent exclusions.

## Approved inputs and observed journey

Link approved business rules, relevant technical/data constraints, and current UX decisions. Describe existing rendered behavior separately from intended flow.

## Actors and goals

Name affected actors and their goals using approved product behavior or labeled research evidence.

## Primary journey

State entry point, actions, decisions, system response, recovery, and outcome in order. Explain removed or added steps that change the task.

## Material alternate states

For each relevant empty, loading, success, validation, permission, error, or interruption state, give its trigger, feedback, available action, and recovery or next step.

## Screens and information hierarchy

List navigation, page responsibilities, content priority, and structural controls. Include focus and responsive structure where they change the flow. Leave visual treatment to Design System.

## Alternatives and tradeoffs

Compare meaningful journey options by task completion, clarity, effort, and recovery. Omit when no consequential UX choice exists.

## Open questions and handoff

Identify product, technical, or data gaps and the affected downstream pages. Keep a dependent revision draft until its governing answer is settled; label exploratory handoffs.

## Approval record

After the owner approves this exact revision, record `status: approved`, `revision`, `approved_by: project_owner`, and `approved_on` in frontmatter. A linked ADR remains draft unless its exact revision was also reviewed.
