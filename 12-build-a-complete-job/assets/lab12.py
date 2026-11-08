"""Prepare an empty job and inspect the dedicated MySQL database."""
import argparse
import json
import shutil
import sys
import time

from common import ASSETS, ROOT, JOB, connect, rows, check_rows, csv_rows


def prepare():
    if ROOT.exists() and any(ROOT.iterdir()):
        raise ValueError(f"Refusing to overwrite existing work: {ROOT}")
    JOB.mkdir(parents=True)
    (ROOT / "data").mkdir()
    shutil.copyfile(ASSETS / "products.csv", ROOT / "data/products.csv")
    (ROOT / ".hydra").mkdir()
    (ROOT / ".hydra/project.json").write_text(json.dumps({
        "id": "lab12-complete-job", "name": "build-job"}))
    secret = ROOT / ".hydra/secrets"
    secret.write_text("MYSQL_PASSWORD=lab12-etl-only\n")
    secret.chmod(0o600)
    (ROOT / ".gitignore").write_text(".hydra/secrets\nevidence/\n")
    print("Prepared data and secrets. jobs/products is empty: write all four YAML files.")


def wait():
    deadline = time.monotonic() + 300
    next_message = 0
    last_error = None
    while time.monotonic() < deadline:
        try:
            connection = connect()
            connection.close()
            print("MySQL accepts authenticated connections as etl.")
            return
        except mysql_error_types() as error:
            last_error = error
            if time.monotonic() >= next_message:
                print("Waiting for MySQL initialization...", flush=True)
                next_message = time.monotonic() + 15
            time.sleep(2)
    raise TimeoutError(f"MySQL did not become ready: {last_error}")


def mysql_error_types():
    import mysql.connector
    return (mysql.connector.Error,)


def seed():
    connection = connect()
    try:
        cursor = connection.cursor()
        # The fixture contains simple statements, no routines or quoted semicolons.
        for statement in (ASSETS / "seed.sql").read_text().split(";"):
            if statement.strip():
                cursor.execute(statement)
        connection.commit()
    finally:
        connection.close()
    ready()


def ready():
    check_rows("before")
    if list(JOB.glob("*.yaml")):
        raise ValueError("Initial job must be empty for the from-scratch exercise.")
    if csv_rows(ROOT / "data/products.csv") != csv_rows(ASSETS / "products.csv"):
        raise ValueError("The initial source file is incorrect.")
    print("Ready: source file, secrets, empty job directory, and seeded MySQL table.")


def update_source():
    checkpoint = ROOT / "evidence/first-run.json"
    if not checkpoint.exists():
        raise ValueError("Finish and verify the first run before changing the CSV.")
    check_rows("first")
    target = ROOT / "data/products.csv"
    if csv_rows(target) != csv_rows(ASSETS / "products.csv"):
        raise ValueError("The source has already changed; refusing to overwrite it.")
    backup = ROOT / "data/products.before-second-run.csv"
    if backup.exists():
        raise ValueError("The source backup already exists; refusing overwrite.")
    shutil.copyfile(target, backup)
    shutil.copyfile(ASSETS / "products.updated.csv", target)
    print("Changed SKU-002 to Keyboard Pro, price 34.95, quantity 7. Same three SKUs.")


def show():
    for row in rows():
        print(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "wait", "seed", "ready", "update-source", "show"))
    args = parser.parse_args()
    try:
        globals()[args.action.replace("-", "_")]()
    except Exception as error:
        sys.exit(f"FAIL: {error}")
