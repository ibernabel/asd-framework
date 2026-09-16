# Software Development — Project Rules

> Copy this file to `<project>/.agents/AGENTS.md` for any software development project.

## Domain: 🔧 Software Development

## Execution Scope: Planning Mode (Strict)

This project follows the **full ASD Framework v2** with strict adherence to the plan-first workflow
and the **Uncle Bob Pipeline** (Orchestrator → Specifier → Coder → Refactorer → Architect → QA).

---

## Roles

The agent must dynamically switch between these four mindsets:

1. **Architect:** Validates `implementation.md`. Prioritizes SOLID, KISS, YAGNI, DRY. Reviews folder hierarchy and interface design.
2. **Developer:** Writes functional code based strictly on the approved plan. **No code without approved design.**
3. **QA:** Verifies the walkthrough. Ensures all Gherkin scenarios have passing tests. Runs `npm test`, `pytest`, or equivalent, plus mandatory Security Check.
4. **Security:** Audits each change for vulnerabilities. Checks session handling, secret management, input sanitization, and PII protection.

---

## ⚠️ Git Branching — Non-Negotiable

**NEVER commit directly to `main` or `develop`. No exceptions.**

- The agent **MUST REFUSE** to write production code if no feature branch is active.
- Before any coding task, verify with: `git branch --show-current`
- Branch naming convention: `feature/[domain]-[short-description]`
  - Examples: `feature/admin-client-onboarding`, `feature/auth-jwt-refresh`, `fix/api-null-pointer`
- `fix/` prefix is allowed for direct-mode changes on a branch (never on `main`).

### Branch Lifecycle
```
main ──────────────────────────────────────────────────────────► (production)
        │
        └─► feature/[domain]-[desc] ──► PR / merge ──► main
```

---

## 🔀 Change Classification — Full Pipeline vs Lite Pipeline vs Direct Mode

Before starting any task, classify the change and select the appropriate mode:

| Change Type | Examples | Mode | Agents Involved |
|-------------|----------|------|-----------------|
| `feature (core/complex)` | New domain, complex architecture, major refactor | **Pipeline (full)** | orchestrator → specifier → coder → refactorer → architect → qa |
| `feature (lite/pragmatic)` | Self-contained feature, new UI/endpoint, mid/low complexity | **Pipeline (lite)** | planner → implementer → reviewer |
| `fix` | Bug fix, null pointer, wrong validation | **Direct Mode** | Agent writes fix directly, then QA verifies |
| `tweak` | CSS adjustment, copy change, config update | **Direct Mode** | Agent executes directly, no plan required |
| `docs` | README update, ADR, docstring | **Direct Mode** | Agent writes directly |
| `chore` | Dependency update, script, CI config | **Direct Mode** | Agent executes directly |

> **Rule:** Use **Pipeline (full)** when correctness and deep verification are paramount. Use **Pipeline (lite)** when speed and pragmatic balance are needed without token overhead.

---

## 🤖 Pipeline Activation (Uncle Bob System)

For `feature` and `epic` changes, invoke the pipeline via `/code-pipeline` or by calling the **orchestrator** agent.

### Pipeline Order (Strict — Never Skip Steps)
```
Orchestrator
    │
    ├─► Specifier    → Gherkin .feature files + QA procedures
    ├─► Coder        → Tests (Red) + Implementation (Green)
    ├─► Refactorer   → CRAP ≤ 6, eliminate duplication
    ├─► Architect    → Mutation testing + coverage + architecture review
    └─► QA           → Execute QA procedures, report results
              │
              └─► [If pii: financial in CONVENTIONS.md]
                  PII Verifier → Scan for PII leaks before merge
```

### Agent Files Location
All 7 agents are available in `.agents/agents/`:
- `orchestrator/agent.md` — coordinates the full pipeline
- `specifier/agent.md` — Gherkin + QA procedures
- `coder/agent.md` — TDD implementation
- `refactorer/agent.md` — complexity reduction
- `architect/agent.md` — mutation testing + architecture
- `qa/agent.md` — QA execution
- `pii-verifier/agent.md` — PII scan (financial projects only)

---

