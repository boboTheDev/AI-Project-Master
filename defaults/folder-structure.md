# Folder Structure Defaults

A managed project is a project root with two sibling directories, each its own git repository:

```text
PROJECT_ROOT/
├── AGENTS.md         # local runtime adapter, outside both repositories
├── CLAUDE.md         # local runtime adapter, outside both repositories
├── .project-meta/    # private: context, approved and draft intent, decisions, changes, review evidence, prototype
│   ├── project/       # everything formerly under .project/
│   └── prototype/      # disposable frontend candidate, own lightweight tooling
└── workspace/         # the real implementation, shareable with collaborators, no Project Master trace
```

There is no pointer file inside `workspace/` and no symlink between the two repositories. A skill locates the project root by finding the nearest ancestor that directly contains both `.project-meta/` and `workspace/`. Root adapters direct supported runtimes to the private bootstrap without entering either repository. Open agents from `PROJECT_ROOT`; opening `workspace/` alone may hide its parent from runtime discovery or permissions. Create only the folders a domain actually uses.

Inside `.project-meta/project/`, use domain folders such as `business/`, `tech/`, `database/`, `ux/`, `design/`, and `ui/` when those domains have real artifacts. Put ADRs in the configured decision directory and consequential change records in the configured change directory. A single meaningful document is better than several empty files.

For an existing project, Mastermind uses the current repository directory as the managed-project root and transactionally moves all existing entries, including `.git`, under `workspace/`. Git history, remotes, branches, local configuration, tracked files, and uncommitted files stay with the repository; a handled setup failure restores the original layout. The `.project-meta/` / `workspace/` boundary is the invariant. Project Master does not impose a structure inside `workspace/`.
