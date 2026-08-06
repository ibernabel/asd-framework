# Software Development — Project Rules

> Copy this file to `<project>/.agents/AGENTS.md` for any software development project.

## Domain: 🔧 Software Development

## Execution Scope: Planning Mode (Strict)

This project follows the **full ASD Framework v2** with strict adherence to the plan-first workflow
and the **Uncle Bob Pipeline** (Orchestrator → Specifier → Coder → Refactorer → Architect → QA).

---

## Roles

The agent must dynamically switch between these four mindsets:

1. **Architect:** Validates `implementation.md`. Prioritizes SOLID, KISS, DRY. Reviews folder hierarchy and interface design.
2. **Developer:** Writes functional code based strictly on the approved plan. **No code without approved design.**
3. **QA:** Verifies the walkthrough. Ensures all Gherkin scenarios have passing tests. Runs `npm test`, `pytest`, or equivalent.
4. **Security:** Audits each change for vulnerabilities. Checks session handling, secret management, input sanitization.

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

## 🔀 Change Classification — Pipeline vs Direct Mode

Before starting any task, classify the change and select the appropriate mode:

| Change Type | Examples | Mode | Agents Involved |
|-------------|----------|------|-----------------|
| `feature` | New endpoint, new UI component, new module | **Pipeline** (full) | orchestrator → specifier → coder → refactorer → architect → qa |
| `epic` | New domain, full vertical, major refactor | **Pipeline** (full) | orchestrator → specifier → coder → refactorer → architect → qa |
| `fix` | Bug fix, null pointer, wrong validation | **Direct Mode** | Agent writes fix directly, then QA verifies |
| `tweak` | CSS adjustment, copy change, config update | **Direct Mode** | Agent executes directly, no plan required |
| `docs` | README update, ADR, docstring | **Direct Mode** | Agent writes directly |
| `chore` | Dependency update, script, CI config | **Direct Mode** | Agent executes directly |

> **Rule:** When in doubt, default to **Pipeline**. The overhead is worth the quality guarantee.

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

## ✅ Quality Standards — TDD & Coverage

- **SOLID** principles are non-negotiable
- **KISS:** Avoid over-engineering
- **DRY:** Extract shared logic into reusable modules
- **TDD:** The Coder always writes tests first (Red → Green → Refactor)
- **Coverage standard:** 100% of Gherkin scenarios defined by the Specifier MUST have passing tests.
  Line coverage % is not enforced; scenario coverage is the quality gate.
- Every PR-worthy change must have a `walkthrough.md`
- Security audit on session handling, secrets, and user input

---

## 🔒 PII Verifier Activation

Check `.agents/CONVENTIONS.md` before each pipeline run:

```yaml
# If this is set:
pii: financial
# → Activate pii-verifier agent as the final step after QA
```

Projects that require PII verification: any project touching user financial data,
credit applications, personal identifiers, or reports (Lender, Solufime, Consultor/technology).

---

## Workflow Summary

```
1. Classify change (table above)
       │
       ├─ feature/epic ──► Create branch → /code-pipeline → PR → merge
       │
       └─ fix/tweak/docs ──► Create branch → Direct mode → commit → PR → merge
```

**Detailed Steps (Pipeline path):**
1. **Branch** → `git checkout -b feature/[domain]-[desc]`
2. **Architect reads** requirements, resolves ambiguities
3. **Implementation.md** → technical proposal (folder hierarchy, interfaces/schemas, error handling, security)
4. **User Approval** → no code without explicit user sign-off
5. **Pipeline** → `/code-pipeline` (Specifier → Coder → Refactorer → Architect → QA)
6. **PII Check** → if `pii: financial`, run `pii-verifier` agent
7. **Walkthrough** → QA report with test commands and results
8. **Documentation** → update `docs/` and `ROADMAP.md`
9. **PR / Merge** → never push directly to `main`

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
| `commit` | Creating git commits |
| `code-review` | Reviewing PRs or branches |
| `diagnosing-bugs` | Debugging hard bugs or regressions |
