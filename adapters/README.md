# Agent Entry Points and Local Skill Links

The managed-project template contains three thin instruction files: `AGENTS.md` for Codex and other supporting agents, `CLAUDE.md` importing it for Claude Code, and `.github/copilot-instructions.md` for GitHub Copilot in VS Code. Each points to `.project/README.md`, the canonical project bootstrap. Copy these into a managed project carefully; merge with existing agent instructions rather than replacing them.

The skills themselves have one source in this `project-master/` directory. The optional [install-local.sh](install-local.sh) creates personal symlinks for the ten `SKILL.md` directories in `~/.agents/skills/` (Codex and GitHub Copilot) and `~/.claude/skills/` (Claude Code). It refuses to replace an existing file or foreign link. Review its dry-run output before using it on a device:

```sh
sh adapters/install-local.sh --dry-run
sh adapters/install-local.sh
```

Run these commands from the `project-master/` directory. They link skills only; they do not bootstrap a project or copy project knowledge into the global library. The user requested no runtime discovery test, so discovery and invocation have not been exercised in the target applications.

Current documentation for discovery paths: [Codex skills](https://developers.openai.com/codex/skills/), [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude Code `CLAUDE.md` imports](https://code.claude.com/docs/en/memory), and [GitHub Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills). Other VS Code agents may require a different entry file.
