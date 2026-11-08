# Three ways, one result

All three implementations produce BE = 20 and FR = 45. The latest paid C200 and C400 orders have empty amounts; they do not add revenue. The cancelled C300 order is excluded. The early C100 order is excluded by the latest-order rule.

The three source files are different lengths because SQL expresses operations with CTEs, pandas includes file handling and method calls, and Hydra expresses transformations as named YAML steps while its other three manifest files handle I/O. Line count alone does not measure maintainability.

The typo experiment shows the practical diagnostic difference: SQLite reports `no such column`, pandas raises `KeyError`, and Hydra identifies the step and lists available columns. Inspect `output/errors.json` to compare the exact messages.
