# Jobs vs workflows

A Hydra ETL project holds two kinds of things, and `hdrctl` has a command family for each:

- **jobs**, in `jobs/<name>/` — one source, one destination, one pipeline. `hdrctl validate`, `test`, `run` and `list` act on them;
- **workflows**, in `workflows/<name>.yaml` — a DAG that decides which jobs run, in which order. `hdrctl workflow validate` and `hdrctl workflow run` act on them.

In this lab you will add a second job that reads the first job's output, see it fail when it runs on its own too early, then let the workflow run both in the right order.

Hydra ETL installs in the background while you read this.
