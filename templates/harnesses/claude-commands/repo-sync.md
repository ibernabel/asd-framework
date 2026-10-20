---
description: Bump SemVer, update CHANGELOG, commit, tag, and push
---

Follow the instructions in `.agents/skills/repo-sync/SKILL.md` (or `~/.agents/skills/repo-sync/SKILL.md`).
1. Determine release bump type (patch, minor, major).
2. Bump `VERSION` file using `python3 scripts/bump_version.py <type>`.
3. Update `CHANGELOG.md` following Keep a Changelog standards.
4. Stage changes, generate conventional commit, create git tag, and push to origin.
