# 3. Stop a rollback safely

This time the third action simulates a separate writer inserting payment `(999, 999)` after the two jobs load. Hydra notices that `payments` changed and stops its automatic undo rather than deleting another writer's data.

```bash
cd /root/lab/rollback-in-action
/opt/hydra/bin/python /root/lab/lab20-resources/lab20.py arm
/opt/hydra/bin/python /root/lab/lab20-resources/lab20.py run interrupted
/opt/hydra/bin/python /root/lab/lab20-resources/lab20.py show
cat .hydra/undo/rollback_demo.json
```

The report should show `rollback.status: failed` and a journal containing both loads. Both tables still have the loaded rows; `payments` also has row 999. Press **Check**.
