import json,os,sys,time
from pathlib import Path
import psycopg2
from hydra_etl.workflow.project import ProjectRunner,prepare_project
from hydra_etl.workflow.thread import load_thread
root=Path(os.environ.get('HYDRA_LAB21_ROOT','/root/lab/orchestrate-project'))
thread=root/'workflows'/'thread.yaml'
normal=[('load_referentials',1),('load_sales',1),('load_stock',1),('load_sales',2),('load_stock',2),('build_reports',1)]
backup=[('load_referentials',1),('load_sales_backup',1),('load_stock',1),('load_sales_backup',2),('load_stock',2),('build_reports',1)]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def seed():
 with psycopg2.connect(host='127.0.0.1',port=5445,user='lab21',password='lab21-only',dbname='hydra_lab21',connect_timeout=3) as db:
  with db.cursor() as cur:
   cur.execute('CREATE SCHEMA lab21')
   cur.execute('CREATE TABLE lab21.sales (id INTEGER PRIMARY KEY, region TEXT, total INTEGER)')
   cur.execute("INSERT INTO lab21.sales VALUES (1,'EAST',400),(2,'WEST',600)")
 print('Seeded lab21.sales')
def check_thread():
 th=load_thread(thread)
 need(len(th.thread)==3 and [s.mode for s in th.thread]==['sequential','parallel','sequential'],'Build three stages with a parallel middle stage')
 need(th.workflow_names()==['load_referentials','load_sales','load_stock','build_reports'],'Use four primary workflows in order')
 need(len(th.loops)==1 and th.loops[0].from_=='load_stock' and th.loops[0].to=='load_sales' and th.loops[0].times==2,'Loop the parallel stage twice')
 fb=th.thread[1].workflows[0].fallback
 need(fb is not None and fb.use==['load_sales_backup'] and fb.when=="not source_available('sales_db')",'Add the source-availability fallback')
 need(th.thread[1].delay_seconds==0.2 and th.loops[0].delay_seconds==0.1,'Keep the short lesson delays')
 print('PASS: three stages, four workflows, parallel loop and fallback')
def run(mode):
 need(mode in ('normal','fallback','restored'),'Unknown run')
 check_thread()
 output=root/'reports'/f'{mode}.json'
 need(not output.exists(),f'Report already exists: {output}')
 events=[]
 def event(kind,data):
  now=time.time()
  if kind=='fallback':events.append({'kind':kind,'time':now,'name':data['name'],'use':data['use'],'trigger':data['trigger'],'iteration':data['iteration']})
  elif kind=='loop':events.append({'kind':kind,'time':now,'iteration':data['iteration']})
  elif kind=='start':events.append({'kind':kind,'time':now,'name':data['name'],'iteration':data['iteration']})
 result=ProjectRunner(prepare_project(root)).run(event)
 report_path=root/'data'/'output'/'report.json'
 data={'success':result.success,'duration_seconds':round(result.duration,3),
       'runs':[{'name':r.name,'status':r.status,'stage':r.stage,'iteration':r.iteration,'replaces':r.replaces,'error':r.error} for r in result.runs],
       'events':events,'summary':json.loads(report_path.read_text()) if report_path.exists() else None}
 output.write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps(data,indent=2));print(f'Written: {output}')
def check(mode):
 check_thread()
 if mode=='thread':return
 data=json.loads((root/'reports'/f'{mode}.json').read_text())
 expected=backup if mode=='fallback' else normal
 need(data['success'],'Project failed')
 need([(r['name'],r['iteration']) for r in data['runs']]==expected,'Wrong workflow order or loop count')
 need(all(r['status']=='success' for r in data['runs']),'A workflow failed')
 fb=[e for e in data['events'] if e['kind']=='fallback']
 if mode=='fallback':
  need(len(fb)==2 and all(e['name']=='load_sales' and e['use']=='load_sales_backup' and e['trigger']=='when' for e in fb),'Expected two database-triggered fallbacks')
  need(data['summary']['sales_source']=='backup','Expected backup sales')
 else:
  need(not fb and data['summary']['sales_source']=='postgres','Expected PostgreSQL sales')
 need(data['summary']['sales_rows']==2 and data['summary']['stock_rows']==2 and data['summary']['reference_rows']==2,'Unexpected row counts')
 need(len([e for e in data['events'] if e['kind']=='loop'])==1,'Expected one loop transition')
 print(f'PASS: {mode} run')
if __name__=='__main__':
 try:
  args=sys.argv[1:]
  if args==['seed']:seed()
  elif len(args)==2 and args[0] in ('run','check'):(run if args[0]=='run' else check)(args[1])
  else:raise ValueError('Usage: seed | run normal|fallback|restored | check thread|normal|fallback|restored')
 except Exception as exc:raise SystemExit(f'FAIL: {exc}') from None
