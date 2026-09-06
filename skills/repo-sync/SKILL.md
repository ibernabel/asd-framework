---
name: repo-sync
description: Define el procedimiento para sincronizar de forma segura los cambios locales con GitHub (SemVer, CHANGELOG.md, Git tags, commit convencional, push).
triggers:
  - repo-sync
  - sync repo
  - git push
  - release version
  - bump version
user-invocable: true
---

# Skill / Workflow: Sincronización con GitHub (`repo-sync`)

## Descripción
Este workflow define el procedimiento estándar para sincronizar de forma segura y consistente los cambios locales del proyecto con el repositorio remoto en GitHub, garantizando un historial de commits lineal, versionado semántico formal (SemVer), **actualización obligatoria de `CHANGELOG.md`**, creación de etiquetas anotadas (**Git tags**) sobre el commit de release y alineación estricta con las reglas del **Framework ASD v2**.

---

## Disparador (When to run)
Ejecutar este workflow cuando:
- Se haya completado una tarea, feature o hito del roadmap.
- Se hayan aplicado soluciones a errores (fixes) o refactorizaciones.
- Se haya completado el workflow de documentación post-sesión (`/post-session-doc` o `/docs-and-sync`).
- Se requiera publicar o respaldar el trabajo actual en GitHub.

---

## Reglas de Incremento SemVer (Criterios `versioning-guide`)

| Tipo de Bump | Comando | Criterio de Aplicación | Ejemplos |
|--------------|---------|------------------------|----------|
| **`patch`** (Z) | `python3 scripts/bump_version.py patch -m "..." --no-tag` | Corrección de bugs, refactorización sin cambio de comportamiento, documentación, ajustes de estilo o dependencias. | `0.1.0` $\to$ `0.1.1` |
| **`minor`** (Y) | `python3 scripts/bump_version.py minor -m "..." --no-tag` | Nuevas funcionalidades, nuevos componentes, endpoints API retrocompatibles, integración de nuevas skills o workflows. | `0.1.1` $\to$ `0.2.0` |
| **`major`** (X) | `python3 scripts/bump_version.py major -m "..." --no-tag` | Cambios que rompen compatibilidad (breaking changes), restructuración profunda de arquitectura o modelo de datos. | `0.2.0` $\to$ `1.0.0` |

---

## Pasos del Workflow

### Paso 1: Verificación de Pre-Sincronización y Seguridad
```bash
# Check current branch and modified files
git status
git branch --show-current
```

### Paso 2: Sincronización con Remoto (Fetch & Rebase)
```bash
# Fetch and rebase to ensure linear history
git fetch origin
git pull --rebase origin $(git branch --show-current)
```

### Paso 3: Incrementar Versión y Actualizar `CHANGELOG.md` (SemVer)
```bash
# Bump SemVer and scaffold/update CHANGELOG.md
python3 scripts/bump_version.py [patch|minor|major] -m "Descripción de los cambios" --no-tag
```

### Paso 4: Staging y Commit Convencional
```bash
# Stage modified files, version files, and changelog
git add .

# Conventional commit
git commit -m "<type>: <descripción>"
```

### Paso 5: Creación del Git Tag Anotado sobre el Commit de Release
```bash
# Create annotated Git tag on the new release commit
python3 scripts/bump_version.py --tag-only
```

### Paso 6: Push a GitHub (Commits + Tags)
```bash
# Push branch commits and all tags to remote origin
git push origin $(git branch --show-current)
git push origin --tags
```

### Paso 7: Verificación Post-Push
```bash
# Verify clean working tree
git status
```
