"""Check fixture boundaries, real manifest parsing, and rejection of false passes."""
import ast
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import yaml

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "assets"))
from common import JOBS, EXPECTED
from exercise import evaluate
from hydra_etl.internal.connector.csv_connector import CSVConnector
from hydra_etl.internal.connector.postgresql_connector import PostgreSQLConnector
from hydra_etl.internal.connector.load_session import resolve_atomic


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def reject(job, code, log, rows):
    try:
        evaluate(job, code, log, rows)
    except ValueError:
        return
    raise AssertionError("Incorrect outcome was accepted")


def main():
    for path in BASE.rglob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    spec = json.loads((BASE / "index.json").read_text())
    details = spec["details"]
    for asset in details["assets"]["host01"]:
        require((BASE / "assets" / asset["file"]).is_file(), asset["file"])
    for step in details["steps"]:
        for key in ("text", "verify"):
            require((BASE / step[key]).is_file(), step[key])
    for key in ("text", "background", "foreground"):
        require((BASE / details["intro"][key]).is_file(), key)
    require((BASE / details["finish"]["text"]).is_file(), "Missing finish")
    require((BASE / "requirements.txt").read_bytes() ==
            (BASE / "assets/requirements.txt").read_bytes(), "Dependency pins differ")
    conn = PostgreSQLConnector("probe", {"connection": {"user": "lab11",
                                "database": "hydra_lab11"}})
    require(resolve_atomic(conn, "append", None)[0] is False, "append default")
    require(resolve_atomic(conn, "upsert", None)[0] is False, "upsert default")
    require(resolve_atomic(conn, "replace", None)[0] is True, "replace default")
    require(resolve_atomic(conn, "append", True)[0] is True, "atomic support")
    for job in JOBS:
        failure = job in ("partial", "atomic")
        evaluate(job, 1 if failure else 0,
                 "violates lab11_quantity_nonnegative" if failure else "", EXPECTED[job])
    reject("atomic", 1, "connection refused", EXPECTED["atomic"])
    reject("partial", 0, "lab11_quantity_nonnegative", EXPECTED["partial"])
    reject("partial", 1, "lab11_quantity_nonnegative", EXPECTED["atomic"])
    wrong = [(1, 999), (2, 25), (3, 30)]
    reject("upsert", 0, "", wrong)

    with tempfile.TemporaryDirectory(prefix="hydra-lab11-") as temp:
        project = Path(temp) / "project"
        env = dict(os.environ, HYDRA_LAB11_ROOT=str(project), HYDRA_LANG="en",
                   PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
        subprocess.run([sys.executable, "-B", str(BASE / "assets/lab11.py"), "prepare"],
                       env=env, check=True)
        for name in JOBS:
            job = project / "jobs" / name
            source = yaml.safe_load((job / "sources.yaml").read_text())
            extract = source["sources"]["incoming"]["extract"]
            require(extract["batch_size"] == 100, "Uncontrolled batch size")
            require((job / extract["table"]).resolve().is_file(), "Missing source")
            result = subprocess.run(
                [sys.executable, "-B", "-m", "hydra_etl.cli.hdrctl", "validate", str(job)],
                cwd=project, env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=90)
            require(result.returncode == 0, result.stdout + result.stderr)
            print(f"PASS: real CLI validation of {name}")
        csv_conn = CSVConnector("fixture", {"connection": {}}, job_dir=str(project))
        batches = list(csv_conn.extract_batches(table="data/failure.csv", batch_size=100))
        require([len(batch) for batch in batches] == [100, 100, 100, 100],
                "CSV connector did not yield four 100-row batches")
        bad = [(index + 1, offset + 1) for index, batch in enumerate(batches)
               for offset, row in enumerate(batch) if int(row["quantity"]) < 0]
        require(bad == [(3, 1)], "Failure must be first row of batch 3 only")
        require(int(batches[2][0]["id"]) == 1201, "Wrong failed ID")
        print("PASS: actual CSV extraction places the invalid row at batch 3")
        repeat = subprocess.run(
            [sys.executable, "-B", str(BASE / "assets/lab11.py"), "prepare"],
            env=env, capture_output=True)
        require(repeat.returncode != 0, "Existing project must not be overwritten")
    print("PASS: references, policy defaults, expected outcomes and failure rejection")
    print("This offline check does not establish live PostgreSQL behavior.")


if __name__ == "__main__":
    main()
