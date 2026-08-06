#!/usr/bin/env python3
"""
Bump version script for software projects.
Supports: patch, minor, major.
Updates VERSION file and optionally package.json, then creates a Git tag vX.Y.Z.
"""

import sys
import os
import re
import json
import subprocess

VERSION_FILE = "VERSION"
PACKAGE_JSON = "package.json"

def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    elif os.path.exists(PACKAGE_JSON):
        with open(PACKAGE_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("version", "0.1.0")
    return "0.1.0"

def parse_version(ver_str):
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", ver_str.strip())
    if not match:
        raise ValueError(f"Invalid SemVer format: {ver_str}")
    return [int(x) for x in match.groups()]

def bump_version(ver_str, bump_type):
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
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(f"{new_version}\n")
    print(f"Updated {VERSION_FILE} -> {new_version}")

    if os.path.exists(PACKAGE_JSON):
        try:
            with open(PACKAGE_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["version"] = new_version
            with open(PACKAGE_JSON, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                f.write("\n")
            print(f"Updated {PACKAGE_JSON} -> {new_version}")
        except Exception as e:
            print(f"Warning: Could not update package.json: {e}")

def create_git_tag(new_version):
    tag_name = f"v{new_version}"
    # Check if in git repository
    res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
    if res.returncode != 0:
        print("Not inside a git repository, skipping tag creation.")
        return

    # Create tag
    res_tag = subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], capture_output=True, text=True)
    if res_tag.returncode == 0:
        print(f"Successfully created Git tag: {tag_name}")
    else:
        print(f"Note: Git tag creation output: {res_tag.stderr.strip() or res_tag.stdout.strip()}")

def main():
    bump_type = sys.argv[1] if len(sys.argv) > 1 else "patch"
    current = get_current_version()
    new_ver = bump_version(current, bump_type)
    print(f"Bumping version: {current} -> {new_ver} ({bump_type})")
    update_version_files(new_ver)
    create_git_tag(new_ver)

if __name__ == "__main__":
    main()
