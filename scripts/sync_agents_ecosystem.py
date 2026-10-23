#!/usr/bin/env python3
"""
Sync Agents Ecosystem for ASD Framework.
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
FRAMEWORK_REPO_DIR = os.path.expanduser("~/develop/asd-framework")

PIPELINE_AGENTS = [
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

COUNCIL_AGENTS = [
    "council-chairman",
    "council-contrarian",
    "council-executor",
    "council-expansionist",
    "council-first-principles",
    "council-outsider",
]

ALL_PROJECT_AGENTS = PIPELINE_AGENTS + COUNCIL_AGENTS

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

    # 1. Agents pool (pipeline agents only)
    dest_agents = os.path.join(FRAMEWORK_REPO_DIR, "agents")
    synced = 0
    for agent in PIPELINE_AGENTS:
        src_agent_dir = os.path.join(GLOBAL_AGENTS_POOL_DIR, agent)
        dest_agent_dir = os.path.join(dest_agents, agent)
        if os.path.exists(src_agent_dir):
            synced += sync_directory_files(src_agent_dir, dest_agent_dir, dry_run=dry_run)
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


def push_framework_to_global(dry_run=False):
    """Synchronize files from asd-framework-public repo to canonical ~/.agents/."""
    print(f"\n[*] ─── Propagando Framework Público ({FRAMEWORK_REPO_DIR}) -> Global ({GLOBAL_AGENTS_DIR}) ───")
    if not os.path.exists(FRAMEWORK_REPO_DIR):
        print(f"[!] Framework repo not found at {FRAMEWORK_REPO_DIR}")
        return False

    total_synced = 0

    # 1. Templates
    src_templates = os.path.join(FRAMEWORK_REPO_DIR, "templates")
    synced = sync_directory_files(src_templates, GLOBAL_TEMPLATES_DIR, dry_run=dry_run)
    total_synced += synced
    print(f"  [+] Plantillas sincronizadas a {GLOBAL_TEMPLATES_DIR}: {synced} archivos")

    # 2. Scripts
    src_scripts = os.path.join(FRAMEWORK_REPO_DIR, "scripts")
    synced = sync_directory_files(src_scripts, GLOBAL_SCRIPTS_DIR, dry_run=dry_run)
    total_synced += synced
    print(f"  [+] Scripts sincronizados a {GLOBAL_SCRIPTS_DIR}: {synced} archivos")

    # 3. Agents pool
    src_agents = os.path.join(FRAMEWORK_REPO_DIR, "agents")
    synced = sync_directory_files(src_agents, GLOBAL_AGENTS_POOL_DIR, dry_run=dry_run)
    total_synced += synced
    print(f"  [+] Agentes sincronizados a {GLOBAL_AGENTS_POOL_DIR}: {synced} archivos")

    # 4. Meta-skills
    framework_skills_dir = os.path.join(FRAMEWORK_REPO_DIR, "skills")
    if os.path.exists(framework_skills_dir):
        for skill_name in os.listdir(framework_skills_dir):
            src_skill = os.path.join(framework_skills_dir, skill_name)
            dest_skill = os.path.join(GLOBAL_SKILLS_DIR, skill_name)
            if os.path.isdir(src_skill):
                synced = sync_directory_files(src_skill, dest_skill, dry_run=dry_run)
                total_synced += synced
        print(f"  [+] Meta-skills canónicas sincronizadas a {GLOBAL_SKILLS_DIR}")

    action = "[DRY-RUN] Simulación completa" if dry_run else "Propagación global completada"
    print(f"[✓] {action} ({total_synced} modificaciones aplicadas en {GLOBAL_AGENTS_DIR}).\n")
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


def update_project_agents_md(project_dir, dry_run=False):
    """Ensure project AGENTS.md references all 16 root agents."""
    agents_md = os.path.join(project_dir, ".agents", "AGENTS.md")
    if not os.path.exists(agents_md):
        return False

    try:
        with open(agents_md, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return False

    new_section = """### Agent Files Location
All 16 agents are hosted in root `~/.agents/agents/` and available locally in `.agents/agents/`:

#### 1. Full Pipeline (Uncle Bob — 7 Agents)
- `orchestrator/agent.md` — Coordinates the full pipeline (`/code-pipeline`)
- `specifier/agent.md` — Gherkin scenarios + QA test procedures
- `coder/agent.md` — TDD unit/integration tests + implementation
- `refactorer/agent.md` — Complexity reduction (CRAP ≤ 6) + DRY
- `architect/agent.md` — Mutation testing + coverage gate + architecture review
- `qa/agent.md` — QA execution, verification report + security audit
- `pii-verifier/agent.md` — PII scan (mandatory on financial projects)

