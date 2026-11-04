"""Exercise setup messages and failure reporting without installing software."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

SCENARIO = Path(__file__).resolve().parents[1]
BASH = shutil.which("bash")
if os.name == "nt":
    BASH = "C:/Program Files/Git/bin/bash.exe"


def shell_path(path):
    if os.name == "nt":
        return subprocess.check_output([BASH, "-c", 'cygpath -u "$1"', "bash", str(path)],
                                       text=True).strip()
    return str(path)


def run_script(text, directory):
    path = directory / "test.sh"
    path.write_text(text, encoding="utf-8", newline="\n")
    return subprocess.run([BASH, shell_path(path)], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=10)


def main():
    if not BASH:
        raise RuntimeError("Bash is required for these tests.")
    with tempfile.TemporaryDirectory(prefix="hydra-lab09-setup-") as temp:
        root = Path(temp)
        prefix = shell_path(root)
        project = root / "lab/sql-products"
        project.mkdir(parents=True)
        (root / "activate").write_text("export HYDRA_LANG=en\n", encoding="utf-8")
        foreground = (SCENARIO / "setup/foreground.sh").read_text(encoding="utf-8")
        foreground = foreground.replace("/tmp/hydra-lab09", prefix + "/hydra-lab09")
        foreground = foreground.replace("/root/lab/sql-products", prefix + "/lab/sql-products")
        foreground = foreground.replace("/opt/hydra/bin/activate", prefix + "/activate")
        foreground = foreground.replace("seq 1 600", "seq 1 2").replace("sleep 1", ":")
        ready = root / "hydra-lab09-ready"
        failed = root / "hydra-lab09-failed"
        status = root / "hydra-lab09-status"
        log = root / "hydra-lab09-setup.log"
        status.write_text("Ready: test environment\n", encoding="utf-8")
        ready.touch()
        result = run_script(foreground, root)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "Ready. You are in" in result.stdout
        print("PASS: a ready setup opens the project.")
        ready.unlink()
        failed.touch()
        log.write_text("TEST: database startup failed\n", encoding="utf-8")
        status.write_text("Setup failed during: database startup\n", encoding="utf-8")
        result = run_script(foreground, root)
        assert result.returncode == 1
        assert "TEST: database startup failed" in result.stdout
        print("PASS: setup failure displays the log and diagnostic command.")
        failed.unlink()
        status.write_text("Waiting for database tables\n", encoding="utf-8")
        result = run_script(foreground, root)
        assert result.returncode == 1
        assert "Latest status: Waiting for database tables" in result.stdout
        print("PASS: timeout reports the last known stage.")
        background = (SCENARIO / "setup/background.sh").read_text(encoding="utf-8")
        background = background.replace("/tmp/hydra-lab09", prefix + "/hydra-lab09")
        background = background.replace("/root/lab", prefix + "/lab")
        background = background.replace("seq 1 90", "seq 1 1").replace("sleep 1", ":")
        result = run_script(background, root)
        assert result.returncode != 0
        assert failed.is_file()
        assert "Missing lesson file:" in log.read_text(encoding="utf-8")
        assert "Setup failed during:" in status.read_text(encoding="utf-8")
        print("PASS: a missing asset reports its filename and stops before installation.")
    print("PASS: all setup-message checks completed.")


if __name__ == "__main__":
    main()
