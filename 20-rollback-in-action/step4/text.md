# 4. Resume with `hdrctl workflow undo`

Remove **only** the sentinel payment that the lesson added. The helper checks the exact table state before deleting that one row. Then let Hydra resume the saved undo stack:

```bash
cd /root/lab/rollback-in-action
/opt/hydra/bin/python /root/lab/lab20-resources/lab20.py repair
/opt/hydra/bin/hdrctl workflow undo rollback_demo
/opt/hydra/bin/python /root/lab/lab20-resources/lab20.py show
```

Hydra undoes `load_payments`, then `load_invoices`. Both tables return to `[[1, 100]]`, and `.hydra/undo/rollback_demo.json` disappears. Press **Check**.
