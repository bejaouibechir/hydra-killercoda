"""Prepare the three jobs and inspect a dedicated MongoDB fixture."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys

import yaml

ASSETS = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("HYDRA_LAB10_ROOT", "/root/lab/mongodb-drift"))
URI = "mongodb://127.0.0.1:27020/?serverSelectionTimeoutMS=5000"
POLICIES = ("warn", "fail", "adapt")


def fixture():
    return json.loads((ASSETS / "documents.json").read_text(encoding="utf-8"))


def prepare():
    if ROOT.exists() and any(ROOT.iterdir()):
        raise ValueError(f"Refusing to overwrite a non-empty folder: {ROOT}")
    for policy in POLICIES:
        job = ROOT / "jobs" / policy
        (job / "output").mkdir(parents=True)
        source = yaml.safe_load((ASSETS / "sources.template.yaml").read_text())
        source["sources"]["orders"]["schema"]["drift_policy"] = policy
        (job / "sources.yaml").write_text(yaml.safe_dump(source, sort_keys=False))
        for filename in ("destinations.yaml", "pipeline.yaml"):
            shutil.copyfile(ASSETS / filename, job / filename)
    (ROOT / ".hydra").mkdir()
    (ROOT / ".hydra/project.json").write_text(json.dumps({
        "id": "lab10-mongodb-drift", "name": "mongodb-drift"}))
    print(f"Prepared three independent jobs in {ROOT}")


def collection(client):
    return client["hydra_lab10"]["orders"]


def verify_collection(coll):
    docs = fixture()
    actual = list(coll.find({}))
    if sorted(actual, key=lambda d: d["_id"]) != docs:
        raise ValueError("The collection differs from the 102-document fixture.")
    # MongoDB does not guarantee natural order. Check this prerequisite before
    # every run rather than assuming the inference sample has no drift.
    sample = list(coll.find({}).limit(100))
    if len(sample) != 100 or any("sales_channel" in doc for doc in sample):
        raise ValueError("Inference sample includes drift; use a fresh lab instance.")
    return actual


def seed():
    from pymongo import MongoClient
    with MongoClient(URI) as client:
        coll = collection(client)
        docs = fixture()
        existing = list(coll.find({}))
        if existing:
            if sorted(existing, key=lambda d: d["_id"]) != docs:
                raise ValueError("Refusing to replace an existing, different collection.")
        else:
            coll.insert_many(docs, ordered=True)
        verify_collection(coll)
    print("PASS: 100 baseline documents followed by two documents with sales_channel.")


def show():
    from pymongo import MongoClient
    with MongoClient(URI) as client:
        docs = verify_collection(collection(client))
    print("Collection: hydra_lab10.orders; documents:", len(docs))
    print("Inference sample: 100 documents without sales_channel.")
    for doc in (docs[0], *[d for d in docs if "sales_channel" in d]):
        print(json.dumps(doc, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "seed", "show"))
    args = parser.parse_args()
    try:
        globals()[args.action]()
    except Exception as error:
        sys.exit(f"FAIL: {error}")