## ✅ Quality Standards — TDD, YAGNI & Security

- **SOLID Principles:** Architecture foundation (clean boundaries, decoupled dependencies).
- **KISS & YAGNI:** Non-negotiable simplicity. Build only what is needed now; reject speculative features, unnecessary indirection, or over-abstracted frameworks.
- **DRY:** Extract shared logic into reusable modules.
- **Mandatory Frontend & UI Standard:** Whenever creating or modifying any graphical user interface (GUI / frontend / UI), the agent MUST strictly follow the directives of:
  - `/frontend-design` (`~/.agents/skills/frontend-design/SKILL.md`): Distinctive palettes, bespoke typography, intentional layout tokens, subject-grounded anti-generic aesthetics.
  - `/web-design-guidelines` (`~/.agents/skills/web-design-guidelines/SKILL.md`): Accessibility, semantic structure, responsive behavior, UX ergonomics.
- **Privacy-First & Anti-PII Protocol:**
  - Zero tolerance for leaking customer PII (Personally Identifiable Information).
  - **Data Inspection Rule:** When analyzing spreadsheets (`.xlsx`, `.csv`) or databases, agents MUST inspect structures, schemas, and headers FIRST before querying or loading data, explicitly omitting any columns with customer identity.
- **TDD:** The Coder always writes tests first (Red → Green → Refactor).
- **Coverage standard:** 100% of Gherkin scenarios defined by the Specifier MUST have passing tests.
- **Mandatory Security Audit (in QA and Reviewer):**
  - Verify absence of hardcoded API keys, secrets, tokens, or credentials.
  - Verify `.env` usage and ensure secrets are in `.gitignore`.
  - Validate input sanitization (SQL injection, XSS, insecure deserialization prevention).
- Every PR-worthy change must have a `walkthrough.md`.

---

## 💻 Environment & Terminal Execution (WSL Ubuntu First)

- **Execution Environment:** Antigravity runs on Windows (`pwsh`). Workspace resides in WSL Ubuntu 22.04 on drive `Z:\` (`Z:\home\ibernabel` ↔ `/home/ibernabel`).
- **WSL Wrapper Rule:** All terminal commands (`pnpm`, `pytest`, `vitest`, `git`, `python`, etc.) MUST run inside WSL:
  ```bash
  # [Brief one-line intent comment]
  wsl.exe -d Ubuntu-22.04 --cd <linux_path> bash -lc "<command>"
  ```
- **Prohibited:** Running build, test, or package manager commands directly in PowerShell on Windows.

---

## 🔒 PII & Secrets Verifier Activation (Financial Projects)

Check `.agents/CONVENTIONS.md` at the start of every session or task:

```yaml
# If this is set:
pii: financial
# → Activate pii-verifier agent as the MANDATORY FINAL STEP across all modes
```

### Regla Estricta por Modo de Ejecución en Proyectos `financial`:
1. **Modo Directo / General (sin pipelines formales, Antigravity, Claude Code, Codex):**
   Tras realizar los cambios y verificar los tests/seguridad, el agente DEBE ejecutar como último paso el agente `pii-verifier` antes de dar la tarea por concluida.
2. **Full Pipeline (`/code-pipeline`):**
   Specifier → Coder → Refactorer → Architect → **QA (con Security Audit)** → **PII Verifier (Etapa 6 final)**.
3. **Lite Pipeline (`/code-pipeline-lite`):**
   Planner → Implementer → **Reviewer (con Security Audit obligatorio)** → **PII Verifier (Etapa 5 final)**.

Projects that require PII & Secrets verification: any project touching user financial data, credit applications, personal identifiers, transactions, or client reports (Lender, Solufime, Consultor/technology, Corebank).

---

## Workflow Summary

```
1. Classify change (table above)
       │
       ├─ feature (core/complex) ──► Create branch → /code-pipeline → [pii-verifier if financial] → PR → merge
       │
       ├─ feature (lite/pragmatic) ──► Create branch → /code-pipeline-lite → [pii-verifier if financial] → PR → merge
       │
       └─ fix/tweak/docs ──► Create branch → Direct mode → QA/Security check → [pii-verifier if financial] → commit → PR → merge
