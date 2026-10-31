"""Prepare and verify the CSV lesson using the real Hydra CLI."""
import argparse
import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ASSETS = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("HYDRA_LAB08_ROOT", "/root/lab/csv-shapes"))
CASES = ("comma", "semicolon", "latin1")
ROWS = [["id", "customer", "city"], ["1", "Jos\u00e9", "Madrid"],
        ["2", "Zo\u00eb", "London"], ["3", "M\u00fcller", "Berlin"]]


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.reader(stream))


def source(case, fixed=False):
    connection = {}
    if case == "latin1" or (case == "semicolon" and fixed):
        connection["delimiter"] = ";"
    if case == "latin1" and fixed:
        connection["encoding"] = "latin-1"
    return {"version": "1.0", "sources": {"orders": {
        "type": "csv", "connection": connection,
        "extract": {"table": "../../data/orders-" + case + ".csv"}}}}


def write_yaml(path, value):
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def prepare():
    if ROOT.exists() and any(ROOT.iterdir()):
        raise ValueError(f"Refusing to overwrite a non-empty lab folder: {ROOT}")
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "data").mkdir()
    (ROOT / "outputs").mkdir()
    (ROOT / "evidence").mkdir()
    (ROOT / "solutions").mkdir()
    (ROOT / ".hydra").mkdir()
    (ROOT / ".hydra" / "project.json").write_text(
        json.dumps({"id": "csv-shapes", "name": "csv-shapes"}), encoding="utf-8")
    for case in CASES:
        shutil.copyfile(ASSETS / ("orders-" + case + ".csv"),
                        ROOT / "data" / ("orders-" + case + ".csv"))
        job = ROOT / "jobs" / case
        job.mkdir(parents=True)
        write_yaml(job / "sources.yaml", source(case))
        write_yaml(ROOT / "solutions" / ("sources-" + case + ".yaml"), source(case, True))
        write_yaml(job / "destinations.yaml", {"version": "1.0", "destinations": {
            "result": {"type": "csv", "connection": {},
                       "load": {"table": "../../outputs/" + case + ".csv", "mode": "replace"}}}})
        write_yaml(job / "pipeline.yaml", {"version": "1.0",
                   "pipeline": {"from": "orders", "to": "result"}})
    print(f"Ready: {ROOT}")


def run(case):
    env = dict(os.environ, HYDRA_LANG="en", HYDRA_ENV="",
               PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([sys.executable, "-B", "-m", "hydra_etl.cli.hdrctl",
                           "run", "jobs/" + case], cwd=ROOT, env=env,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=60)


def assert_source(case, fixed):
    value = yaml.safe_load((ROOT / "jobs" / case / "sources.yaml").read_text(encoding="utf-8"))
    if value != source(case, fixed):
        raise ValueError("Keep the supplied source and change only the requested connection settings.")


def diagnose(case):
    if case == "comma":
        raise ValueError("The comma exercise has no deliberate error.")
    assert_source(case, False)
    output = ROOT / "outputs" / (case + ".csv")
    if output.exists():
        output.unlink()
    result = run(case)
    print(result.stdout)
    print(result.stderr)
    print(f"Exit code: {result.returncode}")
    if case == "semicolon":
        expected = [[";".join(row)] for row in ROWS]
        if result.returncode != 0 or read_csv(output) != expected:
            raise ValueError("Expected a successful run with one incorrectly parsed column.")
        print("Observation: the job succeeded, but every row has ONE column.")
    else:
        detail = (result.stdout + result.stderr).lower()
        if result.returncode == 0 or "decode" not in detail or "utf-8" not in detail:
            raise ValueError("Expected a UTF-8 decoding failure.")
        if output.exists():
            raise ValueError("A failed read unexpectedly produced output.")
        print("Observation: the Latin-1 bytes cannot be decoded as UTF-8.")
    (ROOT / "evidence" / (case + ".json")).write_text(json.dumps({
        "case": case, "returncode": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr}), encoding="utf-8")


def inspect(case):
    rows = read_csv(ROOT / "outputs" / (case + ".csv"))
    print(f"Columns ({len(rows[0])}): {rows[0]}")
    for row in rows[1:]:
        print(row)


def check(case):
    assert_source(case, True)
    if case != "comma":
        evidence = json.loads((ROOT / "evidence" / (case + ".json")).read_text(encoding="utf-8"))
        if evidence["case"] != case:
            raise ValueError("Diagnostic evidence belongs to another exercise.")
        if case == "semicolon" and evidence["returncode"] != 0:
            raise ValueError("First observe the incorrect delimiter with diagnose semicolon.")
        if case == "latin1" and (evidence["returncode"] == 0 or
                                "decode" not in (evidence["stdout"] + evidence["stderr"]).lower()):
            raise ValueError("First observe the decoding error with diagnose latin1.")
    output = ROOT / "outputs" / (case + ".csv")
    if read_csv(output) != ROWS:
        raise ValueError("Run the corrected job: its output must have three columns and all three expected rows.")
    result = run(case)
    if result.returncode != 0 or read_csv(output) != ROWS:
        raise ValueError("A fresh run did not reproduce the expected result.\n" + result.stdout + result.stderr)
    print(f"PASS: {case} has the correct settings, columns, values and three rows.")


def compare():
    for case in CASES:
        if read_csv(ROOT / "outputs" / (case + ".csv")) != ROWS:
            raise ValueError(f"{case}: output does not match the expected data.")
    print("PASS: all three inputs produce the same UTF-8 CSV data.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "diagnose", "inspect", "check", "compare"])
    parser.add_argument("case", nargs="?", choices=CASES)
    args = parser.parse_args()
    try:
        if args.command in ("prepare", "compare"):
            globals()[args.command]()
        else:
            if args.case is None:
                parser.error("This command requires comma, semicolon or latin1.")
            globals()[args.command](args.case)
    except (OSError, ValueError, KeyError, yaml.YAMLError, subprocess.SubprocessError) as error:
        parser.exit(1, f"FAIL: {error}\n")
