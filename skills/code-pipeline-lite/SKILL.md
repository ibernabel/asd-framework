---
name: code-pipeline-lite
description: Lanza el pipeline lite (Planner → Implementer → Reviewer) para features de complejidad media-baja. Ideal cuando se quiere buen resultado sin el gauntlet completo de Uncle Bob.
---

# Code Pipeline Lite

Quiero implementar una feature usando el **pipeline lite**.

## Petición / Especificación informal

$ARGUMENTS

---

Sigue este flujo de forma estricta:

1. **Planner**  
   Invoca al agente `planner` para convertir la petición informal en:
   - Criterios de aceptación claros (viñetas)
   - Escenarios de comportamiento simples
   - Edge cases relevantes

2. **Aprobación humana**  
   Muéstrame los criterios generados y espera mi aprobación o correcciones antes de continuar.

3. **Implementer**  
   Una vez aprobados los criterios, invoca al agente `implementer` pasándole **únicamente** los criterios de aceptación aprobados (nunca las specs informales originales).  
   Debe escribir tests + código y no parar hasta que todo esté en verde.

4. **Reviewer**  
   Cuando el implementer termine, invoca al agente `reviewer` para una pasada rápida de limpieza, calidad y spot-check de seguridad (sin secretos ni PII expuestos).

5. **Resumen final**  
   Al terminar, entrega un resumen claro con:
   - Qué se implementó
   - Estado de los tests
   - Cambios de limpieza realizados por el reviewer (KISS & YAGNI)
   - Verificación de seguridad y secretos
   - Puntos que debo revisar manualmente

### Reglas importantes
- No saltes etapas.
- El implementer solo debe ver los criterios aprobados.
- Mantén el flujo ligero y pragmático: aplica **KISS** y **YAGNI**.
- Si la feature involucra interfaz gráfica / frontend, es obligatorio cumplir las directrices de `/frontend-design` y `/web-design-guidelines`.
- Enfoque **Privacy-First**: jamás incluir o mockear datos reales de clientes (PII) ni comprometer secretos.
- Si algún agente falla, detente y reporta el problema.
