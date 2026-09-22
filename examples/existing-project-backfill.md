# Example: Backfill an Existing Project

This fictional walkthrough separates observed implementation from owner-approved intent.

1. Mastermind creates the minimal `.project/` bootstrap and sets `STATUS.md` to unassessed. It identifies the code and documents relevant to current behavior.
2. Enforcer records observable facts with file, test, schema, or rendered evidence. Because there is no approved baseline, its report is an observation inventory, not a drift report. It names gaps it could not verify. Business Architect drafts a product description, Technical Architect reconstructs system boundaries, and other specialists join only where the repository has those domains.
3. Every reconstructed artifact is `draft` or `needs-review`. A note such as "the API currently rejects expired invites" is an observation; "expired invites must be rejected" is proposed intent until the owner confirms it.
4. Mastermind groups consequential uncertainties into a review brief. The owner approves or corrects concrete revisions; Decision Manager records meaningful confirmed choices. Only then can Enforcer use those approved revisions as a drift baseline. `STATUS.md` becomes an index of what is approved and what remains unknown.

Backfill does not turn the codebase into automatic product authority.
