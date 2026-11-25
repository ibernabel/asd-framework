# Implementación: Regla `answer-in-the-same-language` en Todo el Ecosistema ASD

- **Fecha:** 2026-11-25
- **Rama:** `feature/answer-in-the-same-language`

## Objetivo

Eliminar la contradicción que obligaba a responder en inglés en chat y documentación Markdown, instaurando la regla canónica **`answer-in-the-same-language`**:

- **Chat (`answer-in-the-same-language`):** responder siempre en el mismo idioma del usuario, sin importar el idioma de cualquier skill, regla o código invocado.
- **Código fuente (`.py`, `.php`, `.html`, `.js`, `.ts`, `.sql`, etc.), comentarios/docstrings y mensajes de commit:** siempre en **inglés**.
- **Archivos Markdown (`.md`):** siguen el idioma de la conversación o el definido por el proyecto.
- **Contenido para audiencia:** idioma objetivo del proyecto (por defecto **español**).

## Componentes Afectados

- **Plantillas de dominio (`templates/`):** `software-dev-agents.md`, `ai-agents-agents.md`, `business-admin-agents.md`, `content-brand-agents.md`, `video-production-agents.md`, `user-template.md`, `USER.example.md`.
- **Adaptadores multi-harness (`templates/harnesses/`):** `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `cursor-rule.mdc`, `.windsurfrules`, `copilot-instructions.md`.
- **Motor de sincronización:** `scripts/sync_agents_ecosystem.py` (`sync_linguistic_section_in_agents_md`, `sync_project_harnesses_language`, `discover_subvertical_dirs`) y `scripts/install_project_skills.py`.
- **Pruebas unitarias:** `tests/test_language_rules_sync.py`.

## Pruebas de Verificación

```bash
# Ejecutar suite completa de pruebas en asd-framework
python3 -m unittest discover -s tests -v
```

- Resultado: 9 de 9 pruebas pasaron (`OK`), validando idempotencia, preservación de secciones personalizadas (`corebank`, `caketoppers`) y preservación de saltos de línea (`LF`/`CRLF`).
- Propagación verificada mediante `sync_agents_ecosystem.py --catalog` sobre 38 directorios y 266 archivos sin incidencias.
