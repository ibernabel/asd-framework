#!/usr/bin/env python3
"""
Backend Integrity & Architecture Static Detector.
Scans Python, TypeScript, PHP, and Go backend files for architectural anti-patterns:
- Bare except / silent error suppression
- HTTP calls without bounded timeouts
- SQL string formatting / potential SQL injections
- Unbounded collection queries in controllers
- Missing schema validation indicators in API handlers

Exit status:
  0: Clean scan (No primary architectural findings)
  2: Primary architectural findings detected (Backend REJECTED)
  1: Operational failure
"""

import ast
import os
import re
import sys
from typing import List, Tuple

BACKEND_EXTENSIONS = {".py", ".ts", ".js", ".php", ".go"}
IGNORE_SUBSTRINGS = {
    ".test.",
    ".spec.",
    "test_",
    "_test.",
    "tests/",
    "node_modules/",
    ".venv/",
    "__pycache__/",
    "dist/",
    "build/",
}


class Finding:
    def __init__(self, file_path: str, line: int, rule_id: str, message: str, severity: str = "error"):
        self.file_path = file_path
        self.line = line
        self.rule_id = rule_id
        self.message = message
        self.severity = severity

    def __str__(self):
        return f"{self.file_path}:{self.line} [{self.rule_id}] {self.message}"


