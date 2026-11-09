"""Create a safe starter project without overwriting learner work."""
from pathlib import Path
import json
import os
import shutil

root = Path(os.environ.get("HYDRA_LAB26_ROOT", "/root/lab/three-environments"))
if root.exists():
    raise SystemExit(f"Refusing to replace an existing learner project: {root}")
assets = Path(__file__).resolve().parent
for folder in (".hydra", "workflows", "environments", "reports"):
    (root / folder).mkdir(parents=True, exist_ok=True)
(root / ".hydra" / "project.json").write_text(
    json.dumps({"id": "lab26-three-environments", "name": "three-environments"}) + "\n",
    encoding="utf-8")
(root / "parameters.yaml").write_text("version: '1.0'\nparameters: {}\n", encoding="utf-8")
shutil.copyfile(assets / "thread.yaml", root / "workflows" / "thread.yaml")
shutil.copyfile(assets / "workflow.yaml", root / "workflows" / "show_parameters.yaml")
print(f"Ready: {root}")
