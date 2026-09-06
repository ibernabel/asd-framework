# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and adheres to [Semantic Versioning](https://semver.org/).

## [0.3.0] - 2026-09-06

### Changed
- **Workflows to Skills Migration**: Deprecated legacy `.agents/workflows/` and migrated all core commands (`project-init`, `code-pipeline`, `docs-and-sync`, `repo-sync`, `post-session-doc`, `domain-modeling`, `grilling`, etc.) to modern first-class skills in `.agents/skills/`.
- **Project Init**: Updated `/project-init` meta-skill to install skills via deterministic presets instead of legacy workflows.
- **Installer & Tooling**: Updated `install.sh` and `install_project_skills.py` to link skills into `.agents/skills/` and clean up legacy workflow references.
- **Agent Templates**: Updated all domain agent templates (`software`, `admin`, `ai-agent`, `content`, `video`) to reference `Global Skills & Meta-Commands`.
- **Skill Presets**: Added `code-pipeline` and `docs-and-sync` to default and essential skill presets.

## [0.2.1] - 2026-08-17

### Fixed
- feat: add WSL terminal execution standard to agents, templates and project-init

## [0.2.0] - 2026-08-15

### Added
- feat: add global workflows resolution in templates and wizard-of-oz workflow

