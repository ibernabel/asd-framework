# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and adheres to [Semantic Versioning](https://semver.org/).

## [0.6.2] - 2026-10-23

### Fixed
- Normalize ASD Framework branding across harnesses, scripts, and skills

## [0.6.1] - 2026-10-19

### Added
- **Architecture Distinction**: Explicitly delineated the ASD Framework (rules, harness adapters, agent pipeline) from the ASD Methodology (domain-adaptive roles, execution scopes, SSOT).
- **Persona Onboarding Guides**: Added targeted workflows and quick-start entry points for Solopreneurs, Engineering Teams, and AI Engineers.
- **Production Walkthrough**: Added end-to-end scenario demonstrating real-world project lifecycle from idea to deployment.
- **Spanish Edition (README.es.md)**: Full Spanish documentation covering all framework concepts, harnesses, and architectural models.

### Changed
- **Humanizer Refinements**: Polished README.md and README.es.md to remove AI writing mannerisms, buzzwords, and repetitive framing in favor of direct, engineering-grade clarity.

## [0.6.0] - 2026-10-19

### Added
- **Universal Multi-Harness Architecture**: Added native, out-of-the-box bridge support for all major AI coding platforms: Claude Code, OpenAI Codex, Cursor, Windsurf, and GitHub Copilot.
- **Root Manifest (`AGENTS.md`)**: Implemented standardized root manifest conforming to the open AGENTS.md specification (OpenAI Codex, ChatGPT, Aider) linking to `.agents/`.
- **Claude Code Integration (`CLAUDE.md` & `.claude/commands/`)**: Added root memory file and native custom slash command prompt wrappers (`/code-pipeline`, `/code-pipeline-lite`, `/project-init`, `/repo-sync`, `/post-session-doc`, `/docs-and-sync`, `/backend-integrity`, `/humanizer`).
- **Cursor Dual Support**: Added universal `.cursorrules` and Cursor Rules 2.0 `.cursor/rules/asd-framework.mdc` with `alwaysApply: true`.
- **Windsurf & Copilot Bridges**: Added `.windsurfrules` for Windsurf Cascade and `.github/copilot-instructions.md` for GitHub Copilot Workspace and Chat.
- **Harness Adapter CLI (`scripts/harness_adapter.py`)**: Added automated generator and validation auditor (`--validate`) to inspect and install harness adapters non-destructively.
- **Test Suite**: Added unit and integration tests (`tests/test_harness_adapter.py`) covering harness generation, validation, non-destructive updates, and skill installer integration.

### Changed
- **Project Initialization (`/project-init`)**: Added Step 6D to automatically deploy multi-harness bridges and added multi-harness audit checks to post-execution verification.
- **Skill Installer (`install_project_skills.py`)**: Automatically deploys and synchronizes harness bridges when installing skills.
- **Installer Script (`install.sh`)**: Updated to fetch harness templates and scripts into `~/.agents/`.
- **Ecosystem Synchronizer (`sync_agents_ecosystem.py`)**: Added `--push-to-global` flag and synchronized harness templates across the environment.

## [0.5.1] - 2026-10-19

### Changed
- **Documentation**: Updated `README.md` to reflect all v0.5.0 features and integrations (10 pipeline agents, dual pipelines, UI/UX craft and backend integrity certification gates, financial PII protocol, ecosystem sync, and skill registries).
- **Humanizer**: Applied `humanizer` standards to eliminate AI-generated writing patterns, emoji noise, and inflated corporate language in favor of a clean, natural developer voice.

## [0.5.0] - 2026-10-14

### Added
- introduce UI/UX craft and backend integrity certification gates and tooling

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
