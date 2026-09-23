# Project Master

Project Master is a global library of reusable agent skills for managed projects. Its design rationale is in [IDEA.md](../IDEA.md).

## Library

- [SKILL-CONTRACT.md](SKILL-CONTRACT.md) defines the shared shape and boundaries for each skill.
- [AUTHORITY-MAP.md](AUTHORITY-MAP.md) assigns domain ownership and distinguishes intent, rationale, coordination, and evidence.
- [OPERATING-GUIDE.md](OPERATING-GUIDE.md) explains initialization, common workflows, approval, implementation, verification, and backfill.
- [INTEGRATION-REVIEW.md](INTEGRATION-REVIEW.md) records the completed cross-skill static review and its remaining validation boundary.
- `mastermind/`, `business-architect/`, `technical-architect/`, `data-architect/`, `ux-architect/`, `design-system/`, `ui-prototyper/`, `ui-reviewer/`, `decision-manager/`, and `enforcer/` each contain a canonical `SKILL.md`.
- [defaults/](defaults/) contains optional starting conventions and a candidate `web-standard` technology profile. No profile is selected by the blank project manifest.
- [templates/project-meta/project/README.md](templates/project-meta/project/README.md) is the bootstrap document a managed project keeps in its private `.project-meta/`, beside its own `workspace/`.
- [templates/project-meta/project/project.yaml](templates/project-meta/project/project.yaml) is the minimal manifest.
- [templates/project-meta/project/STATUS.md](templates/project-meta/project/STATUS.md) is a derived state index.
- [templates/project-root/](templates/project-root/) contains the local `AGENTS.md` and `CLAUDE.md` adapters generated outside both repositories.
- [templates/project-meta/prototype/README.md](templates/project-meta/prototype/README.md) and its `.gitignore` define the disposable prototype boundary and exclude dependencies, secrets, and generated output.
- [templates/artifacts/](templates/artifacts/) contains optional specialist document shapes, including [prototype notes](templates/artifacts/ui-prototype-notes.md), a [UI review](templates/artifacts/ui-review.md), and an [Enforcer evidence report](templates/artifacts/enforcer-review.md); copying all of them into a project is unnecessary.
- [schemas/](schemas/) documents version-one manifest and artifact metadata.
- [examples/](examples/) illustrates Mastermind interactions, business and ADR approval boundaries, technical and data choices, an Enforcer alignment check, a UX-to-rendered-review handoff, a consequential feature change, and existing-project backfill.
- [adapters/](adapters/) contains personal skill linking instructions and explains the project-root adapters.
- [mastermind/scripts/bootstrap_project.py](mastermind/scripts/bootstrap_project.py) transactionally creates and commits `.project-meta/` beside a new `workspace/`, or restructures an existing repository in place while preserving its Git repository, remotes, history, branches, configuration, and working-tree state.
- [tools/validate-library.py](tools/validate-library.py) performs dependency-free static integration checks; [tools/validate-bootstrap.py](tools/validate-bootstrap.py) exercises isolated bootstrap and rollback behavior.

When onboarding a project, invoke Mastermind from the intended parent directory for a new project or from the root of an existing Git repository. It creates root runtime adapters plus sibling `.project-meta/` and `workspace/` repositories before planning. For backfill, it moves the repository's complete contents, including `.git`, under `workspace/` and preserves its Git state. Open subsequent agent sessions from the outer project root so both repositories are accessible. Create specialist artifacts and their subdirectories only when actual work calls for them.

The global library contains reusable behavior. A managed project's `.project-meta/` contains its intent, decisions, disposable prototype, and persistent context, as its own private repository. Implementation belongs in that project's `workspace/`, its own separate repository that can be shared with collaborators with no trace of Project Master. The sole project owner reviews consequential revisions; routine authorized work can complete automatically. Third-party material in [inspirations/](../inspirations/) is research material and does not govern Project Master.

The ten skills and their shared artifact model have a documented static integration review plus isolated bootstrap checks. Skill discovery and behavior in Claude, Codex, and VS Code and a real-project pilot have not been exercised. Run `python3 tools/validate-library.py` and `python3 tools/validate-bootstrap.py` after library maintenance.
