# Change one product and run again

The lesson helper changes only SKU-002 in the CSV and saves a backup of the original
file. It does not modify MySQL or run Hydra.

`/opt/hydra/bin/python /root/lab/lab12-resources/lab12.py update-source`{{exec}}

`cat data/products.csv`{{exec}}

SKU-002 now has name **Keyboard Pro**, price **34.95**, and quantity **7**.
The three SKUs in the source are unchanged.

`hdrctl run jobs/products`{{exec}}

`/opt/hydra/bin/python /root/lab/lab12-resources/lab12.py show`{{exec}}

`/opt/hydra/bin/python /root/lab/lab12-resources/check.py second`{{exec}}

Expected: exactly **four destination rows**, with SKU-002 updated. Every other row
must match the first-run result, including SKU-099.

A row count alone would not prove the update. The check compares every SKU, name,
price, and quantity and checks the first-run checkpoint too.

Click **Check** to complete the lab. Use a fresh session to repeat the entire
exercise; setup never resets an existing database or overwrites your job files.
