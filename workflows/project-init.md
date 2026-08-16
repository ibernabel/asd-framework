---
description: Inicializar un nuevo proyecto configurando Git, GitHub (privado), marco ASD v2, docs/, .agents/, AGENTS.md, CONVENTIONS.md, workflows, agentes del pipeline, plantillas deterministas de skills y versionado.
user-invocable: true
---

# Workflow: Project Initialization (`project-init`)

## Descripción

Este workflow automatiza la inicialización de cualquier directorio como un proyecto estructurado bajo los estándares del desarrollador (Idequel Bernabel) y el **Framework ASD v2**.

Soporta proyectos de dominio único y proyectos **multi-vertical** (ej: Consultor con verticales `admin`, `technology`, `content`). Configura Git, GitHub privado, `.gitignore`, jerarquía `docs/`, reglas de agente por dominio, **instalación determinista de skills vía symlinks** desde `~/.agents/skills/`, sincronización de la tabla `## Auto-invoke Skills` en `AGENTS.md`, y para proyectos de software instala el pipeline Uncle Bob completo (7 agentes + workflows).

---

## Dominios de Proyecto y Presets de Skills

El proyecto debe clasificarse en una de las 5 categorías para aplicar la plantilla y el conjunto de skills adecuado desde `/home/ibernabel/.agents/templates/`:

| Dominio | Plantilla | Modo | Preset de Skills | Aplica para |
|---------|-----------|------|------------------|-------------|
| `software` | `software-dev-agents.md` | Planning Mode (Strict) | `software` (36+ skills) | APIs, web apps, CLIs, microservicios backend/frontend |
| `admin` | `business-admin-agents.md` | Admin Mode | `admin` (14 skills) | Gestión de clientes, facturación, contratos, CRM |
| `ai-agent` | `ai-agents-agents.md` | Planning Mode | `ai-agent` (24 skills) | Agentes LLM, RAG, chatbots, pipelines de IA |
| `content` | `content-brand-agents.md` | Fast Mode | `content` (12 skills) | Redes sociales, blogs, newsletters, marca personal |
| `video` | `video-production-agents.md` | Fast Mode | `video` (12 skills) | YouTube, Shorts, Reels, guiones, postproducción |

---

## Modos de Operación

El agente detecta automáticamente el modo correcto según el estado del directorio:

| Condición detectada | Modo | Comportamiento |
|---------------------|------|----------------|
| Sin `.git/` | **Init** (normal) | Flujo completo: GitHub, Git init, docs, AGENTS.md, skills, etc. |
| `.git/` existe, sin `.agents/` | **Retrofit** | Inyecta infraestructura ASD, skills y agentes. No toca código ni Git. |
| `.git/` existe + `.agents/` existe | **Update** | Actualiza lo que falta o está desactualizado (skills, workflows, docs). |

```bash
# Auto-detection logic
if [ ! -d ".git" ]; then MODE="init"
elif [ ! -d ".agents" ]; then MODE="retrofit"
else MODE="update"; fi
echo "Detected mode: $MODE"
```

### ⚡ Modo Retrofit & Update (Proyectos Existentes)

Usado cuando el proyecto ya tiene código activo, commits y estructura. **No se modifica nada existente sin autorización.**

**Pasos que se SALTAN en modo retrofit:**
- Paso 2 (GitHub + Git init) — el repo ya existe
- `.gitignore` — si ya existe, no se sobreescribe (se hace merge no destructivo)
- `README.md` — no se sobreescribe si ya existe

**Pasos que SÍ se ejecutan en modo retrofit y update:**
- Skill Inventory Check y Preset Resolution (Paso 1B)
- Detección de verticales (Paso 1, punto 3-4)
- Creación de `docs/` y subcarpetas faltantes (sin tocar los existentes)
- Paso 6A/6B: `.agents/AGENTS.md` por dominio/vertical
- Paso 6C: **Instalación de Skills del Proyecto vía symlinks y sincronización de AGENTS.md**
- Paso 7 completo (si dominio = software): agentes, CONVENTIONS.md, code-pipeline, tests/
- Paso 8: workflows globales y auditoría post-ejecución

