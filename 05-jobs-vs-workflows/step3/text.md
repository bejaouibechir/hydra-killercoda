# Wire both jobs in the workflow

The project's workflow still runs `job1` only:

`cat chainproject/workflows/workflow1.yaml`{{exec}}

Replace it with a three-step DAG — `job1`, then `job2` (`depends_on: [job1]`), then a `log` action:

```
cat > chainproject/workflows/workflow1.yaml <<'YAML'
version: "1.0"
workflow:
  name: workflow1
  description: "job1, then job2, then a log message"
  trigger:
    type: manual
  steps:
    - name: job1
      type: job
      job: ../jobs/job1
      depends_on: []
      on_failure: fail
    - name: job2
      type: job
      job: ../jobs/job2
      depends_on: [job1]
      on_failure: fail
    - name: notify
      type: action
      action: log
      params:
        message: "workflow1 completed: job1 then job2"
      depends_on: [job2]
      on_failure: skip
YAML
```{{exec}}

Job paths are relative to the workflow file, hence `../jobs/...`. Check the manifest:

`hdrctl workflow validate chainproject/workflows/workflow1.yaml`{{exec}}

```
  ✅ Workflow valid — no errors detected.
```

When you are done, click **Check** to continue.
