"""Prepare the lesson and compare one completed stage with its reference."""
import argparse,csv,os,pathlib,shutil,sys,yaml
ASSETS=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB13_ROOT','/root/lab/clean-file'))
def read(path):
 with path.open(newline='',encoding='utf-8-sig') as f:
  reader=csv.DictReader(f);return reader.fieldnames,list(reader)
def prepare():
 if ROOT.exists():raise ValueError('Refusing to overwrite an existing project')
 for path in ('data','job','output','evidence'): (ROOT/path).mkdir(parents=True,exist_ok=True)
 shutil.copyfile(ASSETS/'orders.csv',ROOT/'data/orders.csv')
 for name in ('sources.yaml','destinations.yaml','pipeline.yaml'):shutil.copyfile(ASSETS/name,ROOT/'job'/name)
 print('Ready: edit job/transformations.yaml and inspect data/orders.csv')
def check(stage):
 if not ROOT.exists():raise ValueError('Project not ready')
 if stage>1 and not (ROOT/'evidence'/f'stage{stage-1}.csv').exists():raise ValueError(f'Complete and check stage {stage-1} first')
 expected=yaml.safe_load((ASSETS/f'stage{stage}.yaml').read_text())['transformations']['steps']
 actual=yaml.safe_load((ROOT/'job/transformations.yaml').read_text())['transformations']['steps']
 if actual!=expected:raise ValueError(f'Stage {stage}: transformation steps differ from the lesson')
 output=ROOT/'output/result.csv'
 if not output.exists():raise ValueError('Run Hydra before using Check')
 if read(output)!=read(ASSETS/f'expected{stage}.csv'):raise ValueError(f'Stage {stage}: CSV differs from the expected output')
 snapshot=ROOT/'evidence'/f'stage{stage}.csv'
 if snapshot.exists() and read(snapshot)!=read(output):raise ValueError('Previous evidence differs')
 shutil.copyfile(output,snapshot)
 print(f'PASS: stage {stage}; result saved in evidence/stage{stage}.csv')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','check']);p.add_argument('stage',type=int,nargs='?',choices=[1,2,3,4]);a=p.parse_args()
 try:
  if a.action=='prepare':prepare()
  elif a.stage:check(a.stage)
  else:p.error('check requires a stage number')
 except Exception as e:sys.exit(f'FAIL: {e}')
