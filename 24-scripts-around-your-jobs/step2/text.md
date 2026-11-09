# 2. Archive, load and check

~~~bash
/opt/hydra/bin/python /root/lab/lab24-resources/lab24.py run local
cat /root/lab/scripts-around-jobs/reports/check.json
~~~

Bash writes archive/orders.csv.gz while leaving the original input for the CSV job. Python checks the destination: 3 rows, amount total 42. Press Check after the local run succeeds.
