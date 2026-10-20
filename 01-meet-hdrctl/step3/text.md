# Validate and run the project's workflow

The bottom of `hdrctl init`'s output suggested two commands: validate the workflow, then run it. Read the workflow first — open `myproject/workflows/workflow1.yaml` in the **Editor** tab, or:

`cat myproject/workflows/workflow1.yaml`{{exec}}

One step, `job1`, pointing at `../jobs/job1` — paths in a workflow are relative to the workflow file.

Check it without running anything:

`hdrctl workflow validate myproject/workflows/workflow1.yaml`{{exec}}

```
  ✅ Workflow valid — no errors detected.
```

Then run it:

`hdrctl workflow run myproject/workflows/workflow1.yaml`{{exec}}

```
  ✓  Step 'job1' OK (0.2s)
  ✅ Workflow 'workflow1' completed in 0.2s — 1/1 steps OK
```

The job wrote its result next to its input:

`cat myproject/jobs/job1/data/output.csv`{{exec}}

```
id,name,value
1,Alice,100.0
2,Bob,200.0
```

Three rows in, two out: the last step of `myproject/jobs/job1/transformations.yaml`, `filter: value > 0`, drops `Charlie` (value `-5`).

When you are done, click **Check** to continue.
