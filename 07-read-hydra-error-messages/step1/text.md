# Fix an unknown action

Inspect the prepared workflow:

`cd /root/lab/error-messages && cat workflows/errors.yaml`{{exec}}

The second step contains `action: webhok`. Diagnose it:

`python3 ../lab07-resources/lab07.py diagnose unknown-action`{{exec}}

The helper runs `hdrctl run . --dry-run`, prints its output and exit code, and saves them for **Check**. It never runs the workflow.

Look for these parts of the message:

```text
Step 'notify': unknown action 'webhok'.
... did you mean 'webhook'?
Exit code: 1
```

The full message also lists valid actions. `notify` is your step name; `webhok` is the unrecognised action.

Correct the line in the Editor, or use:

`sed -i 's/action: webhok/action: webhook/' workflows/errors.yaml`{{exec}}

Validate again:

`hdrctl run . --dry-run`{{exec}}

`echo $?`{{exec}}

The exit code is now **0**. This proves that this workflow passes project validation; it does not prove that the webhook endpoint works.

Click **Check**. It checks the recorded diagnostic, the correction and a fresh dry-run.
