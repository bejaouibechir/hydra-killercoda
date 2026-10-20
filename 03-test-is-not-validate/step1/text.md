# Create a broken job

Scaffold a project from the `mysql` template:

`hdrctl init dbproject --template mysql`{{exec}}

`find dbproject | sort`{{exec}}

`hdrctl init` creates a whole **project**, not a bare job: `jobs/job1/` holds the job itself (`sources.yaml`, `destinations.yaml`, `pipeline.yaml`, `transformations.yaml`, plus a `.env.example`), `workflows/workflow1.yaml` orchestrates it, `Data/` and `output/` are the project's conventional folders, and `.hydra/project.json` marks the project root. Every job command in this lab — `validate`, `test`, `run` — targets the job folder, `dbproject/jobs/job1`.

`cat dbproject/jobs/job1/destinations.yaml`{{exec}}

The destination loads rows with `mode: upsert` (insert or update on `key: [id]`). Now break it — a one-letter typo:

`sed -i 's/mode: upsert/mode: upsret/' dbproject/jobs/job1/destinations.yaml`{{exec}}

`grep mode dbproject/jobs/job1/destinations.yaml`{{exec}}

`dbproject/jobs/job1` now asks for a load mode, `upsret`, that does not exist.

When you are done, click **Check** to continue.
