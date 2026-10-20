# ASD Framework

> Agent-Driven Structured Development (ASD): engineering discipline and workflow guardrails for human-AI pair programming.

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.6.0-green.svg)](VERSION)
[![Harness Compatibility](https://img.shields.io/badge/harness-universal-purple.svg)](#universal-ai-harness-compatibility)

[English](README.md) · [Español](README.es.md)

</div>

---

ASD sets practical operating boundaries for AI coding agents across five domains: software engineering, autonomous agents, business operations, content, and video production.

Left on their own, coding agents routinely hallucinate imports, skip test suites, stuff business logic into controllers, and push unverified changes straight to `main`. But locking them behind 20-page requirement documents for a small CSS fix is just as counterproductive.

ASD balances speed and discipline with domain-specific pipelines, scripted quality checks, and strict branch protection.

---

## What is ASD?

ASD is an engineering workflow and governance layer, not a software library you import into your application code. Your production app never touches ASD; it exists entirely to keep your AI coding assistants disciplined.

It applies three core principles to everyday development:

- **Inversion of control for agents**: In a standard chat session, the model decides what to do next. ASD reverses this: the framework dictates the steps (`Specifier` → `Coder` → `Refactorer` → `Architect` → `QA`), pauses for human approval, and requires green tests before moving forward. The agent writes the code, but the workflow controls the lifecycle.
- **Deterministic quality gates**: Scripted checks catch problems before code gets committed: missing schema validation, unpaginated queries, multi-table writes without transactions, leaky credentials, and broken UI accessibility.
- **Universal harness sync**: Keep your conventions in one place (`.agents/`). ASD automatically generates and updates configuration files for Antigravity, Claude Code, Cursor, Windsurf, and GitHub Copilot so everyone on the team stays aligned.

---

## Who is it for?

### Developers who write clean code by hand
If you already practice TDD, follow Clean Architecture, and care about maintainability, you've probably watched an AI agent tear through your codebase with sloppy shortcuts. ASD turns the agent into a disciplined junior engineer: it writes tests first, respects layer boundaries, validates schemas, and keeps cyclomatic complexity down (CRAP score $\le 6$).

### Developers getting started with AI
You don't need 50-line prompts or prompt-engineering tricks to get reliable code. Run `/code-pipeline-lite`, review the concise plan the agent generates, approve it, and let it implement the feature against automated checks. If the agent makes a mistake, the quality gates reject the code before it reaches git.

### Engineering teams and tech leads
Developers on the same team often use different tools: one prefers Cursor, another runs Claude Code in the terminal, while someone else uses Windsurf or Copilot. ASD centralizes your coding standards, branch rules, and agent definitions in `.agents/`, syncing native configuration files across every editor so code quality stays consistent across pull requests.

---

## The workflow in 30 seconds

```
       Feature request or idea
                  │
                  ▼
         [ Choose pipeline ]
          │               │
          │ (Complex)     │ (Standard / Isolated)
          ▼               ▼
   /code-pipeline   /code-pipeline-lite
          │               │
          ▼               ▼
     [ Plan & acceptance criteria ] ──► Pauses for your sign-off
          │
          ▼
     [ TDD implementation ] ──────────► Failing test first, then minimal code
          │
          ▼
     [ Automated quality gates ]
          ├─► UI craft gate (WCAG AA, no AI-slop patterns)
          ├─► Backend integrity gate (Schemas, transactions, timeouts)
          └─► PII & security gate (Secrets audit, zero customer data in git)
          │
          ▼
     [ Dedicated git branch & conventional commit ]
```

---

## Quickstart: from zero to first feature

### 1. Install ASD globally

Install ASD into your global environment (`~/.agents/`):

```bash
# Install all domains
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash
```

To install specific domains only:

```bash
# Software engineering only
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software

# Software + Business Administration
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software --domain admin
```

### 2. Initialize or retrofit your project

Open your AI coding environment (Claude Code, Cursor, Windsurf, or Antigravity) in your project directory and run:

```bash
/project-init
```

ASD inspects your workspace and runs in one of three modes:
- **Init mode** (empty directory): Sets up git, `.gitignore`, the canonical `docs/` tree, `AGENTS.md`, `CONVENTIONS.md`, and pipeline agents.
- **Retrofit mode** (existing repository): Adds ASD governance files without altering existing source code or git history.
- **Update mode** (existing ASD project): Updates agents, skills, and bridge files while preserving your project conventions.

### 3. Build a feature step-by-step

Here is how a typical session unfolds:

1. **Trigger a task:**
   ```text
   /code-pipeline-lite Add avatar upload endpoint with 2MB image validation
   ```

2. **The Planner extracts criteria and pauses for your approval:**
   ```text
   [Planner] Proposed acceptance criteria:
   1. POST /api/user/avatar accepts JPEG and PNG files only.
   2. Files exceeding 2MB return 413 Payload Too Large.
   3. File contents validated via magic bytes (not just extension).
   4. Uploaded key links to the authenticated user ID.

   Do you approve these criteria before implementation begins?
   ```

3. **You review and approve:**
   ```text
   Approved, proceed.
   ```

4. **The Implementer writes tests and code:**
   - Checks out a dedicated branch (`feature/software-avatar-upload`).
   - Writes unit and integration tests covering valid uploads, oversized files, and invalid formats.
   - Writes the minimal endpoint logic to turn all tests green.

5. **The Reviewer certifies quality gates:**
   - Confirms schema validation is in place.
   - Verifies no hardcoded secrets or customer data.
   - Runs `verify_backend_integrity.py`.
   - Creates a conventional commit: `feat(api): add avatar upload endpoint with file size validation`.

### 4. Run quality gates manually

You can run quality gates anytime from your terminal:

```bash
# Audit backend architecture, schemas, and transactions
python3 scripts/verify_backend_integrity.py src/

# Audit UI code for accessibility defects and design flaws
impeccable detect src/components/
```

### 5. Sync session docs and releases

When your work is done and merged, sync documentation and release metadata:

```bash
# Save session deliverables to docs/ and sync GitHub (SemVer, CHANGELOG, tags)
/docs-and-sync
```

---

## Execution scopes

ASD adapts its level of process depending on what you're working on:

| Domain | Mode | Execution style | Quality gates |
|---|---|---|---|
| **Software** | Planning Mode (Strict) | Uncle Bob Pipeline or Code Pipeline Lite; Gherkin TDD | UI craft check, backend integrity check, security audit, PII scan |
| **AI Agents** | Planning Mode (Strict) | Prompt versioning, evaluation datasets, guardrails | Behavioral regression suite |
| **Business Admin** | Admin Mode | Scoped checklists, delivery summaries | Financial double-check, zero customer data in git |
| **Content & Brand** | Fast Mode | Direct execution, platform formatting | Brand voice guidelines, humanizer review |
| **Video Production** | Fast Mode | Scripts, shot lists, metadata | Template verification, direct delivery |

---

## Choosing your software pipeline

ASD provides two pipelines depending on task scope:

### 1. Code Pipeline Lite (`/code-pipeline-lite`)
Use for day-to-day work: isolated endpoints, bug fixes, UI components, and utility functions (most daily tasks).

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
Use for core business logic, complex database migrations, multi-service features, and structural architecture changes.

```
/code-pipeline
      │
      ├─► 1. Specifier      → Writes Gherkin .feature specifications & QA test procedures
      ├─► 2. Coder          → TDD: writes failing tests first, then implementation
      ├─► 3. Refactorer     → Removes duplication, keeps CRAP complexity $\le 6$
      ├─► 4. Architect      → Mutation testing, coverage review, boundary checks
      └─► 5. QA             → Executes QA test plan, validates UI and backend gates
                │
                └─► 6. [If pii: financial]
                    PII Verifier → Deep scan for data leaks
```

### Change classification

| Change type | When to use | Recommended flow |
|---|---|---|
| **Complex feature** | Core domain logic, new architectural boundaries | `/code-pipeline` |
| **Standard feature** | Isolated endpoints, UI components, background jobs | `/code-pipeline-lite` |
| **Bug fix** | Defect repairs, regression fixes | Branch + targeted test + fix + QA check |
| **Chore / Docs** | Dependency updates, documentation, style polish | Branch + direct fix + automated check |

---

## The 10 pipeline agents

Defined in `.agents/agents/` and activated by pipeline commands:

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

## Automated quality gates

ASD relies on deterministic, scriptable checks rather than subjective reviews:

### 1. UI craft gate (`impeccable`)
- **Rules**: Agents follow `/frontend-design` and the Craft Floor guidelines. Bans common AI interface habits: gradient text, decorative badges, arbitrary card grids, and raw hex codes in markup.
- **Verification**: `impeccable detect <files>`.
- **Standards**: WCAG AA contrast ($\ge 4.5:1$ body / $\ge 3:1$ large), minimum $44\times 44\text{px}$ touch targets, responsive layouts tested at 390px and desktop sizes, visible focus rings, and proper empty, loading, and error states.
- **Enforcement**: Any primary defect halts pipeline approval until resolved.

### 2. Backend integrity gate (`backend-integrity`)
- **Rules**: Agents follow `/backend-integrity` and the Backend Floor specification.
- **Core checks**:
  1. Input validation: Request bodies and parameters must match typed schemas before reaching domain logic (Zod, Pydantic, DTOs).
  2. Atomic transactions: Operations mutating two or more tables must run inside a transaction (`db.transaction()`).
  3. Explicit timeouts: All external network calls must specify bounded timeouts ($\le 10\text{s}$).
  4. Bounded queries: Collection queries must be paginated.
  5. Layer isolation: Controllers handle HTTP transport only; business logic stays in domain services.
  6. Structured errors: No silent exception suppression (`except: pass`); errors map to explicit HTTP status codes.
- **Verification**: `python3 scripts/verify_backend_integrity.py <files>`.
- **Enforcement**: Exit code 2 blocks QA or Reviewer sign-off.

### 3. Privacy & PII gate (`pii-verifier`)
- Runs automatically when `pii: financial` is declared in `CONVENTIONS.md`.
- Inspects database schemas and fixtures prior to execution, stripping customer identity and financial columns from agent exploration queries.

---

## Core commands and meta-skills

Centralized in `~/.agents/skills/` and available across all your repositories:

| Command / Skill | Scope | Description |
|---|---|---|
| `/project-init` | Global | Initialize, retrofit, or update project structure, ASD docs, and skills. |
| `/code-pipeline` | Project | Run full Uncle Bob pipeline (Specifier → Coder → Refactorer → Architect → QA). |
| `/code-pipeline-lite` | Project | Run lightweight 3-stage pipeline (Planner → Implementer → Reviewer). |
| `/backend-integrity` | Project / Global | Audit backend code against architecture, schema, and transaction rules. |
| `/humanizer` | Project / Global | Strip AI-generated writing patterns and restore natural voice. |
| `/repo-sync` | Project | Bump SemVer, update CHANGELOG, commit, tag, and push safely. |
| `/post-session-doc` | Project | Save session notes and deliverables into canonical `docs/` hierarchy. |
| `/docs-and-sync` | Project | Run `/post-session-doc` followed by `/repo-sync` sequentially. |
| `/domain-modeling` | Project | Build ubiquitous language, bounded contexts, and ADR drafts. |
| `/grilling` | Project | Interactive interview to stress-test architectural decisions before coding. |
| `/ask-the-council` | Project | Multi-perspective evaluation using five advisor roles and a coordinator. |
| `/wizard-of-oz-mode` | Project | Simulate end-to-end automation with a manual facade for quick testing. |

---

## Project structure

Running `/project-init` on a software repository establishes this layout:

```
my-project/
├── .agents/                        ← Canonical ASD Single Source of Truth (SSOT)
│   ├── AGENTS.md                   ← Agent rules & auto-invoke skills table
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
├── docs/                           ← Canonical documentation repository
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

## Universal AI harness compatibility

ASD is harness-agnostic. While canonical rules and agents live in `.agents/`, the framework synchronizes native bridge configurations across major AI coding platforms:

| AI Harness / Environment | Status | Integration Mechanism | Key Capabilities |
|---|:---:|---|---|
| **Google Antigravity** | Supported (Primary) | Native `.agents/` structure & subagents | Full Uncle Bob pipeline, skills, and slash commands |
| **Claude Code** (`claude` CLI) | Supported | `CLAUDE.md` + `.claude/commands/` | Project memory & native custom slash commands (`/code-pipeline`, etc.) |
| **OpenAI Codex & Open Standard** | Supported | Root manifest `AGENTS.md` | Conforms to open AGENTS.md standard (ChatGPT, Codex, Aider) |
| **Cursor** | Supported | `.cursorrules` & `.cursor/rules/asd-framework.mdc` | Dual-mode: legacy rules and modern Cursor Rules 2.0 (`alwaysApply: true`) |
| **Windsurf** (Codeium) | Supported | `.windsurfrules` | Cascade workflow rules, branch policy, and planning gates |
| **GitHub Copilot** | Supported | `.github/copilot-instructions.md` | Copilot Chat and Workspace quality gate enforcement |
| **WSL Ubuntu 22.04** | Native | Commands run in WSL through PowerShell wrappers | Cross-platform shell compatibility |

### Validate harness setup

Audit your project's compatibility across all tools:

```bash
# Validate compatibility across all supported harnesses
python3 scripts/harness_adapter.py --validate --project-dir .

# Install or sync missing harness bridges without overwriting custom rules
python3 scripts/harness_adapter.py --project-dir .
```

---

## Skill ecosystem and registries

ASD supports discovering, installing, and managing skills from registries documented in [SKILL_REGISTRIES.md](SKILL_REGISTRIES.md):

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

# Install a skill into your ecosystem
python3 scripts/skill_registry.py install "fastapi"
```

---

## Frequently asked questions

### Does ASD slow down development?
Writing tests and reviewing a plan takes a few minutes upfront, but it eliminates the hours spent untangling broken controllers, missed edge cases, and subtle regressions that unconstrained agents leave behind.

### Can I use ASD on an existing codebase?
Yes. Running `/project-init` in an existing repository activates **Retrofit mode**. It injects the `.agents/` folder and bridge files without modifying your application code or touching git history.

### Do team members need to use the same editor?
No. One developer can use Claude Code in the terminal, another Cursor, and another Windsurf or Antigravity. Everyone shares the same `.agents/` source of truth, so every assistant enforces the exact same rules and quality gates.

### What languages and frameworks work with ASD?
ASD is stack-agnostic. It works with TypeScript/JavaScript, Python, Go, Rust, PHP/Laravel, Java, C#, and Ruby. The quality gates hook into whatever test runner (Vitest, Jest, PyTest, PHPUnit, Cargo test) and schema validation libraries your project already uses.

---

## License

MIT License © [Idequel Bernabel](https://github.com/ibernabel).

Community skills from [Matt Pocock](https://github.com/mattpocock/skills) and other open-source contributors are subject to their respective licenses.
