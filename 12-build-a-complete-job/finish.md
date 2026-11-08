# Complete job verified

You wrote sources.yaml, transformations.yaml, destinations.yaml, and pipeline.yaml.

The first execution inserted new products and updated an existing one. The second
execution changed SKU-002 while keeping exactly four destination rows.
A product absent from the CSV remained in MySQL.

The primary key on sku and mode: upsert together provide the matching behavior.
