import json, os, sys
from pathlib import Path
from hydra_etl.triggers.core import check_triggers, read_history
from hydra_etl.triggers.models import load_triggers

base = Path(os.environ.get('HYDRA_LAB23_ROOT', '/root/lab/project-triggers'))
producer = base / 'producer'
consumer = base / 'consumer'

def need(ok, message):
    if not ok: raise ValueError(message)

def check_config():
    for root in (producer, consumer):
        result = check_triggers(root, load_triggers(root))
        need(not result.errors, '; '.join(result.errors))
    names = [t.name for t in load_triggers(producer).triggers]
    need(names == ['minute_clock', 'inbox_file', 'http_hook'], 'Producer triggers changed')
    need(load_triggers(consumer).get('after_producer').project == '../producer', 'Consumer target changed')
    need((producer / '.hydra' / 'secrets').is_file(), 'Webhook token missing')
    print('PASS: cron, file, webhook and after_project triggers are valid')

def events(root, name, origin=None):
    return [e for e in read_history(root) if e.get('trigger') == name and
            e.get('status') == 'success' and (origin is None or e.get('origin') == origin)]

def check_watch():
    check_config()
    need(events(producer, 'minute_clock', 'watch'), 'Wait for the next real cron minute in hdrctl watch')
    need(events(producer, 'inbox_file', 'watch'), 'Drop a NEW CSV file while hdrctl watch is running')
    need(events(consumer, 'after_producer', 'watch'), 'Wait for the consumer project in hdrctl watch')
    print('PASS: cron, file and downstream project ran under hdrctl watch')

def switch_webhook():
    check_watch()
    before = len(events(consumer, 'after_producer'))
    (base / 'consumer-baseline.json').write_text(json.dumps({'before': before}) + '\n')
    path = producer / 'triggers.yaml'
    content = path.read_text()
    need('enabled: false' not in content, 'Already switched to webhook stage')
    content = content.replace('    type: cron\n', '    type: cron\n    enabled: false\n', 1)
    content = content.replace('    type: file\n', '    type: file\n    enabled: false\n', 1)
    path.write_text(content)
    print('Cron and file polling disabled for the HTTP stage. Start hdrctl serve after stopping watch.')

def token():
    from hydra_etl.internal.config.secrets import SecretResolver, project_secrets
    value = SecretResolver(secrets={}, fallback=project_secrets(producer))._get_secret('trigger.http_hook.token')
    print(value)

def check_webhook():
    need((base / 'consumer-baseline.json').exists(), 'Switch to the webhook stage first')
    need(events(producer, 'http_hook', 'webhook'), 'Call the localhost webhook with curl')
    print('PASS: localhost HTTP webhook started the producer project')

def check_consumer():
    check_webhook()
    before = json.loads((base / 'consumer-baseline.json').read_text())['before']
    need(len(events(consumer, 'after_producer')) > before, 'Wait for the consumer after the webhook run')
    print('PASS: producer completion started the consumer project')

if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        if args == ['check', 'config']: check_config()
        elif args == ['check', 'watch']: check_watch()
        elif args == ['switch-webhook']: switch_webhook()
        elif args == ['token']: token()
        elif args == ['check', 'webhook']: check_webhook()
        elif args == ['check', 'consumer']: check_consumer()
        else: raise ValueError('Usage: check config|watch|webhook|consumer | switch-webhook | token')
    except Exception as exc:
        raise SystemExit(f'FAIL: {exc}') from None
