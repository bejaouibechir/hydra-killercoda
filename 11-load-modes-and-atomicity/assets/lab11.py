"""Prepare the project, seed its dedicated schema, and inspect real data."""
import argparse
import csv
import json
import shutil
import sys
import time

import yaml

from common import ASSETS, ROOT, JOBS, BASELINE, connect, transaction, rows


def prepare():
    if ROOT.exists() and any(ROOT.iterdir()):
        raise ValueError(f"Refusing to overwrite non-empty project: {ROOT}")
    (ROOT / "data").mkdir(parents=True)
    for name in ("products.csv", "failure.csv"):
        shutil.copyfile(ASSETS / name, ROOT / "data" / name)
    for name, table in JOBS.items():
        job = ROOT / "jobs" / name
        job.mkdir(parents=True)
        source = yaml.safe_load((ASSETS / "sources.template.yaml").read_text())
        destination = yaml.safe_load((ASSETS / "destinations.template.yaml").read_text())
        load = destination["destinations"]["target"]["load"]
        load.update(table=table, mode=name if name in ("append", "replace", "upsert")
                    else "append")
        if name == "upsert":
            load["key"] = ["id"]
        if name in ("partial", "atomic"):
            source["sources"]["incoming"]["extract"]["table"] = "../../data/failure.csv"
            load["atomic"] = name == "atomic"
        for filename, content in (("sources.yaml", source),
                                  ("destinations.yaml", destination)):
            (job / filename).write_text(yaml.safe_dump(content, sort_keys=False),
                                       encoding="utf-8")
        shutil.copyfile(ASSETS / "pipeline.yaml", job / "pipeline.yaml")
    (ROOT / ".hydra").mkdir()
    (ROOT / ".hydra/project.json").write_text(json.dumps({
        "id": "lab11-load-modes", "name": "load-modes"}), encoding="utf-8")
    secret = ROOT / ".hydra/secrets"
    secret.write_text("PG_PASSWORD=lab11-postgres-only\n", encoding="utf-8")
    secret.chmod(0o600)
    (ROOT / ".gitignore").write_text(".hydra/secrets\nevidence/\n", encoding="utf-8")
    print(f"Prepared five jobs in {ROOT}")


def seed():
    # CREATE SCHEMA deliberately refuses an existing schema; no silent reset.
    with transaction() as connection:
        with connection.cursor() as cursor:
            cursor.execute((ASSETS / "seed.sql").read_text(encoding="utf-8"))
    ready()


def ready():
    for job in JOBS:
        if rows(job) != BASELINE:
            raise ValueError(f"{job}: expected the two baseline rows.")
    with transaction() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) FROM pg_constraint c "
                "JOIN pg_namespace n ON n.oid=c.connamespace "
                "WHERE n.nspname='lab11' AND c.conname='lab11_quantity_nonnegative'")
            if cursor.fetchone()[0] != 2:
                raise ValueError("The two deliberate failure constraints are missing.")
    print("PASS: all five destination tables contain the two baseline rows.")


def wait():
    deadline = time.monotonic() + 300
    next_message = 0
    last_error = None
    while time.monotonic() < deadline:
        try:
            connection = connect()
            connection.close()
            print("PostgreSQL is accepting connections.")
            return
        except Exception as error:
            last_error = error
            if time.monotonic() >= next_message:
                print("Waiting for PostgreSQL to accept authenticated connections...", flush=True)
                next_message = time.monotonic() + 15
            time.sleep(2)
    raise TimeoutError(f"PostgreSQL did not become ready within five minutes: {last_error}")


def show(job):
    if job == "source":
        print((ROOT / "data/products.csv").read_text())
        with (ROOT / "data/failure.csv").open(newline="") as handle:
            data = list(csv.DictReader(handle))
        print("Failure file: 400 rows; batch_size: 100.")
        for index in (0, 99, 100, 199, 200, 299, 300, 399):
            print(f"Data row {index + 1}: {data[index]}")
        return
    actual = rows(job)
    print(f"{JOBS[job]}: {len(actual)} rows")
    selected = actual if len(actual) < 12 else actual[:5] + actual[-3:]
    for row in selected:
        print(row)
    if len(actual) >= 12:
        print("(First five and last three rows shown.)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "seed", "ready", "wait", "show"))
    parser.add_argument("target", nargs="?", choices=("source", *JOBS))
    args = parser.parse_args()
    try:
        if args.action == "show":
            if not args.target:
                parser.error("show requires source or a job name")
            show(args.target)
        else:
            globals()[args.action]()
    except Exception as error:
        sys.exit(f"FAIL: {error}")
