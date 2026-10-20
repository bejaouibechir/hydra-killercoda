# Create an invalid job

Scaffold a project from the `csv` template — the only built-in template that ships with real sample data, so it can actually run once it is fixed:

`hdrctl init brokenproject --template csv`{{exec}}

`find brokenproject | sort`{{exec}}

`hdrctl init` creates a whole **project**, not a bare job: `jobs/job1/` holds the job itself (`sources.yaml`, `destinations.yaml`, `pipeline.yaml`, `transformations.yaml`, `data/input.csv`), `workflows/workflow1.yaml` orchestrates it, `Data/` and `output/` are the project's conventional folders, and `.hydra/project.json` marks the project root. Every job command in this lab — `validate`, `test`, `run` — targets the job folder, `brokenproject/jobs/job1`.

`cat brokenproject/jobs/job1/pipeline.yaml`{{exec}}

`pipeline.yaml` says which source feeds which destination:

```yaml
pipeline:
  from: src_csv
  to: dest_csv
```

Now break it — a realistic typo, the kind you get from renaming a source and missing one reference:

`sed -i 's/from: src_csv/from: src_csv_typo/' brokenproject/jobs/job1/pipeline.yaml`{{exec}}

`cat brokenproject/jobs/job1/pipeline.yaml`{{exec}}

`brokenproject/jobs/job1` now points `pipeline.from` at a source, `src_csv_typo`, that does not exist in `sources.yaml`.

When you are done, click **Check** to continue.
