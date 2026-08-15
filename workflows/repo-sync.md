---
description: Sincronizar cambios locales de forma segura con GitHub (SemVer, CHANGELOG.md, commit convencional, Git tags, push).
user-invocable: true
---

# Workflow: Sincronización con GitHub (Repo Sync)

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

## Roles Asociados (ASD Framework)
- **Developer / QA:** Encargado de verificar que el código pase las pruebas antes de subirlo.
- **Security:** Auditar que no se incluyan archivos `.env`, credenciales ni secretos en el staging.
- **Architect / Release:** Determinar el tipo de incremento SemVer (`patch`, `minor`, `major`) según las reglas de `versioning-guide`.

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
Comprobar el estado local de Git, confirmar la rama activa y auditar que no existan archivos confidenciales sin ignorar:

```bash
# 1. Check current branch and modified files
git status

# 2. Confirm current active branch name
git branch --show-current
```

> [!WARNING]
> Verificar siempre que archivos confidenciales (`.env`, secretos, tokens de API, PII financiero de clientes) **NO** estén en staging ni sin ignorar en `.gitignore`.

---

### Paso 2: Sincronización con Remoto (Fetch & Rebase)
Traer las últimas actualizaciones del repositorio en GitHub para asegurar un historial lineal:

```bash
# Fetch latest changes from remote origin
git fetch origin

# Pull remote changes using rebase for linear history
git pull --rebase origin $(git branch --show-current)
```

Si existen conflictos durante el rebase, resolverlos localmente y continuar con:
```bash
# Continue rebase after resolving conflicts
git rebase --continue
```

---

### Paso 3: Incrementar Versión y Actualizar `CHANGELOG.md` (SemVer)
Ejecutar el script de versionado para actualizar `VERSION`, manifiestos (`package.json` / `pyproject.toml`) y registrar la entrada en `CHANGELOG.md`:

```bash
# Bump version and update CHANGELOG.md (deferred tag until commit)
python3 scripts/bump_version.py [patch|minor|major] -m "Breve descripción de los cambios de la sesión" --no-tag
```

**Ejemplo para patch:**
```bash
python3 scripts/bump_version.py patch -m "fix loan calculation rounding and update PRD traceability" --no-tag
```

---

### Paso 4: Staging y Commit Convencional

1. Preparar todos los archivos modificados, documentación, `VERSION` y `CHANGELOG.md`:
```bash
# Stage modified files, version files, and changelog
git add .
```

2. Generar el commit siguiendo el estándar de **Conventional Commits**:
   - `feat: [descripción]` para nuevas características.
   - `fix: [descripción]` para correcciones de errores.
   - `docs: [descripción]` para cambios en documentación.
   - `refactor: [descripción]` para refactorización sin cambios de comportamiento.
   - `chore: [descripción]` para tareas de mantenimiento, dependencias o bumps.

```bash
# Commit release changes using Conventional Commit syntax
git commit -m "feat: complete website loan calculator and bump to v$(cat VERSION)"
```

---

### Paso 5: Creación del Git Tag Anotado sobre el Commit de Release
Crear la etiqueta Git apuntando exactamente al nuevo commit que contiene la versión y el `CHANGELOG.md`:

```bash
# Create annotated Git tag on the new release commit
python3 scripts/bump_version.py --tag-only
```

*(Equivalente manual: `git tag -a "v$(cat VERSION)" -m "Release v$(cat VERSION)"`)*

---

### Paso 6: Push a GitHub (Commits + Tags)
Enviar los commits y las etiquetas al repositorio remoto:

```bash
# Push current branch commits to origin
git push origin $(git branch --show-current)

# Push all release tags to GitHub
git push origin --tags
```

---

### Paso 7: Verificación Post-Push
Confirmar que el espacio de trabajo quedó completamente limpio y en sincronía con el remoto:

```bash
# Confirm clean working tree and up-to-date branch status
git status
```

---

## Resumen de Comandos Rápidos (Cheat Sheet)

```bash
# 1. Pull & rebase
git fetch origin && git pull --rebase origin $(git branch --show-current)

# 2. Bump SemVer & update CHANGELOG.md
python3 scripts/bump_version.py patch -m "implement core changes" --no-tag

# 3. Commit & Tag
git add .
git commit -m "chore(release): v$(cat VERSION) - implement core changes"
python3 scripts/bump_version.py --tag-only

# 4. Push branch and tags
git push origin $(git branch --show-current) --tags
```
