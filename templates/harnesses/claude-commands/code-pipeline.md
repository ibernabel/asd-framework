---
description: Execute the Uncle Bob 7-Agent Pipeline (Specifier -> Coder -> Refactorer -> Architect -> QA)
---

Follow the instructions in `.agents/skills/code-pipeline/SKILL.md` (or `~/.agents/skills/code-pipeline/SKILL.md`).
Coordinate the pipeline sequentially:
1. Verify active branch is NOT main/develop (`feature/*`).
2. Specifier: Draft Gherkin acceptance scenarios and QA test procedures.
3. Coder: Write failing tests, then implement code to pass.
4. Refactorer: Clean code smells and ensure CRAP <= 6.
5. Architect: Run mutation tests and verify boundary isolation.
6. QA: Run security check, UI craft detection (`impeccable detect`), and backend integrity audit (`verify_backend_integrity.py`).
7. If financial project, run PII verifier before final sign-off.
