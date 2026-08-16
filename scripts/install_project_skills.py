#!/usr/bin/env python3
"""
Install / Link Project Skills and Workflows for ASD Framework v2.
Reads deterministic presets from ~/.agents/templates/skills/presets.json,
verifies against ~/.agents/skills/, creates symlinks in <project>/.agents/skills/,
creates symlinks for global workflows in <project>/.agents/workflows/ (excluding project-init.md),
and automatically synchronizes the ## Auto-invoke Skills table in <project>/.agents/AGENTS.md.
"""

import argparse
import glob
import json
import os
import re
import shutil
import sys

GLOBAL_AGENTS_DIR = os.path.expanduser("~/.agents")
GLOBAL_SKILLS_DIR = os.path.join(GLOBAL_AGENTS_DIR, "skills")
GLOBAL_WORKFLOWS_DIR = os.path.join(GLOBAL_AGENTS_DIR, "workflows")
PRESETS_FILE = os.path.join(GLOBAL_AGENTS_DIR, "templates", "skills", "presets.json")

# Workflows that are strictly global/meta and must not exist locally in projects
EXCLUDED_PROJECT_WORKFLOWS = {"project-init.md"}


def load_presets():
    """Load skill presets from presets.json."""
    if not os.path.exists(PRESETS_FILE):
        return {}
    with open(PRESETS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("presets", {})


def extract_skill_trigger_desc(skill_name):
    """Extract a concise trigger / description from the skill's SKILL.md."""
    skill_md = os.path.join(GLOBAL_SKILLS_DIR, skill_name, "SKILL.md")
    if not os.path.exists(skill_md):
        return f"Assistance with {skill_name}"

    try:
        with open(skill_md, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Check YAML frontmatter description
        if content.startswith("---"):
            fm_parts = content.split("---", 2)
            if len(fm_parts) >= 3:
                fm = fm_parts[1]
                match = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
                if match:
                    desc = match.group(1).strip().strip('"\'')
                    if len(desc) > 90:
                        desc = desc[:87] + "..."
                    return desc

        # Check blockquote under title
        bq_match = re.search(r"^>\s*(.+)$", content, re.MULTILINE)
        if bq_match:
            desc = bq_match.group(1).strip()
            if len(desc) > 90:
                desc = desc[:87] + "..."
            return desc

        # Fallback to first text line
        lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        if lines:
            desc = lines[0]
            if len(desc) > 90:
                desc = desc[:87] + "..."
            return desc

    except Exception:
        pass

    return f"Trigger: when working on {skill_name} tasks"


def resolve_skills(domain, stacks=None, extra_skills=None):
    """Resolve the list of skills to install based on preset and stacks."""
    presets = load_presets()
    preset = presets.get(domain, {})
    skills_set = set(preset.get("default_preset_skills", []))

    if not skills_set:
        skills_set = set(preset.get("essential_skills", []))

    # Add stack specific skills
    stack_dict = preset.get("stack_skills", {})
    if stacks:
        for stack in stacks:
            for item in stack_dict.get(stack, []):
                skills_set.add(item)

    # Add extra skills
    if extra_skills:
        for s in extra_skills:
            if s.strip():
                skills_set.add(s.strip())

    return sorted(list(skills_set))


def sync_agents_md(project_dir, installed_skills):
    """Update the Auto-invoke Skills table in <project>/.agents/AGENTS.md."""
    agents_md_path = os.path.join(project_dir, ".agents", "AGENTS.md")
    if not os.path.exists(agents_md_path):
        print(f"[!] Warning: {agents_md_path} not found. Skipping AGENTS.md sync.")
        return False

    with open(agents_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Build new Markdown table
    table_lines = [
        "## Auto-invoke Skills\n",
        "| Skill | Trigger |",
        "|-------|---------|",
    ]

    for skill in sorted(installed_skills):
        desc = extract_skill_trigger_desc(skill)
        desc = desc.replace("|", "/")
        table_lines.append(f"| `{skill}` | {desc} |")

    new_table_str = "\n".join(table_lines) + "\n"

    # Replace existing table or append
    pattern = re.compile(r"## Auto-invoke Skills.*?(?=\n## |\Z)", re.DOTALL)
    if pattern.search(content):
        updated_content = pattern.sub(new_table_str, content)
    else:
        updated_content = content.rstrip() + "\n\n" + new_table_str

    with open(agents_md_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"[+] Updated {agents_md_path} Auto-invoke table with {len(installed_skills)} skills.")
    return True


def link_project_workflows(project_dir, dry_run=False):
    """Symlink global workflows into <project>/.agents/workflows/ and remove outdated copies."""
    target_wf_dir = os.path.join(project_dir, ".agents", "workflows")
    if not os.path.exists(GLOBAL_WORKFLOWS_DIR):
        print(f"[!] Global workflows directory {GLOBAL_WORKFLOWS_DIR} not found.")
        return []

    if not dry_run:
        os.makedirs(target_wf_dir, exist_ok=True)

    # 1. Clean up excluded/meta workflows (e.g. project-init.md should only live globally)
    for excl in EXCLUDED_PROJECT_WORKFLOWS:
        local_excl_path = os.path.join(target_wf_dir, excl)
        if os.path.islink(local_excl_path) or os.path.exists(local_excl_path):
            if not dry_run:
                if os.path.islink(local_excl_path):
                    os.unlink(local_excl_path)
                elif os.path.isdir(local_excl_path):
                    shutil.rmtree(local_excl_path)
                else:
                    os.remove(local_excl_path)
                print(f"[-] Removed local copy of global-only workflow: {local_excl_path}")
            else:
                print(f"  [DRY-RUN] rm {local_excl_path}")

    # 2. Symlink global workflows into project
    global_wfs = [f for f in os.listdir(GLOBAL_WORKFLOWS_DIR) if f.endswith(".md") and f not in EXCLUDED_PROJECT_WORKFLOWS]
    linked_wfs = []

    for wf_file in sorted(global_wfs):
        src_path = os.path.join(GLOBAL_WORKFLOWS_DIR, wf_file)
        dest_path = os.path.join(target_wf_dir, wf_file)

        if dry_run:
            print(f"  [DRY-RUN] ln -sfn {src_path} -> {dest_path}")
            linked_wfs.append(wf_file)
        else:
            try:
                if os.path.islink(dest_path) or os.path.exists(dest_path):
                    if os.path.islink(dest_path):
                        os.unlink(dest_path)
                    elif os.path.isdir(dest_path):
                        shutil.rmtree(dest_path)
                    else:
                        os.remove(dest_path)

                os.symlink(src_path, dest_path)
                linked_wfs.append(wf_file)
            except Exception as e:
                print(f"[!] Error symlinking workflow '{wf_file}': {e}", file=sys.stderr)

    print(f"[✓] Successfully linked {len(linked_wfs)} global workflows into {target_wf_dir}")
    return linked_wfs


def install_project_skills(project_dir, domain, stacks=None, extra_skills=None, dry_run=False, sync_md=True, link_wf=True):
    """Install skills and workflows via symlinks into <project>/.agents/."""
    target_skills_dir = os.path.join(project_dir, ".agents", "skills")
    resolved = resolve_skills(domain, stacks, extra_skills)

    if not resolved:
        print(f"[!] No skills resolved for domain '{domain}'.")
        return []

    print(f"[*] Target Project: {project_dir}")
    print(f"[*] Domain: {domain} | Resolved Skills: {len(resolved)}")

    missing_global = []
    installed = []

    if not dry_run:
        os.makedirs(target_skills_dir, exist_ok=True)

    for skill in resolved:
        global_skill_path = os.path.join(GLOBAL_SKILLS_DIR, skill)
        if not os.path.exists(global_skill_path):
            missing_global.append(skill)
            continue

        target_link_path = os.path.join(target_skills_dir, skill)
        if dry_run:
            print(f"  [DRY-RUN] ln -sfn {global_skill_path} -> {target_link_path}")
            installed.append(skill)
        else:
            try:
                if os.path.islink(target_link_path) or os.path.exists(target_link_path):
                    if os.path.islink(target_link_path):
                        os.unlink(target_link_path)
                    elif os.path.isdir(target_link_path):
                        shutil.rmtree(target_link_path)
                    else:
                        os.remove(target_link_path)

                os.symlink(global_skill_path, target_link_path)
                installed.append(skill)
            except Exception as e:
                print(f"[!] Error creating symlink for '{skill}': {e}", file=sys.stderr)

    if missing_global:
        print(f"\n[⚠️ Warning] The following {len(missing_global)} skills are not installed in ~/.agents/skills/:")
        for m in missing_global:
            print(f"    - {m}")
        print("    -> Run: python3 ~/.agents/scripts/skill_registry.py search <name> to find and install them.\n")

    print(f"[✓] Successfully linked {len(installed)} skills into {target_skills_dir}")

    if link_wf:
        link_project_workflows(project_dir, dry_run=dry_run)

    if sync_md and not dry_run:
        sync_agents_md(project_dir, installed)

    return installed


def main():
    parser = argparse.ArgumentParser(description="Deterministic Skill & Workflow Linker for ASD Projects")
    parser.add_argument("--project-dir", default=".", help="Project root directory (default: current dir)")
    parser.add_argument(
        "--domain",
        choices=["software", "admin", "ai-agent", "content", "video"],
        help="Project domain category",
    )
    parser.add_argument("--stack", action="append", help="Technology stack flavors (e.g. typescript, frontend, backend, python)")
    parser.add_argument("--skill", action="append", dest="extra_skills", help="Specific extra skill(s) to include")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing files")
    parser.add_argument("--no-sync-md", action="store_true", help="Do not update AGENTS.md Auto-invoke table")
    parser.add_argument("--no-workflows", action="store_true", help="Skip linking workflows")
    parser.add_argument("--workflows-only", action="store_true", help="Only symlink global workflows without modifying skills")

    args = parser.parse_args()
    project_dir = os.path.abspath(args.project_dir)

    if args.workflows_only:
        link_project_workflows(project_dir=project_dir, dry_run=args.dry_run)
        return

    if not args.domain:
        parser.error("--domain is required unless --workflows-only is specified.")

    install_project_skills(
        project_dir=project_dir,
        domain=args.domain,
        stacks=args.stack,
        extra_skills=args.extra_skills,
        dry_run=args.dry_run,
        sync_md=not args.no_sync_md,
        link_wf=not args.no_workflows,
    )


if __name__ == "__main__":
    main()
