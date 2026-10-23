#!/usr/bin/env python3
import os
import subprocess

projects = [
    "/home/ibernabel/develop/consultor/technology/projects/solufime/solipres",
    "/home/ibernabel/develop/consultor/technology/projects/solufime/solufime-website",
    "/home/ibernabel/develop/consultor/technology/projects/aisa/find-job",
    "/home/ibernabel/develop/consultor/technology/projects/aisa/frm-system",
    "/home/ibernabel/develop/consultor/technology/projects/aisa/firma-digital",
    "/home/ibernabel/develop/consultor/technology/projects/aisa/customer-service-system",
    "/home/ibernabel/develop/consultor/technology/projects/aisa/learner",
    "/home/ibernabel/develop/consultor/technology/projects/idequelbernabel/portfolio",
    "/home/ibernabel/develop/consultor/admin/businesses/lender",
]

for p in projects:
    name = os.path.basename(p)
    print("=" * 70)
    print(f"[PROJECT] {name} ({p})")
    if not os.path.isdir(os.path.join(p, ".git")):
        print("  Not a git repo directly.")
        continue

    # Branch and upstream status
    res_sb = subprocess.run(["git", "status", "-sb"], cwd=p, capture_output=True, text=True)
    first_line = res_sb.stdout.strip().splitlines()[0] if res_sb.stdout.strip() else "unknown"
    print(f"  {first_line}")

    # Diff stat
    diff_stat = subprocess.run(["git", "diff", "--stat"], cwd=p, capture_output=True, text=True).stdout.strip()
    if diff_stat:
        print("  Tracked changes:")
        for line in diff_stat.splitlines():
            print(f"    {line}")
    else:
        print("  No tracked changes.")

    # Untracked files
    untracked = subprocess.run(["git", "status", "--porcelain"], cwd=p, capture_output=True, text=True).stdout.strip()
    untracked_lines = [l for l in untracked.splitlines() if l.startswith("??")]
    if untracked_lines:
        print(f"  Untracked ({len(untracked_lines)} entries):")
        for l in untracked_lines[:10]:
            print(f"    {l}")
        if len(untracked_lines) > 10:
            print(f"    ... (+{len(untracked_lines) - 10} more)")
