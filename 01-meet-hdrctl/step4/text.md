# Let hdrctl list check your reading

List the jobs `hdrctl` sees in the project's `jobs/` folder:

`hdrctl list myproject/jobs`{{exec}}

`job1` shows up as `✅ OK`, tagged `[transforms]` because it has a `transformations.yaml`. `hdrctl list` looks one level deep in the folder you give it for job folders — a `sources.yaml`, `destinations.yaml` and `pipeline.yaml` sitting together. That's why you point it at `jobs/`, not at the project root:

`hdrctl list myproject`{{exec}}

`No jobs found`: `myproject/` holds `jobs/` and `workflows/`, not a job.

That's the rule for the whole CLI: `hdrctl validate`, `test`, `run` and `list` take a **job folder** (or, for `list`, a folder of jobs); `hdrctl workflow validate` and `run` take a **workflow file**. Run the job alone, without its workflow:

`hdrctl run myproject/jobs/job1`{{exec}}

```
  ✅ Pipeline completed successfully
  Rows read   : 3
  Rows written: 2
```

Same job, same result. The workflow adds nothing to what a job does — it decides *when* jobs run and *in which order*.

Click **Check** to finish.
