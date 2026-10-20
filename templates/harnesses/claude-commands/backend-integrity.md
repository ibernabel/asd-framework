---
description: Audit backend code against architecture, validation, timeout, and transaction rules
---

Follow the instructions in `.agents/skills/backend-integrity/SKILL.md`.
Run `python3 ~/.agents/skills/backend-integrity/scripts/verify_backend_integrity.py <target-files-or-dir>`
Enforce:
1. Input validation with typed schemas (Zod, Pydantic, DTOs).
2. Atomic transactions on multi-table mutations.
3. Explicit network request timeouts (<= 10s).
4. Mandatory pagination on collection endpoints.
5. Clean architectural separation between transport and domain logic.
