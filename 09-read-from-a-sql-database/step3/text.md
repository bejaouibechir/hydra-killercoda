# Transfer and verify

Execute the job:

`hdrctl run jobs/products`{{exec}}

Inspect PostgreSQL:

`/opt/hydra/bin/python /root/lab/lab09-resources/lab09.py show destination`{{exec}}

The helper executes:

```sql
SELECT id, product_name, total
FROM public.product_totals
ORDER BY id;
```

| id | product_name | total |
| --- | --- | --- |
| 1 | Notebook | 50.00 |
| 2 | Keyboard | 59.85 |
| 3 | Monitor | 299.80 |
| 4 | USB cable | 0.00 |
| 5 | Mouse | 52.50 |

Verify all IDs, names and totals:

`/opt/hydra/bin/python /root/lab/lab09-resources/lab09.py check result`{{exec}}

Run the job a second time:

`hdrctl run jobs/products`{{exec}}

`/opt/hydra/bin/python /root/lab/lab09-resources/lab09.py check result`{{exec}}

There must still be exactly **five rows**. `mode: replace` refreshes the destination instead of appending copies.

Click **Check**. It reads the actual PostgreSQL table and compares every row with the expected result; a success message or a row count alone is not enough.
