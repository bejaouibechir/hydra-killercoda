# 3. Stop PostgreSQL and take the fallback

Stop only this lab's named database container and run the same thread:

~~~bash
cd /root/lab/orchestrate-project
docker stop hydra-lab21-postgres
/opt/hydra/bin/python /root/lab/lab21-resources/lab21.py run fallback
cat reports/fallback.json
cat data/output/report.json
~~~

Before each sales pass, Hydra evaluates source_available('sales_db'). With PostgreSQL stopped, it chooses load_sales_backup. Stock still runs in the parallel stage. The final report says sales_source: backup. Press Check.
