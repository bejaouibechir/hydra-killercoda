"""Check only the project, run captures and answer of this lesson."""
from pathlib import Path
import os
import re
import sys
import yaml

ROOT = Path(os.environ.get("HYDRA_LAB26_ROOT", "/root/lab/three-environments"))
NAMES = ("min_amount", "country", "batch_label", "sample_size")
DECL = {
    "min_amount": ("int", 50),
    "country": ("str", "FR"),
    "batch_label": ("str", "baseline"),
    "sample_size": ("int", 5),
}
ENV = {
    "dev": {"min_amount": 0, "country": "FR", "batch_label": "dev", "sample_size": 2},
    "test": {"min_amount": 25, "country": "DE", "batch_label": "test", "sample_size": 3},
    "prod": {"min_amount": 100, "country": "US", "batch_label": "prod", "sample_size": 4},
}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def data(path):
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    need(isinstance(value, dict), f"Expected YAML mapping in {path}")
    return value

def declarations():
    d = data(ROOT / "parameters.yaml").get("parameters")
    need(isinstance(d, dict) and set(d) == set(NAMES),
         "Declare exactly min_amount, country, batch_label and sample_size")
    for name, (typ, default) in DECL.items():
        spec = d[name]
        need(isinstance(spec, dict), f"Use the long form for {name}")
        need(spec.get("type") == typ and spec.get("default") == default,
             f"Set {name} to type {typ} with default {default!r}")
    print("PASS: four parameter declarations and typed defaults")
    return d

def environments():
    declarations()
    for env, expected in ENV.items():
        path = ROOT / "environments" / f"{env}.yaml"
        values = data(path).get("parameters")
        need(values == expected, f"{path.name} must define the four lesson values: {expected}")
    print("PASS: dev, test and prod each define four values")

def capture(name, expected, override=False):
    path = ROOT / "reports" / f"{name}.txt"
    need(path.is_file(), f"Run Hydra and save output in reports/{name}.txt")
    text = path.read_text(encoding="utf-8")
    need("Workflow 'show_parameters' OK" in text and "workflow(s) OK" in text,
         f"{name}: Hydra did not report a successful project run")
    marker = " ".join(f"{key}={value}" for key, value in expected.items())
    need(marker in text, f"{name}: expected resolved values: {marker}")
    if override:
        need("min_amount=0 " not in text, "The dev environment value did not get replaced")
    print(f"PASS: {name}: {marker}")

def runs():
    environments()
    for name, values in ENV.items():
        capture(name, values)

def override():
    runs()
    values = dict(ENV["dev"], min_amount=100)
    capture("dev-override", values, True)
    answer = (ROOT / "reports" / "answer.txt").read_text(encoding="utf-8").lower()
    need(re.search(r"\b100\b", answer) and "--param" in answer and "dev" in answer
         and re.search(r"\b0\b", answer) and re.search(r"\b50\b", answer),
         "Explain that --param=100 wins over dev=0 and default=50")
    print("PASS: your explanation identifies the winning run override")

if __name__ == "__main__":
    try:
        command = sys.argv[1] if len(sys.argv) == 2 else ""
        if command == "declarations":
            declarations()
        elif command == "environments":
            environments()
        elif command == "runs":
            runs()
        elif command == "override":
            override()
        else:
            raise ValueError("Usage: lab26.py declarations|environments|runs|override")
    except Exception as exc:
        raise SystemExit(f"FAIL: {exc}") from None
