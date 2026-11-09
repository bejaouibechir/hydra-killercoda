import json, os
from pathlib import Path

base = Path(os.environ.get('HYDRA_LAB22_ROOT', '/root/lab/master-and-subprojects'))
if base.exists():
    raise SystemExit(f'Refusing to replace {base}')

def put(name, content):
    p = base / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')

for name in ('master', 'crm', 'billing'):
    put(f'{name}/.hydra/project.json', json.dumps({'id': f'lab22-{name}', 'name': name}) + '\n')
    put(f'{name}/workflows/thread.yaml', 'thread:\n  - mode: sequential\n    workflows:\n      - name: main\n')

put('crm/parameters.yaml', 'parameters:\n  batch_date: {type: string, required: true}\n  label: {type: string, required: true}\n')
put('crm/environments/dev.yaml', 'parameters:\n  label: CRM-DEV\n')
put('billing/parameters.yaml', 'parameters:\n  batch_date: {type: string, required: true}\n  label: {type: string, required: true}\n')
put('billing/environments/prod.yaml', 'parameters:\n  label: BILLING-PROD\n')

child = '''workflow:
  name: main
  trigger:
    type: manual
  steps:
    - name: publish_batch
      type: action
      action: set_param
      params:
        name: last_batch
        value: "{{ param:label }}-{{ param:batch_date }}"
'''
put('crm/workflows/main.yaml', child)
put('billing/workflows/main.yaml', child)

put('master/parameters.yaml', 'parameters:\n  run_date: {type: string, default: 2026-11-09}\n')
put('master/workflows/main.yaml', '''workflow:
  name: main
  trigger:
    type: manual
  steps:
    - name: crm_sync
      type: project
      project: ../crm
      env: dev
      params:
        batch_date: "{{ param:run_date }}"
      outputs: [last_batch]
    - name: billing_sync
      type: project
      project: ../billing
      env: prod
      params:
        batch_date: "{{ param:run_date }}"
      outputs: [last_batch]
      depends_on: [crm_sync]
    - name: read_results
      type: action
      action: python
      depends_on: [billing_sync]
      params:
        script: |
          import json
          from pathlib import Path
          Path('published.json').write_text(json.dumps({
              'crm': '{{ project:crm_sync.param.last_batch }}',
              'billing': '{{ project:billing_sync.param.last_batch }}',
              'crm_status': '{{ project:crm_sync.status }}',
              'billing_status': '{{ project:billing_sync.status }}'
          }, indent=2) + '\\n')
''')
print(f'Prepared {base}')
