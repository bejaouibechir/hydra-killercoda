import json, os
from pathlib import Path
from hydra_etl.triggers.core import create_token
from hydra_etl.triggers.models import load_triggers

base = Path(os.environ.get('HYDRA_LAB23_ROOT', '/root/lab/project-triggers'))
if base.exists(): raise SystemExit(f'Refusing to replace {base}')

def put(name, value):
    path = base / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8')

for name in ('producer', 'consumer'):
    put(f'{name}/.hydra/project.json', json.dumps({'id': f'lab23-{name}', 'name': name}) + '\n')
    put(f'{name}/workflows/thread.yaml', 'thread:\n  - mode: sequential\n    workflows:\n      - name: main\n')
put('projects.index.json', json.dumps({f'lab23-{name}': str(base / name) for name in ('producer', 'consumer')}) + '\n')

put('producer/workflows/main.yaml', '''workflow:
  name: main
  trigger:
    type: manual
  steps:
    - name: record_event
      type: action
      action: log
      params:
        message: "Producer project ran"
''')
put('consumer/workflows/main.yaml', '''workflow:
  name: main
  trigger:
    type: manual
  steps:
    - name: record_followup
      type: action
      action: log
      params:
        message: "Consumer ran after producer"
''')
put('producer/triggers.yaml', '''version: '1.0'
triggers:
  - name: minute_clock
    type: cron
    cron: '* * * * *'
    timezone: UTC
  - name: inbox_file
    type: file
    path: inbox/*.csv
    events: [added]
    every: 1s
    debounce: 0s
  - name: http_hook
    type: webhook
    token: ${SECRET:trigger.http_hook.token}
''')
put('consumer/triggers.yaml', '''version: '1.0'
triggers:
  - name: after_producer
    type: after_project
    project: ../producer
    'on': success
''')
(base / 'producer' / 'inbox').mkdir(parents=True)
value, _, _ = create_token(base / 'producer', load_triggers(base / 'producer').get('http_hook'))
print(f'Prepared {base}; local webhook token generated (not displayed)')
