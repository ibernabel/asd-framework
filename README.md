# ASD Framework

> Agent-Driven Structured Development for human-AI pair programming.

ASD gives AI coding agents structured operating constraints across five domains: software engineering, business operations, content, video production, and autonomous AI agents.

AI agents often swing between two extremes. Without guardrails, they hallucinate dependencies, skip tests, write bloated controllers, and push unverified changes straight to `main`. But excessive process is just as bad: nobody wants to write an exhaustive PRD for a two-line CSS fix. 

ASD replaces arbitrary agent behavior with domain-specific execution modes and automated quality gates.

---

## Execution scopes

| Domain | Mode | Execution style | Quality gates |
|--------|------|-----------------|---------------|
| Software | Planning Mode (Strict) | Full Uncle Bob Pipeline or Code Pipeline Lite; Gherkin TDD | UI craft check, backend integrity check, security audit, PII scan |
| AI Agents | Planning Mode (Strict) | Prompt versioning, evaluation datasets, guardrails | Behavioral regression suite |
| Business Admin | Admin Mode | Scoped checklists, delivery summaries | Financial double-check, zero customer data in git |
| Content & Brand | Fast Mode | Direct execution, platform formatting | Brand voice guidelines, humanizer review |
| Video Production | Fast Mode | Scripts, shot lists, metadata | Template verification, direct delivery |

---

## What ASD does

- **Dual development pipelines**: For complex features, `/code-pipeline` runs an orchestrated pipeline with dedicated roles (Specifier, Coder, Refactorer, Architect, QA, and PII Verifier). For smaller, self-contained tasks, `/code-pipeline-lite` provides a faster 3-stage flow (Planner, Implementer, Reviewer).
- **Universal multi-harness compatibility**: ASD is completely harness-agnostic. While `.agents/` remains the canonical single source of truth, the framework generates and synchronizes native bridge files for Claude Code (`CLAUDE.md` and `.claude/commands/`), OpenAI Codex & the open AGENTS.md standard (`AGENTS.md` at root), Cursor (`.cursorrules` and modern `.cursor/rules/*.mdc`), Windsurf (`.windsurfrules`), and GitHub Copilot (`.github/copilot-instructions.md`).
- **Automated UI craft gate (`impeccable`)**: Before writing interface code, agents review the Craft Floor guidelines (design tokens, typography hierarchy, responsive breakpoints, avoiding AI-slop patterns like gradient text and repetitive icon cards). After coding, `impeccable detect` scans the UI. Any primary defect blocks QA approval.
- **Automated backend integrity gate (`backend-integrity`)**: Enforces clean architecture boundaries, schema-first input validation (Zod, Pydantic, DTOs), explicit database transactions on multi-table writes, bounded network timeouts ($\le 10\text{s}$), and no unpaginated collection queries. Verified through `verify_backend_integrity.py`.
- **Privacy-first financial protocol**: Projects marked with `pii: financial` in `CONVENTIONS.md` automatically run the `pii-verifier` agent as the final check across all execution modes. Agents inspect database and spreadsheet structures first, omitting personal data columns from data analysis.
- **Built-in security audits**: Both QA and Reviewer agents check for hardcoded secrets, verify `.env` handling, and check input sanitization before approving any pull request.
- **Branch protection**: Agents refuse to work on `main` or `develop`. All work happens on dedicated branches (`feature/[domain]-[description]`).
- **Gherkin acceptance criteria**: Pass rate on acceptance scenarios determines when a feature is done, rather than arbitrary line coverage percentages.
- **Physical skill distribution**: Skills are installed as physical copies in `.agents/skills/` instead of symlinks, ensuring Antigravity, Claude Code, Cursor, and Windsurf read them without path resolution issues.
- **WSL Ubuntu environment support**: On Windows systems, development and test commands execute inside WSL Ubuntu 22.04 through standard wrappers rather than raw PowerShell.
- **Ecosystem synchronization**: The `sync_agents_ecosystem.py` script keeps framework templates, global skills, and active project directories in sync.

---

## Quick start

### 1. Install the framework

To install all domains globally in `~/.agents/`:

```bash
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash
```

Or install specific domains:

```bash
# Software development only
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software

# Software + Business Admin
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software --domain admin

# All domains
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain all
```

The installer:
1. Creates the `~/.agents/` directory structure.
2. Copies selected domain templates and Universal AI Harness templates (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `cursor-rule.mdc`, `.windsurfrules`, `copilot-instructions.md`, and Claude Code slash commands) to `~/.agents/templates/`.
3. Installs core meta-skills (`project-init`, `code-pipeline`, `code-pipeline-lite`, `repo-sync`, `post-session-doc`, `docs-and-sync`, `backend-integrity`) to `~/.agents/skills/`.
4. Deploys the 10 pipeline agents to `~/.agents/agents/` for the software domain.
5. Deploys automation and sync scripts (`harness_adapter.py`, `install_project_skills.py`, `sync_agents_ecosystem.py`, `bump_version.py`) to `~/.agents/scripts/`.

