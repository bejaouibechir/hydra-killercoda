# Read from a SQL database

Move products from **MySQL** to **PostgreSQL**, with a calculation between extraction and loading.

```text
MySQL: shop.product
id, name, unit_price, quantity
              |
      total = quantity * unit_price
      name -> product_name
      keep id, product_name, total
              |
PostgreSQL: warehouse.public.product_totals
id, product_name, total
```

**Time:** about 15 minutes. **Prerequisite:** basic YAML and SQL.

The environment installs Hydra ETL 0.16.0 and starts both databases. MySQL contains five products; PostgreSQL starts empty. Setup can take a few minutes while the database images download.

**Wait for the terminal to display "Ready" before starting.** It reports progress
while Hydra installs, the project files are created and the databases initialize.
The exercise files are in `/root/lab/sql-products/jobs/products/`.

You will inspect the job, add its transformations, run it, and verify every destination row.
