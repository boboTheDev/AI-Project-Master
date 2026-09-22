# Folder Structure Defaults

Keep durable project intent in `.project/` and implementation in code directories. Create only folders the project uses.

```text
PROJECT/
├── .project/        # bootstrap, status, approved and draft intent, decisions
├── web/             # optional frontend
├── api/             # optional server
├── mobile/          # optional mobile app
└── ...              # project-specific code and tooling
```

Inside `.project/`, use domain folders such as `business/`, `tech/`, `database/`, `ux/`, `design/`, and `ui/` when those domains have real artifacts. Put ADRs in the configured decision directory and consequential change records in the configured change directory. A single meaningful document is better than several empty files.

For an existing project, respect its established implementation layout unless a change has a clear benefit. The `.project/` boundary is the invariant; `web/`, `api/`, and `mobile/` are examples.
