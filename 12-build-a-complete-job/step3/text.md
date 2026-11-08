# Run the complete job once

Inspect the two original rows:

`/opt/hydra/bin/python /root/lab/lab12-resources/lab12.py show`{{exec}}

The database initially has SKU-001 with old values, plus SKU-099, which is absent
from the CSV.

`hdrctl run jobs/products`{{exec}}

`/opt/hydra/bin/python /root/lab/lab12-resources/lab12.py show`{{exec}}

Expected results:

| SKU | Name | Unit price | Quantity |
| --- | --- | ---: | ---: |
| SKU-001 | Notebook | 12.50 | 4 |
| SKU-002 | Keyboard | 29.95 | 3 |
| SKU-003 | Mouse | 8.75 | 6 |
| SKU-099 | Legacy product | 5.00 | 1 |

The job updated SKU-001, inserted SKU-002 and SKU-003, and preserved SKU-099.

Record and verify the result before changing the source:

`/opt/hydra/bin/python /root/lab/lab12-resources/check.py first`{{exec}}

Click **Check**. The next step compares against this verified first-run checkpoint.