---

## Pasos de Ejecución del Agente

### Paso 1: Determinación de Nombre, Dominio, Verticales y Stack

1. Leer el nombre del directorio actual o consultar al usuario el nombre deseado.
2. Si el usuario no especificó el dominio, solicitar la selección de uno de los 5 dominios.
3. Si el dominio es `software`, detectar o preguntar por los stacks adicionales (ej: `frontend`, `backend`, `typescript`, `python`).
4. **Detección multi-vertical:** Verificar si el directorio actual contiene subdirectorios que puedan ser verticales de trabajo:

```bash
# Detect potential vertical subdirectories (non-hidden, non-standard dirs)
ls -d */ 2>/dev/null | grep -vE '^(node_modules|\.git|dist|build|__pycache__|\.venv)/$'
```

5. Si se detectan subdirectorios, preguntar al usuario:
   - ¿Este proyecto tiene múltiples verticales? (ej: `admin/`, `technology/`, `content/`)
   - Para cada subdirectorio relevante: ¿qué dominio ASD aplica? (software / admin / ai-agent / content / video)
   - Guardar el mapa de verticales → dominios para usar en los Pasos 6B y 6C.

---

### Paso 1B: Skill Inventory & Registry Resolution

Antes de configurar el proyecto, el agente verifica que las skills necesarias están instaladas en el almacén global `~/.agents/skills/`.

```bash
# List all installed global skills
ls /home/ibernabel/.agents/skills/
```

#### Skills Principales por Dominio

| Dominio | Skills Clave a Garantizar |
|---------|---------------------------|
| `software` | `prd`, `domain-modeling`, `concise-planning`, `c4-architecture`, `mermaid-diagram-specialist`, `codebase-design`, `tdd`, `code-review`, `diagnosing-bugs`, `refactor`, `test-api`, `playwright`, `pytest`, `typescript`, `frontend-design`, `api-design-principles`, `security-compliance`, `best-practices`, `performance`, `commit`, `repo-sync`, `post-session-doc`, `versioning-guide` |
| `admin` | `invoice-generator`, `proposal-writer`, `contract-drafter`, `client-crm-workflow`, `project-estimator`, `email-composer`, `excel-analysis`, `pdf-processing-pro`, `freelance-job-analyzer`, `meeting-insights-analyzer`, `commit`, `post-session-doc`, `repo-sync`, `versioning-guide` |
| `ai-agent` | `langchain`, `langgraph`, `langfuse`, `langsmith-observability`, `ai-sdk-5`, `prompt-engineering`, `prompt-caching`, `autonomous-agents`, `context-window-management`, `agent-development`, `notebooklm`, `prd`, `domain-modeling`, `tdd`, `commit`, `post-session-doc`, `repo-sync`, `versioning-guide` |
| `content` | `social-media-writer`, `content-calendar`, `hook-writer`, `seo-copywriter`, `brand-voice-enforcer`, `newsletter-composer`, `humanizer`, `audience-analyzer`, `email-composer`, `commit`, `post-session-doc`, `repo-sync` |
| `video` | `video-script-writer`, `shot-list-generator`, `thumbnail-designer`, `video-seo`, `subtitle-generator`, `editing-workflow`, `hook-writer`, `audience-analyzer`, `brand-voice-enforcer`, `commit`, `post-session-doc`, `repo-sync` |

#### Búsqueda en Registros Online si falta alguna skill
Si alguna skill no se encuentra instalada localmente, el agente puede consultar el registro online usando:

```bash
# Search online registries (SkillsMP, Antigravity-Skills, Skills.md)
python3 /home/ibernabel/.agents/scripts/skill_registry.py search "<query>"

# Install missing skill from GitHub repository
python3 /home/ibernabel/.agents/scripts/skill_registry.py install "<repo_url>" [--skill-path "<path>"] [--name "<name>"]
```

