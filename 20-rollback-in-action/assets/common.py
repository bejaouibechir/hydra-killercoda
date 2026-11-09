"""Local PostgreSQL helpers for this disposable lesson schema only."""
import json
import os
from pathlib import Path

import psycopg2

ROOT = Path(os.environ.get('HYDRA_LAB20_ROOT', '/root/lab/rollback-in-action'))
BASELINE = [(1, 100)]
LOADED = {'invoices': [(2, 200), (3, 300)],
          'payments': [(2, 220), (3, 330)]}
JOURNAL = ROOT / '.hydra' / 'undo' / 'rollback_demo.json'


def connect():
    config = json.loads((ROOT / 'lab20-config.json').read_text(encoding='utf-8'))
    return psycopg2.connect(**config)


def snapshot():
    result = {}
    with connect() as db:
        with db.cursor() as cursor:
            for name in ('invoices', 'payments'):
                cursor.execute(f'SELECT id, amount FROM lab20.{name} ORDER BY id')
                result[name] = [list(row) for row in cursor.fetchall()]
    return result


def baseline():
    return {'invoices': [[1, 100]], 'payments': [[1, 100]]}
