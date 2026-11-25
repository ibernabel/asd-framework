#!/usr/bin/env python3
"""
Unit tests for answer-in-the-same-language propagation and template invariants.
"""

import os
import shutil
import sys
import tempfile
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TEST_DIR)
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
TEMPLATES_DIR = os.path.join(REPO_ROOT, "templates")
HARNESS_TEMPLATES_DIR = os.path.join(TEMPLATES_DIR, "harnesses")
sys.path.insert(0, SCRIPTS_DIR)

import sync_agents_ecosystem as sae


def _read(path, mode="r"):
    kwargs = {"encoding": "utf-8"} if "b" not in mode else {}
    with open(path, mode, **kwargs) as f:
        return f.read()


class TestLanguageRulesSync(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="asd_test_lang_")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_templates_enforce_same_language_and_have_no_chat_english_mandate(self):
        """All domain and harness templates must include answer-in-the-same-language."""
        domain_templates = [
            "software-dev-agents.md",
            "ai-agents-agents.md",
            "business-admin-agents.md",
            "content-brand-agents.md",
            "video-production-agents.md",
        ]
        for fname in domain_templates:
            content = _read(os.path.join(TEMPLATES_DIR, fname))
            self.assertIn("answer-in-the-same-language", content, f"Missing rule in {fname}")
            self.assertNotIn("explanations in chat must be in", content.lower(), f"Legacy rule in {fname}")

        harness_files = [
            "AGENTS.md",
            "CLAUDE.md",
            ".cursorrules",
            "cursor-rule.mdc",
            ".windsurfrules",
            "copilot-instructions.md",
        ]
        for fname in harness_files:
            content = _read(os.path.join(HARNESS_TEMPLATES_DIR, fname))
            self.assertIn("answer-in-the-same-language", content, f"Missing rule in harness {fname}")
            self.assertNotIn("technical explanations must be in", content.lower(), f"Legacy rule in harness {fname}")
            self.assertNotIn("technical explanations in english", content.lower(), f"Legacy rule in harness {fname}")

    def test_agents_md_injection_is_idempotent(self):
        """update_project_agents_md injects the linguistic section once and stays idempotent."""
        agents_dir = os.path.join(self.test_dir, ".agents")
        os.makedirs(agents_dir, exist_ok=True)
        agents_md = os.path.join(agents_dir, "AGENTS.md")
        with open(agents_md, "w", encoding="utf-8") as f:
            f.write(
                "# Software Project\n\n"
                "## 👤 Developer & Global Ecosystem Context\n\n"
                "- **Developer Profile:** `~/.agents/USER.md`\n\n"
                "## Roles\n"
            )

        changed_first = sae.update_project_agents_md(self.test_dir, dry_run=False)
        self.assertTrue(changed_first)
        content_first = _read(agents_md)
        self.assertIn(sae.LINGUISTIC_SECTION_TITLE, content_first)
        self.assertEqual(content_first.count("answer-in-the-same-language"), 2)

        changed_second = sae.update_project_agents_md(self.test_dir, dry_run=False)
        self.assertFalse(changed_second)
        content_second = _read(agents_md)
        self.assertEqual(content_first, content_second)

    def test_preserves_custom_caketoppers_and_corebank_rules(self):
        """Custom project language sections must be preserved intact."""
        agents_dir = os.path.join(self.test_dir, ".agents")
        os.makedirs(agents_dir, exist_ok=True)
        local_agents_md = os.path.join(agents_dir, "AGENTS.md")
        with open(local_agents_md, "w", encoding="utf-8") as f:
            f.write(
                "# Reglas Cake Toppers\n\n"
                "## 3. Idioma de Interacción y Documentación\n\n"
                "- **Interacción:** Español.\n"
                "- **Código Fuente:** Inglés.\n\n"
                "---\n\n"
                "## 4. Mensajes de Commit\n"
            )

        root_agents_md = os.path.join(self.test_dir, "AGENTS.md")
        with open(root_agents_md, "w", encoding="utf-8") as f:
            f.write(
                "# Corebank\n\n"
                "## Idioma oficial\n\n"
                "- **Español:** chat y markdown.\n"
                "- **Inglés:** código fuente.\n\n"
                "## Contexto de trabajo\n"
            )

        sae.update_project_agents_md(self.test_dir, dry_run=False)
        sae.sync_project_harnesses_language(self.test_dir, dry_run=False)

        local_out = _read(local_agents_md)
        self.assertIn("## 3. Idioma de Interacción y Documentación", local_out)
        self.assertIn("answer-in-the-same-language", local_out)
        self.assertIn("## 4. Mensajes de Commit", local_out)

        root_out = _read(root_agents_md)
        self.assertIn("## Idioma oficial", root_out)
        self.assertIn("answer-in-the-same-language", root_out)
        self.assertIn("## Contexto de trabajo", root_out)

    def test_harnesses_surgical_patch_and_eol_preservation(self):
        """Existing legacy harness files are updated in place without losing CRLF or surrounding content."""
        os.makedirs(os.path.join(self.test_dir, ".cursor", "rules"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, ".github"), exist_ok=True)

        claude_path = os.path.join(self.test_dir, "CLAUDE.md")
        with open(claude_path, "w", encoding="utf-8", newline="") as f:
            f.write(
                "# CLAUDE.md\r\n"
                "- Act as a proactive collaborator.\r\n"
                "- Code, comments, commits, and technical explanations must be in **English**.\r\n"
            )

        windsurf_path = os.path.join(self.test_dir, ".windsurfrules")
        with open(windsurf_path, "w", encoding="utf-8") as f:
            f.write("# Windsurf\n- Code, commits, and technical explanations must be in English.\n")

        mdc_path = os.path.join(self.test_dir, ".cursor", "rules", "asd-framework.mdc")
        with open(mdc_path, "w", encoding="utf-8") as f:
            f.write("- **Engineering Principles:** Strictly uphold SOLID, KISS, YAGNI, and DRY.\n")

        count = sae.sync_project_harnesses_language(self.test_dir, dry_run=False)
        self.assertEqual(count, 3)

        claude_raw = _read(claude_path, mode="rb")
        self.assertIn(b"\r\n", claude_raw)
        self.assertIn(b"answer-in-the-same-language", claude_raw)
        self.assertNotIn(b"technical explanations must be in **English**", claude_raw)

        # Second pass must be idempotent
        count_second = sae.sync_project_harnesses_language(self.test_dir, dry_run=False)
        self.assertEqual(count_second, 0)


if __name__ == "__main__":
    unittest.main()
