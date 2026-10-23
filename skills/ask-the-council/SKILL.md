---
name: ask-the-council
description: "Ejecuta el método canónico 'Ask the Council' (The Council) para someter cualquier idea, tesis, arquitectura o decisión a un panel de 5 asesores virtuales independientes y un Chairman."
---

# Workflow: Ask the Council (The Council Framework)

El usuario ha invocado al Consejo para evaluar críticamente una idea, tesis, arquitectura de software, modelo de negocio o decisión estratégica sin sesgos de complacencia (*sycophancy*).

## Consulta del Usuario

$ARGUMENTS

---

## Protocolo de Ejecución para Antigravity

Sigue estrictamente las 3 fases del método canónico:

### Fase 1: Context Enrichment & Neutral Framing
1. **Escaneo de Contexto Rápido:** Revisa si existen archivos de contexto relevantes en el workspace (`AGENTS.md`, `CLAUDE.md`, docs de arquitectura o negocio).
2. **Encuadre Neutral:** Formula el problema en un prompt neutral y claro que capture:
   - La decisión central o tesis propuesta.
   - Restricciones, contexto clave y lo que está verdaderamente en juego.

### Fase 2: Deliberación Paralela e Independiente (Blind Query)
Invoca mediante subagentes (`invoke_subagent`) o simula de forma aislada a los 5 asesores canónicos ubicados en `~/.agents/agents/council-*/`. **Cada asesor debe evaluar el prompt de forma independiente, sin ver las respuestas de los demás:**

1. 😈 **The Contrarian** (`council-contrarian` / `~/.agents/agents/council-contrarian/agent.md`):
   - Caza el fallo fatal, riesgos ocultos, costos de mantenimiento y razones de fracaso.
2. 🧬 **The First Principles Thinker** (`council-first-principles` / `~/.agents/agents/council-first-principles/agent.md`):
   - Desmonta la premisa superficial y analiza cuál es el problema raíz y verdad fundamental.
3. 🚀 **The Expansionist** (`council-expansionist` / `~/.agents/agents/council-expansionist/agent.md`):
   - Identifica ventajas ocultas, multiplicadores de valor y oportunidades de escala 10x.
4. 👁️ **The Outsider** (`council-outsider` / `~/.agents/agents/council-outsider/agent.md`):
   - Evalúa sin contexto previo ni sesgo de inmersión para detectar fallos obvios de sentido común.
5. 🛠️ **The Executor** (`council-executor` / `~/.agents/agents/council-executor/agent.md`):
   - Aterriza la viabilidad táctica y define el plan de acción inmediato para el lunes a las 9:00 AM.

### Fase 3: Síntesis & Veredicto del Chairman
Entrega las 5 deliberaciones completas a **The Chairman** (`council-chairman` / `~/.agents/agents/council-chairman/agent.md`) para:
1. Identificar el consenso unánime de alta confianza.
2. Analizar el choque central entre los asesores (ej. Contrarian vs Expansionist).
3. Exponer los puntos ciegos que todos pasaron por alto.
4. Emitir el **Veredicto Estratégico Final** con el formato oficial:

```markdown
# 🏛️ The Council: Strategic Verdict

## 🎯 Executive Re-Framing
...

## 💬 Council Deliberations
- 😈 **The Contrarian:** ...
- 🧬 **First Principles Thinker:** ...
- 🚀 **The Expansionist:** ...
- 👁️ **The Outsider:** ...
- 🛠️ **The Executor:** ...

## ⚔️ Internal Clashes & Peer Review
- **High-Confidence Consensus:** ...
- **The Central Battlefield:** ...
- **Unaddressed Blind Spots:** ...

## 👑 The Chairman's Final Verdict
- **Verdict:** [Approve | Approve with Conditions | Pivot | Kill]
- **Decisive Rationale:** ...
- **Monday 9:00 AM Action:** ...
```
