# Candidate Technology Profiles

These are reusable starting choices, not approved project architecture. `tech_profile: null` in a managed project's manifest means no profile is selected. Explicit owner instructions and approved project architecture govern. An existing project's working stack is evidence and often the lowest-change option, but it does not itself approve future architecture. A selected profile fills unresolved choices; it does not override approved project decisions. Its project-specific architecture still needs owner review when consequential.

## `web-standard`

For a conventional browser-based product with an optional API and relational persistence:

| Concern | Starting choice | Use only when |
| --- | --- | --- |
| Frontend | TypeScript, React, Vite | The project needs an interactive browser app and has no stronger existing framework choice. |
| API | TypeScript, Node.js | The product needs a separate server; do not add one for a static or local-only interface. |
| Data | PostgreSQL | Durable relational data is needed; do not add a database just to complete a template. |
| Browser verification | Playwright or the project's existing browser tool | Rendered or interaction evidence materially helps the task. |

Prefer existing project tooling when extending a repository. Record selected versions, hosting, authentication, deployment, and unusual constraints in the project's `.project/tech/`; this profile does not choose them. A project may override any row in `project.yaml` and document the reason in an approved technical artifact or decision. Technical Architect proposes a profile or override; it does not silently select one in the manifest.
