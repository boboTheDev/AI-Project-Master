# Working Conventions

These defaults fill gaps in a managed project's own conventions. They do not override explicit project choices.

- Keep approved intent, drafts, observations, and open questions distinguishable. Cite the artifact, decision, file, or evidence behind consequential claims.
- Default to a decisive recommendation over a question; follow the shared decision protocol in SKILL-CONTRACT.md so the owner reviews concrete proposals, not a running interrogation.
- Use plain, searchable Markdown for durable reasoning. Add diagrams as text-based Mermaid or DBML where a diagram clarifies relationships or flow.
- Name ADRs `ADR-###-slug.md` and consequential changes `CHG-###-slug.md`; assign the next ID from existing files, and preserve superseded history.
- Keep the current approved artifact at its canonical path. Stage a replacement separately as `<name>.proposed.md` or inside the active change's evidence area; after approval, preserve the prior revision through version history or retained change evidence and promote only the exact reviewed content.
- Treat CHG approval and implementation progress separately. Use `status` for review state and `implementation_state` for `not-started`, `in-progress`, `implemented`, `verified`, or `blocked`.
- Make an implementation handoff identify the approved sources, affected behavior, interfaces, likely files, and verification needed. Scale detail to the change.
- Check behavior with the project's existing tools. Add tests when they establish a meaningful invariant or catch a real regression; do not prescribe one coding or commit rhythm globally.
- Keep secret values out of `.project-meta/` and examples. Record required environment variable names and access assumptions without credentials.
- Update `STATUS.md` as a derived index after the underlying state changes; do not let it become a second requirements document.
