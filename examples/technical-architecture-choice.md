# Example: A Technical Architecture Choice

These fictional cases show the boundary between a useful default, observed code, and approved architecture.

1. A new interactive browser app has `tech_profile: web-standard`, whose profile includes an optional Node API. The approved requirements need no server-side behavior. Technical Architect proposes a browser-only build and explains why no API is needed. The selected profile does not force an unused service into the architecture.
2. An existing project has an approved requirement to generate a report after a user request without holding the response open. Its current API generates reports in the request handler. Technical Architect compares a bounded background worker with keeping the current synchronous path, using latency, failure recovery, operating cost, and migration effort. It drafts the changed boundary, job contract, rollout, and verification plan. Data Architect owns any durable job-state schema; UX Architect owns progress and error states.
3. Because the worker changes approved system boundaries, Mastermind gives the owner the concrete technical revision and any draft ADR that explains the lasting choice. The current approved architecture remains in force until the owner green-lights the exact revisions shown. A routine code edit within that approved worker design can then proceed without another architecture approval.
