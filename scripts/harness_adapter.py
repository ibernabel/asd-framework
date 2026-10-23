#!/usr/bin/env python3
"""
Universal AI Harness Adapter for ASD Framework.

Generates, validates, and synchronizes harness configuration files ensuring
full out-of-the-box compatibility across:
- Google Antigravity (.agents/AGENTS.md, physical skills)
- Claude Code (CLAUDE.md, .claude/commands/*.md)
- OpenAI Codex & Open Standard (root AGENTS.md)
- Cursor (.cursorrules, .cursor/rules/asd-framework.mdc)
- Windsurf (.windsurfrules)
- GitHub Copilot (.github/copilot-instructions.md)
"""

import argparse
import os
import shutil
import sys

# Ensure UTF-8 output even on Windows command prompts with legacy charmaps
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GLOBAL_AGENTS_DIR = os.path.expanduser("~/.agents")
GLOBAL_TEMPLATES_DIR = os.path.join(GLOBAL_AGENTS_DIR, "templates", "harnesses")
REPO_TEMPLATES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "templates", "harnesses")


def get_templates_dir():
    """Locate the harness templates directory (global ~/.agents or repo-local)."""
    if os.path.isdir(GLOBAL_TEMPLATES_DIR):
        return GLOBAL_TEMPLATES_DIR
    if os.path.isdir(REPO_TEMPLATES_DIR):
        return REPO_TEMPLATES_DIR
    return None


def copy_or_create(src_path, dest_path, dry_run=False, force=False):
    """Copy template to destination if missing or if force is enabled."""
    if os.path.exists(dest_path) and not force:
        return False, "already exists"

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        if dry_run:
            print(f"  [DRY-RUN] mkdir -p {dest_dir}")
        else:
            os.makedirs(dest_dir, exist_ok=True)

    if not os.path.exists(src_path):
        return False, f"source template not found: {src_path}"

    if dry_run:
        print(f"  [DRY-RUN] cp {src_path} -> {dest_path}")
        return True, "simulated copy"

    try:
        shutil.copy2(src_path, dest_path)
        return True, "installed"
    except Exception as e:
        return False, f"error: {e}"


def install_harness_adapters(project_dir, domain="software", dry_run=False, force=False):
    """
    Install or update all AI harness configuration files in target project.
    Returns dict of {harness_target: status_message}.
    """
    templates_dir = get_templates_dir()
    if not templates_dir:
        print("[!] Error: Harness templates directory not found.", file=sys.stderr)
        return {}

    project_dir = os.path.abspath(project_dir)
    results = {}

    harness_files = [
        # (template_relative_path, project_relative_path, description)
        ("AGENTS.md", "AGENTS.md", "Open Standard / Codex root manifest"),
        ("CLAUDE.md", "CLAUDE.md", "Claude Code project instructions"),
        (".cursorrules", ".cursorrules", "Cursor legacy/universal rules"),
        ("cursor-rule.mdc", os.path.join(".cursor", "rules", "asd-framework.mdc"), "Cursor Rules 2.0"),
        (".windsurfrules", ".windsurfrules", "Windsurf Cascade rules"),
        ("copilot-instructions.md", os.path.join(".github", "copilot-instructions.md"), "GitHub Copilot instructions"),
    ]

    for tmpl_rel, proj_rel, desc in harness_files:
        src = os.path.join(templates_dir, tmpl_rel)
        dest = os.path.join(project_dir, proj_rel)
        success, msg = copy_or_create(src, dest, dry_run=dry_run, force=force)
        results[proj_rel] = {"success": success, "status": msg, "description": desc}

    # Install Claude Code custom slash commands
    claude_cmd_tmpl_dir = os.path.join(templates_dir, "claude-commands")
    claude_cmd_dest_dir = os.path.join(project_dir, ".claude", "commands")

    if os.path.isdir(claude_cmd_tmpl_dir):
        for cmd_file in os.listdir(claude_cmd_tmpl_dir):
            if cmd_file.endswith(".md"):
                src = os.path.join(claude_cmd_tmpl_dir, cmd_file)
                dest = os.path.join(claude_cmd_dest_dir, cmd_file)
                rel_key = os.path.join(".claude", "commands", cmd_file)
                success, msg = copy_or_create(src, dest, dry_run=dry_run, force=force)
                results[rel_key] = {"success": success, "status": msg, "description": f"Claude command: /{cmd_file[:-3]}"}

    return results


