# Registro de Repositorios y Catálogo de Skills en Línea

Este documento es la **Fuente Única de Verdad (SSOT)** para el registro, consulta e instalación de Agent Skills provenientes de repositorios y marketplaces en línea para el **Framework ASD v2**.

---

## 1. Repositorios y Marketplaces Registrados

### A. Skills Marketplace (SkillsMP)
* **Website:** https://skillsmp.com
* **Documentación API:** https://skillsmp.com/docs/api
* **Tipo de Acceso:** REST API con autenticación Bearer Token
* **Variable de Entorno:** `SKILLSMP_API_KEY` (definida en `~/.agents/.env`)
* **Endpoint Principal:**
  ```http
  GET https://skillsmp.com/api/v1/skills/search?q={query}&page=1&limit=20&sortBy=stars
  ```
* **Headers:**
  ```http
  Authorization: Bearer <SKILLSMP_API_KEY>
  ```
* **Parámetros Soportados:**
  - `q` (requerido): Término de búsqueda (ej. `semver`, `astro`, `fastapi`, `prisma`)
  - `page`: Número de página (default: 1)
  - `limit`: Cantidad por página (default: 20, max: 100)
  - `sortBy`: `stars` o `recent` (default: `stars`)
  - `category`: Filtro de categoría (ej: `data-ai`, `devops`, `frontend`)
  - `occupation`: Filtro SOC (ej: `software-developers`)
  - `language`: Código ISO de idioma detectado (`en`, `es`, `mul`)
* **Límites de Uso:** 500 peticiones/día, 30 peticiones/minuto con API Key.

#### Ejemplo de Consulta Rápida (cURL)
```bash
# Consultar SkillsMP con token autenticado
KEY=$(grep SKILLSMP_API_KEY ~/.agents/.env | cut -d= -f2 | tr -d "\r\n")
curl -s -H "Authorization: Bearer $KEY" "https://skillsmp.com/api/v1/skills/search?q=database" | jq .
```

---

### B. Paul Bakaus Impeccable (`pbakaus/impeccable`)
* **Website / Docs:** https://impeccable.style
* **Repositorio GitHub:** https://github.com/pbakaus/impeccable
* **Skill Principal:** `impeccable` (`~/.agents/skills/impeccable`)
* **Especialidad:** Craft floor para interfaces web, mobile y dashboards. Ejecuta detección automatizada de defectos UI y anti-patrones de IA mediante `impeccable detect`, audita jerarquía tipográfica, ratios de contraste WCAG $\ge 4.5:1$, tokens de diseño semánticos y cobertura exhaustiva de estados de interacción (hover, focus, active, disabled, loading, empty, error).

---

### C. Matt Pocock's Skills (`mattpocock/skills`)
* **Repositorio GitHub:** https://github.com/mattpocock/skills
* **Skills Principales:** `to-spec`, `to-tickets`, `triage`, `wayfinder`, `prototype`, `code-review`, `setup-matt-pocock-skills`
* **Especialidad:** Suite de ingeniería de software orientada a clarificación de requerimientos, descomposición de tickets (`to-tickets`), clasificación de bugs/features (`triage`), revisión de código y prototipado rápido.

---

### D. Anthropic Skills (`anthropics/skills`)
* **Repositorio GitHub:** https://github.com/anthropics/skills
* **Skill Principal:** `frontend-design` (`~/.agents/skills/frontend-design`)
* **Especialidad:** Principios de diseño frontend de alta calidad, diseño responsivo, ergonomía visual y patrones modernos de maquetación web.

---

### E. Antigravity Skills (`rmyndharis/antigravity-skills`)
* **Repositorio GitHub:** https://github.com/rmyndharis/antigravity-skills
* **Catálogo Raw:** `https://raw.githubusercontent.com/rmyndharis/antigravity-skills/main/CATALOG.md`
* **Metadatos JSON:** `https://raw.githubusercontent.com/rmyndharis/antigravity-skills/main/catalog.json`
* **Especialidad:** Paquete integral de skills de desarrollo backend, DevOps, arquitecturas distribuidas (CQRS, Event Sourcing, Saga), testing avanzado, contratos de empleo y finanzas descentralizadas.

---

### F. Skills.md / Hasna Skills (`hasna/skills`)
* **Website:** https://skills.md
* **Repositorio GitHub:** https://github.com/hasna/skills
* **Especialidad:** Skills modulares orientadas a utilidades de agentes, automatización de repositorios (`commitpush`, `diff-viewer`, `generate-api-client`), procesamiento de datos, generación de reportes y creación de contenido.

---

### G. Cathy Kim SemVer (`cathy-kim/skill-semver`)
* **Repositorio GitHub:** https://github.com/cathy-kim/skill-semver
* **Skill Principal:** `versioning-guide` (`~/.agents/skills/versioning-guide` y alias `skill-semver`)
* **Especialidad:** Guías y automatizaciones de versionado semántico (SemVer: MAJOR.MINOR.PATCH) para proyectos, skills y changelogs.

---

### H. Awesome Copilot & Agent Scaffolding (`github/awesome-copilot` & `wshobson/agents`)
* **Repositorios GitHub:** https://github.com/github/awesome-copilot y https://github.com/wshobson/agents
* **Skills Principales:** `prd`, `refactor`, `api-design-principles`, `architecture-patterns`, `secrets-management`, `github-actions-templates`, suite integral de `python-*`.
* **Especialidad:** Generación rigurosa de PRDs, refactorización de código, patrones de arquitectura de APIs y buenas prácticas en desarrollo backend con Python y CI/CD.

---

## 2. Catálogo Resumido por Vertical de Trabajo

