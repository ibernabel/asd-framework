import os, subprocess

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
    "/home/ibernabel/develop/consultor/technology/projects/aisa/creditgraph-legacy-backup",
    "/home/ibernabel/develop/consultor/technology/projects/aisa/lamas-py-legacy-backup",
]

for p in projects:
    print(f"\n{"="*60}\nPROJECT: {p}")
    if os.path.isdir(os.path.join(p, ".git")):
        res_b = subprocess.run(["git", "branch", "--show-current"], cwd=p, capture_output=True, text=True)
        branch = res_b.stdout.strip()
        res_r = subprocess.run(["git", "remote", "get-url", "origin"], cwd=p, capture_output=True, text=True)
        remote = res_r.stdout.strip()
        print(f"Git: Yes | Branch: {branch} | Remote: {remote}")
        res_s = subprocess.run(["git", "status", "-s"], cwd=p, capture_output=True, text=True)
        status = res_s.stdout.strip()
        if status:
            print("Status: DIRTY")
            for line in status.splitlines()[:15]:
                print(f"  {line}")
            if len(status.splitlines()) > 15:
                print(f"  ... (+{len(status.splitlines()) - 15} more files)")
        else:
            print("Status: CLEAN")
    else:
        print("Git: No (.git folder not present directly in project root)")
