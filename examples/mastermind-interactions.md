# Mastermind Interaction Walkthroughs

These are fictional cases for Mastermind's main entry modes. Their project states and IDs are illustrative, not facts about a managed project.

## “Use Mastermind. Create a new project called Acme here, then help me define its business model.”

Mastermind resolves `Acme` as the display name and an ordinary folder slug such as `acme`, then creates and configures the project bootstrap in that folder. It verifies `.project/README.md`, `.project/project.yaml`, `.project/STATUS.md`, and the applicable agent entry instructions before asking product questions. Business Architect then helps shape the model, and every resulting draft is written under `acme/.project/` from the beginning. The bootstrap itself does not approve the business model.

## “Use Mastermind. Backfill this project.”

Mastermind confirms the current repository root and initializes it in existing-project mode. Missing bootstrap files are added, existing files are preserved, and agent entry instructions are merged when needed. Only after this setup does Mastermind inventory the repository, reconstruct useful drafts, separate evidence from inferred intent, and prepare focused owner review packets.

## “Use Mastermind. Tell me where we are in this project.”

Mastermind reads `.project/STATUS.md`, checks the referenced business and technical approvals, and finds a UX draft plus an active `CHG-014`. It reports the phase, approved areas, draft areas, pending owner review, open questions, and a suggested next step with links to those records. It corrects an index entry only if the underlying artifact proves it stale. It does not open another change record, infer approval from code, or begin implementation.

## “Use Mastermind as the brainstorming lead. Here is my scope; let's solidify business logic.”

Inside an initialized project, Mastermind reads existing approved business intent, asks the few product questions that change the rule, and uses Business Architect to draft actors, workflow, permissions, edge cases, and acceptance criteria. If the current directory is not yet a managed project and the request is for a new project, Mastermind obtains the missing name or target, bootstraps it, and then begins this conversation. It labels assumptions and returns a concise proposal showing the exact content that would become authoritative. If the owner gives a green light after reviewing that revision, the approved business artifact and any meaningful decision record are updated. The task ends at solidified business logic unless the owner also requested downstream design or implementation.

## “Use Mastermind to fix the misaligned Save button.”

Mastermind checks the approved UI context and sees a routine implementation defect. The working agent fixes the button and checks the rendered result; no new business proposal or owner approval is needed. If the fix reveals a missing consequential design rule, Mastermind routes only that question for review while unrelated routine work continues.
