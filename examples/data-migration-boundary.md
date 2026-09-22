# Example: Data Model and Migration Boundary

This fictional case separates data design approval from permission to run a migration.

1. An approved rule says member email addresses must be unique within an organization. The current schema has no matching constraint, and a scoped query finds duplicate values. Data Architect records the approved rule, schema evidence, duplicate count without personal data, and affected readers and writers. The current schema is observed state, not approved intent.
2. The product has no approved rule for resolving existing duplicates. Data Architect can draft a staged uniqueness constraint and compatibility plan, but the backfill step depends on that product choice. Mastermind returns only the duplicate-resolution question to Business Architect and the owner. The dependent data revision stays draft.
3. Once the owner settles the duplicate-resolution rule, Data Architect completes the draft data revision with migration order, dry-run checks, verification, and recovery limits. A meaningful lasting tradeoff may have a draft ADR. Mastermind shows the owner those exact business, data, and ADR revisions for review. Approval of the design permits an implementation handoff; running a migration against real data still follows its own task authorization and safeguards.
