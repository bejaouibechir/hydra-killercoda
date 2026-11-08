# Run a total within each month

Cast amount to float. Partition by month and order by id; `cumsum` grows within each month and restarts in the next.

Study the reference, place it in this stage's job, run Hydra, and inspect the result. You can edit the YAML before running.

```bash
cd /root/lab/window-functions
cat /root/lab/lab14-resources/stage3.yaml
cp /root/lab/lab14-resources/stage3.yaml jobs/stage3/transformations.yaml
hdrctl run jobs/stage3
cat output/stage3/result.csv
```

Press **Check** after comparing the output with the input file and your earlier stage snapshots.
