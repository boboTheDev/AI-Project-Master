# Folder Structure Defaults

A managed project is a project root with two sibling directories, each its own git repository:

```text
PROJECT_ROOT/
├── .project-meta/    # private: context, approved and draft intent, decisions, changes, review evidence, prototype
│   ├── project/       # everything formerly under .project/
│   └── prototype/      # disposable frontend candidate, own lightweight tooling
└── workspace/         # the real implementation, shareable with collaborators, no Project Master trace
```

There is no pointer file inside `workspace/` and no symlink between the two directories. A skill locates the project root by finding the nearest ancestor — from the current directory, or by walking upward — that directly contains both `.project-meta/` and `workspace/`. This is pure relative-path convention, so it holds identically across devices and operating systems. Create only the folders a domain actually uses.

Inside `.project-meta/project/`, use domain folders such as `business/`, `tech/`, `database/`, `ux/`, `design/`, and `ui/` when those domains have real artifacts. Put ADRs in the configured decision directory and consequential change records in the configured change directory. A single meaningful document is better than several empty files.

For an existing project, Mastermind uses the current repository directory as the managed-project root and moves all of its existing entries, including `.git`, together under `workspace/`. This changes only the outer folder structure: Git history, remotes, branches, tracked files, and uncommitted files stay with the repository. The `.project-meta/` / `workspace/` boundary is the invariant; what `workspace/` contains internally (`src/`, `api/`, `mobile/`, or any other layout) is the project's own and Project Master does not impose a structure on it.
