# Number each customer’s orders

Partition by customer_id and order by id. `row_number` starts at 1 in each partition. All six rows remain.

Study the reference, place it in this stage's job, run Hydra, and inspect the result. You can edit the YAML before running.

```bash
cd /root/lab/window-functions
cat /root/lab/lab14-resources/stage1.yaml
cp /root/lab/lab14-resources/stage1.yaml jobs/stage1/transformations.yaml
hdrctl run jobs/stage1
cat output/stage1/result.csv
```

Press **Check** after comparing the output with the input file and your earlier stage snapshots.
