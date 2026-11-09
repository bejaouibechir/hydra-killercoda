# 1. Build the thread

The starter thread is empty. Write the three stages, the fallback on load_sales, and the loop. The backup workflow is a separate file and is not listed among the four thread workflows.

~~~bash
cd /root/lab/orchestrate-project
cat > workflows/thread.yaml <<'EOF'
version: '1.0'
thread:
  - mode: sequential
    workflows:
      - name: load_referentials
  - mode: parallel
    delay_after: 200ms
    workflows:
      - name: load_sales
        fallback:
          use: [load_sales_backup]
          when: "not source_available('sales_db')"
          on_probe_error: keep
      - name: load_stock
  - mode: sequential
    workflows:
      - name: build_reports
loops:
  - from: load_stock
    to: load_sales
    times: 2
    delay: 100ms
EOF
cat workflows/thread.yaml
~~~

The loop covers the whole parallel stage, even though its endpoints name the two workflows. Press Check.
