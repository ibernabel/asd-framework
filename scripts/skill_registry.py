#!/usr/bin/env python3
"""
Skill Registry CLI & Library for ASD Framework v2.
Interacts with online registries (SkillsMP, Antigravity-Skills, Hasna/Skills.md, GitHub)
to search, inspect, and install skills globally into ~/.agents/skills/.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import urllib.error

GLOBAL_AGENTS_DIR = os.path.expanduser("~/.agents")
GLOBAL_SKILLS_DIR = os.path.join(GLOBAL_AGENTS_DIR, "skills")
ENV_PATH = os.path.join(GLOBAL_AGENTS_DIR, ".env")
LOCK_FILE = os.path.join(GLOBAL_AGENTS_DIR, ".skill-lock.json")


def get_skillsmp_key():
    """Retrieve SKILLSMP_API_KEY from environment or .agents/.env."""
    key = os.environ.get("SKILLSMP_API_KEY", "")
    if not key and os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("SKILLSMP_API_KEY="):
                    key = line.strip().split("=", 1)[1].strip('"\'\r\n ')
                    break
    return key


def search_skillsmp(query, limit=10):
    """Search skills on Skills Marketplace via REST API."""
    key = get_skillsmp_key()
    url = f"https://skillsmp.com/api/v1/skills/search?q={urllib.parse.quote(query)}&limit={limit}&sortBy=stars"
    headers = {"User-Agent": "ASD-Skill-Registry/2.0"}
    if key:
        headers["Authorization"] = f"Bearer {key}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            skills = data.get("data", {}).get("skills", [])
            return [
                {
                    "source": "SkillsMP",
                    "name": s.get("name"),
                    "author": s.get("author"),
                    "description": s.get("description"),
                    "githubUrl": s.get("githubUrl"),
                    "stars": s.get("stars", 0),
                    "skillUrl": s.get("skillUrl"),
                }
                for s in skills
            ]
    except Exception as e:
        print(f"[SkillsMP Search Warning]: {e}", file=sys.stderr)
        return []


def search_antigravity(query):
    """Search skills in rmyndharis/antigravity-skills repository catalog."""
    url = "https://raw.githubusercontent.com/rmyndharis/antigravity-skills/main/CATALOG.md"
    req = urllib.request.Request(url, headers={"User-Agent": "ASD-Skill-Registry/2.0"})
    results = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            # Parse table rows: | `skill-name` | description | tags | triggers |
            pattern = re.compile(r"\|\s*`([^`]+)`\s*\|\s*([^|]+)\|\s*([^|]*)\|\s*([^|]*)\|")
            q_lower = query.lower()
            for match in pattern.finditer(content):
                name, desc, tags, triggers = match.groups()
                full_text = f"{name} {desc} {tags} {triggers}".lower()
                if q_lower in full_text:
                    results.append(
                        {
                            "source": "Antigravity-Skills",
                            "name": name.strip(),
                            "author": "rmyndharis",
                            "description": desc.strip()[:140],
                            "githubUrl": f"https://github.com/rmyndharis/antigravity-skills/tree/main/skills/{name.strip()}",
                            "stars": "N/A",
                            "skillUrl": f"https://github.com/rmyndharis/antigravity-skills/blob/main/skills/{name.strip()}/SKILL.md",
                        }
                    )
    except Exception as e:
        print(f"[Antigravity Catalog Search Warning]: {e}", file=sys.stderr)
    return results


def search_hasna(query):
    """Search skills in hasna/skills repository."""
    url = "https://api.github.com/repos/hasna/skills/contents/skills"
    req = urllib.request.Request(url, headers={"User-Agent": "ASD-Skill-Registry/2.0"})
    results = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            items = json.loads(resp.read().decode("utf-8"))
            q_lower = query.lower()
            for item in items:
                name = item.get("name", "")
                if q_lower in name.lower():
                    results.append(
                        {
                            "source": "Skills.md (hasna/skills)",
                            "name": name,
                            "author": "hasna",
                            "description": f"Modular agent skill '{name}' from skills.md directory",
                            "githubUrl": f"https://github.com/hasna/skills/tree/main/skills/{name}",
                            "stars": "N/A",
                            "skillUrl": f"https://github.com/hasna/skills/blob/main/skills/{name}/SKILL.md",
                        }
                    )
    except Exception as e:
        print(f"[Hasna Skills Search Warning]: {e}", file=sys.stderr)
    return results


def search_all(query, source="all"):
    """Search across specified sources."""
    results = []
    if source in ("all", "skillsmp"):
        results.extend(search_skillsmp(query))
    if source in ("all", "antigravity"):
        results.extend(search_antigravity(query))
    if source in ("all", "hasna"):
        results.extend(search_hasna(query))
    return results


def list_local_skills(filter_q=None):
    """List installed skills in ~/.agents/skills."""
    if not os.path.exists(GLOBAL_SKILLS_DIR):
        return []
    skills = sorted(os.listdir(GLOBAL_SKILLS_DIR))
    if filter_q:
        skills = [s for s in skills if filter_q.lower() in s.lower()]
    return skills


def install_skill_from_git(repo_url, skill_path=None, name=None):
    """Clone a git repo and install a skill folder into ~/.agents/skills/."""
    os.makedirs(GLOBAL_SKILLS_DIR, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix="asd_skill_install_")
    try:
        print(f"[*] Cloning {repo_url}...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], check=True, capture_output=True)

        # Determine source skill directory
        source_dir = temp_dir
        if skill_path:
            source_dir = os.path.join(temp_dir, skill_path)
        elif not os.path.exists(os.path.join(temp_dir, "SKILL.md")):
            # Look for skills/ subdirectory
            if os.path.exists(os.path.join(temp_dir, "skills")):
                subdirs = [d for d in os.listdir(os.path.join(temp_dir, "skills")) if os.path.isdir(os.path.join(temp_dir, "skills", d))]
                if subdirs:
                    source_dir = os.path.join(temp_dir, "skills", subdirs[0])
                    if not name:
                        name = subdirs[0]

        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Skill directory not found in repo at: {source_dir}")

        if not name:
            name = os.path.basename(os.path.normpath(source_dir))
            if name in ("", "skills", "src", "."):
                name = os.path.basename(repo_url.rstrip("/").removesuffix(".git"))

        target_dir = os.path.join(GLOBAL_SKILLS_DIR, name)
        os.makedirs(target_dir, exist_ok=True)
        for item in os.listdir(source_dir):
            src_item = os.path.join(source_dir, item)
            dst_item = os.path.join(target_dir, item)
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
            else:
                shutil.copy2(src_item, dst_item)

        print(f"[+] Successfully installed skill '{name}' to {target_dir}")

        # Update .skill-lock.json
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        lock_data = {"version": 3, "skills": {}}
        if os.path.exists(LOCK_FILE):
            try:
                with open(LOCK_FILE, "r", encoding="utf-8") as f:
                    lock_data = json.load(f)
            except Exception:
                pass

        lock_data.setdefault("skills", {})[name] = {
            "source": repo_url,
            "sourceType": "github",
            "sourceUrl": repo_url,
            "skillPath": skill_path or "SKILL.md",
            "skillFolderHash": f"installed-{name}",
            "installedAt": now,
            "updatedAt": now,
        }
        with open(LOCK_FILE, "w", encoding="utf-8") as f:
            json.dump(lock_data, f, indent=2)

        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="ASD Framework v2 Skill Registry Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search command
    search_parser = subparsers.add_parser("search", help="Search online skills registries")
    search_parser.add_argument("query", help="Keyword or skill name to search")
    search_parser.add_argument(
        "--source", choices=["all", "skillsmp", "antigravity", "hasna"], default="all", help="Registry to search"
    )
    search_parser.add_argument("--limit", type=int, default=10, help="Max results from API")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install a skill from a git repository")
    install_parser.add_argument("repo_url", help="Git repository URL")
    install_parser.add_argument("--skill-path", help="Relative path to skill folder inside repo (e.g. skills/versioning-guide)")
    install_parser.add_argument("--name", help="Target skill name in ~/.agents/skills/")

    # List local command
    list_parser = subparsers.add_parser("list-local", help="List installed global skills")
    list_parser.add_argument("--filter", dest="filter_q", help="Filter by name")

    args = parser.parse_args()

    if args.command == "search":
        results = search_all(args.query, source=args.source)
        if not results:
            print(f"No skills found matching '{args.query}' on source '{args.source}'.")
            return
        print(f"\nFound {len(results)} skills matching '{args.query}':\n")
        for i, r in enumerate(results, 1):
            print(f"[{i}] {r['name']} ({r['source']})")
            if r.get("description"):
                print(f"    Desc:   {r['description']}")
            if r.get("githubUrl"):
                print(f"    GitHub: {r['githubUrl']}")
            print()

    elif args.command == "install":
        install_skill_from_git(args.repo_url, skill_path=args.skill_path, name=args.name)

    elif args.command == "list-local":
        skills = list_local_skills(args.filter_q)
        print(f"\nInstalled Global Skills in ~/.agents/skills/ ({len(skills)} total):\n")
        for s in skills:
            print(f" - {s}")
        print()


if __name__ == "__main__":
    main()
