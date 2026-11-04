"""Shared settings for the dedicated, disposable PostgreSQL lab."""
from contextlib import contextmanager
import os
from pathlib import Path

import psycopg2
from psycopg2 import sql

ASSETS = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("HYDRA_LAB11_ROOT", "/root/lab/load-modes"))
BASELINE = [(1, 10), (2, 20)]
JOBS = {
    "append": "mode_append",
    "replace": "mode_replace",
    "upsert": "mode_upsert",
    "partial": "partial_load",
    "atomic": "atomic_load",
}
EXPECTED = {
    "append": [(1, 10), (2, 20), (2, 25), (3, 30)],
    "replace": [(2, 25), (3, 30)],
    "upsert": [(1, 10), (2, 25), (3, 30)],
    "partial": BASELINE + [(1000 + i, i) for i in range(1, 201)],
    "atomic": BASELINE,
}


def connect():
    return psycopg2.connect(host="127.0.0.1", port=5441, user="lab11",
                            password="lab11-postgres-only", dbname="hydra_lab11",
                            connect_timeout=5)


@contextmanager
def transaction():
    connection = connect()
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def rows(job):
    with transaction() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT id, quantity FROM lab11.{} ORDER BY id, quantity")
                           .format(sql.Identifier(JOBS[job])))
            return cursor.fetchall()
