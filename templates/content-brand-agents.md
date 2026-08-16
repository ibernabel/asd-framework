# Content & Personal Brand — Project Rules

> Copy this file to `<project>/.agents/AGENTS.md` for any content creation or personal branding project.

## Domain: 📣 Content & Personal Brand

## Execution Scope: Fast Mode (Direct Execution)

This project uses **Fast Mode** by default. Content creation tasks execute directly without ASD planning overhead. Planning Mode only activates when building content tools or automation systems.

## Roles

The agent switches between these three mindsets:

1. **Strategist:** Owns the content strategy. Plans content calendars, defines content pillars, selects platforms, and ensures alignment with brand goals.
2. **Writer:** Produces content following brand voice guidelines. Writes hooks, body copy, and CTAs optimized for each platform.
3. **Editor:** Reviews content for brand voice compliance, SEO optimization, grammar, and naturalness. Runs humanizer check before publishing.

## Quality Standards

- All content must pass the **humanizer** check before publishing
- Every content piece must include: **Hook → Body → CTA**
- Platform-specific formatting is mandatory (character limits, hashtags, etc.)
- SEO checklist must be completed for all web-published content
- Brand voice guidelines must be referenced for every piece
- Content calendar must be maintained and updated weekly

## Brand Voice

<!-- TODO: Link to or paste your brand voice guidelines here -->
> Reference your brand voice profile document for tone, vocabulary, do's/don'ts, and personality traits. Every piece of content must be validated against these guidelines.

## Content Pillars

<!-- TODO: Define your 3-5 content pillars here -->
> Define the main topics/themes your content revolves around. Each piece should map to a pillar.

## Workflow

### Planning
1. **Content Calendar** → Plan weekly/monthly schedule across platforms
2. **Pillar Mapping** → Assign each piece to a content pillar
3. **Platform Selection** → Choose platform(s) based on content type

### Creation
4. **Hook First** → Generate 3-5 hook variations, select the strongest
5. **Body Copy** → Write following platform template
6. **CTA** → Clear call-to-action aligned with business goals
7. **Visual Brief** → If images/video needed, create asset brief

### Review
8. **Brand Voice Audit** → Validate against brand guidelines
9. **Humanizer Check** → Remove AI-writing patterns
10. **SEO Check** → Meta description, keywords, heading structure
11. **Platform Compliance** → Character limits, hashtags, formatting

### Publishing
12. **Schedule** → Post at optimal times per platform
13. **Cross-Platform** → Adapt and repurpose for secondary platforms

## Documentation

Content assets live in the project directory:
```
<project>/
├── calendar/         (weekly/monthly content plans)
├── posts/            (published content by platform)
│   ├── twitter/
│   ├── linkedin/
│   ├── instagram/
│   └── blog/
├── newsletters/      (email newsletter issues)
├── brand/            (voice guidelines, brand assets)
├── analytics/        (engagement reports)
└── ideas/            (content backlog and brainstorms)
```

## Auto-invoke Skills

| Skill | Trigger |
|-------|---------|
| `content-calendar` | Planning content schedules |
| `social-media-writer` | Writing social media posts |
| `seo-copywriter` | Writing SEO content |
| `newsletter-composer` | Drafting newsletters |
| `hook-writer` | Crafting hooks for any platform |
| `brand-voice-enforcer` | Validating brand voice compliance |
| `audience-analyzer` | Analyzing engagement metrics |
| `humanizer` | Removing AI-writing patterns |
| `commit` | Creating git commits |

## Fast Mode Reminder

When in Fast Mode:
- ❌ Do NOT generate `implementation.md`
- ❌ Do NOT generate `walkthrough.md`
- ✅ Execute directly using the appropriate template
- ✅ Always validate against brand voice
- ✅ Always run humanizer check on final output

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

