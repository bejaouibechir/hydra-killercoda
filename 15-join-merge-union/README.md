# LAB lab-02-08 — Join, merge, union

Killercoda scenario 15 for `02-jobs-part2.md`. Three independent jobs use the same `orders.csv` as the main flow. `join` reads `customers.csv`; `merge` reads full order updates; `union` reads additional full orders. This distinction is essential to the semantics of the three operations.

Each Check compares YAML and CSV with the expected result and saves an evidence snapshot. Hydra ETL 0.19.1; no database or Docker service.
