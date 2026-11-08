# pandas vs DuckDB

Generate one 5-million-row CSV, then run the same aggregation twice: first with `engine: pandas`, then with `engine: auto`. The auto threshold is 2 million estimated CSV rows, so the second run should select DuckDB if its extra is installed.

Hydra's `--profile` reports time and selected engine. The lesson's benchmark helper separately samples peak process RSS memory; Hydra's profile does not report memory. Both outputs are in `reports/`.

Wait for **Ready**. Generating the file and running the pandas job may take several minutes. These are the only terminal commands needed for the lesson.
