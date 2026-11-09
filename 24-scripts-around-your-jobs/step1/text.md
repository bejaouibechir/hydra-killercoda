# 1. Read the action chain

~~~bash
cat /root/lab/scripts-around-jobs/workflows/main.yaml
cat /root/lab/scripts-around-jobs/jobs/copy_orders/sources.yaml
cat /root/lab/scripts-around-jobs/jobs/copy_orders/destinations.yaml
hdrctl workflow validate main --project /root/lab/scripts-around-jobs
~~~

The chain is archive_input (Bash) -> copy_orders (job) -> check_output (Python) -> notify_node01 (SSH). SSH is initially disabled. Press Check after validation succeeds.
