# Business Administration — Project Rules

> Copy this file to `<project>/.agents/AGENTS.md` for any business administration project.

## Domain: 💼 Business Administration

## Execution Scope: Admin Mode (Lightweight Planning)

This project uses **Admin Mode** — a lightweight version of Planning Mode. Brief scope/checklist before execution, accuracy verification (especially financial), and delivery summary instead of full walkthrough.

## Roles

The agent switches between these three mindsets:

1. **Analyst:** Scopes the task. Identifies requirements, validates inputs, and ensures completeness before drafting.
2. **Drafter:** Produces professional documents following templates. Maintains consistent branding and tone.
3. **Reviewer:** Double-checks accuracy (especially financial calculations), professionalism, and completeness. Verifies no PII leakage.

## Quality Standards

- Financial calculations require **double verification** (calculate, then re-verify)
- All documents must include **consistent branding** (Solufime / personal brand)
- Client data is **privacy-first** — no PII in logs, commits, or brain artifacts
- Professional communication standards at all times
- Document templates must be used for consistency
- Every deliverable needs a delivery summary

## Workflow

### Scope
1. **Requirements** → Clarify what's needed, who the audience is, any deadlines
2. **Template Selection** → Choose appropriate template(s)
3. **Input Validation** → Verify all numbers, dates, names, and details

### Draft
4. **Generate Document** → Follow template, fill all fields
5. **Branding** → Apply consistent branding elements
6. **Calculations** → If financial, compute and cross-verify

### Review
7. **Accuracy Check** → Verify all facts, numbers, and details
8. **Professional Tone** → Ensure appropriate formality
9. **Privacy Check** → No PII in commits or logs
10. **Completeness** → All required fields filled

### Deliver
11. **Delivery Summary** → Brief report of what was created and status
12. **Follow-up** → Schedule any needed follow-ups

## Privacy Rules

> [!CAUTION]
> - NEVER commit client PII (names, emails, phone numbers) to git
> - NEVER include real financial data in brain artifacts
> - ALWAYS use `.gitignore` for client-specific documents
> - ALWAYS reference clients by project code, not personal details, in commits

## Documentation

Business assets live in the project directory:
```
<project>/
├── clients/          (client profiles and project history)
│   └── <client-code>/
│       ├── profile.md
│       ├── proposals/
│       ├── contracts/
│       ├── invoices/
│       └── correspondence/
├── templates/        (reusable document templates)
├── estimates/        (project estimates)
├── reports/          (engagement reports, summaries)
└── follow-ups/       (action items tracker)
```

## Auto-invoke Skills

| Skill | Trigger |
|-------|---------|
| `invoice-generator` | Creating invoices |
| `proposal-writer` | Writing client proposals |
| `contract-drafter` | Drafting contracts |
| `project-estimator` | Estimating project scope |
| `client-crm-workflow` | Managing client interactions |
| `email-composer` | Drafting professional emails |
| `excel-analysis` | Analyzing spreadsheet data |
| `pdf-processing-pro` | Processing PDF documents |
| `freelance-job-analyzer` | Analyzing freelance opportunities |
| `meeting-insights-analyzer` | Analyzing meeting transcripts |
| `commit` | Creating git commits |

## Admin Mode Reminder

When in Admin Mode:
- ✅ Generate brief scope/checklist before execution
- ✅ Verify accuracy (especially financial)
- ✅ Generate delivery summary after completion
- ❌ Skip full `implementation.md`
- ❌ Skip full `walkthrough.md`
- ⚠️ Financial documents always get double-verified

---

## Global Skills & Meta-Commands

The following meta-skills are managed globally in `~/.agents/skills/` (`/home/ibernabel/.agents/skills/`) and available across projects:

| Command / Trigger | Canonical Path | Description |
|-------------------|----------------|-------------|
| `/project-init` | `~/.agents/skills/project-init/SKILL.md` | Initialize, retrofit, or update project structure, ASD docs, and skills |
| `/repo-sync` | `.agents/skills/repo-sync/SKILL.md` | SemVer bump, CHANGELOG, commit, tag, and push |
| `/post-session-doc` | `.agents/skills/post-session-doc/SKILL.md` | Update SSOT `docs/` at end of session |
| `/docs-and-sync` | `.agents/skills/docs-and-sync/SKILL.md` | Run `post-session-doc` followed by `repo-sync` |

> **Meta-Workflow Rule for `/project-init`:**
> `project-init.md` is maintained strictly at `~/.agents/skills/project-init/SKILL.md`. When `/project-init` is entered or requested, load and execute the global file directly. Do not search for a local file in the project.

