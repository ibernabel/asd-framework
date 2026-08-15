#!/usr/bin/env python3
"""
Install / Link Project Skills for ASD Framework v2.
Reads deterministic presets from ~/.agents/templates/skills/presets.json,
verifies against ~/.agents/skills/, creates symlinks in <project>/.agents/skills/,
and automatically synchronizes the ## Auto-invoke Skills table in <project>/.agents/AGENTS.md.
"""

import argparse
import json
import os
import re
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
                    # Trim to concise trigger phrase
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

        # Fallback to first section
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
        # Sanitize pipe chars in description
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


def install_project_skills(project_dir, domain, stacks=None, extra_skills=None, dry_run=False, sync_md=True):
    """Install skills via symlinks into <project>/.agents/skills/."""
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
                # Remove if existing symlink/file
                if os.path.islink(target_link_path) or os.path.exists(target_link_path):
                    if os.path.islink(target_link_path):
                        os.unlink(target_link_path)
                    elif os.path.isdir(target_link_path):
                        import shutil
                        shutil.rmtree(target_link_path)
                    else:
                        os.remove(target_link_path)

                # Create symlink
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

    if sync_md and not dry_run:
        sync_agents_md(project_dir, installed)

    return installed


def main():
    parser = argparse.ArgumentParser(description="Deterministic Skill Linker for ASD Projects")
    parser.add_argument("--project-dir", default=".", help="Project root directory (default: current dir)")
    parser.add_argument(
        "--domain",
        required=True,
        choices=["software", "admin", "ai-agent", "content", "video"],
        help="Project domain category",
    )
    parser.add_argument("--stack", action="append", help="Technology stack flavors (e.g. typescript, frontend, backend, python)")
    parser.add_argument("--skill", action="append", dest="extra_skills", help="Specific extra skill(s) to include")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing files")
    parser.add_argument("--no-sync-md", action="store_true", help="Do not update AGENTS.md Auto-invoke table")

    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_dir)
    install_project_skills(
        project_dir=project_dir,
        domain=args.domain,
        stacks=args.stack,
        extra_skills=args.extra_skills,
        dry_run=args.dry_run,
        sync_md=not args.no_sync_md,
    )


if __name__ == "__main__":
    main()
