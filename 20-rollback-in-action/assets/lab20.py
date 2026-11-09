"""Run this lab and check only its dedicated PostgreSQL schema and journal."""
import json
import sys

from hydra_etl.workflow.parser import load_workflow
from hydra_etl.workflow.runner import WorkflowRunner

from common import BASELINE, JOURNAL, LOADED, ROOT, baseline, connect, snapshot

WORKFLOW = ROOT / 'workflows' / 'rollback_demo.yaml'
FLAG = ROOT / 'data' / 'interrupt.flag'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def seed():
    require(not JOURNAL.exists(), 'Do not reseed while an undo journal exists')
    with connect() as db:
        with db.cursor() as cursor:
            cursor.execute('CREATE SCHEMA lab20')
            for name in ('invoices', 'payments'):
                cursor.execute(f'CREATE TABLE lab20.{name} (id INTEGER PRIMARY KEY, amount INTEGER)')
                cursor.execute(f'INSERT INTO lab20.{name} VALUES (1, 100)')
    require(snapshot() == baseline(), 'Baseline seed failed')
    print('Seeded both tables with the original row (1, 100)')


def show():
    print(json.dumps({'tables': snapshot(), 'journal_exists': JOURNAL.exists()}, indent=2))


def run(mode):
    require(mode in ('normal', 'interrupted'), 'Choose normal or interrupted')
    report = ROOT / 'reports' / f'{mode}.json'
    require(not report.exists(), f'Report already exists: {report}')
    require(not JOURNAL.exists(), 'Finish the existing undo journal before rerunning')
    require(snapshot() == baseline(), 'Both tables must be at their original values before this run')
    require(FLAG.exists() == (mode == 'interrupted'), 'Use arm before the interrupted run only')
    result = WorkflowRunner(load_workflow(WORKFLOW), base_dir=WORKFLOW.parent).run()
    data = {'workflow_success': result.success, 'error': result.error,
            'rollback': result.rollback, 'tables_after': snapshot(),
            'journal_exists': JOURNAL.exists(),
            'steps': [{'name': s.step_name, 'success': s.success,
                       'undo_of': s.undo_of, 'error': s.error} for s in result.steps]}
    report.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(data, indent=2))
    print(f'Written: {report}')
    # The third step deliberately fails; that is a successful lesson run.


def arm():
    require((ROOT / 'reports' / 'normal.json').exists(), 'Finish the normal run first')
    require(snapshot() == baseline(), 'Expected the restored baseline before arming')
    require(not JOURNAL.exists(), 'An undo journal already exists')
    require(not FLAG.exists(), 'Interrupted run already armed')
    FLAG.write_text('Simulate an outside write after the payment load\n', encoding='utf-8')
    print('Armed: step three will add payment 999, then fail')


def repair():
    require(JOURNAL.exists(), 'No stopped rollback to repair')
    rows = snapshot()
    require(rows['invoices'] == [list(r) for r in LOADED['invoices']], 'Unexpected invoices state')
    require(rows['payments'] == [list(r) for r in LOADED['payments']] + [[999, 999]],
            'Expected only the lab sentinel payment 999 to differ')
    with connect() as db:
        with db.cursor() as cursor:
            cursor.execute('DELETE FROM lab20.payments WHERE id = 999 AND amount = 999')
            require(cursor.rowcount == 1, 'Expected one sentinel row')
    FLAG.unlink(missing_ok=True)
    require(snapshot()['payments'] == [list(r) for r in LOADED['payments']],
            'Payments are not back to the post-load state')
    print('Removed only the lab sentinel row. Now run: hdrctl workflow undo rollback_demo')


def check(stage):
    require(stage in ('ready', 'normal', 'interrupted', 'recovered'), 'Unknown stage')
    wf = load_workflow(WORKFLOW)
    require(wf.rollback and [s.name for s in wf.steps] ==
            ['load_invoices', 'load_payments', 'fail_third'], 'Expected the three-step rollback workflow')
    rows = snapshot()
    if stage == 'ready':
        require(rows == baseline() and not JOURNAL.exists(), 'Expected both baseline tables and no journal')
    elif stage == 'normal':
        data = json.loads((ROOT / 'reports' / 'normal.json').read_text(encoding='utf-8'))
        require(not data['workflow_success'] and data['rollback']['status'] == 'done',
                'Expected the third step to fail and automatic rollback to complete')
        require([s['step'] for s in data['rollback']['steps']] ==
                ['load_payments', 'load_invoices'], 'Expected reverse undo order')
        require(rows == baseline() and not JOURNAL.exists(), 'The original rows were not restored')
    elif stage == 'interrupted':
        data = json.loads((ROOT / 'reports' / 'interrupted.json').read_text(encoding='utf-8'))
        require(data['rollback']['status'] == 'failed' and JOURNAL.exists(),
                'Expected a stopped rollback and its journal')
        require([e['step'] for e in json.loads(JOURNAL.read_text(encoding='utf-8'))['entries']] ==
                ['load_invoices', 'load_payments'], 'Expected both loads in the undo journal')
        require(rows['invoices'] == [list(r) for r in LOADED['invoices']] and
                rows['payments'] == [list(r) for r in LOADED['payments']] + [[999, 999]],
                'Expected the loaded rows plus the outside write')
    else:
        require((ROOT / 'reports' / 'interrupted.json').exists(), 'Run the interrupted case first')
        require(not JOURNAL.exists() and not FLAG.exists(), 'Undo is not finished')
        require(rows == baseline(), 'Both tables should be restored to the original row')
    print(f'PASS: {stage} matches the expected PostgreSQL rollback state')


if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        if args == ['seed']:
            seed()
        elif args == ['show']:
            show()
        elif args == ['arm']:
            arm()
        elif args == ['repair']:
            repair()
        elif len(args) == 2 and args[0] in ('run', 'check'):
            (run if args[0] == 'run' else check)(args[1])
        else:
            raise ValueError('Usage: lab20.py seed|show|arm|repair|run {normal,interrupted}|check {ready,normal,interrupted,recovered}')
    except Exception as exc:
        raise SystemExit(f'FAIL: {exc}') from None
