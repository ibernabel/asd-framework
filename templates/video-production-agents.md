# Video Production — Project Rules

> Copy this file to `<project>/.agents/AGENTS.md` for any video production project.

## Domain: 🎬 Video Production

## Execution Scope: Fast Mode (Direct Execution)

This project uses **Fast Mode** by default. The ASD planning overhead is skipped for content tasks. Planning Mode only activates when modifying production pipeline tools (Python scripts, automation workflows).

## Roles

The agent switches between these three mindsets:

1. **Director:** Owns the creative vision. Reviews scripts for narrative arc, pacing, and audience engagement. Ensures the hook captures attention within the first 5 seconds.
2. **Editor:** Focuses on technical execution. Reviews shot lists for coverage, editing checklists for completeness, and metadata for SEO optimization.
3. **Reviewer:** Quality control. Checks brand consistency, platform compliance, and content accuracy before publishing.

## Quality Standards

- Every video must have a **script** before shooting
- Scripts must follow the **Hook → Content → CTA** structure
- Shot lists must cover all script segments
- Thumbnails need a design brief before creation
- YouTube metadata (title, description, tags, chapters) must be SEO-optimized
- Subtitles/captions required for accessibility

## Workflow

### Pre-Production
1. **Concept Brief** → Define topic, angle, target audience, platform
2. **Script** → Write using appropriate template (long-form, short-form, tutorial)
3. **Shot List** → Generate from script with B-roll checklist
4. **Thumbnail Brief** → Design concept before shooting

### Production
5. **Shooting** → Follow shot list, capture all planned shots + B-roll
6. **Raw Review** → Quick review of footage against shot list

### Post-Production
7. **Edit Checklist** → Rough cut → fine cut → color → audio → graphics → export
8. **Color Grading** → Apply color specs from grading notes
9. **Audio Mix** → Apply levels, music, SFX, VO balance
10. **Subtitles** → Generate and format captions

### Publishing
11. **Metadata** → SEO-optimized title, description, tags, chapters
12. **Thumbnail** → Final design based on brief
13. **Schedule** → Platform-specific scheduling

## Documentation

Production assets live in the project directory:
```
<project>/
├── scripts/          (video scripts)
├── shot-lists/       (shot breakdowns)
├── thumbnails/       (thumbnail briefs and assets)
├── metadata/         (titles, descriptions, tags)
├── subtitles/        (SRT/VTT files)
├── edit-notes/       (color grading, audio mix notes)
└── docs/             (pipeline tools documentation ONLY)
```

## Auto-invoke Skills

| Skill | Trigger |
|-------|---------|
| `video-script-writer` | Writing video scripts |
| `shot-list-generator` | Creating shot lists |
| `editing-workflow` | Post-production tasks |
| `thumbnail-designer` | Creating thumbnail briefs |
| `video-seo` | YouTube metadata optimization |
| `subtitle-generator` | Caption/subtitle work |
| `humanizer` | Reviewing content for naturalness |
| `hook-writer` | Crafting opening hooks |
| `commit` | Creating git commits |

## Fast Mode Reminder

When in Fast Mode:
- ❌ Do NOT generate `implementation.md`
- ❌ Do NOT generate `walkthrough.md`
- ❌ Do NOT update `ROADMAP.md`
- ✅ Execute directly, correctly, and concisely
- ✅ Use the appropriate template for the task
- ✅ Ensure quality standards are met

---

## Global Workflows & Meta-Commands

The following meta-workflows are managed globally in `~/.agents/workflows/` (`/home/ibernabel/.agents/workflows/`) and available in all projects:

| Command / Trigger | Canonical Path | Description |
|-------------------|----------------|-------------|
| `/project-init` | `~/.agents/workflows/project-init.md` | Initialize, retrofit, or update project structure, ASD docs, and skills |
| `/repo-sync` | `.agents/workflows/repo-sync.md` | SemVer bump, CHANGELOG, commit, tag, and push |
| `/post-session-doc` | `.agents/workflows/post-session-doc.md` | Update SSOT `docs/` at end of session |
| `/docs-and-sync` | `.agents/workflows/docs-and-sync.md` | Run `post-session-doc` followed by `repo-sync` |

> **Meta-Workflow Rule for `/project-init`:**
> `project-init.md` is maintained strictly at `~/.agents/workflows/project-init.md`. When `/project-init` is entered or requested, load and execute the global file directly. Do not search for a local file in the project.

