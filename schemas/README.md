# Metadata Schemas

These JSON Schemas describe the YAML data in `.project-meta/project/project.yaml` and the extracted YAML frontmatter of project artifacts. They do not validate the prose of Markdown documents or grant approval. The `$id` values are identifiers for local schema resolution, not network services.

Evidence and handoff reports such as an Enforcer review, UI review, or prototype notes may be plain Markdown without approval-lifecycle frontmatter. They record what was checked or demonstrated; they do not become approved intent.

- `project-manifest.schema.json`: stable Project Master library identity and contract version, project paths, selected profile, and default approval categories. Device-local library paths stay in ignored `.project-meta/local.yaml` and are outside this durable schema.
- `artifact-metadata.schema.json`: lifecycle state and required original approval evidence for `approved` and retained `superseded` revisions.
- `decision-metadata.schema.json`: ADR identifiers, artifact lifecycle metadata, and a replacement link required when an ADR is superseded.
- `change-metadata.schema.json`: CHG identifiers, owner-review status, independent implementation state, affected domains, and linked ADRs.

Schemas are version-one starting contracts. A validator should resolve the sibling `$ref` files locally and validate frontmatter only after parsing YAML. Human review remains the authority for whether a consequential revision is approved.
