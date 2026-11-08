# Write the source and transformation files

Wait for MySQL and the seed table to be ready:

`bash /root/lab/lab12-resources/wait-ready.sh`{{exec}}

`cd /root/lab/build-job`{{exec}}

`cat data/products.csv`{{exec}}

The CSV uses commas. Its three products have columns sku, name, unit_price, and
quantity. The path in sources.yaml is relative to jobs/products.

Create your first file:

```bash
cat > jobs/products/sources.yaml <<'YAML'
version: "1.0"
sources:
  src_products:
    type: csv
    connection: {}
    extract:
      table: ../../data/products.csv
YAML
```{{exec}}

Create the transformation file:

```bash
cat > jobs/products/transformations.yaml <<'YAML'
version: "1.0"
transformations:
  steps:
    - cast:
        mapping:
          quantity: int
YAML
```{{exec}}

The cast makes quantity an integer before loading. No calculation is needed.
MySQL stores unit_price as DECIMAL(10,2).

Click **Check**. It parses both files and checks the source path and quantity cast.
