# Keep the latest order per customer

Order IDs descending within each customer, assign `row_number`, then filter to number 1. The latest IDs are 6, 5, and 4.

Study the reference, place it in this stage's job, run Hydra, and inspect the result. You can edit the YAML before running.

```bash
cd /root/lab/window-functions
cat /root/lab/lab14-resources/stage2.yaml
cp /root/lab/lab14-resources/stage2.yaml jobs/stage2/transformations.yaml
hdrctl run jobs/stage2
cat output/stage2/result.csv
```

Press **Check** after comparing the output with the input file and your earlier stage snapshots.