### 2. Initialize or retrofit a project

Open your AI coding environment (Antigravity, Claude Code, Cursor, or Windsurf) in your project directory and run:

```bash
/project-init
```

The initialization skill detects your project state automatically:
- **Init Mode**: Empty directory. Sets up Git, private GitHub repository, `.gitignore`, canonical `docs/` hierarchy, `AGENTS.md`, `CONVENTIONS.md`, deterministic skills, and pipeline agents.
- **Retrofit Mode**: Existing repository without ASD. Injects the ASD structure and skills without altering your existing codebase.
- **Update Mode**: Existing ASD project. Updates skills, agent personas, and documentation standards while preserving your custom project rules and conventions.

---

## How the software pipelines work

ASD provides two execution pipelines depending on task scope:

### 1. Full Uncle Bob Pipeline (`/code-pipeline`)

Recommended for core domain logic, architectural additions, and complex features:

```
/code-pipeline
      │
      ├─► 1. Specifier      → Writes Gherkin .feature files + QA test procedures
      ├─► 2. Coder          → TDD: writes failing tests first, then implementation
      │                       Enforces UI Craft Floor & Backend Floor during coding
      ├─► 3. Refactorer     → Reduces complexity (CRAP ≤ 6), removes duplication
      ├─► 4. Architect      → Mutation testing, coverage review, boundary checks
      └─► 5. QA             → Executes QA test plan
                │             • Security & secrets check
                │             • UI craft certification (impeccable detect)
                │             • Backend integrity certification (verify_backend_integrity.py)
                │
                └─► 6. [If pii: financial]
                    PII Verifier → Scans diffs and datasets for customer data leaks
```

### 2. Code Pipeline Lite (`/code-pipeline-lite`)

Recommended for isolated endpoints, components, and minor features:

```
/code-pipeline-lite
      │
      ├─► 1. Planner        → Extracts clear acceptance criteria and edge cases
      │                       (Pauses for user sign-off before code is written)
      ├─► 2. Implementer    → Writes tests + implementation against approved criteria
      │                       Applies UI Craft Floor & Backend Floor
      └─► 3. Reviewer       → Code cleanup, test run, security audit
                │             • Security & secrets check
                │             • UI craft certification
                │             • Backend integrity certification
                │
                └─► 4. [If pii: financial]
                    PII Verifier → Scans for customer data before merge
```

### 3. Change classification

| Change type | When to use | Workflow |
|-------------|-------------|----------|
| Complex feature | Core business logic, major models, architecture changes | `/code-pipeline` |
| Lite feature | Isolated endpoints, UI components, small utilities | `/code-pipeline-lite` |
| Bug fix | Defect repairs, regression fixes | Branch + direct fix + QA check |
| Tweak / Docs / Chore | Copy adjustments, CSS tweaks, documentation, dependencies | Branch + direct fix + QA check |

Every path requires an active git branch, passes a security check, runs the PII verifier if financial, and produces a conventional commit before opening a pull request.

---

## The 10 pipeline agents

Located in `.agents/agents/`:

| Agent | Scope | Responsibility |
|-------|-------|----------------|
| `orchestrator` | Pipeline | Coordinates sequential execution of multi-agent workflows. |
| `specifier` | Full Pipeline | Writes Gherkin acceptance criteria, edge cases, and QA test plans. |
| `coder` | Full Pipeline | Writes failing tests first, then writes minimal code to pass them. |
| `refactorer` | Full Pipeline | Cleans code smells, removes duplicate logic, and keeps CRAP scores $\le 6$. |
| `architect` | Full Pipeline | Runs mutation tests, reviews architecture boundaries, and checks test coverage. |
| `qa` | Full Pipeline | Executes QA procedures, audits security, and validates certification gates. |
| `planner` | Lite Pipeline | Converts loose requirements into concise, reviewable acceptance criteria. |
| `implementer` | Lite Pipeline | Implements approved acceptance criteria with accompanying unit tests. |
| `reviewer` | Lite Pipeline | Reviews code quality, checks security, and enforces certification gates. |
| `pii-verifier` | Full / Lite / Direct | Scans code, fixtures, and queries for customer data and credentials. |

---

## Automated quality gates

ASD uses deterministic, scriptable checks to catch common agent mistakes:

