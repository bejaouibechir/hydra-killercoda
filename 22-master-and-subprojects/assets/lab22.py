import json, os, sys
from pathlib import Path

base = Path(os.environ.get('HYDRA_LAB22_ROOT', '/root/lab/master-and-subprojects'))
master = base / 'master'
crm = base / 'crm'
expected = {'crm': 'CRM-DEV-2026-11-09', 'billing': 'BILLING-PROD-2026-11-09',
            'crm_status': 'success', 'billing_status': 'success'}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def check_config():
    from hydra_etl.workflow.subprojects import check_project_calls
    result = check_project_calls(master)
    need(not result.errors, '; '.join(result.errors))
    for project, env in ((crm, 'dev'), (base / 'billing', 'prod')):
        need((project / 'environments' / f'{env}.yaml').exists(), f'Missing {env} environment')
    print('PASS: master validates and both child environments exist')

def run():
    from hydra_etl.workflow.project import ProjectRunner, prepare_project
    check_config()
    out = ProjectRunner(prepare_project(master)).run()
    report = {'success': out.success, 'runs': [
        {'name': r.name, 'status': r.status, 'error': r.error,
         'steps': [{'name': s.step_name, 'success': s.success, 'error': s.error}
                   for s in (r.result.steps if r.result else [])]}
        for r in out.runs]}
    (master / 'reports').mkdir(exist_ok=True)
    (master / 'reports' / 'run.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    need(out.success, 'Master workflow failed; inspect reports/run.json')
    print('Published parameters:', (master / 'published.json').read_text())

def check_run():
    report = json.loads((master / 'reports' / 'run.json').read_text())
    need(report['success'], 'Master workflow did not succeed')
    need(len(report['runs']) == 1 and report['runs'][0]['status'] == 'success', 'Unexpected master result')
    need([s['name'] for s in report['runs'][0]['steps']] ==
         ['crm_sync', 'billing_sync', 'read_results'], 'Unexpected step order')
    need(all(s['success'] for s in report['runs'][0]['steps']), 'One master step failed')
    data = json.loads((master / 'published.json').read_text())
    need(data == expected, f'Published parameters mismatch: {data}')
    print('PASS: dev and prod outputs were published and read by the master')

def introduce_cycle():
    path = crm / 'workflows' / 'main.yaml'
    content = path.read_text()
    need('call_master' not in content, 'Cycle already introduced')
    path.write_text(content + '''
    - name: call_master
      type: project
      project: ../master
      depends_on: [publish_batch]
''')
    print('Added crm -> master; now validate the master workflow.')

def check_cycle():
    log = (master / 'reports' / 'cycle-validation.txt').read_text()
    need('cycle:' in log.lower(), f'Expected a cycle diagnostic; got: {log}')
    need('master' in log and 'crm' in log, 'Cycle should involve master and crm')
    from hydra_etl.workflow.subprojects import check_project_calls
    need(bool(check_project_calls(master).errors), 'Validation currently accepts the cycle')
    print('PASS: hdrctl workflow validate refused master -> crm -> master')

if __name__ == '__main__':
    try:
        command = sys.argv[1:]
        if command == ['check', 'config']: check_config()
        elif command == ['run']: run()
        elif command == ['check', 'run']: check_run()
        elif command == ['introduce-cycle']: introduce_cycle()
        elif command == ['check', 'cycle']: check_cycle()
        else: raise ValueError('Usage: check config | run | check run | introduce-cycle | check cycle')
    except Exception as exc:
        raise SystemExit(f'FAIL: {exc}') from None