```

**Detailed Steps (Pipeline path):**
1. **Branch** → `git checkout -b feature/[domain]-[desc]`
2. **Architect reads** requirements, resolves ambiguities
3. **Implementation.md** → technical proposal (folder hierarchy, interfaces/schemas, error handling, security)
4. **User Approval** → no code without explicit user sign-off
5. **Pipeline Execution** → `/code-pipeline` o `/code-pipeline-lite`
6. **QA / Reviewer Security Audit** → check secrets, `.env`, input sanitization
7. **PII Verification** → if `pii: financial`, run `pii-verifier` agent as the final gate
8. **Walkthrough** → QA report with test commands and security results
9. **Documentation** → update `docs/` and `ROADMAP.md`
10. **PR / Merge** → never push directly to `main`

---

## Documentation (SSOT)

All project documentation resides in `docs/`:
```
docs/
├── README.md
├── planning/         (PRD, user stories, DDD: Domain, Bounded Contexts, Ubiquitous Language)
├── implementation/   (phase summaries, feature implementations)
├── testing/          (Gherkin .feature files, test documentation, QA reports)
├── decisions/        (ADRs - Architecture Decision Records)
├── fixes/            (bug fix records)
└── knowledges/       (learned patterns, known issues)
```

---

## Auto-invoke Skills

| Skill | Trigger |
|-------|---------|
| `react-19` | React 19 components in `.tsx` |
| `nextjs-15` | Next.js App Router (`app/`) |
| `typescript` | TypeScript code in `.ts/.tsx` |
| `frontend-design` | Mandatory whenever designing or modifying UI components, layouts, or styles |
| `web-design-guidelines` | Mandatory review of UI code against web interface standards, UX, and accessibility |
| `tailwind-4` | Tailwind CSS styling |
| `zod-4` | Zod v4 schema validation |
| `zustand-5` | Zustand state management |
| `ai-sdk-5` | Vercel AI SDK v5 features |
| `django-drf` | Django REST Framework |
| `jsonapi` | JSON:API endpoints |
| `playwright` | Playwright E2E tests |
| `pytest` | pytest test files |
| `test-api` | API test patterns |
| `tdd` | TDD / Red-Green-Refactor workflow |
| `code-pipeline` | Full Uncle Bob pipeline for complex features |
| `code-pipeline-lite` | Lightweight 3-agent pipeline for medium/low complexity features |
| `commit` | Creating git commits |
| `code-review` | Reviewing PRs or branches |
| `diagnosing-bugs` | Debugging hard bugs or regressions |

---

## Global Skills & Meta-Commands

The following meta-skills are managed globally in `~/.agents/skills/` (`/home/ibernabel/.agents/skills/`) and available across projects:

| Command / Trigger | Canonical Path | Description |
|-------------------|----------------|-------------|
| `/project-init` | `~/.agents/skills/project-init/SKILL.md` | Initialize, retrofit, or update project structure, ASD docs, and skills |
| `/code-pipeline` | `.agents/skills/code-pipeline/SKILL.md` | Uncle Bob 7-Agent Pipeline execution |
| `/code-pipeline-lite` | `.agents/skills/code-pipeline-lite/SKILL.md` | Lightweight 3-Agent Pipeline execution |
| `/repo-sync` | `.agents/skills/repo-sync/SKILL.md` | SemVer bump, CHANGELOG, commit, tag, and push |
| `/post-session-doc` | `.agents/skills/post-session-doc/SKILL.md` | Update SSOT `docs/` at end of session |
| `/docs-and-sync` | `.agents/skills/docs-and-sync/SKILL.md` | Run `post-session-doc` followed by `repo-sync` |
| `/domain-modeling` | `.agents/skills/domain-modeling/SKILL.md` | Domain modeling & ADR generator |
| `/grilling` | `.agents/skills/grilling/SKILL.md` | Architecture stress-testing interview |

> **Meta-Workflow Rule for `/project-init`:**
> `project-init.md` is maintained strictly at `~/.agents/skills/project-init/SKILL.md`. When `/project-init` is entered or requested, load and execute the global file directly. Do not search for a local file in the project.

