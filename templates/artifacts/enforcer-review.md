# Enforcer Review

This is an evidence record, not an approval of product intent. Keep it under the managed project's `.project-meta/project/changes/` or affected review folder when a finding needs to persist.

## Scope and baseline

State the requested scope, reviewed revision or build, and links to the approved artifacts and decisions used as the baseline. If there is no approved baseline, label this an observation inventory and list the missing sources.

## Evidence and limits

List the code paths and lines, tests and results, migrations, or rendered routes and states inspected. Say what could not be verified.

## Findings

| Category | Severity | Expected vs observed | Evidence | Owning domain | Disposition |
| --- | --- | --- | --- | --- | --- |

Use `blocking`, `material`, or `minor` for severity. Mark suggestions and unverified observations plainly; neither is proven drift.

## Resolution and verification

Link fixes and the checks that reverified them. For open findings, name the affected artifact or code area, proposed next action, and any owner review needed. Link the persistent finding from `STATUS.md` without copying the full report there.
