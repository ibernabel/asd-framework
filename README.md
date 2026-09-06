# ASD Framework — Agent-Driven Structured Development

> **The framework for human-AI pair programming that actually scales.**

ASD is a practical meta-framework that lets you work with AI coding agents across **multiple domains** — software development, business administration, content creation, video production, and AI agents — with the right level of rigor for each context.

Stop fighting your AI agent. Give it a structured operating system.

---

## Why ASD?

Most AI agent setups are either too rigid (every task requires a full plan and tests) or too loose (the agent does whatever it wants). ASD solves this with **adaptive execution scopes**:

| Domain | Mode | What it means |
|--------|------|---------------|
| 🔧 Software Dev | Planning Mode (Strict) | Full pipeline: Gherkin → TDD → Refactor → QA |
| 🤖 AI Agents | Planning Mode (Strict) | Prompt versioning, eval datasets, guardrails |
| 💼 Business Admin | Admin Mode | Double-check financials, zero PII in git |
| 📣 Content & Brand | Fast Mode | Direct execution, no overhead |
| 🎬 Video Production | Fast Mode | Templates, no planning friction |

**One framework. Five domains. Zero bloat.**

---

## Key Features

- 🏗️ **Uncle Bob Pipeline** — 7 specialized AI agents: Orchestrator → Specifier → Coder → Refactorer → Architect → QA → PII Verifier
- 🌿 **Mandatory Git branching** — Never commit to `main`. The agent refuses without an active branch.
- 🧪 **Gherkin-based TDD** — Coverage is measured by scenario pass rate, not line %, powered by the Specifier agent
- 📁 **Multi-vertical support** — One project, multiple domains (e.g., Consultor: admin + software + content)
- 🔒 **Conditional PII scanning** — Financial projects auto-trigger the PII Verifier agent
- 🔀 **Change Classification** — Features go through the full pipeline; fixes use direct mode
- 📋 **CONVENTIONS.md per project** — Git rules, stack, DDD settings, PII flag — all in one config file
- 🚀 **`project-init` skill** — Initialize any project (new or existing) with the full ASD setup in minutes

---

## Quick Start

### Install all domains

```bash
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash
```

### Install a specific domain

```bash
# Software development only
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software

# Content + Admin (e.g., a blog-based business)
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain content --domain admin

# All domains
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain all
```

The installer:
1. Creates `~/.agents/` if it doesn't exist
2. Copies the selected domain templates to `~/.agents/templates/`
3. Installs core meta-skills (`project-init`, `repo-sync`, `post-session-doc`, `code-pipeline`, `docs-and-sync`) to `~/.agents/skills/`
4. For `software` domain: installs all 7 pipeline agents to `~/.agents/agents/`
5. Prints post-installation instructions

### Initialize a project

Once installed, navigate to your project directory and run:

```bash
# In your AI agent IDE (Antigravity, Cursor, Claude Code, etc.)
/project-init
```

The skill will auto-detect if it's a new project, an existing one (**retrofit mode**), or a multi-vertical project, and configure everything accordingly.

---

## The Uncle Bob Pipeline (Software Domain)

Inspired by Robert C. Martin's philosophy of quality through constraints, not willpower:

```
/code-pipeline
      │
      ├─► Specifier    → Converts requirements to Gherkin .feature files + QA procedures
      ├─► Coder        → TDD: writes failing tests first, then makes them pass
      ├─► Refactorer   → Reduces complexity (CRAP ≤ 6), eliminates duplication
      ├─► Architect    → Mutation testing + coverage + architecture review
      └─► QA           → Executes QA procedures, reports results
                │
                └─► [Optional] PII Verifier → Scans for PII leaks (financial projects)
```

**Git rule:** Every change lives on a branch. `feature/[domain]-[description]`. No exceptions.

---

## Recommended: Matt Pocock's Skills

