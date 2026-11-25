---
name: ask-the-council
description: "Ejecuta la deliberación paralela de The Council invocando a los 5 asesores en paralelo mediante subagentes y sintetizando con The Chairman."
---

# Workflow: Ask the Council (The Council Framework)

El usuario ha invocado al Consejo para evaluar críticamente una idea, tesis, arquitectura de software, modelo de negocio o decisión estratégica sin sesgos de complacencia (*sycophancy*).

## Consulta del Usuario

$ARGUMENTS

---

## Instrucción de Orquestación Directa para el Asistente

> ⚠️ **REGLA CRÍTICA DE VISIBILIDAD EN LA UI Y CONCURRENCIA PARALELA:**
> - **ESTÁ ESTRICTAMENTE PROHIBIDO simular a los asesores o generar sus opiniones en el hilo principal.**
> - Tú (el agente principal) actúas como el **Orquestador del Consejo**.
> - En la **Fase 2**, DEBES despachar a los 5 asesores canónicos **SIMULTÁNEAMENTE en un único turno con 5 llamadas de herramienta `invoke_subagent`**. Esto garantiza que los 5 asesores se ejecuten en paralelo en segundo plano y aparezcan con sus tarjetas individuales en el timeline visual de Antigravity.
> - En la **Fase 3**, una vez recibidas las 5 deliberaciones, DEBES invocar al subagente `council-chairman` mediante `invoke_subagent` para que realice el arbitraje, peer review ciego y emita el veredicto estratégico final.

---

### Protocolo de Ejecución Paso a Paso

#### Fase 1: Context Enrichment & Neutral Framing (Hilo Principal)
1. **Revisión de Contexto Rápido:** Consulta brevemente si existen archivos clave en el workspace (`AGENTS.md`, `CLAUDE.md`, docs de arquitectura o negocio) para enriquecer el encuadre sin sesgar la pregunta.
2. **Formulación del Prompt Neutral:** Redacta un prompt neutral y conciso que describa:
   - La decisión central, hipótesis o arquitectura planteada.
   - Restricciones, trade-offs conocidos y contexto operativo.
   - **Regla Anti-Sycophancy:** No agregues juicios de valor ni indiques si al usuario le gusta la idea; preserva la neutralidad para un blind review genuino.

#### Fase 2: Deliberación Paralela Concurrente (Fan-Out)
Emite **exactamente 5 llamadas a la herramienta `invoke_subagent` en la misma respuesta** (llamadas paralelas):

1. **The Contrarian:**
   - `invoke_subagent` con:
     - `TypeName`: `"council-contrarian"`
     - `Role`: `"Council Contrarian"`
     - `Prompt`: El prompt neutral de la Fase 1.

2. **The First Principles Thinker:**
   - `invoke_subagent` con:
     - `TypeName`: `"council-first-principles"`
     - `Role`: `"Council First Principles"`
     - `Prompt`: El prompt neutral de la Fase 1.

3. **The Expansionist:**
   - `invoke_subagent` con:
     - `TypeName`: `"council-expansionist"`
     - `Role`: `"Council Expansionist"`
     - `Prompt`: El prompt neutral de la Fase 1.

4. **The Outsider:**
   - `invoke_subagent` con:
     - `TypeName`: `"council-outsider"`
     - `Role`: `"Council Outsider"`
     - `Prompt`: El prompt neutral de la Fase 1.

5. **The Executor:**
   - `invoke_subagent` con:
     - `TypeName`: `"council-executor"`
     - `Role`: `"Council Executor"`
     - `Prompt`: El prompt neutral de la Fase 1.

> **Importante:** Al emitir estas 5 llamadas, finaliza tu turno inmediatamente sin llamar a más herramientas. Antigravity ejecutará los 5 subagentes en paralelo y te despertará automáticamente mediante *reactive wakeup* a medida que entreguen sus respuestas.

#### Fase 3: Arbitraje & Veredicto del Chairman (Fan-In)
Una vez que hayas recibido las 5 respuestas de los asesores:
1. Reúne las 5 deliberaciones completas junto con la formulación neutral inicial.
2. Invoca al subagente Chairman mediante la herramienta `invoke_subagent`:
   - `TypeName`: `"council-chairman"`
   - `Role`: `"Council Chairman"`
   - `Prompt`:
     ```text
     Consulta Neutral Evaluada:
     <pregunta neutral>

     Deliberaciones de los 5 Asesores:
     ---
     Contrarian: <respuesta>
     ---
     First Principles: <respuesta>
     ---
     Expansionist: <respuesta>
     ---
     Outsider: <respuesta>
     ---
     Executor: <respuesta>
     ---
     Por favor realiza el peer review ciego, arbitra los choques y emite el veredicto estratégico final en el formato oficial de The Council.
     ```

#### Fase 4: Entrega al Usuario en el Hilo Principal
Cuando el subagente `council-chairman` retorne su veredicto estructurado, preséntalo directamente al usuario en el chat asegurando el formato canónico:

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
