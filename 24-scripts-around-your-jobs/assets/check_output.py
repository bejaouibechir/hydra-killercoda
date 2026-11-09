import csv, json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
with (root / 'output' / 'report.csv').open(newline='', encoding='utf-8') as handle:
    rows = list(csv.DictReader(handle))
total = sum(int(row['amount']) for row in rows)
if len(rows) != 3 or total != 42:
    raise SystemExit('Expected three rows with amount total 42')
result = {'rows': len(rows), 'amount_total': total}
(root / 'reports' / 'check.json').write_text(json.dumps(result, indent=2) + '\n')
print(f"CHECK rows={len(rows)} amount_total={total}")
