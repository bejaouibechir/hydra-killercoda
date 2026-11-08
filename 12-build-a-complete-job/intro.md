# Build a complete job

Write the four YAML files of a CSV-to-MySQL job from scratch:

1. sources.yaml — read the product CSV.
2. transformations.yaml — cast quantity to an integer.
3. destinations.yaml — upsert into MySQL using sku.
4. pipeline.yaml — connect the source to the destination.

Then run the job twice. Between runs, change the name, price, and quantity of one
product while keeping its SKU. Verify that MySQL updates the row instead of
inserting a duplicate.

Setup installs Hydra and MySQL and prepares the data and local demo secrets.
**The job directory starts empty.** Wait for **Ready**; files appearing in the
project do not mean the database has finished initializing.

All commands below belong to the lesson. No extra platform diagnostics are needed.
Estimated time: 20 minutes.