Consulta el catálogo completo en `~/.agents/SKILL_REGISTRIES.md`.

---

### Paso 2: Verificación e Inicialización de GitHub & Git

1. Comprobar si el repositorio remoto ya existe en GitHub:
```bash
# Check if GitHub repository exists
gh repo view $(basename "$PWD")
```

2. Si no existe, crear un nuevo repositorio **privado** en GitHub y conectarlo:
```bash
# Create private GitHub repository and set origin remote
gh repo create $(basename "$PWD") --private --source=. --remote=origin
```

3. Inicializar Git si aún no se ha inicializado:
```bash
# Initialize local git repository
git init && git branch -M main
```

---

### Paso 3: Actualización de `.gitignore`

> ⚠️ **REGLA ESTRICTA: NUNCA sobreescribir ni borrar `.gitignore`.** Si el archivo existe, solo se agregan las entradas que falten. Si no existe, se crea desde la plantilla.

**Plantillas de referencia**:
- `software` → `/home/ibernabel/.agents/templates/gitignore/gitignore_software.txt`
- `admin` → `/home/ibernabel/.agents/templates/gitignore/gitignore_admin.txt`
- Otros dominios → `/home/ibernabel/.agents/templates/gitignore/gitignore_general.txt`

**Procedimiento obligatorio:**

```bash
# 1. Verificar si .gitignore ya existe
if [ -f ".gitignore" ]; then
  echo "⚠️  .gitignore ya existe — modo MERGE (no sobreescritura)"
  # 2. Leer la plantilla del dominio y agregar solo las entradas faltantes
else
  echo "ℹ️  .gitignore no existe — creando desde plantilla"
  cp /home/ibernabel/.agents/templates/gitignore/gitignore_<domain>.txt .gitignore
fi
```

**Entradas mínimas a garantizar en cualquier proyecto de software**:
```gitignore
# Code intelligence cache — never commit
.codegraph/

# Environment secrets
.env
.env.local
.env.*.local

# Dependencies
node_modules/
__pycache__/
.venv/
```

---

### Paso 4: Estructura del Marco ASD (`docs/`)

Crear el directorio `docs/` con su estructura completa de subcarpetas (SSOT):

```bash
# Create ASD SSOT documentation structure
mkdir -p docs/{planning,implementation,fixes,testing,decisions,knowledges}
```

```
docs/
├── README.md
├── planning/         (PRD, user stories, DDD: Domain, Bounded Contexts, Ubiquitous Language)
├── implementation/   (resúmenes de features e implementaciones)
├── fixes/            (registros de solución de bugs)
├── testing/          (Gherkin .feature files, QA reports, test documentation)
├── decisions/        (ADRs - Registro de Decisiones de Arquitectura)
└── knowledges/       (patrones aprendidos, problemas conocidos)
```

Generar `docs/README.md` con el índice del SSOT y enlaces a cada subdirectorio.

---

### Paso 5: Archivos Principales de Documentación

1. Crear `README.md` en la raíz del proyecto con:
   - Título y descripción del proyecto.
   - Dominio y tipo de proyecto (y verticales si aplica).
   - Estructura de directorios.
   - Comandos principales (desarrollo, pruebas, sincronización).

2. Crear `ROADMAP.md` — el formato varía por dominio:
   - **Para dominio `software`:** Incluir secciones de DDD:
     ```markdown
     # ROADMAP

     ## Domain Model
     - **Domain:** [nombre del dominio de negocio]
     - **Bounded Contexts:** [listar contexts]
     - **Ubiquitous Language:** [términos clave del dominio]

     ## Milestones
     - [ ] v0.1.0 — MVP: [descripción]
     - [ ] v0.2.0 — [siguiente hito]

     ## Backlog
     <!-- Features pendientes clasificadas por dominio -->
     ```
   - **Para otros dominios:** Roadmap simple con hitos y tareas.

---

### Paso 6A: Configuración de Reglas del Agente — Proyecto de Dominio Único

