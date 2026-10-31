"""Build and check the MySQL-to-PostgreSQL product lesson."""
import argparse
from decimal import Decimal, ROUND_HALF_UP
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ASSETS = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("HYDRA_LAB09_ROOT", "/root/lab/sql-products"))
SEED = [(1, "Notebook", Decimal("12.50"), 4),
        (2, "Keyboard", Decimal("19.95"), 3),
        (3, "Monitor", Decimal("149.90"), 2),
        (4, "USB cable", Decimal("4.25"), 0),
        (5, "Mouse", Decimal("8.75"), 6)]
MYSQL = dict(host="127.0.0.1", port=3309, user="lab09_reader",
             password="lab09-mysql-only", database="shop", connection_timeout=5)
POSTGRES = dict(host="127.0.0.1", port=5439, user="lab09_writer",
                password="lab09-postgres-only", dbname="warehouse", connect_timeout=5)


def expected():
    records = json.loads((ASSETS / "expected.json").read_text(encoding="utf-8"))
    return [(row["id"], row["product_name"], Decimal(row["total"])) for row in records]


def prepare():
    if ROOT.exists() and any(ROOT.iterdir()):
        raise ValueError(f"Refusing to overwrite a non-empty folder: {ROOT}")
    job = ROOT / "jobs/products"
    job.mkdir(parents=True, exist_ok=True)
    (ROOT / "solutions").mkdir()
    (ROOT / ".hydra").mkdir()
    for name in ("sources.yaml", "destinations.yaml", "pipeline.yaml"):
        shutil.copyfile(ASSETS / name, job / name)
    shutil.copyfile(ASSETS / "transformations.solution.yaml",
                    ROOT / "solutions/transformations.yaml")
    (ROOT / ".hydra/project.json").write_text(json.dumps({
        "id": "lab09-products", "name": "sql-products"}), encoding="utf-8")
    secrets = ROOT / ".hydra/secrets"
    secrets.write_text("MYSQL_PASSWORD=lab09-mysql-only\nPG_PASSWORD=lab09-postgres-only\n",
                       encoding="utf-8")
    secrets.chmod(0o600)
    (ROOT / ".gitignore").write_text(".hydra/secrets\n", encoding="utf-8")
    print(f"Ready: {ROOT}")


def mysql_rows():
    import mysql.connector
    connection = mysql.connector.connect(**MYSQL)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, unit_price, quantity FROM product ORDER BY id")
        return cursor.fetchall()
    finally:
        connection.close()


def pg_query(sql, parameters=None, write=False):
    import psycopg2
    connection = psycopg2.connect(**POSTGRES)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, parameters)
            if write:
                connection.commit()
                return None
            return cursor.fetchall()
    finally:
        connection.close()


def destination():
    return pg_query("SELECT id, product_name, total FROM public.product_totals ORDER BY id")


def connections():
    if mysql_rows() != SEED:
        raise ValueError("MySQL product does not contain the five expected source records.")
    columns = pg_query("SELECT column_name, data_type, numeric_precision, numeric_scale "
                       "FROM information_schema.columns WHERE table_schema = 'public' "
                       "AND table_name = 'product_totals' ORDER BY ordinal_position")
    if [(c[0], c[1]) for c in columns] != [
            ("id", "integer"), ("product_name", "character varying"), ("total", "numeric")]:
        raise ValueError("PostgreSQL destination has unexpected columns or types.")
    if columns[2][2:] != (14, 2):
        raise ValueError("Destination total must be NUMERIC(14,2).")
    print("PASS: MySQL source data and PostgreSQL destination schema are correct.")


def wait_databases():
    last_error = None
    for _ in range(150):
        try:
            connections()
            return
        except Exception as error:
            last_error = error
            time.sleep(2)
    raise RuntimeError(f"Databases did not become ready: {last_error}")


def run_cli(*args):
    env = dict(os.environ, HYDRA_LANG="en", PYTHONUTF8="1",
               PYTHONDONTWRITEBYTECODE="1")
    # Use only this disposable project's secrets, even on a configured workstation.
    for name in ("MYSQL_PASSWORD", "PG_PASSWORD", "HYDRA_SECRETS_FILE", "HYDRA_ENV"):
        env.pop(name, None)
    result = subprocess.run([sys.executable, "-B", "-m", "hydra_etl.cli.hdrctl", *args],
                            cwd=ROOT, env=env, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=90)
    if result.returncode:
        raise ValueError(result.stdout + result.stderr)
    return result


def manifests():
    job = ROOT / "jobs/products"
    for name in ("sources.yaml", "destinations.yaml", "pipeline.yaml"):
        actual = yaml.safe_load((job / name).read_text(encoding="utf-8"))
        reference = yaml.safe_load((ASSETS / name).read_text(encoding="utf-8"))
        if actual != reference:
            raise ValueError(f"Keep the supplied {name}; this exercise edits transformations.yaml.")


def transformed_rows(raw):
    import pandas as pd
    from hydra_etl.internal.engines.pandas_engine import PandasEngine
    from hydra_etl.internal.parser.transform import TransformParser
    parsed = TransformParser().parse(raw)
    steps = [{"op": item.op, "params": item.params} for item in parsed.steps]
    frame = pd.DataFrame(SEED, columns=["id", "name", "unit_price", "quantity"])
    output = PandasEngine().apply_pipeline(frame, steps).output
    if list(output.columns) != ["id", "product_name", "total"]:
        raise ValueError("Keep exactly id, product_name and total, in that order.")
    return sorted([(int(row.id), row.product_name,
                    Decimal(str(row.total)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
                   for row in output.itertuples(index=False)])


def transform():
    manifests()
    raw = yaml.safe_load((ROOT / "jobs/products/transformations.yaml").read_text(encoding="utf-8"))
    if transformed_rows(raw) != expected():
        raise ValueError("The transformation does not produce all five expected records.")
    run_cli("run", "jobs/products", "--dry-run")
    print("PASS: transformation values and real CLI dry-run are correct.")


def check(stage):
    if stage in ("connections", "ready"):
        manifests()
        connections()
        if stage == "ready" and destination():
            raise ValueError("The destination must be empty before the lab begins.")
    elif stage == "transform":
        transform()
    elif stage == "result":
        transform()
        connections()
        if destination() != expected():
            raise ValueError("PostgreSQL must contain exactly the five expected IDs, names and totals.")
        print("PASS: PostgreSQL contains all five expected product totals.")


def show(which):
    headers = ["id", "name", "unit_price", "quantity"] if which == "source" else [
        "id", "product_name", "total"]
    rows = mysql_rows() if which == "source" else destination()
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(value) for value in row))
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "wait", "show", "check"])
    parser.add_argument("target", nargs="?")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            prepare()
        elif args.command == "wait":
            wait_databases()
        elif args.command == "show" and args.target in ("source", "destination"):
            show(args.target)
        elif args.command == "check" and args.target in ("ready", "connections", "transform", "result"):
            check(args.target)
        else:
            parser.error("Use show source|destination or check ready|connections|transform|result.")
    except Exception as error:
        parser.exit(1, f"FAIL: {error}\n")
