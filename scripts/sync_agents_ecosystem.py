#!/usr/bin/env python3
"""
Sync Agents Ecosystem for ASD Framework v2.
Propagates updated pipeline agents, skills, templates, and UI/UX validation tooling
from canonical ~/.agents/ to:
1. The public framework repository: ~/.agents/asd-framework-public/
2. All registered and discovered projects with .agents/ directories in the workspace.

Preserves custom project rules, conventions, and git histories.
"""

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys

GLOBAL_AGENTS_DIR = os.path.expanduser("~/.agents")
GLOBAL_SKILLS_DIR = os.path.join(GLOBAL_AGENTS_DIR, "skills")
GLOBAL_AGENTS_POOL_DIR = os.path.join(GLOBAL_AGENTS_DIR, "agents")
GLOBAL_TEMPLATES_DIR = os.path.join(GLOBAL_AGENTS_DIR, "templates")
GLOBAL_SCRIPTS_DIR = os.path.join(GLOBAL_AGENTS_DIR, "scripts")
FRAMEWORK_REPO_DIR = os.path.join(GLOBAL_AGENTS_DIR, "asd-framework-public")

ALL_10_AGENTS = [
    "orchestrator",
    "specifier",
    "coder",
    "refactorer",
    "architect",
    "qa",
    "pii-verifier",
    "planner",
    "implementer",
    "reviewer",
]

DEFAULT_PROJECT_DIRS = [
    os.path.expanduser("~/develop/consultor"),
    os.path.expanduser("~/develop/consultor/admin"),
    os.path.expanduser("~/develop/consultor/content"),
    os.path.expanduser("~/develop/consultor/technology"),
    os.path.expanduser("~/admin"),
    os.path.expanduser("~/content"),
    os.path.expanduser("~/technology"),
]


def sync_directory_files(src_dir, dest_dir, dry_run=False, delete_extraneous=False):
    """Synchronize files and subdirectories from src_dir to dest_dir."""
    if not os.path.exists(src_dir):
        print(f"[!] Source directory not found: {src_dir}")
        return 0

    if not os.path.exists(dest_dir):
        if dry_run:
            print(f"  [DRY-RUN] mkdir -p {dest_dir}")
        else:
            os.makedirs(dest_dir, exist_ok=True)

    copied = 0
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        target_root = os.path.join(dest_dir, rel_path)

        for d in dirs:
            target_sub = os.path.join(target_root, d)
            if not os.path.exists(target_sub):
                if dry_run:
                    print(f"  [DRY-RUN] mkdir -p {target_sub}")
                else:
                    os.makedirs(target_sub, exist_ok=True)

        for f in files:
            src_file = os.path.join(root, f)
            dest_file = os.path.join(target_root, f)

            should_copy = False
            if not os.path.exists(dest_file):
                should_copy = True
            else:
                # Compare modified time or content
                try:
                    with open(src_file, "rb") as sf, open(dest_file, "rb") as df:
                        if sf.read() != df.read():
                            should_copy = True
                except Exception:
                    should_copy = True

            if should_copy:
                if dry_run:
                    print(f"  [DRY-RUN] cp {src_file} -> {dest_file}")
                else:
                    shutil.copy2(src_file, dest_file)
                copied += 1

    return copied


def sync_framework_repo(dry_run=False):
    """Synchronize canonical files from ~/.agents to asd-framework-public repo."""
    print(f"\n[*] ─── Sincronizando Framework ASD Público ({FRAMEWORK_REPO_DIR}) ───")
    if not os.path.exists(FRAMEWORK_REPO_DIR):
        print(f"[!] Framework repo not found at {FRAMEWORK_REPO_DIR}")
        return False

    total_synced = 0

    # 1. Agents pool (all 10 agents)
    dest_agents = os.path.join(FRAMEWORK_REPO_DIR, "agents")
    synced = sync_directory_files(GLOBAL_AGENTS_POOL_DIR, dest_agents, dry_run=dry_run)
    total_synced += synced
    print(f"  [+] Agentes del pipeline: {synced} archivos actualizados en {dest_agents}")

    # 2. Templates (skills presets, software-dev-agents, gitignore, etc.)
    dest_templates = os.path.join(FRAMEWORK_REPO_DIR, "templates")
    synced = sync_directory_files(GLOBAL_TEMPLATES_DIR, dest_templates, dry_run=dry_run)
    total_synced += synced
    print(f"  [+] Plantillas y presets: {synced} archivos actualizados en {dest_templates}")

    # 3. Scripts
    dest_scripts = os.path.join(FRAMEWORK_REPO_DIR, "scripts")
    synced = sync_directory_files(GLOBAL_SCRIPTS_DIR, dest_scripts, dry_run=dry_run)
    total_synced += synced
    print(f"  [+] Scripts: {synced} archivos actualizados en {dest_scripts}")

    # 4. Canonical meta-skills that live in framework repo
    framework_skills_dir = os.path.join(FRAMEWORK_REPO_DIR, "skills")
    if os.path.exists(framework_skills_dir):
        for skill_name in os.listdir(framework_skills_dir):
            src_skill = os.path.join(GLOBAL_SKILLS_DIR, skill_name)
            dest_skill = os.path.join(framework_skills_dir, skill_name)
            if os.path.isdir(src_skill):
                synced = sync_directory_files(src_skill, dest_skill, dry_run=dry_run)
                total_synced += synced
        print(f"  [+] Meta-skills canónicas sincronizadas en {framework_skills_dir}")

    action = "[DRY-RUN] Simulación completa" if dry_run else "Sincronización completada"
    print(f"[✓] {action} para asd-framework-public ({total_synced} modificaciones detectadas).\n")
    return True


