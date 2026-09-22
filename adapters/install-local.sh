#!/bin/sh
set -eu

dry_run=0
if [ "${1:-}" = "--dry-run" ]; then
  dry_run=1
  shift
fi
if [ "$#" -ne 0 ]; then
  echo "usage: sh adapters/install-local.sh [--dry-run]" >&2
  exit 2
fi

library_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
conflicts=0
count=0

for skill_file in "$library_root"/*/SKILL.md; do
  [ -f "$skill_file" ] || continue
  skill_dir=${skill_file%/SKILL.md}
  skill_name=${skill_dir##*/}
  for target_dir in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
    target="$target_dir/$skill_name"
    if [ -L "$target" ] && [ "$(readlink "$target")" = "$skill_dir" ]; then
      echo "already linked: $target"
    elif [ -e "$target" ] || [ -L "$target" ]; then
      echo "collision, left unchanged: $target" >&2
      conflicts=$((conflicts + 1))
    elif [ "$dry_run" -eq 1 ]; then
      echo "would link: $target -> $skill_dir"
    else
      mkdir -p "$target_dir"
      ln -s "$skill_dir" "$target"
      echo "linked: $target -> $skill_dir"
    fi
    count=$((count + 1))
  done
done

if [ "$count" -eq 0 ]; then
  echo "no skills found under $library_root" >&2
  exit 1
fi
if [ "$conflicts" -ne 0 ]; then
  echo "$conflicts existing target(s) need manual review" >&2
  exit 1
fi
