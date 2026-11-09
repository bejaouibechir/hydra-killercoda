# 1. Fail: stop the workflow

The starter workflow has `on_failure: fail` on `B_fails`. Inspect it and run the real Hydra engine:

```bash
cd /root/lab/when-things-go-wrong
cat workflow.yaml
/opt/hydra/bin/python /root/lab/lab19-resources/lab19.py run
```

The Python action deliberately raises an error. Inspect `reports/fail.json`: A succeeded, B failed, C succeeded in the same parallel group, and D was never started. The helper's command returns normally because this failure is expected in the exercise.

```bash
cat reports/fail.json
```

Press **Check** after the report exists. It reads only this lab's files.
