---
description: Execute the 3-Stage Lite Pipeline (Planner -> Implementer -> Reviewer)
---

Follow the instructions in `.agents/skills/code-pipeline-lite/SKILL.md` (or `~/.agents/skills/code-pipeline-lite/SKILL.md`).
1. Verify active branch is NOT main/develop (`feature/*`).
2. Planner: Extract concise acceptance criteria and edge cases. Obtain sign-off.
3. Implementer: Implement approved criteria accompanied by unit tests.
4. Reviewer: Run test suite, audit security, check UI craft and backend integrity.
5. If financial project, run PII verifier before completion.
