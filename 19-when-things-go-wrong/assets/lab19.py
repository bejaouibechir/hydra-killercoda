"""Run the installed Hydra engine and check only this lab's local reports."""
import json
import os
import sys
from pathlib import Path

from hydra_etl.workflow.parser import load_workflow
from hydra_etl.workflow.runner import WorkflowRunner

ROOT = Path(os.environ.get('HYDRA_LAB19_ROOT', '/root/lab/when-things-go-wrong'))
POLICIES = {'fail', 'skip', 'continue'}


def config():
    workflow = load_workflow(ROOT / 'workflow.yaml')
    steps = {step.name: step for step in workflow.steps}
    if set(steps) != {'A_start', 'B_fails', 'C_independent', 'D_after_B'}:
        raise ValueError('Keep the four lesson steps')
    if steps['B_fails'].on_failure not in POLICIES:
        raise ValueError('Choose fail, skip or continue for B_fails')
    return workflow, steps['B_fails']


def run():
    workflow, failing = config()
    is_retry = failing.retry is not None
    name = 'retry' if is_retry else failing.on_failure
    result = WorkflowRunner(workflow, base_dir=ROOT).run()
    data = {
        'policy': failing.on_failure,
        'retry': failing.retry.model_dump() if is_retry else None,
        'workflow_success': result.success,
        'duration_seconds': round(result.duration, 3),
        'error': result.error,
        'steps': [
            {'name': step.step_name, 'success': step.success, 'skipped': step.skipped,
             'error': step.error, 'logs': step.logs}
            for step in result.steps
        ],
    }
    output = ROOT / 'reports' / f'{name}.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(data, indent=2))
    print(f'Written: {output}')
    # An intentional failure is the lesson's expected result, not a helper error.


def check(stage):
    workflow, failing = config()
    expected_policy = 'continue' if stage == 'retry' else stage
    if failing.on_failure != expected_policy:
        raise ValueError(f'Set B_fails on_failure to {expected_policy}')
    if stage == 'retry':
        retry = failing.retry
        if retry is None or retry.max != 2 or retry.delay != 1 or retry.backoff != 'exponential':
            raise ValueError('Add retry: max 2, delay 1, backoff exponential to B_fails')
    elif failing.retry is not None:
        raise ValueError('Add retry only after the three policy runs')
    path = ROOT / 'reports' / f'{stage}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    if data['policy'] != expected_policy:
        raise ValueError('Report policy does not match this stage')
    if (data['retry'] is None) != (stage != 'retry'):
        raise ValueError('Report retry configuration does not match this stage')
    steps = {step['name']: step for step in data['steps']}
    if not steps.get('A_start', {}).get('success'):
        raise ValueError('A_start did not run successfully')
    if steps.get('B_fails', {}).get('success') is not False:
        raise ValueError('B_fails did not fail as intended')
    if not steps.get('C_independent', {}).get('success'):
        raise ValueError('The independent branch C should complete')
    downstream = steps.get('D_after_B')
    if stage == 'fail':
        if downstream is not None or data['workflow_success']:
            raise ValueError('With fail, execution should stop before D')
    elif stage == 'skip':
        if not downstream or not downstream['skipped'] or downstream['success']:
            raise ValueError('With skip, D should be recorded as skipped')
    else:
        if not downstream or not downstream['success'] or downstream['skipped']:
            raise ValueError('With continue, D should run')
    if stage == 'retry':
        saved = data['retry']
        if saved != {'max': 2, 'delay': 1.0, 'backoff': 'exponential'}:
            raise ValueError('Report was not generated with the required retry policy')
        logs = '\n'.join(steps['B_fails']['logs'])
        for marker in ('retry 1/2 in 1s', 'retry 2/2 in 2s', 'gave up after 2 retry(ies)'):
            if marker not in logs:
                raise ValueError(f'Missing retry evidence: {marker}')
        if data['duration_seconds'] < 2.8:
            raise ValueError('Expected roughly 1s + 2s exponential waits')
    print(f'PASS: {stage} run matches the real Hydra workflow result')


if __name__ == '__main__':
    try:
        if sys.argv[1:] == ['run']:
            run()
        elif len(sys.argv) == 3 and sys.argv[1] == 'check' and sys.argv[2] in POLICIES | {'retry'}:
            check(sys.argv[2])
        else:
            raise ValueError('Usage: lab19.py run | check {fail,skip,continue,retry}')
    except Exception as exc:
        raise SystemExit(f'FAIL: {exc}') from None
