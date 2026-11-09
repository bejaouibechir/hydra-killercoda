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
ART = """+---------------+
| load_orders   |----+------------------------+
+---------------+    |                        |
                     v                        v
              +-----------------+      +---------------+
              | validate_orders |      | enrich_orders |
              +-----------------+      +---------------+
                      |                       ^    |
                      |                       |    |
+----------------+    |                       |    |
| load_customers |----|-----------------------+    |
+----------------+    |                            |
                      +------------+---------------+
                                   |
                                   v
                          +------------------+
                          | publish_report   |
                          +------------------+"""

def graph():
 report()
 raw=(ROOT/'graph.txt').read_text(encoding='utf-8')
 normalize=lambda value: '\n'.join(line.rstrip() for line in value.strip().splitlines())
 if normalize(raw)!=normalize(ART):
  raise ValueError('graph.txt differs from the five-step ASCII diagram shown in the lesson')
 print('PASS: the boxed ASCII graph matches all five workflow dependencies')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['report','graph']);a=p.parse_args()
 try:report() if a.action=='report' else graph()
 except Exception as e:sys.exit(f'FAIL: {e}')
