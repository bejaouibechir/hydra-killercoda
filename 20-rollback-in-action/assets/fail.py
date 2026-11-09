"""The third action fails; an optional outside write stops automatic undo."""
import json
from pathlib import Path

import psycopg2

root = Path(__file__).resolve().parents[1]
if (root / 'data' / 'interrupt.flag').exists():
    config = json.loads((root / 'lab20-config.json').read_text(encoding='utf-8'))
    with psycopg2.connect(**config) as db:
        with db.cursor() as cursor:
            cursor.execute('INSERT INTO lab20.payments (id, amount) VALUES (999, 999)')
    print('A separate writer added payment 999 after the load')
raise SystemExit('intentional failure at step three')
