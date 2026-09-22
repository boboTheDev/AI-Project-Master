---
status: draft
owner: project_owner
revision: 1
depends_on: []
---

# Data Model

## Owner review brief

State the exact proposed data revision, impact, related artifact and draft ADR revisions shown to the owner, and independent exclusions. Keep dependent unresolved policy draft.

## Approved inputs and observed state

Link approved product rules, technical boundaries, current data intent, and decisions. Describe actual schema, migration history, and data evidence separately.

## Entities and invariants

Describe affected ownership, keys, relationships, validation, constraints, sensitive data, access rules, and creation, update, archive, deletion, and retention behavior. Trace consequential invariants to approved sources.

## Access and consistency

Name important readers, writers, queries, indexes, transactions, and consistency needs with their justification.

## Migration plan

For an existing database, describe deployment order, old and new reader/writer compatibility, backfill, verification, and rollback or recovery. Mark destructive, irreversible, or uncertain steps and the authorization needed before execution. Omit when no migration is involved.

## Alternatives and open questions

Compare meaningful model choices and migration tradeoffs. Separate approved facts from assumptions; route missing retention, permission, or lifecycle rules to their owner.

## Relationships

Link a text-based Mermaid or DBML diagram when it clarifies the model.

## Approval record

After the owner approves this exact revision, record `status: approved`, `revision`, `approved_by: project_owner`, and `approved_on` in frontmatter. A linked ADR remains draft unless its own exact revision was also reviewed.
