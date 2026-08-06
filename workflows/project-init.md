---
description: Inicializar un nuevo proyecto configurando Git, GitHub (privado), marco ASD v2, docs/, .agents/, AGENTS.md, CONVENTIONS.md, workflows, agentes del pipeline y versionado.
user-invocable: true
---

# Workflow: Project Initialization (`project-init`)

## Descripción

Este workflow automatiza la inicialización de cualquier directorio como un proyecto estructurado bajo los estándares del desarrollador (Idequel Bernabel) y el **Framework ASD v2**.

Soporta proyectos de dominio único y proyectos **multi-vertical** (ej: Consultor con verticales `admin`, `technology`, `content`). Configura Git, GitHub privado, `.gitignore`, jerarquía `docs/`, reglas de agente por dominio, y para proyectos de software instala el pipeline Uncle Bob completo (7 agentes + workflows).

---

## Dominios de Proyecto Disponibles

El proyecto debe clasificarse en una de las 5 categorías para aplicar la plantilla adecuada desde `/home/ibernabel/.agents/templates/`:

| Dominio | Plantilla | Modo | Aplica para |
|---------|-----------|------|-------------|
| `software` | `software-dev-agents.md` | Planning Mode (Strict) | APIs, web apps, CLIs, servicios backend/frontend |
| `admin` | `business-admin-agents.md` | Admin Mode | Gestión de clientes, facturación, contratos, CRM |
| `ai-agent` | `ai-agents-agents.md` | Planning Mode | Agentes LLM, RAG, chatbots, pipelines de IA |
| `content` | `content-brand-agents.md` | Fast Mode | Redes sociales, blogs, newsletters, marca personal |
| `video` | `video-production-agents.md` | Fast Mode | YouTube, Shorts, Reels, guiones, postproducción |

---

## Modos de Operación

El agente detecta automáticamente el modo correcto según el estado del directorio:

| Condición detectada | Modo | Comportamiento |
|---------------------|------|----------------|
| Sin `.git/` | **Init** (normal) | Flujo completo: GitHub, Git init, docs, AGENTS.md, etc. |
| `.git/` existe, sin `.agents/` | **Retrofit** | Solo inyecta infraestructura ASD. No toca código ni Git. |
| `.git/` existe + `.agents/` existe | **Update** | Solo actualiza lo que falta o está desactualizado. |

```bash
# Auto-detection logic
if [ ! -d ".git" ]; then MODE="init"
elif [ ! -d ".agents" ]; then MODE="retrofit"
else MODE="update"; fi
echo "Detected mode: $MODE"
```

### ⚡ Modo Retrofit (Proyectos Existentes: Lender, Consultor, Lamas, etc.)

Usado cuando el proyecto ya tiene código activo, commits y estructura. **No se modifica nada existente.**

**Pasos que se SALTAN en modo retrofit:**
- Paso 2 (GitHub + Git init) — el repo ya existe
- `.gitignore` — si ya existe, no se sobreescribe (se muestra diff de qué añadir manualmente)
- `README.md` — no se sobreescribe si ya existe

**Pasos que SÍ se ejecutan en modo retrofit:**
- Skill Inventory Check (Paso 1B)
- Detección de verticales (Paso 1, punto 3-4)
- Creación de `docs/` y subcarpetas faltantes (sin tocar los existentes)
- Paso 6A/6B: `.agents/AGENTS.md` por dominio/vertical
- Paso 7 completo (si dominio = software): agentes, CONVENTIONS.md, code-pipeline, tests/
- Paso 8: workflows

---

## Pasos de Ejecución del Agente

### Paso 1: Determinación de Nombre, Dominio y Verticales

1. Leer el nombre del directorio actual o consultar al usuario el nombre deseado.
2. Si el usuario no especificó el dominio, solicitar la selección de uno de los 5 dominios.
3. **Detección multi-vertical:** Verificar si el directorio actual contiene subdirectorios que puedan ser verticales de trabajo:

```bash
# Detect potential vertical subdirectories (non-hidden, non-standard dirs)
ls -d */ 2>/dev/null | grep -vE '^(node_modules|\.git|dist|build|__pycache__|\.venv)/$'
```

4. Si se detectan subdirectorios, preguntar al usuario:
   - ¿Este proyecto tiene múltiples verticales? (ej: `admin/`, `technology/`, `content/`)
   - Para cada subdirectorio relevante: ¿qué dominio ASD aplica? (software / admin / ai-agent / content / video)
   - Guardar el mapa de verticales → dominios para usar en el Paso 6B.

---

### Paso 1B: Skill Inventory Check

Antes de configurar el proyecto, el agente verifica que las skills requeridas por el dominio seleccionado están instaladas globalmente.

```bash
# List all installed global skills
ls /home/ibernabel/.agents/skills/
```