| Categoría | Skills Destacadas (Globales & Online) | Fuentes Recomendadas |
|-----------|--------------------------------------|----------------------|
| **Core Architecture, DDD & PRD** | `prd`, `concise-planning`, `domain-modeling`, `c4-architecture`, `mermaid-diagram-specialist`, `codebase-design`, `architecture-patterns`, `cqrs-implementation`, `event-sourcing-architect` | Local `~/.agents/skills/`, Antigravity-Skills, GitHub Awesome Copilot |
| **Frontend, UI Craft & Styling** | `impeccable`, `frontend-design`, `web-design-guidelines`, `react-19`, `nextjs-15`, `tailwind-4`, `zustand-5`, `prototype`, `vercel-react-best-practices`, `tailwind-design-system`, `playwright` | `pbakaus/impeccable`, Anthropic, Local `~/.agents/skills/`, SkillsMP |
| **Backend, APIs & Architecture** | `backend-integrity`, `api-design-principles`, `api-documentation-generator`, `api-integration-specialist`, `architecture-patterns`, `jsonapi`, `django-drf`, `fastapi-templates`, `async-python-patterns`, `test-api`, `typescript`, `zod-4`, `uv-package-manager` | Local `~/.agents/skills/` (ASD Core), wshobson/agents, SkillsMP |
| **Python Engineering & Resilience** | `pytest`, `python-code-style`, `python-testing-patterns`, `python-type-safety`, `python-error-handling`, `python-design-patterns`, `python-resilience`, `python-observability`, `python-background-jobs`, `python-configuration`, `python-packaging`, `python-performance-optimization`, `python-project-structure`, `python-anti-patterns` | wshobson/agents, SkillsMP |
| **Testing, Quality & Security (QA)** | `tdd`, `code-review`, `diagnosing-bugs`, `refactor`, `test-api`, `playwright`, `performance`, `best-practices`, `security-compliance`, `secrets-management`, `wcag-audit-patterns` | Matt Pocock, wshobson/agents, Local `~/.agents/skills/` |
| **Release, CI/CD & Git Lifecycle** | `commit`, `repo-sync`, `post-session-doc`, `docs-and-sync`, `versioning-guide` (`skill-semver`), `github-actions-templates`, `resolving-merge-conflicts` | Local `~/.agents/skills/` (ASD Core), Cathy Kim, wshobson/agents |
| **Pipeline Orchestration (ASD Core)** | `code-pipeline`, `code-pipeline-lite`, `project-init`, `improve-mode` | Local `~/.agents/skills/` (ASD Framework) |
| **Discovery, Grilling & Strategic Deliberation** | `grilling`, `grill-me-matt`, `grill-with-docs`, `ask-the-council`, `wizard-of-oz-mode`, `brainstorming`, `triage`, `to-spec`, `to-tickets`, `to-questionnaire`, `setup-matt-pocock-skills`, `wayfinder` | Local `~/.agents/skills/` (ASD Core), Matt Pocock |
| **AI Agents, LLMs & Orchestration** | `langchain`, `langgraph`, `langfuse`, `langsmith-observability`, `ai-sdk-5`, `prompt-engineering`, `prompt-caching`, `autonomous-agents`, `context-window-management`, `agent-development`, `notebooklm` | Local `~/.agents/skills/`, SkillsMP |
| **Business Administration & Consulting** | `invoice-generator`, `proposal-writer`, `contract-drafter`, `client-crm-workflow`, `project-estimator`, `email-composer`, `meeting-insights-analyzer`, `excel-analysis`, `pdf-processing-pro`, `freelance-job-analyzer` | Local `~/.agents/skills/`, Hasna Skills |
| **Marketing, Content & Brand** | `social-media-writer`, `content-calendar`, `hook-writer`, `seo-copywriter`, `brand-voice-enforcer`, `newsletter-composer`, `humanizer`, `audience-analyzer`, `email-composer` | Local `~/.agents/skills/` |
| **Video Production** | `video-script-writer`, `shot-list-generator`, `thumbnail-designer`, `video-seo`, `subtitle-generator`, `editing-workflow`, `hook-writer`, `audience-analyzer`, `brand-voice-enforcer` | Local `~/.agents/skills/` |

---

## 3. Herramienta de Búsqueda e Instalación: `skill_registry.py`

Ubicación: `~/.agents/scripts/skill_registry.py`

### Comandos Disponibles:

```bash
# 1. Buscar una skill en SkillsMP API
python3 ~/.agents/scripts/skill_registry.py search "astro"

# 2. Buscar en Antigravity-Skills
python3 ~/.agents/scripts/skill_registry.py search "cqrs" --source antigravity

# 3. Instalar una skill desde un repositorio GitHub a ~/.agents/skills/
python3 ~/.agents/scripts/skill_registry.py install https://github.com/cathy-kim/skill-semver --skill-path skills/versioning-guide --name versioning-guide

# 4. Instalar Impeccable UI Craft Gate (Paul Bakaus)
python3 ~/.agents/scripts/skill_registry.py install https://github.com/pbakaus/impeccable --name impeccable

# 5. Instalar skill de Matt Pocock
python3 ~/.agents/scripts/skill_registry.py install https://github.com/mattpocock/skills --skill-path skills/engineering/code-review --name code-review

# 6. Instalar skill oficial de Anthropic (frontend-design)
python3 ~/.agents/scripts/skill_registry.py install https://github.com/anthropics/skills --skill-path skills/frontend-design --name frontend-design

# 7. Listar todas las skills locales
python3 ~/.agents/scripts/skill_registry.py list-local
```
