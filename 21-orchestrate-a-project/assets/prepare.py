import json,os,shutil
from pathlib import Path
assets=Path(__file__).resolve().parent
root=Path(os.environ.get('HYDRA_LAB21_ROOT','/root/lab/orchestrate-project'))
if root.exists():raise SystemExit(f'Refusing to replace {root}')
for folder in ('.hydra','workflows','scripts','data/output','reports'):(root/folder).mkdir(parents=True,exist_ok=True)
(root/'.hydra'/'project.json').write_text(json.dumps({'id':'lab21-orchestrate','name':'orchestrate-project'}))
shutil.copyfile(assets/'build_reports.py',root/'scripts'/'build_reports.py')
for name in ('refs.csv','stock.csv','sales-backup.csv'):shutil.copyfile(assets/name,root/'data'/name)
(root/'workflows'/'thread.yaml').write_text("version: '1.0'\nthread: []\n")
jobs={'referentials':('csv','../../data/refs.csv','../../data/output/refs.csv'),
      'sales':('postgresql','lab21.sales','../../data/output/sales.csv'),
      'stock':('csv','../../data/stock.csv','../../data/output/stock.csv'),
      'sales_backup':('csv','../../data/sales-backup.csv','../../data/output/sales.csv')}
for name,(stype,source_path,dest_path) in jobs.items():
 job=root/'jobs'/name;job.mkdir(parents=True)
 source_id='sales_db' if stype=='postgresql' else 'input'
 if stype=='postgresql':
  source="""version: '1.0'
sources:
  sales_db:
    type: postgresql
    connection:
      host: 127.0.0.1
      port: 5445
      user: lab21
      password: lab21-only
      database: hydra_lab21
      schema: lab21
    extract:
      table: sales
"""
 else:
  source=f"""version: '1.0'
sources:
  input:
    type: csv
    connection: {{}}
    extract:
      table: {source_path}
"""
 (job/'sources.yaml').write_text(source)
 (job/'destinations.yaml').write_text(f"""version: '1.0'
destinations:
  output:
    type: csv
    load:
      table: {dest_path}
      mode: replace
""")
 (job/'pipeline.yaml').write_text(f'pipeline:\n  from: {source_id}\n  to: output\n')
for wf,job in {'load_referentials':'referentials','load_sales':'sales','load_stock':'stock','load_sales_backup':'sales_backup'}.items():
 step='copy_stock' if wf=='load_stock' else 'copy_data'
 extra="""    - name: wait_briefly
      type: action
      action: delay
      params: {seconds: 0.6}
      depends_on: [copy_stock]
""" if wf=='load_stock' else ''
 (root/'workflows'/f'{wf}.yaml').write_text(f"""version: '1.0'
workflow:
  name: {wf}
  trigger:
    type: manual
  steps:
    - name: {step}
      type: job
      job: ../jobs/{job}
"""+extra)
(root/'workflows'/'build_reports.yaml').write_text("""version: '1.0'
workflow:
  name: build_reports
  trigger:
    type: manual
  steps:
    - name: summarize
      type: action
      action: python
      params:
        file_path: scripts/build_reports.py
""")
print(f'Prepared {root}')