def validate_harness_compatibility(project_dir):
    """
    Validate presence and readiness of configuration files across all supported harnesses.
    Returns (overall_status: bool, report: dict).
    """
    project_dir = os.path.abspath(project_dir)
    harnesses = {
        "Google Antigravity": {
            "files": [os.path.join(".agents", "AGENTS.md")],
            "optional": False,
            "purpose": "Native ASD agent definitions and execution scopes",
        },
        "OpenAI Codex / Open Standard": {
            "files": ["AGENTS.md"],
            "optional": False,
            "purpose": "Root manifest conforming to the open AGENTS.md specification",
        },
        "Claude Code": {
            "files": ["CLAUDE.md"],
            "recommended": [
                os.path.join(".claude", "commands", "code-pipeline.md"),
                os.path.join(".claude", "commands", "repo-sync.md"),
            ],
            "optional": False,
            "purpose": "Project memory and custom slash commands for Claude Code CLI",
        },
        "Cursor": {
            "files": [".cursorrules", os.path.join(".cursor", "rules", "asd-framework.mdc")],
            "match_any": True,
            "optional": False,
            "purpose": "Cursor Composer / Chat rules and quality gate enforcement",
        },
        "Windsurf": {
            "files": [".windsurfrules"],
            "optional": False,
            "purpose": "Windsurf Cascade workflow rules",
        },
        "GitHub Copilot": {
            "files": [os.path.join(".github", "copilot-instructions.md")],
            "optional": False,
            "purpose": "GitHub Copilot Chat and Workspace instructions",
        },
    }

    report = {}
    all_passed = True

    for harness_name, config in harnesses.items():
        files = config["files"]
        match_any = config.get("match_any", False)
        found_files = []
        missing_files = []

        for f in files:
            full_path = os.path.join(project_dir, f)
            if os.path.exists(full_path):
                found_files.append(f)
            else:
                missing_files.append(f)

        if match_any:
            passed = len(found_files) > 0
        else:
            passed = len(missing_files) == 0

        # Check recommended files if applicable
        rec_found = []
        rec_missing = []
        for rf in config.get("recommended", []):
            full_path = os.path.join(project_dir, rf)
            if os.path.exists(full_path):
                rec_found.append(rf)
            else:
                rec_missing.append(rf)

        if not passed and not config.get("optional", False):
            all_passed = False

        report[harness_name] = {
            "passed": passed,
            "found": found_files,
            "missing": missing_files,
            "recommended_found": rec_found,
            "recommended_missing": rec_missing,
            "purpose": config["purpose"],
        }

    return all_passed, report


def print_validation_report(all_passed, report, project_dir):
    """Format and print an informative validation report."""
    print("\n" + "━" * 70)
    print(f"  ASD Multi-Harness Compatibility Audit: {project_dir}")
    print("━" * 70)

    for harness, data in report.items():
        icon = "✅" if data["passed"] else "❌"
        status = "COMPATIBLE" if data["passed"] else "MISSING CONFIG"
        print(f"\n{icon}  {harness} [{status}]")
        print(f"    Purpose: {data['purpose']}")
        if data["found"]:
            print(f"    Detected: {', '.join(data['found'])}")
        if data["missing"]:
            print(f"    Missing:  {', '.join(data['missing'])}")
        if data.get("recommended_missing"):
            print(f"    Recommended missing: {', '.join(data['recommended_missing'])}")

    print("\n" + "━" * 70)
    if all_passed:
        print("  ✅ All supported AI coding harnesses are fully configured.")
    else:
        print("  ⚠️  One or more harnesses require bridge configuration.")
        print("  Run: python3 scripts/harness_adapter.py --project-dir <path> to install.")
    print("━" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Universal AI Harness Adapter for ASD Framework")
    parser.add_argument("--project-dir", default=".", help="Target project root directory (default: current dir)")
    parser.add_argument("--domain", default="software", help="Project domain category")
    parser.add_argument("--validate", action="store_true", help="Validate harness compatibility without modifying files")
    parser.add_argument("--dry-run", action="store_true", help="Simulate installation without writing files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing harness files")

    args = parser.parse_args()
    project_dir = os.path.abspath(args.project_dir)

    if args.validate:
        all_passed, report = validate_harness_compatibility(project_dir)
        print_validation_report(all_passed, report, project_dir)
        sys.exit(0 if all_passed else 1)

    print(f"[*] Installing AI Harness Bridges for ASD Framework in: {project_dir}")
    results = install_harness_adapters(project_dir, domain=args.domain, dry_run=args.dry_run, force=args.force)

    for path, data in sorted(results.items()):
        status_icon = "✓" if data["success"] else "•"
        print(f"  [{status_icon}] {path} ({data['description']}): {data['status']}")

    # Run quick validation check after installation
    if not args.dry_run:
        all_passed, _ = validate_harness_compatibility(project_dir)
        if all_passed:
            print("\n[✓] All AI harnesses (Antigravity, Claude Code, Codex, Cursor, Windsurf, Copilot) are now compatible!")
        else:
            print("\n[!] Warning: Some harness files could not be confirmed. Run with --validate for details.")


if __name__ == "__main__":
    main()