Copiar la plantilla del dominio seleccionado a `.agents/AGENTS.md`:

```bash
# Create .agents directory and copy domain template
mkdir -p .agents
cp /home/ibernabel/.agents/templates/<domain-template>.md .agents/AGENTS.md
```

Mapa de templates:
- `software` → `software-dev-agents.md`
- `admin` → `business-admin-agents.md`
- `ai-agent` → `ai-agents-agents.md`
- `content` → `content-brand-agents.md`
- `video` → `video-production-agents.md`

---

### Paso 6B: Configuración de Reglas del Agente — Proyecto Multi-Vertical

Para proyectos con múltiples verticales (ej: Consultor):

1. Copiar la plantilla del dominio primario a la raíz:
```bash
# Set root-level AGENTS.md (primary domain)
mkdir -p .agents
cp /home/ibernabel/.agents/templates/<primary-domain-template>.md .agents/AGENTS.md
```

2. Para **cada vertical** identificada en el Paso 1, colocar el `AGENTS.md` correspondiente:
```bash
# Configure each vertical with its domain-specific rules
mkdir -p <vertical>/.agents
cp /home/ibernabel/.agents/templates/<vertical-domain-template>.md <vertical>/.agents/AGENTS.md
```

---

### Paso 6C: Instalación Determinista de Skills del Proyecto

Instalar las skills del dominio en el proyecto creando enlaces simbólicos en `.agents/skills/` apuntando a `~/.agents/skills/` y sincronizar automáticamente la tabla `## Auto-invoke Skills` en `.agents/AGENTS.md`:

```bash
# Install deterministic skill preset and sync Auto-invoke table in AGENTS.md
python3 /home/ibernabel/.agents/scripts/install_project_skills.py --project-dir . --domain <domain>
```

Si el proyecto tiene stacks específicos (ej: fullstack con frontend y backend):
```bash
# Example for fullstack software project with python backend and react frontend
python3 /home/ibernabel/.agents/scripts/install_project_skills.py --project-dir . --domain software --stack frontend --stack backend --stack typescript
```

Para proyectos multi-vertical, ejecutar este comando en cada vertical:
```bash
# Example for multi-vertical project
python3 /home/ibernabel/.agents/scripts/install_project_skills.py --project-dir technology --domain software
python3 /home/ibernabel/.agents/scripts/install_project_skills.py --project-dir admin --domain admin
python3 /home/ibernabel/.agents/scripts/install_project_skills.py --project-dir content --domain content
```

---

### Paso 7: Configuración Completa del Dominio Software

**Se ejecuta para:** cualquier proyecto con dominio `software`, ya sea dominio único o una vertical dentro de un proyecto multi-vertical. El directorio base `$SW_DIR` es la raíz del proyecto (dominio único) o el subdirectorio de la vertical (ej: `technology/`).

#### 7A — Archivo de versión y script de bump
```bash
# Create initial VERSION file
echo "0.1.0" > $SW_DIR/VERSION

# Copy bump_version script
mkdir -p $SW_DIR/scripts
cp /home/ibernabel/.agents/templates/scripts/bump_version.py $SW_DIR/scripts/bump_version.py

# Set executable permission on bump_version script
chmod +x $SW_DIR/scripts/bump_version.py
```

#### 7B — Pipeline Uncle Bob: 7 Agentes
```bash
# Install all 7 pipeline agents into .agents/agents/
mkdir -p $SW_DIR/.agents/agents

# Copy each agent
for AGENT in orchestrator specifier coder refactorer architect qa pii-verifier; do
  cp -r /home/ibernabel/.agents/agents/$AGENT $SW_DIR/.agents/agents/$AGENT
done
```

#### 7C — Workflow code-pipeline
```bash
# Install code-pipeline workflow (for /code-pipeline command)
mkdir -p $SW_DIR/.agents/workflows
cp /home/ibernabel/.agents/workflows/code-pipeline.md $SW_DIR/.agents/workflows/code-pipeline.md
```

