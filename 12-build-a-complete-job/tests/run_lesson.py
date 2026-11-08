"""Execute the exact lesson commands on a prepared disposable Linux instance."""
import os
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = Path("/root/lab/build-job")
HELPER = "/root/lab/lab12-resources/check.py"


def shell(command):
    result = subprocess.run(["bash", "-euo", "pipefail", "-c", command],
                            cwd=ROOT, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def must_fail(phase):
    result = subprocess.run([sys.executable, HELPER, phase], cwd=ROOT,
                            capture_output=True, text=True, timeout=90)
    if result.returncode == 0:
        raise AssertionError(f"{phase} accepted an incomplete result")
    print(f"PASS: premature {phase} check rejected")


def main():
    assert not list((ROOT / "jobs/products").glob("*.yaml")), "Job must start empty"
    must_fail("files")
    runs = 0
    pattern = re.compile(r"```bash\n(.*?)\n```\{\{exec\}\}|`([^`\n]+)`\{\{exec\}\}", re.S)
    for number in range(1, 5):
        text = (BASE / f"step{number}/text.md").read_text()
        commands = [a or b for a, b in pattern.findall(text)]
        assert commands, f"No executable commands found in step {number}"
        for command in commands:
            if command.strip() == "hdrctl run jobs/products":
                runs += 1
                must_fail("first" if runs == 1 else "second")
            shell(command)
        output = shell(f"bash {BASE}/step{number}/verify.sh")
        print(f"PASS: step {number} commands and Check script")
        print(output.strip())
    assert runs == 2
    result = subprocess.run([sys.executable, "/root/lab/lab12-resources/lab12.py",
                             "update-source"], cwd=ROOT, capture_output=True)
    assert result.returncode != 0, "Must refuse to overwrite changed source"
    print("PASS: two actual loads; changed values verified; repeated source update refused")


if __name__ == "__main__":
    main()
