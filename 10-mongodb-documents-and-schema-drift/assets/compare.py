"""Run the real CLI and retain evidence; never implement drift behavior here."""
import argparse
import csv
from decimal import Decimal
import json
import os
from pathlib import Path
import subprocess
import sys

from lab10 import ROOT, POLICIES, URI, collection, fixture, verify_collection


def read_output(path):
    if not path.exists():
        return [], []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return reader.fieldnames or [], rows


def evaluate(policy, code, log, headers, rows):
    drift_message = "sales_channel" in log and any(
        term in log.lower() for term in ("drift", "unexpected", "extra", "schema"))
    if policy == "fail":
        return code != 0 and drift_message and not rows
    baseline = {"_id", "customer", "amount"}
    expected_columns = baseline | ({"sales_channel"} if policy == "adapt" else set())
    if code != 0 or set(headers) != expected_columns or len(rows) != 102:
        return False
    by_id = {row["_id"]: row for row in rows}
    if len(by_id) != 102:
        return False
    for doc in fixture():
        row = by_id.get(doc["_id"], {})
        if row.get("customer") != doc["customer"]:
            return False
        if Decimal(row.get("amount", "NaN")) != Decimal(doc["amount"]):
            return False
        if policy == "adapt" and row.get("sales_channel") != doc.get("sales_channel", ""):
            return False
    return policy == "adapt" or (drift_message and "warn" in log.lower())


def run(policy):
    from pymongo import MongoClient
    with MongoClient(URI) as client:
        verify_collection(collection(client))
    job = ROOT / "jobs" / policy
    output = job / "output/orders.csv"
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    # Each variant runs once in a fresh project; never mistake stale output for
    # the result of a failed CLI invocation.
    if output.exists() or (evidence / f"{policy}.json").exists():
        raise ValueError("Evidence already exists for this variant. Use a fresh lab instance.")
    env = dict(os.environ, HYDRA_LANG="en", PYTHONUTF8="1",
               PYTHONDONTWRITEBYTECODE="1", NO_COLOR="1")
    result = subprocess.run(
        [sys.executable, "-B", "-m", "hydra_etl.cli.hdrctl", "run", str(job)],
        cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120)
    log = result.stdout + "\n" + result.stderr
    (evidence / f"{policy}.log").write_text(log, encoding="utf-8")
    headers, rows = read_output(output)
    passed = evaluate(policy, result.returncode, log, headers, rows)
    report = {"policy": policy, "cli_exit_code": result.returncode,
              "columns": headers, "rows": len(rows), "contract_passed": passed}
    (evidence / f"{policy}.json").write_text(json.dumps(report, indent=2))
    print(log)
    print(json.dumps(report, indent=2))
    if not passed:
        raise ValueError("Observed behavior does not satisfy this variant's acceptance criteria.")


def check(policies):
    for policy in policies:
        report = json.loads((ROOT / f"evidence/{policy}.json").read_text())
        log = (ROOT / f"evidence/{policy}.log").read_text(encoding="utf-8")
        headers, rows = read_output(ROOT / f"jobs/{policy}/output/orders.csv")
        if not evaluate(policy, report["cli_exit_code"], log, headers, rows):
            raise ValueError(f"{policy}: the recorded run does not meet the drift contract.")
        print(f"PASS: {policy}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("run", "check"))
    parser.add_argument("policy", choices=(*POLICIES, "all"))
    args = parser.parse_args()
    try:
        if args.action == "run":
            if args.policy == "all":
                parser.error("Run each policy individually to inspect its evidence.")
            run(args.policy)
        else:
            check(POLICIES if args.policy == "all" else (args.policy,))
    except Exception as error:
        sys.exit(f"FAIL: {error}")
