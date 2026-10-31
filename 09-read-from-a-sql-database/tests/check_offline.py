"""Check scenario references, DSL and transformation results without database servers."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import yaml

SCENARIO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lab09", SCENARIO / "assets/lab09.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def reject(action, label):
    try:
        action()
    except (ValueError, OSError):
        print("PASS: rejected " + label)
    else:
        raise AssertionError("Accepted " + label)


def main():
    index = json.loads((SCENARIO / "index.json").read_text(encoding="utf-8"))
    for asset in index["details"]["assets"]["host01"]:
        assert (SCENARIO / "assets" / asset["file"]).is_file(), asset
    for section in ("intro", "finish"):
        for path in index["details"][section].values():
            assert (SCENARIO / path).is_file(), path
    for step in index["details"]["steps"]:
        assert (SCENARIO / step["text"]).is_file()
        assert (SCENARIO / step["verify"]).is_file()
    print("PASS: all scenario references resolve.")
    raw = yaml.safe_load((lab.ASSETS / "transformations.solution.yaml").read_text(encoding="utf-8"))
    assert lab.transformed_rows(raw) == lab.expected()
    assert len(lab.expected()) == 5
    assert lab.expected()[3][2] == 0
    print("PASS: all five totals, names and IDs match, including the zero quantity.")
    wrong = copy.deepcopy(raw)
    wrong["transformations"]["steps"][1]["calculate"]["expr"] = "quantity + unit_price"
    assert lab.transformed_rows(wrong) != lab.expected()
    print("PASS: an incorrect calculation is detected.")
    missing = copy.deepcopy(raw)
    missing["transformations"]["steps"].append({"filter": {"expr": "total > 0"}})
    assert lab.transformed_rows(missing) != lab.expected()
    print("PASS: dropping the zero-quantity product is detected.")
    with tempfile.TemporaryDirectory(prefix="hydra-lab09-offline-") as directory:
        lab.ROOT = Path(directory) / "sql-products"
        lab.prepare()
        reject(lab.prepare, "overwriting an existing project")
        reject(lab.transform, "a missing transformation")
        shutil.copyfile(lab.ASSETS / "transformations.solution.yaml",
                        lab.ROOT / "jobs/products/transformations.yaml")
        lab.transform()
        target = lab.ROOT / "jobs/products/transformations.yaml"
        target.write_text(yaml.safe_dump(wrong), encoding="utf-8")
        reject(lab.transform, "the incorrect total expression")
    print("PASS: all offline lab 09 checks completed.")


if __name__ == "__main__":
    main()
