import json, os, shutil
from pathlib import Path
assets = Path(__file__).resolve().parent
root = Path(os.environ.get('HYDRA_LAB24_ROOT', '/root/lab/scripts-around-jobs'))
if root.exists(): raise SystemExit(f'Refusing to replace {root}')
for folder in ('.hydra','workflows','jobs/copy_orders','input','archive','output','reports','scripts'):
    (root / folder).mkdir(parents=True, exist_ok=True)
(root / '.hydra' / 'project.json').write_text(json.dumps({'id':'lab24-scripts','name':'scripts-around-jobs'}) + '\n')
for source, target in [('orders.csv','input/orders.csv'),('workflow.yaml','workflows/main.yaml'),('check_output.py','scripts/check_output.py')]:
    shutil.copyfile(assets / source, root / target)
(root / 'workflows' / 'thread.yaml').write_text('thread:\n  - mode: sequential\n    workflows:\n      - name: main\n')
(root / 'jobs' / 'copy_orders' / 'sources.yaml').write_text("version: '1.0'\nsources:\n  orders:\n    type: csv\n    connection: {}\n    extract:\n      table: ../../input/orders.csv\n")
(root / 'jobs' / 'copy_orders' / 'destinations.yaml').write_text("version: '1.0'\ndestinations:\n  report:\n    type: csv\n    load:\n      table: ../../output/report.csv\n      mode: replace\n")
(root / 'jobs' / 'copy_orders' / 'pipeline.yaml').write_text('pipeline:\n  from: orders\n  to: report\n')
print(f'Prepared {root}')
