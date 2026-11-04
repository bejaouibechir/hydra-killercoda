# Inspect the databases and the job

`cd /root/lab/sql-products`{{exec}}

Inspect the source with a real SQL query:

`/opt/hydra/bin/python /root/lab/lab09-resources/lab09.py show source`{{exec}}

The helper executes:

```sql
SELECT id, name, unit_price, quantity FROM product ORDER BY id;
```

| id | name | unit_price | quantity |
| --- | --- | --- | --- |
| 1 | Notebook | 12.50 | 4 |
| 2 | Keyboard | 19.95 | 3 |
| 3 | Monitor | 149.90 | 2 |
| 4 | USB cable | 4.25 | 0 |
| 5 | Mouse | 8.75 | 6 |

PostgreSQL has the destination table, but no rows:

`/opt/hydra/bin/python /root/lab/lab09-resources/lab09.py show destination`{{exec}}

Read the supplied manifests:

`cat jobs/products/sources.yaml`{{exec}}

`cat jobs/products/destinations.yaml`{{exec}}

`cat jobs/products/pipeline.yaml`{{exec}}

`extract.table: product` reads the MySQL table. `pipeline.from` and `pipeline.to` reference the connector IDs. PostgreSQL uses `load.table: product_totals` and `mode: replace`.

The names `unit_price` and `product_name` use underscores so SQL identifiers have no spaces. Passwords are resolved from the project's `.hydra/secrets`; these credentials are disposable lab examples.

Test both connections without transferring data:

`hdrctl test jobs/products`{{exec}}

Click **Check**. It verifies the MySQL seed data and the destination schema.
