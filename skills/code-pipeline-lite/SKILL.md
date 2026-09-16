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
   Cuando el implementer termine, invoca al agente `reviewer` para:
   - Limpieza y calidad de código (KISS & YAGNI, eliminar duplicación, mejorar nombres).
   - **Security Audit obligatorio:** Verificar ausencia de claves API, tokens o secretos hardcodeados, uso correcto de `.env`, y sanitización básica de inputs.

5. **PII & Secrets Verifier (Obligatorio en proyectos `financial`)**  
   Si el proyecto está catalogado como `'financial'` o tiene `pii: financial` en `.agents/CONVENTIONS.md`:
   - Invoca al agente `pii-verifier` como **último paso** antes de finalizar para realizar el escaneo estricto de PII (datos personales de clientes), credenciales y asegurar el cumplimiento del protocolo Privacy-First.

6. **Resumen final**  
   Al terminar, entrega un resumen claro con:
   - Qué se implementó
   - Estado de los tests
   - Cambios de limpieza realizados por el reviewer
   - Resultado de la auditoría de seguridad (Reviewer) y verificación PII (si aplicó)
   - Puntos que debo revisar manualmente

### Reglas importantes
- No saltes etapas.
- El implementer solo debe ver los criterios aprobados.
- El `reviewer` SIEMPRE ejecuta la auditoría de seguridad (Security Audit).
- En proyectos `'financial'`, el agente `pii-verifier` es OBLIGATORIO como etapa final post-reviewer.
- Mantén el flujo ligero y pragmático: aplica **KISS** y **YAGNI**.
- Si la feature involucra interfaz gráfica / frontend, es obligatorio cumplir las directrices de `/frontend-design` y `/web-design-guidelines`.
- Enfoque **Privacy-First**: jamás incluir o mockear datos reales de clientes (PII) ni comprometer secretos.
- Si algún agente falla, detente y reporta el problema.
