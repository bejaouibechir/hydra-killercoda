# Done

You now know:

- a project holds **jobs** (`jobs/<name>/`) and **workflows** (`workflows/<name>.yaml`);
- `hdrctl list`, `validate`, `test` and `run` act on jobs — `list` on a folder of jobs, the others on one job folder;
- `hdrctl workflow validate` and `hdrctl workflow run` act on a workflow file;
- a job can be valid and still fail if it runs too early — `validate` checks the YAML, not the order;
- `depends_on` is what puts jobs in order; each step still runs through the same executor as `hdrctl run`.

Next in the series: one job, two environments — parameters and secrets.

**Next**

- Install it on your machine: `pip install hydra-etl`
- Docs and examples: [hydraetl.com](https://hydraetl.com/?utm_source=killercoda&utm_medium=lab&utm_campaign=jobs-vs-workflows)
- Source (AGPL-3.0): [github.com/bejaouibechir/Hydra](https://github.com/bejaouibechir/Hydra)

Hydra ETL is a beta, built by one maintainer. If something in this lab felt wrong or unclear, [open an issue](https://github.com/bejaouibechir/Hydra/issues) — that's the most useful thing you can do.
