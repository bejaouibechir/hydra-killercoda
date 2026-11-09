# 2. Skip: keep the other branch

Change only B's policy from `fail` to `skip`, then run again:

```bash
cd /root/lab/when-things-go-wrong
sed -i 's/on_failure: fail/on_failure: skip/' workflow.yaml
/opt/hydra/bin/python /root/lab/lab19-resources/lab19.py run
cat reports/skip.json
```

The independent C succeeds. D depends on B, so Hydra records D as skipped (`skipped: true`). The workflow still reports errors because B failed. Press **Check**.
