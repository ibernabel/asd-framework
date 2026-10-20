# ASD Framework

> **Agent-Driven Structured Development** — Metodología abierta de ingeniería y gobernanza para el desarrollo de software en pareja Humano-IA.

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.6.0-green.svg)](VERSION)
[![Compatibilidad Harness](https://img.shields.io/badge/harness-universal-purple.svg)](#compatibilidad-universal-con-entornos-de-ia-harnesses)

**[[English](README.md)]** · **[ Español ]**

</div>

---

ASD proporciona restricciones operativas estructuradas para agentes de codificación con IA a través de cinco dominios: **ingeniería de software**, **agentes autónomos de IA**, **administración y operaciones de negocio**, **contenido y marca personal**, y **producción de video**.

Los agentes de IA suelen oscilar entre dos extremos perjudiciales:
- **Sin restricciones**, alucinan dependencias, omiten pruebas unitarias, inflan controladores con código espagueti y envían cambios sin verificar directo a la rama `main`.
- **Con burocracia excesiva**, ahogan al desarrollador en documentos de requisitos de 20 páginas para un simple ajuste de dos líneas de CSS.

ASD reemplaza la improvisación de prompts con **pipelines de ejecución por dominio**, **puertas de calidad (*quality gates*) deterministas** y **desarrollo guiado por pruebas (TDD)**.

---

## ¿Qué es realmente ASD?

ASD **no** es una librería o runtime de software tradicional (como React, Laravel o Django). Tu aplicación nunca importa ASD en su código ni añade peso a tu bundle de producción.

En su lugar, ASD es un **framework metodológico y de gobernanza** para la ingeniería con agentes de IA—el equivalente contemporáneo de lo que *Extreme Programming (XP)* y *Agile* representaron para los equipos de software humanos:

- **Inversión de Control (IoC) para LLMs**: En un chat convencional, la IA decide arbitrariamente cómo proceder. Con ASD, el framework retiene el control del ciclo de vida. Dicta qué rol actúa (`Specifier` → `Coder` → `Refactorer` → `Architect` → `QA`), qué puertas de calidad deben superarse y qué artefactos deben generarse antes de avanzar. El agente ejecuta dentro de los límites; el framework gobierna el flujo.
- **Capa de Gobernanza y Calidad Agéntica**: Actúa como un guardián automatizado que previene los antipatrones comunes de la IA: entradas sin validar, pruebas omitidas, controladores sobrecargados, commits directos a `main` y fugas de credenciales o datos sensibles (PII).
- **Abstracción Universal de Entornos (*Multi-Harness*)**: En lugar de atar tu proyecto a una sola herramienta de IA, ASD mantiene una Fuente Única de Verdad (*SSOT*) en `.agents/` y sincroniza automáticamente puentes de configuración nativos para Antigravity, Claude Code, Cursor, Windsurf y GitHub Copilot.

---

## ¿Para quién es ASD?

### 🛠️ Para Desarrolladores Tradicionales (que programan a mano)
> *"Quiero aprovechar la velocidad de la IA, pero me niego a aceptar código espagueti sin pruebas y difícil de mantener."*

Si valoras la Arquitectura Limpia (*Clean Architecture*), los principios SOLID y las buenas prácticas de ingeniería, ASD está diseñado para ti. La IA trabaja como un desarrollador junior disciplinado bajo tu supervisión arquitectónica:
- Aplica TDD estricto: primero se escriben las pruebas unitarias que fallan, y el código de implementación solo se acepta cuando todas las pruebas pasan en verde.
- Limita la complejidad ciclomática y cognitiva (puntuación CRAP $\le 6$).
- Exige transacciones en base de datos para escrituras multitabla, validación de esquemas (Zod, Pydantic, DTOs) y tiempos de espera de red acotados ($\le 10\text{s}$).

### 🚀 Para Desarrolladores que están Comenzando a usar IA
> *"No quiero perder horas escribiendo prompts interminables ni arriesgarme a que la IA cometa errores que no sé detectar."*

No necesitas hacer malabares de *prompt engineering*. ASD te ofrece comandos intuitivos y probados en batalla:
- Solo escribe `/code-pipeline-lite <tu funcionalidad>` en tu editor con IA.
- El agente analiza el requerimiento, extrae los criterios de aceptación y **hace una pausa obligatoria para pedir tu aprobación** antes de escribir código.
- Si la IA se equivoca, las puertas de calidad automáticas detectan el error y bloquean el avance antes de que llegue a git.

### 👥 Para Equipos de Ingeniería y Tech Leads
> *"Cada desarrollador de mi equipo usa una herramienta de IA distinta, generando estilos inconsistentes y deuda técnica invisible."*

ASD establece un estándar unificado para toda tu organización:
- **Una Fuente Única de Verdad (`.agents/`)**: Las reglas del proyecto, convenciones de código y definiciones de agentes se versionan en Git junto con el proyecto.
- **Interoperabilidad Total**: Los integrantes del equipo pueden usar Claude Code, Cursor, Windsurf, Copilot o Antigravity al mismo tiempo sin discrepancias de configuración.
- **Pull Requests Listos para Auditoría**: Cada rama de trabajo atraviesa revisiones de seguridad, pruebas de regresión y verificación de datos financieros/PII antes de crear el PR.

---

## El Modelo Mental en 30 Segundos

```
    Tu Requerimiento o Idea
              │
              ▼
    [ Elegir Pipeline ]
      │             │
      │ (Complejo)  │ (Estándar / Aislado)
      ▼             ▼
/code-pipeline  /code-pipeline-lite
      │             │
      ▼             ▼
 [ Plan y Criterios de Aceptación ] ──► (Pausa para aprobación humana)
      │
      ▼
 [ Implementación TDD ] ─────────────► (Escribe test fallido, luego código mínimo)
      │
      ▼
 [ Quality Gates Automatizados ]
      ├─► UI Craft Gate (WCAG AA, sin patrones genéricos de IA)
      ├─► Backend Integrity Gate (Esquemas, transacciones, timeouts)
      └─► PII & Seguridad Gate (Auditoría de secretos, cero datos de clientes en git)
      │
      ▼
 [ Rama Git Protegida y Commit Convencional ]
```

---

## Guía Rápida Paso a Paso (De 0 a tu Primer Feature en 3 Minutos)

### Paso 1: Instalar ASD Globalmente

Instala ASD en tu entorno global (`~/.agents/`):

```bash
# Instalar todos los dominios globalmente
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash
```

*¿Deseas instalar solo dominios específicos?*
```bash
# Solo ingeniería de software
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software

# Software + Administración de Negocios
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software --domain admin
```

### Paso 2: Inicializar o Adaptar Cualquier Proyecto

Navega a la raíz de tu proyecto, abre tu entorno de desarrollo con IA (Claude Code, Cursor, Windsurf o Antigravity) y ejecuta:

```bash
/project-init
```

ASD detecta automáticamente el estado de tu espacio de trabajo y opera en uno de tres modos:
- **Modo Init** (directorio vacío): Configura Git, `.gitignore`, la jerarquía canónica `docs/`, `AGENTS.md`, `CONVENTIONS.md` y los agentes del pipeline.
- **Modo Retrofit** (proyecto existente sin ASD): Inyecta la infraestructura de gobernanza de ASD **sin alterar tu código existente ni tu historial de Git**.
- **Modo Update** (proyecto ASD existente): Actualiza agentes, habilidades y archivos puente respetando tus convenciones personalizadas.

### Paso 3: Desarrollar tu Primer Feature (Paso a Paso)

Así se ve una interacción real en el chat de tu asistente de IA:

1. **Inicias la tarea con un comando:**
   ```text
   /code-pipeline-lite Añadir endpoint para subir avatar de usuario con validación de 2MB
   ```

2. **El agente Planner analiza el requerimiento y solicita tu confirmación:**
   ```text
   [Planner] Criterios de aceptación propuestos:
   1. POST /api/user/avatar acepta únicamente archivos JPEG y PNG.
   2. Archivos mayores a 2MB devuelven HTTP 413 Payload Too Large.
   3. El tipo de archivo se valida mediante magic bytes (no solo por extensión).
   4. El avatar queda vinculado al ID del usuario autenticado.

   ¿Apruebas estos criterios antes de comenzar la implementación?
   ```

3. **Das tu visto bueno:**
   ```text
   Aprobado, procede.
   ```

4. **El agente Implementer ejecuta TDD:**
   - Crea automáticamente la rama `feature/software-avatar-upload`.
   - Escribe pruebas unitarias y de integración que cubren subidas válidas, archivos con sobrepeso y tipos MIME no permitidos.
   - Desarrolla el código mínimo para hacer pasar todas las pruebas en verde.

5. **El agente Reviewer certifica las puertas de calidad:**
   - Verifica la validación de esquemas de entrada.
   - Comprueba que no existan credenciales expuestas ni datos reales de clientes.
   - Ejecuta `verify_backend_integrity.py`.
   - Genera un commit convencional: `feat(api): add avatar upload endpoint with file size validation`.

### Paso 4: Validar con Quality Gates Automatizados

Puedes ejecutar las verificaciones de calidad manualmente en cualquier momento:

```bash
# Auditar arquitectura backend, esquemas y transacciones
python3 scripts/verify_backend_integrity.py src/

# Auditar código UI para accesibilidad y evitar patrones genéricos de IA
impeccable detect src/components/
```

### Paso 5: Sincronización Segura de Git y Documentación

Al terminar tu trabajo, actualiza la documentación persistente y el versionado con un solo comando:

```bash
# Guarda las notas de sesión en docs/ y sincroniza GitHub (SemVer, CHANGELOG, tags)
/docs-and-sync
```

---

## Modos de Ejecución por Dominio

ASD adapta dinámicamente sus niveles de rigor según lo que estés construyendo:

| Dominio | Modo | Estilo de Ejecución | Quality Gates |
|---|---|---|---|
| **Software** | Planning Mode (Estricto) | Pipeline Uncle Bob o Code Pipeline Lite; TDD Gherkin | UI craft check, backend integrity check, auditoría de seguridad, escaneo PII |
| **Agentes IA** | Planning Mode (Estricto) | Versionado de prompts, datasets de evaluación, guardrails | Suite de regresión conductual |
| **Administración** | Admin Mode | Checklists acotadas, resúmenes de entrega | Verificación financiera doble, cero datos de clientes en git |
| **Contenido y Marca** | Fast Mode | Ejecución directa, formateo por plataforma | Guías de voz de marca, revisión humanizadora |
| **Producción de Video**| Fast Mode | Guiones, listas de planos (*shot lists*), metadatos | Verificación contra plantillas, entrega directa |

---

## Cómo Elegir tu Pipeline de Software

ASD ofrece dos pipelines complementarios según la complejidad de la tarea:

### 1. Code Pipeline Lite (`/code-pipeline-lite`)
**Recomendado para**: Funcionalidades del día a día, endpoints aislados, corrección de errores, componentes de interfaz y utilidades ($\approx 80\%$ del trabajo habitual).

```
/code-pipeline-lite
      │
      ├─► 1. Planner        → Extrae criterios y casos borde (pausa para aprobación)
      ├─► 2. Implementer    → TDD: escribe pruebas primero, luego la solución
      └─► 3. Reviewer       → Audita calidad, corre quality gates, genera el commit
                │
                └─► 4. [Si pii: financial]
                    PII Verifier → Escanea en busca de datos de clientes antes del merge
```

### 2. Full Uncle Bob Pipeline (`/code-pipeline`)
**Recomendado para**: Lógica central de negocio (*core domain*), arquitecturas complejas, migraciones de base de datos críticas o refactorizaciones estructurales.

```
/code-pipeline
      │
      ├─► 1. Specifier      → Redacta especificaciones Gherkin .feature y plan de QA
      ├─► 2. Coder          → TDD: escribe pruebas fallidas primero, luego el código
      ├─► 3. Refactorer     → Elimina duplicación y asegura complejidad CRAP $\le 6$
      ├─► 4. Architect      → Pruebas de mutación, revisión de límites de arquitectura
      └─► 5. QA             → Ejecuta el plan de QA y certifica los quality gates
                │
                └─► 6. [Si pii: financial]
                    PII Verifier → Auditoría profunda contra fugas de datos
```

### Tabla de Clasificación de Cambios

| Tipo de Cambio | Cuándo Usarlo | Flujo Recomendado |
|---|---|---|
| **Funcionalidad Compleja** | Lógica central del dominio, cambios arquitectónicos mayores | `/code-pipeline` |
| **Funcionalidad Estándar** | Endpoints independientes, componentes de interfaz, workers | `/code-pipeline-lite` |
| **Corrección de Error** | Defectos, bugs de regresión | Rama + test de reproducción + fix + QA |
| **Ajuste / Docs / Chore** | Textos, estilos menores, documentación, dependencias | Rama + cambio directo + verificación |

---

## Los 10 Agentes del Pipeline

Ubicados en `.agents/agents/` y orquestados automáticamente según el comando:

| Agente | Alcance | Responsabilidad Principal |
|---|---|---|
| `orchestrator` | Pipeline | Coordina la ejecución secuencial de los flujos multiagente. |
| `planner` | Lite Pipeline | Convierte requerimientos libres en criterios de aceptación claros y revisables. |
| `implementer` | Lite Pipeline | Implementa los criterios aprobados mediante pruebas unitarias y código limpio. |
| `reviewer` | Lite Pipeline | Revisa calidad, audita seguridad y valida las puertas de certificación. |
| `specifier` | Full Pipeline | Redacta criterios formales en Gherkin y procedimientos de prueba para QA. |
| `coder` | Full Pipeline | Escribe pruebas fallidas primero, luego el código mínimo para superarlas. |
| `refactorer` | Full Pipeline | Elimina código redundante y mantiene la complejidad CRAP $\le 6$. |
| `architect` | Full Pipeline | Ejecuta pruebas de mutación, revisa límites de módulos y cobertura. |
| `qa` | Full Pipeline | Ejecuta procedimientos de QA, audita seguridad y certifica calidad. |
| `pii-verifier` | Full / Lite / Direct | Escanea código, fixtures y consultas en busca de credenciales y datos privados. |

---

## Quality Gates Automatizados

ASD sustituye las revisiones subjetivas por verificaciones deterministas ejecutables por script:

### 1. UI Craft Gate (`impeccable`)
- **Reglas de diseño**: Los agentes consultan `/frontend-design` y la especificación *Craft Floor*. Prohíbe vicios comunes de la IA: textos con degradados innecesarios, tarjetas repetitivas sin función y estilos hardcodeados en HTML.
- **Verificación**: `impeccable detect <archivos>`.
- **Estándares**: Contraste WCAG AA ($\ge 4.5:1$ en texto normal / $\ge 3:1$ en texto grande), áreas táctiles mínimas de $44\times 44\text{px}$, diseño responsive verificado en 390px y pantallas de escritorio, y estados visibles de carga, vacío y error.
- **Bloqueo**: Cualquier defecto primario detiene la aprobación de QA.

### 2. Backend Integrity Gate (`backend-integrity`)
- **Reglas de diseño**: Los agentes aplican `/backend-integrity` y el estándar *Backend Floor*.
- **Comprobaciones principales**:
  1. **Validación de Esquemas**: Cuerpos y parámetros de petición deben validarse con esquemas tipados (Zod, Pydantic, DTOs) antes de llegar a la lógica de negocio.
  2. **Transacciones Atómicas**: Operaciones que muten dos o más tablas deben ejecutarse dentro de una transacción explícita (`db.transaction()`).
  3. **Timeouts Obligatorios**: Toda llamada de red externa debe definir un límite de tiempo ($\le 10\text{s}$).
  4. **Paginación Requerida**: Se prohíben consultas masivas de colecciones sin paginar.
  5. **Aislamiento de Capas**: Los controladores solo gestionan transporte HTTP; la lógica de negocio reside en servicios de dominio.
  6. **Manejo Estructurado de Errores**: Se prohíbe silenciar excepciones (`except: pass`); cada error mapea a códigos de estado HTTP explícitos.
- **Verificación**: `python3 scripts/verify_backend_integrity.py <archivos>`.
- **Bloqueo**: Código de salida 2 impide la aprobación de QA o Reviewer.

### 3. Puerta de Privacidad y PII (`pii-verifier`)
- Se activa automáticamente al declarar `pii: financial` en `CONVENTIONS.md`.
- Inspecciona esquemas de base de datos antes de consultar, excluyendo columnas de identidad o datos bancarios del alcance del agente.

---

## Comandos Principales y Meta-Habilidades

Centralizados en `~/.agents/skills/` y disponibles globalmente en tus proyectos:

| Comando / Skill | Ámbito | Descripción |
|---|---|---|
| `/project-init` | Global | Inicializa, adapta (*retrofit*) o actualiza la estructura, docs y skills de ASD. |
| `/code-pipeline` | Proyecto | Ejecuta el pipeline Uncle Bob completo (Specifier → Coder → Refactorer → Architect → QA). |
| `/code-pipeline-lite` | Proyecto | Ejecuta el pipeline ágil de 3 etapas (Planner → Implementer → Reviewer). |
| `/backend-integrity` | Proyecto / Global | Audita código backend contra reglas de arquitectura, esquemas y transacciones. |
| `/humanizer` | Proyecto / Global | Elimina patrones artificiales de redacción generada por IA en contenidos. |
| `/repo-sync` | Proyecto | Incrementa versión SemVer, actualiza CHANGELOG, hace commit, tag y push seguro. |
| `/post-session-doc` | Proyecto | Consolida notas y entregables de la sesión en la jerarquía canónica `docs/`. |
| `/docs-and-sync` | Proyecto | Ejecuta consecutivamente `/post-session-doc` seguido de `/repo-sync`. |
| `/domain-modeling` | Proyecto | Construye el lenguaje ubicuo, contextos delimitados y borradores de ADR. |
| `/grilling` | Proyecto | Entrevista interactiva para poner a prueba decisiones de arquitectura antes de codificar. |
| `/ask-the-council` | Proyecto | Deliberación multiagente con 5 perfiles asesores y un coordinador imparcial. |
| `/wizard-of-oz-mode` | Proyecto | Simula automatizaciones complejas con fachada manual para validar ideas rápido. |

---

## Estructura Canónica del Proyecto (SSOT)

Al ejecutar `/project-init` en un proyecto de software, se genera esta estructura:

```
mi-proyecto/
├── .agents/                        ← Fuente Única de Verdad Canónica de ASD (SSOT)
│   ├── AGENTS.md                   ← Reglas de agentes y tabla de auto-invocación
│   ├── CONVENTIONS.md              ← Stack tecnológico, reglas Git y banderas PII
│   ├── agents/                     ← Definiciones de los 10 agentes del pipeline
│   │   ├── orchestrator/
│   │   ├── planner/
│   │   ├── implementer/
│   │   ├── reviewer/
│   │   ├── specifier/
│   │   ├── coder/
│   │   ├── refactorer/
│   │   ├── architect/
│   │   ├── qa/
│   │   └── pii-verifier/
│   └── skills/                     ← Copias físicas de las habilidades del proyecto
│       ├── code-pipeline/
│       ├── code-pipeline-lite/
│       ├── backend-integrity/
│       ├── humanizer/
│       ├── repo-sync/
│       ├── post-session-doc/
│       └── docs-and-sync/
├── AGENTS.md                       ← Manifiesto raíz (Estándar Abierto / Codex / ChatGPT)
├── CLAUDE.md                       ← Punto de entrada para Claude Code
├── .claude/
│   └── commands/                   ← Slash commands nativos de Claude Code
├── .cursorrules                    ← Reglas para versiones anteriores de Cursor
├── .cursor/
│   └── rules/
│       └── asd-framework.mdc       ← Cursor Rules 2.0 moderno (alwaysApply: true)
├── .windsurfrules                  ← Reglas para Codeium Windsurf Cascade
├── .github/
│   └── copilot-instructions.md     ← Reglas para GitHub Copilot Chat y Workspace
├── docs/                           ← Repositorio Canónico de Documentación
│   ├── README.md                   ← Índice de documentación
│   ├── planning/                   ← PRD, historias de usuario, lenguaje ubicuo
│   ├── implementation/             ← Especificaciones de fases y funcionalidades
│   ├── testing/                    ← Planes de prueba de QA, reportes, specs Gherkin
│   ├── decisions/                  ← Registros de Decisiones de Arquitectura (ADRs)
│   ├── fixes/                      ← Registro de correcciones de bugs
│   └── knowledges/                 ← Patrones aprendidos y problemas conocidos
├── tests/                          ← Pruebas unitarias, integración y aceptación
└── README.md
```

---

## Compatibilidad Universal con Entornos de IA (Harnesses)

ASD no depende de una sola herramienta. Mientras que las reglas canónicas residen en `.agents/`, el framework genera y sincroniza configuraciones nativas para los principales entornos de IA:

| Entorno / Asistente IA | Estado | Mecanismo de Integración | Capacidades Clave |
|---|:---:|---|---|
| **Google Antigravity** | Soportado (Principal) | Estructura nativa `.agents/` y subagentes | Pipeline Uncle Bob completo, skills y slash commands |
| **Claude Code** (`claude` CLI) | Soportado | `CLAUDE.md` + `.claude/commands/` | Memoria de proyecto y slash commands nativos (`/code-pipeline`, etc.) |
| **OpenAI Codex y Estándar Abierto** | Soportado | Manifiesto raíz `AGENTS.md` | Cumple el estándar abierto AGENTS.md (ChatGPT, Codex, Aider) |
| **Cursor** | Soportado | `.cursorrules` y `.cursor/rules/asd-framework.mdc` | Modo dual: reglas clásicas y Cursor Rules 2.0 (`alwaysApply: true`) |
| **Windsurf** (Codeium) | Soportado | `.windsurfrules` | Reglas de flujo Cascade, política de ramas y quality gates |
| **GitHub Copilot** | Soportado | `.github/copilot-instructions.md` | Cumplimiento de gates en Copilot Chat y Workspace |
| **WSL Ubuntu 22.04** | Nativo | Ejecución transparente en WSL mediante wrappers | Compatibilidad multiplataforma completa en Windows |

### Validar Compatibilidad de Entornos

Comprueba la preparación de tu proyecto en todos los entornos con un solo comando:

```bash
# Validar compatibilidad en todos los asistentes soportados
python3 scripts/harness_adapter.py --validate --project-dir .

# Instalar o sincronizar puentes faltantes sin sobreescribir tus reglas
python3 scripts/harness_adapter.py --project-dir .
```

---

## Ecosistema de Skills y Registros

ASD permite descubrir, instalar y gestionar habilidades desde los registros documentados en [SKILL_REGISTRIES.md](SKILL_REGISTRIES.md):

- **[Skills Marketplace (SkillsMP)](https://skillsmp.com)**: Catálogo público de habilidades de agentes accesible vía API REST (`SKILLSMP_API_KEY`).
- **[Paul Bakaus Impeccable](https://github.com/pbakaus/impeccable)**: Criterios de diseño visual, accesibilidad WCAG y escáner automático de defectos UI (`impeccable detect`).
- **[Antigravity Skills](https://github.com/rmyndharis/antigravity-skills)**: Habilidades para backend, sistemas distribuidos y DevOps.
- **[Skills.md](https://skills.md)**: Herramientas para automatización de repositorios y flujos de contenido.
- **[Habilidades de Matt Pocock](https://github.com/mattpocock/skills)**: Habilidades para `grilling`, `domain-modeling`, `to-spec`, `refactor` y `prototype`.
- **[Habilidades Oficiales de Anthropic](https://github.com/anthropics/skills)**: Patrones de diseño ergonómico y frontend (`frontend-design`).
- **[Cathy Kim SemVer](https://github.com/cathy-kim/skill-semver)**: Estándares SemVer y automatización de versiones.

```bash
# Buscar habilidades en los registros conectados
python3 scripts/skill_registry.py search "fastapi"

# Instalar una habilidad en tu ecosistema
python3 scripts/skill_registry.py install "fastapi"
```

---

## Preguntas Frecuentes (FAQ)

### ¿ASD hace más lento el desarrollo con IA?
**No, lo acelera de forma medible.** Sin ASD, la IA genera código rápidamente que luego toma horas depurar, refactorizar y probar a mano. Al atrapar casos borde, exigir TDD y verificar con puertas automáticas desde el inicio, ASD elimina el 80% del tiempo perdido arreglando regresiones causadas por la IA.

### ¿Puedo incorporar ASD en un proyecto existente sin romperlo?
**Sí.** Al ejecutar `/project-init` en un repositorio existente, el framework se activa en **Modo Retrofit**. Esto inyecta la carpeta `.agents/` y los puentes de configuración sin tocar una sola línea de tu código de aplicación ni alterar tu historial de Git.

### ¿Todos en el equipo deben usar el mismo asistente o editor de IA?
**No.** Esa es la ventaja fundamental de la arquitectura Multi-Harness de ASD. Un desarrollador puede usar Claude Code en la terminal, otro Cursor, otro Windsurf y otro Antigravity. Como todos comparten la Fuente Única de Verdad en `.agents/`, el asistente de cada desarrollador respeta exactamente las mismas convenciones y quality gates.

### ¿Qué lenguajes y frameworks soporta ASD?
ASD es agnóstico del stack tecnológico. Funciona de inmediato con TypeScript/JavaScript, Python, Go, Rust, PHP/Laravel, Java, C# y Ruby. Las puertas de calidad se adaptan al framework de pruebas que uses en tu proyecto (Vitest, Jest, PyTest, PHPUnit, Cargo test) y a tus librerías de validación de esquemas.

---

## Licencia

Licencia MIT © [Idequel Bernabel](https://github.com/ibernabel).

Las habilidades comunitarias de [Matt Pocock](https://github.com/mattpocock/skills) y otros colaboradores de código abierto están sujetas a sus respectivas licencias.
