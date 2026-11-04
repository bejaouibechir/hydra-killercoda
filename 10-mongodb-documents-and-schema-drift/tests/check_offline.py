"""Offline integrity and false-positive checks; no database or engine changes."""
import ast
import copy
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import yaml

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "assets"))
import compare
from lab10 import fixture


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    docs = fixture()
    require(len(docs) == 102, "Expected 102 documents")
    require(len({d["_id"] for d in docs}) == 102, "IDs must be unique")
    require(all(set(d) == {"_id", "customer", "amount"} for d in docs[:100]),
            "Baseline sample must not contain drift")
    require([d["sales_channel"] for d in docs[100:]] == ["web", "store"],
            "Two drift values must be distinguishable")
    for path in BASE.rglob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    spec = json.loads((BASE / "index.json").read_text())
    details = spec["details"]
    for item in details["assets"]["host01"]:
        require((BASE / "assets" / item["file"]).is_file(), item["file"])
    for step in details["steps"]:
        for key in ("text", "verify"):
            require((BASE / step[key]).is_file(), step[key])
    for key in ("text", "background", "foreground"):
        require((BASE / details["intro"][key]).is_file(), key)
    require((BASE / details["finish"]["text"]).is_file(), "finish.md")
    require((BASE / "requirements.txt").read_bytes() ==
            (BASE / "assets/requirements.txt").read_bytes(), "Requirement pins differ")

    baseline = [{key: str(doc[key]) for key in ("_id", "customer", "amount")}
                for doc in docs]
    adapted = [{**row, "sales_channel": doc.get("sales_channel", "")}
               for row, doc in zip(baseline, docs)]
    columns = ["_id", "customer", "amount"]
    warning = "WARNING: schema drift: unexpected field sales_channel"
    require(compare.evaluate("warn", 0, warning, columns, baseline), "Valid warn")
    require(not compare.evaluate("warn", 0, "", columns, baseline), "Silent warn")
    require(compare.evaluate("fail", 1, "Unexpected field sales_channel", [], []),
            "Valid fail")
    require(not compare.evaluate("fail", 0, "", columns, baseline), "Silent fail")
    require(not compare.evaluate("fail", 1, "Connection refused", [], []),
            "Unrelated error must not count")
    require(compare.evaluate("adapt", 0, "", columns + ["sales_channel"], adapted),
            "Valid adapt")
    require(not compare.evaluate("adapt", 0, "", columns, baseline), "Dropped field")
    damaged = copy.deepcopy(adapted)
    damaged[-1]["sales_channel"] = ""
    require(not compare.evaluate("adapt", 0, "", columns + ["sales_channel"], damaged),
            "Lost new value")
    require(not compare.evaluate("adapt", 0, "", columns + ["sales_channel"], adapted[:-1]),
            "Lost source row")

    with tempfile.TemporaryDirectory(prefix="hydra-lab10-") as temporary:
        project = Path(temporary) / "project"
        env = dict(os.environ, HYDRA_LAB10_ROOT=str(project), HYDRA_LANG="en",
                   PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
        subprocess.run([sys.executable, "-B", str(BASE / "assets/lab10.py"), "prepare"],
                       env=env, check=True)
        for policy in ("warn", "fail", "adapt"):
            job = project / "jobs" / policy
            source = yaml.safe_load((job / "sources.yaml").read_text())
            require(source["sources"]["orders"]["schema"]["drift_policy"] == policy,
                    "Wrong policy")
            result = subprocess.run(
                [sys.executable, "-B", "-m", "hydra_etl.cli.hdrctl", "validate", str(job)],
                cwd=project, env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=90)
            require(result.returncode == 0, result.stdout + result.stderr)
            print(f"PASS: real Hydra CLI validation of {policy}")
        second = subprocess.run(
            [sys.executable, "-B", str(BASE / "assets/lab10.py"), "prepare"],
            env=env, capture_output=True, text=True)
        require(second.returncode != 0, "Must refuse to overwrite prepared work")
    print("PASS: fixtures, references, parsing, output checks, and overwrite guard")
    print("NOTE: these checks do not validate live MongoDB or drift support.")


if __name__ == "__main__":
    main()
