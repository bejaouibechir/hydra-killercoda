"""Settings and independent MySQL reads for this disposable lab."""
import csv
from decimal import Decimal
import json
import os
from pathlib import Path

import mysql.connector

ASSETS = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("HYDRA_LAB12_ROOT", "/root/lab/build-job"))
JOB = ROOT / "jobs/products"


def connect():
    return mysql.connector.connect(host="127.0.0.1", port=3313, user="etl",
                                   password="lab12-etl-only", database="shop",
                                   connection_timeout=5)


def rows():
    connection = connect()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT sku, name, unit_price, quantity FROM products ORDER BY sku")
        return cursor.fetchall()
    finally:
        connection.close()


def expected(phase):
    records = json.loads((ASSETS / "expected.json").read_text())[phase]
    return [(r[0], r[1], Decimal(r[2]), r[3]) for r in records]


def check_rows(phase):
    actual = rows()
    if actual != expected(phase):
        raise ValueError(f"{phase}: unexpected destination contents: {actual!r}")
    print(f"PASS: {phase}; all {len(actual)} destination rows match.")
    return actual


def csv_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