### UI craft gate (`impeccable`)
- **Design rules**: Agents follow `/frontend-design` and the Craft Floor reference. The rules ban common AI interface habits: gradient text, unnecessary card grids, decorative section badges, and raw hex codes in markup.
- **Verification**: Run `impeccable detect <files>`.
- **Standards**: WCAG AA contrast ratio ($\ge 4.5:1$ body / $\ge 3:1$ large), minimum $44\times 44\text{px}$ touch targets, responsive layouts tested at 390px and desktop sizes, visible focus rings, and proper empty, loading, and error states.
- **Enforcement**: Any primary finding stops QA or Reviewer approval until fixed.

### Backend integrity gate (`backend-integrity`)
- **Design rules**: Agents follow `/backend-integrity` and the Backend Floor reference.
- **Core checks**:
  1. Input validation: Request bodies and parameters must match typed schemas before reaching domain logic (Zod, Pydantic, DTOs).
  2. Transactions: Operations mutating two or more tables must run inside a transaction (`db.transaction()`).
  3. Timeouts: All external network calls must set explicit timeouts ($\le 10\text{s}$).
  4. Query limits: No unbounded collection queries; pagination is required.
  5. Layer isolation: Controllers handle HTTP transport only; business logic stays in domain services.
  6. Structured errors: No silent exception suppression (`except: pass`); errors map to explicit HTTP status codes.
- **Verification**: Run `verify_backend_integrity.py <files>`.
- **Enforcement**: Exit code 2 blocks QA or Reviewer approval until resolved.

### Privacy and PII gate
- When `pii: financial` is set in `CONVENTIONS.md`, the `pii-verifier` agent runs before completing any task.
- Agents inspect database schemas and file headers before running queries, excluding customer identity columns from data exploration.

---

## Core commands and meta-skills

Centralized in `~/.agents/skills/` and available across projects:

| Command / Skill | Scope | Description |
|-----------------|-------|-------------|
| `/project-init` | Global | Initialize, retrofit, or update project structure, ASD docs, and skills |
| `/code-pipeline` | Project | Run full Uncle Bob pipeline (Specifier → Coder → Refactorer → Architect → QA) |
| `/code-pipeline-lite` | Project | Run lightweight pipeline (Planner → Implementer → Reviewer) |
| `/backend-integrity` | Project / Global | Audit backend code against architecture and integrity rules |
| `/humanizer` | Project / Global | Remove AI-generated writing patterns and improve natural voice |
| `/repo-sync` | Project | Bump SemVer, update CHANGELOG, commit, tag, and push |
| `/post-session-doc` | Project | Save session notes and deliverables into canonical `docs/` |
| `/docs-and-sync` | Project | Run `/post-session-doc` followed by `/repo-sync` |
| `/domain-modeling` | Project | Build ubiquitous language, bounded contexts, and ADR drafts |
| `/grilling` | Project | Interactive interview to pressure-test architecture plans before coding |
| `/ask-the-council` | Project | Multi-perspective evaluation using five advisor roles and a coordinator |
| `/wizard-of-oz-mode` | Project | Simulate end-to-end automation with a manual facade for quick testing |

---

## Project structure

Running `/project-init` on a software project sets up this structure:

```
my-project/
├── .agents/                        ← Canonical ASD SSOT
│   ├── AGENTS.md                   ← Detailed agent rules & Auto-invoke Skills table
│   ├── CONVENTIONS.md              ← Project stack, git rules, pipeline settings, PII flag
│   ├── agents/                     ← 10 pipeline agent definitions
│   │   ├── orchestrator/
│   │   ├── specifier/
│   │   ├── coder/
│   │   ├── refactorer/
│   │   ├── architect/
│   │   ├── qa/
│   │   ├── planner/
│   │   ├── implementer/
│   │   ├── reviewer/
│   │   └── pii-verifier/
│   └── skills/                     ← Physical copies of project skills
│       ├── code-pipeline/
│       ├── code-pipeline-lite/
│       ├── backend-integrity/
│       ├── humanizer/
│       ├── repo-sync/
│       ├── post-session-doc/
│       └── docs-and-sync/
├── AGENTS.md                       ← Root manifest (Open Standard / Codex / ChatGPT)
├── CLAUDE.md                       ← Anthropic Claude Code entry point
├── .claude/
│   └── commands/                   ← Native Claude Code custom slash commands
│       ├── code-pipeline.md
│       ├── code-pipeline-lite.md
│       ├── project-init.md
│       ├── repo-sync.md
│       ├── docs-and-sync.md
│       ├── post-session-doc.md
│       ├── backend-integrity.md
│       └── humanizer.md
├── .cursorrules                    ← Universal Cursor configuration
├── .cursor/
│   └── rules/
│       └── asd-framework.mdc       ← Modern Cursor Rules 2.0 (alwaysApply: true)
├── .windsurfrules                  ← Codeium Windsurf Cascade rules
├── .github/
│   └── copilot-instructions.md     ← GitHub Copilot Workspace & Chat rules
├── docs/                           ← Canonical documentation (SSOT)
│   ├── README.md                   ← Documentation index
│   ├── planning/                   ← PRD, user stories, domain ubiquitous language
│   ├── implementation/             ← Phase records and feature technical specs
│   ├── testing/                    ← QA test plans, test reports, Gherkin specs
│   ├── decisions/                  ← Architecture Decision Records (ADRs)
│   ├── fixes/                      ← Bug fix records
│   └── knowledges/                 ← Learned project patterns and known issues
├── tests/
│   ├── test_harness_adapter.py     ← Harness adapter test suite
│   └── features/                   ← Gherkin .feature files
├── scripts/
│   ├── harness_adapter.py          ← Universal AI harness adapter & validator
│   ├── install_project_skills.py   ← Skill installer & harness synchronizer
│   ├── sync_agents_ecosystem.py    ← Global ecosystem synchronizer
│   └── bump_version.py             ← SemVer versioning script
├── VERSION                         ← Current version (e.g. 0.6.0)
├── ROADMAP.md                      ← Milestones and bounded contexts
└── README.md
```

