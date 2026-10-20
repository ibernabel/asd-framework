#!/usr/bin/env python3
"""
Unit and integration tests for Universal AI Harness Adapter.
"""

import os
import shutil
import tempfile
import unittest
import sys

# Add scripts directory to path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TEST_DIR)
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from harness_adapter import (
    get_templates_dir,
    install_harness_adapters,
    validate_harness_compatibility,
)


class TestHarnessAdapter(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="asd_test_harness_")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_get_templates_dir(self):
        tmpl_dir = get_templates_dir()
        self.assertIsNotNone(tmpl_dir)
        self.assertTrue(os.path.isdir(tmpl_dir))
        self.assertTrue(os.path.isfile(os.path.join(tmpl_dir, "CLAUDE.md")))
        self.assertTrue(os.path.isfile(os.path.join(tmpl_dir, "AGENTS.md")))
        self.assertTrue(os.path.isfile(os.path.join(tmpl_dir, ".cursorrules")))
        self.assertTrue(os.path.isfile(os.path.join(tmpl_dir, "cursor-rule.mdc")))
        self.assertTrue(os.path.isfile(os.path.join(tmpl_dir, ".windsurfrules")))
        self.assertTrue(os.path.isfile(os.path.join(tmpl_dir, "copilot-instructions.md")))

    def test_dry_run_creates_no_files(self):
        results = install_harness_adapters(self.test_dir, dry_run=True)
        self.assertTrue(len(results) > 0)
        # Ensure no files were actually written
        self.assertEqual(os.listdir(self.test_dir), [])

    def test_install_and_validate_compatibility(self):
        # Initial validation should fail on empty directory
        passed, report = validate_harness_compatibility(self.test_dir)
        self.assertFalse(passed)

        # Mock Antigravity config in .agents/
        os.makedirs(os.path.join(self.test_dir, ".agents"), exist_ok=True)
        with open(os.path.join(self.test_dir, ".agents", "AGENTS.md"), "w", encoding="utf-8") as f:
            f.write("# Mock Agent Rules\n")

        # Install harness bridges
        results = install_harness_adapters(self.test_dir, dry_run=False)
        self.assertTrue(len(results) >= 6)

        # Check all required files are present
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "AGENTS.md")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "CLAUDE.md")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, ".cursorrules")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, ".cursor", "rules", "asd-framework.mdc")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, ".windsurfrules")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, ".github", "copilot-instructions.md")))

        # Check Claude Code custom commands
        claude_cmds_dir = os.path.join(self.test_dir, ".claude", "commands")
        self.assertTrue(os.path.isdir(claude_cmds_dir))
        self.assertTrue(os.path.isfile(os.path.join(claude_cmds_dir, "code-pipeline.md")))
        self.assertTrue(os.path.isfile(os.path.join(claude_cmds_dir, "repo-sync.md")))

        # Now validation should pass completely
        passed, report = validate_harness_compatibility(self.test_dir)
        self.assertTrue(passed)
        for harness, data in report.items():
            self.assertTrue(data["passed"], f"Harness {harness} failed validation")

    def test_non_destructive_preservation(self):
        claude_md = os.path.join(self.test_dir, "CLAUDE.md")
        with open(claude_md, "w", encoding="utf-8") as f:
            f.write("# Custom Existing Claude Rules\n")

        # Run installation without force
        results = install_harness_adapters(self.test_dir, dry_run=False, force=False)
        self.assertEqual(results["CLAUDE.md"]["status"], "already exists")

        # Ensure content was preserved
        with open(claude_md, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "# Custom Existing Claude Rules\n")

        # Run installation with force
        results = install_harness_adapters(self.test_dir, dry_run=False, force=True)
        self.assertEqual(results["CLAUDE.md"]["status"], "installed")

        # Content should now match template
        with open(claude_md, "r", encoding="utf-8") as f:
            new_content = f.read()
        self.assertIn("ASD Framework", new_content)

    def test_integration_with_install_project_skills(self):
        # Create a mock .agents structure with AGENTS.md
        os.makedirs(os.path.join(self.test_dir, ".agents"), exist_ok=True)
        with open(os.path.join(self.test_dir, ".agents", "AGENTS.md"), "w", encoding="utf-8") as f:
            f.write("# Software Development Project\n")

        import install_project_skills
        # Run install_project_skills with sync_harnesses=True
        installed = install_project_skills.install_project_skills(
            project_dir=self.test_dir,
            domain="software",
            dry_run=False,
            sync_md=False,
            sync_harnesses=True
        )

        # Validate that harness bridges were automatically created
        passed, report = validate_harness_compatibility(self.test_dir)
        self.assertTrue(passed, "Validation should pass after install_project_skills execution")
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "CLAUDE.md")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "AGENTS.md")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, ".cursorrules")))


if __name__ == "__main__":
    unittest.main()
