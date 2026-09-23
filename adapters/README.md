# Runtime Adapters

Project Master uses two adapter layers.

## Personal skill links

The skills have one source in this `project-master/` directory. Optional [install-local.sh](install-local.sh) creates personal symlinks for the ten skill directories in `~/.agents/skills/` for Codex and GitHub Copilot, and `~/.claude/skills/` for Claude Code. It refuses to replace an existing file or foreign link. Review its dry run first:

```sh
sh adapters/install-local.sh --dry-run
sh adapters/install-local.sh
```

Run these commands from `project-master/`. They install reusable skills only; they do not bootstrap a project or copy project knowledge into the global library.

## Managed-project root adapters

Bootstrap generates `AGENTS.md` and `CLAUDE.md` at the managed project root. They sit outside both `.project-meta/` and `workspace/`, direct supported runtimes to the private project bootstrap, and keep the shared implementation repository free of Project Master files. The root also contains the two sibling directories, which provide runtime-independent structural discovery.

Open and run agents from the managed project root. Opening only `workspace/` can prevent a runtime from seeing its parent adapters or `.project-meta/`. Root adapters are local coordination files and are not part of either repository.

The user requested no application discovery test, so invocation in target applications remains unverified. Current discovery references: [Codex skills](https://developers.openai.com/codex/skills/), [Claude Code skills](https://code.claude.com/docs/en/skills), and [GitHub Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills).
