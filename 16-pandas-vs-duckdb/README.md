# LAB lab-02-09 — pandas vs DuckDB

Scenario 16 for `02-jobs-part2.md`. A deterministic generator writes five million rows. Two otherwise identical jobs aggregate the CSV with `engine: pandas` and `engine: auto`. The latter should select DuckDB at the default 2,000,000-row threshold. `--profile` gives Hydra's timings and chosen engine; `benchmark.py` separately records wall time and sampled peak RSS memory. Check compares four expected country totals and byte-identical outputs. Hydra ETL 0.19.1.
