"""Create a fresh three-step project from the deployed lesson assets."""
import json
import os
import shutil
from pathlib import Path

assets = Path(__file__).resolve().parent
root = Path(os.environ.get('HYDRA_LAB20_ROOT', '/root/lab/rollback-in-action'))
if root.exists():
    raise SystemExit(f'Refusing to replace an existing project: {root}')
port = int(os.environ.get('LAB20_PORT', '5443'))
for folder in ('data', 'jobs/invoices', 'jobs/payments', 'workflows', 'scripts', 'reports', '.hydra'):
    (root / folder).mkdir(parents=True, exist_ok=True)
(root / '.hydra' / 'project.json').write_text(json.dumps(
    {'id': 'lab20-rollback', 'name': 'rollback-in-action'}), encoding='utf-8')
config = {'host': '127.0.0.1', 'port': port, 'user': 'lab20',
          'password': 'lab20-postgres-only', 'dbname': 'hydra_lab20'}
(root / 'lab20-config.json').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
shutil.copyfile(assets / 'workflow.yaml', root / 'workflows' / 'rollback_demo.yaml')
shutil.copyfile(assets / 'fail.py', root / 'scripts' / 'fail.py')
for name in ('invoices', 'payments'):
    shutil.copyfile(assets / f'{name}.csv', root / 'data' / f'{name}.csv')
    job = root / 'jobs' / name
    (job / 'sources.yaml').write_text(f"""version: '1.0'
sources:
  input:
    type: csv
    connection: {{}}
    extract:
      table: ../../data/{name}.csv
""", encoding='utf-8')
    (job / 'destinations.yaml').write_text(f"""version: '1.0'
destinations:
  target:
    type: postgresql
    connection:
      host: 127.0.0.1
      port: {port}
      user: lab20
      password: lab20-postgres-only
      database: hydra_lab20
      schema: lab20
    load:
      table: {name}
      mode: replace
""", encoding='utf-8')
    (job / 'pipeline.yaml').write_text('pipeline:\n  from: input\n  to: target\n', encoding='utf-8')
print(f'Prepared workflow and two jobs in {root}')
