# GitHub Copilot Instructions — ASD Framework

## Project Governance
This repository follows the ASD Framework pair programming and engineering standards.

## Development Rules
- **Branching Policy:** All changes must be developed on a dedicated branch (`feature/*` or `fix/*`). Never commit directly to `main` or `develop`.
- **Engineering Standards:** Follow SOLID, KISS, YAGNI, and DRY. Favor simple, decoupled, testable code over speculative abstractions.
- **TDD:** Write unit and integration tests covering positive and negative edge cases. Use Gherkin `.feature` acceptance scenarios for core features.
- **Security & Integrity:**
  - Never commit credentials or secrets.
  - Enforce typed request validation schemas (Zod, Pydantic, DTOs).
  - Wrap multi-table database writes in atomic transactions.
  - Set explicit timeouts (<= 10s) on external HTTP requests.
- **Frontend / UI:** Maintain WCAG AA accessibility, minimum 44px tap targets, and clean semantic structure.
- **Language & Commits:** All code, comments, and commit messages must be in English. Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`).
- **Canonical Architecture:** Refer to `.agents/AGENTS.md`, `.agents/CONVENTIONS.md`, and `docs/` for domain boundaries and architecture decision records.