#### Skills requeridas por dominio

| Dominio | Skills esenciales a verificar |
|---------|-------------------------------|
| `software` | `tdd`, `typescript`, `commit`, `code-review`, `diagnosing-bugs`, `playwright`, `pytest`, `react-19`, `nextjs-15`, `zod-4` |
| `admin` | `invoice-generator`, `proposal-writer`, `contract-drafter`, `client-crm-workflow`, `project-estimator` |
| `ai-agent` | `langchain`, `langgraph`, `prompt-engineering`, `autonomous-agents`, `langfuse` |
| `content` | `social-media-writer`, `content-calendar`, `hook-writer`, `seo-copywriter`, `brand-voice-enforcer` |
| `video` | `video-script-writer`, `shot-list-generator`, `thumbnail-designer`, `video-seo`, `subtitle-generator` |

Si alguna skill requerida **no está instalada**, el agente avisa:
```
⚠️  Skill 'tdd' no encontrada en ~/.agents/skills/
    Para instalarla: buscar en el repositorio de skills de Matt Pocock
    o crearla con /skill-creator
```

#### Verificación de Matt Pocock's Skills

Para cualquier dominio, verificar también la presencia de las skills de Matt Pocock que potencian el flujo ASD:
```bash
# Check key Matt Pocock skills
for skill in grill-with-docs grilling domain-modeling brainstorming implement refactor to-spec; do
  [ -d "/home/ibernabel/.agents/skills/$skill" ] && echo "✅ $skill" || echo "⚠️  $skill (not found)"
done
```

Si no están instaladas, sugerir: `setup-matt-pocock-skills` skill o ver https://github.com/mattpocock/skills

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

### Paso 3: Generación de `.gitignore`

Crear `.gitignore` copiando la plantilla adecuada desde `/home/ibernabel/.agents/templates/gitignore/`:
- `software` → `gitignore_software.txt`
- `admin` → `gitignore_admin.txt`
- Otros dominios → `gitignore_general.txt`

Para proyectos multi-vertical, usar la plantilla del dominio raíz (dominio primario del proyecto).

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

   **Ejemplo para Consultor:**
   ```bash
   # admin vertical
   mkdir -p admin/.agents
   cp /home/ibernabel/.agents/templates/business-admin-agents.md admin/.agents/AGENTS.md

   # technology vertical (software domain)
   mkdir -p technology/.agents
   cp /home/ibernabel/.agents/templates/software-dev-agents.md technology/.agents/AGENTS.md

   # content vertical
   mkdir -p content/.agents
   cp /home/ibernabel/.agents/templates/content-brand-agents.md content/.agents/AGENTS.md
   ```

3. Las verticales de dominio `software` requieren el Paso 7 (pipeline completo) aplicado a su subdirectorio.

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

### Paso 8: Copia de Workflows Globales (`repo-sync` & `post-session-doc`)

```bash
# Copy global workflows to project .agents/workflows/
mkdir -p .agents/workflows
cp /home/ibernabel/.agents/workflows/repo-sync.md .agents/workflows/repo-sync.md
cp /home/ibernabel/.agents/workflows/post-session-doc.md .agents/workflows/post-session-doc.md
```

> **Nota:** Si el proyecto es multi-vertical con una vertical de software, copiar también estos workflows al `$SW_DIR/.agents/workflows/` de esa vertical.

---

### Paso 9: Commit Inicial y Push a GitHub

```bash
# Stage all initialized files
git add .

# Create initial commit using Conventional Commit format
git commit -m "chore: initialize project with ASD framework v2 standards"

# Push initial commit to origin main branch
git push -u origin main
```

---

## Verificación Post-Inicialización

```bash
# Verify git status and project structure
git status && tree -L 3 .
```

### Checklist de verificación para dominio `software`

- [ ] `.agents/AGENTS.md` existe y es `software-dev-agents.md`
- [ ] `.agents/CONVENTIONS.md` existe con `project.name` y `project.pii` completados
- [ ] `.agents/agents/` contiene los 7 agentes del pipeline
- [ ] `.agents/workflows/code-pipeline.md` existe
- [ ] `.agents/workflows/repo-sync.md` existe
- [ ] `.agents/workflows/post-session-doc.md` existe
- [ ] `docs/` tiene todas las subcarpetas (planning, implementation, fixes, testing, decisions, knowledges)
- [ ] `ROADMAP.md` tiene secciones de DDD (Domain Model, Bounded Contexts, Ubiquitous Language)
- [ ] `VERSION` contiene `0.1.0`
- [ ] `scripts/bump_version.py` existe y tiene permisos de ejecución
- [ ] `tests/features/` existe para archivos Gherkin
- [ ] Repositorio GitHub privado creado y conectado
- [ ] Commit inicial hecho con mensaje `chore: initialize project with ASD framework v2 standards`
