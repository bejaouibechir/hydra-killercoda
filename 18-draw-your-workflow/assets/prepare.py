"""Prepare a clean learner workspace without replacing existing files."""
import os,pathlib,shutil,sys
ROOT=pathlib.Path(os.environ.get('HYDRA_LAB18_ROOT','/root/lab/draw-workflow'))
if ROOT.exists():sys.exit('Refusing to overwrite existing project')
ROOT.mkdir(parents=True)
shutil.copyfile(pathlib.Path(__file__).with_name('workflow.yaml'),ROOT/'workflow.yaml')
(ROOT/'graph.txt').write_text('# ASCII workflow graph: draw one arrow for each direct dependency.\n# Example: [source_step] ----> [target_step]\n',encoding='utf-8')
print('Ready: inspect workflow.yaml, then run the workflow')