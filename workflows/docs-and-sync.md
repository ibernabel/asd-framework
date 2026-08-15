---
description: Ejecuta consecutivamente los workflows de documentación de fin de sesión (post-session-doc) y sincronización con repositorio (repo-sync).
user-invocable: true
---

# Workflow: Documentación y Sincronización Completa (Docs & Sync)

## Descripción
Este workflow define el procedimiento estándar para ejecutar de forma secuencial la documentación del cierre de sesión de trabajo (`post-session-doc.md`) y la sincronización segura con el repositorio remoto en GitHub (`repo-sync.md`). Garantiza la actualización de la **Única Fuente de Verdad (SSOT)** en `docs/` antes de realizar commits, etiquetado SemVer y push.

---

## Disparador (When to run)
Ejecutar este workflow cuando:
- Se haya finalizado una sesión de desarrollo o hito de trabajo.
- Se requiera actualizar la documentación del proyecto (`docs/`) y publicar/respaldar inmediatamente los cambios en GitHub.

---

## Roles Asociados (ASD Framework)
- **QA / Technical Writer:** Auditar los cambios realizados y generar/actualizar los documentos dentro de `docs/`.
- **Developer / QA:** Ejecutar la suite de pruebas, realizar la sincronización Git y asegurar un árbol de trabajo limpio.
- **Security:** Auditar que no se incluyan archivos `.env`, secretos ni datos confidenciales/PII antes de staging/commit.
- **Architect:** Validar cumplimiento de principios SOLID, KISS y DRY en ADRs y cambios estructurales.

---

## Pasos del Workflow

### Fase 1: Documentación de Fin de Sesión (`post-session-doc.md`)

1. **Auditoría de la Sesión:**
   ```bash
   # 1. Inspect status of modified and untracked files
   git status

   # 2. Review summary of line and file changes
   git diff --stat

   # 3. Review recent commits in current session
   git log -n 5 --oneline
   ```

2. **Generar Documentación Específica en `docs/`:**
   - **Nuevas Funcionalidades / Refactorizaciones:** Crear/actualizar `docs/implementation/YYYY-MM-DD-[nombre-feature].md`.
   - **Correcciones / Bugs Fixes:** Crear/actualizar `docs/fixes/FIX-YYYY-MM-DD-[descripcion-bug].md`.
   - **Decisiones de Arquitectura:** Crear/actualizar `docs/decisions/ADR-XXX-[titulo-decision].md`.

3. **Actualizar el SSOT (`docs/README.md`) y Roadmap:**
   - Registrar enlaces a los nuevos documentos creados en `docs/README.md`.
   - Actualizar estado de tareas en `ROADMAP.md` si aplica.

4. **Verificación de Seguridad y PII:**
   - Confirmar ausencia de credenciales, tokens o PII en los archivos creados.

---

### Fase 2: Sincronización con Repositorio Remoto (`repo-sync.md`)

1. **Verificación de Pre-Sincronización:**
   ```bash
   # 1. Check current branch and modified files
   git status

   # 2. Confirm current active branch name
   git branch --show-current
   ```

2. **Actualización Remota (Fetch & Rebase):**
   ```bash
   # Fetch latest changes from remote origin
   git fetch origin

   # Pull remote changes using rebase for linear history
   git pull --rebase origin $(git branch --show-current)
   ```

3. **Incremento de Versión y Tag Git (SemVer):**
   ```bash
   # Bump patch version (e.g. 1.0.1 -> 1.0.2) and auto-create tag vX.Y.Z
   python3 scripts/bump_version.py patch
   
   # Or create manual tag if bump_version.py is not used
   # git tag -a v1.0.0 -m "Release v1.0.0"
   ```

4. **Staging y Commit Convencional:**
   ```bash
   # Stage modified files and documentation
   git add .

   # Commit changes using Conventional Commit syntax
   git commit -m "docs & feat: update documentation and finalize session changes"
   ```

5. **Push a GitHub (Commits + Tags):**
   ```bash
   # Push current branch commits to origin
   git push origin $(git branch --show-current)

   # Push all git tags to GitHub
   git push origin --tags
   ```

6. **Verificación Post-Push:**
   ```bash
   # Confirm clean working tree and branch status
   git status
   ```

---

## Resumen de Ejecución Rápida (Unified Command Sequence)

```bash
# Audit changes, update docs, pull rebase, stage, commit and push with tags
git status && git fetch origin && git pull --rebase origin $(git branch --show-current)
git add .
git commit -m "docs & feat: finalize session documentation and sync repository"
git push origin $(git branch --show-current) --tags
```
