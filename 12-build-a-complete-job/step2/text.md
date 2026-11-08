# Write the destination and pipeline files

MySQL already contains shop.products with a primary key on sku. A declared
`key: [sku]` does not create a database key automatically.

Create destinations.yaml:

```bash
cat > jobs/products/destinations.yaml <<'YAML'
version: "1.0"
destinations:
  db_products:
    type: mysql
    connection:
      host: 127.0.0.1
      port: 3313
      user: etl
      password: ${SECRET:MYSQL_PASSWORD}
      database: shop
    load:
      table: products
      mode: upsert
      key: [sku]
YAML
```{{exec}}

The password is read from the project's prepared .hydra/secrets file. It is a
disposable lab credential; do not put a real production password in YAML.

Create pipeline.yaml:

```bash
cat > jobs/products/pipeline.yaml <<'YAML'
version: "1.0"
pipeline:
  from: src_products
  to: db_products
YAML
```{{exec}}

You now have all four files. Hydra automatically applies transformations.yaml
between the pipeline's source and destination.

`hdrctl validate jobs/products`{{exec}}

Click **Check**. It verifies the IDs, upsert key, and all four manifests.
