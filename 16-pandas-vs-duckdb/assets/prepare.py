"""Prepare two independent jobs from the deployed manifest assets."""
import os,pathlib,shutil,sys
ASSETS=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB16_ROOT','/root/lab/engine-comparison'))
if ROOT.exists():sys.exit('Refusing to overwrite an existing project')
(ROOT/'reports').mkdir(parents=True);(ROOT/'data').mkdir()
for name in ('pandas','auto'):
 job=ROOT/'jobs'/name;job.mkdir(parents=True)
 for part in ('sources','pipeline','transformations','destinations'):
  shutil.copyfile(ASSETS/f'{name}.{part}.yaml',job/f'{part}.yaml')
 (job/'output').mkdir()
print('Ready: two jobs; generate the CSV before running them')
