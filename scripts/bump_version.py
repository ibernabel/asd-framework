#!/usr/bin/env python3
"""
Bump version script for ASD Framework v2 projects.
Supports: patch, minor, major.
Updates VERSION, package.json / pyproject.toml, scaffolds/updates CHANGELOG.md,
and supports Git tagging conforming to SemVer and versioning-guide standards.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

VERSION_FILE = "VERSION"
PACKAGE_JSON = "package.json"
PYPROJECT_TOML = "pyproject.toml"
CHANGELOG_FILE = "CHANGELOG.md"


def get_current_version():
    """Retrieve current version from VERSION, package.json, or pyproject.toml."""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    elif os.path.exists(PACKAGE_JSON):
        with open(PACKAGE_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("version", "0.1.0")
    elif os.path.exists(PYPROJECT_TOML):
        with open(PYPROJECT_TOML, "r", encoding="utf-8") as f:
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', f.read())
            if match:
                return match.group(1)
    return "0.1.0"


def parse_version(ver_str):
    """Parse SemVer string into major, minor, patch integers."""
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", ver_str.strip())
    if not match:
        raise ValueError(f"Invalid SemVer format: {ver_str}. Expected X.Y.Z")
    return [int(x) for x in match.groups()]


def bump_version(ver_str, bump_type):
    """Calculate next version based on SemVer bump type."""
    major, minor, patch = parse_version(ver_str)
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Unknown bump type: {bump_type}. Use patch, minor, or major.")
    return f"{major}.{minor}.{patch}"


def update_version_files(new_version):
    """Update VERSION and manifest files."""
    # 1. Update VERSION file
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(f"{new_version}\n")
    print(f"[+] Updated {VERSION_FILE} -> {new_version}")

    # 2. Update package.json if present
    if os.path.exists(PACKAGE_JSON):
        try:
            with open(PACKAGE_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["version"] = new_version
            with open(PACKAGE_JSON, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                f.write("\n")
            print(f"[+] Updated {PACKAGE_JSON} -> {new_version}")
        except Exception as e:
            print(f"[!] Warning: Could not update package.json: {e}")

    # 3. Update pyproject.toml if present
    if os.path.exists(PYPROJECT_TOML):
        try:
            with open(PYPROJECT_TOML, "r", encoding="utf-8") as f:
                content = f.read()
            updated = re.sub(r'(version\s*=\s*["\'])[^"\']+(["\'])', rf'\g<1>{new_version}\g<2>', content, count=1)
            with open(PYPROJECT_TOML, "w", encoding="utf-8") as f:
                f.write(updated)
            print(f"[+] Updated {PYPROJECT_TOML} -> {new_version}")
        except Exception as e:
            print(f"[!] Warning: Could not update pyproject.toml: {e}")


def update_changelog(new_version, message=None, bump_type="patch"):
    """Update or initialize CHANGELOG.md following versioning-guide standard."""
    today = datetime.date.today().isoformat()
    header = f"## [{new_version}] - {today}\n"

    # Default category based on bump type
    category = "Added" if bump_type in ("minor", "major") else "Fixed"
    item_text = message if message else f"Release version {new_version}"
    entry = f"{header}\n### {category}\n- {item_text}\n\n"

    if not os.path.exists(CHANGELOG_FILE):
        content = f"# Changelog\n\nAll notable changes to this project will be documented in this file.\n\nThe format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and adheres to [Semantic Versioning](https://semver.org/).\n\n{entry}"
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Created {CHANGELOG_FILE} with initial release [{new_version}]")
    else:
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            existing = f.read()

        # Find first release section "## ["
        first_release_match = re.search(r"^## \[", existing, re.MULTILINE)
        if first_release_match:
            idx = first_release_match.start()
            new_content = existing[:idx] + entry + existing[idx:]
        else:
            new_content = existing.rstrip() + "\n\n" + entry

        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[+] Updated {CHANGELOG_FILE} with entry for [{new_version}]")


def create_git_tag(new_version):
    """Create annotated git tag vX.Y.Z."""
    tag_name = f"v{new_version}"
    res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
    if res.returncode != 0:
        print("[!] Not inside a git repository, skipping tag creation.")
        return

    res_tag = subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], capture_output=True, text=True)
    if res_tag.returncode == 0:
        print(f"[+] Successfully created Git tag: {tag_name}")
    else:
        print(f"[!] Note: Git tag output: {res_tag.stderr.strip() or res_tag.stdout.strip()}")


def main():
    parser = argparse.ArgumentParser(description="Bump project version conforming to SemVer and update CHANGELOG.md")
    parser.add_argument("type", nargs="?", choices=["patch", "minor", "major"], default="patch", help="SemVer bump type (default: patch)")
    parser.add_argument("-m", "--message", help="Summary message for CHANGELOG.md and commit")
    parser.add_argument("--no-changelog", action="store_true", help="Skip updating CHANGELOG.md")
    parser.add_argument("--no-tag", action="store_true", help="Skip creating git tag immediately (e.g. tag after commit)")
    parser.add_argument("--tag-only", action="store_true", help="Only create tag for current version in VERSION file")

    args = parser.parse_args()

    if args.tag_only:
        ver = get_current_version()
        create_git_tag(ver)
        return

    current = get_current_version()
    new_ver = bump_version(current, args.type)
    print(f"[*] Bumping SemVer: {current} -> {new_ver} ({args.type})")

    update_version_files(new_ver)

    if not args.no_changelog:
        update_changelog(new_ver, message=args.message, bump_type=args.type)

    if not args.no_tag:
        create_git_tag(new_ver)


if __name__ == "__main__":
    main()