#### 2. Lite Pipeline (Pragmatic — 3 Agents)
- `planner/agent.md` — Acceptance criteria & simple scenarios (`/code-pipeline-lite`)
- `implementer/agent.md` — Direct TDD implementation to green
- `reviewer/agent.md` — Pragmatic code quality, cleanup & security check

#### 3. The Council Deliberation Suite (6 Agents)
- `council-chairman/agent.md` — Moderation, peer-review & strategic verdict (`/ask-the-council`)
- `council-contrarian/agent.md` — Fatal flaws, hidden risks & failure modes
- `council-first-principles/agent.md` — Deconstruction of core axioms & root truth
- `council-expansionist/agent.md` — Asymmetric upside & 10x scale vectors
- `council-outsider/agent.md` — Unbiased common-sense & curse-of-knowledge check
- `council-executor/agent.md` — Tactical feasibility & Monday 9:00 AM action plan"""

    pattern = r"### Agent Files Location.*?(?=\n---|\n## |\Z)"
    if re.search(pattern, content, flags=re.DOTALL):
        updated_content = re.sub(pattern, new_section, content, count=1, flags=re.DOTALL)
        if updated_content != content:
            if dry_run:
                print(f"  [DRY-RUN] update Agent Files Location in {agents_md}")
            else:
                with open(agents_md, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"  [+] AGENTS.md actualizado con los 16 agentes en {agents_md}")
            return True
    return False


def sync_project_instance(project_dir, dry_run=False):
    """Synchronize pipeline agents and install skills in a project."""
    agents_dir = os.path.join(project_dir, ".agents")
    if not os.path.exists(agents_dir):
        return

    print(f"\n[*] ─── Actualizando Proyecto: {project_dir} ───")

    # 1. Update pipeline and council agents if .agents/agents exists or if project is software/technology
    project_agents_pool = os.path.join(agents_dir, "agents")
    if os.path.exists(project_agents_pool) or "technology" in project_dir or "software" in project_dir:
        os.makedirs(project_agents_pool, exist_ok=True)
        synced_agents = 0
        for agent in ALL_PROJECT_AGENTS:
            src_agent_dir = os.path.join(GLOBAL_AGENTS_POOL_DIR, agent)
            dest_agent_dir = os.path.join(project_agents_pool, agent)
            if os.path.exists(src_agent_dir):
                synced_agents += sync_directory_files(src_agent_dir, dest_agent_dir, dry_run=dry_run)
        print(f"  [+] Agentes del root (~/.agents/agents): {synced_agents} archivos actualizados en {project_agents_pool}")

    # 2. Update AGENTS.md Agent Files Location
    update_project_agents_md(project_dir, dry_run=dry_run)

    # 3. Re-run install_project_skills.py to install physical copies and update AGENTS.md
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
    parser = argparse.ArgumentParser(description="ASD Framework Ecosystem Synchronizer")
    parser.add_argument("--dry-run", action="store_true", help="Simulate synchronization without modifying files")
    parser.add_argument("--catalog", action="store_true", help="Read project directories from ~/.agents/projects.json")
    parser.add_argument("--no-framework-repo", action="store_true", help="Skip synchronizing asd-framework-public repo")
    parser.add_argument("--push-to-global", action="store_true", help="Propagate changes from asd-framework-public to canonical ~/.agents/")
    parser.add_argument("--project-dir", action="append", help="Specific project directory to synchronize")
    parser.add_argument("--scan-root", action="append", help="Root directory to scan for .agents/ projects")

    args = parser.parse_args()

    print("════════════════════════════════════════════════════════════════")
    print("  ASD Framework — Global Agent Ecosystem Synchronizer")
    print("════════════════════════════════════════════════════════════════")

    if args.push_to_global:
        push_framework_to_global(dry_run=args.dry_run)
        return

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

    # Also load catalog projects from projects.json
    catalog_file = os.path.join(GLOBAL_AGENTS_DIR, "projects.json")
    if os.path.exists(catalog_file):
        try:
            with open(catalog_file, "r", encoding="utf-8") as cf:
                cdata = json.load(cf)
                for proj in cdata.get("projects", []):
                    lpath = proj.get("linux_path")
                    if lpath and os.path.exists(lpath) and os.path.exists(os.path.join(lpath, ".agents")):
                        all_targets.add(os.path.abspath(lpath))
        except Exception as e:
            print(f"[!] Error leyendo {catalog_file}: {e}")

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
