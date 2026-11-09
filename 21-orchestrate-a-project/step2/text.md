# 2. Run the parallel stage and loop

PostgreSQL is running. Execute the real Hydra project and inspect the report:

~~~bash
cd /root/lab/orchestrate-project
/opt/hydra/bin/python /root/lab/lab21-resources/lab21.py run normal
cat reports/normal.json
cat data/output/report.json
~~~

The report has one referentials run, two live sales runs, two stock runs, one reports run, and one loop transition. Sales comes from PostgreSQL. Press Check.
