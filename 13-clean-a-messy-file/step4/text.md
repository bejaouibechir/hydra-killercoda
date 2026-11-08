# Fill the missing amount

First cast `amount` to a number so the CSV empty string becomes a missing numeric value. Then `fill_null` sets only that missing `amount` to 0. Four records remain.

Read the stage template, then put its YAML in `job/transformations.yaml`. You may edit the file directly; the template gives a working reference.

```bash
cat /root/lab/lab13-resources/stage4.yaml
cp /root/lab/lab13-resources/stage4.yaml job/transformations.yaml
hdrctl run job
cat output/result.csv
```

Compare the output with the input and the previous checked snapshot in `evidence/`. Then press **Check**.
