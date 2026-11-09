from pathlib import Path
import json
import os
import shutil

root = Path(os.environ.get("HYDRA_LAB25_ROOT", "/root/lab/reversible-actions"))
if root.exists():
    raise SystemExit(f"Refusing to replace an existing learner project: {root}")
for folder in (".hydra", "workflows", "scripts", "reports", "work"):
    (root / folder).mkdir(parents=True, exist_ok=True)
(root / ".hydra" / "project.json").write_text(
    json.dumps({"id": "lab25-reversible", "name": "reversible-actions"}) + "\n",
    encoding="utf-8")
(root / "workflows" / "reversible.yaml").write_text(
    "version: '1.0'\nworkflow:\n  name: reversible\n  rollback: true\n"
    "  trigger:\n    type: manual\n  steps:\n",
    encoding="utf-8")
for name in ("create_folder.py", "remove_folder.py", "fail.py"):
    shutil.copyfile(Path(__file__).with_name(name), root / "scripts" / name)
print(f"Ready: {root}")
