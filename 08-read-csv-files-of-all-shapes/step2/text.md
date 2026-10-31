# Fix the separator

This file contains the same data, separated by semicolons:

`cat data/orders-semicolon.csv && cat jobs/semicolon/sources.yaml`{{exec}}

The source still uses the default comma separator. Observe the result:

`python3 ../lab08-resources/lab08.py diagnose semicolon`{{exec}}

The helper runs the real `hdrctl run jobs/semicolon`, displays its exit code, and records the observation for **Check**.

**The command succeeds, but the data is wrong:** the whole header becomes one column named `id;customer;city`.

`python3 ../lab08-resources/lab08.py inspect semicolon`{{exec}}

In the Editor, open `jobs/semicolon/sources.yaml` and replace `connection: {}` with:

```yaml
    connection:
      delimiter: ";"
```

Or apply the correction:

`sed -i 's/connection: {}/connection: {delimiter: ";"} /' jobs/semicolon/sources.yaml`{{exec}}

Run again and inspect:

`hdrctl run jobs/semicolon`{{exec}}

`python3 ../lab08-resources/lab08.py inspect semicolon`{{exec}}

You should now see three columns and the same three rows as the first job.

A successful exit code does not prove that a CSV has the intended columns. Click **Check**.
