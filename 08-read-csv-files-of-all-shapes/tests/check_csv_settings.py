"""Report whether the installed Hydra honors the lesson's CSV settings."""
import importlib.util
import importlib.metadata
import json
from pathlib import Path
import tempfile
import sys

SCENARIO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lab08", SCENARIO / "assets/lab08.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

results = {"hydra_version": importlib.metadata.version("hydra-etl"), "cases": []}
with tempfile.TemporaryDirectory(prefix="hydra-lab08-probe-") as directory:
    lab.ROOT = Path(directory) / "csv-shapes"
    lab.prepare()
    for case, fixed in (("comma", True), ("semicolon", False),
                        ("semicolon", True), ("latin1", False), ("latin1", True)):
        lab.write_yaml(lab.ROOT / "jobs" / case / "sources.yaml", lab.source(case, fixed))
        output = lab.ROOT / "outputs" / (case + ".csv")
        if output.exists():
            output.unlink()
        run = lab.run(case)
        rows = lab.read_csv(output) if output.exists() else None
        correct = run.returncode == 0 and rows == lab.ROWS
        entry = {"case": case, "corrected_settings": fixed,
                 "exit_code": run.returncode, "correct_output": correct,
                 "columns": len(rows[0]) if rows else None,
                 "utf8_decode_error": "decode" in (run.stdout + run.stderr).lower()
                                    and "utf-8" in (run.stdout + run.stderr).lower()}
        results["cases"].append(entry)
print(json.dumps(results, indent=2))
failed = any(not case["correct_output"] for case in results["cases"] if case["corrected_settings"])
if failed:
    print("BLOCKED: the installed Hydra does not produce the expected CSV data after correction.")
sys.exit(1 if failed else 0)
