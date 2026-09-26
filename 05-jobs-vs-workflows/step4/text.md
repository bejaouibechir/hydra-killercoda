# Validate and run the workflow

`hdrctl workflow validate mypipeline/workflow.yaml`{{exec}}

`hdrctl workflow run mypipeline/workflow.yaml`{{exec}}

```
✓  Step 'job_a' OK (0.0s)
✓  Step 'job_b' OK (0.0s)
✓  Step 'notify' OK (0.0s)

Workflow 'mypipeline' completed in 0.1s — 3/3 steps OK
```

Each step ran through the same `JobExecutor` a plain `hdrctl run` would use — `job_b` only started because `job_a` succeeded first (`depends_on: ["job_a"]`). Check the results:

`cat mypipeline/jobs/job_a/data/output.csv`{{exec}}

`cat mypipeline/jobs/job_b/data/output.csv`{{exec}}
