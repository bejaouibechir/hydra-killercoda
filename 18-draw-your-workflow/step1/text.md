# Inspect the dependency lists

Read `workflow.yaml`. Two steps have no dependencies. One step depends on `load_orders`, another depends on both loading steps, and the final step depends on both middle steps.

```bash
cd /root/lab/draw-workflow
cat workflow.yaml
```

Identify the roots and the final step before pressing **Check**.