---

## Skill ecosystem and registries

ASD supports discovery, installation, and management through registries documented in [SKILL_REGISTRIES.md](SKILL_REGISTRIES.md):

- **[Skills Marketplace (SkillsMP)](https://skillsmp.com)**: Searchable catalog of agent skills accessible via REST API (`SKILLSMP_API_KEY`).
- **[Paul Bakaus Impeccable](https://github.com/pbakaus/impeccable)**: Design craft floor, WCAG accessibility standards, and automated UI defect scanner (`impeccable detect`).
- **[Antigravity Skills](https://github.com/rmyndharis/antigravity-skills)**: Backend, distributed systems, and DevOps skills.
- **[Skills.md](https://skills.md)**: Agent tools for repository automation and content workflows.
- **[Matt Pocock's Skills](https://github.com/mattpocock/skills)**: Skills for `grilling`, `domain-modeling`, `to-spec`, `refactor`, and `prototype`.
- **[Anthropic Official Skills](https://github.com/anthropics/skills)**: Frontend craft and ergonomic design patterns (`frontend-design`).
- **[Cathy Kim SemVer](https://github.com/cathy-kim/skill-semver)**: SemVer standards and release automation.

Use `scripts/skill_registry.py` to search and install skills from connected registries:

```bash
# Search for skills across registries
python3 scripts/skill_registry.py search "fastapi"

# Install a skill into the ecosystem
python3 scripts/skill_registry.py install "fastapi"
```

---

## Universal AI harness compatibility

ASD is harness-agnostic. While canonical rules and 10 pipeline agents live in `.agents/`, the framework automatically generates and synchronizes native bridge configurations across all major AI coding platforms:

| AI Harness / Environment | Status | Integration Mechanism | Key Capabilities |
|---|:---:|---|---|
| **Google Antigravity** | Supported (Primary) | Native `.agents/` structure & subagents | Full Uncle Bob pipeline, skills, and slash commands |
| **Claude Code** (`claude` CLI) | Supported | `CLAUDE.md` + `.claude/commands/` | Project memory & native custom slash commands (`/code-pipeline`, `/repo-sync`, etc.) |
| **OpenAI Codex & Open Standard** | Supported | Root manifest `AGENTS.md` | Conforms to the open AGENTS.md standard (ChatGPT, Codex, Aider) |
| **Cursor** | Supported | `.cursorrules` & `.cursor/rules/asd-framework.mdc` | Dual-mode: legacy rules and modern Cursor Rules 2.0 (`alwaysApply: true`) |
| **Windsurf** (Codeium) | Supported | `.windsurfrules` | Cascade workflow rules, branch policy, and planning gates |
| **GitHub Copilot** | Supported | `.github/copilot-instructions.md` | Copilot Chat and Workspace quality gate enforcement |
| **WSL Ubuntu 22.04** | Native | Commands run in WSL through PowerShell wrappers | Full cross-platform shell compatibility |

### Validate harness readiness

Run the harness auditor in any project directory to verify compatibility across all AI tools:

```bash
# Validate compatibility across all supported harnesses
python3 scripts/harness_adapter.py --validate --project-dir .

# Install or sync missing harness bridges without overwriting custom rules
python3 scripts/harness_adapter.py --project-dir .
```

---

## License

MIT License © [Idequel Bernabel](https://github.com/ibernabel).

Community skills from [Matt Pocock](https://github.com/mattpocock/skills) and other contributors are subject to their respective licenses.
