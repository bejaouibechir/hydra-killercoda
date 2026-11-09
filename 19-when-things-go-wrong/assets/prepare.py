"""Copy the lesson workflow into a fresh learner directory."""
import os
from pathlib import Path
from shutil import copyfile

root = Path(os.environ.get('HYDRA_LAB19_ROOT', '/root/lab/when-things-go-wrong'))
if root.exists():
    raise SystemExit('Refusing to replace an existing learner directory')
root.mkdir(parents=True)
(root / 'reports').mkdir()
copyfile(Path(__file__).with_name('workflow.yaml'), root / 'workflow.yaml')
print('Ready: inspect workflow.yaml')
