# Scaffold a project

`hdrctl init` creates a Hydra ETL project from a template: one job, the workflow that runs it, and the folders around them.

`hdrctl init myproject`{{exec}}

Look at what it created:

`find myproject | sort`{{exec}}

- `jobs/job1/` — the job itself: `sources.yaml`, `destinations.yaml`, `pipeline.yaml`, `transformations.yaml`, and sample data in `data/input.csv`;
- `workflows/workflow1.yaml` — the workflow that runs `job1`;
- `Data/` and `output/` — the project's conventional folders, empty for now;
- `.hydra/project.json` — marks the project root.

Read how the job is wired:

`cat myproject/jobs/job1/pipeline.yaml`{{exec}}

```yaml
pipeline:
  from: src_csv
  to: dest_csv
```

`src_csv` and `dest_csv` are the two IDs declared in `sources.yaml` and `destinations.yaml`:

`cat myproject/jobs/job1/sources.yaml myproject/jobs/job1/destinations.yaml`{{exec}}

That's the whole wiring of a job: one source ID, one destination ID, and `pipeline.yaml` connecting them.

When you are done, click **Check** to continue.
