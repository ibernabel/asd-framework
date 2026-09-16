# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and adheres to [Semantic Versioning](https://semver.org/).

## [0.4.0] - 2026-09-16

### Added
- **YAGNI Standard**: Explicitly integrated YAGNI (You Aren't Gonna Need It) alongside SOLID and KISS across all templates, guidelines, and conventions.
- **Mandatory Frontend & UI Directives**: Enforced mandatory adherence to `/frontend-design` and `/web-design-guidelines` whenever creating or modifying user interfaces.
- **Code Pipeline Lite**: Integrated lightweight 3-agent pipeline (`Planner` → `Implementer` → `Reviewer`) for medium/low complexity tasks, selectable alongside the full 7-agent Uncle Bob pipeline.
- **Financial Privacy & Anti-PII Protocol**: Added strict privacy safeguards forbidding PII reading/logging, requiring structure-first data inspection, and mandating `pii-verifier` as the final execution stage on projects cataloged as `'financial'` across all modes.
- **Reviewer & QA Security Audits**: Mandated security and secrets verification checklists in both `qa` and `reviewer` agents.
- **User Profile Skeleton**: Added `USER.example.md` to provide a template for user background, preferences, and architectural philosophy.

### Changed
- **Skills Distribution (Physical Copies)**: Updated `install_project_skills.py` and `/project-init` to install project skills as physical file copies instead of symlinks, ensuring seamless recognition across IDEs and AI tools.
- **Project Init**: Updated `/project-init` to deploy 10 pipeline agents (`specifier`, `coder`, `refactorer`, `architect`, `qa`, `planner`, `implementer`, `reviewer`, `orchestrator`, `pii-verifier`) and auto-detect `'financial'` project tagging.

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

