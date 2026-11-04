"""Run actual Hydra jobs, retain logs, and verify database values independently."""
import argparse
import importlib.metadata
import json
import os
import subprocess
import sys

from common import ROOT, JOBS, BASELINE, EXPECTED, rows

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def evaluate(job, exit_code, log, actual):
    if actual != EXPECTED[job]:
        raise ValueError(f"{job}: unexpected database contents ({len(actual)} rows).")
    if job in ("partial", "atomic"):
        if exit_code == 0 or "lab11_quantity_nonnegative" not in log:
            raise ValueError("Expected the deliberate PostgreSQL check-constraint error.")
    elif exit_code != 0:
        raise ValueError("A normal load failed; inspect the saved CLI log.")


def run(job):
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    report_file = evidence / f"{job}.json"
    log_file = evidence / f"{job}.log"
    if report_file.exists() or log_file.exists() or rows(job) != BASELINE:
        raise ValueError("This variant has already run or changed. Use a fresh lab instance.")
    env = dict(os.environ, HYDRA_LANG="en", PYTHONUTF8="1",
               PYTHONDONTWRITEBYTECODE="1", NO_COLOR="1")
    for variable in ("PG_PASSWORD", "HYDRA_SECRETS_FILE", "HYDRA_ENV"):
        env.pop(variable, None)
    result = subprocess.run(
        [sys.executable, "-B", "-m", "hydra_etl.cli.hdrctl", "run",
         str(ROOT / "jobs" / job)],
        cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120)
    log = result.stdout + "\n" + result.stderr
    log_file.write_text(log, encoding="utf-8")
    actual = rows(job)
    report = {"job": job, "hydra_version": importlib.metadata.version("hydra-etl"),
              "cli_exit_code": result.returncode, "rows_after": len(actual),
              "rows": actual}
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(log)
    evaluate(job, result.returncode, log, actual)
    print(f"PASS: {job}; Hydra exit={result.returncode}; destination rows={len(actual)}")
    if job in ("partial", "atomic"):
        print("The Hydra job failed as intended; the lesson check passed.")


def check(selection):
    selected = ("append", "replace", "upsert") if selection == "modes" else (
        tuple(JOBS) if selection == "all" else (selection,))
    for job in selected:
        report = json.loads((ROOT / f"evidence/{job}.json").read_text())
        log = (ROOT / f"evidence/{job}.log").read_text(encoding="utf-8")
        actual = rows(job)
        evaluate(job, report["cli_exit_code"], log, actual)
        if report["rows"] != [list(row) for row in actual]:
            raise ValueError("Current table differs from the recorded result.")
        print(f"PASS: {job} ({len(actual)} rows)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("run", "check"))
    parser.add_argument("job", choices=(*JOBS, "modes", "all"))
    args = parser.parse_args()
    try:
        if args.action == "run":
            if args.job not in JOBS:
                parser.error("Run one variant at a time.")
            run(args.job)
        else:
            check(args.job)
    except Exception as error:
        sys.exit(f"FAIL: {error}")
