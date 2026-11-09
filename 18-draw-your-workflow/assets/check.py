"""Check measured dependency order and learner's terminal ASCII arrows."""
import argparse,json,os,pathlib,re,sys
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB18_ROOT','/root/lab/draw-workflow'))
EXPECTED={('load_orders','validate_orders'),('load_orders','enrich_orders'),('load_customers','enrich_orders'),('validate_orders','publish_report'),('enrich_orders','publish_report')}
def report():
 data=json.loads((ROOT/'report.json').read_text())
 if not data['success'] or len(data['steps'])!=5:raise ValueError('Run the five-step workflow first')
 observed={x['name']:x for x in data['steps']}
 if set(observed)!={'load_orders','load_customers','validate_orders','enrich_orders','publish_report'}:raise ValueError('Unexpected steps in run report')
 for a,b in EXPECTED:
  if observed[b]['started_epoch']+0.01<observed[a]['ended_epoch']:raise ValueError(f'{b} started before {a} completed')
 roots=[observed[x] for x in ('load_orders','load_customers')]
 if max(x['started_epoch'] for x in roots)>=min(x['ended_epoch'] for x in roots):raise ValueError('Root jobs did not overlap')
 if not all(x['success'] for x in observed.values()):raise ValueError('A step failed')
 print('PASS: five timed steps, overlapping roots and dependency order')
def graph():
 report()
 raw=(ROOT/'graph.txt').read_text(encoding='utf-8')
 lines=[line.strip() for line in raw.splitlines() if line.strip() and not line.lstrip().startswith('#')]
 pattern=re.compile(r'^\[([a-z_]+)\]\s*-{2,}>\s*\[([a-z_]+)\]$')
 edges=[]
 for line in lines:
  match=pattern.fullmatch(line)
  if not match:raise ValueError(f'Not an ASCII arrow: {line!r}. Use [source] ----> [target].')
  edges.append(match.groups())
 if len(edges)!=5 or len(set(edges))!=5 or set(edges)!=EXPECTED:
  raise ValueError(f'Graph needs five direct arrows: missing={sorted(EXPECTED-set(edges))}, extra={sorted(set(edges)-EXPECTED)}')
 print('PASS: terminal ASCII graph has the five exact dependency arrows')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['report','graph']);a=p.parse_args()
 try:report() if a.action=='report' else graph()
 except Exception as e:sys.exit(f'FAIL: {e}')
