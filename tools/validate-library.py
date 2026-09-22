#!/usr/bin/env python3
"""Static, dependency-free validation for the Project Master library."""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "mastermind",
    "business-architect",
    "technical-architect",
    "data-architect",
    "ux-architect",
    "design-system",
    "ui-prototyper",
    "ui-reviewer",
    "decision-manager",
    "enforcer",
}
REQUIRED_SECTIONS = [
    "PURPOSE",
    "WHEN TO USE",
    "INPUTS",
    "REQUIRED ARTIFACTS",
    "OPTIONAL ARTIFACTS",
    "ALLOWED READS",
    "ALLOWED WRITES",
    "DEPENDENCIES",
    "PROCESS",
    "OUTPUTS",
    "APPROVAL REQUIREMENTS",
    "ESCALATION RULES",
    "FORBIDDEN ACTIONS",
    "COMPLETION CRITERIA",
]
ARTIFACT_STATUSES = {"draft", "needs-review", "approved", "superseded"}
IMPLEMENTATION_STATES = {"not-started", "in-progress", "implemented", "verified", "blocked"}


def fail(message: str) -> None:
    raise AssertionError(message)


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        fail(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if field:
            result[field.group(1)] = (field.group(2) or "").strip()
    return result


def validate_skills() -> None:
    skill_files = sorted(ROOT.glob("*/SKILL.md"))
    names = {path.parent.name for path in skill_files}
    if names != EXPECTED_SKILLS:
        fail(f"skill set differs: expected {sorted(EXPECTED_SKILLS)}, found {sorted(names)}")
    for path in skill_files:
        metadata = frontmatter(path)
        if metadata.get("name") != path.parent.name:
            fail(f"skill name mismatch: {path.relative_to(ROOT)}")
        if not metadata.get("description"):
            fail(f"missing skill description: {path.relative_to(ROOT)}")
        sections = re.findall(r"^## ([A-Z ]+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
        if sections != REQUIRED_SECTIONS:
            fail(f"section contract mismatch: {path.relative_to(ROOT)}")


def validate_artifact_templates() -> None:
    artifact_dir = ROOT / "templates" / "artifacts"
    lifecycle_templates = {
        "business-requirements.md",
        "change-chg.md",
        "context-vision.md",
        "database-schema.md",
        "decision-adr.md",
        "design-system.md",
        "technical-architecture.md",
        "ux-user-journeys.md",
    }
    evidence_templates = {"enforcer-review.md", "ui-prototype-notes.md", "ui-review.md"}
    actual = {path.name for path in artifact_dir.glob("*.md")}
    expected = lifecycle_templates | evidence_templates
    if actual != expected:
        fail(f"artifact template set differs: expected {sorted(expected)}, found {sorted(actual)}")
    for name in lifecycle_templates:
        metadata = frontmatter(artifact_dir / name)
        missing = {"status", "owner", "revision"} - metadata.keys()
        if missing:
            fail(f"missing {sorted(missing)} in templates/artifacts/{name}")
        if metadata["status"] not in ARTIFACT_STATUSES:
            fail(f"invalid artifact status in templates/artifacts/{name}")
    for name in evidence_templates:
        if (artifact_dir / name).read_text(encoding="utf-8").startswith("---\n"):
            fail(f"evidence template must not imply approval lifecycle: templates/artifacts/{name}")

    change = frontmatter(artifact_dir / "change-chg.md")
    if change.get("implementation_state") not in IMPLEMENTATION_STATES:
        fail("change template has invalid implementation_state")


def validate_schemas() -> None:
    schemas: dict[str, dict] = {}
    for path in sorted((ROOT / "schemas").glob("*.json")):
        schemas[path.name] = json.loads(path.read_text(encoding="utf-8"))
    change_schema = schemas["change-metadata.schema.json"]["allOf"][1]
    required = set(change_schema["required"])
    if "implementation_state" not in required:
        fail("change schema does not require implementation_state")
    enum = set(change_schema["properties"]["implementation_state"]["enum"])
    if enum != IMPLEMENTATION_STATES:
        fail("change schema implementation states differ from library contract")


def validate_bootstrap() -> None:
    required = [
        ROOT / "templates/project/.project/README.md",
        ROOT / "templates/project/.project/project.yaml",
        ROOT / "templates/project/.project/STATUS.md",
        ROOT / "templates/project/AGENTS.md",
        ROOT / "templates/project/CLAUDE.md",
        ROOT / "templates/project/.github/copilot-instructions.md",
    ]
    for path in required:
        if not path.is_file():
            fail(f"missing bootstrap file: {path.relative_to(ROOT)}")
    manifest = (ROOT / "templates/project/.project/project.yaml").read_text(encoding="utf-8")
    for key in json.loads((ROOT / "schemas/project-manifest.schema.json").read_text())["required"]:
        if not re.search(rf"^{re.escape(key)}:", manifest, re.MULTILINE):
            fail(f"manifest template missing required key: {key}")
    helper = ROOT / "mastermind/scripts/bootstrap_project.py"
    if not helper.is_file():
        fail("missing Mastermind bootstrap helper")
    ast.parse(helper.read_text(encoding="utf-8"), filename=str(helper))


def validate_local_links() -> None:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    markdown_files = sorted(ROOT.rglob("*.md")) + [ROOT.parent / "IDEA.md"]
    for path in markdown_files:
        for target in pattern.findall(path.read_text(encoding="utf-8")):
            target = target.strip().strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            local = target.split("#", 1)[0]
            if not (path.parent / local).resolve().exists():
                fail(f"broken local link in {path.relative_to(ROOT)}: {target}")


def validate_adapter() -> None:
    script = ROOT / "adapters/install-local.sh"
    result = subprocess.run(["sh", "-n", str(script)], capture_output=True, text=True, check=False)
    if result.returncode:
        fail(f"adapter shell syntax failed: {result.stderr.strip()}")


def main() -> int:
    checks = [
        ("skills", validate_skills),
        ("artifact templates", validate_artifact_templates),
        ("schemas", validate_schemas),
        ("project bootstrap", validate_bootstrap),
        ("local Markdown links", validate_local_links),
        ("adapter syntax", validate_adapter),
    ]
    for label, check in checks:
        check()
        print(f"ok: {label}")
    print("Project Master static integration validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