ASD works best when combined with [Matt Pocock's skills](https://github.com/mattpocock/skills) — a collection of AI agent skills that complement the ASD workflow perfectly:

| Matt's Skill | How it fits with ASD |
|-------------|----------------------|
| `grill-with-docs` | Kick off a grilling session with your docs before any major design decision |
| `grilling` / `grill-me` | Stress-test a plan before writing the `implementation.md` |
| `domain-modeling` | Build the DDD ubiquitous language for your `ROADMAP.md` |
| `brainstorming` | Explore requirements before the Specifier writes Gherkin |
| `to-spec` / `to-tickets` | Convert informal ideas to actionable specs |
| `implement` | Execute a plan with agent guardrails |
| `refactor` | Surgical refactoring with intent |
| `prototype` | Sanity-check a design before committing to it |

Install Matt's skills:
```bash
# Via setup-matt-pocock-skills or see:
# https://github.com/mattpocock/skills
```

---

## Project Structure (Software Domain)

After running `/project-init` for a software project:

```
my-project/
├── .agents/
│   ├── AGENTS.md           ← ASD rules for this project (software-dev-agents.md)
│   ├── CONVENTIONS.md      ← Git rules, stack, DDD, PII flag
│   ├── agents/
│   │   ├── orchestrator/   ← Pipeline coordinator
│   │   ├── specifier/      ← Gherkin + QA procedures
│   │   ├── coder/          ← TDD implementation
│   │   ├── refactorer/     ← Complexity reduction
│   │   ├── architect/      ← Mutation testing + architecture
│   │   ├── qa/             ← QA execution
│   │   └── pii-verifier/   ← PII scan (financial projects)
│   └── skills/
│       ├── code-pipeline/
│       ├── repo-sync/
│       ├── post-session-doc/
│       └── docs-and-sync/
├── docs/
│   ├── planning/           ← PRD, user stories, DDD model
│   ├── implementation/     ← Feature implementation records
│   ├── testing/            ← Gherkin .feature files, QA reports
│   ├── decisions/          ← ADRs
│   ├── fixes/              ← Bug fix records
│   └── knowledges/         ← Learned patterns, known issues
├── tests/
│   └── features/           ← .feature files (Gherkin)
├── scripts/
│   └── bump_version.py     ← SemVer version management
├── VERSION                 ← Current version (e.g. 0.1.0)
├── ROADMAP.md              ← Milestones + DDD: Domain, Bounded Contexts
└── README.md
```

---

## Documentation

- [Concepts: Execution Scopes](./docs/concepts/execution-scopes.md)
- [Concepts: Uncle Bob Pipeline](./docs/concepts/uncle-bob-pipeline.md)
- [Concepts: Multi-Vertical Projects](./docs/concepts/multi-vertical.md)
- [Domain: Software Development](./docs/domains/software.md)
- [Domain: Business Admin](./docs/domains/admin.md)
- [Domain: Content & Brand](./docs/domains/content.md)
- [Domain: Video Production](./docs/domains/video.md)
- [Domain: AI Agents](./docs/domains/ai-agent.md)
- [ADR-001: ASD Framework v2 Multi-Domain](./docs/decisions/ADR-001-asd-framework-v2-multi-domain.md)
- [ADR-002: Uncle Bob Pipeline Integration](./docs/decisions/ADR-002-uncle-bob-pipeline-software-domain.md)

---

## Compatibility

ASD is designed to work with any AI coding agent IDE that supports `AGENTS.md` or `CLAUDE.md` style rules:

- ✅ **Antigravity** (Google DeepMind) — primary platform
- ✅ **Claude Code** (Anthropic)
- ✅ **Cursor**
- ✅ **Windsurf**
- ✅ Any IDE that reads `.agents/AGENTS.md`

---

## License

MIT © [Idequel Bernabel](https://github.com/ibernabel)

Skills by [Matt Pocock](https://github.com/mattpocock/skills) are his own and distributed under his license.
