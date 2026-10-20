# Done

You now know:

- `hdrctl --version`, `--help` and `--lang` — read-only, no project needed;
- `hdrctl init` scaffolds a project: a job in `jobs/job1/`, and the workflow that runs it in `workflows/workflow1.yaml`;
- `hdrctl workflow validate` and `hdrctl workflow run` take a workflow file; `hdrctl run` takes one job folder;
- `hdrctl list` lists the jobs inside the folder you point it at — `myproject/jobs`, not `myproject`.

Everything here was correct from the start. What happens when a YAML file is wrong — that's next.

**Next**

- Install it on your machine: `pip install hydra-etl`
- Docs and examples: [hydraetl.com](https://hydraetl.com/?utm_source=killercoda&utm_medium=lab&utm_campaign=meet-hdrctl)
- Source (AGPL-3.0): [github.com/bejaouibechir/Hydra](https://github.com/bejaouibechir/Hydra)

Hydra ETL is a beta, built by one maintainer. If something in this lab felt wrong or unclear, [open an issue](https://github.com/bejaouibechir/Hydra/issues) — that's the most useful thing you can do.
