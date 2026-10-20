# Run the workflow

`hdrctl workflow run chainproject/workflows/workflow1.yaml`{{exec}}

```
  ✓  Step 'job1' OK (0.2s)
  ✓  Step 'job2' OK (0.0s)
  ✓  Step 'notify' OK (0.0s)
  ✅ Workflow 'workflow1' completed in 0.2s — 3/3 steps OK
```

Same `job2` that failed in step 2 — this time it succeeds, because `job1` ran first and produced the file `job2` reads. Each step runs through the same executor as a plain `hdrctl run`; `depends_on` only sequences the calls.

Follow the data through both jobs:

`cat chainproject/jobs/job1/data/input.csv`{{exec}}

`cat chainproject/jobs/job1/data/output.csv`{{exec}}

`cat chainproject/jobs/job2/data/output.csv`{{exec}}

```
id,name,value
2,Bob,200.0
```

`job1` dropped `Charlie` (`-5`), `job2` dropped `Alice` (`100`): one row left.

When you are done, click **Check** to finish.
