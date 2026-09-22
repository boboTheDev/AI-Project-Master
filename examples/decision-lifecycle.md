# Example: A Decision Record's Lifecycle

This fictional example illustrates when an ADR helps and how it is approved. It does not establish a rule for any real project.

The owner wants managers to restore archived projects. Business Architect drafts the restore behavior. Two plausible return states exist: the project's previous state or Active. Because the choice has lasting product consequences, Decision Manager drafts `ADR-015-restore-target-state.md` with the proposed Active choice, alternative, consequences, and links to the business revision and change record.

Mastermind shows the owner both the business revision and the ADR in one review packet. If the owner green-lights both exact revisions, the business artifact and ADR are marked approved with that review date. If the owner reads and approves only the business revision, the ADR remains draft until reviewed. A question about sending a notification stays in a separate draft and is not covered by either approval.

Later, the owner changes the return state to the previous state. Decision Manager drafts `ADR-024-restore-previous-state.md` and links `supersedes: ADR-015`. Only after the owner approves the new ADR and updated business artifact does `ADR-015` become `superseded` with `superseded_by: ADR-024`. Its original rationale and approval metadata remain available.

A routine alignment fix to the Restore button needs no ADR; it follows the existing approved UX and design artifacts.
