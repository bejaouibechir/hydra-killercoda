import gzip, json, os, sys
from pathlib import Path
root = Path(os.environ.get('HYDRA_LAB24_ROOT', '/root/lab/scripts-around-jobs'))
workflow = root / 'workflows' / 'main.yaml'
names = ['archive_input','copy_orders','check_output','notify_node01']
def need(ok, message):
    if not ok: raise ValueError(message)
def config():
    from hydra_etl.workflow.parser import load_workflow
    from hydra_etl.workflow.project import prepare_project
    prepare_project(root)
    steps = load_workflow(workflow).steps
    need([s.name for s in steps] == names, 'Unexpected workflow steps')
    need([s.action for s in steps] == ['bash',None,'python','ssh'], 'Expected bash, job, python and ssh')
    need([s.depends_on or [] for s in steps] == [[],['archive_input'],['copy_orders'],['check_output']], 'Dependencies changed')
    print('PASS: workflow and CSV job validate')
def run(mode):
    from hydra_etl.workflow.project import ProjectRunner, prepare_project
    config()
    enabled = 'enabled: false' not in workflow.read_text()
    need(enabled == (mode == 'remote'), 'SSH enablement does not match this stage')
    out = ProjectRunner(prepare_project(root)).run()
    data = {'success':out.success,'runs':[{'name':r.name,'status':r.status,'error':r.error,
      'steps':[{'name':s.step_name,'success':s.success,'skipped':s.skipped,'error':s.error}
               for s in (r.result.steps if r.result else [])]} for r in out.runs]}
    (root / 'reports' / f'{mode}.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
    need(out.success, f'{mode} run failed')
def check(mode):
    config()
    if mode == 'config': return
    data = json.loads((root / 'reports' / f'{mode}.json').read_text())
    need(data['success'] and len(data['runs']) == 1 and data['runs'][0]['status'] == 'success','Run failed')
    steps = data['runs'][0]['steps']
    need([s['name'] for s in steps] == names and all(s['success'] for s in steps[:3]),'Local action chain failed')
    with gzip.open(root / 'archive' / 'orders.csv.gz','rt') as handle:
        need(handle.read() == (root / 'input' / 'orders.csv').read_text(),'Archive mismatch')
    need(json.loads((root / 'reports' / 'check.json').read_text()) == {'rows':3,'amount_total':42},'Python check mismatch')
    if mode == 'local':
        need(steps[3]['skipped'],'SSH must be disabled on first run')
    else:
        need(steps[3]['success'] and not steps[3]['skipped'],'SSH action failed')
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname='node01',username='root',timeout=8)
            _, stdout, _ = client.exec_command('cat /root/lab24-remote/receipt.txt',timeout=8)
            receipt = stdout.read().decode().strip()
            need(stdout.channel.recv_exit_status() == 0 and bool(receipt),'Remote receipt missing')
            print('Remote receipt from',receipt)
        finally:
            client.close()
    print(f'PASS: {mode} run')
def enable():
    content = workflow.read_text()
    need(content.count('      enabled: false\n') == 1,'SSH step already enabled')
    workflow.write_text(content.replace('      enabled: false\n','',1))
    config()
    print('SSH step enabled')
if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        if args == ['check','config']: check('config')
        elif args in (['run','local'],['run','remote']): run(args[1])
        elif args in (['check','local'],['check','remote']): check(args[1])
        elif args == ['enable-ssh']: enable()
        else: raise ValueError('Usage: check config|local|remote, run local|remote, enable-ssh')
    except Exception as exc:
        raise SystemExit(f'FAIL: {exc}') from None
