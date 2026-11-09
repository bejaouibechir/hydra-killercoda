# 2. Fail at step three and roll back

Run the real workflow. `fail_third` is expected to fail, so the lesson helper writes a report and returns to the prompt normally.

```bash
cd /root/lab/rollback-in-action
/opt/hydra/bin/python /root/lab/lab20-resources/lab20.py run normal
cat reports/normal.json
/opt/hydra/bin/python /root/lab/lab20-resources/lab20.py show
```

In `rollback.steps`, `load_payments` is undone first, then `load_invoices`. Both tables again contain only `[[1, 100]]`; no undo journal remains. Press **Check**.