#### 7D — CONVENTIONS.md del proyecto
```bash
# Copy CONVENTIONS template and open for project-specific configuration
cp /home/ibernabel/.agents/templates/CONVENTIONS-software.md $SW_DIR/.agents/CONVENTIONS.md
```

Después de copiar, el agente debe **editar `CONVENTIONS.md`** completando al menos:
- `project.name` con el nombre real del proyecto
- `project.pii` con `false` (o `financial` si el proyecto maneja datos financieros)
- `project.primary_stack` con las tecnologías del proyecto (si se conocen)

#### 7E — Directorio de tests Gherkin
```bash
# Create tests directory for Gherkin feature files
mkdir -p $SW_DIR/tests/features
touch $SW_DIR/tests/features/.gitkeep
```

---

### Paso 8: Vinculación de Workflows Globales vía Symlinks (Excluyendo `project-init.md`)

Los workflows globales (`repo-sync.md`, `post-session-doc.md`, `docs-and-sync.md`, `code-pipeline.md`, `domain-modeling.md`, `grilling.md`, etc.) deben instalarse en `.agents/workflows/` mediante **enlaces simbólicos (symlinks)** apuntando al almacén global `~/.agents/workflows/`.

> [!IMPORTANT]
> **Regla de Workflows Globales vs Locales:**
> 1. `project-init.md` es un **meta-workflow estrictamente global** (vive exclusivamente en `~/.agents/workflows/project-init.md`). **NUNCA** debe existir como copia local en proyectos individuales para evitar desfases de versión.
> 2. Los demás workflows globales se vinculan mediante **symlinks** para que cualquier actualización central en `~/.agents/workflows/` se propague automáticamente a todos los proyectos.
> 3. Los workflows específicos de un proyecto (ej: `deploy-zip.md`) se mantienen como archivos locales independientes.

```bash
# Link all global workflows as symlinks (and remove any local project-init.md)
python3 /home/ibernabel/.agents/scripts/install_project_skills.py --project-dir . --workflows-only
```

> **Nota:** Si se ejecutó `install_project_skills.py` en el Paso 6C sin `--no-workflows`, la vinculación de workflows ya se realizó automáticamente. En proyectos multi-vertical, ejecutar también para cada vertical `$SW_DIR`.

---

### Paso 9: Commit Inicial y Push a GitHub (Solo Modo Init)

```bash
# Stage all initialized files
git add .

# Create initial commit using Conventional Commit format
git commit -m "chore: initialize project with ASD framework v2 standards and deterministic skills"

# Push initial commit to origin main branch
git push -u origin main
```

---

## Auditoría Obligatoria Post-Ejecución

> ⚠️ **Esta sección es OBLIGATORIA y no es opcional.** El agente DEBE ejecutar estos comandos y reportar los resultados reales del sistema de archivos. No es suficiente afirmar que algo fue hecho — debe comprobarse con comandos que lean el filesystem.

### Principio de verificación

El agente NO debe confiar en su propio historial de ejecución para determinar si algo fue creado. Debe leer el filesystem con comandos independientes y reportar el estado real.

### Auditoría para dominio `software`

Ejecutar cada comando y reportar el resultado (✅ / ❌) junto con el output real:

