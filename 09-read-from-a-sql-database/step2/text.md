# Calculate and shape the destination rows

Create the missing `jobs/products/transformations.yaml`:

```bash
cat > jobs/products/transformations.yaml <<'YAML'
version: "1.0"
transformations:
  steps:
    - cast:
        mapping:
          unit_price: float
          quantity: int
    - calculate:
        column: total
        expr: "quantity * unit_price"
    - rename:
        mapping:
          name: product_name
    - select:
        columns: [id, product_name, total]
YAML
```{{exec}}

The steps run in order:

1. **cast** prepares numeric values for the calculation.
2. **calculate** adds `total`.
3. **rename** changes `name` to `product_name`.
4. **select** keeps exactly the destination's three columns.

MySQL stores `unit_price` as `DECIMAL(10,2)`. PostgreSQL stores `total` as `NUMERIC(14,2)`, with two decimal places.

For Notebook, `4 * 12.50 = 50.00`. The zero-quantity USB cable remains in the result with `total = 0.00`.

Validate the job without moving data:

`hdrctl run jobs/products --dry-run`{{exec}}

Click **Check**. It validates the manifests and verifies the transformation results against the five sample products.
