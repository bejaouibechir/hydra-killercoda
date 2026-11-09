# Draw the workflow in the terminal

The five steps form this graph. The two loads start in parallel. `load_orders` leads to `validate_orders` and `enrich_orders`; `load_customers` also leads to `enrich_orders`. Both middle steps lead to `publish_report`. Where the horizontal `load_customers` line crosses the vertical `validate_orders` line (`-|`), there is no connection.

```text
+---------------+
| load_orders   |----+------------------------+
+---------------+    |                        |
                     v                        v
              +-----------------+      +---------------+
              | validate_orders |      | enrich_orders |
              +-----------------+      +---------------+
                      |                       ^    |
                      |                       |    |
+----------------+    |                       |    |
| load_customers |----|-----------------------+    |
+----------------+    |                            |
                      +------------+---------------+
                                   |
                                   v
                          +------------------+
                          | publish_report   |
                          +------------------+
```

Reproduce and display it directly in the Killercoda terminal:

```bash
cd /root/lab/draw-workflow
cat > graph.txt <<'EOF'
+---------------+
| load_orders   |----+------------------------+
+---------------+    |                        |
                     v                        v
              +-----------------+      +---------------+
              | validate_orders |      | enrich_orders |
              +-----------------+      +---------------+
                      |                       ^    |
                      |                       |    |
+----------------+    |                       |    |
| load_customers |----|-----------------------+    |
+----------------+    |                            |
                      +------------+---------------+
                                   |
                                   v
                          +------------------+
                          | publish_report   |
                          +------------------+
EOF
cat graph.txt
```

Compare the graph with `workflow.yaml` and the start/end times in `report.json`, then press **Check**.