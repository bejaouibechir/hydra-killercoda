"""Exercise the real CLI and reject incomplete or incorrect learner results."""
import importlib.util
import json
from pathlib import Path
import tempfile

SCENARIO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lab08", SCENARIO / "assets" / "lab08.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def rejected(action, label):
    try:
        action()
    except (ValueError, OSError):
        print("PASS: rejected " + label)
    else:
        raise AssertionError("Accepted " + label)


def run_ok(case):
    result = lab.run(case)
    assert result.returncode == 0, result.stdout + result.stderr


def main():
    index = json.loads((SCENARIO / "index.json").read_text(encoding="utf-8"))
    for asset in index["details"]["assets"]["host01"]:
        assert (SCENARIO / "assets" / asset["file"]).is_file(), asset
    for step in index["details"]["steps"]:
        for key in ("text", "verify"):
            assert (SCENARIO / step[key]).is_file(), step
    for section in ("intro", "finish"):
        for path in index["details"][section].values():
            assert (SCENARIO / path).is_file(), path
    print("PASS: all scenario references resolve.")
    raw = (SCENARIO / "assets" / "orders-latin1.csv").read_bytes()
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        pass
    else:
        raise AssertionError("Latin-1 fixture is also valid UTF-8")
    assert raw.decode("latin-1") == (SCENARIO / "assets" / "orders-semicolon.csv").read_text(encoding="utf-8")
    print("PASS: actual Latin-1 bytes represent the same data.")
    with tempfile.TemporaryDirectory(prefix="hydra-lab08-") as directory:
        lab.ROOT = Path(directory) / "csv-shapes"
        lab.prepare()
        rejected(lab.prepare, "overwriting an existing lab")
        rejected(lambda: lab.check("comma"), "a job that has not been run")
        run_ok("comma")
        lab.check("comma")
        lab.diagnose("semicolon")
        rejected(lambda: lab.check("semicolon"), "the wrong separator")
        lab.write_yaml(lab.ROOT / "jobs/semicolon/sources.yaml", lab.source("semicolon", True))
        rejected(lambda: lab.check("semicolon"), "stale one-column output after a YAML-only fix")
        run_ok("semicolon")
        lab.check("semicolon")
        lab.diagnose("latin1")
        rejected(lambda: lab.check("latin1"), "the wrong encoding")
        lab.write_yaml(lab.ROOT / "jobs/latin1/sources.yaml", lab.source("latin1", True))
        run_ok("latin1")
        lab.check("latin1")
        lab.compare()
        evidence = lab.ROOT / "evidence/latin1.json"
        saved = evidence.read_bytes()
        evidence.unlink()
        rejected(lambda: lab.check("latin1"), "missing diagnostic evidence")
        evidence.write_bytes(saved)
        output = lab.ROOT / "outputs/comma.csv"
        output.write_text(output.read_text(encoding="utf-8").replace("Madrid", "Wrong"),
                          encoding="utf-8")
        rejected(lambda: lab.check("comma"), "an incorrect output value")
        run_ok("comma")
        lab.check("comma")
        lab.compare()
    print("PASS: all lab 08 integration checks completed.")


if __name__ == "__main__":
    main()
