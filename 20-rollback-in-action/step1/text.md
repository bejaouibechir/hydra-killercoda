# 1. Inspect the two target tables

Read the workflow and the job destinations. Both loads use `mode: replace`, and the third action intentionally fails. The tables start with the same original row.

```bash
cd /root/lab/rollback-in-action
cat workflows/rollback_demo.yaml
cat jobs/invoices/destinations.yaml jobs/payments/destinations.yaml
/opt/hydra/bin/python /root/lab/lab20-resources/lab20.py show
```

You should see `[[1, 100]]` in both tables and `journal_exists: false`. Press **Check**.
