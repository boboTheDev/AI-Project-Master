# Example: Enforcer Alignment Check

These cases show how one scoped check can end in a fix, a review question, or an observation.

1. An approved business artifact says expired invites are rejected. The current API accepts them, and a targeted request reproduces the behavior. The task authorizes an API fix. Enforcer records the artifact revision, endpoint, request result, and severity; corrects the bounded code path; reruns the targeted check; and marks the finding fixed and rechecked. No new owner approval is needed because the approved rule did not change.
2. An approved business artifact says an invite expires after seven days, while a current approved technical artifact says fourteen. Enforcer records both source links as a source conflict. It does not edit code toward either number. Mastermind routes the specific choice to the owner and affected specialists; only the affected work waits.
3. A newly adopted project has code that accepts invites for fourteen days but no approved business rule. Enforcer records observed behavior and test evidence in an observation inventory. Business Architect may propose a fourteen-day rule as a draft, but the code does not make it approved. Mastermind presents the concrete draft to the owner.
