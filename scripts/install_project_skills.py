#!/usr/bin/env python3
"""
Install / Copy Project Skills for ASD Framework v2.
Reads deterministic presets from ~/.agents/templates/skills/presets.json,
verifies against ~/.agents/skills/, installs physical copies in <project>/.agents/skills/
(replacing any legacy symlinks for full Antigravity/Claude Code/Codex compatibility),
and automatically synchronizes the ## Auto-invoke Skills table in <project>/.agents/AGENTS.md.

Note: Workflows (.agents/workflows/) are deprecated in favor of skills (.agents/skills/).
All meta-commands (code-pipeline, code-pipeline-lite, docs-and-sync, repo-sync, post-session-doc, etc.)
are now managed and copied as first-class skills.
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
PRESETS_FILE = os.path.join(GLOBAL_AGENTS_DIR, "templates", "skills", "presets.json")


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


def cleanup_legacy_workflows(project_dir, dry_run=False):
    """Clean up broken symlinks or report legacy workflows in <project>/.agents/workflows/."""
    target_wf_dir = os.path.join(project_dir, ".agents", "workflows")
    if not os.path.exists(target_wf_dir):
        return

    cleaned = []
    for item in os.listdir(target_wf_dir):
        item_path = os.path.join(target_wf_dir, item)
        # Check broken symlinks
        if os.path.islink(item_path) and not os.path.exists(item_path):
            if not dry_run:
                os.unlink(item_path)
            cleaned.append(item)

    if cleaned:
        action_label = "[DRY-RUN] Would remove" if dry_run else "Removed"
        print(f"[ℹ️] {action_label} {len(cleaned)} broken legacy workflow symlink(s) in {target_wf_dir}: {', '.join(cleaned)}")


def migrate_symlinks_in_project(project_dir, dry_run=False, sync_md=True):
    """Convert all existing symlinks in <project>/.agents/skills/ to physical copies."""
    target_skills_dir = os.path.join(project_dir, ".agents", "skills")
    if not os.path.exists(target_skills_dir):
        print(f"[!] {target_skills_dir} does not exist.")
        return []

    migrated = []
    failed = []
    items = sorted(os.listdir(target_skills_dir))
    for item in items:
        target_path = os.path.join(target_skills_dir, item)
        if os.path.islink(target_path):
            global_skill_path = os.path.join(GLOBAL_SKILLS_DIR, item)
            if not os.path.exists(global_skill_path):
                print(f"[⚠️ Warning] Global skill not found for symlink '{item}' ({global_skill_path})")
                failed.append(item)
                continue
            if dry_run:
                print(f"  [DRY-RUN] Would replace symlink '{item}' with physical copy from {global_skill_path}")
                migrated.append(item)
            else:
                try:
                    os.unlink(target_path)
                    shutil.copytree(global_skill_path, target_path, ignore_dangling_symlinks=True)
                    migrated.append(item)
                except Exception as e:
                    print(f"[!] Error migrating symlink for '{item}': {e}", file=sys.stderr)
                    failed.append(item)

    action_label = "[DRY-RUN] Would convert" if dry_run else "Converted"
    print(f"[✓] {action_label} {len(migrated)} symlink(s) to physical copies in {target_skills_dir}")
    if sync_md and not dry_run and migrated:
        current_skills = [d for d in os.listdir(target_skills_dir) if os.path.isdir(os.path.join(target_skills_dir, d))]
        sync_agents_md(project_dir, current_skills)
    return migrated


def install_project_skills(project_dir, domain, stacks=None, extra_skills=None, dry_run=False, sync_md=True, use_symlinks=False):
    """Install skills as physical copies into <project>/.agents/skills/."""
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

        target_path = os.path.join(target_skills_dir, skill)
        if dry_run:
            action = "ln -sfn" if use_symlinks else "copy"
            print(f"  [DRY-RUN] {action} {global_skill_path} -> {target_path}")
            installed.append(skill)
        else:
            try:
                if os.path.islink(target_path):
                    os.unlink(target_path)
                elif os.path.isdir(target_path):
                    shutil.rmtree(target_path)
                elif os.path.exists(target_path):
                    os.remove(target_path)

                if use_symlinks:
                    os.symlink(global_skill_path, target_path)
                else:
                    shutil.copytree(global_skill_path, target_path, ignore_dangling_symlinks=True)
                installed.append(skill)
            except Exception as e:
                print(f"[!] Error installing skill '{skill}': {e}", file=sys.stderr)

    if missing_global:
        print(f"\n[⚠️ Warning] The following {len(missing_global)} skills are not installed in ~/.agents/skills/:")
        for m in missing_global:
            print(f"    - {m}")
        print("    -> Run: python3 ~/.agents/scripts/skill_registry.py search <name> to find and install them.\n")

    mode_label = "symlinked" if use_symlinks else "copied"
    print(f"[✓] Successfully {mode_label} {len(installed)} skills into {target_skills_dir}")

    # Clean up any broken legacy workflow symlinks if directory exists
    cleanup_legacy_workflows(project_dir, dry_run=dry_run)

    if sync_md and not dry_run:
        sync_agents_md(project_dir, installed)

    return installed


def main():
    parser = argparse.ArgumentParser(description="Deterministic Skill Installer & Copier for ASD Projects")
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
    parser.add_argument("--migrate-symlinks", action="store_true", help="Convert all existing skill symlinks in project to physical copies")
    parser.add_argument("--symlink", action="store_true", help="Use symlinks instead of physical copies (not recommended)")
    # Deprecated workflow flags preserved for backwards compatibility
    parser.add_argument("--no-workflows", action="store_true", help="[Deprecated] Workflows are no longer used; skills are installed directly.")
    parser.add_argument("--workflows-only", action="store_true", help="[Deprecated] Workflows are no longer used; skills are installed directly.")

    args = parser.parse_args()
    project_dir = os.path.abspath(args.project_dir)

    if args.migrate_symlinks:
        migrate_symlinks_in_project(project_dir, dry_run=args.dry_run, sync_md=not args.no_sync_md)
        return

    if args.workflows_only:
        print("[ℹ️] Workflows are deprecated in favor of skills (.agents/skills/).")
        print("    All meta-commands are now installed as skills. Run with --domain to install skills.")
        cleanup_legacy_workflows(project_dir, dry_run=args.dry_run)
        return

    if not args.domain:
        parser.error("--domain is required (unless using --migrate-symlinks).")

    install_project_skills(
        project_dir=project_dir,
        domain=args.domain,
        stacks=args.stack,
        extra_skills=args.extra_skills,
        dry_run=args.dry_run,
        sync_md=not args.no_sync_md,
        use_symlinks=args.symlink,
    )


if __name__ == "__main__":
    main()
