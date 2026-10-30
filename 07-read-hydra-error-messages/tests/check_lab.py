"""Offline author checks against an installed Hydra CLI; no network actions."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

import yaml

SCENARIO = Path(__file__).resolve().parents[1]
ASSETS = SCENARIO / "assets"


class LabChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hydra-lab07-")
        self.previous = os.environ.get("HYDRA_LAB07_ROOT")
        os.environ["HYDRA_LAB07_ROOT"] = self.temp.name
        spec = importlib.util.spec_from_file_location("lab07_under_test", ASSETS / "lab07.py")
        self.lab = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.lab)
        self.output = StringIO()
        self.stdout = redirect_stdout(self.output)
        self.stderr = redirect_stderr(self.output)
        self.stdout.__enter__()
        self.stderr.__enter__()

    def tearDown(self):
        self.stderr.__exit__(None, None, None)
        self.stdout.__exit__(None, None, None)
        if self.previous is None:
            os.environ.pop("HYDRA_LAB07_ROOT", None)
        else:
            os.environ["HYDRA_LAB07_ROOT"] = self.previous
        self.temp.cleanup()

    def correct(self):
        self.lab.write(self.lab.WORKFLOW, self.lab.read(ASSETS / "solution.yaml"))

    def test_all_exercise_diagnostics_and_corrections(self):
        for case in self.lab.CASES:
            with self.subTest(case=case):
                self.lab.prepare(case)
                with self.assertRaises(ValueError):
                    self.lab.check(case)
                self.lab.diagnose(case)
                # CLI dry-run cannot create job output or run-state files.
                files = sorted(p.relative_to(self.lab.PROJECT).as_posix()
                               for p in self.lab.PROJECT.rglob("*") if p.is_file())
                self.assertEqual(files, [".hydra/project.json", "workflows/errors.yaml"])
                if case != "no-version":
                    with self.assertRaises(ValueError):
                        self.lab.check(case)
                    self.correct()
                self.lab.check(case)

    def test_deleting_a_step_does_not_pass(self):
        self.lab.prepare("unknown-action")
        self.lab.diagnose("unknown-action")
        self.correct()
        data = yaml.safe_load(self.lab.read(self.lab.WORKFLOW))
        data["workflow"]["steps"].pop()
        self.lab.write(self.lab.WORKFLOW, yaml.safe_dump(data))
        with self.assertRaises(ValueError):
            self.lab.check("unknown-action")

    def test_empty_steps_do_not_pass(self):
        self.lab.prepare("unknown-key")
        self.lab.diagnose("unknown-key")
        self.correct()
        data = yaml.safe_load(self.lab.read(self.lab.WORKFLOW))
        data["workflow"]["steps"] = []
        self.lab.write(self.lab.WORKFLOW, yaml.safe_dump(data))
        with self.assertRaises(ValueError):
            self.lab.check("unknown-key")

    def test_fix_without_diagnosing_does_not_pass(self):
        self.lab.prepare("missing-action")
        self.correct()
        with self.assertRaises(ValueError):
            self.lab.check("missing-action")

    def test_wrong_exercise_is_not_recorded(self):
        self.lab.prepare("unknown-key")
        with self.assertRaises(ValueError):
            self.lab.diagnose("unknown-action")

    def test_prepare_removes_stale_evidence(self):
        self.lab.prepare("unknown-action")
        self.lab.diagnose("unknown-action")
        self.correct()
        self.lab.check("unknown-action")
        self.lab.prepare("unknown-action")
        self.correct()
        with self.assertRaises(ValueError):
            self.lab.check("unknown-action")

    def test_no_version_exercise_really_requires_omission(self):
        self.lab.prepare("no-version")
        self.lab.diagnose("no-version")
        self.correct()
        with self.assertRaises(ValueError):
            self.lab.check("no-version")

    def test_bad_yaml_does_not_pass(self):
        self.lab.prepare("unknown-action")
        self.lab.write(self.lab.WORKFLOW, "workflow: [")
        with self.assertRaises(yaml.YAMLError):
            self.lab.check("unknown-action")

    def test_added_thread_does_not_bypass_workflow(self):
        self.lab.prepare("unknown-action")
        self.lab.diagnose("unknown-action")
        self.correct()
        self.lab.write(self.lab.PROJECT / "workflows" / "thread.yaml", "thread: []\n")
        with self.assertRaises(ValueError):
            self.lab.check("unknown-action")

    def test_index_references_and_text_encoding(self):
        index = json.loads((SCENARIO / "index.json").read_text())
        self.assertEqual(index["backend"]["imageid"], "ubuntu")
        for field in ("text", "background", "foreground"):
            self.assertTrue((SCENARIO / index["details"]["intro"][field]).is_file())
        for step in index["details"]["steps"]:
            for field in ("text", "verify"):
                self.assertTrue((SCENARIO / step[field]).is_file())
        self.assertTrue((SCENARIO / index["details"]["finish"]["text"]).is_file())
        for asset in index["details"]["assets"]["host01"]:
            self.assertTrue((ASSETS / asset["file"]).is_file())
        for path in SCENARIO.rglob("*"):
            if path.suffix in (".md", ".json", ".sh", ".yaml", ".py"):
                content = path.read_bytes()
                self.assertFalse(content.startswith(b"\xef\xbb\xbf"), str(path))
                self.assertNotIn(b"\r\n", content, str(path))
                content.decode("utf-8")


if __name__ == "__main__":
    unittest.main(verbosity=2)
