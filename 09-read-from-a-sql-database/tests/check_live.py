"""Run the full lesson against the dedicated lab 09 MySQL and PostgreSQL containers."""
import importlib.util
from pathlib import Path
import shutil
import tempfile

SCENARIO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lab09", SCENARIO / "assets/lab09.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def rejected_result():
    try:
        lab.check("result")
    except ValueError:
        print("PASS: altered destination data was rejected.")
    else:
        raise AssertionError("Altered destination data was accepted")


def main():
    with tempfile.TemporaryDirectory(prefix="hydra-lab09-live-") as directory:
        lab.ROOT = Path(directory) / "sql-products"
        lab.prepare()
        # This guard runs before any write to the database.
        lab.check("ready")
        lab.run_cli("test", "jobs/products")
        print("PASS: hdrctl test connects to both databases.")
        shutil.copyfile(lab.ASSETS / "transformations.solution.yaml",
                        lab.ROOT / "jobs/products/transformations.yaml")
        lab.check("transform")
        assert lab.destination() == [], "Dry run changed the destination"
        print("PASS: dry-run leaves PostgreSQL empty.")
        lab.run_cli("run", "jobs/products")
        lab.check("result")
        initial = lab.destination()
        lab.run_cli("run", "jobs/products")
        assert lab.destination() == initial
        print("PASS: the second execution preserves exactly five rows.")
        try:
            lab.pg_query("UPDATE public.product_totals SET total = total + 1 WHERE id = 2", write=True)
            rejected_result()
        finally:
            lab.run_cli("run", "jobs/products")
        try:
            lab.pg_query("UPDATE public.product_totals SET product_name = %s WHERE id = 2",
                         ("Incorrect name",), write=True)
            rejected_result()
        finally:
            lab.run_cli("run", "jobs/products")
        lab.check("result")
    print("PASS: all live lab 09 checks completed.")


if __name__ == "__main__":
    main()
