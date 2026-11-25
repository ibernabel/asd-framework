# Developer Profile, Personal Context & Operating System: {{USER_NAME}}

> Canonical context file for {{USER_NAME}} — {{PRIMARY_ARCHETYPE}}.
> Referenced globally across all ASD Framework agent sessions to ground architectural decisions, business context, and collaboration tone.

---

## 👤 Executive Profile & Master Archetype

- **Name:** {{USER_NAME}}
- **Master Archetype:** **{{PRIMARY_ARCHETYPE}}** (e.g., Builder & Engineering Founder, Technical Lead & Consultant, Solo Entrepreneur)
- **Core Identity:** {{CORE_IDENTITY_DESCRIPTION}}
- **Location & Timezone:** {{LOCATION_AND_TIMEZONE}} (e.g., Santo Domingo, GMT-4 / AST)
- **Languages (`answer-in-the-same-language`):** 
  - **Chat & Dialogue:** Always reply in the exact same language {{USER_NAME}} uses in the prompt, regardless of invoked skill language.
  - **Markdown Files (`.md`):** Follow the conversation or project documentation language.
  - **Source Code & Commits:** Programming-language files, code comments/docstrings, and git commits strictly in **English**.
  - **{{PRIMARY_COMMUNICATION_LANGUAGE}}:** Native language, audience-facing content, direct interaction.

---

## 🏡 Personal Context, Lifestyle & Vision

- **Work Style & Environment:** {{WORK_STYLE_DESCRIPTION}} (e.g., Remote-first, home-based entrepreneur, studio operator)
- **Financial & Business Vision:** {{FINANCIAL_AND_BUSINESS_VISION}} (e.g., Diversified income streams via high-value consulting, digital products, automated tooling)
- **Personal Passions & Creative Balance:** {{PERSONAL_PASSIONS}} (e.g., Music, writing, digital manufacturing, athletics)

---

## 🌐 Multi-Dimensional Operating Verticals

{{USER_NAME}} operates across multiple domains, leveraging software engineering and AI as force multipliers:

```
                          {{USER_NAME}}
                    ({{PRIMARY_ARCHETYPE}})
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     ▼                           ▼                           ▼
1. Core Engineering         2. Ventures & Products       3. Toolmaking & Ops
   & Client Services           (SaaS / E-commerce)          (Automation / Media)
     │                           │                           │
     ├─ Architectural Advisory   ├─ Proprietary Products     ├─ Operational Scripts
     ├─ Fractional Tech Lead     ├─ Business Operations      ├─ Media Pipelines
     └─ Enterprise Software      └─ Unit Economics           └─ Custom Tooling
```

---

### Vertical 1: Core Engineering & Consulting Services (`{{PRIMARY_SERVICE_BRAND}}`)

- **Brand & Vehicle:** {{PRIMARY_SERVICE_BRAND}}
- **Core Offering:** Fractional CTO, Principal Architecture, and End-to-End Product Engineering.
- **Key Client Accounts & Projects:**
  - `{{ACCOUNT_1}}`: Description of role, architecture, and technology.
  - `{{ACCOUNT_2}}`: Description of role, architecture, and technology.

---

### Vertical 2: Proprietary Ventures & Business Operations (`{{PRIMARY_VENTURE_BRAND}}`)

- **Business Domain:** {{VENTURE_DOMAIN}} (e.g., FinTech, E-commerce, Physical Goods)
- **Operational Reality:** {{VENTURE_OPERATIONS_DESCRIPTION}}
- **Software Lab & Tooling:**
  - `{{PROJECT_TOOL_1}}`: Purpose, stack, and operational impact.
  - `{{PROJECT_TOOL_2}}`: Purpose, stack, and operational impact.

---

### Vertical 3: Rapid Toolmaking, Automation & Personal Initiatives

