#!/usr/bin/env python3
import os
import subprocess

repos = []
for root, dirs, files in os.walk("/home/ibernabel/develop"):
    dirs[:] = [d for d in dirs if d not in (".venv", "node_modules", ".cache", ".codegraph", "vendor")]
    if ".git" in dirs:
        repos.append(root)

print(f"Found {len(repos)} git repositories under /home/ibernabel/develop:\n")
for r in sorted(repos):
    res_b = subprocess.run(["git", "branch", "--show-current"], cwd=r, capture_output=True, text=True).stdout.strip()
    res_sb = subprocess.run(["git", "status", "-s"], cwd=r, capture_output=True, text=True).stdout.strip()
    res_rem = subprocess.run(["git", "remote", "get-url", "origin"], cwd=r, capture_output=True, text=True).stdout.strip()
    dirty = "DIRTY" if res_sb else "CLEAN"
    has_agents = os.path.isdir(os.path.join(r, ".agents"))
    rel = r.replace("/home/ibernabel/develop/", "")
    print(f"[{dirty:5}] .agents: {str(has_agents):5} | {rel:60} | branch: {res_b:12} | {res_rem}")
