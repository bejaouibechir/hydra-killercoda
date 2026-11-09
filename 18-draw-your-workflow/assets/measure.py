"""Run the real Hydra workflow and record step start/end times."""
import datetime,json,os,pathlib,threading,time,sys
from hydra_etl.workflow.parser import load_workflow
from hydra_etl.workflow.runner import WorkflowRunner
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB18_ROOT','/root/lab/draw-workflow'))
report=ROOT/'report.json'
if report.exists():sys.exit('Refusing to overwrite report.json; use a fresh lab instance')
wf=load_workflow(ROOT/'workflow.yaml')
events=[];lock=threading.Lock()
class TimedRunner(WorkflowRunner):
 def _execute_step(self,step):
  start=time.time()
  result=super()._execute_step(step)
  end=time.time()
  with lock:events.append({'name':step.name,'started_at':datetime.datetime.fromtimestamp(start,datetime.timezone.utc).isoformat(timespec='milliseconds'),'ended_at':datetime.datetime.fromtimestamp(end,datetime.timezone.utc).isoformat(timespec='milliseconds'),'started_epoch':start,'ended_epoch':end,'duration_seconds':round(end-start,3),'success':result.success})
  return result
result=TimedRunner(wf,base_dir=ROOT).run()
data={'workflow':wf.name,'success':result.success,'duration_seconds':round(result.duration,3),'steps':sorted(events,key=lambda x:x['started_epoch'])}
report.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps(data,indent=2))
if not result.success or len(events)!=5:sys.exit('Workflow did not complete all five steps')
