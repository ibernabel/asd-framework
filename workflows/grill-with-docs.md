---
description: Sesión de grilling que actualiza automáticamente ADRs y glosario (CONTEXT.md) usando la skill domain-modeling.
user-invocable: true
---

# Workflow: Grill With Docs

El usuario desea ejecutar una sesión de grilling interactiva que además actualice la documentación de dominio (ADRs y glosario `CONTEXT.md`).

## Instrucciones para el Agente

1. Leer las instrucciones de `~/.agents/skills/grill-with-docs/SKILL.md` y `~/.agents/skills/domain-modeling/SKILL.md`.
2. Ejecutar la sesión de grilling actualizando `CONTEXT.md` e inyectando ADRs en `docs/decisions/` a medida que se cristalizan las decisiones.
