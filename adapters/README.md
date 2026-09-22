# Local Skill Links

A managed project carries no Project Master entry file: neither `workspace/` nor `.project-meta/` needs one, because every skill finds the project root by directory structure — the nearest ancestor containing both `.project-meta/` and `workspace/` as siblings — rather than by an in-repo pointer. This is what keeps `workspace/` shareable with collaborators without exposing any Project Master trace.

The skills themselves have one source in this `project-master/` directory. The optional [install-local.sh](install-local.sh) creates personal symlinks for the ten `SKILL.md` directories in `~/.agents/skills/` (Codex and GitHub Copilot) and `~/.claude/skills/` (Claude Code). It refuses to replace an existing file or foreign link. Review its dry-run output before using it on a device:

```sh
sh adapters/install-local.sh --dry-run
sh adapters/install-local.sh
```

Run these commands from the `project-master/` directory. They link skills only; they do not bootstrap a project or copy project knowledge into the global library. The user requested no runtime discovery test, so discovery and invocation have not been exercised in the target applications.

Current documentation for discovery paths: [Codex skills](https://developers.openai.com/codex/skills/), [Claude Code skills](https://code.claude.com/docs/en/skills), and [GitHub Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills). Other VS Code agents may require their own discovery configuration; none of them need a file inside a managed project.
