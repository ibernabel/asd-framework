# ASD Framework

> Agent-Driven Structured Development (ASD): disciplina de ingeniería y límites operativos para el desarrollo de software en pareja Humano-IA.

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.6.0-green.svg)](VERSION)
[![Compatibilidad](https://img.shields.io/badge/harness-universal-purple.svg)](#compatibilidad-con-entornos-de-ia)

[English](README.md) · [Español](README.es.md)

</div>

---

ASD establece límites operativos prácticos para agentes de código con IA en cinco dominios: ingeniería de software, agentes autónomos, operaciones de negocio, contenido y producción de video.

Por su cuenta, los agentes de código suelen alucinar importaciones, saltarse pruebas unitarias, llenar controladores con lógica de negocio y subir cambios sin verificar directo a `main`. Pero exigirles un documento de requisitos de 20 páginas para cambiar dos líneas de CSS es igual de ineficiente.

ASD equilibra velocidad y rigor mediante pipelines por dominio, comprobaciones automatizadas y ramas protegidas.

---

## ¿Qué es ASD?

ASD es una metodología de trabajo y una capa de gobernanza, no una librería que instalas dentro del código de tu aplicación. Tu producto en producción nunca interactúa con ASD; existe únicamente para mantener la disciplina de tus asistentes de IA al programar.

Aplica tres principios concretos al trabajo diario:

- **Inversión de control para agentes**: En un chat ordinario, el modelo decide qué hacer a continuación. Con ASD, el framework marca los pasos (`Specifier` → `Coder` → `Refactorer` → `Architect` → `QA`), hace pausas para pedir aprobación humana y exige pruebas en verde antes de seguir. El agente escribe el código, pero el flujo controla el ciclo de vida.
- **Quality gates automatizados**: Comprobaciones por script detectan problemas antes de que lleguen a git: falta de validación de esquemas, consultas sin paginar, escrituras en varias tablas sin transacciones, credenciales expuestas y problemas de contraste en interfaz.
- **Sincronización universal de entornos**: Mantienes tus reglas en un solo lugar (`.agents/`). ASD genera y actualiza automáticamente los archivos de configuración para Antigravity, Claude Code, Cursor, Windsurf y GitHub Copilot para que todo el equipo trabaje con las mismas normas.

---

## ¿Para quién es?

### Desarrolladores que programan con rigor a mano
Si aplicas TDD, sigues Clean Architecture y cuidas la mantenibilidad, habrás visto a modelos de IA destrozar bases de código con atajos descuidados. ASD convierte al agente en un desarrollador junior disciplinado: escribe pruebas primero, respeta las capas de la arquitectura, valida esquemas y mantiene la complejidad ciclomática bajo control (puntuación CRAP $\le 6$).

### Desarrolladores que empiezan a usar IA
No necesitas prompts de 50 líneas ni trucos complicados. Ejecutas `/code-pipeline-lite`, revisas el plan conciso que propone el agente, lo apruebas y dejas que implemente la funcionalidad contra pruebas automáticas. Si el agente comete un error, los quality gates lo rechazan antes de que toque git.

### Equipos de ingeniería y tech leads
En un mismo equipo cada quien suele tener preferencias distintas: uno usa Cursor, otro Claude Code en la terminal y otro Windsurf o Copilot. ASD centraliza las convenciones de código, reglas de ramas y definiciones de agentes en `.agents/`, sincronizando los archivos nativos de cada editor para que la calidad de los pull requests sea uniforme.

---

## El flujo de trabajo en 30 segundos

```
       Requerimiento o idea
                 │
                 ▼
        [ Elegir pipeline ]
         │               │
         │ (Complejo)    │ (Estándar / Aislado)
         ▼               ▼
  /code-pipeline   /code-pipeline-lite
         │               │
         ▼               ▼
    [ Plan y criterios de aceptación ] ──► Pausa para tu aprobación
         │
         ▼
    [ Implementación TDD ] ──────────────► Prueba fallida primero, luego código mínimo
         │
         ▼
    [ Quality gates automatizados ]
         ├─► UI craft gate (WCAG AA, sin estilos genéricos de IA)
         ├─► Backend integrity gate (Esquemas, transacciones, timeouts)
         └─► PII y seguridad (Auditoría de secretos, sin datos de clientes en git)
         │
         ▼
    [ Rama git dedicada y commit convencional ]
```

---

## Guía rápida: de cero a tu primer feature

### 1. Instalar ASD globalmente

Instala ASD en tu entorno global (`~/.agents/`):

```bash
# Instalar todos los dominios
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash
```

Para instalar únicamente dominios específicos:

```bash
# Solo ingeniería de software
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software

# Software + Administración de negocios
curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash -s -- --domain software --domain admin
```

### 2. Inicializar o adaptar un proyecto

Abre tu entorno de desarrollo con IA (Claude Code, Cursor, Windsurf o Antigravity) en la carpeta de tu proyecto y ejecuta:

```bash
/project-init
```

ASD analiza tu espacio de trabajo y actúa según el estado:
- **Modo Init** (directorio vacío): Crea git, `.gitignore`, la estructura canónica `docs/`, `AGENTS.md`, `CONVENTIONS.md` y los agentes del pipeline.
- **Modo Retrofit** (proyecto existente): Añade los archivos de gobernanza de ASD sin modificar tu código fuente ni tu historial de git.
- **Modo Update** (proyecto ASD existente): Actualiza agentes, skills y puentes respetando tus convenciones personalizadas.

### 3. Crear una funcionalidad paso a paso

Así se desarrolla una tarea típica:

1. **Inicias la tarea:**
   ```text
   /code-pipeline-lite Añadir endpoint para subir avatar con validación de 2MB
   ```

2. **El agente Planner extrae criterios y solicita tu aprobación:**
   ```text
   [Planner] Criterios de aceptación propuestos:
   1. POST /api/user/avatar acepta solo archivos JPEG y PNG.
   2. Archivos mayores a 2MB devuelven 413 Payload Too Large.
   3. Se valida el contenido mediante magic bytes (no solo extensión).
   4. El archivo guardado se vincula al ID del usuario autenticado.

   ¿Apruebas estos criterios antes de comenzar la implementación?
   ```

3. **Revisas y apruebas:**
   ```text
   Aprobado, procede.
   ```

4. **El agente Implementer escribe pruebas y código:**
   - Abre una rama dedicada (`feature/software-avatar-upload`).
   - Escribe pruebas unitarias y de integración para subidas válidas, archivos pesados y formatos inválidos.
   - Escribe la lógica mínima del endpoint hasta que todas las pruebas pasen en verde.

5. **El agente Reviewer certifica los quality gates:**
   - Comprueba la validación de esquemas.
   - Confirma que no haya secretos ni datos de clientes.
   - Ejecuta `verify_backend_integrity.py`.
   - Genera un commit convencional: `feat(api): add avatar upload endpoint with file size validation`.

### 4. Ejecutar quality gates manualmente

Puedes ejecutar las comprobaciones en cualquier momento:

```bash
# Auditar arquitectura backend, esquemas y transacciones
python3 scripts/verify_backend_integrity.py src/

# Auditar código UI contra defectos de accesibilidad
impeccable detect src/components/
```

### 5. Sincronizar documentación y versiones

Al terminar tu trabajo, actualiza la documentación y las etiquetas de versión:

```bash
# Guarda las notas en docs/ y sincroniza GitHub (SemVer, CHANGELOG, tags)
/docs-and-sync
```

---

## Modos de ejecución por dominio

ASD ajusta su proceso según el tipo de trabajo:

| Dominio | Modo | Estilo de ejecución | Quality gates |
|---|---|---|---|
| **Software** | Planning Mode (Estricto) | Pipeline Uncle Bob o Code Pipeline Lite; TDD Gherkin | UI craft check, backend integrity check, auditoría de seguridad, escaneo PII |
| **Agentes IA** | Planning Mode (Estricto) | Versionado de prompts, datasets de evaluación, guardrails | Suite de regresión conductual |
| **Administración** | Admin Mode | Checklists acotadas, resúmenes de entrega | Doble verificación financiera, cero datos de clientes en git |
| **Contenido y marca** | Fast Mode | Ejecución directa, formato por plataforma | Guía de voz de marca, revisión humanizadora |
| **Producción de video**| Fast Mode | Guiones, listas de planos, metadatos | Verificación con plantillas, entrega directa |

---

## Cómo elegir tu pipeline de software

ASD incluye dos pipelines según el alcance del cambio:

### 1. Code Pipeline Lite (`/code-pipeline-lite`)
Para el trabajo diario: endpoints aislados, corrección de errores, componentes de interfaz y funciones auxiliares (la gran mayoría de tareas).

```
/code-pipeline-lite
      │
      ├─► 1. Planner        → Extrae criterios y casos borde (pausa para aprobación)
      ├─► 2. Implementer    → TDD: escribe pruebas primero, luego la solución
      └─► 3. Reviewer       → Audita código, corre quality gates, genera el commit
                │
                └─► 4. [Si pii: financial]
                    PII Verifier → Escanea datos de clientes antes del merge
```

### 2. Full Uncle Bob Pipeline (`/code-pipeline`)
Para lógica central de negocio, migraciones de base de datos multitabla, servicios complejos y cambios arquitectónicos de fondo.

```
/code-pipeline
      │
      ├─► 1. Specifier      → Redacta especificaciones Gherkin .feature y plan de QA
      ├─► 2. Coder          → TDD: escribe pruebas fallidas primero, luego el código
      ├─► 3. Refactorer     → Elimina duplicación y asegura complejidad CRAP $\le 6$
      ├─► 4. Architect      → Pruebas de mutación, revisión de límites modulares
      └─► 5. QA             → Ejecuta el plan de QA y certifica quality gates
                │
                └─► 6. [Si pii: financial]
                    PII Verifier → Auditoría profunda contra fugas de datos
```

### Clasificación de cambios

| Tipo de cambio | Cuándo usarlo | Flujo recomendado |
|---|---|---|
| **Funcionalidad compleja** | Lógica central del dominio, límites arquitectónicos nuevos | `/code-pipeline` |
| **Funcionalidad estándar** | Endpoints independientes, componentes de interfaz, workers | `/code-pipeline-lite` |
| **Corrección de error** | Defectos, bugs de regresión | Rama + test de reproducción + fix + QA |
| **Mantenimiento / Docs** | Dependencias, documentación, ajustes menores de estilo | Rama + cambio directo + verificación |

---

## Los 10 agentes del pipeline

Definidos en `.agents/agents/` y orquestados por los comandos del pipeline:

| Agente | Alcance | Responsabilidad principal |
|---|---|---|
| `orchestrator` | Pipeline | Coordina la ejecución secuencial de los flujos multiagente. |
| `planner` | Lite Pipeline | Convierte requerimientos en criterios de aceptación claros y revisables. |
| `implementer` | Lite Pipeline | Implementa los criterios aprobados mediante pruebas unitarias y código limpio. |
| `reviewer` | Lite Pipeline | Revisa calidad, audita seguridad y valida puertas de certificación. |
| `specifier` | Full Pipeline | Redacta criterios formales en Gherkin y procedimientos de prueba para QA. |
| `coder` | Full Pipeline | Escribe pruebas fallidas primero, luego el código mínimo para superarlas. |
| `refactorer` | Full Pipeline | Elimina código redundante y mantiene la complejidad CRAP $\le 6$. |
| `architect` | Full Pipeline | Ejecuta pruebas de mutación, revisa límites de módulos y cobertura. |
| `qa` | Full Pipeline | Ejecuta procedimientos de QA, audita seguridad y certifica calidad. |
| `pii-verifier` | Full / Lite / Direct | Escanea código, fixtures y consultas en busca de credenciales y datos privados. |

---

## Quality gates automatizados

ASD utiliza verificaciones deterministas por script en lugar de revisiones subjetivas:

### 1. UI craft gate (`impeccable`)
- **Reglas**: Los agentes siguen `/frontend-design` y las directrices de Craft Floor. Prohíbe patrones típicos de IA: degradados innecesarios en texto, insignias decorativas, cuadrículas de tarjetas repetitivas y estilos en línea en el marcado.
- **Verificación**: `impeccable detect <archivos>`.
- **Estándares**: Contraste WCAG AA ($\ge 4.5:1$ texto normal / $\ge 3:1$ texto grande), áreas táctiles mínimas de $44\times 44\text{px}$, diseño responsive verificado en 390px y pantallas de escritorio, y estados visibles de carga, vacío y error.
- **Bloqueo**: Cualquier defecto primario detiene la aprobación de QA.

### 2. Backend integrity gate (`backend-integrity`)
- **Reglas**: Los agentes aplican `/backend-integrity` y el estándar Backend Floor.
- **Comprobaciones principales**:
  1. Validación de esquemas: Cuerpos y parámetros de petición deben validarse con esquemas tipados (Zod, Pydantic, DTOs) antes de llegar a la lógica de negocio.
  2. Transacciones atómicas: Operaciones que muten dos o más tablas deben ejecutarse dentro de una transacción explícita (`db.transaction()`).
  3. Timeouts obligatorios: Toda llamada de red externa debe definir un límite de tiempo ($\le 10\text{s}$).
  4. Paginación obligatoria: Las consultas de colecciones deben estar paginadas.
  5. Aislamiento de capas: Los controladores gestionan transporte HTTP; la lógica de negocio reside en servicios de dominio.
  6. Manejo estructurado de errores: Se prohíbe silenciar excepciones (`except: pass`); cada error mapea a códigos de estado HTTP explícitos.
- **Verificación**: `python3 scripts/verify_backend_integrity.py <archivos>`.
- **Bloqueo**: Código de salida 2 impide la aprobación de QA o Reviewer.

### 3. Puerta de privacidad y PII (`pii-verifier`)
- Se activa automáticamente al declarar `pii: financial` en `CONVENTIONS.md`.
- Inspecciona esquemas de base de datos antes de consultar, excluyendo columnas de identidad o datos bancarios del alcance del agente.

---

## Comandos principales y meta-skills

Centralizados en `~/.agents/skills/` y disponibles en todos tus proyectos:

| Comando / Skill | Ámbito | Descripción |
|---|---|---|
| `/project-init` | Global | Inicializa, adapta (*retrofit*) o actualiza la estructura, docs y skills de ASD. |
| `/code-pipeline` | Proyecto | Ejecuta el pipeline Uncle Bob completo (Specifier → Coder → Refactorer → Architect → QA). |
| `/code-pipeline-lite` | Proyecto | Ejecuta el pipeline ágil de 3 etapas (Planner → Implementer → Reviewer). |
| `/backend-integrity` | Proyecto / Global | Audita código backend contra reglas de arquitectura, esquemas y transacciones. |
| `/humanizer` | Proyecto / Global | Elimina patrones artificiales de redacción generada por IA en contenidos. |
| `/repo-sync` | Proyecto | Incrementa versión SemVer, actualiza CHANGELOG, hace commit, tag y push seguro. |
| `/post-session-doc` | Proyecto | Guarda notas y entregables de la sesión en la jerarquía canónica `docs/`. |
| `/docs-and-sync` | Proyecto | Ejecuta consecutivamente `/post-session-doc` seguido de `/repo-sync`. |
| `/domain-modeling` | Proyecto | Construye el lenguaje ubicuo, contextos delimitados y borradores de ADR. |
| `/grilling` | Proyecto | Entrevista interactiva para poner a prueba decisiones de arquitectura antes de codificar. |
| `/ask-the-council` | Proyecto | Deliberación multiagente con 5 perfiles asesores y un coordinador imparcial. |
| `/wizard-of-oz-mode` | Proyecto | Simula automatizaciones complejas con fachada manual para validar ideas rápido. |

---

## Estructura del proyecto

Al ejecutar `/project-init` en un repositorio de software, se genera esta estructura:

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
├── docs/                           ← Repositorio canónico de documentación
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

## Compatibilidad con entornos de IA

ASD no depende de una sola herramienta. Mientras que las reglas canónicas residen en `.agents/`, el framework sincroniza configuraciones nativas para los principales entornos:

| Entorno / Asistente IA | Estado | Mecanismo de integración | Capacidades clave |
|---|:---:|---|---|
| **Google Antigravity** | Soportado (Principal) | Estructura nativa `.agents/` y subagentes | Pipeline Uncle Bob completo, skills y slash commands |
| **Claude Code** (`claude` CLI) | Soportado | `CLAUDE.md` + `.claude/commands/` | Memoria de proyecto y slash commands nativos (`/code-pipeline`, etc.) |
| **OpenAI Codex y Estándar Abierto** | Soportado | Manifiesto raíz `AGENTS.md` | Cumple el estándar abierto AGENTS.md (ChatGPT, Codex, Aider) |
| **Cursor** | Soportado | `.cursorrules` y `.cursor/rules/asd-framework.mdc` | Modo dual: reglas clásicas y Cursor Rules 2.0 (`alwaysApply: true`) |
| **Windsurf** (Codeium) | Soportado | `.windsurfrules` | Reglas de flujo Cascade, política de ramas y quality gates |
| **GitHub Copilot** | Soportado | `.github/copilot-instructions.md` | Cumplimiento de gates en Copilot Chat y Workspace |
| **WSL Ubuntu 22.04** | Nativo | Ejecución transparente en WSL mediante wrappers | Compatibilidad multiplataforma completa en Windows |

### Validar configuración

Comprueba la preparación de tu proyecto en todos los entornos:

```bash
# Validar compatibilidad en todos los asistentes soportados
python3 scripts/harness_adapter.py --validate --project-dir .

# Instalar o sincronizar puentes faltantes sin sobreescribir tus reglas
python3 scripts/harness_adapter.py --project-dir .
```

---

## Ecosistema de skills y registros

ASD permite descubrir, instalar y gestionar habilidades desde los registros documentados en [SKILL_REGISTRIES.md](SKILL_REGISTRIES.md):

- **[Skills Marketplace (SkillsMP)](https://skillsmp.com)**: Catálogo de habilidades de agentes accesible vía API REST (`SKILLSMP_API_KEY`).
- **[Paul Bakaus Impeccable](https://github.com/pbakaus/impeccable)**: Criterios de diseño visual, accesibilidad WCAG y escáner automático de defectos UI (`impeccable detect`).
- **[Antigravity Skills](https://github.com/rmyndharis/antigravity-skills)**: Habilidades para backend, sistemas distribuidos y DevOps.
- **[Skills.md](https://skills.md)**: Herramientas para automatización de repositorios y flujos de contenido.
- **[Habilidades de Matt Pocock](https://github.com/mattpocock/skills)**: Habilidades para `grilling`, `domain-modeling`, `to-spec`, `refactor` y `prototype`.
- **[Habilidades Oficiales de Anthropic](https://github.com/anthropics/skills)**: Patrones de diseño de frontend (`frontend-design`).
- **[Cathy Kim SemVer](https://github.com/cathy-kim/skill-semver)**: Estándares SemVer y automatización de versiones.

```bash
# Buscar habilidades en los registros conectados
python3 scripts/skill_registry.py search "fastapi"

# Instalar una habilidad en tu ecosistema
python3 scripts/skill_registry.py install "fastapi"
```

---

## Preguntas frecuentes

### ¿ASD hace más lento el desarrollo?
Escribir pruebas y revisar un plan toma un par de minutos al inicio, pero elimina las horas dedicadas a depurar controladores rotos, casos borde olvidados y regresiones invisibles que los agentes descontrolados dejan atrás.

### ¿Puedo usar ASD en un proyecto existente?
Sí. Ejecutar `/project-init` en un repositorio existente activa el **Modo Retrofit**. Añade la carpeta `.agents/` y los archivos de configuración sin tocar una sola línea de código de tu aplicación ni alterar el historial de git.

### ¿Todos en el equipo deben usar el mismo editor?
No. Un desarrollador puede usar Claude Code en la terminal, otro Cursor y otro Windsurf o Antigravity. Todos comparten la misma Fuente de Verdad en `.agents/`, por lo que cada asistente aplica exactamente las mismas reglas y quality gates.

### ¿Qué lenguajes y frameworks funcionan con ASD?
ASD es agnóstico del stack. Funciona con TypeScript/JavaScript, Python, Go, Rust, PHP/Laravel, Java, C# y Ruby. Las puertas de calidad se conectan al framework de pruebas (Vitest, Jest, PyTest, PHPUnit, Cargo test) y a las librerías de validación de esquemas que ya uses.

---

## Licencia

Licencia MIT © [Idequel Bernabel](https://github.com/ibernabel).

Las habilidades comunitarias de [Matt Pocock](https://github.com/mattpocock/skills) y otros colaboradores de código abierto están sujetas a sus respectivas licencias.
