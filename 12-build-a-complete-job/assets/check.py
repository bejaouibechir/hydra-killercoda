"""Verify learner-written manifests and exact database results."""
import argparse
import json
import os
import subprocess
import sys

import yaml
from hydra_etl.internal.parser.source import SourceParser
from hydra_etl.internal.parser.transform import TransformParser
from common import ASSETS, ROOT, JOB, check_rows, csv_rows, expected


def read(name):
    path = JOB / name
    if not path.is_file():
        raise ValueError(f"Create jobs/products/{name} first.")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def source_and_transform():
    source = read("sources.yaml")
    SourceParser().parse(source)
    definition = source["sources"]["src_products"]
    if definition["type"] != "csv":
        raise ValueError("src_products must be a CSV source.")
    target = (JOB / definition["extract"]["table"]).resolve()
    if target != (ROOT / "data/products.csv").resolve():
        raise ValueError("Read ../../data/products.csv relative to the job.")
    transform = read("transformations.yaml")
    TransformParser().parse(transform)
    steps = transform["transformations"]["steps"]
    if not any(step.get("cast", {}).get("mapping", {}).get("quantity") == "int"
               for step in steps):
        raise ValueError("Cast quantity to int in transformations.yaml.")
    print("PASS: sources.yaml and transformations.yaml.")


def manifests():
    source_and_transform()
    destination = read("destinations.yaml")["destinations"]["db_products"]
    load = destination["load"]
    if destination["type"] != "mysql" or load.get("mode") != "upsert":
        raise ValueError("Use a MySQL destination with mode: upsert.")
    if load.get("key") != ["sku"] or load.get("table") != "products":
        raise ValueError("Use table: products and key: [sku].")
    pipeline = read("pipeline.yaml")["pipeline"]
    if pipeline.get("from") != "src_products" or pipeline.get("to") != "db_products":
        raise ValueError("Connect src_products to db_products.")
    env = dict(os.environ, HYDRA_LANG="en", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    for name in ("MYSQL_PASSWORD", "HYDRA_SECRETS_FILE", "HYDRA_ENV"):
        env.pop(name, None)
    result = subprocess.run(
        [sys.executable, "-B", "-m", "hydra_etl.cli.hdrctl", "validate", str(JOB)],
        cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=90)
    if result.returncode:
        raise ValueError(result.stdout + result.stderr)
    print("PASS: all four files; actual Hydra CLI validation passed.")


def first():
    manifests()
    actual = check_rows("first")
    if csv_rows(ROOT / "data/products.csv") != csv_rows(ASSETS / "products.csv"):
        raise ValueError("The first run must use the initial CSV.")
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    snapshot = [[sku, name, str(price), quantity] for sku, name, price, quantity in actual]
    path = evidence / "first-run.json"
    if path.exists() and json.loads(path.read_text()) != snapshot:
        raise ValueError("A different first-run checkpoint already exists.")
    path.write_text(json.dumps(snapshot, indent=2))
    print("PASS: first-run checkpoint saved for comparison.")


def second():
    manifests()
    checkpoint = ROOT / "evidence/first-run.json"
    if not checkpoint.exists():
        raise ValueError("First-run verification is missing.")
    before = [[sku, name, str(price), quantity]
              for sku, name, price, quantity in expected("first")]
    if json.loads(checkpoint.read_text()) != before:
        raise ValueError("First-run checkpoint does not match the initial result.")
    if csv_rows(ROOT / "data/products.csv") != csv_rows(ASSETS / "products.updated.csv"):
        raise ValueError("Use the updated CSV for the second run.")
    check_rows("second")
    print("PASS: SKU-002 changed, all other rows stayed intact, and no SKU was duplicated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("files", "manifests", "first", "second"))
    args = parser.parse_args()
    try:
        {"files": source_and_transform, "manifests": manifests,
         "first": first, "second": second}[args.phase]()
    except Exception as error:
        sys.exit(f"FAIL: {error}")
