"""Prepare and verify SQL, pandas, Hydra, and typo experiments."""
import argparse,csv,json,os,pathlib,shutil,sys,yaml
ASSETS=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB17_ROOT','/root/lab/three-ways'))
def read(path):
 with path.open(newline='',encoding='utf-8-sig') as f:
  reader=csv.DictReader(f);return reader.fieldnames,list(reader)
def prepare():
 if ROOT.exists():raise ValueError('Refusing to overwrite existing project')
 for name in ('data','job','output','evidence'): (ROOT/name).mkdir(parents=True,exist_ok=True)
 shutil.copyfile(ASSETS/'orders.csv',ROOT/'data/orders.csv')
 shutil.copyfile(ASSETS/'run_sql.py',ROOT/'run_sql.py')
 for name in ('sources.yaml','destinations.yaml','pipeline.yaml'):shutil.copyfile(ASSETS/name,ROOT/'job'/name)
 print('Ready: write query.sql, pandas_job.py, and job/transformations.yaml')
def check(i):
 if i>1 and not (ROOT/'evidence'/f'stage{i-1}.json').exists():raise ValueError(f'Check stage {i-1} first')
 if i<=3:
  filename=('sql.csv','pandas.csv','hydra.csv')[i-1]
  if read(ROOT/'output'/filename)!=read(ASSETS/'expected.csv'):raise ValueError(f'{filename} differs from expected country revenue')
  (ROOT/'evidence'/f'stage{i}.json').write_text(json.dumps({'file':filename,'rows':2}))
  print(f'PASS: stage {i}, BE 20 and FR 45')
 else:
  data=json.loads((ROOT/'output/errors.json').read_text())
  for name in ('sql','pandas','hydra'):
   if 'amount_typo' not in data.get(name,''):raise ValueError(f'{name} did not report the misspelled column')
  (ROOT/'evidence/stage4.json').write_text(json.dumps(data,indent=2))
  print('PASS: all three runtimes reported amount_typo')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','check']);p.add_argument('stage',type=int,nargs='?',choices=[1,2,3,4]);a=p.parse_args()
 try:
  if a.action=='prepare':prepare()
  elif a.stage:check(a.stage)
  else:p.error('check needs a stage number')
 except Exception as e:sys.exit(f'FAIL: {e}')
