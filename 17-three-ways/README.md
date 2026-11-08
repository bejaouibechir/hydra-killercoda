# LAB lab-02-12 — Three ways

Scenario 17 for `02-jobs-part2.md`. SQL uses in-memory SQLite, Python uses pandas, and Hydra ETL 0.19.1 uses its CSV connector and seven transformation steps. All three read one seven-row CSV with spaces, mixed case and empty amounts, then produce the same two revenue rows. A fourth stage compares line counts and the error from `amount_typo` in temporary copies.

The SQL, pandas, and Hydra transformation files start absent; Hydra's source, destination, and pipeline manifests are prepared by setup. Reference solutions are deployed as lesson assets. Each Check compares the expected result or error evidence. No database or Docker service is needed.
