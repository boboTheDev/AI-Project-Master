# Example: Restore an Archived Project

This fictional walkthrough shows routing and approval; it is not a rule for any managed project.

1. The owner asks for a restore action. Mastermind reads approved business and UX artifacts and finds only archive behavior. It opens `CHG-014-restore-project.md` with `status: draft` and `implementation_state: not-started`, affecting business, UX, UI, and possibly database.
2. Business Architect drafts who may restore, what state the project returns to, and acceptance criteria. Unknown permission and retention behavior stay as open questions. Data Architect checks whether archived data can be restored without loss. UX Architect maps the action and success/error states; UI Prototyper may show a draft candidate without treating missing rules as settled.
3. If the return-to-Active choice has lasting alternatives, Decision Manager drafts an ADR explaining that choice before approval. Mastermind gives the owner a concrete packet: proposed restore rule, permission choice, data implications, UX flow, the draft ADR, and the artifacts that would change. The existing approved archive behavior remains authoritative while this packet is under review.
4. After the owner approves the exact artifact and ADR revisions shown, the affected `.project-meta/project/` artifacts and ADR become approved, the CHG records its reviewed packet, and `STATUS.md` links the change with implementation still `not-started`. The coding agent receives a handoff limited to `workspace/`. If the owner did not review the ADR, it stays draft.
5. Implementation moves the CHG through `in-progress` and `implemented`. Enforcer compares the implementation and rendered behavior with the approved artifacts; after the required checks pass, the CHG becomes `verified`. A new consequential discovery returns only the affected question to planning.

The example demonstrates why a change record tracks impact but does not replace approved business, UX, or data artifacts.
