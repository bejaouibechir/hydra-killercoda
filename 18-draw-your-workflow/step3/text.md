# Draw the graph in the terminal

Create `graph.txt` as an ASCII edge diagram: one visible arrow for each direct `depends_on` relationship in `workflow.yaml`. Use the format `[source] ----> [target]`. There are five direct arrows among the five named steps.

The starter file shows the syntax. Enter your arrows with a terminal here-document (replace the example placeholders with real step names):

```bash
cd /root/lab/draw-workflow
cat graph.txt
cat > graph.txt <<'EOF'
# My workflow graph
[source_step] ----> [target_step]
# Add the other four direct arrows here.
EOF
cat graph.txt
```

After writing the five real arrows, press **Check**. It compares your ASCII graph with the workflow dependencies and the measured run order. The terminal displays the graph directly; no Markdown renderer or editor is needed.