- **Domain:** {{TOOLING_DOMAINS}} (e.g., Media processing, automated fabrication, audio/video)
- **Key Projects:**
  - `{{TOOL_NAME_1}}`: Problem solved, tools used, and workflow benefits.
  - `{{TOOL_NAME_2}}`: Problem solved, tools used, and workflow benefits.

---

## 🎭 Agent Collaboration Protocol: Adaptive Tri-Modal Interaction

Agents dynamically detect which **"Hat"** {{USER_NAME}} is wearing and adapt their collaboration tone, scrutiny level, and execution speed accordingly:

| Active Hat | Typical Projects | Mindset & Agent Behavior | Primary Standards |
|---|---|---|---|
| **Hat A: Core Software Architect** | Core platforms, client architecture, security-critical code | **Strict & Uncompromising.** Demand clean architecture, strict typing, TDD, DDD boundaries, zero PII exposure, and comprehensive testing. Challenge shortcuts. | DDD, SOLID, Clean Architecture, PII Verifier, Security Audits |
| **Hat B: Co-Founder & Business Operator** | Business administration, costing, operations, client proposals | **Analytical, Pragmatic & ROI-Driven.** Act as a sharp co-founder. Focus on unit economics, operational bottlenecks, legal compliance, and friction reduction. | Admin Mode, PERT estimation, friction elimination, workflow automation |
| **Hat C: Rapid Toolmaker & Media Hacker** | Automation scripts, media pipelines, rapid prototypes | **Fast, Pragmatic & Prototype-First.** Maximize iteration velocity and simplicity (KISS). Leverage scripts, CLI tools, and APIs without bloated layers. | Fast Mode, functional simplicity, immediate utility |

---

## 🏛️ Architectural Principles & Software Engineering Standards

- **SOLID Principles:** Strict adherence to Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.
- **KISS (Keep It Simple, Stupid):** Reject premature abstractions or over-engineered design patterns when a simpler, readable solution suffices.
- **YAGNI (You Aren't Gonna Need It):** Never build speculative features or unneeded code paths. Focus on current requirements with clean extension seams.
- **DRY (Don't Repeat Yourself):** Consolidate business logic into single sources of truth.
- **Domain-Driven Design (DDD):** Explicit Bounded Contexts, Ubiquitous Language, and isolation between Domain Core, Application Services, and Infrastructure.
- **Privacy-First & Data Sanitization:** Zero tolerance for customer data leaks or exposed secrets. Schemas and headers must be audited before querying live databases or spreadsheets, strictly excluding PII.

---

## 💻 Technical Stack & Preferences

### Backend & Core Systems
- **Languages:** {{BACKEND_LANGUAGES}}
- **Architecture:** Hexagonal / Clean Architecture, Modular Monoliths, Event-Driven Services.
- **APIs & Protocols:** RESTful (JSON:API), GraphQL, Webhooks, SSE/WebSockets.
- **Databases & Stores:** {{DATABASES}}

### Frontend & User Interfaces
- **Frameworks & State:** {{FRONTEND_FRAMEWORKS}}
- **UI & Craft Standard:** Strict enforcement of `/frontend-design` and `/web-design-guidelines`. Anti-generic aesthetics, high visual craft, intentional color tokens, responsive layouts, and zero raw hex in classes.

### AI Engineering & Tooling
- **AI Tooling & Orchestration:** {{AI_TOOLS}} (e.g., Antigravity, Claude Code, Vercel AI SDK, LangGraph)

---

## 🔒 Confidentiality, Security & PII Rules

1. **Anti-PII Mandate:** Under no circumstances should agent logs, context windows, or outputs display real client PII (names, identification numbers, bank accounts, or phone numbers).
2. **Data Structure Inspection First:** When working with `.xlsx`, `.csv`, or SQL queries, inspect columns and table definitions first. Filter out sensitive demographic or financial identification fields.
3. **Secrets Hygiene:** All credentials must live strictly inside `.env` files with rigorous `.gitignore` verification. No inline tokens or private keys.
