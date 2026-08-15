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

### B. Antigravity Skills (`rmyndharis/antigravity-skills`)
* **Repositorio GitHub:** https://github.com/rmyndharis/antigravity-skills
* **Catálogo Raw:** `https://raw.githubusercontent.com/rmyndharis/antigravity-skills/main/CATALOG.md`
* **Metadatos JSON:** `https://raw.githubusercontent.com/rmyndharis/antigravity-skills/main/catalog.json`
* **Especialidad:** Paquete integral de skills de desarrollo backend, DevOps, arquitecturas distribuidas (CQRS, Event Sourcing, Saga), testing avanzado, contratos de empleo y finanzas descentralizadas.

---

### C. Skills.md / Hasna Skills (`hasna/skills`)
* **Website:** https://skills.md
* **Repositorio GitHub:** https://github.com/hasna/skills
* **Especialidad:** Skills modulares orientadas a utilidades de agentes, automatización de repositorios (`commitpush`, `diff-viewer`, `generate-api-client`), procesamiento de datos, generación de reportes y creación de contenido.

---

### D. Cathy Kim SemVer (`cathy-kim/skill-semver`)
* **Repositorio GitHub:** https://github.com/cathy-kim/skill-semver
* **Skill Principal:** `versioning-guide` (`~/.agents/skills/versioning-guide` y alias `skill-semver`)
* **Especialidad:** Guías y automatizaciones de versionado semántico (SemVer: MAJOR.MINOR.PATCH) para proyectos, skills y changelogs.

---

## 2. Catálogo Resumido por Vertical de Trabajo

| Categoría | Skills Destacadas (Globales & Online) | Fuentes Recomendadas |
|-----------|--------------------------------------|----------------------|
| **Core Architecture & DDD** | `c4-architecture`, `domain-modeling`, `codebase-design`, `architecture-patterns`, `cqrs-implementation`, `event-sourcing-architect` | Local `~/.agents/skills/`, Antigravity-Skills |
| **Frontend & Web Apps** | `frontend-design`, `react-19`, `nextjs-15`, `tailwind-4`, `zustand-5`, `prototype`, `vercel-react-best-practices`, `tailwind-design-system` | Local `~/.agents/skills/`, SkillsMP |
| **Backend & APIs** | `api-design-principles`, `api-documentation-generator`, `api-integration-specialist`, `jsonapi`, `django-drf`, `fastapi-templates`, `async-python-patterns` | Local `~/.agents/skills/`, SkillsMP |
| **Testing & Quality (QA)** | `tdd`, `pytest`, `playwright`, `test-api`, `code-review`, `diagnosing-bugs`, `refactor`, `wcag-audit-patterns` | Local `~/.agents/skills/`, Matt Pocock |
| **Release & Git Lifecycle** | `commit`, `repo-sync`, `post-session-doc`, `versioning-guide` (`skill-semver`), `resolving-merge-conflicts` | Local `~/.agents/skills/`, Cathy Kim |
| **Business & Consulting** | `invoice-generator`, `proposal-writer`, `contract-drafter`, `client-crm-workflow`, `project-estimator`, `freelance-job-analyzer`, `pdf-processing-pro`, `excel-analysis` | Local `~/.agents/skills/`, Hasna Skills |
| **AI Agents & Orchestration**| `langchain`, `langgraph`, `langfuse`, `langsmith-observability`, `ai-sdk-5`, `prompt-engineering`, `prompt-caching`, `autonomous-agents`, `context-window-management` | Local `~/.agents/skills/`, SkillsMP |
| **Marketing & Content** | `social-media-writer`, `content-calendar`, `hook-writer`, `seo-copywriter`, `brand-voice-enforcer`, `newsletter-composer`, `audience-analyzer`, `humanizer` | Local `~/.agents/skills/` |
| **Video Production** | `video-script-writer`, `shot-list-generator`, `thumbnail-designer`, `video-seo`, `subtitle-generator`, `editing-workflow` | Local `~/.agents/skills/` |

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

# 4. Listar todas las skills locales
python3 ~/.agents/scripts/skill_registry.py list-local
```
