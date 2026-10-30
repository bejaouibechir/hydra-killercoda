#!/usr/bin/env python3
"""Create and check the lab project. Never execute a workflow: dry-run only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import yaml

RESOURCES = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("HYDRA_LAB07_ROOT", "/root/lab")).resolve()
PROJECT = ROOT / "error-messages"
WORKFLOW = PROJECT / "workflows" / "errors.yaml"
EVIDENCE = ROOT / "lab07-evidence"
CASES = {
    "unknown-action": ("unknown action 'webhok'", "did you mean 'webhook'"),
    "unknown-key": ("unknown key 'depend_on'", "did you mean 'depends_on'"),
    "missing-action": ("type=action requires the 'action' field",),
    "no-version": (),
}


def read(path):
    return path.read_text(encoding="utf-8")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run_cli():
    command = shutil.which("hdrctl")
    require(command is not None, "hdrctl is missing. Wait for setup to finish.")
    return subprocess.run(
        [command, "run", ".", "--dry-run"],
        cwd=PROJECT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=30,
        env={**os.environ, "HYDRA_LANG": "en", "PYTHONUTF8": "1",
             "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"},
    )


def prepare(case):
    require(ROOT.is_dir(), "The lab root is missing.")
    require(case in CASES, "Unknown exercise.")
    (PROJECT / ".hydra").mkdir(parents=True, exist_ok=True)
    write(PROJECT / ".hydra" / "project.json",
          json.dumps({"name": "error-messages"}, indent=2) + "\n")
    write(WORKFLOW, read(RESOURCES / (case + ".yaml")))
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    # Starting an exercise invalidates its earlier diagnostic evidence.
    for suffix in (".json", ".log"):
        path = EVIDENCE / (case + suffix)
        if path.exists():
            path.unlink()
    print("Prepared exercise: " + case)
    print("Edit: " + str(WORKFLOW))


def diagnose(case):
    require(WORKFLOW.is_file(), "Prepare the exercise first.")
    before = read(WORKFLOW)
    reference = read(RESOURCES / (case + ".yaml"))
    require(yaml.safe_load(before) == yaml.safe_load(reference),
            "This is not the initial exercise. Run prepare for this case before diagnosing it.")
    result = run_cli()
    output = result.stdout + result.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    print("Exit code: " + str(result.returncode))
    expected_code = 0 if case == "no-version" else 1
    require(result.returncode == expected_code,
            "Unexpected exit code. Read the output; this may be an environment issue.")
    require(all(token in output for token in CASES[case]),
            "The output does not contain the expected diagnostic.")
    write(EVIDENCE / (case + ".log"), output)
    write(EVIDENCE / (case + ".json"), json.dumps({
        "case": case, "exit_code": result.returncode,
        "workflow": before,
        "sha256": hashlib.sha256(before.encode()).hexdigest(),
    }, indent=2) + "\n")
    # The wrapper succeeds after recording an EXPECTED rejection. The printed
    # exit code above is the actual hdrctl exit code, not the wrapper's.
    print("Diagnostic saved. Correct the file, then click Check." if case != "no-version"
          else "No version field, and validation still succeeds. Click Check.")


def check(case):
    require(WORKFLOW.is_file(), "The exercise workflow is missing.")
    manifest = yaml.safe_load(read(WORKFLOW))
    expected = yaml.safe_load(read(RESOURCES / "solution.yaml"))
    if case == "no-version":
        expected.pop("version")
    require(manifest == expected,
            "Keep the supplied workflow and correct only the requested field.")
    evidence_path = EVIDENCE / (case + ".json")
    log_path = EVIDENCE / (case + ".log")
    require(evidence_path.is_file() and log_path.is_file(),
            "Run the exercise's diagnose command before fixing the file.")
    evidence = json.loads(read(evidence_path))
    initial = yaml.safe_load(read(RESOURCES / (case + ".yaml")))
    require(evidence.get("case") == case and
            yaml.safe_load(evidence.get("workflow", "")) == initial,
            "The saved diagnostic belongs to a different exercise.")
    expected_code = 0 if case == "no-version" else 1
    require(evidence.get("exit_code") == expected_code,
            "The expected exit code was not recorded.")
    require(all(token in read(log_path) for token in CASES[case]),
            "The expected diagnostic was not recorded.")
    require((PROJECT / ".hydra").is_dir(), "The project marker is missing.")
    require(not (PROJECT / "workflows" / "thread.yaml").exists(),
            "This exercise uses the default thread; remove the added thread.yaml.")
    require(sorted(p.name for p in (PROJECT / "workflows").iterdir()
                   if p.suffix in (".yaml", ".yml")) == ["errors.yaml"],
            "Keep errors.yaml as the only workflow.")
    result = run_cli()
    require(result.returncode == 0,
            "The corrected project still fails its dry-run:\n" + result.stdout + result.stderr)
    print("PASS: " + case)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "diagnose", "check"])
    parser.add_argument("case", choices=list(CASES))
    args = parser.parse_args()
    try:
        {"prepare": prepare, "diagnose": diagnose, "check": check}[args.command](args.case)
    except (ValueError, OSError, subprocess.SubprocessError, yaml.YAMLError) as exc:
        print("Check failed: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
