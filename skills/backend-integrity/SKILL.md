---
name: backend-integrity
description: Backend Integrity & Architecture Protocol. Guidance and automated verification for Clean/Hexagonal Architecture, Schema-First input validation, transactional atomicity, I/O timeouts, and anti-pattern prevention.
license: Apache-2.0
metadata:
  author: ibernabel
  version: "1.0.0"
  scope: [root, backend, api]
  auto_invoke: "Working on backend, APIs, services, databases, or workers"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Task
---

# Backend Integrity & Architecture Protocol

This skill enforces high-integrity engineering standards for backend development (APIs, services, models/ORMs, queues, and background jobs) across Python, TypeScript/Node, PHP, and Go.

It prevents common AI-generated architectural degradations: bloated "God controllers", missing input schemas (mass-assignment vulnerabilities), calls to external services without timeouts (blocking I/O threads), silent exception suppression, and database N+1 queries.

---

## The Two-Phase Lifecycle

### Phase 1: Pre-Implementation (Backend Floor Gate)
Before writing backend production code, the agent MUST consult [`reference/backend-floor.md`](reference/backend-floor.md) and enforce the **6 Non-Negotiable Rules**:

1. **Schema-First Input Validation (Zero Mass-Assignment):**
   - Every incoming request (HTTP body, query parameters, webhooks) MUST be validated against a typed schema before reaching the domain or database (Zod in TypeScript, Pydantic in Python, FormRequest in Laravel).
2. **Transactional Atomicity:**
   - Any business operation that mutates two or more tables/entities MUST be wrapped in an explicit transaction (`db.transaction()` or `@transaction.atomic`).
3. **Strict I/O Resilience & Timeouts:**
   - Every network call (`httpx`, `requests`, `fetch`, `axios`, Redis, external queues) MUST specify an explicit timeout (recommended: $\le 10\text{s}$) and handle network failure with exponential backoff (`python-resilience`).
4. **Zero N+1 & Mandatory Pagination:**
   - No unrestricted collection queries (`SELECT *` without limit). All relations traversed in loops must use eager loading (`select_related`, `prefetch_related`, `include`).
5. **Layer Isolation (Clean / Hexagonal Architecture):**
   - Controllers/Resolvers ONLY adapt HTTP $\leftrightarrow$ Domain. Business rules, validation logic, and raw queries cannot live inside HTTP controllers.
6. **Semantic Error Hierarchy:**
   - Zero silent exception suppression (`except: pass` or empty `catch`). Errors map to structured responses (`{ "error": { "code": "...", "message": "..." } }`) with proper HTTP status codes (400, 401, 403, 404, 409, 422).

---

## Phase 2: Post-Implementation (Mechanical Verification Gate)

Every backend change must be verified using the automated static detector before passing QA or Reviewer approval:

```bash
# Run backend integrity detector on modified server files
wsl.exe -d Ubuntu-22.04 --cd <project-path> bash -lc "~/.agents/skills/backend-integrity/scripts/verify_backend_integrity.py <modified-backend-files>"
```

### Exit Codes:
- `0`: Scan passed with 0 primary findings (**Backend CERTIFIED**).
- `2`: Primary architectural violations found (**Backend REJECTED** — must be resolved before QA/Reviewer sign-off).

---

## Supporting Skills
- [`architecture-patterns`](file:///z:/home/ibernabel/.agents/skills/architecture-patterns/SKILL.md): Clean Architecture & Domain-Driven Design patterns.
- [`api-design-principles`](file:///z:/home/ibernabel/.agents/skills/api-design-principles/SKILL.md): REST and GraphQL contract conventions.
- [`python-resilience`](file:///z:/home/ibernabel/.agents/skills/python-resilience/SKILL.md): Retries, exponential backoff, jitter, and circuit breakers.
- [`python-error-handling`](file:///z:/home/ibernabel/.agents/skills/python-error-handling/SKILL.md): Custom exception hierarchies and structured errors.
- [`test-api`](file:///z:/home/ibernabel/.agents/skills/test-api/SKILL.md): Tenant isolation, RBAC, and Celery task testing.