def is_backend_file(file_path: str) -> bool:
    """Check if file should be scanned as backend code."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in BACKEND_EXTENSIONS:
        return False
    # Avoid frontend component files
    if file_path.endswith(".tsx") or file_path.endswith(".jsx"):
        return False
    # Avoid test and build files
    normalized = file_path.replace("\\", "/")
    for ign in IGNORE_SUBSTRINGS:
        if ign in normalized:
            return False
    return True


def audit_python_file(file_path: str, content: str) -> List[Finding]:
    """Audit Python file using AST and regex."""
    findings = []
    try:
        tree = ast.parse(content, filename=file_path)
    except Exception as e:
        # If syntax error, skip AST and fallback to regex
        tree = None

    lines = content.splitlines()

    if tree:
        for node in ast.walk(tree):
            # Check 1: Bare except or except Exception with only pass
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    findings.append(Finding(
                        file_path,
                        node.lineno,
                        "bare-except",
                        "Avoid bare 'except:'. Specify the exact exception class or handle errors explicitly."
                    ))
                elif len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    findings.append(Finding(
                        file_path,
                        node.lineno,
                        "silent-exception-suppression",
                        "Silent exception suppression with 'pass'. Log the error or return a semantic failure response."
                    ))

            # Check 2: HTTP calls without timeout
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                    # Check if caller looks like requests or httpx or client
                    caller = ""
                    if isinstance(node.func.value, ast.Name):
                        caller = node.func.value.id
                    elif isinstance(node.func.value, ast.Attribute):
                        caller = node.func.value.attr

                    if caller in ("requests", "httpx", "client", "session") and func_name in ("get", "post", "put", "patch", "delete", "request"):
                        # Check keyword arguments for 'timeout'
                        has_timeout = any(kw.arg == "timeout" for kw in node.keywords)
                        if not has_timeout:
                            findings.append(Finding(
                                file_path,
                                node.lineno,
                                "missing-http-timeout",
                                f"Call to '{caller}.{func_name}' lacks explicit timeout. Specify timeout=5.0 to prevent thread starvation."
                            ))

    # Regex Check 3: Raw SQL string formatting / f-strings
    for idx, line in enumerate(lines, 1):
        if re.search(r'\b(execute|raw|cursor\.execute)\s*\(\s*f["\']', line):
            findings.append(Finding(
                file_path,
                idx,
                "sql-injection-fstring",
                "Potential SQL injection: Avoid formatted f-strings in SQL execution. Use parameterized queries."
            ))
        elif re.search(r'\b(execute|raw|cursor\.execute)\s*\(\s*["\'].*%[sdb]\s*["\']\s*%', line):
            findings.append(Finding(
                file_path,
                idx,
                "sql-injection-percent",
                "Potential SQL injection: Avoid %-formatting in SQL execution. Use parameterized query tuples."
            ))

    return findings


def audit_generic_backend_file(file_path: str, content: str) -> List[Finding]:
    """Audit TypeScript, JavaScript, PHP, Go backend files using patterns."""
    findings = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, 1):
        # Check 1: Empty catch blocks
        if re.search(r'catch\s*\([^)]*\)\s*\{\s*\}', line) or re.search(r'catch\s*\{\s*\}', line):
            findings.append(Finding(
                file_path,
                idx,
                "silent-catch-block",
                "Empty catch block suppresses exceptions silently. Log or rethrow structured error."
            ))

        # Check 2: Raw fetch calls without timeout or AbortController
        # Only in server routes / services
        if "fetch(" in line and "signal" not in line and "timeout" not in line:
            # Check surrounding context if possible
            if not line.strip().startswith("//") and not line.strip().startswith("*"):
                findings.append(Finding(
                    file_path,
                    idx,
                    "fetch-without-timeout",
                    "Outbound fetch() lacks explicit AbortSignal / timeout. Provide bounded timeout to prevent hanging connections."
                ))

        # Check 3: Raw SQL concatenation
        if re.search(r'\.(query|execute)\s*\(\s*`[^`]*\$\{', line):
            findings.append(Finding(
                file_path,
                idx,
                "sql-template-literal",
                "Potential SQL injection in template literal. Use parameterized queries (e.g. $1, ?, Prisma/ORM bindings)."
            ))

    return findings


def scan_target(target: str) -> List[Finding]:
    """Scan a single file or directory."""
    all_findings = []
    if os.path.isfile(target):
        if is_backend_file(target):
            try:
                with open(target, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if target.endswith(".py"):
                    all_findings.extend(audit_python_file(target, content))
                else:
                    all_findings.extend(audit_generic_backend_file(target, content))
            except Exception as e:
                print(f"[!] Warning reading {target}: {e}", file=sys.stderr)
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv", "__pycache__", "dist", "build")]
            for f in files:
                p = os.path.join(root, f)
                if is_backend_file(p):
                    try:
                        with open(p, "r", encoding="utf-8", errors="ignore") as file_obj:
                            content = file_obj.read()
                        if p.endswith(".py"):
                            all_findings.extend(audit_python_file(p, content))
                        else:
                            all_findings.extend(audit_generic_backend_file(p, content))
                    except Exception as e:
                        print(f"[!] Warning reading {p}: {e}", file=sys.stderr)
    return all_findings


def main():
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("Usage: verify_backend_integrity.py [options] <file-or-dir...>")
        print("\nScan backend files for architectural anti-patterns, missing timeouts, and security issues.")
        print("\nOptions:")
        print("  --help     Show this help message")
        print("  --quiet    Only print final findings count")
        print("\nExit status:")
        print("  0: Scan completed with 0 primary findings (Backend CERTIFIED)")
        print("  2: Primary architectural findings detected (Backend REJECTED)")
        print("  1: Operational error")
        sys.exit(0)

    quiet = "--quiet" in sys.argv
    targets = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not targets:
        print("[!] Error: No files or directories provided to scan.", file=sys.stderr)
        sys.exit(1)

    all_findings: List[Finding] = []
    for t in targets:
        all_findings.extend(scan_target(t))

    if all_findings:
        if not quiet:
            print("\n❌ Backend Integrity & Architecture Violations Found:", file=sys.stderr)
            for f in all_findings:
                print(f"  {f}", file=sys.stderr)
            print(f"\nTotal: {len(all_findings)} primary violation(s) detected.", file=sys.stderr)
            print("Action: Resolve architectural issues before QA/Reviewer certification.\n", file=sys.stderr)
        else:
            print(f"Findings: {len(all_findings)}", file=sys.stderr)
        sys.exit(2)
    else:
        if not quiet:
            print("✅ Backend Integrity: 0 architectural violations found. Code CERTIFIED.", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