def discover_project_dirs(scan_roots):
    """Find directories containing .agents/ under scan_roots."""
    found = set()
    for root_dir in scan_roots:
        if not os.path.exists(root_dir):
            continue
        for root, dirs, _ in os.walk(root_dir):
            # Do not traverse into node_modules, .git, venv, cache
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv", "__pycache__", ".codegraph", "dist", "build")]
            if ".agents" in dirs and root != GLOBAL_AGENTS_DIR and root != FRAMEWORK_REPO_DIR:
                found.add(os.path.abspath(root))
    return sorted(list(found))


def sync_project_instance(project_dir, dry_run=False):
    """Synchronize pipeline agents and install skills in a project."""
    agents_dir = os.path.join(project_dir, ".agents")
    if not os.path.exists(agents_dir):
        return

    print(f"\n[*] ─── Actualizando Proyecto: {project_dir} ───")

    # 1. Update pipeline agents if .agents/agents exists or if project is software/technology
    project_agents_pool = os.path.join(agents_dir, "agents")
    if os.path.exists(project_agents_pool) or "technology" in project_dir or "software" in project_dir:
        os.makedirs(project_agents_pool, exist_ok=True)
        synced_agents = 0
        for agent in ALL_10_AGENTS:
            src_agent_dir = os.path.join(GLOBAL_AGENTS_POOL_DIR, agent)
            dest_agent_dir = os.path.join(project_agents_pool, agent)
            if os.path.exists(src_agent_dir):
                synced_agents += sync_directory_files(src_agent_dir, dest_agent_dir, dry_run=dry_run)
        print(f"  [+] Agentes de pipeline: {synced_agents} archivos actualizados en {project_agents_pool}")

    # 2. Re-run install_project_skills.py to install physical copies and update AGENTS.md
    installer_script = os.path.join(GLOBAL_SCRIPTS_DIR, "install_project_skills.py")
    if os.path.exists(installer_script):
        # Determine domain
        domain = "software"
        if "admin" in project_dir.lower():
            domain = "admin"
        elif "content" in project_dir.lower():
            domain = "content"
        elif "video" in project_dir.lower():
            domain = "video"
        elif "ai" in project_dir.lower():
            domain = "ai-agent"

        cmd = [
            sys.executable,
            installer_script,
            "--project-dir",
            project_dir,
            "--domain",
            domain,
        ]
        if domain == "software":
            cmd.extend(["--stack", "frontend", "--stack", "typescript", "--skill", "impeccable"])

        if dry_run:
            cmd.append("--dry-run")

        print(f"  [*] Ejecutando instalador de skills ({domain})...")
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            for line in res.stdout.splitlines():
                if line.startswith("[✓]") or line.startswith("[+]") or line.startswith("[!]"):
                    print(f"    {line}")
        except Exception as e:
            print(f"  [!] Error ejecutando install_project_skills: {e}")


def main():
    parser = argparse.ArgumentParser(description="ASD Framework v2 Ecosystem Synchronizer")
    parser.add_argument("--dry-run", action="store_true", help="Simulate synchronization without modifying files")
    parser.add_argument("--no-framework-repo", action="store_true", help="Skip synchronizing asd-framework-public repo")
    parser.add_argument("--project-dir", action="append", help="Specific project directory to synchronize")
    parser.add_argument("--scan-root", action="append", help="Root directory to scan for .agents/ projects")

    args = parser.parse_args()

    print("════════════════════════════════════════════════════════════════")
    print("  ASD Framework v2 — Global Agent Ecosystem Synchronizer")
    print("════════════════════════════════════════════════════════════════")

    # Step 1: Sync Framework Public Repo
    if not args.no_framework_repo:
        sync_framework_repo(dry_run=args.dry_run)

    # Step 2: Determine target project directories
    scan_roots = [os.path.expanduser("~/develop")]
    if args.scan_root:
        scan_roots.extend(args.scan_root)

    discovered = discover_project_dirs(scan_roots)
    all_targets = set(discovered)

    for p in DEFAULT_PROJECT_DIRS:
        if os.path.exists(p) and os.path.exists(os.path.join(p, ".agents")):
            all_targets.add(os.path.abspath(p))

    if args.project_dir:
        for p in args.project_dir:
            all_targets.add(os.path.abspath(p))

    sorted_targets = sorted(list(all_targets))
    print(f"[*] Proyectos detectados para sincronización ({len(sorted_targets)}):")
    for t in sorted_targets:
        print(f"    - {t}")

    # Step 3: Sync each project
    for target in sorted_targets:
        sync_project_instance(target, dry_run=args.dry_run)

    print("\n[✓] Sincronización del ecosistema completada exitosamente.")


if __name__ == "__main__":
    main()
