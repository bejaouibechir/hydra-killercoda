"""Test startup diagnostics without installing software or starting services."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

BASE = Path(__file__).resolve().parents[1]
BASH = "C:/Program Files/Git/bin/bash.exe" if os.name == "nt" else shutil.which("bash")


def shell_path(path):
    if os.name == "nt":
        return subprocess.check_output([BASH, "-c", 'cygpath -u "$1"', "bash", str(path)],
                                       text=True).strip()
    return str(path)


def run(content, root):
    script = root / "test.sh"
    script.write_text(content, encoding="utf-8", newline="\n")
    return subprocess.run([BASH, shell_path(script)], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=15)


def main():
    with tempfile.TemporaryDirectory(prefix="hydra-lab11-setup-") as temporary:
        root = Path(temporary)
        prefix = shell_path(root)
        (root / "lab/load-modes").mkdir(parents=True)
        foreground = (BASE / "assets/wait-ready.sh").read_text()
        foreground = foreground.replace("/tmp/hydra-lab11", prefix + "/hydra-lab11")
        foreground = foreground.replace("/root/lab/load-modes", prefix + "/lab/load-modes")
        foreground = foreground.replace("seq 1 900", "seq 1 2").replace("sleep 1", ":")
        ready = root / "hydra-lab11-ready"
        failed = root / "hydra-lab11-failed"
        status = root / "hydra-lab11-status"
        log = root / "hydra-lab11-setup.log"
        ready.touch()
        status.write_text("Ready: test\n")
        result = run(foreground, root)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "Ready. Start step 1." in result.stdout
        print("PASS: readiness marker opens the lesson")
        ready.unlink()
        failed.touch()
        log.write_text("TEST: PostgreSQL failed\n")
        result = run(foreground, root)
        assert result.returncode == 1
        assert "Setup failed." in result.stdout
        print("PASS: failure stops the learner without diagnostic commands")
        failed.unlink()
        result = run(foreground, root)
        assert result.returncode == 1
        assert "Setup is still incomplete" in result.stdout
        print("PASS: timeout never reports success")
        background = (BASE / "setup/background.sh").read_text()
        background = background.replace("/tmp/hydra-lab11", prefix + "/hydra-lab11")
        background = background.replace("/root/lab", prefix + "/lab")
        background = background.replace("seq 1 90", "seq 1 1").replace("sleep 1", ":")
        # Execute only the resource check: no installer is present in this test.
        background = background.split('progress "Installing Hydra')[0]
        result = run(background, root)
        assert result.returncode != 0
        assert failed.is_file()
        assert "Missing asset:" in log.read_text()
        assert "Setup failed during:" in status.read_text()
        print("PASS: missing resources stop setup with a diagnostic")


if __name__ == "__main__":
    main()
