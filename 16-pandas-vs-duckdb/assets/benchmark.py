"""Run the real Hydra CLI with --profile and sample process peak RSS."""
import argparse,csv,json,os,pathlib,re,subprocess,sys,time
import psutil
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB16_ROOT','/root/lab/engine-comparison'))
def run(name):
 if name not in ('pandas','auto'):raise ValueError('Unknown engine variant')
 job=ROOT/'jobs'/name
 report=ROOT/'reports'/f'{name}.json';log_path=ROOT/'reports'/f'{name}.log'
 if report.exists() or log_path.exists():raise ValueError('This variant was already measured; use a fresh lab instance')
 env=dict(os.environ,PYTHONUTF8='1',HYDRA_LANG='en',NO_COLOR='1')
 env.pop('HYDRA_ENGINE',None);env.pop('HYDRA_LARGE_VOLUME_ROWS',None)
 start=time.perf_counter()
 with log_path.open('w',encoding='utf-8') as log:
  p=subprocess.Popen([sys.executable,'-B','-m','hydra_etl.cli.hdrctl','run',str(job),'--profile'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
  proc=psutil.Process(p.pid);peak=0
  while p.poll() is None:
   try:peak=max(peak,proc.memory_info().rss+sum(c.memory_info().rss for c in proc.children(recursive=True)))
   except (psutil.NoSuchProcess,psutil.AccessDenied):pass
   time.sleep(.1)
  code=p.wait()
 elapsed=time.perf_counter()-start
 text=log_path.read_text(encoding='utf-8',errors='replace')
 match=re.search(r'(?:moteur|engine)\s+(pandas|duckdb)',text,re.I)
 selected=match.group(1).lower() if match else None
 result={'variant':name,'selected_engine':selected,'exit_code':code,'wall_seconds':round(elapsed,3),'peak_rss_mib':round(peak/1048576,1),'rows':int(os.environ.get('HYDRA_LAB16_ROWS','5000000'))}
 report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,indent=2));print(f'Hydra profile: {log_path}')
 if code:raise ValueError('Hydra run failed; see profile log')
def check(name):
 report=ROOT/'reports'/f'{name}.json';data=json.loads(report.read_text())
 if data['exit_code'] or data['selected_engine']!=name.replace('auto','duckdb'):raise ValueError('Unexpected engine or failed run')
 output=ROOT/'jobs'/name/'output/result.csv'
 with output.open(newline='',encoding='utf-8-sig') as f:
  reader=csv.DictReader(f);rows=list(reader)
 n=data['rows'];expected={'FR':n//4*10,'BE':n//4*20,'DE':n//4*30,'ES':n//4*40}
 if len(rows)!=4 or {r['country']:float(r['total_amount']) for r in rows}!={k:float(v) for k,v in expected.items()}:raise ValueError('Aggregation differs from expected totals')
 if name=='auto':
  other=ROOT/'jobs/pandas/output/result.csv'
  if not other.exists() or other.read_bytes()!=output.read_bytes():raise ValueError('Outputs differ between engines')
 print(f'PASS: {name} engine, four totals, {n:,} input rows')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['run','check']);p.add_argument('variant',choices=['pandas','auto']);a=p.parse_args()
 try:run(a.variant) if a.action=='run' else check(a.variant)
 except Exception as e:sys.exit(f'FAIL: {e}')
