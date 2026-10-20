# ASD Framework

> **Agent-Driven Structured Development** — The open governance and engineering methodology for human-AI pair programming.

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.6.0-green.svg)](VERSION)
[![Harness Compatibility](https://img.shields.io/badge/harness-universal-purple.svg)](#universal-ai-harness-compatibility)

**[ English ]** · **[[Español](README.es.md)]**

</div>

---

ASD gives AI coding agents structured operating constraints across five domains: **software engineering**, **autonomous AI agents**, **business administration**, **content & brand**, and **video production**.

AI coding agents often swing between two extremes:
- **Without guardrails**, they hallucinate dependencies, skip tests, write bloated controllers, and push unverified changes straight to `main`.
- **With excessive bureaucracy**, they drown developers in 20-page requirement documents for two-line CSS fixes.

ASD replaces arbitrary prompt guesswork with **domain-specific execution pipelines**, **deterministic quality gates**, and **automated testing**.

---

## What is ASD?

ASD is **not** a runtime software library (like React, Laravel, or Django). Your application code never imports ASD, and it adds zero overhead to your production bundle.

Instead, ASD is a **methodological and governance framework** for agentic software engineering—the AI-era equivalent of what Extreme Programming (XP) and Agile were for human software teams:

- **Inversion of Control (IoC) for LLMs**: In an unconstrained chat, the AI decides arbitrarily how to proceed. Under ASD, the framework retains control over the lifecycle. It dictates which agent persona executes (`Specifier` → `Coder` → `Refactorer` → `Architect` → `QA`), which quality gates must pass, and what artifacts must be produced before moving forward. The agent executes within boundaries; the framework owns the workflow.
- **Agentic Governance & Quality Layer**: Acts as an automated gatekeeper preventing common AI anti-patterns: unvalidated inputs, bypassed unit tests, bloated controllers, direct pushes to `main`, and customer data or credential leaks.
- **Universal Harness Abstraction**: Rather than locking your project into a single AI tool, ASD maintains a single source of truth in `.agents/` and automatically synchronizes native harness bridges for Antigravity, Claude Code, Cursor, Windsurf, and GitHub Copilot.

---

## Who is ASD for?

### 🛠️ For Traditional Software Engineers (Hand-Coders)
> *"I want AI acceleration, but I refuse to let it generate sloppy, untested spaghetti code."*

If you care about Clean Architecture, SOLID principles, and test-driven development, ASD is built for you. The AI acts as a disciplined junior engineer under your direct architectural supervision:
- Enforces strict TDD: tests are written first, and implementation code only passes when tests turn green.
- Caps code complexity (CRAP score $\le 6$).
- Enforces backend database transactions, schema validation (Zod, Pydantic, DTOs), and bounded network timeouts.

### 🚀 For Developers Starting with AI
> *"I don't know how to write 50-line prompts or catch subtle AI hallucinations."*

You don't need complex prompt engineering gymnastics. ASD provides intuitive, battle-tested slash commands:
- Simply type `/code-pipeline-lite <your feature>` in your AI tool.
- The agent analyzes your requirements, extracts acceptance criteria, and **pauses to ask for your sign-off** before writing a single line of code.
- If the AI makes a mistake, the automated quality gates catch and reject it before it ever reaches git.

### 👥 For Engineering Teams & Tech Leads
> *"Every developer on my team uses a different AI tool, resulting in inconsistent code quality and conventions."*

ASD establishes a single, unified standard across your entire organization:
- **One Source of Truth (`.agents/`)**: Repository rules, coding conventions, and agent definitions are version-controlled in git.
- **Multi-Tool Interoperability**: Teammates can use Claude Code, Cursor, Windsurf, Copilot, or Antigravity simultaneously without configuration drift.
- **Audit-Ready Pull Requests**: Every change branch undergoes security checks, regression tests, and optional financial/PII compliance scanning before opening a PR.

---

## The 30-Second Mental Model

```
       Your Feature Idea
              │
              ▼
    [ Choose Pipeline ]
      │             │
      │ (Complex)   │ (Standard / Isolated)
      ▼             ▼
/code-pipeline  /code-pipeline-lite
      │             │
      ▼             ▼
 [ Plan & Acceptance Criteria ] ──► (Pauses for human approval)
      │
      ▼
 [ TDD Implementation ] ──────────► (Writes failing test, then minimal code)
      │
      ▼
 [ Automated Quality Gates ]
      ├─► UI Craft Gate (WCAG AA, no AI-slop patterns)
      ├─► Backend Integrity Gate (Schemas, transactions, timeouts)
      └─► PII & Security Gate (Secret audit, zero customer data in git)
      │
      ▼
 [ Safe Git Branch & Conventional Commit ]
```

---

## Step-by-Step Quickstart (0 to Working Feature in 3 Minutes)

### Step 1: Install ASD Globally

Install ASD into your global environment (`~/.agents/`):

```bash
# Install all domains globally
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash
```

*Want specific domains only?*
```bash
# Software engineering only
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software

# Software + Business Administration
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software --domain admin
```

### Step 2: Initialize or Retrofit Any Project

Navigate to your project root, open your AI coding environment (Claude Code, Cursor, Windsurf, or Antigravity), and trigger:

```bash
/project-init
```

ASD inspects your workspace and runs in one of three modes:
- **Init Mode** (empty directory): Scaffolds git, `.gitignore`, canonical `docs/` hierarchy, `AGENTS.md`, `CONVENTIONS.md`, and pipeline agents.
- **Retrofit Mode** (existing project): Injects ASD governance infrastructure **without modifying your existing code or git history**.
- **Update Mode** (existing ASD project): Upgrades agents, skills, and bridge files while preserving your custom project conventions.

### Step 3: Build Your First Feature (Walkthrough)

Here is what a typical workflow looks like in your AI chat:

1. **You trigger a task:**
   ```text
   /code-pipeline-lite Add avatar upload endpoint with 2MB image validation
   ```

2. **The Planner agent analyzes the task and requests sign-off:**
   ```text
   [Planner] Proposed Acceptance Criteria:
   1. POST /api/user/avatar accepts JPEG and PNG files only.
   2. Files exceeding 2MB return 413 Payload Too Large.
   3. File contents validated via magic bytes (not just file extension).
   4. Stored file keys linked to authenticated user ID.

   Do you approve these criteria before implementation begins?
   ```

3. **You approve:**
   ```text
   Approved, proceed.
   ```

4. **The Implementer agent executes TDD:**
   - Automatically checks out branch `feature/software-avatar-upload`.
   - Writes unit and integration tests covering valid uploads, oversized files, and invalid MIME types.
   - Writes the minimal endpoint logic to turn all tests green.

5. **The Reviewer agent certifies quality gates:**
   - Verifies input schema validation.
   - Verifies no hardcoded credentials or customer data.
   - Runs `verify_backend_integrity.py`.
   - Generates a conventional commit: `feat(api): add avatar upload endpoint with file size validation`.

### Step 4: Verify with Automated Quality Gates

You can run quality gates manually at any time:

```bash
# Audit backend architecture, schemas, and transactions
python3 scripts/verify_backend_integrity.py src/

# Audit UI code for accessibility and AI design flaws
impeccable detect src/components/
```

### Step 5: Safe Git & Release Sync

When your feature is complete and merged, update project documentation and release version with a single command:

```bash
# Updates session docs in docs/ and syncs GitHub (SemVer, CHANGELOG, tags)
/docs-and-sync
```

---

## Execution Scopes

ASD dynamically adapts its process depending on what you are building:

| Domain | Mode | Execution Style | Quality Gates |
|---|---|---|---|
| **Software** | Planning Mode (Strict) | Full Uncle Bob Pipeline or Code Pipeline Lite; Gherkin TDD | UI craft check, backend integrity check, security audit, PII scan |
| **AI Agents** | Planning Mode (Strict) | Prompt versioning, evaluation datasets, guardrails | Behavioral regression suite |
| **Business Admin** | Admin Mode | Scoped checklists, delivery summaries | Financial double-check, zero customer data in git |
| **Content & Brand** | Fast Mode | Direct execution, platform formatting | Brand voice guidelines, humanizer review |
| **Video Production** | Fast Mode | Scripts, shot lists, metadata | Template verification, direct delivery |

---

## Choosing Your Software Pipeline

ASD offers two complementary software development pipelines:

### 1. Code Pipeline Lite (`/code-pipeline-lite`)
**Best for**: Daily features, isolated endpoints, bug fixes, UI components, and utility functions ($\approx 80\%$ of daily tasks).

```
/code-pipeline-lite
      │
      ├─► 1. Planner        → Extracts criteria & edge cases (pauses for sign-off)
      ├─► 2. Implementer    → TDD: writes tests, then implementation
      └─► 3. Reviewer       → Audits code, runs quality gates, produces commit
                │
                └─► 4. [If pii: financial]
                    PII Verifier → Scans for customer data before merge
```

### 2. Full Uncle Bob Pipeline (`/code-pipeline`)
**Best for**: Core domain logic, complex microservices, multi-table database migrations, and mission-critical architectural additions.

```
/code-pipeline
      │
      ├─► 1. Specifier      → Writes Gherkin .feature specifications & QA test procedures
      ├─► 2. Coder          → TDD: writes failing tests first, then implementation
      ├─► 3. Refactorer     → Eliminates duplication, caps CRAP complexity $\le 6$
      ├─► 4. Architect      → Mutation testing, coverage review, boundary checks
      └─► 5. QA             → Executes QA test plan, validates UI/Backend quality gates
                │
                └─► 6. [If pii: financial]
                    PII Verifier → Deep scan for data leakage
```

### Change Classification Guide

| Change Type | Typical Use Case | Recommended Workflow |
|---|---|---|
| **Complex Feature** | Core domain logic, new architectural boundaries | `/code-pipeline` |
| **Standard Feature** | Isolated endpoints, UI components, background jobs | `/code-pipeline-lite` |
| **Bug Fix** | Defect repairs, regression fixes | Branch + targeted test + fix + QA check |
| **Refactoring / Chore** | Dependency updates, documentation, style polish | Branch + direct fix + automated check |

---

## The 10 Pipeline Agents

Located in `.agents/agents/` and activated dynamically by pipeline commands:

| Agent | Scope | Responsibility |
|---|---|---|
| `orchestrator` | Pipeline | Coordinates sequential execution of multi-agent workflows. |
| `planner` | Lite Pipeline | Converts loose requirements into concise, reviewable acceptance criteria. |
| `implementer` | Lite Pipeline | Implements approved acceptance criteria with accompanying unit tests. |
| `reviewer` | Lite Pipeline | Reviews code quality, checks security, and enforces certification gates. |
| `specifier` | Full Pipeline | Writes formal Gherkin acceptance criteria and QA test plans. |
| `coder` | Full Pipeline | Writes failing tests first, then writes minimal code to pass them. |
| `refactorer` | Full Pipeline | Cleans code smells, removes duplicate logic, and keeps CRAP scores $\le 6$. |
| `architect` | Full Pipeline | Runs mutation tests, reviews architecture boundaries, and checks test coverage. |
| `qa` | Full Pipeline | Executes QA procedures, audits security, and validates certification gates. |
| `pii-verifier` | Full / Lite / Direct | Scans code, fixtures, and queries for customer data and credentials. |

---

## Automated Quality Gates

ASD replaces manual code reviews with deterministic, scriptable checks:

### 1. UI Craft Gate (`impeccable`)
- **Design rules**: Agents follow `/frontend-design` and the Craft Floor guidelines. Eliminates generic AI interface habits: gradient text, unnecessary card grids, decorative badges, and raw hex codes in markup.
- **Verification**: `impeccable detect <files>`.
- **Standards**: WCAG AA contrast ratio ($\ge 4.5:1$ body / $\ge 3:1$ large), minimum $44\times 44\text{px}$ touch targets, responsive layouts tested at 390px and desktop sizes, visible focus rings, and proper empty, loading, and error states.
- **Enforcement**: Any primary defect halts pipeline approval until resolved.

### 2. Backend Integrity Gate (`backend-integrity`)
- **Design rules**: Agents follow `/backend-integrity` and the Backend Floor specification.
- **Core checks**:
  1. **Schema Validation**: Request bodies and parameters must match typed schemas before reaching domain logic (Zod, Pydantic, DTOs).
  2. **Atomic Transactions**: Operations mutating two or more database tables must run inside a transaction (`db.transaction()`).
  3. **Explicit Timeouts**: All external network calls must specify bounded timeouts ($\le 10\text{s}$).
  4. **Bounded Queries**: Unbounded collection queries are prohibited; pagination is mandatory.
  5. **Layer Isolation**: Controllers handle HTTP transport only; business logic stays in domain services.
  6. **Structured Errors**: Silent exception suppression (`except: pass`) is prohibited; errors map to explicit HTTP status codes.
- **Verification**: `python3 scripts/verify_backend_integrity.py <files>`.
- **Enforcement**: Exit code 2 blocks QA or Reviewer sign-off.

### 3. Privacy & PII Gate (`pii-verifier`)
- Activated automatically when `pii: financial` is declared in `CONVENTIONS.md`.
- Inspects database schemas and fixtures prior to execution, stripping customer identity and financial data from agent exploration queries.

---

## Core Commands and Meta-Skills

Centralized in `~/.agents/skills/` and available across all your repositories:

| Command / Skill | Scope | Description |
|---|---|---|
| `/project-init` | Global | Initialize, retrofit, or update project structure, ASD docs, and skills. |
| `/code-pipeline` | Project | Run full Uncle Bob pipeline (Specifier → Coder → Refactorer → Architect → QA). |
| `/code-pipeline-lite` | Project | Run lightweight 3-stage pipeline (Planner → Implementer → Reviewer). |
| `/backend-integrity` | Project / Global | Audit backend code against architecture, schema, and transaction rules. |
| `/humanizer` | Project / Global | Strip AI-generated writing patterns and restore natural human voice. |
| `/repo-sync` | Project | Bump SemVer, update CHANGELOG, commit, tag, and push safely. |
| `/post-session-doc` | Project | Save session notes and deliverables into canonical `docs/` hierarchy. |
| `/docs-and-sync` | Project | Run `/post-session-doc` followed by `/repo-sync` sequentially. |
| `/domain-modeling` | Project | Build ubiquitous language, bounded contexts, and ADR drafts. |
| `/grilling` | Project | Interactive interview to stress-test architectural decisions before coding. |
| `/ask-the-council` | Project | Multi-perspective evaluation using five advisor roles and a coordinator. |
| `/wizard-of-oz-mode` | Project | Simulate end-to-end automation with a manual facade for quick testing. |

---

## Project Structure (Canonical SSOT)

Running `/project-init` on a software repository establishes this canonical layout:

```
my-project/
├── .agents/                        ← Canonical ASD Single Source of Truth (SSOT)
│   ├── AGENTS.md                   ← Agent rules & Auto-invoke Skills table
│   ├── CONVENTIONS.md              ← Project stack, git rules, pipeline settings, PII flag
│   ├── agents/                     ← 10 pipeline agent definitions
│   │   ├── orchestrator/
│   │   ├── planner/
│   │   ├── implementer/
│   │   ├── reviewer/
│   │   ├── specifier/
│   │   ├── coder/
│   │   ├── refactorer/
│   │   ├── architect/
│   │   ├── qa/
│   │   └── pii-verifier/
│   └── skills/                     ← Physical copies of installed project skills
│       ├── code-pipeline/
│       ├── code-pipeline-lite/
│       ├── backend-integrity/
│       ├── humanizer/
│       ├── repo-sync/
│       ├── post-session-doc/
│       └── docs-and-sync/
├── AGENTS.md                       ← Root bridge (Open Standard / Codex / ChatGPT)
├── CLAUDE.md                       ← Anthropic Claude Code entry point
├── .claude/
│   └── commands/                   ← Native Claude Code slash commands
├── .cursorrules                    ← Legacy Cursor rules
├── .cursor/
│   └── rules/
│       └── asd-framework.mdc       ← Modern Cursor Rules 2.0 (alwaysApply: true)
├── .windsurfrules                  ← Codeium Windsurf Cascade rules
├── .github/
│   └── copilot-instructions.md     ← GitHub Copilot Workspace & Chat rules
├── docs/                           ← Canonical Documentation Repository
│   ├── README.md                   ← Documentation index
│   ├── planning/                   ← PRD, user stories, ubiquitous language
│   ├── implementation/             ← Phase records and feature specifications
│   ├── testing/                    ← QA test plans, test reports, Gherkin specs
│   ├── decisions/                  ← Architecture Decision Records (ADRs)
│   ├── fixes/                      ← Bug fix records
│   └── knowledges/                 ← Learned patterns and known issues
├── tests/                          ← Unit, integration, and acceptance tests
└── README.md
```

---

## Universal AI Harness Compatibility

ASD is harness-agnostic. While canonical rules and agents live in `.agents/`, the framework automatically generates and synchronizes native bridge configurations across all major AI coding platforms:

| AI Harness / Environment | Status | Integration Mechanism | Key Capabilities |
|---|:---:|---|---|
| **Google Antigravity** | Supported (Primary) | Native `.agents/` structure & subagents | Full Uncle Bob pipeline, skills, and slash commands |
| **Claude Code** (`claude` CLI) | Supported | `CLAUDE.md` + `.claude/commands/` | Project memory & native custom slash commands (`/code-pipeline`, `/repo-sync`, etc.) |
| **OpenAI Codex & Open Standard** | Supported | Root manifest `AGENTS.md` | Conforms to open AGENTS.md standard (ChatGPT, Codex, Aider) |
| **Cursor** | Supported | `.cursorrules` & `.cursor/rules/asd-framework.mdc` | Dual-mode: legacy rules and modern Cursor Rules 2.0 (`alwaysApply: true`) |
| **Windsurf** (Codeium) | Supported | `.windsurfrules` | Cascade workflow rules, branch policy, and planning gates |
| **GitHub Copilot** | Supported | `.github/copilot-instructions.md` | Copilot Chat and Workspace quality gate enforcement |
| **WSL Ubuntu 22.04** | Native | Commands run in WSL through PowerShell wrappers | Full cross-platform shell compatibility |

### Validate Harness Readiness

Audit your project's compatibility across all AI tools at any time:

```bash
# Validate compatibility across all supported harnesses
python3 scripts/harness_adapter.py --validate --project-dir .

# Install or sync missing harness bridges without overwriting custom rules
python3 scripts/harness_adapter.py --project-dir .
```

---

## Skill Ecosystem and Registries

ASD supports discovery, installation, and management through registries documented in [SKILL_REGISTRIES.md](SKILL_REGISTRIES.md):

- **[Skills Marketplace (SkillsMP)](https://skillsmp.com)**: Searchable catalog of agent skills accessible via REST API (`SKILLSMP_API_KEY`).
- **[Paul Bakaus Impeccable](https://github.com/pbakaus/impeccable)**: Design craft floor, WCAG accessibility standards, and automated UI defect scanner (`impeccable detect`).
- **[Antigravity Skills](https://github.com/rmyndharis/antigravity-skills)**: Backend, distributed systems, and DevOps skills.
- **[Skills.md](https://skills.md)**: Agent tools for repository automation and content workflows.
- **[Matt Pocock's Skills](https://github.com/mattpocock/skills)**: Skills for `grilling`, `domain-modeling`, `to-spec`, `refactor`, and `prototype`.
- **[Anthropic Official Skills](https://github.com/anthropics/skills)**: Frontend craft and ergonomic design patterns (`frontend-design`).
- **[Cathy Kim SemVer](https://github.com/cathy-kim/skill-semver)**: SemVer standards and release automation.

```bash
# Search for skills across connected registries
python3 scripts/skill_registry.py search "fastapi"

# Install a skill into the ecosystem
python3 scripts/skill_registry.py install "fastapi"
```

---

## Frequently Asked Questions (FAQ)

### Does ASD slow down my AI coding workflow?
**No, it significantly speeds up delivery.** Without ASD, AI agents write fast code that takes hours to debug, refactor, and test manually. By catching edge cases, enforcing TDD, and executing automated quality gates upfront, ASD eliminates the 80% time sink spent repairing subtle AI regressions.

### Can I adopt ASD on an existing codebase without breaking it?
**Yes.** Running `/project-init` on an existing repository operates in **Retrofit Mode**. It introduces the `.agents/` governance directory and bridge files without altering a single line of your existing application code or git history.

### Do all teammates need to use the same AI coding assistant?
**No.** That is the core advantage of ASD's Universal Multi-Harness architecture. One developer can use Claude Code in the terminal, another can use Cursor, a third can use Windsurf, and another can use Antigravity. Because they all share the `.agents/` single source of truth, every developer's AI assistant follows the exact same conventions and quality gates.

### What languages and frameworks does ASD support?
ASD is stack-agnostic. It works out-of-the-box with TypeScript/JavaScript, Python, Go, Rust, PHP/Laravel, Java, C#, and Ruby. The quality gates adapt to your project's native test runner (Vitest, Jest, PyTest, PHPUnit, Cargo test) and schema validation libraries.

---

## License

MIT License © [Idequel Bernabel](https://github.com/ibernabel).

Community skills from [Matt Pocock](https://github.com/mattpocock/skills) and other open-source contributors are subject to their respective licenses.
