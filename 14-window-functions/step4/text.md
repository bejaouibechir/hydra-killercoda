# Calculate each country share

Cast amount to float. `sum` covers all rows in each country; calculate each amount divided by that country total.

Study the reference, place it in this stage's job, run Hydra, and inspect the result. You can edit the YAML before running.

```bash
cd /root/lab/window-functions
cat /root/lab/lab14-resources/stage4.yaml
cp /root/lab/lab14-resources/stage4.yaml jobs/stage4/transformations.yaml
hdrctl run jobs/stage4
cat output/stage4/result.csv
```

Press **Check** after comparing the output with the input file and your earlier stage snapshots.
