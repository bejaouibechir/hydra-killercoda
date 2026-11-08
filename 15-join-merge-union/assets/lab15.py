"""Prepare and check three independent combining jobs."""
import argparse,csv,os,pathlib,shutil,sys,yaml
ASSETS=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB15_ROOT','/root/lab/combine-data'))
def read(path):
 with path.open(newline='',encoding='utf-8-sig') as f:
  reader=csv.DictReader(f);return reader.fieldnames,list(reader)
def prepare():
 if ROOT.exists():raise ValueError('Refusing to overwrite an existing project')
 (ROOT/'data').mkdir(parents=True);(ROOT/'evidence').mkdir()
 for name in ('orders.csv','customers.csv','order_updates.csv','more_orders.csv'):shutil.copyfile(ASSETS/name,ROOT/'data'/name)
 for i in (1,2,3):
  job=ROOT/'jobs'/f'stage{i}';job.mkdir(parents=True);(ROOT/'output'/f'stage{i}').mkdir(parents=True)
  shutil.copyfile(ASSETS/f'sources{i}.yaml',job/'sources.yaml')
  shutil.copyfile(ASSETS/'pipeline.yaml',job/'pipeline.yaml')
  dest=(ASSETS/'destinations.yaml').read_text().replace('output/result.csv',f'output/stage{i}/result.csv')
  (job/'destinations.yaml').write_text(dest)
 print('Ready: three independent jobs and four sample CSV files')
def check(i):
 if i>1 and not (ROOT/'evidence'/f'stage{i-1}.csv').exists():raise ValueError(f'Check stage {i-1} first')
 job=ROOT/'jobs'/f'stage{i}'
 expected=yaml.safe_load((ASSETS/f'stage{i}.yaml').read_text())['transformations']['steps']
 actual=yaml.safe_load((job/'transformations.yaml').read_text())['transformations']['steps']
 if actual!=expected:raise ValueError(f'Stage {i}: transformation steps differ from the lesson')
 result=ROOT/'output'/f'stage{i}'/'result.csv'
 if not result.exists():raise ValueError('Run the stage before using Check')
 if read(result)!=read(ASSETS/f'expected{i}.csv'):raise ValueError(f'Stage {i}: output differs from expected')
 snapshot=ROOT/'evidence'/f'stage{i}.csv'
 if snapshot.exists() and read(snapshot)!=read(result):raise ValueError('Existing evidence differs')
 shutil.copyfile(result,snapshot)
 print(f'PASS: stage {i}; result saved in evidence/stage{i}.csv')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','check']);p.add_argument('stage',type=int,nargs='?',choices=[1,2,3]);a=p.parse_args()
 try:
  if a.action=='prepare':prepare()
  elif a.stage:check(a.stage)
  else:p.error('check needs a stage number')
 except Exception as e:sys.exit(f'FAIL: {e}')
