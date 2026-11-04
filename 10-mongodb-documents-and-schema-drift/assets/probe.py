"""Exercise real Hydra boundaries using an in-memory MongoDB cursor.
No server is contacted. This is a compatibility check, not an ETL replacement.
"""
import copy
import importlib.metadata
import io
import json
import logging
from pathlib import Path
import sys
from unittest.mock import patch

import yaml
from hydra_etl.internal.parser.source import SourceParser
from hydra_etl.internal.runner.executor import JobExecutor
from hydra_etl.plugins.connectors.mongodb.connector import MongoDBConnector

ASSETS = Path(__file__).resolve().parent


class Cursor:
    def __init__(self, docs):
        self.docs = copy.deepcopy(docs)

    def limit(self, count):
        self.docs = self.docs[:count]
        return self

    def __iter__(self):
        return iter(self.docs)


class Collection:
    def __init__(self, docs):
        self.docs = docs

    def find(self, query):
        if query:
            raise ValueError("This probe supports only the lab's empty filter.")
        return Cursor(self.docs)


def inspect():
    source = yaml.safe_load((ASSETS / "sources.template.yaml").read_text())
    docs = json.loads((ASSETS / "documents.json").read_text())
    definition = SourceParser().parse(source).sources["orders"]
    executor = JobExecutor(ASSETS, root_dir=ASSETS)
    with patch("hydra_etl.internal.runner.executor.build_connector",
               side_effect=lambda **kwargs: kwargs["config"]):
        forwarded = executor._build_connector("orders", definition, is_source=True)
    report = {
        "hydra_version": importlib.metadata.version("hydra-etl"),
        "schema_forwarded": forwarded.get("schema") == definition.schema.model_dump(),
        "connector": {},
    }
    # Supply schema directly to isolate extraction from the executor defect.
    for policy in ("warn", "fail", "adapt"):
        config = copy.deepcopy(source["sources"]["orders"])
        config["schema"]["drift_policy"] = policy
        connector = MongoDBConnector("orders", config)
        connector.client = object()
        connector.collection = Collection(docs)
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.setLevel(logging.WARNING)
        logger = logging.getLogger("hydra_etl")
        logger.addHandler(handler)
        rows, error = [], None
        try:
            for batch in connector.extract_batches():
                rows.extend(batch)
        except Exception as exc:
            error = str(exc)
        finally:
            logger.removeHandler(handler)
        values = {r.get("_id"): r.get("sales_channel") for r in rows}
        report["connector"][policy] = {
            "rows": len(rows),
            "error": error,
            "drift_warning": "sales_channel" in stream.getvalue(),
            "new_values_preserved": (
                values.get("ORD-101") == "web" and values.get("ORD-102") == "store"),
        }
    return report


def supported(report):
    warn, fail, adapt = (report["connector"][p] for p in ("warn", "fail", "adapt"))
    return all((
        report["schema_forwarded"],
        warn["rows"] == 102 and warn["error"] is None and warn["drift_warning"],
        fail["error"] is not None and "sales_channel" in fail["error"],
        adapt["rows"] == 102 and adapt["error"] is None and adapt["new_values_preserved"],
    ))


if __name__ == "__main__":
    report = inspect()
    print(json.dumps(report, indent=2))
    if not supported(report):
        sys.exit("BLOCKED: this Hydra build does not satisfy the lab's drift contract.")
    print("PASS: boundary probe passed; live MongoDB acceptance is still required.")
