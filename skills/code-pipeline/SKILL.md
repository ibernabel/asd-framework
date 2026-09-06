---
name: code-pipeline
description: "Ejecuta el pipeline completo de Uncle Bob (Specifier → Coder → Refactorer → Architect → QA) orquestando directamente cada subagente de forma secuencial visible en la UI."
---

# Code Pipeline (Uncle Bob style)

Implementación guiada por el pipeline formal de desarrollo con subagentes especializados.

## Requerimiento / Especificaciones

$ARGUMENTS

---

## Instrucción de Orquestación Directa para el Asistente

> ⚠️ **REGLA CRÍTICA DE VISIBILIDAD EN LA UI:**
> **NO invoques un subagente intermediario llamado `orchestrator`.**
> Tú (el agente principal) debes actuar como el **Orquestador Principal**, ejecutando directamente y de forma secuencial cada subagente especializado mediante la herramienta `invoke_subagent`.
> Esto garantiza que cada agente aparezca con su nombre, rol y estado individual en el timeline visual de Antigravity.

---

### Protocolo Secuencial de Ejecución (Paso a Paso)

Debes ejecutar rigurosamente las siguientes 5 etapas en orden, esperando a que cada subagente concluya su trabajo y te notifique antes de invocar al siguiente:

#### 1. Etapa 1: Specifier
- **Invocación:** `invoke_subagent` con `TypeName: "specifier"`, `Role: "Feature Specifier"`.
- **Payload:** Pasa las especificaciones del requerimiento ($ARGUMENTS).
- **Entregables requeridos:** Archivo(s) Gherkin (`.feature`), plan de QA paso a paso (`docs/qa/qa-plan-*.md`) y lista de tareas claras.

#### 2. Etapa 2: Coder
- **Invocación:** `invoke_subagent` con `TypeName: "coder"`, `Role: "TDD Coder"`.
- **Payload:** Pasa la ruta de los archivos Gherkin y los objetivos de implementación.
- **Entregables requeridos:** Tests de aceptación que implementan el Gherkin, tests unitarios exhaustivos y código de producción que deje toda la suite en verde (100% passing).

#### 3. Etapa 3: Refactorer
- **Invocación:** `invoke_subagent` con `TypeName: "refactorer"`, `Role: "Code Refactorer"`.
- **Payload:** Pasa las rutas de los archivos modificados/creados por el Coder.
- **Entregables requeridos:** Código limpio, sin duplicaciones, con complejidad ciclomática reducida (CRAP ≤ 6) y preservando la suite de tests en verde.

#### 4. Etapa 4: Architect / Hardener
- **Invocación:** `invoke_subagent` con `TypeName: "architect"`, `Role: "Architecture Hardener"`.
- **Payload:** Pasa el código refactorizado y las suites de pruebas.
- **Entregables requeridos:** Cobertura alta (≥ 90-95%), análisis / simulación de mutation testing (matar mutantes críticos), validación de desacoplamiento y no-regresión.

#### 5. Etapa 5: QA
- **Invocación:** `invoke_subagent` con `TypeName: "qa"`, `Role: "QA Engineer"`.
- **Payload:** Pasa el plan de pruebas generado en la Etapa 1 (`docs/qa/qa-plan-*.md`).
- **Entregables requeridos:** Ejecución sistemática de todos los casos de prueba, generación del reporte formal de QA (`docs/qa/qa-report-*.md`) y actualización de documentación de estado/roadmap.

---

### Resumen Final al Usuario

Una vez que el agente QA finalice, compila y presenta un resumen ejecutivo claro:
1. Funcionalidades implementadas y módulos afectados.
2. Estado consolidado de la suite de pruebas (Backend + Frontend).
3. Métricas de cobertura y resultados de mutation testing.
4. Dictamen del reporte de QA.
5. Puntos o recomendaciones que el desarrollador deba validar manualmente.
