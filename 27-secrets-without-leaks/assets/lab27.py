"""Run the lesson job with one secret source and check only local evidence."""
from pathlib import Path
import csv
import json
import os
import subprocess
import sys

ROOT = Path(os.environ.get("HYDRA_LAB27_ROOT", "/root/lab/secrets-without-leaks"))
PRIVATE = Path(os.environ.get("HYDRA_LAB27_PRIVATE", "/root/lab27-private/secrets"))
HDRCTL = os.environ.get("HYDRA_LAB27_HDRCTL", "/opt/hydra/bin/hdrctl")
LOCAL = ROOT / ".hydra" / "secrets"
EXPECTED = [{"id": "1", "name": "Mug"}, {"id": "2", "name": "Lamp"}]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def secret_from(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    values = [line.split("=", 1)[1] for line in lines if line.startswith("db.password=")]
    need(len(values) == 1 and bool(values[0]), f"Missing db.password in {path}")
    return values[0]

def git_status():
    result = subprocess.run(["git", "-C", str(ROOT), "status", "--short",
                             "--untracked-files=all"], capture_output=True, text=True)
    need(result.returncode == 0, "The lesson project is not a Git repository")
    status = result.stdout
    need(".hydra/secrets" not in status and "lab27-private" not in status,
         "A secret file appeared in git status")
    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--",
                              ".hydra/secrets"], capture_output=True, text=True)
    need(not tracked.stdout.strip(), "The project secret file is tracked")
    return status

def check_source(mode):
    need(mode in ("local", "env", "external"), "Choose local, env or external")
    need((ROOT / "jobs" / "read_products" / "sources.yaml").is_file(), "Missing database job")
    need("SECRET:" in (ROOT / "jobs" / "read_products" / "sources.yaml").read_text(encoding="utf-8"),
         "The source must use a secret placeholder")
    need("DB_PASSWORD" not in os.environ or mode == "env",
         "Unset DB_PASSWORD outside the environment-variable stage")
    need("HYDRA_SECRETS_FILE" not in os.environ,
         "Unset HYDRA_SECRETS_FILE; this lesson uses the CLI option for the external file")
    if mode == "local":
        need(LOCAL.is_file(), "The project secret file is missing")
        need("DB_PASSWORD" not in os.environ, "Unset DB_PASSWORD to test the project secret")
        password = secret_from(LOCAL)
    elif mode == "env":
        need(not LOCAL.exists(), "Remove .hydra/secrets to test only DB_PASSWORD")
        password = os.environ.get("DB_PASSWORD", "")
        need(bool(password), "Export DB_PASSWORD from the project secret before removing that file")
    else:
        need(not LOCAL.exists(), "Remove .hydra/secrets before the external-file stage")
        need("DB_PASSWORD" not in os.environ, "Unset DB_PASSWORD so it cannot win over --secrets-file")
        need(PRIVATE.is_file() and not PRIVATE.resolve().is_relative_to(ROOT.resolve()),
             "Create the private secrets file outside the project")
        password = secret_from(PRIVATE)
    need(bool(password), "Missing secret value")
    return password

def run(mode):
    password = check_source(mode)
    ignored = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-q",
                              ".hydra/secrets"], capture_output=True)
    need(ignored.returncode == 0, ".gitignore must protect .hydra/secrets")
    cmd = [HDRCTL, "run", str(ROOT / "jobs" / "read_products")]
    if mode == "external":
        cmd += ["--secrets-file", str(PRIVATE)]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    output = result.stdout + result.stderr
    need(password not in output, "The secret appeared in Hydra's console output")
    need(result.returncode == 0, f"Hydra job failed: {output[-600:]}")
    with (ROOT / "outputs" / "products.csv").open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    need(rows == EXPECTED, f"Unexpected database rows: {rows}")
    status = git_status()
    report = {"mode": mode, "success": True, "rows": rows,
              "git_status": status.splitlines(), "secret_masked": True,
              "used_secrets_file": mode == "external"}
    (ROOT / "reports" / f"{mode}.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Hydra read {len(rows)} database rows with the {mode} secret source.")
    print("Git status contains no secret file.")
    print("Hydra output contains no secret value.")
    print(f"Report: reports/{mode}.json")

def check(mode):
    need(mode in ("local", "env", "external"), "Choose local, env or external")
    if mode == "local":
        need(LOCAL.is_file(), "The project secret file is missing")
    else:
        need(not LOCAL.exists(), "Remove .hydra/secrets after the first stage")
    if mode == "external":
        need(PRIVATE.is_file() and not PRIVATE.resolve().is_relative_to(ROOT.resolve()),
             "The external secrets file is missing")
    reports = ["local", "env", "external"][:["local", "env", "external"].index(mode)+1]
    for name in reports:
        path = ROOT / "reports" / f"{name}.json"
        need(path.is_file(), f"Run the {name} stage first")
        data = json.loads(path.read_text(encoding="utf-8"))
        need(data["mode"] == name and data["success"] and data["rows"] == EXPECTED,
             f"Invalid {name} report")
        need(data["secret_masked"] and not any(
            ".hydra/secrets" in line or "lab27-private" in line
            for line in data["git_status"]), f"{name} exposed a secret")
    git_status()
    print(f"PASS: {mode} secret source worked and Git never listed the secret.")

if __name__ == "__main__":
    try:
        if len(sys.argv) != 3 or sys.argv[1] not in ("run", "check"):
            raise ValueError("Usage: lab27.py run|check local|env|external")
        if sys.argv[1] == "run":
            run(sys.argv[2])
        else:
            check(sys.argv[2])
    except Exception as exc:
        raise SystemExit(f"FAIL: {exc}") from None
