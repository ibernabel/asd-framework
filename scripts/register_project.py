#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASD Framework - Project Catalog Registry Utility
Manages ~/.agents/projects.json and ~/.agents/PROJECTS.md
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

CATALOG_DIR = os.path.expanduser("~/.agents")
JSON_PATH = os.path.join(CATALOG_DIR, "projects.json")
MD_PATH = os.path.join(CATALOG_DIR, "PROJECTS.md")


def load_projects():
    if not os.path.exists(JSON_PATH):
        return {"version": "2.0.0", "updated_at": datetime.now().isoformat(), "projects": []}
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Error loading {JSON_PATH}: {e}", file=sys.stderr)
        return {"version": "2.0.0", "updated_at": datetime.now().isoformat(), "projects": []}


def save_projects(data):
    data["updated_at"] = datetime.now().isoformat()
    # Sort projects by domain then id
    data["projects"].sort(key=lambda p: (p.get("domain", ""), p.get("id", "")))
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    render_markdown(data)


def detect_project_info(project_path):
    abs_path = os.path.abspath(os.path.expanduser(project_path))
    info = {
        "linux_path": abs_path,
        "windows_path": abs_path.replace("/home/ibernabel", r"Z:\home\ibernabel").replace("/", "\\") if abs_path.startswith("/home/ibernabel") else abs_path.replace("/mnt/c", r"C:").replace("/", "\\"),
        "git_remote": "",
        "status": "pending_init",
        "domain": "software",
        "pii": "standard",
        "stack": [],
    }

    if abs_path == "/mnt/c/develop/corebank" or "corebank" in abs_path:
        info["symlink_path"] = "/home/ibernabel/develop/corebank"
        info["windows_path"] = r"C:\develop\corebank"

    if os.path.exists(os.path.join(abs_path, ".git")):
        info["status"] = "pending_retrofit"
        try:
            res = subprocess.run(["git", "remote", "get-url", "origin"], cwd=abs_path, capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                info["git_remote"] = res.stdout.strip()
        except Exception:
            pass

    if os.path.exists(os.path.join(abs_path, ".agents")):
        info["status"] = "active"

    conv_path = os.path.join(abs_path, ".agents", "CONVENTIONS.md")
    if os.path.exists(conv_path):
        try:
            with open(conv_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for line in content.splitlines()[:30]:
                    l_lower = line.lower()
                    if "domain:" in l_lower and "#" in line:
                        info["domain"] = line.split(":", 1)[1].split("#")[0].strip()
                    elif "domain:" in l_lower:
                        info["domain"] = line.split(":", 1)[1].strip()
                    if "pii:" in l_lower and "#" in line:
                        info["pii"] = line.split(":", 1)[1].split("#")[0].strip()
                    elif "pii:" in l_lower:
                        info["pii"] = line.split(":", 1)[1].strip()
        except Exception:
            pass

    # Stack detection
    pkg_path = os.path.join(abs_path, "package.json")
    if os.path.exists(pkg_path):
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                pkg = json.load(f)
                deps = list(pkg.get("dependencies", {}).keys()) + list(pkg.get("devDependencies", {}).keys())
                for fw in ["astro", "next", "react", "vue", "svelte", "express", "tailwindcss", "typescript"]:
                    if fw in deps or any(fw in d for d in deps):
                        info["stack"].append(fw)
        except Exception:
            info["stack"].append("node")

    if os.path.exists(os.path.join(abs_path, "composer.json")):
        info["stack"].append("php/composer")
    if os.path.exists(os.path.join(abs_path, "pyproject.toml")) or os.path.exists(os.path.join(abs_path, "requirements.txt")):
        info["stack"].append("python")

    return info


def render_markdown(data):
    projects = data.get("projects", [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    total = len(projects)
    active = sum(1 for p in projects if p.get("status") == "active")
    retrofit = sum(1 for p in projects if p.get("status") == "pending_retrofit")
    pending = sum(1 for p in projects if p.get("status") == "pending_init")
    financial = sum(1 for p in projects if p.get("pii") == "financial")

    lines = [
        "# Catálogo de Proyectos — ASD Framework",
        "",
        "> **Registro Central (SSOT) de proyectos desarrollados o en adopción del Framework ASD.**",
        "> Este archivo sirve como inventario canónico para auditar, propagar cambios de plantillas, skills, reglas globales y agentes de pipeline.",
        "",
        f"**Última actualización:** `{now}` | **Total Proyectos:** `{total}` (`{active}` Activos ASD, `{retrofit}` Pendientes Retrofit, `{pending}` Pendientes Init, `{financial}` Clasificación Financiera/PII)",
        "",
        "---",
        "",
        "## 📊 Resumen Ejecutivo del Ecosistema",
        "",
        "| ID | Proyecto | Dominio | Estado ASD | PII / Seguridad | Stack Principal | Repositorio Remoto |",
        "|---|---|---|---|---|---|---|",
    ]

    for p in projects:
        status_badge = {
            "active": "🟢 Activo (`.agents/`)",
            "pending_retrofit": "🟡 Pendiente Retrofit",
            "pending_init": "⚪ Pendiente Init",
        }.get(p.get("status", ""), p.get("status", ""))

        pii_badge = {
            "financial": "🔒 `financial` (PII Gate)",
            "standard": "🛡️ `standard`",
            "false": "🔓 `false`",
        }.get(p.get("pii", "standard"), p.get("pii", "standard"))

        stack_str = ", ".join(p.get("stack", [])) if p.get("stack") else "-"
        repo_link = f"[{p.get('git_remote').split('/')[-1]}]({p.get('git_remote')})" if "github.com" in p.get("git_remote", "") else (p.get("git_remote") or "Local")

        lines.append(
            f"| `{p.get('id')}` | **{p.get('name')}** | `{p.get('domain')}` | {status_badge} | {pii_badge} | {stack_str} | {repo_link} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 📁 Detalle de Proyectos Registrados",
        "",
    ])

    for p in projects:
        lines.extend([
            f"### `{p.get('id')}` — {p.get('name')}",
            "",
            f"- **Descripción:** {p.get('description', 'Sin descripción')}",
            f"- **Ruta Linux (WSL):** `{p.get('linux_path')}`",
            f"- **Ruta Windows:** `{p.get('windows_path')}`",
        ])
        if p.get("symlink_path"):
            lines.append(f"- **Symlink WSL:** `{p.get('symlink_path')}`")
        lines.extend([
            f"- **Dominio ASD:** `{p.get('domain')}`",
            f"- **Estado de Adopción:** `{p.get('status')}`",
            f"- **Clasificación PII:** `{p.get('pii')}`",
            f"- **Stack / Tecnologías:** {', '.join(f'`{s}`' for s in p.get('stack', [])) if p.get('stack') else 'N/A'}",
            f"- **Git Remote:** `{p.get('git_remote', 'N/A')}`",
            f"- **Tags de Propagación:** {', '.join(f'`{t}`' for t in p.get('tags', [])) if p.get('tags') else '`all`'}",
            "",
        ])

    lines.extend([
        "---",
        "",
        "## 🔄 Protocolo de Propagación de Cambios del Framework",
        "",
        "Cuando se realicen modificaciones al ASD Framework (en `~/.agents/templates/`, `~/.agents/skills/`, o reglas de agentes):",
        "",
        "1. **Auditoría de Impacto:** Consultar este catálogo para identificar qué proyectos coinciden con el dominio o stack modificado.",
        "2. **Ejecución Automática de Sincronización:**",
        "   ```bash",
        "   # Sincronizar todos los proyectos activos registrados en el catálogo",
        "   python3 ~/.agents/scripts/sync_agents_ecosystem.py --catalog",
        "   ```",
        "3. **Retrofit Progresivo:** Para proyectos con estado `pending_retrofit`, ejecutar `/project-init` desde su raíz para inyectar `.agents/` y skills deterministas.",
        "",
        "---",
        "",
        "## 📜 Regla de Registro Obligatorio (`/project-init`)",
        "",
        "> [!IMPORTANT]",
        "> **Regla Global de Registro:**",
        "> Cada vez que se inicialice un proyecto nuevo (`init`), se aplique un retrofit (`retrofit`), o se actualice (`update`) mediante la meta-skill `/project-init`, el agente DEBE ejecutar automáticamente el registro en este catálogo:",
        "> ```bash",
        "> python3 /home/ibernabel/.agents/scripts/register_project.py --path .",
        "> ```",
        "> Esto garantiza que el inventario se mantenga siempre sincronizado con el 100% de los proyectos bajo el Framework ASD.",
        "",
    ])

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[✓] Catálogo Markdown actualizado en {MD_PATH}")


def main():
    parser = argparse.ArgumentParser(description="ASD Framework - Project Catalog Utility")
    parser.add_argument("--path", help="Project path to register or update")
    parser.add_argument("--id", help="Unique identifier for the project")
    parser.add_argument("--name", help="Display name of the project")
    parser.add_argument("--domain", choices=["software", "admin", "content", "video", "ai-agent", "multi-vertical"], help="ASD Domain")
    parser.add_argument("--pii", choices=["financial", "standard", "false"], help="PII classification")
    parser.add_argument("--status", choices=["active", "pending_retrofit", "pending_init"], help="Adoption status")
    parser.add_argument("--description", help="Short project description")
    parser.add_argument("--stack", action="append", help="Technology stack items")
    parser.add_argument("--tag", action="append", help="Propagation tags")
    parser.add_argument("--rebuild-md", action="store_true", help="Re-render PROJECTS.md from projects.json")
    parser.add_argument("--list", action="store_true", help="List registered projects")

    args = parser.parse_args()
    data = load_projects()

    if args.rebuild_md:
        render_markdown(data)
        return

    if args.list:
        print(f"Total projects: {len(data.get('projects', []))}")
        for p in data.get("projects", []):
            print(f"- [{p.get('id')}] {p.get('name')} ({p.get('domain')}) -> {p.get('linux_path')} [{p.get('status')}]")
        return

    if not args.path:
        parser.print_help()
        sys.exit(1)

    abs_path = os.path.abspath(os.path.expanduser(args.path))
    auto_info = detect_project_info(abs_path)

    project_id = args.id or os.path.basename(abs_path)
    name = args.name or project_id.replace("-", " ").replace("_", " ").title()

    existing = next((p for p in data["projects"] if p.get("id") == project_id or p.get("linux_path") == abs_path), None)

    if existing:
        print(f"[*] Updating existing project: {project_id}")
        existing["name"] = args.name or existing.get("name", name)
        existing["domain"] = args.domain or existing.get("domain", auto_info["domain"])
        existing["pii"] = args.pii or existing.get("pii", auto_info["pii"])
        existing["status"] = args.status or auto_info["status"]
        if auto_info.get("git_remote"):
            existing["git_remote"] = auto_info["git_remote"]
        if args.description:
            existing["description"] = args.description
        if args.stack:
            existing["stack"] = list(set(existing.get("stack", []) + args.stack))
        elif auto_info["stack"]:
            existing["stack"] = list(set(existing.get("stack", []) + auto_info["stack"]))
        if args.tag:
            existing["tags"] = list(set(existing.get("tags", []) + args.tag))
    else:
        print(f"[*] Adding new project: {project_id}")
        new_proj = {
            "id": project_id,
            "name": name,
            "linux_path": auto_info["linux_path"],
            "windows_path": auto_info["windows_path"],
            "git_remote": auto_info.get("git_remote", ""),
            "domain": args.domain or auto_info["domain"],
            "status": args.status or auto_info["status"],
            "pii": args.pii or auto_info["pii"],
            "description": args.description or "",
            "stack": list(set((args.stack or []) + auto_info["stack"])),
            "tags": args.tag or ["all", args.domain or auto_info["domain"]],
        }
        if "symlink_path" in auto_info:
            new_proj["symlink_path"] = auto_info["symlink_path"]
        data["projects"].append(new_proj)

    save_projects(data)
    print(f"[✓] Project {project_id} successfully saved to {JSON_PATH} and {MD_PATH}")


if __name__ == "__main__":
    main()
