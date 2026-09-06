---
name: improve-mode
description: "Modo meta-analítico de revisión crítica, introspección y mejora continua del sistema de agentes, workflows, prompts y pipelines."
---

# Workflow: Improve Mode (Modo de Mejora e Introspección)

## 1. Propósito y Filosofía
El **Improve Mode** es un protocolo especial que suspende la ejecución mecánica estándar y activa el pensamiento crítico y meta-analítico del agente sobre el propio sistema de trabajo.

Su objetivo es auditar, perfeccionar y evolucionar:
- Definiciones de workflows (`.agents/workflows/*.md`).
- Definiciones y roles de agentes (`.agents/agents/*/agent.md`).
- Habilidades y manuales de referencia (`.agents/skills/*`).
- Reglas del espacio de trabajo (`.agents/AGENTS.md`, `RULE[...]`).
- Calidad, ergonomía y fidelidad de los artefactos generados.

---

## 2. Responsabilidades del Agente en Improve Mode

1. **Introspección y Análisis de Causa Raíz:** No asumir que el fallo o la fricción es casualidad; diagnosticar la causa raíz a nivel de prompt, jerarquía de subagentes, contexto o instrucciones.
2. **Evaluación Comparativa (Expectativa vs. Realidad):** Contrastar minuciosamente lo que el usuario esperaba observar (ej. visibilidad en el timeline del IDE, formato de tests, salida estructurada) frente a lo que realmente ocurrió.
3. **Acción Directa en Archivos de Definición:** No limitarse a dar consejos abstractos; proponer y aplicar cambios directos en los archivos `.md` correspondientes.
4. **Propagación y Sincronización:** Si una mejora aplica a nivel global (`~/.agents/`), sincronizarla en cascada a todos los repositorios y entornos configurados.

---

## 3. Modos de Activación y Comportamiento

Dependiendo del momento en que se invoque este workflow, el agente adoptará la postura adecuada:

### A. Activación Previa (Antes de Iniciar un Trabajo)
*El usuario desea ejecutar una tarea como banco de pruebas para auditar un workflow.*
- **Respuesta inicial:** Confirmar el modo activo y consultar:
  > *"Estamos en **Improve Mode**. ¿Cuál es el workflow o requerimiento que ejecutaremos? Realizaremos el trabajo estándar pero con mentalidad de auditoría continua, evaluando fricciones, calidad y oportunidades de optimización en cada etapa."*
- **Durante la ejecución:** Monitorear puntos ciegos, latencias o instrucciones ambiguas en los prompts.
- **Al concluir:** Entregar el entregable principal acompañado de una sección formal de **"Hallazgos y Propuestas de Mejora al Workflow"**.

### B. Activación Intermedia (Pausa / Fricción en Tiempo Real)
*El usuario o el agente detecta un comportamiento no óptimo a mitad de camino.*
- **Acción:** Pausar la ejecución operativa.
- **Diagnóstico:** Identificar qué regla, herramienta o instrucción provocó la desviación.
- **Ajuste:** Proponer la corrección del `.md` o de la estrategia antes de reanudar el flujo.

### C. Activación Retrospectiva (Post-Ejecución / Cierre de Tarea)
*La tarea finalizó (con éxito o fallo) y se desea capitalizar el aprendizaje.*
- **Acción:** Conducir un Post-Mortem estructurado:
  1. **Qué funcionó excepcionalmente bien** (patrones a preservar/estandarizar).
  2. **Dónde hubo fricción, ambigüedad o falta de visibilidad**.
  3. **Modificaciones concretas aplicadas** a los archivos `.md` de `.agents/`.
  4. **Plan de prueba/verificación** para confirmar que las próximas ejecuciones adoptarán el nuevo estándar.

---

## 4. Entregables del Improve Mode

Toda sesión o intervención bajo este modo debe culminar con:
1. **Informe de Diagnóstico y Mejoras** (explicación clara en chat o artefacto markdown).
2. **Edición efectiva de los archivos de configuración** (`workflows/*.md`, `agents/*.md`, etc.).
3. **Sincronización en cascada** a nivel global y local en los proyectos donde aplique.