```bash
# ── Estructura de agentes ──────────────────────────────────────────────────
echo "=== AGENTS AUDIT ===" && \
ls -la .agents/AGENTS.md 2>/dev/null && echo "✅ AGENTS.md" || echo "❌ AGENTS.md MISSING" && \
ls -la .agents/CONVENTIONS.md 2>/dev/null && echo "✅ CONVENTIONS.md" || echo "❌ CONVENTIONS.md MISSING" && \
ls .agents/agents/ 2>/dev/null && echo "✅ agents/ dir" || echo "❌ agents/ dir MISSING"

# ── Verificar los 7 agentes del pipeline ──────────────────────────────────
for agent in orchestrator specifier coder refactorer architect qa pii-verifier; do
  ls .agents/agents/$agent/agent.md 2>/dev/null \
    && echo "✅ agents/$agent/agent.md" \
    || echo "❌ agents/$agent/agent.md MISSING"
done

# ── Skills del Proyecto (Symlinks) ────────────────────────────────────────
echo "=== SKILLS AUDIT ===" && \
SKILLS_COUNT=$(ls -la .agents/skills/ 2>/dev/null | grep -E '^l' | wc -l) && \
if [ "$SKILLS_COUNT" -gt 0 ]; then
  echo "✅ $SKILLS_COUNT project skills linked in .agents/skills/"
else
  echo "❌ .agents/skills/ is empty or missing symlinks"
fi

# ── Workflows ─────────────────────────────────────────────────────────────
for wf in code-pipeline repo-sync post-session-doc; do
  ls .agents/workflows/$wf.md 2>/dev/null \
    && echo "✅ workflows/$wf.md" \
    || echo "❌ workflows/$wf.md MISSING"
done

# ── Estructura docs/ ──────────────────────────────────────────────────────
echo "=== DOCS AUDIT ===" && \
for dir in planning implementation fixes testing decisions knowledges; do
  ls -d docs/$dir 2>/dev/null \
    && echo "✅ docs/$dir/" \
    || echo "❌ docs/$dir/ MISSING"
done

# ── Archivos de software ──────────────────────────────────────────────────
echo "=== SOFTWARE FILES AUDIT ===" && \
cat VERSION 2>/dev/null && echo "✅ VERSION" || echo "❌ VERSION MISSING" && \
ls scripts/bump_version.py 2>/dev/null && echo "✅ bump_version.py" || echo "❌ bump_version.py MISSING" && \
ls tests/features/ 2>/dev/null && echo "✅ tests/features/" || echo "❌ tests/features/ MISSING" && \
ls ROADMAP.md 2>/dev/null && echo "✅ ROADMAP.md" || echo "❌ ROADMAP.md MISSING"

# ── .gitignore integridad ─────────────────────────────────────────────────
echo "=== GITIGNORE AUDIT ===" && \
if [ -f ".gitignore" ]; then
  echo "✅ .gitignore exists"
  grep -q ".codegraph" .gitignore && echo "✅ .codegraph/ entry present" || echo "⚠️  .codegraph/ entry MISSING — add manually"
  grep -q "\.env" .gitignore && echo "✅ .env entry present" || echo "⚠️  .env entry MISSING — add manually"
else
  echo "❌ .gitignore MISSING"
fi

# ── Git remote ────────────────────────────────────────────────────────────
echo "=== GIT AUDIT ===" && \
git remote -v 2>/dev/null || echo "❌ No git remote configured"
```

### Reporte final obligatorio

Al terminar la auditoría, el agente debe producir un resumen en este formato:

```
## Resultado de Auditoría — [nombre del proyecto] — [fecha]

| Item | Estado | Notas |
|------|--------|-------|
| AGENTS.md | ✅/❌ | |
| Skills Vinculadas (.agents/skills/) | ✅/❌ | Total de skills enlazadas |
| Auto-invoke Skills (AGENTS.md) | ✅/❌ | Tabla sincronizada |
| CONVENTIONS.md | ✅/❌ | |
| agents/ (7 agentes) | ✅/❌ | Listar cuáles faltan si aplica |
| workflows/ (archivos) | ✅/❌ | |
| docs/ (6 subdirectorios) | ✅/❌ | |
| VERSION | ✅/❌ | |
| scripts/bump_version.py | ✅/❌ | |
| tests/features/ | ✅/❌ | |
| ROADMAP.md | ✅/❌ | |
| .gitignore (sin sobreescritura) | ✅/❌ | |
| Git remote | ✅/❌ | |

**Items faltantes:** [lista o "Ninguno"]
**Acción requerida:** [pasos para corregir los faltantes, si los hay]
```

> Si hay ❌ en el reporte, el agente debe intentar corregirlos inmediatamente y re-ejecutar la verificación del item fallido antes de dar la tarea por completada.
