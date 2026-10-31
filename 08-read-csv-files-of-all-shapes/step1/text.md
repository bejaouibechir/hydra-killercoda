# Read the comma-separated file

Start in the lab folder:

`cd /root/lab/csv-shapes && cat jobs/comma/sources.yaml`{{exec}}

The source uses `connection: {}`: the default separator is a comma and the default encoding is UTF-8.

`cat data/orders-comma.csv`{{exec}}

Run the job:

`hdrctl run jobs/comma`{{exec}}

Inspect the result as CSV, rather than just looking at the text:

`python3 ../lab08-resources/lab08.py inspect comma`{{exec}}

Expect **three columns** (`id`, `customer`, `city`) and **three data rows**. The customer names contain accented characters.

There is no `transformations.yaml`: the job copies the data. The destination writes UTF-8 with commas and `mode: replace`.

`cat jobs/comma/destinations.yaml && cat jobs/comma/pipeline.yaml`{{exec}}

Paths in these manifests are relative to their job folder. `../../data/` points to the shared input folder.

Click **Check** to verify the settings and every output value.
