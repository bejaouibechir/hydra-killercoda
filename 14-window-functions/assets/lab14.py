"""Prepare four independent window jobs and check observed CSV output."""
import argparse,csv,os,pathlib,shutil,sys,yaml
ASSETS=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB14_ROOT','/root/lab/window-functions'))
def read(path):
 with path.open(newline='',encoding='utf-8-sig') as f:
  reader=csv.DictReader(f);return reader.fieldnames,list(reader)
def prepare():
 if ROOT.exists():raise ValueError('Refusing to overwrite an existing project')
 (ROOT/'data').mkdir(parents=True);(ROOT/'evidence').mkdir()
 shutil.copyfile(ASSETS/'sales.csv',ROOT/'data/sales.csv')
 for i in range(1,5):
  job=ROOT/'jobs'/f'stage{i}'
  job.mkdir(parents=True);(ROOT/'output'/f'stage{i}').mkdir(parents=True)
  for name in ('sources.yaml','destinations.yaml','pipeline.yaml'):shutil.copyfile(ASSETS/name,job/name)
  dest=job/'destinations.yaml'
  dest.write_text(dest.read_text().replace('output/result.csv',f'output/stage{i}/result.csv'))
 print('Ready: four independent jobs and one shared sales.csv')
def check(i):
 if i>1 and not (ROOT/'evidence'/f'stage{i-1}.csv').exists():raise ValueError(f'Check stage {i-1} first')
 job=ROOT/'jobs'/f'stage{i}'
 expected_steps=yaml.safe_load((ASSETS/f'stage{i}.yaml').read_text())['transformations']['steps']
 actual_steps=yaml.safe_load((job/'transformations.yaml').read_text())['transformations']['steps']
 if actual_steps!=expected_steps:raise ValueError(f'Stage {i}: transformation steps differ from the lesson')
 result=ROOT/'output'/f'stage{i}'/'result.csv'
 if not result.exists():raise ValueError('Run the stage before using Check')
 if read(result)!=read(ASSETS/f'expected{i}.csv'):raise ValueError(f'Stage {i}: result differs from the reference')
 snapshot=ROOT/'evidence'/f'stage{i}.csv'
 if snapshot.exists() and read(snapshot)!=read(result):raise ValueError('Existing evidence differs')
 shutil.copyfile(result,snapshot)
 print(f'PASS: stage {i}; result saved in evidence/stage{i}.csv')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','check']);p.add_argument('stage',type=int,nargs='?',choices=[1,2,3,4]);a=p.parse_args()
 try:
  if a.action=='prepare':prepare()
  elif a.stage:check(a.stage)
  else:p.error('check needs a stage number')
 except Exception as e:sys.exit(f'FAIL: {e}')
