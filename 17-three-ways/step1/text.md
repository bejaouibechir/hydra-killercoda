# SQL: clean, filter, latest, aggregate

Build `query.sql` using CTEs: clean country and status, filter paid orders, rank each customer's orders by descending ID, then sum only `rn = 1`. SQLite runs in memory; the CSV remains unchanged. Review the reference and type or copy it into `query.sql`.

```bash
cd /root/lab/three-ways
cat /root/lab/lab17-resources/query.solution.sql
cp /root/lab/lab17-resources/query.solution.sql query.sql
/opt/hydra/bin/python run_sql.py
cat output/sql.csv
```

The latest paid C200 order has an empty amount; SQL ignores it in `SUM`. Press **Check** after confirming BE = 20 and FR = 45.
