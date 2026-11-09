"""Create this disposable project and a random local database credential."""
from pathlib import Path
import json
import os
import secrets
import shutil

root = Path(os.environ.get("HYDRA_LAB27_ROOT", "/root/lab/secrets-without-leaks"))
if root.exists():
    raise SystemExit(f"Refusing to replace an existing learner project: {root}")
assets = Path(__file__).resolve().parent
for folder in (".hydra", "jobs/read_products", "outputs", "reports"):
    (root / folder).mkdir(parents=True, exist_ok=True)
(root / ".hydra" / "project.json").write_text(
    json.dumps({"id": "lab27-secrets", "name": "secrets-without-leaks"}) + "\n",
    encoding="utf-8")
(root / ".gitignore").write_text(
    ".hydra/secrets\n.hydra/secrets.*\n!.hydra/secrets.yaml\n"
    "outputs/*.csv\nreports/\n", encoding="utf-8")
password = secrets.token_hex(20)
secret_path = root / ".hydra" / "secrets"
secret_path.write_text("db.password=" + password + "\n", encoding="utf-8")
secret_path.chmod(0o600)
for name in ("sources.yaml", "destinations.yaml", "pipeline.yaml"):
    shutil.copyfile(assets / name, root / "jobs" / "read_products" / name)
print(f"Ready: {root}; private credential created without displaying its value")
