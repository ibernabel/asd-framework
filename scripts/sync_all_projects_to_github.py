#!/usr/bin/env python3
"""
Sync all active ASD projects to their respective GitHub repositories.
Propagates framework changes, bumps SemVer patch version when applicable,
creates release tags, and pushes to GitHub.
"""

import os
import shutil
import subprocess
import sys

GLOBAL_BUMP_SCRIPT = os.path.expanduser("~/.agents/scripts/bump_version.py")

TARGET_PROJECTS = [
    {
        "name": "solufime-website",
        "path": "/home/ibernabel/develop/consultor/technology/projects/solufime/solufime-website",
        "has_version": True,
    },
    {
        "name": "find-job",
        "path": "/home/ibernabel/develop/consultor/technology/projects/aisa/find-job",
        "has_version": True,
    },
    {
        "name": "frm-system",
        "path": "/home/ibernabel/develop/consultor/technology/projects/aisa/frm-system",
        "has_version": False,
    },
    {
        "name": "firma-digital",
        "path": "/home/ibernabel/develop/consultor/technology/projects/aisa/firma-digital",
        "has_version": True,
    },
    {
        "name": "customer-service-system",
        "path": "/home/ibernabel/develop/consultor/technology/projects/aisa/customer-service-system",
        "has_version": True,
    },
    {
        "name": "learner",
        "path": "/home/ibernabel/develop/consultor/technology/projects/aisa/learner",
        "has_version": True,
    },
    {
        "name": "portfolio",
        "path": "/home/ibernabel/develop/consultor/technology/projects/idequelbernabel/portfolio",
        "has_version": True,
    },
    {
        "name": "lender",
        "path": "/home/ibernabel/develop/consultor/admin/businesses/lender",
        "has_version": False,
    },
]


def run_cmd(cmd, cwd, check=True):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"  [ERROR] Command failed in {cwd}: {' '.join(cmd)}")
        print(f"  STDOUT: {res.stdout.strip()}")
        print(f"  STDERR: {res.stderr.strip()}")
        raise RuntimeError(f"Command failed with exit code {res.returncode}")
    return res


def sync_project(proj):
    name = proj["name"]
    path = proj["path"]
    has_version = proj["has_version"]

    print(f"\n{'='*70}\n[*] SYNCING PROJECT: {name}\n    Path: {path}")

    if not os.path.isdir(os.path.join(path, ".git")):
        print(f"  [!] Not a git repository: {path}")
        return

    # 1. Check branch
    branch = run_cmd(["git", "branch", "--show-current"], cwd=path).stdout.strip()
    if not branch:
        branch = "main"
    print(f"  Branch: {branch}")

    # 2. Fetch origin
    print(f"  Fetching origin...")
    run_cmd(["git", "fetch", "origin"], cwd=path, check=False)

    # 3. Check status
    status = run_cmd(["git", "status", "--porcelain"], cwd=path).stdout.strip()
    if not status:
        print(f"  [✓] Working tree is already clean.")
        # Check if ahead
        ahead = run_cmd(["git", "rev-list", "--count", f"origin/{branch}..HEAD"], cwd=path, check=False).stdout.strip()
        if ahead and ahead != "0":
            print(f"  Ahead by {ahead} commits. Pushing...")
            run_cmd(["git", "push", "origin", branch], cwd=path)
            run_cmd(["git", "push", "origin", "--tags"], cwd=path, check=False)
            print(f"  [✓] Pushed ahead commits to origin/{branch}.")
        return

    print(f"  Changes detected. Preparing release commit...")

    if has_version and os.path.exists(os.path.join(path, "VERSION")):
        scripts_dir = os.path.join(path, "scripts")
        bump_script = os.path.join(scripts_dir, "bump_version.py")
        if not os.path.exists(bump_script):
            os.makedirs(scripts_dir, exist_ok=True)
            shutil.copy2(GLOBAL_BUMP_SCRIPT, bump_script)
            os.chmod(bump_script, 0o755)
            print(f"  Installed bump_version.py in {scripts_dir}")

        # Run bump_version patch
        msg = "sync ASD framework agents, UI/UX craft, and backend integrity tooling"
        print(f"  Bumping patch version...")
        run_cmd([sys.executable, bump_script, "patch", "-m", msg, "--no-tag"], cwd=path)

        with open(os.path.join(path, "VERSION"), "r", encoding="utf-8") as vf:
            new_version = vf.read().strip()
        print(f"  New version: {new_version}")

        # Stage and commit
        run_cmd(["git", "add", "."], cwd=path)
        commit_msg = f"chore(release): bump version to {new_version} and sync ASD v2 tooling"
        run_cmd(["git", "commit", "-m", commit_msg], cwd=path)
        print(f"  Committed: {commit_msg}")

        # Tag
        run_cmd([sys.executable, bump_script, "--tag-only"], cwd=path)
        print(f"  Created tag v{new_version}")

        # Push branch and tags
        print(f"  Pushing to origin {branch} with tags...")
        run_cmd(["git", "push", "origin", branch], cwd=path)
        run_cmd(["git", "push", "origin", "--tags"], cwd=path)
        print(f"  [✓] Successfully synced and pushed {name} (v{new_version}).")

    else:
        # Non-versioned project (or no VERSION file)
        commit_msg = "chore(framework): sync ASD framework agents, UI/UX craft, and backend integrity tooling"
        run_cmd(["git", "add", "."], cwd=path)
        run_cmd(["git", "commit", "-m", commit_msg], cwd=path)
        print(f"  Committed: {commit_msg}")

        print(f"  Pushing to origin {branch}...")
        run_cmd(["git", "push", "origin", branch], cwd=path)
        print(f"  [✓] Successfully synced and pushed {name}.")


def main():
    print(f"Starting ecosystem GitHub synchronization for {len(TARGET_PROJECTS)} projects...\n")
    successes = []
    failures = []

    for p in TARGET_PROJECTS:
        try:
            sync_project(p)
            successes.append(p["name"])
        except Exception as e:
            print(f"  [FAILED] {p['name']}: {e}")
            failures.append((p["name"], str(e)))

    print("\n" + "="*70)
    print(f"ECOSYSTEM SYNC SUMMARY: {len(successes)} succeeded, {len(failures)} failed.")
    for s in successes:
        print(f"  ✅ {s}")
    for f_name, f_err in failures:
        print(f"  ❌ {f_name}: {f_err}")


if __name__ == "__main__":
    main()
