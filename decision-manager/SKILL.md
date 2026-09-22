---
name: decision-manager
description: Record and maintain ADRs for consequential project choices with lasting rationale, alternatives, or supersession. Use when a proposed choice warrants an owner-reviewed decision record; skip routine details already clear in approved artifacts.
---

# Decision Manager

## PURPOSE

Keep a durable trail of why important choices were made, what the owner approved, and how later choices supersede them. Current approved project artifacts remain the source of current behavior.

## WHEN TO USE

Use when a product, business, technical, data, UX, or design choice has lasting consequences, a meaningful alternative, a cross-domain tradeoff, an exception to an approved direction, or replaces an earlier ADR. Do not create an ADR for every requirement, acceptance criterion, routine fix, or restatement of an existing approved choice. Link an existing ADR when it already explains the decision.

## INPUTS

The concrete proposed choice, its evidence and alternatives, affected artifact revisions, related change record, prior ADRs, and the owner's review outcome when available.

## REQUIRED ARTIFACTS

Read `.project/README.md`, `project.yaml`, relevant current approved artifacts and proposed revisions, and records in the manifest's `decision_directory`. Confirm the next ID from actual files; do not rely on `STATUS.md` alone. During backfill, treat inferred choices as draft even when code implements them.

## OPTIONAL ARTIFACTS

The scoped change record, evidence behind alternatives, and the library's ADR template when useful.

## ALLOWED READS

The configured global library and relevant managed-project artifacts and evidence.

## ALLOWED WRITES

The configured `decision_directory`, including supersession metadata on old records, and accurate links in scoped project artifacts, change records, or `STATUS.md`. The owning specialist updates the meaning of a current product or technical artifact.

## DEPENDENCIES

The owning specialist supplies the choice, alternatives, and impact. Mastermind coordinates the owner review packet and cross-domain updates. An ADR may be reviewed together with its linked artifact revision; it does not require a separate approval ceremony when both are explicitly in the same packet.

## PROCESS

1. Decide whether a durable ADR adds value under `WHEN TO USE`. Search existing records first. Reuse or link an existing ADR for the same approved choice; do not create a duplicate merely because a new feature cites it.
2. For a new choice, assign the next sequential `ADR-###` ID from existing filenames. Put one coherent decision in each record: context and evidence, exact proposed choice, realistic alternatives, consequences, affected current artifacts, related change, and any ADR it would replace. Label inferred history and unsupported claims.
3. Keep the ADR `draft` or `needs-review` while planning. Include its exact revision in Mastermind's owner review packet alongside any linked artifact revisions. Keep an ADR draft if a dependent open question changes the choice; place independent open choices in separate drafts.
4. After the owner gives a green light to this exact ADR revision, record `status: approved`, its revision, `approved_by: project_owner`, and `approved_on`. Link the approved artifact and any related change record. If the owner approved only the linked artifact and did not review this ADR, leave the ADR draft until its wording is reviewed.
5. When an approved new ADR replaces an older one, set the older record to `superseded`, add `superseded_by: ADR-###`, and link `supersedes: ADR-###` from the new record. Preserve the older record's original approval metadata and rationale. Coordinate current artifact updates with the owning specialist; an ADR is not the current requirements document.
6. If a proposed or existing approved ADR conflicts with another approved source, surface the exact conflict to Mastermind before changing authority. Update `STATUS.md` and scoped links only from the settled record state.

## OUTPUTS

An `ADR-###-slug.md` in the configured `decision_directory` only when warranted, with a reviewable choice and rationale, approval metadata for the exact reviewed revision, and links to affected current artifacts and change records. Superseded records retain history and point to their replacement.

## APPROVAL REQUIREMENTS

The sole owner approves a consequential ADR after reading its concrete revision, possibly in one packet with related artifact revisions. Approval of an artifact alone does not approve an unseen ADR or independent linked draft. A change to an approved decision requires a new reviewed revision or superseding ADR; mechanical link or formatting repairs may proceed automatically when they cannot change meaning.

## ESCALATION RULES

Report a conflict with another approved decision or current approved artifact to Mastermind, naming both sources and the affected scope. Do not pick a winner by recency alone. If a proposed choice depends on an unresolved product rule, return it to the owning specialist and keep the ADR draft.

## FORBIDDEN ACTIONS

Do not mark an inferred, proposed, or unseen ADR approved; recycle IDs; erase or silently rewrite approved history; supersede an ADR before its replacement is approved; or turn the decision directory into a duplicate source of current project rules.

## COMPLETION CRITERIA

The record adds a distinct rationale, its exact reviewed revision and owner approval are visible, current artifacts and changes link to it, and any superseded record remains discoverable with accurate history. If no ADR is warranted, the existing approved source is linked and no extra record is created.
