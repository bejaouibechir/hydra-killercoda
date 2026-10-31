# From MySQL products to PostgreSQL totals

You completed a job with four YAML files:

| Manifest | Role |
| --- | --- |
| `sources.yaml` | Read MySQL `shop.product` |
| `transformations.yaml` | Calculate totals, rename, select |
| `destinations.yaml` | Write PostgreSQL `public.product_totals` |
| `pipeline.yaml` | Connect the source and destination IDs |

The destination contains only `id`, `product_name` and `total`. All five products remain, including the zero-quantity product.

You checked both connectivity and actual output values. A second execution refreshed the same five rows.

The reference transformation is available at `/root/lab/sql-products/solutions/transformations.yaml`.
